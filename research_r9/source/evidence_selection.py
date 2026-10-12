"""Finite-family calibration and fair semantic/direct-renewal selection."""
import json,sys,time
from functools import lru_cache
from pathlib import Path
import numpy as np
import pandas as pd
from event_semantics import Event,Atom,Card,cp_upper,containment,procedural_contains,digest
from task_requirements import TASKS,VARIANTS,ANCHORS,POLICIES,ALLOWANCES,requirement,context,event_capsule,procedural_capsule_equal
from prospective_protocol import verify,sha
from runtime import HERE

METHODS=('ContractCover','ProceduralCoverValidated','DirectRecertCached','ExactCard')

@lru_cache(maxsize=8192)
def validated_numeric_card(card):
    # Card is an immutable value object. Changes in any field create a new
    # cache key and force the exact count/bound check again.
    return card.valid()

def metrics(frame):return {k:frame[k].to_numpy() for k in ('gsd_m','blur_px','coverage','reprojection_px',
                 'association_m','localization_ready','report_delay_s','image_age_s')}

def read_phase(study,phase):
    root=HERE/'data'/study/phase
    m=json.loads((root/'manifest.json').read_text())
    if not m['complete'] or sha(root/'outcomes.csv.gz')!=m['result_sha256']:
        raise RuntimeError('Incomplete or changed result phase')
    frame=pd.read_csv(root/'outcomes.csv.gz')
    if len(frame)!=m['repeated_outcomes'] or frame['seed'].nunique()!=m['unique_inputs']:
        raise RuntimeError('Independent input denominator differs')
    if frame.duplicated(['seed','service','policy']).any():raise RuntimeError('Repeated policy/source row')
    return frame,m

def candidate(card,request,method,new_context,population,allowance):
    anchor=Event(tuple(Atom(*a) for a in card['atoms']))
    c=Card(card['event_id'],card['producer_id'],card['population_id'],card['calibration_manifest'],
           card['n'],card['k'],card['alpha'],card['upper'])
    if not validated_numeric_card(c) or c.event_id!=anchor.identity or c.population_id!=population:return None
    old=card['context']
    if c.producer_id!=event_capsule(anchor,old):return None
    if method in ('DirectRecertCached','ExactCard'):
        if request.identity!=anchor.identity or event_capsule(request,new_context)!=event_capsule(request,old):return None
        if method=='ExactCard' and card['variant'] not in ANCHORS:return None
        witness=[('exact_event',request.identity)]
    elif method=='ContractCover':
        if card['variant'] not in ANCHORS:return None
        witness=containment(anchor,request)
        if witness is None or event_capsule(request,old)!=event_capsule(request,new_context):return None
    else:
        if card['variant'] not in ANCHORS or not procedural_contains(anchor,request):return None
        if not procedural_capsule_equal(request,old,new_context):return None
        witness=[('procedural_full_knowledge',request.identity)]
    if c.upper>allowance:return None
    return dict(upper=c.upper,card=card['id'],witness=witness,n=c.n,k=c.k)

def build_plan(cards,objectives,study,profile,service,task,variant,method,allowance,p):
    target=requirement(task,variant);choices=[]
    for policy in POLICIES:
        ctx=context(study,policy,service,p['camera_clock'])
        admitted=[]
        for card in cards:
            if card['profile']!=profile or card['service']!=service or card['policy']!=policy:continue
            # Cross-study use is only through the checked target dependencies.
            if study=='A' and card['study']!='A':continue
            if method=='DirectRecertCached' and card['study']!=study:continue
            valid=candidate(card,target,method,ctx,profile,allowance)
            if valid is not None:admitted.append(valid)
        if admitted:
            proof=min(admitted,key=lambda x:(x['upper'],x['card']))
            choices.append((objectives[(study,profile,service,policy)],policy,proof))
    base=dict(study=study,profile=profile,service=service,task=task,variant=variant,
              method=method,allowance=allowance,event_id=target.identity)
    if not choices:return dict(**base,status='REFUSED',policy=None,upper=None)
    objective,policy,proof=min(choices,key=lambda x:(x[0],x[1]))
    return dict(**base,status='AUTHORIZED',policy=policy,objective=objective,**proof)

