#!/usr/bin/env sage
# Independent SageMath cross-check. This file is not imported by the Python engines.
import json
from itertools import permutations
from pathlib import Path

PRIMES = [1009, 32003, 65521]
R = PolynomialRing(QQ, names=('x11','x12','x13','x21','x22','x23','x31','x32','x33'))
xs = R.gens()

def sgn(p):
    return -1 if sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1,len(p))) % 2 else 1

def make_form(signed):
    ans = R.zero()
    for p in permutations(range(3)):
        mon = R.one()
        for i in range(3):
            mon *= xs[3*i+p[i]]
        ans += (sgn(p) if signed else 1) * mon
    return ans

def weak_compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for a in range(total+1):
            for tail in weak_compositions(total-a, length-1):
                yield (a,) + tail

def derivative_factor(gamma, beta):
    out = 1
    for g,b in zip(gamma,beta):
        out *= factorial(g)//factorial(b)
    return out

def catalecticant(F, a, field):
    P = PolynomialRing(field, names=R.variable_names())
    G = P(F)
    rows = list(weak_compositions(a,9))
    cols = list(weak_compositions(9-a,9))
    ci = {e:j for j,e in enumerate(cols)}
    entries = {}
    for i,alpha in enumerate(rows):
        for gamma, coeff in G.dict().items():
            if all(g>=b for g,b in zip(gamma,alpha)):
                beta=tuple(g-b for g,b in zip(gamma,alpha))
                entries[(i,ci[beta])] = entries.get((i,ci[beta]),field.zero()) + coeff*field(derivative_factor(gamma,beta))
    return matrix(field,len(rows),len(cols),entries,sparse=True)

det3 = make_form(True)
per3 = make_form(False)
Ddet = det(matrix(R, [[det3.derivative(xi).derivative(xj) for xj in xs] for xi in xs]))
Dper = det(matrix(R, [[per3.derivative(xi).derivative(xj) for xj in xs] for xi in xs]))
assert Ddet == -2*det3^3

out = {'schema':'reverse_hessian.sage_independent.v1','primes':PRIMES,'checks':[]}
for a in range(10):
    row={'a':a,'ranks':{}}
    for p in PRIMES:
        K=GF(p)
        row['ranks'][str(p)]={
            'Ddet': int(catalecticant(Ddet,a,K).rank()),
            'Dper': int(catalecticant(Dper,a,K).rank()),
        }
    out['checks'].append(row)
Path('certificates/independent_catalecticant_check_sage.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
