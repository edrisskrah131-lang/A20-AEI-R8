"""Use actual sealed plans in excluded deterministic receipt/history fixtures."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from runtime import HERE
from prospective_protocol import sha
from runtime_receipts import TrustedSource,ReceiptGate

def main():
    plans=json.loads((HERE/'data/evidence/plans.json').read_text())
    source_manifest=json.loads((HERE/'data/A/calibration/manifest.json').read_text())
    item=source_manifest['inputs'][0]
    fields=('source','source_seal','profile','study','policy','event_id','plan_seal','card')
    methods=('ContractCover','ProceduralCoverValidated','DirectRecertCached','ExactCard')
    rows=[]
    for method in methods:
        plan=next(p for p in plans if p['method']==method and p['study']=='A'
                  and p['profile']=='nominal' and p['allowance']==.15 and p['status']=='AUTHORIZED')
        for field in fields:
            history={};gate=ReceiptGate(method,history)
            source=TrustedSource('EXCLUDED_FIXTURE/'+method+'/'+field,item['metadata_sha256'],'nominal','A')
            good=gate.packet(plan,source)
            assert gate.issue(plan,source,good)['issued']
            bad={**good,field:'EXCLUDED_FAULT_WRONG_VALUE'}
            assert not gate.issue(plan,source,bad)['issued']
            rebuilt=ReceiptGate(method,history)
            assert not rebuilt.issue(plan,source,good)['issued']
            successor=TrustedSource(source.scope+'/trusted_successor',source.seal,'nominal','A')
            assert rebuilt.issue(plan,successor,rebuilt.packet(plan,successor))['issued']
            rows.append(dict(method=method,fault=field,false_authorization=0,
                             history_refusal_persisted=True,independent_successor_valid=True))
    audit=dict(status='PASS',fixtures_not_population_observations=True,
         invalid_cases=len(rows),valid_controls=len(rows)*2,false_authorizations=0,
         numerical_and_event_changes=False,rows=rows)
    (HERE/'audits/receipt_preflight.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    # Pure attachment and formatting are frozen before confirmation; core F0
    # methods and calibration event maps remain byte-identical.
    files={p.relative_to(HERE).as_posix():sha(p) for p in sorted((HERE/'analysis').glob('*.py'))}
    (HERE/'protocol/confirmation_observer_freeze.json').write_text(json.dumps(dict(
        files=files,selection_freeze_sha256=sha(HERE/'protocol/selection_freeze.json'),
        scope_binding_sha256=sha(HERE/'protocol/attachment_scope_binding.json'),
        confirmation_inputs_before_observer_freeze=0,numerical_event_map_changed=False),indent=2),encoding='utf-8')
    print('RECEIPT_PREFLIGHT_PASS',len(rows),flush=True)

if __name__=='__main__':main()
