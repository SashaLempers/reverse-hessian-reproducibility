#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'05_PROVENANCE/PROVENANCE_MAP.csv'
SKIP={'.git','.work','__pycache__','.pytest_cache'}
SKIP_SUFFIXES={'.pyc','.pyo','.aux','.bbl','.blg','.fdb_latexmk','.fls','.log','.out','.synctex.gz'}
MODIFIED=set(subprocess.check_output(
    ['git','-C',str(ROOT),'diff','--name-only','-z','HEAD','--']
).decode('utf-8',errors='surrogateescape').split('\0'))
def h(p):
    x=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): x.update(block)
    return x.hexdigest()

def canonical_bytes(p, rel):
    if rel.startswith('07_MANIFEST/') or rel not in MODIFIED:
        return subprocess.check_output(['git','-C',str(ROOT),'show',f'HEAD:{rel}'])
    oid=subprocess.check_output([
        'git','-C',str(ROOT),'hash-object','-w',f'--path={rel}','--filters',str(p)
    ],text=True).strip()
    return subprocess.check_output(['git','-C',str(ROOT),'cat-file','blob',oid])
rows=[]
for p in sorted(ROOT.rglob('*'),key=lambda item:item.relative_to(ROOT).as_posix()):
    if not p.is_file() or p==out: continue
    relp=p.relative_to(ROOT)
    if any(part in SKIP for part in relp.parts): continue
    if any(p.name.endswith(s) for s in SKIP_SUFFIXES): continue
    rel=relp.as_posix()
    if rel.startswith('01_CANONICAL/'): role='canonical'
    elif rel.startswith('04_EVIDENCE/'): role='reproduction_evidence'
    elif rel.startswith('05_PROVENANCE/'): role='provenance_or_history_index'
    elif rel.startswith('07_MANIFEST/'): role='generated_manifest'
    else: role='release_metadata_or_tool'
    data=canonical_bytes(p,rel)
    rows.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest(),'size_bytes':len(data),'role':role,'canonical_or_generated':'canonical' if role=='canonical' else 'generated_or_evidence','superseded':'no'})
with out.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator='\n');w.writeheader();w.writerows(rows)
print(len(rows))
