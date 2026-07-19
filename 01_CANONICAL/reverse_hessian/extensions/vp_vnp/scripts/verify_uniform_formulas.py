#!/usr/bin/env python3
"""Deterministic finite checks supporting the paper proofs of the uniform formulas."""
from __future__ import annotations
import argparse, hashlib, json
from itertools import permutations
from math import factorial, prod
from pathlib import Path
import sympy as sp


def sign(p):
    return -1 if sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1,len(p))) % 2 else 1


def predicted_c(n):
    return (n-1) * ((-1) ** (((n-1)*(n+2))//2))


def det_hessian_at_identity(n):
    # Bilinear form B(U,V)=tr(U)tr(V)-tr(UV) in row-major matrix-unit basis.
    M=sp.zeros(n*n)
    for i in range(n):
        for j in range(n):
            a=n*i+j
            for k in range(n):
                for l in range(n):
                    b=n*k+l
                    M[a,b]=(1 if i==j and k==l else 0) - (1 if j==k and i==l else 0)
    return int(M.det())


def structured_per_hessian(n,t):
    A=sp.ones(n)-sp.eye(n)
    C=sp.zeros(n)
    for i in range(1,n):
        for j in range(1,n):
            if i!=j: C[i,j]=1
    return factorial(n-2)*sp.kronecker_product(A,A)+(t-1)*factorial(n-3)*sp.kronecker_product(C,C)


def kappa(n):
    return sp.Integer(factorial(n-2))**(n*n)*sp.Integer(n-1)**(2*n)/sp.Integer(n-2)**((n-2)**2)


def direct_per_hessian_line(n,t):
    xs=sp.symbols('x0:'+str(n*n))
    x=lambda i,j: xs[n*i+j]
    per=sum(prod(x(i,s[i]) for i in range(n)) for s in permutations(range(n)))
    H=sp.hessian(per,xs)
    subs={x(i,j):(t if (i,j)==(0,0) else 1) for i in range(n) for j in range(n)}
    return sp.Matrix(H.subs(subs))


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,default=Path('certificates/uniform_formulas.json')); a=ap.parse_args()
    t=sp.symbols('t')
    det_checks=[]
    for n in range(2,9):
        actual=det_hessian_at_identity(n); pred=predicted_c(n)
        if actual!=pred: raise AssertionError((n,actual,pred))
        det_checks.append({'n':n,'actual_det_at_identity':actual,'predicted_constant':pred,'verified':True})
    line=[]
    for n in range(3,6):
        values=[]
        for tv in (0,2):
            actual=int(structured_per_hessian(n,sp.Integer(tv)).det())
            pred=int(kappa(n)*sp.Integer(tv+n-3)**((n-2)**2))
            if actual!=pred: raise AssertionError((n,tv,actual,pred))
            values.append({'t':tv,'actual':str(actual),'predicted':str(pred),'verified':True})
        line.append({'n':n,'numeric_exact_checks':values,'verified':True})
    direct=[]
    for n in (3,4):
        H=direct_per_hessian_line(n,t); S=structured_per_hessian(n,t)
        eq=H==S
        if not eq: raise AssertionError('direct structured mismatch')
        direct.append({'n':n,'direct_matrix_equals_structured_matrix':True,'direct_determinant':str(sp.factor(H.det()))})
    formula='det Hess(det_n)=(n-1)(-1)^((n-1)(n+2)/2)det_n^(n(n-2)); det Hess(per_n)(J_n+(t-1)E_11)=kappa_n(t+n-3)^((n-2)^2)'
    cert={'schema':'reverse_hessian.uniform_formula_checks.v2','deterministic':True,'finite_checks_are_not_general_proofs':True,'general_proof_location':'paper/reverse_hessian_VP_VNP_upgrade.tex','formula_sha256':hashlib.sha256(formula.encode()).hexdigest(),'determinant_hessian_constant_checks':det_checks,'permanent_hessian_line_checks':line,'direct_minor_formula_checks':direct}
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
    print('uniform formulas: finite checks passed')
    return 0
if __name__=='__main__': raise SystemExit(main())
