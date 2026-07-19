#!/usr/bin/env python3
"""Exact small-case checks for the one-padding-variable Hessian factorization.

The paper proves, for homogeneous g of degree d in N variables and k>=1,
 det Hess(l^k g) = -k(k+d-1)/(d-1) * l^(k(N+1)-2) * g * det Hess(g).
The full Hessian in a larger ambient space with any unused variable is zero.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import sympy as sp


def check(g,xs,k,l):
    d=sp.Poly(g,*xs).total_degree(); N=len(xs)
    F=sp.expand(l**k*g)
    actual=sp.expand(sp.hessian(F,(l,)+tuple(xs)).det())
    predicted=sp.expand(-sp.Rational(k*(k+d-1),d-1)*l**(k*(N+1)-2)*g*sp.hessian(g,xs).det())
    return {'degree_g':int(d),'variables_g':N,'k':k,'residual_zero':bool(sp.expand(actual-predicted)==0),'actual_total_degree':int(sp.Poly(actual,l,*xs).total_degree())}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,default=Path('certificates/transverse_hessian_experiments.json')); a=ap.parse_args()
    l,u=sp.symbols('l u'); x,y,z=sp.symbols('x y z')
    examples=[('binary_cubic',x**3+2*x*y**2+y**3,(x,y),1),('binary_cubic_k2',x**3+2*x*y**2+y**3,(x,y),2),('ternary_cubic',x**3+y**3+z**3+3*x*y*z,(x,y,z),2)]
    checks=[]
    for name,g,xs,k in examples:
        r=check(g,xs,k,l); r['name']=name
        if not r['residual_zero']: raise AssertionError(name)
        checks.append(r)
    g=x**3+y**3+z**3+3*x*y*z
    F=l**2*g
    ambient=sp.hessian(F,(l,x,y,z,u)).det()
    if sp.expand(ambient)!=0: raise AssertionError('unused-variable Hessian should vanish')
    cert={'schema':'reverse_hessian.transverse_hessian_experiments.v1','deterministic':True,'identity_checked':'det Hess(l^k g)=-k(k+d-1)/(d-1) l^(k(N+1)-2) g det Hess(g)','checks':checks,'unused_variable_check':{'ambient_variables':5,'active_variables':4,'full_hessian_determinant_zero':True},'interpretation':'The standard padded permanent in m^2 variables has unused variables for m>n, hence its full m^2-variable Hessian determinant is identically zero.'}
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
    print('transverse Hessian experiments: passed')
    return 0
if __name__=='__main__': raise SystemExit(main())
