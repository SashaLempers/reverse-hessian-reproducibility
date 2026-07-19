#!/usr/bin/env python3
"""Independent clean-room modular engine for the n=3 catalecticants.

Independence properties:
- imports no code from the primary exact-rank script;
- constructs det_3/per_3 as exponent dictionaries;
- differentiates exponent dictionaries directly;
- reconstructs Hessian matrices and determinants;
- constructs catalecticants directly from exponent dictionaries;
- computes modular ranks by a custom sparse Gaussian elimination.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from itertools import permutations
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Sequence, Tuple

import sympy as sp

Exp = Tuple[int, ...]
Poly = Dict[Exp, int]
N = 9
D = 9
PRIMES = (1009, 32003, 65521)


def sign(p: Sequence[int]) -> int:
    inv = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inv & 1 else 1


def zero_exp() -> Exp:
    return (0,) * N


def permanent_dict(with_sign: bool) -> Poly:
    out: Poly = {}
    for sigma in permutations(range(3)):
        e = [0] * N
        for i in range(3):
            e[3 * i + sigma[i]] += 1
        t = tuple(e)
        out[t] = out.get(t, 0) + (sign(sigma) if with_sign else 1)
    return {e: c for e, c in out.items() if c}


def diff(poly: Poly, var: int) -> Poly:
    out: Poly = {}
    for e, c in poly.items():
        if e[var]:
            f = list(e)
            f[var] -= 1
            out[tuple(f)] = out.get(tuple(f), 0) + c * e[var]
    return {e: c for e, c in out.items() if c}


def poly_to_expr(poly: Poly, xs: Sequence[sp.Symbol]) -> sp.Expr:
    return sp.Add(*(c * sp.prod(x**a for x, a in zip(xs, e)) for e, c in poly.items()))


def expr_to_poly(expr: sp.Expr, xs: Sequence[sp.Symbol]) -> Poly:
    return {tuple(m): int(c) for m, c in sp.Poly(sp.expand(expr), *xs, domain=sp.ZZ).terms()}


def hessian_determinant(poly: Poly, xs: Sequence[sp.Symbol]) -> Poly:
    entries = []
    for i in range(N):
        row = []
        di = diff(poly, i)
        for j in range(N):
            row.append(poly_to_expr(diff(di, j), xs))
        entries.append(row)
    return expr_to_poly(sp.Matrix(entries).det(method="domain-ge"), xs)


def monomials(n: int, degree: int) -> Iterator[Exp]:
    if n == 1:
        yield (degree,)
        return
    for a in range(degree + 1):
        for tail in monomials(n - 1, degree - a):
            yield (a,) + tail


def factorial_ratio(gamma: Exp, beta: Exp) -> int:
    r = 1
    for g, b in zip(gamma, beta):
        for q in range(b + 1, g + 1):
            r *= q
    return r


def catalecticant_entries(poly: Poly, a: int):
    row_basis = list(monomials(N, a))
    col_basis = list(monomials(N, D - a))
    col_index = {e: j for j, e in enumerate(col_basis)}
    rows: Dict[int, Dict[int, int]] = {}
    for i, alpha in enumerate(row_basis):
        row: Dict[int, int] = {}
        for gamma, coeff in poly.items():
            if all(g >= b for g, b in zip(gamma, alpha)):
                beta = tuple(g - b for g, b in zip(gamma, alpha))
                j = col_index[beta]
                row[j] = row.get(j, 0) + coeff * factorial_ratio(gamma, beta)
        row = {j: v for j, v in row.items() if v}
        if row:
            rows[i] = row
    return (len(row_basis), len(col_basis)), rows


def sparse_rank_mod(rows_in: Dict[int, Dict[int, int]], ncols: int, p: int) -> int:
    pivots: Dict[int, Dict[int, int]] = {}
    for ridx in sorted(rows_in):
        row = {j: v % p for j, v in rows_in[ridx].items() if v % p}
        while row:
            lead = min(row)
            if lead not in pivots:
                inv = pow(row[lead], -1, p)
                row = {j: (v * inv) % p for j, v in row.items() if (v * inv) % p}
                pivots[lead] = row
                break
            factor = row[lead]
            pivot = pivots[lead]
            for j, v in pivot.items():
                nv = (row.get(j, 0) - factor * v) % p
                if nv:
                    row[j] = nv
                elif j in row:
                    del row[j]
    return len(pivots)


def poly_hash(poly: Poly) -> str:
    payload = [[list(e), [int(c), 1]] for e, c in sorted(poly.items(), reverse=True)]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def matrix_hash(shape: Tuple[int, int], rows: Dict[int, Dict[int, int]]) -> str:
    triples = [[i, j, int(rows[i][j])] for i in sorted(rows) for j in sorted(rows[i])]
    payload = {"shape": list(shape), "entries": triples}
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--primary", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=Path("certificates/independent_catalecticant_check.json"))
    args = ap.parse_args()

    primary = json.loads(args.primary.read_text(encoding="utf-8")) if args.primary else None
    xs = sp.symbols("x11 x12 x13 x21 x22 x23 x31 x32 x33")
    det3 = permanent_dict(True)
    per3 = permanent_dict(False)
    Ddet = hessian_determinant(det3, xs)
    Dper = hessian_determinant(per3, xs)

    expected_poly_hashes = primary["polynomial_hashes"] if primary else None
    actual_poly_hashes = {
        "det3": poly_hash(det3),
        "per3": poly_hash(per3),
        "Ddet3": poly_hash(Ddet),
        "Dper3": poly_hash(Dper),
    }
    if primary and actual_poly_hashes != expected_poly_hashes:
        raise AssertionError(f"polynomial hash disagreement: {actual_poly_hashes} != {expected_poly_hashes}")

    rows_out: List[dict] = []
    for a in range(10):
        entry = {"a": a, "forms": {}}
        primary_row = primary["catalecticants"][a] if primary else None
        for name, poly, rank_key, matrix_key in (
            ("Ddet", Ddet, "rank_Ddet", "matrix_sha256_Ddet"),
            ("Dper", Dper, "rank_Dperm", "matrix_sha256_Dperm"),
        ):
            shape, entries = catalecticant_entries(poly, a)
            ranks = {str(p): sparse_rank_mod(entries, shape[1], p) for p in PRIMES}
            expected = int(primary_row[rank_key]) if primary else None
            if primary and any(r != expected for r in ranks.values()):
                raise AssertionError(f"rank mismatch a={a} {name}: {ranks}, expected {expected}")
            mh = matrix_hash(shape, entries)
            if primary and matrix_key in primary_row and mh != primary_row[matrix_key]:
                raise AssertionError(f"matrix hash mismatch a={a} {name}")
            form_entry = {
                "shape": list(shape),
                "nnz": sum(len(r) for r in entries.values()),
                "matrix_sha256": mh,
                "ranks_mod_p": ranks,
            }
            if expected is not None:
                form_entry["expected_rank_Q_from_primary"] = expected
            entry["forms"][name] = form_entry
        rows_out.append(entry)

    cert = {
        "schema": "reverse_hessian.independent_catalecticant_check.v2",
        "deterministic": True,
        "engine": "clean-room exponent dictionaries + custom sparse Gaussian elimination modulo primes",
        "imports_primary_code": False,
        "primes": list(PRIMES),
        "polynomial_hashes": actual_poly_hashes,
        "checks": rows_out,
        "result": ("all independently reconstructed modular ranks equal the primary exact-Q ranks" if primary else "independent polynomial, matrix, and modular-rank reconstruction completed"),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["result"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
