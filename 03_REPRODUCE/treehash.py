#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os
from pathlib import Path
EXCLUDE={'.git','__pycache__','.pytest_cache'}
def file_hash(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def snapshot(root):
 root=root.resolve(); rows=[]
 for p in sorted(root.rglob('*')):
  rel=p.relative_to(root).as_posix()
  if any(part in EXCLUDE for part in p.parts): continue
  if p.is_symlink(): rows.append({'path':rel,'type':'symlink','target':os.readlink(p)})
  elif p.is_file(): rows.append({'path':rel,'type':'file','size':p.stat().st_size,'mode':oct(p.stat().st_mode & 0o777),'sha256':file_hash(p)})
 raw=json.dumps(rows,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
 return {'root_label':root.name,'file_count':sum(r['type']=='file' for r in rows),'entry_count':len(rows),'tree_sha256':hashlib.sha256(raw).hexdigest(),'entries':rows}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('root',type=Path); ap.add_argument('--out',type=Path); a=ap.parse_args(); obj=snapshot(a.root)
 txt=json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+'\n'
 if a.out: a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(txt,encoding='utf-8')
 else: print(txt,end='')
if __name__=='__main__': main()
