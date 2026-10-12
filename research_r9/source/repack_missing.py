"""Repackage only unverified transport archives without changing research bytes."""
from pathlib import Path
import json,hashlib,zipfile
from package_phase import make_archive
repo=Path(__file__).resolve().parents[2]
old=repo.parents[1]/'outputs/R9_checkpoints'
out=repo.parents[1]/'outputs/R9_small';out.mkdir(exist_ok=True)
scan=json.loads((old/'REMOTE_PHASE_SCAN.json').read_text())
verified={r['file'] for r in scan['rows'] if r['verified']}
for phase in ('calibration','confirmation'):
    index_path=next(old.glob(f'A20_R9_B_{phase}_complete_*_INDEX.json'))
    original=json.loads(index_path.read_text());replacement=[]
    root=repo/original['restore_prefix']
    for archive in original['archives']:
        if archive['archive'] in verified or '_tables.' in archive['archive']:
            replacement.append(archive);continue
        entries=archive['entries'];assert len(entries)%3==0
        part=[];weight=0;part_number=0
        def flush(paths):
            global part_number
            part_number+=1
            name=Path(archive['archive']).stem+f'_small_{part_number:02}'
            return make_archive(root,paths,out,name,original['restore_prefix'])
        for offset in range(0,len(entries),3):
            group=entries[offset:offset+3]
            assert group[0]['path'].endswith('.json')
            paths=[root/e['path'] for e in group]
            for path,e in zip(paths,group):
                assert path.stat().st_size==e['bytes']
                assert hashlib.sha256(path.read_bytes()).hexdigest()==e['sha256']
            size=sum(e['bytes'] for e in group)
            if weight+size>64*1024**2 and part:
                replacement.append(flush(part));part=[];weight=0
            part+=paths;weight+=size
        if part:replacement.append(flush(part))
    def entries_map(archives):
        result={}
        for archive in archives:
            for e in archive['entries']:
                assert e['path'] not in result
                result[e['path']]=(e['bytes'],e['sha256'])
        return result
    assert entries_map(original['archives'])==entries_map(replacement)
    updated={**original,'archives':replacement,'transport_repack_only':True,
      'original_index':index_path.name,'member_bytes_hashes_identical':True,
      'reason':'Interrupted large uploads; reuse verified archives and replace missing archives by complete small ZIPs.'}
    (out/(index_path.stem.replace('_INDEX','_SMALL_INDEX')+'.json')).write_text(json.dumps(updated,indent=2),encoding='utf-8')
    print('REPACK_VERIFIED',phase,len(replacement),len(entries_map(replacement)),flush=True)
