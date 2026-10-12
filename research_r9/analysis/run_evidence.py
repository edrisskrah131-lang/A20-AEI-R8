"""Conservative evidence-scope amendment before selection/confirmation freeze.

Numerical generation and event labels are unchanged. The sampled capture and
motion providers are explicit dependencies of every requested quantity.
"""
from pathlib import Path
import sys,json
from types import MappingProxyType
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
import task_requirements as tr
from event_semantics import Atom,Event,Card,cp_upper
from prospective_protocol import sha,verify
from runtime import HERE
import evidence_selection as es

def apply_overlay():
    enriched={m:tuple(sorted(set(fields)|{'capture_sampler','motion_sampler','geometry_sampler'}))
              for m,fields in tr.DEPENDENCIES.items()}
    tr.DEPENDENCIES=MappingProxyType(enriched)

def preflight():
    verify();clock={'A':{'total_s':.0625},'B':{'total_s':.125}}
    old_spec=tr.DEPENDENCIES
    before={}
    for task in tr.TASKS:
        for variant in tr.VARIANTS:
            event=tr.requirement(task,variant)
            a=tr.context('A','Fixed2','relaxed',clock);b=tr.context('B','Fixed2','relaxed',clock)
            before[task,variant]=tr.event_capsule(event,a)==tr.event_capsule(event,b)
    apply_overlay();tested=0
    for key,invariant in before.items():
        event=tr.requirement(*key);a=tr.context('A','Fixed2','relaxed',clock);b=tr.context('B','Fixed2','relaxed',clock)
        assert invariant==(tr.event_capsule(event,a)==tr.event_capsule(event,b))
        for field in ('capture_sampler','motion_sampler','geometry_sampler'):
            altered={**a,field:'EXCLUDED_FAULT_FIXTURE_CHANGED_PROVIDER'}
            assert tr.event_capsule(event,a)!=tr.event_capsule(event,altered);tested+=1
    raw={s:sha(HERE/'data'/s/'calibration/manifest.json') for s in ('A','B')}
    audit=dict(status='PASS',scope_only_amendment=True,formal_confirmation_inputs=0,
        canonical_A_B_invariance_decisions_unchanged=True,provider_fault_checks=tested,
        old_dependencies={k:list(v) for k,v in old_spec.items()},
        amended_dependencies={k:list(v) for k,v in tr.DEPENDENCIES.items()},
        calibration_manifests=raw,numerical_generator_changed=False,event_labels_changed=False,
        rationale='Capture/motion sampling affects planned target addresses and physical pose; '
                  'conservative source-provider dependencies prevent unsupported transfers.')
    (HERE/'audits/attachment_scope_amendment.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    print('SCOPE_AMENDMENT_PASS',tested,flush=True)

def main():
    preflight()
    if '--calibrate' in sys.argv:
        es.calibrate()
        binding=dict(version='R9-evidence-scope-1',F0_sha256=sha(HERE/'protocol/freeze.json'),
            F1_sha256=sha(HERE/'protocol/selection_freeze.json'),
            files={'analysis/run_evidence.py':sha(__file__),
                   'audits/attachment_scope_amendment.json':sha(HERE/'audits/attachment_scope_amendment.json')},
            confirmation_inputs_before_binding=0)
        (HERE/'protocol/attachment_scope_binding.json').write_text(json.dumps(binding,indent=2),encoding='utf-8')

if __name__=='__main__':main()
