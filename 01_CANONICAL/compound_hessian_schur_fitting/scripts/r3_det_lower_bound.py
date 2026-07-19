#!/usr/bin/env python3
from __future__ import annotations
import itertools,json,sys,time,argparse
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import compound_hessian_r2 as ch
from compound_hessian_r3_s0 import det3_poly,normalize

def add_row(row,piv,p):
 row={k:v%p for k,v in row.items() if v%p}
 while row:
  lead=min(row)
  if lead not in piv:
   inv=pow(row[lead],-1,p);row={k:(v*inv)%p for k,v in row.items() if (v*inv)%p};piv[lead]=row;return True
  f=row[lead]
  for k,v in piv[lead].items():
   z=(row.get(k,0)-f*v)%p
   if z:row[k]=z
   elif k in row:del row[k]
 return False

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--target',type=int,default=850);a=ap.parse_args()
 f=ch.det4_terms();H=ch.hessian(f);ts=list(itertools.combinations(range(16),3));seen=set();piv={};tested=nonzero=0;t=time.time();witness=[]
 done=False
 for ai,I in enumerate(ts):
  for J in ts[ai:]:
   q=det3_poly(H,I,J);tested+=1
   if not q:continue
   nonzero+=1;k=normalize(q)
   if k in seen:continue
   seen.add(k)
   if add_row(q,piv,1009):
    witness.append({'I':list(I),'J':list(J)})
    if len(piv)>=a.target:done=True;break
  if done:break
 rec={'schema':'reverse_hessian.r3_det_lower_bound.v1','prime':1009,'target_rank':a.target,'rank_mod_p_lower_bound':len(piv),'rank_Q_lower_bound':len(piv),'tested_symmetric_coordinates':tested,'nonzero_coordinates_seen':nonzero,'unique_generators_seen':len(seen),'witness_generator_labels':witness,'elapsed_seconds':round(time.time()-t,3),'reason':'rank over F_p is at most rank over Q for the same integer coefficient matrix'}
 a.out.write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n');print({k:v for k,v in rec.items() if k!='witness_generator_labels'})
if __name__=='__main__':main()
