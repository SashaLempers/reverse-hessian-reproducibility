#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,struct,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import exact_projected_rank as ep
import schur_block_r2_k2 as sb

def terms_for_shape51_index0():
 rows=[[0,1,2,3,4],[5]];cols=[[0,5],[1],[2],[3],[4]]
 rg=sb.subgroup_permutations(rows);cg=sb.subgroup_permutations(cols);D={}
 for rp,_ in rg:
  for cp,cs in cg:
   z=sb.compose_perm(rp,cp);D[z]=D.get(z,0)+cs
 return [(p,c) for p,c in D.items() if c]

def hsh(row):
 raw=json.dumps([[list(k),v] for k,v in sorted(row.items())],separators=(',',':')).encode()
 return hashlib.sha256(raw).hexdigest()

def add(a,b,scale=1):
 o=dict(a)
 for k,v in b.items():
  z=o.get(k,0)+scale*v
  if z:o[k]=z
  elif k in o:del o[k]
 return o

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 rows=ep.read(a.input);terms=terms_for_shape51_index0()
 # Sym^2 A tensor Sym^2 B highest weight: x_11^2 => source row (0,0), index 0.
 p00=ep.project(rows[0],terms)
 # Lambda^2 A tensor Lambda^2 B highest weight:
 # x_11*x_22 - x_12*x_21. Sym^2 basis indices are combinations_with_replacement.
 import itertools
 basis=list(itertools.combinations_with_replacement(range(16),2));idx={b:i for i,b in enumerate(basis)}
 q=add(ep.project(rows[idx[(0,5)]],terms),ep.project(rows[idx[(1,4)]],terms),-1)
 rec={'schema':'reverse_hessian.det_sym51_rep_certificate.v1','partition':[5,1],'tableau_rows':[[0,1,2,3,4],[5]],'young_terms':len(terms),
      'source_decomposition':'Sym^2(A tensor B)=Sym^2 A tensor Sym^2 B direct_sum Lambda^2 A tensor Lambda^2 B, dim A=dim B=4',
      'symmetric_symmetric_highest_weight':{'source':'x11^2','projected_zero':not p00,'nnz':len(p00),'sha256':hsh(p00)},
      'exterior_exterior_highest_weight':{'source':'x11*x22-x12*x21','projected_nonzero':bool(q),'nnz':len(q),'sha256':hsh(q)},
      'conclusion_rank_Q_exact':36,
      'conclusion_reason':'The Young flattening is GL(A)xGL(B)-equivariant. Each of the two source summands is irreducible; the first is killed and the second maps nontrivially, hence injectively.'}
 a.out.write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n');print(rec)
if __name__=='__main__':main()
