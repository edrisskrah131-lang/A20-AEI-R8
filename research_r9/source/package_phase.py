"""Archive complete raw phase in bounded chunks, preserving every input once."""
from pathlib import Path
import json,argparse,hashlib,zipfile
from datetime import datetime,timezone
from checkpoint_archive import sha

def make_archive(root,paths,output,name,prefix):
    archive=output/(name+'.zip')
    entries=[dict(path=p.relative_to(root).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in paths]
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=3) as z:
        for p,item in zip(paths,entries):
            z.write(p,item['path'],compress_type=zipfile.ZIP_STORED if p.suffix in ('.npz','.gz') else zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(archive) as z:
        for item in entries:
            if hashlib.sha256(z.read(item['path'])).hexdigest()!=item['sha256']:raise RuntimeError('Archive verification failed')
    m=dict(archive=archive.name,bytes=archive.stat().st_size,sha256=sha(archive),
           restore_prefix=prefix,entries=entries,remote_upload_verified=False)
    manifest=output/(name+'.json');manifest.write_text(json.dumps(m,indent=2),encoding='utf-8')
    print('PACKAGED',archive.name,m['bytes'],flush=True)
    return m

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--stage',required=True)
    ap.add_argument('--restore-prefix',required=True);ap.add_argument('--max-mb',type=int,default=256)
    args=ap.parse_args();root=args.root.resolve();args.output.mkdir(parents=True,exist_ok=True)
    phase=json.loads((root/'manifest.json').read_text())
    if not phase['complete']:raise RuntimeError('Only complete phases can be archived by this packager')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');name='A20_R9_'+args.stage+'_'+stamp
    limit=args.max_mb*1024**2;part=[];size=0;all_manifests=[];seen=set()
    for item in phase['inputs']:
        seed=item['seed'];base=root/item['profile']
        group=[base/f'{seed}.json',*[base/n for n in item['files']]]
        if sha(group[0])!=item['metadata_sha256']:raise RuntimeError('Raw metadata differs from phase manifest')
        for p in group[1:]:
            if sha(p)!=item['files'][p.name]:raise RuntimeError('Raw array differs from phase manifest')
        if any(p in seen for p in group):raise RuntimeError('Duplicate raw input in phase')
        seen.update(group);weight=sum(p.stat().st_size for p in group)
        if size+weight>limit and part:
            all_manifests.append(make_archive(root,part,args.output,name+f'_raw_{len(all_manifests)+1:03}',args.restore_prefix))
            part=[];size=0
        part+=group;size+=weight
    if part:all_manifests.append(make_archive(root,part,args.output,name+f'_raw_{len(all_manifests)+1:03}',args.restore_prefix))
    extra=sorted(p for p in root.iterdir() if p.is_file())
    all_manifests.append(make_archive(root,extra,args.output,name+'_tables',args.restore_prefix))
    actual=set(p for p in root.rglob('*') if p.is_file())
    if actual!=seen|set(extra):raise RuntimeError('Unindexed file would be omitted from checkpoint')
    index=dict(stage=args.stage,utc=datetime.now(timezone.utc).isoformat(),
               unique_inputs=phase['unique_inputs'],repeated_outcomes=phase['repeated_outcomes'],
               restore_prefix=args.restore_prefix,archives=all_manifests,all_files_covered=True,
               remote_upload_verified=False)
    (args.output/(name+'_INDEX.json')).write_text(json.dumps(index,indent=2),encoding='utf-8')
    print('PHASE_ARCHIVES_COMPLETE',len(all_manifests),phase['unique_inputs'],flush=True)

if __name__=='__main__':main()
