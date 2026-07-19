#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, py_compile, tempfile, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path); a=ap.parse_args()
 if a.out:
  out=a.out.expanduser().resolve()
  if out==ROOT or ROOT in out.parents: raise SystemExit('--out must be outside sealed tree')
 checks=[]; failures=[]
 forbidden=[]
 for p in ROOT.rglob('*'):
  if p.name in {'__pycache__','.pytest_cache'} or p.suffix in {'.pyc','.pyo'}: forbidden.append(str(p.relative_to(ROOT)))
 checks.append({'name':'no_cache_artifacts','ok':not forbidden,'details':forbidden})
 for p in ROOT.rglob('*.json'):
  try: json.loads(p.read_text(encoding='utf-8'))
  except Exception as e: failures.append({'path':str(p.relative_to(ROOT)),'error':str(e)})
 checks.append({'name':'json_parse','ok':not failures,'details':failures})
 pyfails=[]
 with tempfile.TemporaryDirectory() as td:
  for p in ROOT.rglob('*.py'):
   try: py_compile.compile(str(p),cfile=str(Path(td)/(p.name+'.pyc')),doraise=True)
   except Exception as e: pyfails.append({'path':str(p.relative_to(ROOT)),'error':str(e)})
 checks.append({'name':'python_compile_external_cache','ok':not pyfails,'details':pyfails})
 unsafe=[]
 for p in ROOT.rglob('*'):
  rel=p.relative_to(ROOT)
  if any(x in {'..',''} for x in rel.parts) or p.is_symlink(): unsafe.append(str(rel))
 checks.append({'name':'safe_paths_no_symlinks','ok':not unsafe,'details':unsafe})
 obj={'schema':'nvsnvp.tree_validation.v2','status':'PASS' if all(c['ok'] for c in checks) else 'FAIL','checks':checks}
 txt=json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
 if a.out: a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(txt,encoding='utf-8')
 else: print(txt,end='')
 raise SystemExit(0 if obj['status']=='PASS' else 1)
if __name__=='__main__': main()
