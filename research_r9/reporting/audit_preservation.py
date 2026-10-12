"""Verify that revision keeps the original displayed evidence and core chapters."""
from pathlib import Path
import argparse,hashlib,json,re

def expanded(root,text):
    return re.sub(r'\\input\{([^}]+)\}',lambda m:expanded(root,(root/(m.group(1)+'.tex')).read_text(encoding='utf-8')),text)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--baseline',type=Path,required=True);ap.add_argument('--paper',type=Path,default=Path(__file__).resolve().parents[1]/'paper');ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    a=expanded(args.baseline,(args.baseline/'main.tex').read_text(encoding='utf-8'));b=expanded(args.paper,(args.paper/'main.tex').read_text(encoding='utf-8'))
    patterns={'figures':r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',
      'equations':r'\\begin\{equation\}(.*?)\\end\{equation\}',
      'tables':r'\\begin\{tabular(?:x)?\}(.*?)\\end\{tabular(?:x)?\}',
      'formal_results':r'\\begin\{(?:theorem|proposition)\}(.*?)\\end\{(?:theorem|proposition)\}'}
    checks={}
    for name,pattern in patterns.items():
        items=re.findall(pattern,a,re.S);checks[name]=dict(original_count=len(items),present_count=sum(x in b for x in items),all_retained=all(x in b for x in items))
    core={}
    for name in ['r8_formulation.tex','r8_knowledge.tex','r8_method.tex','r8_theory.tex']:
        x=(args.baseline/'sections'/name).read_bytes();y=(args.paper/'sections'/name).read_bytes();core[name]=dict(byte_identical=x==y,sha256=hashlib.sha256(y).hexdigest())
    ok=all(x['all_retained'] and x['original_count']>0 for x in checks.values()) and all(x['byte_identical'] for x in core.values())
    result=dict(status='PASS' if ok else 'FAIL',checks=checks,core_sections=core,scope='Content retention only; does not establish research quality or author approval.')
    args.output.write_text(json.dumps(result,indent=2),encoding='utf-8');print(result['status'])
    if not ok:raise SystemExit(1)
if __name__=='__main__':main()
