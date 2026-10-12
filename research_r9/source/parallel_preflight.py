"""Excluded execution fixtures, testing worker isolation and resumable arrays."""
from concurrent.futures import ProcessPoolExecutor
from collect_study import execute,init_worker
from prospective_protocol import draft
from runtime import HERE
import json

def main():
    p=draft();p['camera_clock']={'A':{'total_s':.0625},'B':{'total_s':.125}}
    cases=[('A','nominal',12000002),('B','unfitted',12000003),
           ('A','occlusion',12000004),('B','map_shift',12000005)]
    jobs=[(s,'excluded_parallel_preflight',profile,seed,
           str(HERE/'data/parallel_preflight'/s/profile),p) for s,profile,seed in cases]
    with ProcessPoolExecutor(max_workers=2,initializer=init_worker) as pool:
        results=list(pool.map(execute,jobs))
    assert all(len(r['outcomes'])==32 and len(r['execution_traces'])==32 for r in results)
    # The second invocation really reads and verifies the saved raw archives.
    with ProcessPoolExecutor(max_workers=2,initializer=init_worker) as pool:
        resumed=list(pool.map(execute,jobs))
    assert [r['files'] for r in results]==[r['files'] for r in resumed]
    audit=dict(status='PASS',excluded_fixtures=True,formal_inputs_generated=0,
               worker_count=2,resume_raw_hashes_verified=True,
               cases=[dict(study=r['study'],profile=r['source']['profile'],seed=r['source']['seed'],
                           outcomes=len(r['outcomes']),files=r['files']) for r in results])
    (HERE/'audits/parallel_preflight.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in audit.items() if k!='cases'}),flush=True)

if __name__=='__main__':main()
