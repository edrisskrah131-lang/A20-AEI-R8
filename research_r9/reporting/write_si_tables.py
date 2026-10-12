from pathlib import Path
import pandas as pd
root=Path(__file__).resolve().parents[1];parts=[]
tables=[('confirmation_geometry_statistics.csv','Complete geometry-separated confirmation means',
 ['study','mesh','service','policy','n','rmse_m','loss_m2s','total_work_ms','capture_success','tail_max_q95_m'],
 ['Study','Mesh','Service','Policy','$n$','RMSE','$L$','Work','Success','$Q_{.95}$']),
 ('unsupported_stress_statistics.csv','All unsupported stress means; no transferred certificate',
 ['study','profile','mesh','service','policy','n','rmse_m','tail_max_q95_m','union_failure'],
 ['Study','Stress','Mesh','Service','Policy','$n$','RMSE','$Q_{.95}$','Union fail'])]
for filename,title,fields,head in tables:
 f=pd.read_csv(root/'tables'/filename)
 parts.append('\\subsection{'+title+'}\n\\scriptsize\\setlength{\\tabcolsep}{3pt}\\begin{longtable}{@{}'+'l'*len(fields)+'@{}}\n\\caption{'+title+'. Errors are in meters; $Q_{.95}$ is the 95th percentile of episode maxima. Loss is m$^2$s; work is milliseconds where present. Independent counts remain explicit.}\\\\\\toprule\n')
 parts.append(' & '.join(head)+'\\\\\\midrule\\endfirsthead\n\\toprule\n')
 parts.append(' & '.join(head)+'\\\\\\midrule\\endhead\n')
 for _,row in f.iterrows():
  cells=[]
  for col in fields:
   x=row[col]
   if col=='n':v=str(int(x))
   elif isinstance(x,float):v=f'{x:.4f}'
   else:v=str(x).replace('UnfittedAirframe','Unfitted').replace('_','\\_')
   cells.append(v)
  parts.append(' & '.join(cells)+'\\\\\n')
 parts.append('\\bottomrule\\end{longtable}\\normalsize\\setlength{\\tabcolsep}{6pt}\n')
(root/'paper/sections/r9_supplement_tables.tex').write_text(''.join(parts),encoding='utf-8')
