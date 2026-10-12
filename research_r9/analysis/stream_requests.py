"""Bounded-memory output formatting of the frozen confirmation procedure.

No calibration, plan choice, event definition or producer is changed here.
One compiled before-sensing plan is repeated across its independent sources.
"""
from pathlib import Path
import sys,json,gzip,csv,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from evidence_selection import read_phase,metrics
from task_requirements import requirement
from prospective_protocol import verify,sha
from runtime import HERE
from run_evidence import apply_overlay
from runtime_receipts import TrustedSource,ReceiptGate

def main(study):
    verify();apply_overlay();frame,manifest=read_phase(study,'confirmation')
    seal=json.loads((HERE/'protocol/selection_freeze.json').read_text())
    for p,h in seal['files'].items():
        if sha(HERE/p)!=h:raise RuntimeError('Changed sealed evidence: '+p)
    plans=json.loads((HERE/'data/evidence/plans.json').read_text())
    trusted={item['seed']:TrustedSource(f'{study}/confirmation/{item["profile"]}/{item["seed"]}',
                item['metadata_sha256'],item['profile'],study) for item in manifest['inputs']}
    gates={m:ReceiptGate(m) for m in ('ContractCover','ProceduralCoverValidated','DirectRecertCached','ExactCard')}
    gate_wall={m:0. for m in gates}
    checks={m:0 for m in gates}
    lookup={(profile,service,policy):f.sort_values('seed').set_index('seed')
            for (profile,service,policy),f in frame.groupby(['profile','service','policy'])}
    seeds={profile:sorted(frame.loc[frame['profile']==profile,'seed'].unique()) for profile in ('nominal','unfitted')}
    fields=['study','profile','service','task','variant','method','allowance','status','policy','upper',
            'seed','failure','authorized','margin','rmse_m','loss_m2s','total_work_s','report_delay_s','image_age_s']
    target=HERE/'data'/study/'confirmation/requests.csv.gz';count=0
    with gzip.open(target,'wt',newline='',encoding='utf-8') as output:
        writer=csv.DictWriter(output,fieldnames=fields);writer.writeheader()
        for i,plan in enumerate(q for q in plans if q['study']==study):
            base={k:plan[k] for k in fields[:10]}
            if plan['status']=='AUTHORIZED':
                selected=lookup[plan['profile'],plan['service'],plan['policy']]
                failed=requirement(plan['task'],plan['variant']).failure(metrics(selected))
                for j,(seed,row) in enumerate(selected.iterrows()):
                    source=trusted[int(seed)];gate=gates[plan['method']]
                    packet=gate.packet(plan,source);begin=time.perf_counter_ns()
                    receipt=gate.issue(plan,source,packet)
                    gate_wall[plan['method']]+=(time.perf_counter_ns()-begin)*1e-9
                    checks[plan['method']]+=1
                    if not receipt['issued']:raise RuntimeError('Canonical source unexpectedly lost its receipt')
                    writer.writerow(dict(**base,seed=int(seed),failure=int(failed[j]),authorized=1,
                        margin=plan['allowance']-plan['upper'],**{k:row[k] for k in fields[14:]}));count+=1
            else:
                for seed in seeds[plan['profile']]:
                    writer.writerow(dict(**base,seed=int(seed),failure=None,authorized=0,margin=None,
                        **{k:None for k in fields[14:]}));count+=1
            if (i+1)%256==0:print('REQUEST_STREAM',study,i+1,count,flush=True)
    expected=sum(len(seeds[q['profile']]) for q in plans if q['study']==study)
    if count!=expected:raise RuntimeError('Request repetition denominator differs')
    audit=dict(study=study,rows=count,independent_confirmation_sources=manifest['unique_inputs'],
               formatter='stream of frozen evidence_selection.confirm fields and predicates',
               changed_methods=False,source_bound_receipt_checks=checks,
               measured_receipt_wall_s=gate_wall,sha256=sha(target))
    (HERE/'audits'/f'{study}_request_stream.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    print('REQUEST_STREAM_COMPLETE',study,count,flush=True)

if __name__=='__main__':main(sys.argv[-1])
