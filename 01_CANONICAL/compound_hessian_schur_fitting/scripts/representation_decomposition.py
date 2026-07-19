#!/usr/bin/env python3
"""Exact symmetric-function decompositions needed for compound Hessian search.

Uses power-sum plethysm and Murnaghan--Nakayama, with Fraction arithmetic.
No external CAS is required.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from math import factorial
from pathlib import Path
import argparse, json

Partition=tuple[int,...]

def partitions(n:int,maxpart:int|None=None)->list[Partition]:
    if n==0:return [()]
    if maxpart is None or maxpart>n:maxpart=n
    out=[]
    def rec(rem,cap,prefix):
        if rem==0:out.append(tuple(prefix));return
        for x in range(min(cap,rem),0,-1):rec(rem-x,x,prefix+[x])
    rec(n,maxpart,[]);return out

def zpart(mu:Partition)->int:
    c=Counter(mu);z=1
    for i,m in c.items():z*=i**m*factorial(m)
    return z

def cells(lam:Partition):return {(i,j) for i,r in enumerate(lam) for j in range(r)}

def contained_partitions(lam:Partition,target_size:int):
    out=[]
    def rec(i,prev,rem,vals):
        if i==len(lam):
            if rem==0:
                while vals and vals[-1]==0:vals.pop()
                out.append(tuple(vals))
            return
        for x in range(min(lam[i],prev,rem),-1,-1):
            rec(i+1,x,rem-x,vals+[x])
    rec(0,10**9,target_size,[])
    return out

def is_border_strip(lam:Partition,mu:Partition,k:int):
    L=cells(lam);M=cells(mu);S=L-M
    if len(S)!=k or not S:return None
    # connected by edges
    seen={next(iter(S))};stack=list(seen)
    while stack:
        i,j=stack.pop()
        for q in ((i+1,j),(i-1,j),(i,j+1),(i,j-1)):
            if q in S and q not in seen:seen.add(q);stack.append(q)
    if seen!=S:return None
    # no 2x2 block
    for i,j in S:
        if {(i,j),(i+1,j),(i,j+1),(i+1,j+1)}<=S:return None
    rows={i for i,j in S}
    return len(rows)-1

@lru_cache(None)
def rim_removals(lam:Partition,k:int):
    target=sum(lam)-k
    if target<0:return ()
    out=[]
    for mu in contained_partitions(lam,target):
        h=is_border_strip(lam,mu,k)
        if h is not None:out.append((mu,h))
    return tuple(out)

@lru_cache(None)
def character(lam:Partition,rho:Partition)->int:
    if not rho:return 1 if not lam else 0
    if sum(lam)!=sum(rho):return 0
    k=rho[0];rest=rho[1:]
    return sum(((-1)**h)*character(mu,rest) for mu,h in rim_removals(lam,k))

def hook_dimension(lam:Partition)->int:
    n=sum(lam);den=1
    for i,row in enumerate(lam):
        for j in range(row):
            below=sum(i2>i and lam[i2]>j for i2 in range(len(lam)))
            right=row-j-1
            den*=1+right+below
    return factorial(n)//den

def mul_ps(a:dict[Partition,Fraction],b:dict[Partition,Fraction]):
    out=defaultdict(Fraction)
    for x,c in a.items():
        for y,d in b.items():out[tuple(sorted(x+y,reverse=True))]+=c*d
    return dict(out)

def h_power_sum(n:int,scale:int=1):
    return {tuple(sorted((scale*x for x in mu),reverse=True)):Fraction(1,zpart(mu)) for mu in partitions(n)}

def plethysm_h_h(r:int,d:int):
    # h_r[h_d]
    out=defaultdict(Fraction)
    for mu in partitions(r):
        prod={():Fraction(1)}
        for k in mu:prod=mul_ps(prod,h_power_sum(d,k))
        for rho,c in prod.items():out[rho]+=c/Fraction(zpart(mu))
    return dict(out)

def schur_decompose_power_sum(ps:dict[Partition,Fraction]):
    n=sum(next(iter(ps))) if ps else 0
    out={}
    for lam in partitions(n):
        m=sum(c*character(lam,rho) for rho,c in ps.items())
        if m:
            if m.denominator!=1:raise ArithmeticError((lam,m))
            out[lam]=m.numerator
    return out

def horizontal_strip(lam:Partition,base:Partition,added:int)->bool:
    if sum(lam)-sum(base)!=added:return False
    L=cells(lam);B=cells(base)
    if not B<=L:return False
    S=L-B
    cols=[j for i,j in S]
    return len(cols)==len(set(cols))

def pieri(base:Partition,k:int):
    n=sum(base)+k
    return [lam for lam in partitions(n) if horizontal_strip(lam,base,k)]

def validate_chars(up_to=8):
    for n in range(up_to+1):
        idcy=(1,)*n
        for lam in partitions(n):
            assert character(lam,idcy)==hook_dimension(lam),(lam,character(lam,idcy),hook_dimension(lam))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    validate_chars(12)
    records={}
    for r in (2,3,4):
        dec=schur_decompose_power_sum(plethysm_h_h(r,4))
        base=(2,)*r
        target=pieri(base,2*r)
        inter={lam:dec[lam] for lam in target if lam in dec}
        records[str(r)]={
          'domain':f'Sym^{r}(Sym^4 V)',
          'domain_schur_decomposition':[[list(lam),m] for lam,m in dec.items()],
          'compound_target':f'S_{{(2^{r})}} V tensor Sym^{2*r} V',
          'target_pieri_partitions':[list(x) for x in target],
          'intersection':[[list(lam),m] for lam,m in inter.items()],
        }
    result={'schema':'reverse_hessian.compound_representation_decomposition.v1','method':'exact power-sum plethysm + Murnaghan-Nakayama + Pieri','records':records}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    for r,x in records.items():print('r',r,'intersection',x['intersection'])
if __name__=='__main__':main()
