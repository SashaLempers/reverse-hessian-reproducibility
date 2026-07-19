#!/usr/bin/env python3
"""Clean-room exact engine for the n=3 Hessian forms and catalecticants.

No project-local module is imported.  The determinant and permanent are stored
as exponent dictionaries, differentiated directly, and the 9x9 polynomial
Hessian determinants are expanded by an independent permutation formula.
Only the final sparse rational ranks use SymPy DomainMatrix.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from itertools import permutations
from pathlib import Path
from typing import Dict, Iterator, Tuple

from sympy import ZZ
from sympy.polys.matrices import DomainMatrix

NVAR = 9
DEGREE = 9
Exponent = Tuple[int, ...]
Polynomial = Dict[Exponent, int]


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sign_of_permutation(p: tuple[int, ...]) -> int:
    inversions = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inversions % 2 else 1


def add_monomial(poly: Polynomial, exp: Exponent, coeff: int) -> None:
    if coeff:
        poly[exp] = poly.get(exp, 0) + coeff
        if poly[exp] == 0:
            del poly[exp]


def monomial_for_permutation(sigma: tuple[int, ...]) -> Exponent:
    exp = [0] * NVAR
    for i in range(3):
        exp[3 * i + sigma[i]] += 1
    return tuple(exp)


def base_forms() -> tuple[Polynomial, Polynomial]:
    det: Polynomial = {}
    per: Polynomial = {}
    for sigma in permutations(range(3)):
        exp = monomial_for_permutation(sigma)
        add_monomial(det, exp, sign_of_permutation(sigma))
        add_monomial(per, exp, 1)
    return det, per


def differentiate(poly: Polynomial, variable: int) -> Polynomial:
    result: Polynomial = {}
    for exp, coeff in poly.items():
        if exp[variable]:
            new_exp = list(exp)
            factor = new_exp[variable]
            new_exp[variable] -= 1
            add_monomial(result, tuple(new_exp), coeff * factor)
    return result


def hessian(poly: Polynomial) -> list[list[Polynomial]]:
    first = [differentiate(poly, i) for i in range(NVAR)]
    return [[differentiate(first[i], j) for j in range(NVAR)] for i in range(NVAR)]


def polynomial_matrix_determinant(matrix: list[list[Polynomial]]) -> Polynomial:
    # For a cubic input every second derivative is zero or a single monomial.
    for row in matrix:
        for entry in row:
            assert len(entry) <= 1
    result: Polynomial = {}
    for sigma in permutations(range(NVAR)):
        coefficient = sign_of_permutation(sigma)
        exponent = [0] * NVAR
        nonzero = True
        for i, j in enumerate(sigma):
            entry = matrix[i][j]
            if not entry:
                nonzero = False
                break
            (entry_exp, entry_coeff), = entry.items()
            coefficient *= entry_coeff
            for k in range(NVAR):
                exponent[k] += entry_exp[k]
        if nonzero:
            add_monomial(result, tuple(exponent), coefficient)
    return result


def multiply_polynomials(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for a, ca in left.items():
        for b, cb in right.items():
            add_monomial(result, tuple(x + y for x, y in zip(a, b)), ca * cb)
    return result


def power(poly: Polynomial, exponent: int) -> Polynomial:
    result: Polynomial = {(0,) * NVAR: 1}
    base = dict(poly)
    e = exponent
    while e:
        if e & 1:
            result = multiply_polynomials(result, base)
        e //= 2
        if e:
            base = multiply_polynomials(base, base)
    return result


def canonical_payload(poly: Polynomial) -> list:
    return [[list(exp), [coeff, 1]] for exp, coeff in sorted(poly.items(), reverse=True)]


def canonical_hash(poly: Polynomial) -> str:
    return hashlib.sha256(json.dumps(canonical_payload(poly), separators=(",", ":")).encode()).hexdigest()


def compositions(parts: int, total: int) -> Iterator[Exponent]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(parts - 1, total - first):
            yield (first,) + rest


def falling(n: int, k: int) -> int:
    value = 1
    for j in range(k):
        value *= n - j
    return value


def catalecticant(poly: Polynomial, order: int):
    rows = list(compositions(NVAR, order))
    columns = list(compositions(NVAR, DEGREE - order))
    column_index = {exp: j for j, exp in enumerate(columns)}
    sparse: dict[int, dict[int, object]] = {}
    serialized_rows: list[list[list[int]]] = []
    nnz = 0
    for i, alpha in enumerate(rows):
        row: dict[int, int] = {}
        for gamma, coeff in poly.items():
            if all(g >= a for g, a in zip(gamma, alpha)):
                beta = tuple(g - a for g, a in zip(gamma, alpha))
                value = coeff
                for g, a in zip(gamma, alpha):
                    value *= falling(g, a)
                if value:
                    j = column_index[beta]
                    row[j] = row.get(j, 0) + value
        row = {j: value for j, value in row.items() if value}
        serialized_rows.append([[j, row[j]] for j in sorted(row)])
        if row:
            sparse[i] = {j: ZZ(value) for j, value in row.items()}
            nnz += len(row)
    shape = (len(rows), len(columns))
    matrix_hash = hashlib.sha256(
        json.dumps({"shape": list(shape), "rows": serialized_rows}, separators=(",", ":"), sort_keys=True).encode()
    ).hexdigest()
    return DomainMatrix(sparse, shape, ZZ), nnz, matrix_hash


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    det3, per3 = base_forms()
    d_det = polynomial_matrix_determinant(hessian(det3))
    d_per = polynomial_matrix_determinant(hessian(per3))
    det_cube = power(det3, 3)
    assert d_det == {exp: -2 * coeff for exp, coeff in det_cube.items()}
    assert len(d_det) == 54
    assert len(d_per) == 55

    expected = {
        "Ddet": [1, 9, 45, 165, 270, 270, 165, 45, 9, 1],
        "Dper": [1, 9, 45, 165, 414, 414, 165, 45, 9, 1],
    }
    direct: list[dict] = []
    for order in range(5):
        md, nd, hd = catalecticant(d_det, order)
        mp, np, hp = catalecticant(d_per, order)
        rd = int(md.rank())
        rp = int(mp.rank())
        assert rd == expected["Ddet"][order]
        assert rp == expected["Dper"][order]
        direct.append(
            {
                "order": order,
                "shape": list(md.shape),
                "nnz": {"Ddet": nd, "Dper": np},
                "matrix_sha256": {"Ddet": hd, "Dper": hp},
                "ranks_Q": {"Ddet": rd, "Dper": rp},
                "method": "direct clean-room exponent-dictionary reconstruction plus exact DomainMatrix rank",
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
    rank_vectors = {name: [r["ranks_Q"][name] for r in rows] for name in ("Ddet", "Dper")}
    assert rank_vectors == expected

    certificate = {
        "schema": "reverse-hessian.independent-exact-catalecticants.v3",
        "status": "CERTIFIED-COMP (independent exact reproduction; not a proof-assistant certificate)",
        "independent_of": "scripts/primary_exact_catalecticants.py",
        "engine": "clean-room exponent dictionaries; permutation determinant; SymPy only for final exact sparse ranks",
        "variable_order": ["x11", "x12", "x13", "x21", "x22", "x23", "x31", "x32", "x33"],
        "basis_order": "weak compositions; first coordinate increasing recursively",
        "polynomial_monomial_counts": {"Ddet": len(d_det), "Dper": len(d_per)},
        "polynomial_sha256": {
            "det3": canonical_hash(det3),
            "per3": canonical_hash(per3),
            "Ddet": canonical_hash(d_det),
            "Dper": canonical_hash(d_per),
        },
        "rank_vectors": rank_vectors,
        "rows": rows,
        "script_sha256": file_hash(Path(__file__).resolve()),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"success": True, "rank_vectors": rank_vectors}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
