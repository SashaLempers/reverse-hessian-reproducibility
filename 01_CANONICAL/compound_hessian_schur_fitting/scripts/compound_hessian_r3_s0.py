#!/usr/bin/env python3
"""Exact construction of 3x3 Hessian minors for det4 and z*per3.
Computes the degree-6 span [I_3(f)]_6 over Q when feasible.
"""
from __future__ import annotations
import argparse,itertools,json,math,sys,time
from pathlib import Path
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
import compound_hessian_r2 as ch

def det3_poly(H,I,J):
 out={}
 for p in itertools.permutations(range(3)):
  s=ch.perm_sign(p);q={():1}
  for a in range(3):q=ch.poly_mul(q,H[I[a]][J[p[a]]])
  out=ch.poly_add(out,q,s)
 return out

def normalize(poly):return ch.normalized_poly_key(poly)

def run(name,f,exact=True):
 t=time.time();H=ch.hessian(f);triples=list(itertools.combinations(range(ch.N),3));seen={};nonzero=0
 for ai,I in enumerate(triples):
  for J in triples[ai:]:
   p=det3_poly(H,I,J)
   if p:
    nonzero+=1;k=normalize(p)
    if k not in seen:seen[k]=p
  if (ai+1)%50==0:print(name,'I',ai+1,'unique',len(seen),'nonzero',nonzero,flush=True)
 gs=list(seen.values());build=time.time()-t
 rec={'form':name,'r':3,'symmetric_coordinates':len(triples)*(len(triples)+1)//2,'nonzero_coordinates':nonzero,'unique_nonzero_up_to_scalar':len(gs),'generator_nnz':sum(len(g) for g in gs),'build_seconds':round(build,3)}
 if exact:
  cols=list(ch.multiset_monomials(ch.N,6));ci={m:i for i,m in enumerate(cols)}
  data={i:{ci[m]:ZZ(v) for m,v in g.items()} for i,g in enumerate(gs)};M=DomainMatrix(data,(len(gs),len(cols)),ZZ);t2=time.time();rank=int(M.rank())
  rec.update({'matrix_shape':list(M.shape),'rank_Q_exact':rank,'rank_seconds':round(time.time()-t2,3)})
 return rec

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--forms',choices=('both','det4','z_per3'),default='both');a=ap.parse_args()
 forms=[('det4',ch.det4_terms()),('z_per3',ch.padded_per3_terms())]
 if a.forms!='both':forms=[x for x in forms if x[0]==a.forms]
 rec=[]
 for name,f in forms:
  x=run(name,f);print(x,flush=True);rec.append(x)
 a.out.write_text(json.dumps({'schema':'reverse_hessian.compound_hessian_r3_s0.v1','records':rec},indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
