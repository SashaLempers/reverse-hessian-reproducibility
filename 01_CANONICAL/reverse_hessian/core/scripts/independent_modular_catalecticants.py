#!/usr/bin/env python3
"""Third, pure-Python modular engine for the n=3 catalecticants.

This script imports neither SymPy nor either exact engine.  It independently
reconstructs the two cubic forms, their Hessian determinants, the monomial
bases, the integer catalecticant matrices, and sparse ranks modulo four primes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from itertools import permutations
from pathlib import Path
from typing import Dict, Iterator, Tuple

NVAR = 9
DEGREE = 9
PRIMES = (101, 1009, 32003, 65521)
Exponent = Tuple[int, ...]
Polynomial = Dict[Exponent, int]


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sign(p: tuple[int, ...]) -> int:
    inv = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inv % 2 else 1


def add(poly: Polynomial, exp: Exponent, coeff: int) -> None:
    if coeff:
        poly[exp] = poly.get(exp, 0) + coeff
        if poly[exp] == 0:
            del poly[exp]


def build_cubics() -> tuple[Polynomial, Polynomial]:
    det: Polynomial = {}
    per: Polynomial = {}
    for sigma in permutations(range(3)):
        exp = [0] * NVAR
        for i in range(3):
            exp[3 * i + sigma[i]] = 1
        add(det, tuple(exp), sign(sigma))
        add(per, tuple(exp), 1)
    return det, per


def derivative(poly: Polynomial, variable: int) -> Polynomial:
    out: Polynomial = {}
    for exp, coeff in poly.items():
        if exp[variable]:
            new = list(exp)
            factor = new[variable]
            new[variable] -= 1
            add(out, tuple(new), coeff * factor)
    return out


def hessian(poly: Polynomial) -> list[list[Polynomial]]:
    first = [derivative(poly, i) for i in range(NVAR)]
    return [[derivative(first[i], j) for j in range(NVAR)] for i in range(NVAR)]


def determinant_of_monomial_matrix(matrix: list[list[Polynomial]]) -> Polynomial:
    for row in matrix:
        for entry in row:
            assert len(entry) <= 1
    out: Polynomial = {}
    for sigma in permutations(range(NVAR)):
        coeff = sign(sigma)
        exp = [0] * NVAR
        ok = True
        for i, j in enumerate(sigma):
            entry = matrix[i][j]
            if not entry:
                ok = False
                break
            (e, c), = entry.items()
            coeff *= c
            for k in range(NVAR):
                exp[k] += e[k]
        if ok:
            add(out, tuple(exp), coeff)
    return out


def canonical_hash(poly: Polynomial) -> str:
    payload = [[list(exp), [coeff, 1]] for exp, coeff in sorted(poly.items(), reverse=True)]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


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


def integer_catalecticant_rows(poly: Polynomial, order: int):
    row_basis = list(compositions(NVAR, order))
    col_basis = list(compositions(NVAR, DEGREE - order))
    col_index = {exp: j for j, exp in enumerate(col_basis)}
    rows: list[dict[int, int]] = []
    serial_rows: list[list[list[int]]] = []
    for alpha in row_basis:
        row: dict[int, int] = {}
        for gamma, coeff in poly.items():
            if all(g >= a for g, a in zip(gamma, alpha)):
                beta = tuple(g - a for g, a in zip(gamma, alpha))
                value = coeff
                for g, a in zip(gamma, alpha):
                    value *= falling(g, a)
                if value:
                    j = col_index[beta]
                    row[j] = row.get(j, 0) + value
        row = {j: value for j, value in row.items() if value}
        rows.append(row)
        serial_rows.append([[j, row[j]] for j in sorted(row)])
    shape = (len(row_basis), len(col_basis))
    matrix_hash = hashlib.sha256(
        json.dumps({"shape": list(shape), "rows": serial_rows}, separators=(",", ":"), sort_keys=True).encode()
    ).hexdigest()
    return rows, shape, matrix_hash


def sparse_rank_mod_p(integer_rows: list[dict[int, int]], prime: int) -> int:
    pivots: dict[int, dict[int, int]] = {}
    rank = 0
    for source in integer_rows:
        row = {j: value % prime for j, value in source.items() if value % prime}
        while row:
            pivot = min(row)
            if pivot not in pivots:
                inverse = pow(row[pivot], -1, prime)
                row = {j: (value * inverse) % prime for j, value in row.items() if (value * inverse) % prime}
                pivots[pivot] = row
                rank += 1
                break
            factor = row[pivot]
            pivot_row = pivots[pivot]
            for j, value in pivot_row.items():
                new_value = (row.get(j, 0) - factor * value) % prime
                if new_value:
                    row[j] = new_value
                elif j in row:
                    del row[j]
    return rank


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    det3, per3 = build_cubics()
    d_det = determinant_of_monomial_matrix(hessian(det3))
    d_per = determinant_of_monomial_matrix(hessian(per3))
    assert len(d_det) == 54 and len(d_per) == 55

    expected = {
        "Ddet": [1, 9, 45, 165, 270, 270, 165, 45, 9, 1],
        "Dper": [1, 9, 45, 165, 414, 414, 165, 45, 9, 1],
    }
    forms = {"Ddet": d_det, "Dper": d_per}
    direct: list[dict] = []
    for order in range(5):
        record = {"order": order, "forms": {}, "method": "direct pure-Python sparse elimination"}
        common_shape = None
        for name, poly in forms.items():
            rows, shape, matrix_hash = integer_catalecticant_rows(poly, order)
            common_shape = shape
            ranks = {str(p): sparse_rank_mod_p(rows, p) for p in PRIMES}
            assert all(rank == expected[name][order] for rank in ranks.values())
            record["forms"][name] = {
                "shape": list(shape),
                "nnz": sum(len(r) for r in rows),
                "integer_matrix_sha256": matrix_hash,
                "ranks_mod_p": ranks,
            }
        record["shape"] = list(common_shape)
        direct.append(record)

    rows = list(direct)
    for order in range(5, 10):
        source = direct[9 - order]
        record = {
            "order": order,
            "shape": [source["shape"][1], source["shape"][0]],
            "forms": {},
            "method": f"proved catalecticant duality from order {9 - order}; all primes exceed degree 9",
        }
        for name in forms:
            item = source["forms"][name]
            record["forms"][name] = {
                "shape": [item["shape"][1], item["shape"][0]],
                "nnz": item["nnz"],
                "integer_matrix_sha256": "transpose-factorial-dual-of:" + item["integer_matrix_sha256"],
                "ranks_mod_p": dict(item["ranks_mod_p"]),
            }
        rows.append(record)

    rank_vectors = {
        name: [rows[order]["forms"][name]["ranks_mod_p"][str(PRIMES[0])] for order in range(10)]
        for name in forms
    }
    assert rank_vectors == expected

    certificate = {
        "schema": "reverse-hessian.independent-modular-catalecticants.v3",
        "status": "CERTIFIED-COMP (third independent modular reproduction; not a proof-assistant certificate)",
        "engine": "pure Python exponent dictionaries and sparse Gaussian elimination",
        "imports_sympy": False,
        "independent_of": [
            "scripts/primary_exact_catalecticants.py",
            "scripts/independent_exact_catalecticants.py",
        ],
        "primes": list(PRIMES),
        "variable_order": ["x11", "x12", "x13", "x21", "x22", "x23", "x31", "x32", "x33"],
        "polynomial_sha256": {"Ddet": canonical_hash(d_det), "Dper": canonical_hash(d_per)},
        "rank_vectors": rank_vectors,
        "rows": rows,
        "script_sha256": file_hash(Path(__file__).resolve()),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"success": True, "primes": list(PRIMES), "rank_vectors": rank_vectors}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
