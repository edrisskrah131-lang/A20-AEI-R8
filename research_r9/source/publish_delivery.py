"""Publish the explicitly authorized data archive; the manuscript remains a draft."""
from pathlib import Path
import json,subprocess
from github_backup import API,credential,REPOSITORY,BRANCH,TAG
from resumable_backup import execute
repo=Path(__file__).resolve().parents[2];out=repo.parents[1]/'outputs'
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
raw=json.loads((out/'R9_checkpoints/GITHUB_FINAL_RAW.json').read_text());assert raw['remote_upload_verified']
api=API(credential());base='https://api.github.com/repos/'+REPOSITORY
assert api.request('https://api.github.com/user')['login']=='edrisskrah131-lang'
assert api.request(base+'/git/ref/heads/'+BRANCH)['object']['sha']==commit
final_tag='r9-data-complete-20261012'
body="""## R9 data archive complete; restored manuscript is a draft

All six new simulation phases are remotely verified: 12,800 independent inputs, 38,400 raw files, 176 canonical archive/index/manifest assets and 8,084,697,189 compressed archive bytes. Read R9_DATA_DOWNLOAD_CN.md and R9_DATA_CATALOG.json for the exact complete set. Large raw data remain in the checkpoint release; no second large download is needed.

**The earlier 17-page R9 manuscript was rejected by the author for removing the original research from the main paper. Do not use it as the current manuscript.** The 45-page Restored_Draft restores R8 equations, methods, proofs, figures and localization/route results, then adds the new task study. It needs editorial synthesis and independent review; data-backup completion is not a claim of 9/10, acceptance or submission readiness.

Start with A20_AEI_R9_Restored_Reading_And_Handoff.zip. Editable source and original/R9 figures are separate. R8/A19/A20 history remains in the historical release. The complete procedural comparator matches the semantic system; direct renewal supports more requests, and full reporting remains uncertified at 0.15.

[Latest R9 branch](https://github.com/edrisskrah131-lang/A20-AEI-R8/tree/r9-rebuild-20261012) · [Raw checkpoints](https://github.com/edrisskrah131-lang/A20-AEI-R8/releases/tag/r9-checkpoints-20261012) · [Historical R8 release](https://github.com/edrisskrah131-lang/A20-AEI-R8/releases/tag/r8-handoff-2026-10-12)
"""
try:release=api.request(base+'/releases/tags/'+final_tag)
except RuntimeError as exc:
    if 'HTTP 404' not in str(exc):raise
    release=api.request(base+'/releases','POST',dict(tag_name=final_tag,target_commitish=commit,name='R9 data complete and restored manuscript draft',body=body,prerelease=True))
else:api.request(base+'/releases/'+str(release['id']),'PATCH',dict(body=body,prerelease=True))
checkpoint=api.request(base+'/releases/tags/'+TAG)
api.request(base+'/releases/'+str(checkpoint['id']),'PATCH',dict(body='Raw research checkpoints. All six formal phases are now complete: use the authoritative R9_DATA_CATALOG.json in the [data handoff release](https://github.com/'+REPOSITORY+'/releases/tag/'+final_tag+'). B calibration/confirmation use SMALL_INDEX. Earlier incomplete large-upload placeholders are not part of the canonical set. The earlier 17-page paper and reading package are superseded; use the restored draft from the data handoff release.'))
paths=sorted([p for p in (out/'R91_delivery').iterdir() if p.is_file()],key=lambda p:p.stat().st_size)
execute(paths,out/'R9_checkpoints/GITHUB_FINAL_DELIVERY.json',commit,final_tag,3)
print('DELIVERY_RELEASE',release['html_url'],flush=True)
