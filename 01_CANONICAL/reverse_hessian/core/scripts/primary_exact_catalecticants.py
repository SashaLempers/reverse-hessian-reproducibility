#!/usr/bin/env python3
"""Primary exact reconstruction of the n=3 Hessian forms and catalecticants.

This engine uses SymPy's polynomial and DomainMatrix layers.  It imports no
project-local mathematical code.  Certificates are deterministic: no paths,
timestamps, host names, or elapsed times are serialized.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from itertools import permutations
from math import prod
from pathlib import Path
from typing import Dict, Iterator, Sequence, Tuple

import sympy as sp
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix

NVAR = 9
DEGREE = 9
Exponent = Tuple[int, ...]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permutation_sign(p: Sequence[int]) -> int:
    inversions = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inversions % 2 else 1


def compositions(parts: int, total: int) -> Iterator[Exponent]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(parts - 1, total - first):
            yield (first,) + rest


def canonical_polynomial_payload(poly: sp.Expr, variables: Sequence[sp.Symbol]) -> list:
    p = sp.Poly(poly, *variables, domain=sp.QQ)
    return [[list(exp), [int(coeff.p), int(coeff.q)]] for exp, coeff in p.terms()]


def canonical_polynomial_hash(poly: sp.Expr, variables: Sequence[sp.Symbol]) -> str:
    raw = json.dumps(canonical_polynomial_payload(poly, variables), separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def integer_terms(poly: sp.Expr, variables: Sequence[sp.Symbol]) -> Dict[Exponent, int]:
    return {exp: int(coeff) for exp, coeff in sp.Poly(poly, *variables, domain=sp.ZZ).terms()}


def falling_factorial(n: int, k: int) -> int:
    value = 1
    for j in range(k):
        value *= n - j
    return value


def build_catalecticant(terms: Dict[Exponent, int], order: int):
    row_basis = list(compositions(NVAR, order))
    col_basis = list(compositions(NVAR, DEGREE - order))
    col_index = {exp: j for j, exp in enumerate(col_basis)}
    data: dict[int, dict[int, object]] = {}
    integer_rows: list[list[list[int]]] = []
    nnz = 0

    for i, alpha in enumerate(row_basis):
        row: dict[int, int] = {}
        for gamma, coeff in terms.items():
            if all(g >= a for g, a in zip(gamma, alpha)):
                beta = tuple(g - a for g, a in zip(gamma, alpha))
                value = coeff
                for g, a in zip(gamma, alpha):
                    value *= falling_factorial(g, a)
                if value:
                    j = col_index[beta]
                    row[j] = row.get(j, 0) + value
        row = {j: value for j, value in row.items() if value}
        integer_rows.append([[j, row[j]] for j in sorted(row)])
        if row:
            data[i] = {j: ZZ(value) for j, value in row.items()}
            nnz += len(row)

    shape = (len(row_basis), len(col_basis))
    matrix_payload = {"shape": list(shape), "rows": integer_rows}
    matrix_hash = hashlib.sha256(
        json.dumps(matrix_payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ).hexdigest()
    return DomainMatrix(data, shape, ZZ), nnz, matrix_hash


def reconstruct_forms():
    variables = sp.symbols("x11 x12 x13 x21 x22 x23 x31 x32 x33")
    x = {(i, j): variables[3 * i + j] for i in range(3) for j in range(3)}
    det3 = sum(
        permutation_sign(sigma) * prod(x[i, sigma[i]] for i in range(3))
        for sigma in permutations(range(3))
    )
    per3 = sum(prod(x[i, sigma[i]] for i in range(3)) for sigma in permutations(range(3)))
    d_det = sp.expand(sp.hessian(det3, variables).det(method="domain-ge"))
    d_per = sp.expand(sp.hessian(per3, variables).det(method="domain-ge"))
    return variables, sp.expand(det3), sp.expand(per3), d_det, d_per


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    variables, det3, per3, d_det, d_per = reconstruct_forms()
    assert sp.expand(d_det + 2 * det3**3) == 0
    det_terms = integer_terms(d_det, variables)
    per_terms = integer_terms(d_per, variables)

    expected = {
        "Ddet": [1, 9, 45, 165, 270, 270, 165, 45, 9, 1],
        "Dper": [1, 9, 45, 165, 414, 414, 165, 45, 9, 1],
    }
    direct: list[dict] = []
    for order in range(5):
        m_det, nnz_det, hash_det = build_catalecticant(det_terms, order)
        m_per, nnz_per, hash_per = build_catalecticant(per_terms, order)
        rank_det = int(m_det.rank())
        rank_per = int(m_per.rank())
        assert rank_det == expected["Ddet"][order]
        assert rank_per == expected["Dper"][order]
        direct.append(
            {
                "order": order,
                "shape": list(m_det.shape),
                "nnz": {"Ddet": nnz_det, "Dper": nnz_per},
                "matrix_sha256": {"Ddet": hash_det, "Dper": hash_per},
                "ranks_Q": {"Ddet": rank_det, "Dper": rank_per},
                "method": "direct exact DomainMatrix rank over Q",
            }
        )

    rows = list(direct)
    for order in range(5, 10):
        source = direct[9 - order]
        rows.append(
            {
                "order": order,
                "shape": [source["shape"][1], source["shape"][0]],
                "nnz": dict(source["nnz"]),
                "matrix_sha256": {
                    "Ddet": "transpose-factorial-dual-of:" + source["matrix_sha256"]["Ddet"],
                    "Dper": "transpose-factorial-dual-of:" + source["matrix_sha256"]["Dper"],
                },
                "ranks_Q": dict(source["ranks_Q"]),
                "method": f"proved catalecticant duality from order {9 - order}",
            }
        )

    rank_vectors = {
        name: [row["ranks_Q"][name] for row in rows] for name in ("Ddet", "Dper")
    }
    assert rank_vectors == expected

    certificate = {
        "schema": "reverse-hessian.primary-exact-catalecticants.v3",
        "status": "CERTIFIED-COMP (exact reproducible computation; not a proof-assistant certificate)",
        "engine": "SymPy 1.14 DomainMatrix over ZZ/QQ",
        "variable_order": [str(v) for v in variables],
        "basis_order": "weak compositions; first coordinate increasing recursively",
        "identity": "det Hess(det_3) = -2 det_3^3",
        "polynomial_monomial_counts": {"Ddet": len(det_terms), "Dper": len(per_terms)},
        "polynomial_sha256": {
            "det3": canonical_polynomial_hash(det3, variables),
            "per3": canonical_polynomial_hash(per3, variables),
            "Ddet": canonical_polynomial_hash(d_det, variables),
            "Dper": canonical_polynomial_hash(d_per, variables),
        },
        "rank_vectors": rank_vectors,
        "rows": rows,
        "script_sha256": sha256_file(Path(__file__).resolve()),
        "nonclaims": [
            "The rank inequalities do not prove orbit-closure membership.",
            "No Young, Koszul, or representation-multiplicity obstruction is certified here.",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"success": True, "rank_vectors": rank_vectors}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
