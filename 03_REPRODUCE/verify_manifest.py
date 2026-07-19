#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; M=ROOT/'07_MANIFEST/MANIFEST.json'; S=ROOT/'07_MANIFEST/MANIFEST_SEAL.json'
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads(M.read_text(encoding='utf-8')); seal=json.loads(S.read_text(encoding='utf-8')); errors=[]
if h(M)!=seal['manifest_sha256']: errors.append('manifest seal mismatch')
for r in manifest['files']:
 p=ROOT/r['path']
 if not p.is_file(): errors.append(f"missing {r['path']}")
 elif p.stat().st_size!=r['size_bytes'] or h(p)!=r['sha256']: errors.append(f"mismatch {r['path']}")
print(json.dumps({'status':'PASS' if not errors else 'FAIL','checked':len(manifest['files']),'errors':errors},indent=2));raise SystemExit(0 if not errors else 1)
