"""Five fixed source replays; replays never increase inferential sample size."""
from pathlib import Path
import sys,json
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from runtime import HERE
from prospective_protocol import verify,sha
from collect_study import init_worker,execute

SOURCES=(('A','nominal',13200000),('A','nominal',13201023),('A','unfitted',13300000),('B','nominal',14200000),('B','unfitted',14300000))
def main():
    p=verify();root=HERE/'verification/replays';root.mkdir(parents=True,exist_ok=True)
    (root/'selection.json').write_text(json.dumps(dict(selection='Fixed first/last A nominal and first A/B population sources before replay inspection',sources=SOURCES,additional_independent_inputs=0),indent=2),encoding='utf-8')
    init_worker();rows=[]
    for study,profile,seed in SOURCES:
        old=HERE/'data'/study/'confirmation'/profile
        assert (old/f'{seed}.json').is_file()
        dest=root/study/profile
        result=execute((study,'confirmation',profile,seed,str(dest),p))
        numeric_keys=0;max_difference=0.
        for name in (f'{seed}.npz',f'{seed}_camera.npz'):
            a=np.load(old/name);b=np.load(dest/name)
            assert set(a.files)==set(b.files)
            for key in a.files:
                if key in ('cpu_s','wall_s'):continue
                x,y=a[key],b[key]
                assert x.shape==y.shape,(name,key)
                if np.issubdtype(x.dtype,np.number):
                    assert np.allclose(x,y,rtol=0,atol=1e-12,equal_nan=True),(name,key)
                    finite=np.isfinite(x)&np.isfinite(y)
                    if finite.any():max_difference=max(max_difference,float(np.max(np.abs(x[finite]-y[finite]))))
                else:assert np.array_equal(x,y),(name,key)
                numeric_keys+=1
        prior=json.loads((old/f'{seed}.json').read_text())
        event_fields=('gsd_m','blur_px','coverage','reprojection_px','association_m','localization_ready','report_delay_s','image_age_s','rmse_m','loss_m2s','trajectory_failure','observation_failure','union_failure','stop_iteration','publications')
        for before,after in zip(prior['outcomes'],result['outcomes']):
            assert (before['policy'],before['service'])==(after['policy'],after['service'])
            for key in event_fields:
                if before[key] is None or after[key] is None:assert before[key]==after[key],key
                else:assert abs(float(before[key])-float(after[key]))<1e-12,(seed,key)
        rows.append(dict(study=study,profile=profile,seed=seed,status='PASS',array_keys=numeric_keys,max_absolute_difference=max_difference,policy_service_outcomes=32,source_sha256=sha(old/f'{seed}.json'),replay_sha256=sha(dest/f'{seed}.json'),timing_fields_excluded=True))
        print('SOURCE_REPLAY_PASS',study,seed,flush=True)
    (HERE/'audits/source_replay.json').write_text(json.dumps(dict(status='PASS',additional_independent_inputs=0,scope='Same platform cold numerical/pixel replay; native measured timings are not expected bitwise equal.',sources=rows),indent=2),encoding='utf-8')

if __name__=='__main__':main()
