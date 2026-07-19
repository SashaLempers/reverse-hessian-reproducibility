#!/usr/bin/env python3
from __future__ import annotations
import json,time,sys,argparse
from pathlib import Path
import sympy as sp
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
import compound_hessian_r2 as ch

def run(name,f):
 H=ch.hessian(f);labs,cs=ch.compound2_symmetric(H);gs=ch.unique_nonzero_components(cs)
 cols=list(ch.multiset_monomials(ch.N,ch.Q));ci={m:i for i,m in enumerate(cols)}
 data={i:{ci[m]:ZZ(v) for m,v in g.items()} for i,g in enumerate(gs)}
 M=DomainMatrix(data,(len(gs),len(cols)),ZZ);t=time.time();r=int(M.rank())
 return {'form':name,'matrix_shape':list(M.shape),'nnz':sum(len(g) for g in gs),'rank_Q_exact':r,'rank_seconds':round(time.time()-t,3)}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 out={'schema':'reverse_hessian.fitting_s0_exact.v1','records':[run('det4',ch.det4_terms()),run('z_per3',ch.padded_per3_terms())]}
 a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out)
if __name__=='__main__':main()
