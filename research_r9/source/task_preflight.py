"""Pre-freeze assertions use marked fixtures, never empirical calibration cards."""
import json,itertools
from event_semantics import cp_upper,digest,Atom
from task_requirements import TASKS,VARIANTS,ANCHORS,requirement,context,event_capsule,DEPENDENCIES
from evidence_selection import candidate,METHODS
from runtime import HERE

def main():
    clock={'A':{'total_s':.0625},'B':{'total_s':.125}}
    old=context('A','Fixed2','relaxed',clock);new=context('B','Fixed2','relaxed',clock)
    checks=[]
    # Counts below are schema fixtures only. They do not enter any real study.
    for task in TASKS:
      for anchor_name in ANCHORS:
        anchor=requirement(task,anchor_name)
        fixture=dict(atoms=[(a.metric,a.lower,a.upper) for a in anchor.atoms],event_id=anchor.identity,
            producer_id=event_capsule(anchor,old),population_id='nominal',calibration_manifest='FIXTURE_ONLY',
            n=2048,k=100,alpha=.05/4608,upper=cp_upper(100,2048,.05/4608),
            context=old,variant=anchor_name,id='FIXTURE/'+task+'/'+anchor_name)
        for variant in VARIANTS:
            requested=requirement(task,variant)
            for ctx in (old,new):
                a=candidate(fixture,requested,'ContractCover',ctx,'nominal',.15)
                b=candidate(fixture,requested,'ProceduralCoverValidated',ctx,'nominal',.15)
                assert bool(a)==bool(b)
                assert candidate(fixture,requested,'ContractCover',ctx,'unfitted',.15) is None
                corrupted={**fixture,'upper':0.}
                assert candidate(corrupted,requested,'ContractCover',ctx,'nominal',.15) is None
                checks.append(dict(task=task,anchor=anchor_name,variant=variant,
                    roi_changed=ctx is new,authorized=bool(a)))
    optical=requirement('acquisition','single_service')
    assert event_capsule(optical,old)==event_capsule(optical,new)
    changed={**new,'focal_px':900.}
    assert event_capsule(optical,old)!=event_capsule(optical,changed)
    complete=requirement('report','full')
    assert event_capsule(complete,old)!=event_capsule(complete,new)
    try:Atom.quantity('gsd_m','mm',upper=True)
    except ValueError:pass
    else:raise AssertionError('Boolean quantity passed typed compiler')
    # All declared metric dependency sets contain the values their pure labels
    # access. The actual paired raster invariance is checked separately.
    for task in TASKS:
        for variant in VARIANTS:
            event_capsule(requirement(task,variant),old)
    audit=dict(status='PASS',fixtures_not_observations=True,schema_decisions=len(checks),
               semantic_procedural_agreement=True,wrong_population_refused=True,
               corrupted_card_refused=True,optical_ROI_invariance=True,
               focal_change_invalidates_optical=True,full_report_ROI_change_invalidates=True,
               formal_calibration_inputs=0,formal_confirmation_inputs=0,decisions=checks)
    (HERE/'audits/task_preflight.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in audit.items() if k!='decisions'}),flush=True)

if __name__=='__main__':main()
