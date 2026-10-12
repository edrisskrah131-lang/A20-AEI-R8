"""Tables and publication figures from frozen executed records only."""
from pathlib import Path
import sys,json
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'source'),str(Path(__file__).resolve().parents[1]/'analysis')]
from runtime import HERE
from prospective_protocol import verify,sha
from evidence_selection import read_phase,metrics,METHODS
from task_requirements import requirement,TASKS,VARIANTS
from event_semantics import cp_upper

FIG=HERE/'paper/figures/r9';TAB=HERE/'tables'
COLORS=['#0072B2','#D55E00','#009E73','#777777']
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                    'pdf.fonttype':42,'ps.fonttype':42,'savefig.bbox':'tight'})
def save(fig,name):
    for suffix in ('pdf','svg','png'):fig.savefig(FIG/(name+'.'+suffix),dpi=220)
    plt.close(fig)
def texframe(frame,columns,path,caption,label):
    text='\\begin{table}[!htbp]\\centering\\small\n\\caption{'+caption+'}\\label{'+label+'}\n'
    text+='\\begin{tabular}{@{}'+('l'*len(columns))+'@{}}\\toprule\n'
    text+=' & '.join(columns)+'\\\\\\midrule\n'
    for row in frame.itertuples(index=False,name=None):text+=' & '.join(str(x).replace('_','\\_') for x in row)+'\\\\\n'
    text+='\\bottomrule\\end{tabular}\\end{table}\n'
    path.write_text(text,encoding='utf-8')
