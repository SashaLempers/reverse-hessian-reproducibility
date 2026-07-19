#!/usr/bin/env python3
"""Primary exact-Q engine for the n=3 reverse-Hessian catalecticants.

This script constructs det_3 and per_3, their Hessian determinants, and the
ordinary apolar catalecticant matrices.  Ranks are computed exactly over Q.
The JSON output contains no timing, host, or absolute path information.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from itertools import permutations
from math import prod
from pathlib import Path
from typing import Dict, Iterator, List, Sequence, Tuple

import sympy as sp
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix

NVAR = 9
DEGREE = 9
Exponent = Tuple[int, ...]


def permutation_sign(p: Sequence[int]) -> int:
    inv = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inv % 2 else 1


def monomials_of_degree(n: int, d: int) -> Iterator[Exponent]:
    if n == 1:
        yield (d,)
        return
    for a in range(d + 1):
        for rest in monomials_of_degree(n - 1, d - a):
            yield (a,) + rest


def coeff_dict(poly: sp.Expr, variables: Sequence[sp.Symbol]) -> Dict[Exponent, int]:
    return {m: int(c) for m, c in sp.Poly(poly, *variables, domain=sp.ZZ).terms()}


def canonical_poly_hash(poly: sp.Expr, variables: Sequence[sp.Symbol]) -> str:
    payload = [
        [list(m), [int(c.p), int(c.q)]]
        for m, c in sp.Poly(poly, *variables, domain=sp.QQ).terms()
    ]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def derivative_factor(gamma: Exponent, beta: Exponent) -> int:
    out = 1
    for gi, bi in zip(gamma, beta):
        for t in range(bi + 1, gi + 1):
            out *= t
    return out


def matrix_payload_hash(shape: Tuple[int, int], entries: Dict[int, Dict[int, int]]) -> str:
    triples = []
    for i in sorted(entries):
        for j in sorted(entries[i]):
            triples.append([i, j, int(entries[i][j])])
    payload = {"shape": list(shape), "entries": triples}
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def catalecticant_matrix(coeffs: Dict[Exponent, int], a: int):
    rows = list(monomials_of_degree(NVAR, a))
    cols = list(monomials_of_degree(NVAR, DEGREE - a))
    col_index = {b: j for j, b in enumerate(cols)}
    dod_int: Dict[int, Dict[int, int]] = {}
    for i, alpha in enumerate(rows):
        row: Dict[int, int] = {}
        for gamma, coeff in coeffs.items():
            if all(g >= x for g, x in zip(gamma, alpha)):
                beta = tuple(g - x for g, x in zip(gamma, alpha))
                j = col_index[beta]
                value = coeff * derivative_factor(gamma, beta)
                row[j] = row.get(j, 0) + value
        row = {j: v for j, v in row.items() if v}
        if row:
            dod_int[i] = row
    shape = (len(rows), len(cols))
    dod_zz = {i: {j: ZZ(v) for j, v in row.items()} for i, row in dod_int.items()}
    matrix = DomainMatrix(dod_zz, shape, ZZ)
    return matrix, shape, sum(len(r) for r in dod_int.values()), matrix_payload_hash(shape, dod_int)


def make_forms():
    xs = sp.symbols("x11 x12 x13 x21 x22 x23 x31 x32 x33")
    x = {(i, j): xs[3 * i + j] for i in range(3) for j in range(3)}
    det3 = sum(permutation_sign(s) * prod(x[i, s[i]] for i in range(3)) for s in permutations(range(3)))
    perm3 = sum(prod(x[i, s[i]] for i in range(3)) for s in permutations(range(3)))
    Ddet = sp.expand(sp.hessian(det3, xs).det())
    Dperm = sp.expand(sp.hessian(perm3, xs).det())
    return xs, det3, perm3, Ddet, Dperm


def direct_row(coeffs_det, coeffs_perm, a: int) -> dict:
    md, shape_d, nnz_d, hash_d = catalecticant_matrix(coeffs_det, a)
    mp, shape_p, nnz_p, hash_p = catalecticant_matrix(coeffs_perm, a)
    if shape_d != shape_p:
        raise AssertionError("shape mismatch")
    rd, rp = int(md.rank()), int(mp.rank())
    if rd > rp:
        raise AssertionError(f"unexpected obstruction at a={a}: {rd}>{rp}")
    return {
        "a": a,
        "shape": list(shape_d),
        "nnz_Ddet": nnz_d,
        "nnz_Dperm": nnz_p,
        "matrix_sha256_Ddet": hash_d,
        "matrix_sha256_Dperm": hash_p,
        "rank_Ddet": rd,
        "rank_Dperm": rp,
        "rank_source": "exact_Q_DomainMatrix",
    }


def mirrored_row(source: dict, a: int) -> dict:
    out = dict(source)
    out["a"] = a
    out["shape"] = [source["shape"][1], source["shape"][0]]
    # The canonical matrix hashes differ under transpose/factorial rescaling, so
    # they are intentionally omitted for rows derived by duality.
    out.pop("matrix_sha256_Ddet", None)
    out.pop("matrix_sha256_Dperm", None)
    out["rank_source"] = f"proved_duality_with_C_{DEGREE-a}"
    return out


def build_certificate(full: bool) -> dict:
    xs, det3, perm3, Ddet, Dperm = make_forms()
    if sp.expand(Ddet + 2 * det3**3) != 0:
        raise AssertionError("Ddet identity failed")
    cd, cp = coeff_dict(Ddet, xs), coeff_dict(Dperm, xs)
    if full:
        rows = [direct_row(cd, cp, a) for a in range(10)]
    else:
        base = {a: direct_row(cd, cp, a) for a in range(5)}
        rows = [base[a] if a in base else mirrored_row(base[9-a], a) for a in range(10)]
    return {
        "schema": "reverse_hessian.catalecticant_exact.v3",
        "deterministic": True,
        "base_field": "Q",
        "variables": [str(v) for v in xs],
        "degree": 9,
        "hessian_convention": "ordinary 9x9 Hessian in row-major variable order",
        "Ddet_identity": "det Hess(det_3) = -2 det_3^3",
        "polynomial_hashes": {
            "det3": canonical_poly_hash(det3, xs),
            "per3": canonical_poly_hash(perm3, xs),
            "Ddet3": canonical_poly_hash(Ddet, xs),
            "Dper3": canonical_poly_hash(Dperm, xs),
        },
        "polynomial_monomial_counts": {
            "det3": len(coeff_dict(det3, xs)),
            "per3": len(coeff_dict(perm3, xs)),
            "Ddet3": len(cd),
            "Dper3": len(cp),
        },
        "rank_engine": "SymPy DomainMatrix exact rank over ZZ/Q",
        "duality_statement": "rank C_a(F)=rank C_{9-a}(F); matrices differ by transpose and invertible factorial diagonal scalings",
        "catalecticants": rows,
        "rank_vectors": {
            "Ddet": [r["rank_Ddet"] for r in rows],
            "Dper": [r["rank_Dperm"] for r in rows],
        },
        "certified_statement": "rank C_a(Ddet)<=rank C_a(Dper) for a=0,...,9",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=Path("certificates/catalecticant_ranks.json"))
    p.add_argument("--full", action="store_true")
    args = p.parse_args()
    cert = build_certificate(args.full)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("Ddet", cert["rank_vectors"]["Ddet"])
    print("Dper", cert["rank_vectors"]["Dper"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
