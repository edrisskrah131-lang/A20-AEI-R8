"""Resumable real simulation blocks; separate raw input and repeated outcomes."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import argparse,json,gzip,csv,time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from runtime import HERE,initialize
from prospective_protocol import verify,sha
from camera_renderer import render,detect_fiducials
from target_metrics import planned_gimbal,plan_targets,target_geometry,score_image,score_association
from r8_protocol import PROTOCOL as R8_PROTOCOL

RT=None
def init_worker():
    global RT
    RT=initialize()

def finite_json(value):
    if isinstance(value,float) and not np.isfinite(value):return None
    if isinstance(value,dict):return {k:finite_json(v) for k,v in value.items()}
    if isinstance(value,list):return [finite_json(v) for v in value]
    return value

def execute(job):
    study,phase,profile,seed,folder,protocol=job
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    meta=folder/f'{seed}.json'
    if meta.exists():
        existing=json.loads(meta.read_text())
        if existing['study']!=study or existing['source']['phase']!=phase or existing['source']['profile']!=profile:
            raise RuntimeError('Saved source identity differs from requested job')
        for file,digest in existing['files'].items():
            if sha(folder/file)!=digest:raise RuntimeError('Corrupt existing input: '+file)
        return existing
    r=RT['generate'](seed,phase,profile,RT['meshes'],RT['routes'],folder)
    z=np.load(folder/f'{seed}.npz')
    rng=np.random.default_rng(seed+50000000)
    tick=int(rng.integers(1,4));pose=z['future_truth'][tick]
    planned=RT['routes'][r['mesh']][r['frame']+tick]
    gimbal=planned_gimbal(RT['meshes'][r['mesh'],0],planned,RT['exp'])
    targets=plan_targets(RT['meshes'][r['mesh'],0],planned,RT['exp'],gimbal_R=gimbal)
    speed=float(np.linalg.norm(z['future_truth'][tick,:3]-z['future_truth'][tick-1,:3])/.1)
    geom=target_geometry(RT['meshes'][r['mesh'],r['level']],targets,pose,z['map_t'],z['map_R'],
                         RT['exp'],1800.,speed,.006,gimbal)
    width,height=protocol['studies'][study]['roi']
    frame=render(RT['meshes'][r['mesh'],r['level']],pose,z['map_t'],z['map_R'],
                 np.random.default_rng(seed+60000000),RT['exp'],width,height,1800.,.006,speed,gimbal,geom)
    detected,detect_cpu=detect_fiducials(frame['rgb'],len(targets['faces']))
    camera_file=folder/f'{seed}_camera.npz'
    np.savez_compressed(camera_file,**{k:v for k,v in frame.items() if k!='model'},
        target_faces=targets['faces'],target_bary=targets['bary'],target_cad=targets['cad_points'],
        target_world=geom['world'],target_gsd=geom['gsd'],target_xy=geom['xy'],
        detected_xy=detected,gimbal_R=gimbal,capture_tick=tick,speed_m_s=speed)
    image=score_image(frame,geom,width,height,detected)
    cache=RT['prediction_cache'](r,RT['models'])
    outcomes=[];execution_traces=[]
    for service in R8_PROTOCOL['services']:
        for policy in RT['policies']:
            out=RT['controlled'](r,z,policy,cache,RT['clock'],service,RT['bindings'])
            execution_traces.append(dict(policy=policy['id'],service=service['id'],
                actual_execution=json.loads(out['trace']),sender_total_work_s=out['sender_total_work_s'],
                normalized_work_s=out['work_s'],native_charged_cpu_s=out['native_charged_cpu_s']))
            journal=json.loads(out['trace'])['installations']
            arrived=sorted([j for j in journal if 'tick' in j and j['tick']<=tick and not j.get('refused')],
                           key=lambda j:(j['tick'],j['sequence']))
            active=0
            if arrived:
                it=arrived[-1]['active_iteration']
                active=next((a+1 for a,s in enumerate(r['trace']) if s['iteration']==it),0)
            state=RT['state_from'](z,active)
            for t in range(tick):state=RT['propagate'](state,.1,z['increment'][t])
            assoc=score_association(state,targets,geom,RT['exp'],width,height,1800.,gimbal,detected)
            camera_work=protocol['camera_clock'][study]['total_s']
            report_delay=max(out['first_delivery_s'],tick*.1+.05+service['load']*camera_work)
            # The report delivers the fixed capture-time association; later
            # localization cannot retrospectively count as capture-time ready.
            metrics=dict(**{k:image[k] for k in ('gsd_m','blur_px','coverage')},**assoc,
                         localization_ready=float(active>0),report_delay_s=report_delay,
                         image_age_s=report_delay-tick*.1)
            record=dict(study=study,seed=seed,phase=phase,profile=profile,mesh=r['mesh'],
                        capture_tick=tick,active_index=active,**metrics,
                        camera_cpu_s=frame['cpu_s'],detector_cpu_s=detect_cpu,
                        camera_work_s=camera_work, total_work_s=out['work_s']+camera_work,
                        total_native_cpu_s=out['native_charged_cpu_s']+frame['cpu_s']+detect_cpu,
                        **{k:out[k] for k in ['policy','service','load','rmse_m','p95_m','max_m',
                        'loss_m2s','capture_success','first_delivery_s','stop_iteration',
                        'publications','budget_stop','trajectory_failure','observation_failure','union_failure']})
            outcomes.append(record)
    record=dict(source=r,study=study,capture_tick=tick,speed_m_s=speed,
                image_model=frame['model'],image_metrics=finite_json(image),
                execution_traces=execution_traces,
                outcomes=finite_json(outcomes),files={f'{seed}.npz':sha(folder/f'{seed}.npz'),
                                                     camera_file.name:sha(camera_file)})
    meta.write_text(json.dumps(record,allow_nan=False,separators=(',',':')),encoding='utf-8')
    return record

def jobs_for(study,phase,p,folder):
    if phase in ('calibration','confirmation'):
        n=p['counts'][phase+'_per_population']
        for profile in ('nominal','unfitted'):
            base=p['seeds'][study][profile+'_'+phase]
            for i in range(n):yield study,phase,profile,base+i,str(folder/profile),p
    else:
        for k,profile in enumerate(p['stress_profiles']):
            base=p['seeds'][study]['stress']+k*1000
            for i in range(p['counts']['stress_per_profile']):yield study,phase,profile,base+i,str(folder/profile),p

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study',choices=['A','B'],required=True)
    ap.add_argument('--phase',choices=['calibration','confirmation','stress'],required=True)
    ap.add_argument('--workers',type=int,default=6);ap.add_argument('--limit',type=int)
    args=ap.parse_args();p=verify()
    if args.phase!='calibration':
        lock=HERE/'protocol/selection_freeze.json'
        if not lock.exists():raise RuntimeError('Seal all calibration cards and selections before confirmation/stress')
        seal=json.loads(lock.read_text())
        for name,h in seal['files'].items():
            if sha(HERE/name)!=h:raise RuntimeError('Selection artifact changed: '+name)
        # Verify the actual calibration inputs, not only their result tables.
        for study in ('A','B'):
            cal=HERE/'data'/study/'calibration'
            manifest=json.loads((cal/'manifest.json').read_text())
            for item in manifest['inputs']:
                base=cal/item['profile']
                if sha(base/f"{item['seed']}.json")!=item['metadata_sha256']:
                    raise RuntimeError('Changed raw calibration metadata')
                for name,h in item['files'].items():
                    if sha(base/name)!=h:raise RuntimeError('Changed raw calibration input: '+name)
    folder=HERE/'data'/args.study/args.phase;folder.mkdir(parents=True,exist_ok=True)
    jobs=list(jobs_for(args.study,args.phase,p,folder))
    if args.limit:jobs=jobs[:args.limit]
    begin=time.perf_counter();rows=[];inputs=[]
    with ProcessPoolExecutor(max_workers=args.workers,initializer=init_worker) as pool:
        for i,r in enumerate(pool.map(execute,jobs,chunksize=4)):
            inputs.append(dict(seed=r['source']['seed'],profile=r['source']['profile'],
                              files=r['files'],metadata_sha256=sha(folder/r['source']['profile']/f"{r['source']['seed']}.json")))
            for row in r['outcomes']:
                rows.append({k:(np.inf if v is None and k in ('gsd_m','blur_px','reprojection_px','association_m') else v)
                             for k,v in row.items()})
            if (i+1)%64==0:print('R9_EXECUTE',args.study,args.phase,i+1,len(jobs),round(time.perf_counter()-begin,1),flush=True)
    results=folder/'outcomes.csv.gz'
    with gzip.open(results,'wt',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    manifest=dict(study=args.study,phase=args.phase,unique_inputs=len(inputs),repeated_outcomes=len(rows),
                  inputs=inputs,result_sha256=sha(results),protocol_sha256=sha(HERE/'protocol/protocol.json'),
                  wall_s=time.perf_counter()-begin,complete=len(jobs)==len(list(jobs_for(args.study,args.phase,p,folder))))
    (folder/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print('R9_EXECUTE_DONE',args.study,args.phase,len(inputs),len(rows),round(manifest['wall_s'],1),flush=True)

if __name__=='__main__':main()
