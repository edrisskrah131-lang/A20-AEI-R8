"""Archive an existing research stage; never invent missing run evidence."""
from pathlib import Path
import argparse, hashlib, json, zipfile
from datetime import datetime, timezone

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--stage', required=True)
    ap.add_argument('--exclude-data',action='store_true')
    ap.add_argument('--parent-archive')
    args = ap.parse_args()
    root = args.root.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in root.rglob('*') if p.is_file()
                   and '.git' not in p.parts and '__pycache__' not in p.parts
                   and not (args.exclude_data and p.relative_to(root).parts[0]=='data'))
    entries = [dict(path=p.relative_to(root).as_posix(), bytes=p.stat().st_size,
                    sha256=sha(p)) for p in files]
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    name = f'A20_R9_{args.stage}_{stamp}'
    archive = args.output / (name + '.zip')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for p, item in zip(files, entries):
            z.write(p, item['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for item in entries:
            assert hashlib.sha256(z.read(item['path'])).hexdigest() == item['sha256']
    manifest = dict(stage=args.stage, utc=datetime.now(timezone.utc).isoformat(),
                    archive=archive.name, bytes=archive.stat().st_size,
                    sha256=sha(archive), entries=entries,
                    excluded_data=args.exclude_data,parent_archive=args.parent_archive,
                    remote_upload_verified=False,
                    note='Update remote status only after GitHub readback.')
    (args.output / (name + '.json')).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k != 'entries'}), flush=True)

if __name__ == '__main__':
    main()
