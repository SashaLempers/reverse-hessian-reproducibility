#!/usr/bin/env python3
"""Deterministic exact certificate that D_per,3 is squarefree over Q."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from itertools import permutations
from pathlib import Path

import sympy as sp

PRIMES = (1009, 32003, 65521)


def sign(p):
    inv = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inv % 2 else 1


def canonical_poly_hash(poly: sp.Expr, xs) -> str:
    payload = [[list(m), [int(c.p), int(c.q)]] for m, c in sp.Poly(poly, *xs, domain=sp.QQ).terms()]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def make_forms():
    xs = sp.symbols("x11 x12 x13 x21 x22 x23 x31 x32 x33")
    x = {(i, j): xs[3 * i + j] for i in range(3) for j in range(3)}
    det3 = sum(sign(s) * sp.prod(x[i, s[i]] for i in range(3)) for s in permutations(range(3)))
    per3 = sum(sp.prod(x[i, s[i]] for i in range(3)) for s in permutations(range(3)))
    Ddet = sp.expand(sp.hessian(det3, xs).det())
    Dper = sp.expand(sp.hessian(per3, xs).det())
    return xs, det3, per3, Ddet, Dper


def gcd_partials(poly, xs, domain=None, modulus=None):
    kwargs = {"modulus": modulus} if modulus is not None else {"domain": domain}
    ps = [sp.Poly(sp.diff(poly, x), *xs, **kwargs) for x in xs]
    g = ps[0]
    for q in ps[1:]:
        g = sp.gcd(g, q)
    return g


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("certificates/squarefree_Dper3.json"))
    args = ap.parse_args()

    xs, det3, per3, Ddet, Dper = make_forms()
    if sp.expand(Ddet + 2 * det3**3) != 0:
        raise AssertionError("determinant Hessian identity failed")

    gq = gcd_partials(Dper, xs, domain=sp.QQ)
    if gq.total_degree() != 0:
        raise AssertionError(f"nonconstant gcd over Q: {gq.as_expr()}")

    partials = [sp.diff(Dper, x) for x in xs]
    contents = [abs(int(sp.Poly(q, *xs, domain=sp.ZZ).content())) for q in partials]
    content_gcd = 0
    for c in contents:
        content_gcd = math.gcd(content_gcd, c)

    # Lightweight modular sanity checks.  The characteristic-zero gcd above is
    # the proof of squarefreeness; these checks only confirm that the same
    # polynomial data reduce nontrivially at the listed primes.
    modular = {}
    Dper_ZZ = sp.Poly(Dper, *xs, domain=sp.ZZ)
    for p in PRIMES:
        Pp = sp.Poly(Dper, *xs, modulus=p)
        nonzero_partials = sum(not sp.Poly(q, *xs, modulus=p).is_zero for q in partials)
        modular[str(p)] = {
            "Dper3_total_degree_mod_p": int(Pp.total_degree()),
            "Dper3_monomials_mod_p": len(Pp.terms()),
            "nonzero_first_partials": int(nonzero_partials),
            "role": "sanity check only; the squarefreeness proof is the exact QQ gcd",
        }

    core = {
        "degree": int(sp.Poly(Dper, *xs).total_degree()),
        "number_of_variables": len(xs),
        "method": "construct Dper3 exactly over ZZ and compute the gcd of all first partial derivatives over QQ; modular reductions are supplementary sanity checks",
        "characteristic_for_proof": 0,
        "gcd_of_partial_derivatives_over_Q": str(gq.monic().as_expr()),
        "gcd_total_degree_over_Q": int(gq.total_degree()),
        "integer_content_gcd_of_partials": content_gcd,
        "primes_used": list(PRIMES),
        "modular_checks": modular,
        "Dper3_monomials": len(sp.Poly(Dper, *xs, domain=sp.ZZ).terms()),
        "Dper3_sha256": canonical_poly_hash(Dper, xs),
        "conclusion": "Dper3 is squarefree over Q (hence over C) because gcd(Dper3, all first partial derivatives)=1; equivalently the gcd of its first partials is constant for this homogeneous polynomial.",
    }
    math_hash = hashlib.sha256(json.dumps(core, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    cert = {
        "schema": "reverse_hessian.squarefree_Dper3.v2",
        "deterministic": True,
        **core,
        "script_sha256": sha256_file(Path(__file__)),
        "mathematical_output_sha256": math_hash,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("squarefree_Dper3: verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
