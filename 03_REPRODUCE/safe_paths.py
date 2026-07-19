#!/usr/bin/env python3
from pathlib import Path
import shutil
def checked_external(path, sealed_root):
 p=Path(path).expanduser().resolve(); root=Path(sealed_root).resolve()
 if str(path).strip() in {'','/','.','..'} or p in {Path('/'),Path('.').resolve(),root} or root in p.parents or p.parent==p:
  raise ValueError(f'unsafe external path: {p}')
 if p.is_symlink(): raise ValueError('workspace root may not be a symlink')
 return p
def safe_rmtree(path, sealed_root):
 p=checked_external(path,sealed_root)
 if p.exists(): shutil.rmtree(p)
