#!/usr/bin/env python3
"""Normalize JSON certificates by removing known runtime-only fields."""
from __future__ import annotations
import argparse,json
from pathlib import Path
DROP={'elapsed_seconds','absolute_path','cwd','hostname','timestamp','started_at','finished_at','platform','python_executable'}

def clean(x):
    if isinstance(x,dict): return {k:clean(v) for k,v in sorted(x.items()) if k not in DROP}
    if isinstance(x,list): return [clean(v) for v in x]
    return x

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('directory',nargs='?',type=Path,default=Path('certificates')); a=ap.parse_args()
    for p in sorted(a.directory.glob('*.json')):
        obj=clean(json.loads(p.read_text(encoding='utf-8')))
        p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')
        print('normalized',p.name)
    return 0
if __name__=='__main__': raise SystemExit(main())
