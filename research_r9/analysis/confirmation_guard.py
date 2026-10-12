"""Verify scope/observer bindings before delegating unchanged frozen collection."""
from pathlib import Path
import sys,json,subprocess
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from runtime import HERE
from prospective_protocol import verify,sha

def main():
    verify()
    scope=json.loads((HERE/'protocol/attachment_scope_binding.json').read_text())
    observer=json.loads((HERE/'protocol/confirmation_observer_freeze.json').read_text())
    for binding in (scope,observer):
        for path,h in binding['files'].items():
            if sha(HERE/path)!=h:raise RuntimeError('Changed bound evidence layer: '+path)
    if sha(HERE/'protocol/selection_freeze.json')!=observer['selection_freeze_sha256']:
        raise RuntimeError('Changed selection freeze')
    command=[sys.executable,str(HERE/'source/collect_study.py'),*sys.argv[1:]]
    subprocess.run(command,check=True,cwd=HERE.parent)

if __name__=='__main__':main()
