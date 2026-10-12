"""Differential, failure-closed and counterexample checks before any freeze."""
from pathlib import Path
import json
import numpy as np
from event_semantics import Atom, Event, Card, containment, procedural_contains, authorize, cp_upper

def main():
    rng = np.random.default_rng(202610129)
    checked = 0
    for _ in range(10000):
        hi = float(rng.uniform(.005,.2))
        lo = float(rng.uniform(.1,.8))
        anchor = Event((Atom('association_m',upper=hi),Atom('coverage',lower=lo)))
        target = Event((Atom('association_m',upper=hi*float(rng.uniform(.5,2))),
                        Atom('coverage',lower=lo*float(rng.uniform(.5,1.2)))))
        proof = containment(anchor,target)
        assert (proof is not None) == procedural_contains(anchor,target)
        values = {'association_m':rng.uniform(0,.3,100),'coverage':rng.uniform(0,1,100)}
        if proof is not None:
            assert not np.any(target.failure(values)&~anchor.failure(values))
        checked += 1
    anchor = Event((Atom.quantity('gsd_m','mm',upper=8.),))
    relaxed = Event((Atom.quantity('gsd_m','m',upper=.012),))
    assert containment(anchor,relaxed) is not None
    assert anchor.failure({'gsd_m':[np.inf,np.nan,.009,.008]}).tolist() == [True,True,True,False]
    for bad in [float('inf'),float('nan')]:
        try:
            Atom('gsd_m',upper=bad)
            raise AssertionError('Non-finite threshold accepted')
        except ValueError:
            pass
    try:
        Atom.quantity('gsd_m','ms',upper=2.)
        raise AssertionError('Incompatible unit accepted')
    except ValueError:
        pass
    card = Card(anchor.identity,'producer_A','population_A','cal_manifest',2048,10,
                .05/4096,cp_upper(10,2048,.05/4096))
    assert authorize(card,anchor,relaxed,'producer_A','population_A',.15)['status']=='AUTHORIZED'
    assert authorize(card,anchor,relaxed,'producer_B','population_A',.15)['status']=='REFUSED'
    assert authorize(card,anchor,relaxed,'producer_A','population_B',.15)['status']=='REFUSED'
    assert authorize(card,anchor,relaxed,'producer_A','population_A',.15,True)['status']=='REFUSED'
    # Online switching between two individually safe events can double failure risk.
    a = np.arange(1000)<100
    b = (np.arange(1000)>=100)&(np.arange(1000)<200)
    assert a.mean()==b.mean()==.1 and (a|b).mean()==.2
    result = {'status':'PASS','random_event_pairs':checked,'metric_vectors_checked':checked*100,
              'procedural_witness_agreement':True,'nonfinite_failure_closed':True,
              'unit_mismatch_rejected':True,'producer_population_mismatch_rejected':True,
              'adaptive_anchor_counterexample':{'marginal_A':.1,'marginal_B':.1,'union':.2},
              'formal_calibration_inputs_generated':0,'formal_confirmation_inputs_generated':0}
    out = Path(__file__).resolve().parents[1]/'audits/semantic_preflight.json'
    out.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result),flush=True)

if __name__=='__main__':
    main()
