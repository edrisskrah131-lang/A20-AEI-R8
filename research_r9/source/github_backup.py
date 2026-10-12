"""Explicitly authorized GitHub checkpoint publication with remote verification.

Credentials stay in memory and come from the existing Git credential manager.
No token is accepted as a command argument, stored in a file, or printed.
Default mode is read-only. --publish uploads only the named validated assets.
"""
from pathlib import Path
import argparse, hashlib, json, os, subprocess, urllib.request, urllib.error
from urllib.parse import quote

REPOSITORY = 'edrisskrah131-lang/A20-AEI-R8'
BRANCH = 'r9-rebuild-20261012'
TAG = 'r9-checkpoints-20261012'

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for data in iter(lambda:f.read(1024*1024),b''):h.update(data)
    return h.hexdigest()

def credential():
    requested=('protocol=https\nhost=github.com\nusername=edrisskrah131-lang\n'
               'path=edrisskrah131-lang/A20-AEI-R8.git\n\n')
    env={**os.environ,'GIT_TERMINAL_PROMPT':'0','GCM_INTERACTIVE':'Never'}
    p=subprocess.run(['git','credential','fill'],input=requested,text=True,
                     capture_output=True,env=env,timeout=20)
    if p.returncode:
        raise RuntimeError('No authorized edr credential is available; complete official GitHub login.')
    values=dict(line.split('=',1) for line in p.stdout.splitlines() if '=' in line)
    secret=values.get('password')
    if not secret:raise RuntimeError('Credential manager returned no credential.')
    return secret

class API:
    def __init__(self,secret):self.secret=secret
    def request(self,url,method='GET',body=None,content_type='application/json'):
        if not url.startswith(('https://api.github.com/','https://uploads.github.com/')):
            raise ValueError('Unexpected credential destination')
        if body is not None and not isinstance(body,bytes):body=json.dumps(body).encode()
        req=urllib.request.Request(url,data=body,method=method,headers={
            'Authorization':'Bearer '+self.secret,'Accept':'application/vnd.github+json',
            'X-GitHub-Api-Version':'2026-03-10','Content-Type':content_type,
            'User-Agent':'A20-R9-verified-backup'})
        try:
            with urllib.request.urlopen(req,timeout=600) as r:
                return None if r.status==204 else json.load(r)
        except urllib.error.HTTPError as e:
            # Avoid displaying request headers, response bodies or credentials.
            raise RuntimeError(f'GitHub returned HTTP {e.code} for {method} {url.split("?")[0]}') from None

def publish_assets(api,assets,commit):
    base='https://api.github.com/repos/'+REPOSITORY
    try:release=api.request(base+'/releases/tags/'+TAG)
    except RuntimeError as e:
        if 'HTTP 404' not in str(e):raise
        release=api.request(base+'/releases','POST',dict(tag_name=TAG,target_commitish=commit,
            name='A20 AEI R9 — verified research checkpoints',prerelease=True,
            body='In-progress research. Code, prospective protocols and actual execution checkpoints. '
                 'No claim of final acceptance or completed formal study. Per-asset SHA256 manifests accompany archives.'))
    existing={};page=1
    while True:
        batch=api.request(base+f'/releases/{release["id"]}/assets?per_page=100&page={page}')
        existing.update({a['name']:a for a in batch})
        if len(batch)<100:break
        page+=1
    verified=[]
    for path in assets:
        digest=sha(path)
        asset=existing.get(path.name)
        if asset is not None and asset.get('state')=='starter' and asset.get('size')==0:
            # An interrupted upload of this exact named checkpoint left no data.
            api.request(base+'/releases/assets/'+str(asset['id']),'DELETE');asset=None
        if asset is None:
            # Archive sizes are kept below 1 GB by the stage packager.
            if path.stat().st_size>1024**3:raise ValueError('Split this checkpoint before publication.')
            url=release['upload_url'].split('{')[0]+'?name='+quote(path.name)
            asset=api.request(url,'POST',path.read_bytes(),'application/octet-stream')
        fresh=api.request(base+'/releases/assets/'+str(asset['id']))
        server=fresh.get('digest')
        if fresh['size']!=path.stat().st_size:raise RuntimeError('Remote checkpoint byte count differs')
        if server:
            if server!='sha256:'+digest:raise RuntimeError('Remote checkpoint digest differs')
            check='GitHub server SHA256 and byte count'
        else:
            h=hashlib.sha256()
            req=urllib.request.Request(fresh['browser_download_url'],headers={'User-Agent':'A20-R9-verified-backup'})
            with urllib.request.urlopen(req,timeout=600) as r:
                for data in iter(lambda:r.read(1024*1024),b''):h.update(data)
            if h.hexdigest()!=digest:raise RuntimeError('Downloaded checkpoint digest differs')
            check='Full public-download SHA256 and byte count'
        verified.append(dict(file=path.name,sha256=digest,bytes=fresh['size'],
                             url=fresh['browser_download_url'],verification=check))
        print('VERIFIED_ASSET',path.name,flush=True)
    return release['html_url'],verified

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--publish',action='store_true')
    ap.add_argument('--asset',type=Path,action='append',default=[])
    ap.add_argument('--commit',required=True);ap.add_argument('--record',type=Path,required=True)
    args=ap.parse_args()
    paths=[p.resolve(strict=True) for p in args.asset]
    if any(p.suffix.lower() not in ('.zip','.json','.pdf','.md','.gz','.npz') for p in paths):
        raise ValueError('Unsupported checkpoint format')
    record=dict(repository=REPOSITORY,branch=BRANCH,commit=args.commit,
                assets=[dict(file=p.name,bytes=p.stat().st_size,sha256=sha(p)) for p in paths],
                remote_upload_verified=False)
    if args.publish:
        api=API(credential())
        who=api.request('https://api.github.com/user')['login']
        repo=api.request('https://api.github.com/repos/'+REPOSITORY)
        if not repo.get('permissions',{}).get('push'):
            raise RuntimeError(f'{who} has no push permission for the requested repository')
        ref=api.request('https://api.github.com/repos/'+REPOSITORY+'/git/ref/heads/'+BRANCH)
        if ref['object']['sha']!=args.commit:raise RuntimeError('Push and verify the code commit before publishing its checkpoint')
        release,verified=publish_assets(api,paths,args.commit)
        record.update(remote_upload_verified=True,authenticated_login=who,release_url=release,verified_assets=verified)
    args.record.parent.mkdir(parents=True,exist_ok=True)
    args.record.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(remote_upload_verified=record['remote_upload_verified'],
                         repository=REPOSITORY,assets=len(paths)),ensure_ascii=False),flush=True)

if __name__=='__main__':main()
