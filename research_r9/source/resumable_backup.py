"""Per-asset durable receipts and retries for explicitly authorized R9 backup."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from threading import Lock
import argparse,json,time,os
from urllib.parse import quote
from github_backup import API,credential,sha,REPOSITORY,BRANCH,TAG

def list_assets(api,base,release):
    assets={};page=1
    while True:
        batch=api.request(base+f'/releases/{release["id"]}/assets?per_page=30&page={page}')
        assets.update({a['name']:a for a in batch})
        if len(batch)<30:return assets
        page+=1

def execute(paths,record,commit,tag=TAG,workers=3):
    api=API(credential());base='https://api.github.com/repos/'+REPOSITORY
    assert api.request('https://api.github.com/user')['login']=='edrisskrah131-lang'
    assert api.request(base)['permissions']['push']
    assert api.request(base+'/git/ref/heads/'+BRANCH)['object']['sha']==commit
    release=api.request(base+'/releases/tags/'+tag)
    existing=list_assets(api,base,release)
    assert len({p.name for p in paths})==len(paths)
    lock=Lock();verified=[];failed=[]
    def persist():
        result=dict(repository=REPOSITORY,branch=BRANCH,commit=commit,release_url=release['html_url'],
          remote_upload_verified=len(verified)==len(paths) and not failed,
          requested_assets=len(paths),verified_assets=verified,failed=failed)
        temp=record.with_suffix('.tmp');temp.write_text(json.dumps(result,indent=2),encoding='utf-8');temp.replace(record)
    def one(path):
        digest=sha(path);size=path.stat().st_size;asset=existing.get(path.name)
        for attempt in range(1,7):
            try:
                if attempt>1:
                    # Only this worker owns this unique name. Refresh after a
                    # disconnected response before retrying a POST.
                    fresh_assets=list_assets(api,base,release);asset=fresh_assets.get(path.name)
                if asset and asset.get('state')=='starter':
                    api.request(base+'/releases/assets/'+str(asset['id']),'DELETE');asset=None
                if asset is None:
                    print('UPLOAD_START',path.name,'attempt',attempt,flush=True)
                    url=release['upload_url'].split('{')[0]+'?name='+quote(path.name)
                    asset=api.upload_path(url,path) if size>8*1024**2 and os.name=='nt' else api.request(url,'POST',path.read_bytes(),'application/octet-stream')
                assert asset.get('state')=='uploaded','Incomplete remote asset'
                assert asset['size']==size,'Remote byte mismatch'
                assert asset.get('digest')=='sha256:'+digest,'Remote SHA256 mismatch'
                result=dict(file=path.name,sha256=digest,bytes=size,url=asset['browser_download_url'],verification='GitHub server SHA256 and byte count',state='uploaded')
                with lock:
                    verified.append(result);persist()
                    print('ASSET_VERIFIED',len(verified),'/',len(paths),path.name,flush=True)
                return
            except Exception as exc:
                print('RETRY_ASSET',path.name,attempt,type(exc).__name__,str(exc)[:180],flush=True)
                if attempt==6:
                    with lock:failed.append(dict(file=path.name,error=type(exc).__name__));persist()
                    return
                time.sleep(min(5*attempt,30))
    record.parent.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures=[pool.submit(one,p) for p in paths]
        for f in as_completed(futures):f.result()
    persist()
    print('BACKUP_COMPLETE',len(verified),len(paths),'FAILED',len(failed),flush=True)
    if failed:raise SystemExit(1)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['raw','reading','delivery'],required=True)
    ap.add_argument('--commit',required=True);ap.add_argument('--workers',type=int,default=3)
    ap.add_argument('--tag',default=TAG);args=ap.parse_args()
    repo=Path(__file__).resolve().parents[2];out=repo.parents[1]/'outputs'
    old=out/'R9_checkpoints';small=out/'R9_small';release=out/'R9_release';paths=[]
    if args.mode=='raw':
        indexes=list(small.glob('*_SMALL_INDEX.json'))
        assert len(indexes)==2
        indexes+= [p for p in old.glob('*_INDEX.json') if '_B_calibration_' not in p.name and '_B_confirmation_' not in p.name]
        assert len(indexes)==6
        for index_path in indexes:
            paths.append(index_path);index=json.loads(index_path.read_text())
            assert index['all_files_covered']
            for a in index['archives']:
                p=small/a['archive']
                if not p.exists():p=old/a['archive']
                assert p.exists()
                paths.extend([p,p.with_suffix('.json')])
        paths=sorted(set(paths),key=lambda p:(p.suffix=='.zip',p.stat().st_size))
    elif args.mode=='reading':
        paths=[release/'A20_AEI_R9_Reading_And_Handoff.zip',release/'A20_AEI_R9_Reading_And_Handoff.json']
    else:
        paths=sorted(p for p in release.iterdir() if p.is_file() and p.suffix in ('.zip','.json','.pdf','.md'))
    execute(paths,out/'R9_checkpoints'/('GITHUB_FINAL_'+args.mode.upper()+'.json'),args.commit,args.tag,args.workers)

if __name__=='__main__':main()
