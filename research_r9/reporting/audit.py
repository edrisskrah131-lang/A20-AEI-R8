"""Independent probability-inversion and complete executed-source audit."""
from pathlib import Path
import json,sys,math
from scipy.stats import binom
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from runtime import HERE
from prospective_protocol import verify,sha

def main():
 p=verify();cards=json.loads((HERE/'data/evidence/cards.json').read_text());errors=[]
 for c in cards:
  assert 0<=c['k']<=c['n'] and c['n'] in (2048,4096)
  if c['k']<c['n']:
   error=abs(float(binom.logcdf(c['k'],c['n'],c['upper']))-math.log(c['alpha']));errors.append(error)
   assert error<1e-8,(c['id'],error)
  else:assert c['upper']==1
 unique=set();phase_records=[];raw_files=0
 for study in ('A','B'):
  for phase in ('calibration','confirmation','stress'):
   root=HERE/'data'/study/phase;m=json.loads((root/'manifest.json').read_text())
   assert m['complete'] and sha(root/'outcomes.csv.gz')==m['result_sha256']
   for item in m['inputs']:
    seed=item['seed'];assert seed not in unique;unique.add(seed);base=root/item['profile']
    assert sha(base/f'{seed}.json')==item['metadata_sha256'];raw_files+=1
    for name,digest in item['files'].items():assert sha(base/name)==digest;raw_files+=1
   phase_records.append({k:m[k] for k in ('study','phase','unique_inputs','repeated_outcomes','wall_s')})
 assert len(unique)==12800 and sum(q['repeated_outcomes'] for q in phase_records)==409600
 rows=0
 for study in ('A','B'):
  a=json.loads((HERE/'audits'/f'{study}_request_stream.json').read_text())
  assert a['sha256']==sha(HERE/'data'/study/'confirmation/requests.csv.gz');assert a['rows']==3145728
  assert a['independent_confirmation_sources']==2048;rows+=a['rows']
 output=dict(status='PASS',independent_inputs=len(unique),raw_files_checked=raw_files,
   repeated_policy_service_outcomes=409600,repeated_confirmation_requests=rows,
   CP_independent_log_binomial_inversion_max_error=max(errors),phases=phase_records,
   observer_fixtures_not_probability_observations=True,hidden_drift_detection_claim=False)
 (HERE/'audits/final_execution_audit.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
 print('FINAL_EXECUTION_AUDIT_PASS',len(unique),raw_files,rows,max(errors),flush=True)

if __name__=='__main__':main()
