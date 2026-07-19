#!/usr/bin/env python3
from __future__ import annotations
import argparse,struct,sys,time,json
from pathlib import Path
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
import schur_block_r2_k2 as sb

def unpack(k):return tuple((k>>(4*i))&15 for i in range(6))
def _read_exact(f, n, label):
 data=f.read(n)
 if len(data)!=n: raise ValueError(f"truncated {label}: expected {n}, got {len(data)}")
 return data

def read(path):
 rows=[]
 with open(path,'rb') as f:
  magic=_read_exact(f,8,'magic')
  if magic!=b'RHT6v1\0\0': raise ValueError(f'bad magic: {magic!r}')
  n,nr=struct.unpack('<II',_read_exact(f,8,'header'))
  if n!=16 or nr not in (120,136): raise ValueError(f'bad header n={n} nrows={nr}')
  for row_index in range(nr):
   a,b,pad,nnz=struct.unpack('<BBHI',_read_exact(f,8,f'row {row_index} header'))
   if a>=16 or b>=16 or pad!=0: raise ValueError(f'bad row header at {row_index}')
   if nnz>50_000_000: raise ValueError(f'impossible nnz at {row_index}: {nnz}')
   r={}
   for entry_index in range(nnz):
    k,v=struct.unpack('<Ii',_read_exact(f,8,f'row {row_index} entry {entry_index}'))
    vals=unpack(k)
    if any(z>=16 for z in vals): raise ValueError('encoded value outside range')
    if vals in r: raise ValueError(f'duplicate key in row {row_index}')
    r[vals]=v
   rows.append(r)
  if f.read(1)!=b'': raise ValueError('trailing bytes after exact payload')
 return rows

def project(row,terms):
 out={}
 for perm,c in terms:
  for key,v in row.items():
   nk=tuple(key[perm[i]] for i in range(6));z=out.get(nk,0)+c*v
   if z:out[nk]=z
   elif nk in out:del out[nk]
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--partition',required=True);ap.add_argument('--index',type=int,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 lam=tuple(map(int,a.partition.split(',')))
 # generate all standard tableaux by brute-force labels and use sb.tableau_groups generalized by rows
 # reproduce C++ standard order
 import itertools
 tabs=[]
 shape=lam
 for cells in itertools.permutations(range(6)):
  rows=[];q=0
  for L in shape:rows.append(list(cells[q:q+L]));q+=L
  if any(any(r[j-1]>r[j] for j in range(1,len(r))) for r in rows):continue
  ok=True
  for j in range(max(shape)):
   col=[rows[i][j] for i in range(len(rows)) if j<len(rows[i])]
   if any(col[t-1]>col[t] for t in range(1,len(col))):ok=False
  if ok:tabs.append(rows)
 rowsT=tabs[a.index]
 # build terms from arbitrary rows
 cols=[]
 for j in range(max(shape)):cols.append([rowsT[i][j] for i in range(len(rowsT)) if j<len(rowsT[i])])
 rg=sb.subgroup_permutations(rowsT);cg=sb.subgroup_permutations(cols);termsD={}
 for rp,_ in rg:
  for cp,cs in cg:
   z=sb.compose_perm(rp,cp);termsD[z]=termsD.get(z,0)+cs
 terms=[(p,c) for p,c in termsD.items() if c]
 base=read(a.input);t=time.time();proj=[]
 for i,r in enumerate(base):
  z=project(r,terms);proj.append(z)
  if (i+1)%10==0:print('projected',i+1,'nnz',len(z),flush=True)
 keys=sorted({k for r in proj for k in r});ci={k:i for i,k in enumerate(keys)}
 data={}
 for i,r in enumerate(proj):
  if r:data[i]={ci[k]:ZZ(v) for k,v in r.items()}
 M=DomainMatrix(data,(len(proj),len(keys)),ZZ)
 print('shape',M.shape,'nnz',sum(len(r) for r in proj),'project_seconds',time.time()-t,flush=True)
 rank=int(M.rank());print('rank',rank,flush=True)
 rec={'schema':'reverse_hessian.exact_projected_rank.v1','input':a.input.name,'partition':list(lam),'tableau_index':a.index,'tableau_rows':rowsT,'young_terms':len(terms),'matrix_shape':list(M.shape),'matrix_nnz':sum(len(r) for r in proj),'rank_Q_exact':rank}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