def calibrate():
    p=verify();data={};manifest={};cards=[];objectives={};prep=[]
    alpha=p['family_alpha']/p['family_size']
    for study in ('A','B'):
        data[study],manifest[study]=read_phase(study,'calibration')
        for (profile,service,policy),frame in data[study].groupby(['profile','service','policy']):
            objectives[study,profile,service,policy]=float(np.mean(frame['loss_m2s']+frame['total_work_s']))
            ctx=context(study,policy,service,p['camera_clock'])
            for task in TASKS:
                for variant in VARIANTS:
                    event=requirement(task,variant);values=metrics(frame);n=len(frame)
                    pool=False
                    if study=='B':
                        old_ctx=context('A',policy,service,p['camera_clock'])
                        if event_capsule(event,old_ctx)==event_capsule(event,ctx):
                            old=data['A'].query('profile==@profile and service==@service and policy==@policy')
                            old_values=metrics(old)
                            values={k:np.r_[values[k],old_values[k]] for k in values};n+=len(old);pool=True
                    start=time.perf_counter_ns();failed=event.failure(values);k=int(failed.sum())
                    upper=cp_upper(k,n,alpha);elapsed=(time.perf_counter_ns()-start)*1e-9
                    ident=f'{study}/{profile}/{service}/{policy}/{task}/{variant}'
                    card=dict(id=ident,study=study,profile=profile,service=service,policy=policy,
                         task=task,variant=variant,event_id=event.identity,
                         atoms=[(a.metric,a.lower,a.upper) for a in event.atoms],n=n,k=k,alpha=alpha,
                         upper=upper,margin_015=.15-upper,producer_id=event_capsule(event,ctx),
                         population_id=profile,context=ctx,pooled_invariant_A_B=pool,
                         source_manifests={s:sha(HERE/'data'/s/'calibration/manifest.json')
                                           for s in (('A','B') if pool else (study,))})
                    card['calibration_manifest']=digest(card['source_manifests'])
                    cards.append(card);prep.append(dict(**{k:card[k] for k in ['study','profile','service','policy','task','variant']},
                                                       evaluated_records=n,wall_s=elapsed,anchor=variant in ANCHORS))
            if len(cards)%192==0:print('R9_CARDS',study,len(cards),flush=True)
    if len(cards)>p['family_size']:raise RuntimeError('Confidence family exceeded')
    plans=[]
    for study in ('A','B'):
      for profile in ('nominal','unfitted'):
       for service in ('relaxed','standard','tight','contended'):
        for task in TASKS:
         for variant in VARIANTS:
          for allowance in ALLOWANCES:
           for method in METHODS:
            plans.append(build_plan(cards,objectives,study,profile,service,task,variant,method,allowance,p))
        print('R9_SELECTION',study,profile,service,len(plans),flush=True)
    keyed={(q['study'],q['profile'],q['service'],q['task'],q['variant'],q['allowance'],q['method']):q for q in plans}
    for key,q in keyed.items():
        if key[-1]!='ContractCover':continue
        other=keyed[(*key[:-1],'ProceduralCoverValidated')]
        if (q['status'],q['policy'],q['upper'])!=(other['status'],other['policy'],other['upper']):
            raise RuntimeError('Strong semantic baseline disagrees')
    output=HERE/'data/evidence';output.mkdir(exist_ok=True)
    (output/'cards.json').write_text(json.dumps(cards,indent=2),encoding='utf-8')
    (output/'plans.json').write_text(json.dumps(plans,indent=2),encoding='utf-8')
    pd.DataFrame(prep).to_csv(output/'calibration_preparation.csv',index=False)
    files={str(f.relative_to(HERE)):sha(f) for f in sorted(output.glob('*'))}
    for study in ('A','B'):
        for name in ['manifest.json','outcomes.csv.gz']:
            path=HERE/'data'/study/'calibration'/name;files[str(path.relative_to(HERE))]=sha(path)
    (HERE/'protocol/selection_freeze.json').write_text(json.dumps(dict(files=files,
        cards=len(cards),plan_queries=len(plans),confirmation_inputs_before_seal=0),indent=2),encoding='utf-8')
    print('CALIBRATION_SEALED',len(cards),len(plans),flush=True)

def confirm(study):
    verify();frame,manifest=read_phase(study,'confirmation')
    lock=json.loads((HERE/'protocol/selection_freeze.json').read_text())
    for path,h in lock['files'].items():
        if sha(HERE/path)!=h:raise RuntimeError('Changed frozen evidence')
    plans=json.loads((HERE/'data/evidence/plans.json').read_text());queries=[]
    lookup={(profile,service,policy):f.sort_values('seed').set_index('seed')
            for (profile,service,policy),f in frame.groupby(['profile','service','policy'])}
    for plan in plans:
        if plan['study']!=study:continue
        seeds=sorted(frame.loc[frame['profile']==plan['profile'],'seed'].unique())
        if plan['status']=='AUTHORIZED':
            selected=lookup[plan['profile'],plan['service'],plan['policy']]
            failures=requirement(plan['task'],plan['variant']).failure(metrics(selected))
            for i,seed in enumerate(selected.index):
                row=selected.loc[seed]
                queries.append(dict(**{k:plan[k] for k in ['study','profile','service','task','variant','method','allowance','status','policy','upper']},
                    seed=int(seed),failure=int(failures[i]),authorized=1,margin=plan['allowance']-plan['upper'],
                    rmse_m=row['rmse_m'],loss_m2s=row['loss_m2s'],total_work_s=row['total_work_s'],
                    report_delay_s=row['report_delay_s'],image_age_s=row['image_age_s']))
        else:
            for seed in seeds:
                queries.append(dict(**{k:plan[k] for k in ['study','profile','service','task','variant','method','allowance','status','policy','upper']},
                    seed=int(seed),failure=None,authorized=0,margin=None,rmse_m=None,loss_m2s=None,
                    total_work_s=None,report_delay_s=None,image_age_s=None))
    target=HERE/'data'/study/'confirmation/requests.csv.gz'
    pd.DataFrame(queries).to_csv(target,index=False,compression='gzip')
    print('CONFIRMATION_REQUESTS',study,len(queries),flush=True)

if __name__=='__main__':
    calibrate() if '--calibrate' in sys.argv else confirm(sys.argv[-1])
