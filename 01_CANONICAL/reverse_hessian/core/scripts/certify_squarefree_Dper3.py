#!/usr/bin/env python3
"""Exact deterministic certificate for squarefreeness of det Hess(per_3)."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from itertools import permutations
from pathlib import Path

import sympy as sp

VARIABLE_NAMES = "x11 x12 x13 x21 x22 x23 x31 x32 x33"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(poly: sp.Expr, variables) -> str:
    p = sp.Poly(poly, *variables, domain=sp.QQ)
    payload = [[list(exp), [int(coeff.p), int(coeff.q)]] for exp, coeff in p.terms()]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    variables = sp.symbols(VARIABLE_NAMES)
    x = [variables[0:3], variables[3:6], variables[6:9]]
    per3 = sum(sp.prod(x[i][sigma[i]] for i in range(3)) for sigma in permutations(range(3)))
    d_per = sp.expand(sp.hessian(per3, variables).det(method="domain-ge"))
    polynomial = sp.Poly(d_per, *variables, domain=sp.QQ)
    assert polynomial.total_degree() == 9
    assert len(polynomial.terms()) == 55

    factor_unit, factors = sp.factor_list(d_per, *variables)
    factor_records = []
    for factor, multiplicity in factors:
        fp = sp.Poly(factor, *variables, domain=sp.QQ)
        factor_records.append(
            {
                "total_degree": int(fp.total_degree()),
                "multiplicity": int(multiplicity),
                "monomial_count": len(fp.terms()),
                "factor_sha256": canonical_hash(factor, variables),
            }
        )
    assert len(factor_records) == 1
    assert factor_records[0]["total_degree"] == 9
    assert factor_records[0]["multiplicity"] == 1

    partials = [sp.Poly(sp.diff(d_per, variable), *variables, domain=sp.QQ) for variable in variables]
    gcd_poly = partials[0]
    for partial in partials[1:]:
        gcd_poly = sp.gcd(gcd_poly, partial)
    gcd_poly = gcd_poly.monic()
    assert gcd_poly.total_degree() == 0 and gcd_poly.as_expr() == 1

    integer_contents = [abs(int(sp.Poly(p.as_expr(), *variables, domain=sp.ZZ).content())) for p in partials]
    content_gcd = 0
    for value in integer_contents:
        content_gcd = math.gcd(content_gcd, value)

    t = sp.symbols("t")
    substitution = {variables[i]: 1 for i in range(9)}
    substitution[variables[0]] = t
    line_value = sp.factor(d_per.subs(substitution))
    assert sp.expand(line_value - 64 * t) == 0

    primes = [101, 1009, 32003, 65521]
    points = [tuple(range(1, 10)), tuple(k * k + 3 * k + 1 for k in range(1, 10))]
    fingerprints = []
    partial_exprs = [p.as_expr() for p in partials]
    for prime in primes:
        evaluations = []
        for point in points:
            sub = dict(zip(variables, [value % prime for value in point]))
            evaluations.append(
                {
                    "Dper_mod_p": int(d_per.subs(sub)) % prime,
                    "partials_mod_p": [int(expr.subs(sub)) % prime for expr in partial_exprs],
                }
            )
        fingerprints.append({"prime": prime, "evaluations": evaluations})

    mathematical_core = {
        "Dper_sha256": canonical_hash(d_per, variables),
        "gcd_partials": "1",
        "factorization": factor_records,
        "line_restriction": "64*t",
        "primes": fingerprints,
    }
    certificate = {
        "schema": "reverse-hessian.squarefree-Dper3.v3",
        "status": "CERTIFIED-COMP (exact reproducible computation; not a proof-assistant certificate)",
        "form": "Dper3 = det Hess(per_3)",
        "characteristic": 0,
        "number_of_variables": 9,
        "total_degree": 9,
        "monomial_count": 55,
        "method": "exact factorization over Q plus exact gcd of all nine first partial derivatives",
        "factor_unit": str(factor_unit),
        "factorization_over_Q": factor_records,
        "irreducibility_statement": "SymPy factor_list over Q returns one degree-9 factor of multiplicity one; no absolute irreducibility claim is made.",
        "gcd_all_partials_over_Q": "1",
        "integer_content_gcd_of_partials": content_gcd,
        "line_restriction_at_J3_plus_t_minus_1_E11": "64*t",
        "primes_used_for_sanity_checks": primes,
        "modular_evaluation_fingerprints": fingerprints,
        "Dper3_polynomial_sha256": mathematical_core["Dper_sha256"],
        "mathematical_output_sha256": hashlib.sha256(
            json.dumps(mathematical_core, separators=(",", ":"), sort_keys=True).encode()
        ).hexdigest(),
        "script_sha256": file_hash(Path(__file__).resolve()),
        "certified_statement": "Dper3 is squarefree over Q and therefore geometrically squarefree over C in characteristic zero.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"success": True, "monomials": 55, "gcd_partials": 1}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
