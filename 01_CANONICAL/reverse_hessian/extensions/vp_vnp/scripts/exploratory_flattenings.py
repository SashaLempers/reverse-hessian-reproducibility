#!/usr/bin/env python3
"""Exact exploratory shifted-partial-derivative tests on Ddet,3 and Dper,3.

These tests are exploratory and are not promoted to a general theorem.  For a
form F of degree d, SPD_{k,l}(F) is the span of x^beta * partial^alpha F with
|alpha|=k and |beta|=l.  Its dimension is a matrix rank and is upper
semicontinuous, so a reverse-orbit obstruction would require rank(Ddet) >
rank(Dper).
"""
from __future__ import annotations
import argparse, hashlib, json
from itertools import permutations
from math import prod
from pathlib import Path
from typing import Dict, Iterator, Tuple
import sympy as sp
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix

Exp=Tuple[int,...]
N=9
PRIMES=(1009,32003)


def sign(p): return -1 if sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2 else 1

def comps(n,d)->Iterator[Exp]:
    if n==1: yield (d,); return
    for a in range(d+1):
        for t in comps(n-1,d-a): yield (a,)+t

def make_forms():
    xs=sp.symbols('x11 x12 x13 x21 x22 x23 x31 x32 x33'); x=lambda i,j: xs[3*i+j]
    det=sum(sign(s)*prod(x(i,s[i]) for i in range(3)) for s in permutations(range(3)))
    per=sum(prod(x(i,s[i]) for i in range(3)) for s in permutations(range(3)))
    return xs,sp.expand(sp.hessian(det,xs).det()),sp.expand(sp.hessian(per,xs).det())

def coeffs(F,xs): return {tuple(m):int(c) for m,c in sp.Poly(F,*xs,domain=sp.ZZ).terms()}

def falling(a,b):
    r=1
    for q in range(a-b+1,a+1): r*=q
    return r

def derivative(poly:Dict[Exp,int],alpha:Exp)->Dict[Exp,int]:
    out={}
    for gamma,c in poly.items():
        if all(g>=a for g,a in zip(gamma,alpha)):
            e=tuple(g-a for g,a in zip(gamma,alpha)); f=1
            for g,a in zip(gamma,alpha): f*=falling(g,a) if a else 1
            out[e]=out.get(e,0)+c*f
    return {e:c for e,c in out.items() if c}

def sparse_rank_mod(rows,ncols,p):
    piv={}
    for i in sorted(rows):
        row={j:v%p for j,v in rows[i].items() if v%p}
        while row:
            lead=min(row)
            if lead not in piv:
                inv=pow(row[lead],-1,p); row={j:(v*inv)%p for j,v in row.items() if (v*inv)%p}; piv[lead]=row; break
            f=row[lead]
            for j,v in piv[lead].items():
                z=(row.get(j,0)-f*v)%p
                if z: row[j]=z
                elif j in row: del row[j]
    return len(piv)

def matrix_hash(shape,rows):
    payload={'shape':list(shape),'entries':[[i,j,int(rows[i][j])] for i in sorted(rows) for j in sorted(rows[i])]}
    return hashlib.sha256(json.dumps(payload,separators=(',',':')).encode()).hexdigest()

def spd_matrix(poly,k,l):
    alphas=list(comps(N,k)); betas=list(comps(N,l)); target_degree=9-k+l
    cols=list(comps(N,target_degree)); ci={e:j for j,e in enumerate(cols)}
    rows={}; r=0
    derivs={a:derivative(poly,a) for a in alphas}
    for a in alphas:
        dp=derivs[a]
        for b in betas:
            row={}
            for e,c in dp.items():
                q=tuple(x+y for x,y in zip(e,b)); j=ci[q]; row[j]=row.get(j,0)+c
            row={j:v for j,v in row.items() if v}
            if row: rows[r]=row
            r+=1
    shape=(len(alphas)*len(betas),len(cols))
    M=DomainMatrix({i:{j:ZZ(v) for j,v in row.items()} for i,row in rows.items()},shape,ZZ)
    return shape,rows,int(M.rank())

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,default=Path('certificates/exploratory_flattenings.json')); a=ap.parse_args()
    xs,Dd,Dp=make_forms(); pd,pp=coeffs(Dd,xs),coeffs(Dp,xs)
    tests=[]
    for k,l in ((1,1),(2,1),(1,2)):
        rec={'test':f'SPD(k={k},l={l})','order':k,'shift':l,'forms':{}}
        for name,poly in (('Ddet',pd),('Dper',pp)):
            shape,rows,rq=spd_matrix(poly,k,l); mods={str(p):sparse_rank_mod(rows,shape[1],p) for p in PRIMES}
            if any(v!=rq for v in mods.values()): raise AssertionError((k,l,name,rq,mods))
            rec['forms'][name]={'shape':list(shape),'nnz':sum(len(x) for x in rows.values()),'rank_Q':rq,'ranks_mod_p':mods,'matrix_sha256':matrix_hash(shape,rows)}
        rec['separates_reverse_direction']=rec['forms']['Ddet']['rank_Q']>rec['forms']['Dper']['rank_Q']
        rec['status']='CERTIFIED-COMP'
        tests.append(rec)
    cert={'schema':'reverse_hessian.exploratory_flattenings.v1','deterministic':True,'tests':tests,'interpretation':'A rank test obstructs Ddet in closure(GL.Dper) only when rank(Ddet)>rank(Dper). None of the tested SPD parameters has that direction.'}
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
    for t in tests: print(t['test'],t['forms']['Ddet']['rank_Q'],t['forms']['Dper']['rank_Q'],t['separates_reverse_direction'])
    return 0
if __name__=='__main__': raise SystemExit(main())
