#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,stat,zipfile
from pathlib import Path
EPOCH=(2026,7,18,0,0,0)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args();src=a.source.resolve();out=a.output.resolve()
 out.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as z:
  for p in sorted(src.rglob('*')):
   if not p.is_file(): continue
   rel=(Path(src.name)/p.relative_to(src)).as_posix(); info=zipfile.ZipInfo(rel,EPOCH); mode=p.stat().st_mode&0o777
   info.create_system=3;info.external_attr=(stat.S_IFREG|mode)<<16;info.compress_type=zipfile.ZIP_DEFLATED
   z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
if __name__=='__main__':main()
