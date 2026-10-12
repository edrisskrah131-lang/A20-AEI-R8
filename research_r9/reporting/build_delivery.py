"""Self-contained editable source and small reading package, with all hashes."""
from pathlib import Path
import sys,json,shutil,zipfile,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from runtime import HERE,WORKSPACE
from checkpoint_archive import sha

def archive(paths,base,destination):
    entries=[]
    with zipfile.ZipFile(destination,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
      for path in paths:
        name=path.relative_to(base).as_posix();z.write(path,name)
        entries.append(dict(path=name,bytes=path.stat().st_size,sha256=sha(path)))
    with zipfile.ZipFile(destination) as z:
      for e in entries:assert hashlib.sha256(z.read(e['path'])).hexdigest()==e['sha256']
    manifest=dict(file=destination.name,bytes=destination.stat().st_size,sha256=sha(destination),entries=entries)
    destination.with_suffix('.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print('DELIVERY_ARCHIVE_VERIFIED',destination.name,destination.stat().st_size,flush=True)
    return manifest

def main():
    output=WORKSPACE/'outputs/R9_release';output.mkdir(exist_ok=True)
    mapping={'main':'A20_AEI_R9_Manuscript','supplement':'A20_AEI_R9_Supplement',
             'revision_report_cn':'A20_AEI_R9_Revision_Report_CN','internal_review_cn':'A20_AEI_R9_Internal_Review_CN'}
    for source,name in mapping.items():shutil.copy2(HERE/'paper/build'/f'{source}.pdf',output/f'{name}.pdf')
    shutil.copy2(HERE/'HANDOFF_R9_CN.md',output/'READ_FIRST_R9_CN.md')
    shutil.copy2(HERE/'REPRODUCE_R9_CN.md',output/'REPRODUCE_R9_CN.md')
    for name in ('RESULT_FACTS.json','PDF_FINAL_QA.json','final_execution_audit.json','source_replay.json','environment.json'):
      shutil.copy2(HERE/'audits'/name,output/name)
    tables=output/'tables';tables.mkdir(exist_ok=True)
    for p in (HERE/'tables').glob('*.csv'):shutil.copy2(p,tables/p.name)
    reading=[p for p in output.rglob('*') if p.is_file() and 'qa' not in p.relative_to(output).parts and not p.name.startswith('A20_AEI_R9_Reading') and not p.name.startswith('A20_AEI_R9_Editable') and not p.name.startswith('A20_AEI_R9_Figures') and p.name!='DELIVERY_MANIFEST.json' and p.suffix!='.zip']
    manifests=[archive(sorted(reading),output,output/'A20_AEI_R9_Reading_And_Handoff.zip')]
    sources=[]
    for p in HERE.rglob('*'):
      if not p.is_file():continue
      rel=p.relative_to(HERE)
      if '__pycache__' in rel.parts or ('paper' in rel.parts and 'build' in rel.parts):continue
      if rel.parts[0]=='data' and not (len(rel.parts)>1 and rel.parts[1]=='evidence'):continue
      sources.append(p)
    manifests.append(archive(sorted(sources),HERE.parent,output/'A20_AEI_R9_Editable_Source.zip'))
    manifests.append(archive(sorted(p for p in (HERE/'paper/figures').rglob('*') if p.is_file()),HERE/'paper',output/'A20_AEI_R9_Figures.zip'))
    result=dict(status='LOCAL_ARCHIVES_VERIFIED',remote_upload_verified=False,
       documents=[dict(file=(output/(n+'.pdf')).name,bytes=(output/(n+'.pdf')).stat().st_size,sha256=sha(output/(n+'.pdf'))) for n in mapping.values()],
       archives=[{k:v for k,v in m.items() if k!='entries'} for m in manifests],
       note='Final remote upload and cleanup receipts are detached to avoid self-referential hashes. Large raw arrays are in complete stage archives, not the small reading package.')
    (output/'DELIVERY_MANIFEST.json').write_text(json.dumps(result,indent=2),encoding='utf-8')

if __name__=='__main__':main()