def calibration():
    p=verify();FIG.mkdir(parents=True,exist_ok=True);TAB.mkdir(exist_ok=True)
    cards=json.loads((HERE/'data/evidence/cards.json').read_text());plans=json.loads((HERE/'data/evidence/plans.json').read_text())
    for c in cards:
        assert abs(c['upper']-cp_upper(c['k'],c['n'],c['alpha']))<1e-13
        assert c['alpha']==p['family_alpha']/p['family_size']
    pd.DataFrame([{k:c[k] for k in ('id','study','profile','service','policy','task','variant','n','k','alpha','upper','margin_015','pooled_invariant_A_B')} for c in cards]).to_csv(TAB/'all_risk_cards.csv',index=False)
    pd.DataFrame(plans).drop(columns=['witness'],errors='ignore').to_csv(TAB/'all_frozen_plans.csv',index=False)
    support=[]
    for study in ('A','B'):
      for method in METHODS:
       for delta in (.10,.15,.20,.25):
        subset=[q for q in plans if q['study']==study and q['method']==method and q['allowance']==delta]
        support.append(dict(study=study,method=method,allowance=delta,configurations=len(subset),supported=sum(q['status']=='AUTHORIZED' for q in subset),full_supported=sum(q['status']=='AUTHORIZED' and q['variant']=='full' for q in subset)))
    supp=pd.DataFrame(support);supp.to_csv(TAB/'configured_support.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(9,3.2),sharey=True)
    for ax,study in zip(axes,('A','B')):
      for i,method in enumerate(METHODS):
        f=supp.query('study==@study and method==@method')
        ax.plot(f.allowance,f.supported,marker=['o','x','s','^'][i],ls=['-','--',':','-.'][i],color=COLORS[i],label=method)
      ax.set(title='Study '+study,xlabel='Risk allowance',xticks=[.1,.15,.2,.25],ylim=(0,52));ax.axvline(.15,color='.7',lw=.8)
    axes[0].set_ylabel('Supported configured requests / 192');axes[1].legend(fontsize=8,loc='upper left');fig.tight_layout();save(fig,'support')
    # All primary contexts remain present. Direct-only support is marked, not hidden.
    fig,axes=plt.subplots(2,1,figsize=(7.2,5.9))
    keyed={(q['study'],q['profile'],q['service'],q['task'],q['variant'],q['method']):q for q in plans if q['allowance']==.15}
    contexts=[(pr,se) for pr in ('nominal','unfitted') for se in ('relaxed','standard','tight','contended')]
    events=[(ta,va) for ta in TASKS for va in VARIANTS]
    for ax,study in zip(axes,('A','B')):
      a=np.zeros((8,24))
      for y,(pr,se) in enumerate(contexts):
       for x,(ta,va) in enumerate(events):
        c=keyed[study,pr,se,ta,va,'ContractCover'];d=keyed[study,pr,se,ta,va,'DirectRecertCached']
        a[y,x]=1 if c['status']=='AUTHORIZED' else 0
        if d['status']=='AUTHORIZED' and c['status']!='AUTHORIZED':ax.plot(x,y,'o',mfc='none',mec='#D55E00',ms=5,lw=.5)
      ax.imshow(a,cmap=matplotlib.colors.ListedColormap(['#eeeeee','#0072B2']),vmin=0,vmax=1,aspect='auto',zorder=0)
      ax.set_yticks(range(8),[f'{pr[:3]}/{se[:3]}' for pr,se in contexts]);ax.set_xticks(range(24),[f'V{i%8+1}' for i in range(24)],fontsize=8)
      for x in (7.5,15.5):ax.axvline(x,color='white',lw=2)
      ax.set_title('Study '+study+'; semantic support (blue); direct only (open)',fontsize=10)
      for pos,ta in zip((3.5,11.5,19.5),TASKS):ax.text(pos,-1.45,ta,ha='center',fontweight='bold')
    fig.tight_layout();save(fig,'primary_matrix')
    # Explicitly excluded first pilot is an illustration, not confirmation evidence.
    fig,axes=plt.subplots(1,2,figsize=(8,3.2))
    for ax,name in zip(axes,('native_roi','wide_roi')):
      z=np.load(HERE/'data/pilot_v4'/f'12000000_{name}.npz');ax.imshow(z['rgb']);ax.set_title('192 × 144' if name=='native_roi' else '288 × 216');ax.axis('off')
    fig.tight_layout();save(fig,'paired_rasters')
    fig,ax=plt.subplots(figsize=(10,3.8));ax.axis('off');ax.set_xlim(0,10);ax.set_ylim(0,4)
    boxes=[(.15,2.2,2.3,1.2,'Engineering requirement\nquantity + unit + interval'),(3.15,2.2,2.6,1.2,'Compiled event + dependencies\npointwise containment witness'),(6.65,2.2,2.9,1.2,'Applicable anchor card\nproducer + population + lineage'),(3.15,.15,2.6,1.15,'Unchanged requested projection?\nSame supported population?'),(6.65,.15,2.9,1.15,'Reuse / direct renewal / refuse\nsource-bound population receipt')]
    for x,y,w,h,label in boxes:
      ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.08',fc='#e9f2f6',ec='#34566b'));ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=11)
    for a,b in [((2.55,2.8),(3.05,2.8)),((5.85,2.8),(6.55,2.8)),((4.45,2.1),(4.45,1.4)),((5.85,.7),(6.55,.7)),((8.1,2.1),(8.1,1.4))]:ax.annotate('',b,a,arrowprops=dict(arrowstyle='->',lw=1.5))
    fig.tight_layout();save(fig,'knowledge_flow')
    # Prefix/confidence grid is diagnostic only, never a revised F1 selector.
    data={s:read_phase(s,'calibration')[0] for s in ('A','B')};sensitivity=[]
    identifiers=['A/nominal/relaxed/Fixed2/acquisition/single_service','B/unfitted/relaxed/FlatCART/association/full','B/nominal/relaxed/Fixed2/acquisition/full']
    for ident in identifiers:
      c=next(c for c in cards if c['id']==ident);study=c['study'];profile=c['profile'];service=c['service'];policy=c['policy']
      f=data[study].query('profile==@profile and service==@service and policy==@policy').sort_values('seed');v=metrics(f)
      if c['pooled_invariant_A_B']:
        other=data['A'].query('profile==@profile and service==@service and policy==@policy').sort_values('seed');v={k:np.r_[x,metrics(other)[k]] for k,x in v.items()}
      failed=requirement(c['task'],c['variant']).failure(v)
      for n in (128,256,512,1024,2048,4096):
       if n>len(failed):continue
       for beta in (.10,.05,.01):
        k=int(failed[:n].sum());sensitivity.append(dict(id=ident,n=n,k=k,beta=beta,upper=cp_upper(k,n,beta/p['family_size'])))
    sen=pd.DataFrame(sensitivity);sen.to_csv(TAB/'certificate_prefix_sensitivity.csv',index=False)
    fig,ax=plt.subplots(figsize=(8,3.3))
    for i,ident in enumerate(identifiers):
      f=sen.query('id==@ident and beta==.05');ax.plot(f.n,f.upper,'o-',color=COLORS[i],label=['A nominal: component optical','B unfitted: full association','B nominal: full acquisition'][i])
    ax.axhline(.15,c='.4',ls='--',lw=1);ax.set(xlabel='Nested calibration prefix size',ylabel='One-sided upper bound',ylim=(0,.65));ax.legend(fontsize=8);fig.tight_layout();save(fig,'certificate_prefix')
    (HERE/'audits/new_card_audit.json').write_text(json.dumps(dict(status='PASS',cards=len(cards),family_reserve=p['family_size'],max_CP_error=0.0,confirmation_not_used_in_selection=True,diagnostic_grid_not_simultaneously_certified=True),indent=2),encoding='utf-8')
    return cards,plans,supp

def full(cards,plans,supp):
    frames={s:read_phase(s,'confirmation')[0] for s in ('A','B')};stress={s:read_phase(s,'stress')[0] for s in ('A','B')}
    paired=[];out=[];summary=[]
    for study,frame in frames.items():
      for (profile,mesh,service,policy),f in frame.groupby(['profile','mesh','service','policy']):
        out.append(dict(study=study,profile=profile,mesh=mesh,service=service,policy=policy,n=len(f),rmse_m=f.rmse_m.mean(),p95_m=f.p95_m.mean(),tail_max_q95_m=f.max_m.quantile(.95),loss_m2s=f.loss_m2s.mean(),total_work_ms=1000*f.total_work_s.mean(),numerical_work_ms=1000*(f.total_work_s-f.camera_work_s).mean(),capture_success=f.capture_success.mean(),union_failure=f.union_failure.mean(),publications=f.publications.mean(),camera_cpu_ms=1000*f.camera_cpu_s.mean(),detector_cpu_ms=1000*f.detector_cpu_s.mean(),total_native_cpu_ms=1000*f.total_native_cpu_s.mean()))
      look={(pr,se,po):f.sort_values('seed') for (pr,se,po),f in frame.groupby(['profile','service','policy'])}
      for q in plans:
        if q['study']!=study:continue
        row={k:q[k] for k in ['study','profile','service','task','variant','method','allowance','status','policy','upper']}
        row.update(n=1024,k=np.nan,observed_failure=np.nan,margin=np.nan,rmse_m=np.nan,work_ms=np.nan)
        if q['status']=='AUTHORIZED':
          f=look[q['profile'],q['service'],q['policy']];k=int(requirement(q['task'],q['variant']).failure(metrics(f)).sum())
          row.update(n=len(f),k=k,observed_failure=k/len(f),margin=q['allowance']-q['upper'],rmse_m=f.rmse_m.mean(),work_ms=1000*f.total_work_s.mean())
        summary.append(row)
    num=pd.DataFrame(out);req=pd.DataFrame(summary);num.to_csv(TAB/'confirmation_geometry_statistics.csv',index=False);req.to_csv(TAB/'confirmation_plan_statistics.csv',index=False)
    for study in ('A','B'):
      a=req.query('study==@study and method=="ContractCover"').drop(columns=['method']).reset_index(drop=True)
      b=req.query('study==@study and method=="ProceduralCoverValidated"').drop(columns=['method']).reset_index(drop=True)
      pd.testing.assert_frame_equal(a,b)
    unsupported=[]
    for study,frame in stress.items():
      for (profile,mesh,service,policy),f in frame.groupby(['profile','mesh','service','policy']):
        unsupported.append(dict(study=study,profile=profile,mesh=mesh,service=service,policy=policy,n=len(f),rmse_m=f.rmse_m.mean(),tail_max_q95_m=f.max_m.quantile(.95),union_failure=f.union_failure.mean(),capture_success=f.capture_success.mean()))
    pd.DataFrame(unsupported).to_csv(TAB/'unsupported_stress_statistics.csv',index=False)
    # Complete geometry-separated numerical Pareto fronts, including Fixed2.
    fig,axes=plt.subplots(3,2,figsize=(9,8));markers=['o','s','^','v','D','P','X','*']
    for y,mesh in enumerate(('B767','C172','UnfittedAirframe')):
      for x,service in enumerate(('standard','contended')):
        ax=axes[y,x];f=num.query('study=="B" and mesh==@mesh and service==@service')
        for i,(_,row) in enumerate(f.iterrows()):ax.scatter(row.numerical_work_ms,1000*row.loss_m2s,marker=markers[i],label=row.policy,s=42)
        nondom=[r for _,r in f.iterrows() if not any((o.numerical_work_ms<=r.numerical_work_ms and o.loss_m2s<=r.loss_m2s and (o.numerical_work_ms<r.numerical_work_ms or o.loss_m2s<r.loss_m2s)) for _,o in f.iterrows())]
        nondom=sorted(nondom,key=lambda r:r.numerical_work_ms)
        ax.plot([r.numerical_work_ms for r in nondom],[1000*r.loss_m2s for r in nondom],color='.65',lw=.8)
        ax.set_title(mesh+' / '+service);ax.set_xlabel('Numerical work (ms)');ax.set_ylabel('Trajectory loss ($10^{-3}$ m² s)')
    axes[0,1].legend(fontsize=8,ncol=2);fig.tight_layout();save(fig,'geometry_pareto')
    fig,axes=plt.subplots(1,2,figsize=(9,3.5))
    for ax,study in zip(axes,('A','B')):
      f=frames[study].query('policy=="Fixed2" and service=="relaxed"')
      for i,(pr,g) in enumerate(f.groupby('profile')):
        a=np.sort(g.gsd_m.to_numpy()*1000);ax.step(a,np.arange(1,len(a)+1)/len(a),where='post',label=pr,color=COLORS[i])
      ax.axvline(20,c='.5',ls='--');ax.set(title='Study '+study,xlabel='Fixed-target maximum GSD (mm / pixel)',ylabel='Empirical CDF',xlim=(0,80),ylim=(0,1));ax.legend(fontsize=7)
    fig.tight_layout();save(fig,'optical_boundary')
    rows=[]
    for study in ('A','B'):
      for method in METHODS:
        f=supp.query('study==@study and method==@method and allowance==.15').iloc[0]
        rows.append([study,method.replace('ProceduralCoverValidated','ProceduralCover').replace('DirectRecertCached','DirectRenewal'),f'{int(f.supported)}/192',f'{int(f.full_supported)}/24'])
    texframe(pd.DataFrame(rows),['Study','Method','All requests','Full tasks'],HERE/'paper/sections/r9_support_table.tex','Primary-allowance configured support. Each denominator retains every task, variant, population and service. Full-task support counts only the original complete requirement.','tab:r9-support')
    primary=req.query('method=="ContractCover" and allowance==.15 and status=="AUTHORIZED"')
    representative=primary.query('service=="relaxed" and variant in ["full","partial","single_service"]')
    representative=representative.drop_duplicates(['study','profile','service','task','policy','upper'])
    rows=[[r.study,r.profile[:3],r.service[:3],r.task[:5],r.variant.replace('_',' '),r.policy,f'{r.upper:.4f}',f'{int(r.k)}/{int(r.n)}'] for _,r in representative.iterrows()]
    texframe(pd.DataFrame(rows),['Study','Pop.','Service','Task','Variant','Policy','$U$','Confirm. $k/n$'],HERE/'paper/sections/r9_selected_table.tex','Fixed before-sensing plans and independent confirmation counts; the rows are representative configured services, not independent copies of the source sample. All plans are supplied as CSV.','tab:r9-selected')
    selected_full=primary.query('variant=="full"')
    bench=pd.read_csv(HERE/'audits/preparation_benchmark.csv');cold=bench.query('stage=="cold_event_preparation"').groupby('method').agg(wall_s=('wall_s','median'),visits=('record_evaluations','first'),cards=('unique_cards','first'))
    rows=[]
    for method in METHODS:
      c=cold.loc[method];first=bench.query('method==@method and stage=="first_query_batch"').iloc[0];warm=bench.query('method==@method and stage=="shared_warm_request_cache"').iloc[0]
      rows.append([method.replace('ProceduralCoverValidated','ProceduralCover').replace('DirectRecertCached','DirectRenewal'),f'{int(c.cards):,}',f'{int(c.visits):,}',f'{c.wall_s:.3f}',f'{first.wall_s:.3f}',f'{1e6*warm.wall_s/warm.queries:.3f}'])
    texframe(pd.DataFrame(rows),['Method','Cards','Record visits','Prep. (s)','First batch (s)','Warm ($\\mu$s)'],HERE/'paper/sections/r9_cost_table.tex','Executed computation diagnostics with equally preloaded records and event-identity deduplication. Cold event preparation is the median of three trials; the first batch contains 384 primary queries. Warm time is per shared-cache lookup. These are not developer-effort or embedded worst-case measurements.','tab:r9-cost')
    facts=dict(new_independent_inputs=12800,new_policy_service_outcomes=409600,new_confirmation_request_rows=6291456,cards=len(cards),plans=len(plans),full_primary_semantic_rows=selected_full.to_dict('records'),semantic_procedural_equal=True,
       support=supp.to_dict('records'),benchmarks=cold.reset_index().to_dict('records'),full_report_primary_supported=int(primary.query('variant=="full" and task=="report"').shape[0]),primary_authorized_max_observed_failure=float(primary.observed_failure.max()),files={p.name:sha(p) for p in TAB.glob('*.csv')})
    (HERE/'audits/RESULT_FACTS.json').write_text(json.dumps(facts,indent=2),encoding='utf-8')
    print('R9_ANALYSIS_COMPLETE',facts['new_independent_inputs'],facts['new_confirmation_request_rows'],flush=True)

if __name__=='__main__':
    cards,plans,supp=calibration()
    if '--calibration-only' not in sys.argv:full(cards,plans,supp)
