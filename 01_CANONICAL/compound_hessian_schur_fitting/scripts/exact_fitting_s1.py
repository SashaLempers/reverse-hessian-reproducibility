#!/usr/bin/env python3
from __future__ import annotations
import json,time,sys,argparse
from pathlib import Path
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
import compound_hessian_r2 as ch

def run(name,f,s=1):
 H=ch.hessian(f);labs,cs=ch.compound2_symmetric(H);gs=ch.unique_nonzero_components(cs)
 degree=ch.Q+s;cols=list(ch.multiset_monomials(ch.N,degree));ci={m:i for i,m in enumerate(cols)}
 data={};ri=0;nnz=0
 for _,row in ch.fitting_rows(gs,s):
  if row:
   data[ri]={ci[m]:ZZ(v) for m,v in row.items()};nnz+=len(row)
  ri+=1
 M=DomainMatrix(data,(ri,len(cols)),ZZ);t=time.time();r=int(M.rank())
 return {'form':name,'s':s,'matrix_shape':list(M.shape),'nnz':nnz,'rank_Q_exact':r,'rank_seconds':round(time.time()-t,3)}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 rec=[]
 for name,f in [('det4',ch.det4_terms()),('z_per3',ch.padded_per3_terms())]:
  x=run(name,f);print(x,flush=True);rec.append(x)
 out={'schema':'reverse_hessian.fitting_s1_exact.v1','records':rec};a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
