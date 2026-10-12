"""Authorized concurrent uploads of disjoint completed phase archives."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import argparse,json
from github_backup import API,credential,publish_assets,REPOSITORY,BRANCH,sha

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--directory',type=Path,required=True)
    ap.add_argument('--commit',required=True);ap.add_argument('--record',type=Path,required=True)
    args=ap.parse_args();api=API(credential())
    assert api.request('https://api.github.com/user')['login']=='edrisskrah131-lang'
    base='https://api.github.com/repos/'+REPOSITORY
    assert api.request(base)['permissions']['push']
    assert api.request(base+'/git/ref/heads/'+BRANCH)['object']['sha']==args.commit
    groups=[]
    for study,phase in (('A','confirmation'),('A','stress'),('B','confirmation'),('B','stress')):
        files=sorted(args.directory.glob(f'A20_R9_{study}_{phase}_complete_*'))
        indexes=[p for p in files if p.name.endswith('_INDEX.json')]
        assert len(indexes)==1,(study,phase)
        index=json.loads(indexes[0].read_text());assert index['all_files_covered']
        groups.append(files)
    assets=[]
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures=[pool.submit(publish_assets,api,group,args.commit) for group in groups]
        for future in as_completed(futures):
            release,verified=future.result();assets+=verified
            # Verified completed subsets survive an interrupted later group.
            args.record.with_name(args.record.stem+'_partial.json').write_text(json.dumps(dict(remote_upload_verified=False,completed_verified_assets=assets),indent=2),encoding='utf-8')
    record=dict(repository=REPOSITORY,branch=BRANCH,commit=args.commit,
                remote_upload_verified=True,authenticated_login='edrisskrah131-lang',
                release_url=release,verified_assets=assets,
                assets=[{k:a[k] for k in ('file','sha256','bytes')} for a in assets])
    args.record.write_text(json.dumps(record,indent=2),encoding='utf-8')
    print('REMAINING_PHASES_REMOTE_VERIFIED',len(assets),flush=True)

if __name__=='__main__':main()
