"""Fresh remote audit before any local research cleanup."""
from pathlib import Path
import json,subprocess,hashlib,urllib.request
from github_backup import API,credential,REPOSITORY,BRANCH,TAG
from resumable_backup import list_assets
repo=Path(__file__).resolve().parents[2];out=repo.parents[1]/'outputs';cp=out/'R9_checkpoints'
api=API(credential());base='https://api.github.com/repos/'+REPOSITORY
expected={}
for name in ['GITHUB_UPLOAD_01.json','GITHUB_UPLOAD_02.json','GITHUB_UPLOAD_03.json','GITHUB_UPLOAD_04.json','GITHUB_FINAL_RAW.json','GITHUB_FINAL_READING.json','GITHUB_FINAL_DELIVERY.json']:
    d=json.loads((cp/name).read_text());assert d['remote_upload_verified'],name
    for a in d['verified_assets']:
        key=a['url'];assert key not in expected or expected[key]['sha256']==a['sha256'];expected[key]=a
verified=[]
for tag in [TAG,'r9-data-complete-20261012']:
    rel=api.request(base+'/releases/tags/'+tag);assets=list_assets(api,base,rel)
    for url,e in expected.items():
        if '/download/'+tag+'/' not in url:continue
        a=assets[e['file']]
        assert a['state']=='uploaded' and a['size']==e['bytes'] and a['digest']=='sha256:'+e['sha256'],e['file']
        verified.append(e)
assert len(verified)==len(expected)
# Historical archive hashes from the original manifest are checked again.
manifest=json.loads((repo.parent/'github_snapshot/GITHUB_ASSET_MANIFEST.json').read_text())
print('HISTORICAL_MANIFEST_TYPE',type(manifest).__name__,flush=True)
rel=api.request(base+'/releases/tags/r8-handoff-2026-10-12');historical=list_assets(api,base,rel)
for e in manifest:
    a=historical[e['filename']]
    assert a['state']=='uploaded' and a['size']==e['bytes'] and a.get('digest')=='sha256:'+e['sha256'],e['filename']
# Preserve the refreshed historical listing after exact manifest comparisons.
hist=[dict(file=a['name'],bytes=a['size'],sha256=a.get('digest'),state=a['state'],url=a['browser_download_url']) for a in historical.values()]
assert all(a['state']=='uploaded' for a in hist)
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
assert api.request(base+'/git/ref/heads/'+BRANCH)['object']['sha']==commit
# Public no-credential full download verifies the small handoff end to end.
reading=next(e for e in verified if e['file']=='A20_AEI_R9_Restored_Reading_And_Handoff.zip')
h=hashlib.sha256();n=0
with urllib.request.urlopen(urllib.request.Request(reading['url'],headers={'User-Agent':'A20-R9-public-check'}),timeout=120) as r:
    for block in iter(lambda:r.read(1024*1024),b''):h.update(block);n+=len(block)
assert n==reading['bytes'] and h.hexdigest()==reading['sha256']
result=dict(status='PASS',remote_upload_verified=True,branch=BRANCH,code_commit=commit,verified_release_assets=verified,historical_remote_assets=hist,public_reading_download_sha256=h.hexdigest(),raw_independent_inputs=12800,canonical_raw_assets=176,all_local_deletion_requires_this_record=True,paper_status='45-page restored draft, not submission-ready or author-approved final')
(repo/'research_r9/audits/FINAL_REMOTE_CLOSURE.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
(out/'FINAL_REMOTE_CLOSURE.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('FINAL_REMOTE_CLOSURE_PASS',len(verified),commit,flush=True)
