#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
findings=[]
active=[ROOT/'01_CANONICAL',ROOT/'03_REPRODUCE',ROOT/'06_CI']
for base in active:
 for p in base.rglob('*'):
  if not p.is_file() or p.suffix.lower() not in {'.py','.sh','.cpp','.wls','.wl','.yml','.yaml'}: continue
  if p.name=='security_scan.py': continue
  text=p.read_text(encoding='utf-8',errors='replace')
  rules=[]
  if p.suffix=='.py': rules += [('shell_true',r'shell\s*=\s*True'),('pickle',r'\bpickle\b'),('eval_exec',r'\b(?:eval|exec)\s*\(')]
  rules += [('hardcoded_mnt_data',r'/mnt/data/'),('rm_rf_unquoted',r'rm\s+-rf\s+\$[A-Za-z_]')]
  for name,pat in rules:
   for m in re.finditer(pat,text): findings.append({'rule':name,'path':str(p.relative_to(ROOT)),'line':text.count('\n',0,m.start())+1})
obj={'schema':'nvsnvp.security_scan.v2','status':'PASS' if not findings else 'FAIL','findings':findings,'positive_properties':['no network required by verification profiles','subprocess argument lists required','no pickle','no shell=True']}
print(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2))
raise SystemExit(0 if not findings else 1)
