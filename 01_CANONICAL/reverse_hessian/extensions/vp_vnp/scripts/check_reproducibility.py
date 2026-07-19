#!/usr/bin/env python3
"""Compare the current build with one fresh isolated rebuild byte-for-byte.

The documented workflow is:
  python run_all.py
  python scripts/check_reproducibility.py
Thus the current certificate directory is run 1 and the temporary rebuild is
run 2.
"""
from __future__ import annotations
import argparse,hashlib,subprocess,sys,tempfile
from pathlib import Path
SCRIPT_DIR=Path(__file__).resolve().parent
PACKAGE_ROOT=SCRIPT_DIR.parent

def hashes(d):
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((d/'certificates').glob('*')) if p.is_file()}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--skip-exploratory',action='store_true'); a=ap.parse_args()
    current=hashes(PACKAGE_ROOT)
    if not current: raise SystemExit('No current certificates: run python run_all.py first.')
    with tempfile.TemporaryDirectory(prefix='rh_repro_') as td:
        fresh=Path(td)/'fresh'
        cmd=[sys.executable,str(SCRIPT_DIR/'run_all.py'),'--output-root',str(fresh)]
        if a.skip_exploratory: cmd.append('--skip-exploratory')
        subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        rebuilt=hashes(fresh)
    if current!=rebuilt:
        diff={k:(current.get(k),rebuilt.get(k)) for k in sorted(set(current)|set(rebuilt)) if current.get(k)!=rebuilt.get(k)}
        raise SystemExit('NONREPRODUCIBLE: '+repr(diff))
    print('BIT-FOR-BIT REPRODUCIBLE:',len(current),'certificate files')
    return 0
if __name__=='__main__': raise SystemExit(main())
