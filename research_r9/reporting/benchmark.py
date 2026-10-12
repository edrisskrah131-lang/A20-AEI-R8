"""Executed preparation, first-query and shared warm-cache measurements.

These are computational diagnostics on already frozen events, not additional
calibration observations, developer effort or embedded worst-case timings.
"""
from pathlib import Path
import sys,json,time,csv
import numpy as np
sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'source'),str(Path(__file__).resolve().parents[1]/'analysis')]
from runtime import HERE
from prospective_protocol import verify,sha
from task_requirements import TASKS,VARIANTS,ANCHORS,requirement,context,event_capsule
from event_semantics import cp_upper
from evidence_selection import read_phase,metrics,validated_numeric_card
import evidence_selection as es
from fair_selection import strengthened
from run_evidence import apply_overlay

def main():
    p=verify();apply_overlay()
    frames={s:read_phase(s,'calibration')[0] for s in ('A','B')}
    groups={s:{key:f for key,f in frame.groupby(['profile','service','policy'])} for s,frame in frames.items()}
    values={s:{key:metrics(f) for key,f in group.items()} for s,group in groups.items()}
    objectives={(s,*key):float(np.mean(f.loss_m2s+f.total_work_s)) for s,g in groups.items() for key,f in g.items()}
    rows=[]
    methods=es.METHODS
    # Order alternates, all competitors receive the same preloaded raw records.
    for trial in range(3):
      for method in (methods if trial%2==0 else methods[::-1]):
        events={}
        for task in TASKS:
          for variant in (VARIANTS if method=='DirectRecertCached' else ANCHORS):
            e=requirement(task,variant);events[e.identity]=e
        count=0;cards_count=0;begin=time.perf_counter_ns()
        for study in ('A','B'):
          for (profile,service,policy),base_values in values[study].items():
            for event in events.values():
              val=base_values;n=len(val['gsd_m'])
              if study=='B' and event_capsule(event,context('A',policy,service,p['camera_clock']))==event_capsule(event,context('B',policy,service,p['camera_clock'])):
                val={k:np.r_[v,values['A'][profile,service,policy][k]] for k,v in val.items()};n*=2
              k=int(event.failure(val).sum());cp_upper(k,n,p['family_alpha']/p['family_size'])
              count+=n;cards_count+=1
        rows.append(dict(trial=trial,method=method,stage='cold_event_preparation',
          wall_s=(time.perf_counter_ns()-begin)*1e-9,record_evaluations=count,unique_cards=cards_count,queries=0))
    cards=json.loads((HERE/'data/evidence/cards.json').read_text())
    # JSON encodes both immutable tuples and lists as arrays. Restore the
    # declared tuple fields before the independent procedural equality check;
    # calibration generated these same typed contexts in memory.
    for card in cards:
        for field in ('roi','localization'):
            card['context'][field]=tuple(card['context'][field])
    plans=json.loads((HERE/'data/evidence/plans.json').read_text());cold=[]
    for method in methods:
        validated_numeric_card.cache_clear();begin=time.perf_counter_ns();result=[]
        for q in plans:
            if q['method']!=method or q['allowance']!=.15:continue
            out=strengthened(cards,objectives,*(q[k] for k in ('study','profile','service','task','variant','method','allowance')),p)
            if json.loads(json.dumps(out))!=q:
                print('BENCHMARK_PLAN_DIFF',method,{k:(q.get(k),out.get(k)) for k in set(q)|set(out) if json.loads(json.dumps(out.get(k)))!=q.get(k)},flush=True)
                raise RuntimeError('Benchmark recomputation differs from frozen plan')
            result.append(out)
        cold.append(dict(trial=0,method=method,stage='first_query_batch',
          wall_s=(time.perf_counter_ns()-begin)*1e-9,record_evaluations=0,unique_cards=0,queries=len(result)))
        cache={(q['study'],q['profile'],q['service'],q['task'],q['variant']):q for q in result}
        keys=tuple(cache);begin=time.perf_counter_ns();checksum=0
        for repeat in range(100):
            for key in keys:checksum+=cache[key]['status']=='AUTHORIZED'
        rows.append(dict(trial=0,method=method,stage='shared_warm_request_cache',
          wall_s=(time.perf_counter_ns()-begin)*1e-9,record_evaluations=0,unique_cards=0,queries=len(keys)*100))
    rows+=cold;out=HERE/'audits/preparation_benchmark.csv'
    with out.open('w',newline='',encoding='utf-8') as f:
      writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
    audit=dict(status='PASS',data_preloaded_equally=True,event_identity_deduplicated_for_every_method=True,
       developer_effort_measured=False,additional_independent_inputs=0,
       scope='CPU/wall diagnostic; first query includes numeric-card validation and plan generation; warm lookup is identical dictionary caching.',
       trials=3,sha256=sha(out),seed_families_unchanged=True)
    (HERE/'audits/preparation_benchmark.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    print('PREPARATION_BENCHMARK_COMPLETE',len(rows),flush=True)

if __name__=='__main__':main()
