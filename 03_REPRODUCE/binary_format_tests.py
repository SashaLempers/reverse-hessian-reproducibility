#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, struct, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'01_CANONICAL/compound_hessian_schur_fitting/scripts/exact_projected_rank.py'
spec=importlib.util.spec_from_file_location('reader',SCRIPT); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
def base_bytes():
 return b'RHT6v1\0\0'+struct.pack('<II',16,120)+b''.join(struct.pack('<BBHI',0,1,0,0) for _ in range(120))
def expect_fail(data,label):
 with tempfile.NamedTemporaryFile(delete=False) as f: f.write(data); path=Path(f.name)
 try:
  try: mod.read(path)
  except Exception: return {'case':label,'ok':True}
  return {'case':label,'ok':False,'error':'accepted invalid file'}
 finally: path.unlink(missing_ok=True)
b=base_bytes(); cases=[
 expect_fail(b'BADMAGIC'+b[8:],'bad_magic'),expect_fail(b[:10],'truncated'),
 expect_fail(b[:18]+b'\x01\x00'+b[20:],'bad_pad'),
 expect_fail(b[:16]+bytes([16])+b[17:],'value_out_of_range_row_index'),
 expect_fail(b[:20]+struct.pack('<I',50_000_001)+b[24:],'impossible_nnz'),
 expect_fail(b+b'X','trailing_byte')]
obj={'schema':'nvsnvp.binary_negative_tests.v2','status':'PASS' if all(c['ok'] for c in cases) else 'FAIL','cases':cases,'format_magic':'RHT6v1\\0\\0'}
print(json.dumps(obj,sort_keys=True,indent=2)); raise SystemExit(0 if obj['status']=='PASS' else 1)
