from pathlib import Path
import json
from github_backup import API,credential,REPOSITORY,TAG
root=Path(__file__).resolve().parents[4]/'outputs/R9_checkpoints'
a=API(credential());base='https://api.github.com/repos/'+REPOSITORY
release=a.request(base+'/releases/tags/'+TAG);assets={};page=1
while True:
    batch=a.request(base+f'/releases/{release["id"]}/assets?per_page=30&page={page}')
    assets.update({x['name']:x for x in batch})
    print('ASSET_PAGE',page,len(batch),flush=True)
    if len(batch)<30:break
    page+=1
rows=[]
for prefix in ('A20_R9_B_calibration_complete_','A20_R9_B_confirmation_complete_'):
    for p in sorted(root.glob(prefix+'*.zip')):
        m=json.loads(p.with_suffix('.json').read_text());v=assets.get(p.name,{})
        ok=v.get('state')=='uploaded' and v.get('digest')=='sha256:'+m['sha256'] and v.get('size')==m['bytes']
        rows.append(dict(file=p.name,verified=ok,state=v.get('state'),bytes=m['bytes'],sha256=m['sha256']))
(root/'REMOTE_PHASE_SCAN.json').write_text(json.dumps(dict(release=release['html_url'],rows=rows,assets=assets),indent=2),encoding='utf-8')
for x in rows:print(x['file'],x['verified'],x['state'],flush=True)
