"""Freeze executable study A and predeclared ROI intervention B before data."""
import json,hashlib,sys
from pathlib import Path
from runtime import HERE,R8
from task_requirements import TASKS,VARIANTS,ANCHORS,POLICIES,requirement,ALLOWANCES

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def draft():
    return dict(version='R9-prospective-1',status='FROZEN_BEFORE_FORMAL_CALIBRATION',
      studies={'A':{'roi':[192,144]},'B':{'roi':[288,216]}},
      counts={'calibration_per_population':2048,'confirmation_per_population':1024,'stress_per_profile':64},
      seeds={'A':{'nominal_calibration':13000000,'unfitted_calibration':13100000,
                  'nominal_confirmation':13200000,'unfitted_confirmation':13300000,'stress':13400000},
             'B':{'nominal_calibration':14000000,'unfitted_calibration':14100000,
                  'nominal_confirmation':14200000,'unfitted_confirmation':14300000,'stress':14400000}},
      pilot_seeds=list(range(12000000,12000048)),pilot_excluded=True,
      policies=list(POLICIES),tasks=list(TASKS),variants=list(VARIANTS),anchors=list(ANCHORS),
      events={t:{v:[(a.metric,a.lower,a.upper) for a in requirement(t,v).atoms] for v in VARIANTS} for t in TASKS},
      primary_allowance=.15,allowances=list(ALLOWANCES),family_alpha=.05,family_size=4608,
      family_note='Reserve both studies, two populations, 32 policy/services and up to 36 events per cell. '
                  'Anchor duplicates need no extra cards; unused budget is not reassigned.',
      selection_objective='mean calibration loss_m2s + 1 m2 * mean normalized total_work_s',
      selection_tie='lexicographic (objective, policy ID)',
      calibration='Fresh independent draws; no fitting of retained R8 predictor. Exact CP upper with alpha=.05/4608.',
      confirmation='No input generated or inspected until ALL A/B calibration cards and choices sealed.',
      timing='R8 retained deterministic operation clock for localization. Pilot median camera+decoder CPU times '
             'frozen separately for each ROI, multiplied by the same declared service load. '
             'Synthetic report delay=max(first positive localization delivery,capture time+queue+load*camera work). '
             'Image age=report time-capture time. Native Windows timing is quantized; not embedded WCET.',
      scoring='Camera pixels actually raycast and processed by synthetic palette detector. '
              'Geotag uses the causally active positive localization version at capture. '
              'Source truth only enters rendering and offline event labels. Fixed-target GSD uses identical '
              'face/barycentric CAD addresses across ROI; it is not a frame-dependent pixel quantile.',
      producer_transfer='Target-event dependency closure unchanged plus pointwise old-anchor cover. '
                        'Only implemented pure program invariants, no OOD or real distribution claim.',
      pooled_calibration='Only predeclared A/B requests with identical pure event dependencies may pool '
                         'the independent same-population calibration draws. All baselines receive the same '
                         'pool and pooled anchors; full raw-manifest lineage is retained.',
      baselines=['ContractCover','ProceduralCoverValidated','DirectRecertCached','ExactCard'],
      baseline_fairness='All methods receive all card/data/request caches, dependency knowledge and same objective/alpha. '
                        'Direct renewal evaluates any predeclared request. Procedural cover implements all semantic/dependency rules.',
      stress_profiles=['occlusion','degeneracy','prior_shift','map_shift'],stress_certificates=False,
      primary_inference='Independent seed is sampling unit; per-request repetitions do not increase n. '
                        'Confirmation per-population empirical failures and exact intervals. '
                        'Paired Contract-Procedural equality; Contract-Direct differences retained.',
      human_effort_claim=False,physical_trials=0,route_guarantee=False)

def freeze():
    import numpy as np
    root=HERE/'data';root.mkdir(exist_ok=True)
    target=HERE/'protocol/freeze.json'
    if target.exists():raise RuntimeError('Freeze exists; verify instead of overwrite')
    if list(root.glob('[AB]/*/*')):raise RuntimeError('Formal data exists before freeze')
    pilot=HERE/'data/pilot_v4'
    records=[json.loads(p.read_text()) for p in sorted(pilot.glob('12*.json'))]
    if len(records)!=48:raise RuntimeError('Complete excluded pilot required')
    clock={}
    for study,producer in [('A','native_roi'),('B','wide_roi')]:
        camera=[a for r in records for a in r['cameras'] if a['producer']==producer]
        render=float(np.median([a['cpu_s'] for a in camera]))
        detect=float(np.median([a['detect_cpu_s'] for a in camera]))
        clock[study]=dict(render_s=render,detector_s=detect,total_s=render+detect,
                          pilot_manifest_sha256=sha(pilot/'manifest.json'))
    protocol=draft();protocol['camera_clock']=clock
    (HERE/'protocol/protocol.json').write_text(json.dumps(protocol,indent=2,ensure_ascii=False),encoding='utf-8')
    files={str(p.relative_to(HERE)):sha(p) for p in sorted((HERE/'source').glob('*.py'))
           if p.name not in ('github_backup.py','checkpoint_archive.py')}
    files['native/bvh_windows.dll']=sha(HERE/'native/bvh_windows.dll')
    components={str(p.relative_to(R8)):sha(p) for p in sorted((R8/'source').glob('*.py'))}
    for folder in ['data/r4_final','data/r8_final/geometry']:
        for p in sorted((R8/folder).glob('*.npz')):components[str(p.relative_to(R8))]=sha(p)
    for rel in ['data/checkpoint_model.npz','data/r4_final/freeze.json',
                'data/r8_final/clock_profile.json','data/r8_final/runtime_bindings.json']:
        components[rel]=sha(R8/rel)
    from r8_geometry import geometry,route
    from r8_protocol import A19
    def asset_name(p):
        try:return 'r8:'+str(p.relative_to(R8)).replace('\\','/')
        except ValueError:return 'a19:'+str(p.relative_to(A19)).replace('\\','/')
    assets={asset_name(p):sha(p) for m in ('B767','C172','UnfittedAirframe')
            for p in [route(m),*[geometry(m,i) for i in range(4)]]}
    for p in sorted((A19/'source').rglob('*')):
        if p.is_file() and p.suffix in ('.py','.cpp'):
            assets[asset_name(p)]=sha(p)
    target.write_text(json.dumps(dict(protocol_sha256=sha(HERE/'protocol/protocol.json'),
        files=files,r8_components=components,assets=assets,formal_inputs_before_freeze=0),indent=2),encoding='utf-8')
    print('FROZEN',sha(target),clock,flush=True)

def verify():
    freeze=json.loads((HERE/'protocol/freeze.json').read_text())
    if sha(HERE/'protocol/protocol.json')!=freeze['protocol_sha256']:raise RuntimeError('Protocol changed')
    for p,h in freeze['files'].items():
        if sha(HERE/p)!=h:raise RuntimeError('Frozen executable changed: '+p)
    for p,h in freeze['r8_components'].items():
        if sha(R8/p)!=h:raise RuntimeError('Retained R8 component changed: '+p)
    for p,h in freeze['assets'].items():
        from r8_protocol import A19
        family,relative=p.split(':',1)
        if sha((R8 if family=='r8' else A19)/relative)!=h:raise RuntimeError('Retained asset changed: '+p)
    return json.loads((HERE/'protocol/protocol.json').read_text())

if __name__=='__main__':freeze() if '--freeze' in sys.argv else print(verify()['version'])
