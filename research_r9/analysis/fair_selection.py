"""Pre-confirmation knowledge-parity amendment for cached exact-event renewal.

Keep F0 generation and card counts unchanged. The direct baseline may use any
old exact-event card with unchanged requested dependencies, like every method.
"""
from pathlib import Path
import sys,json,shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from runtime import HERE
from prospective_protocol import verify,sha
import evidence_selection as es
import run_evidence as re
from task_requirements import POLICIES,context,requirement

original=es.build_plan
def strengthened(cards,objectives,study,profile,service,task,variant,method,allowance,p):
    if method!='DirectRecertCached':
        return original(cards,objectives,study,profile,service,task,variant,method,allowance,p)
    target=requirement(task,variant);choices=[]
    for policy in POLICIES:
        ctx=context(study,policy,service,p['camera_clock']);admitted=[]
        for card in cards:
            if (card['profile'],card['service'],card['policy'])!=(profile,service,policy):continue
            if study=='A' and card['study']!='A':continue
            valid=es.candidate(card,target,method,ctx,profile,allowance)
            if valid is not None:admitted.append(valid)
        if admitted:
            proof=min(admitted,key=lambda x:(x['upper'],x['card']))
            choices.append((objectives[(study,profile,service,policy)],policy,proof))
    base=dict(study=study,profile=profile,service=service,task=task,variant=variant,
              method=method,allowance=allowance,event_id=target.identity)
    if not choices:return dict(**base,status='REFUSED',policy=None,upper=None)
    objective,policy,proof=min(choices,key=lambda x:(x[0],x[1]))
    return dict(**base,status='AUTHORIZED',policy=policy,objective=objective,**proof)

def main():
    verify()
    assert not any((HERE/'data'/s/'confirmation').exists() for s in ('A','B'))
    archive=HERE/'protocol/history_F1_before_direct_parity'
    if archive.exists():raise RuntimeError('Preserve the first amendment execution; do not overwrite history')
    archive.mkdir()
    paths=['protocol/selection_freeze.json','protocol/attachment_scope_binding.json',
           'protocol/confirmation_observer_freeze.json','data/evidence/cards.json',
           'data/evidence/plans.json','data/evidence/calibration_preparation.csv',
           'audits/attachment_scope_amendment.json','audits/receipt_preflight.json']
    for rel in paths:
        dest=archive/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(HERE/rel,dest)
    old=json.loads((HERE/'data/evidence/plans.json').read_text())
    re.preflight();es.build_plan=strengthened;es.calibrate()
    new=json.loads((HERE/'data/evidence/plans.json').read_text())
    assert len(new)==len(old)
    changes=0
    for before,after in zip(old,new):
        if before['method']!='DirectRecertCached':assert before==after
        else:
            if before['status']=='AUTHORIZED':assert after['status']=='AUTHORIZED'
            changes+=before!=after
    audit=dict(status='PASS',confirmation_inputs_before_amendment=0,
        numerical_generator_changed=False,event_labels_changed=False,calibration_counts_changed=False,
        change='Permit applicable A exact-event cards in B direct-renewal candidates.',
        methods_except_direct_bitwise_unchanged=True,direct_old_support_preserved=True,
        changed_direct_plans=changes,old_F1_sha256=sha(archive/'protocol/selection_freeze.json'),
        F1_sha256=sha(HERE/'protocol/selection_freeze.json'),history=str(archive.relative_to(HERE)))
    (HERE/'audits/direct_parity_amendment.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    binding=dict(version='R9-evidence-scope-2-direct-parity',F0_sha256=sha(HERE/'protocol/freeze.json'),
        F1_sha256=sha(HERE/'protocol/selection_freeze.json'),confirmation_inputs_before_binding=0,
        files={rel:sha(HERE/rel) for rel in ['analysis/run_evidence.py','analysis/fair_selection.py',
          'audits/attachment_scope_amendment.json','audits/direct_parity_amendment.json']})
    (HERE/'protocol/attachment_scope_binding.json').write_text(json.dumps(binding,indent=2),encoding='utf-8')
    print('DIRECT_PARITY_AMENDMENT_PASS',changes,flush=True)

if __name__=='__main__':main()
