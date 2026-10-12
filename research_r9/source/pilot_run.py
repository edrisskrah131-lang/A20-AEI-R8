"""Excluded pilot, actual retained solver and synthetic camera execution."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import argparse, json, time, hashlib
from pathlib import Path
import numpy as np
from PIL import Image
from runtime import HERE, initialize
from camera_renderer import render
from target_metrics import plan_targets, target_geometry, score_image, score_association, planned_gimbal
from r8_protocol import PROTOCOL

def run(n):
    rt = initialize()
    folder = HERE/'data/pilot_v2'
    folder.mkdir(parents=True, exist_ok=True)
    start=time.perf_counter()
    records=[]
    for i in range(n):
        seed=12000000+i
        profile='nominal' if i%2==0 else 'unfitted'
        rec=rt['generate'](seed, 'r9_excluded_pilot', profile, rt['meshes'], rt['routes'], folder)
        z=np.load(folder/f'{seed}.npz')
        capture_tick=int(np.random.default_rng(seed+50000000).integers(1,4))
        capture_pose=z['future_truth'][capture_tick]
        planned=rt['routes'][rec['mesh']][rec['frame']+capture_tick]
        gimbal=planned_gimbal(rt['meshes'][rec['mesh'],0],planned,rt['exp'])
        targets=plan_targets(rt['meshes'][rec['mesh'],0],planned,rt['exp'],gimbal_R=gimbal)
        speed=np.linalg.norm(z['future_truth'][capture_tick,:3]-z['future_truth'][capture_tick-1,:3])/.1
        geometry=target_geometry(rt['meshes'][rec['mesh'],rec['level']], targets,capture_pose,
                                 z['map_t'],z['map_R'],rt['exp'],1800.,speed,.006,gimbal)
        cache=rt['prediction_cache'](rec,rt['models'])
        observations=[]
        camera_records=[]
        for producer,width,height in [('native_roi',192,144),('wide_roi',288,216)]:
            frame=render(rt['meshes'][rec['mesh'],rec['level']],capture_pose,z['map_t'],z['map_R'],
                         np.random.default_rng(seed+60000000),rt['exp'],width,height,1800.,.006,speed,gimbal)
            np.savez_compressed(folder/f'{seed}_{producer}.npz',**{k:v for k,v in frame.items() if k not in ('model',) },
                                target_faces=targets['faces'],target_bary=targets['bary'],target_cad=targets['cad_points'],
                                target_gsd=geometry['gsd'],target_xy=geometry['xy'])
            if i<4:Image.fromarray(frame['rgb']).save(folder/f'{seed}_{producer}.png')
            image=score_image(frame,geometry,width,height)
            camera_records.append(dict(producer=producer,cpu_s=frame['cpu_s'],**image))
            for service in PROTOCOL['services']:
                for policy in rt['policies']:
                    out=rt['controlled'](rec,z,policy,cache,rt['clock'],service,rt['bindings'])
                    journal=json.loads(out['trace'])['installations']
                    # Explicitly find source indices from the policy's publication
                    # decision and installed versions; no future version at capture.
                    active=0
                    installed=sorted([j for j in journal if 'tick' in j and j['tick']<=capture_tick and not j.get('refused')],key=lambda j:(j['tick'],j['sequence']))
                    if installed:
                        last=installed[-1]
                        it=last['active_iteration']
                        active=next((a+1 for a,s in enumerate(rec['trace']) if s['iteration']==it),0)
                    state=rt['state_from'](z,active)
                    for t in range(capture_tick):state=rt['propagate'](state,.1,z['increment'][t])
                    assoc=score_association(state,targets,geometry,rt['exp'],width,height,1800.,gimbal)
                    observations.append(dict(producer=producer,policy=policy['id'],service=service['id'],
                                             active_index=active,capture_tick=capture_tick,**assoc,
                                             rmse_m=out['rmse_m'],work_s=out['work_s'],
                                             first_delivery_s=out['first_delivery_s']))
        record=dict(seed=seed,mesh=rec['mesh'],profile=profile,level=rec['level'],
                    capture_tick=capture_tick,speed_m_s=float(speed),cameras=camera_records,
                    outcomes=observations,source=rec)
        records.append(record)
        # Nonfinite scores have a defined failure meaning; JSON uses null and
        # an explicit nonfinite field list rather than non-standard Infinity.
        def clean(v):
            if isinstance(v,float) and not np.isfinite(v):return None
            if isinstance(v,list):return [clean(a) for a in v]
            if isinstance(v,dict):return {k:clean(a) for k,a in v.items()}
            return v
        (folder/f'{seed}.json').write_text(json.dumps(clean(record),ensure_ascii=False,allow_nan=False),encoding='utf-8')
        print('PILOT',i+1,n,rec['mesh'],'targets',camera_records[0]['targets'],
              'coverage',round(camera_records[0]['coverage'],3),round(camera_records[1]['coverage'],3),
              'gsd',camera_records[0]['gsd_m'],'seconds',round(time.perf_counter()-start,1),flush=True)
    manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.glob('*')) if p.is_file() and p.name!='manifest.json'}
    (folder/'manifest.json').write_text(json.dumps(dict(excluded_from_calibration_confirmation=True,
        n=n,formal_inputs_generated=0,files=manifest,wall_s=time.perf_counter()-start),indent=2),encoding='utf-8')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=48);args=ap.parse_args();run(args.n)
