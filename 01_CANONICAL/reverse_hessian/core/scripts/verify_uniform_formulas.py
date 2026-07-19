#!/usr/bin/env python3
"""Finite exact checks for the uniform paper proofs, including n=3,...,8."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import sympy as sp


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def determinant_constant(n: int) -> int:
    return (n - 1) * ((-1) ** (((n - 1) * (n + 2)) // 2))


def determinant_hessian_at_identity(n: int) -> sp.Matrix:
    pairs = [(i, j) for i in range(n) for j in range(n)]
    return sp.Matrix(
        [
            [int(i == j) * int(k == l) - int(i == l) * int(j == k) for k, l in pairs]
            for i, j in pairs
        ]
    )


def kappa(n: int) -> sp.Integer:
    return (
        sp.factorial(n - 2) ** (n * n)
        * sp.Integer(n - 1) ** (2 * n)
        // (sp.Integer(n - 2) ** ((n - 2) ** 2))
    )


def direct_permanent_hessian_line_matrix(n: int, t: sp.Symbol) -> sp.Matrix:
    size = n * n
    matrix = sp.zeros(size)
    for i in range(n):
        for j in range(n):
            a = i * n + j
            for k in range(n):
                for l in range(n):
                    b = k * n + l
                    if i == k or j == l:
                        value = 0
                    else:
                        complementary_minor_contains_11 = i != 0 and k != 0 and j != 0 and l != 0
                        value = math.factorial(n - 2)
                        if complementary_minor_contains_11:
                            value += (t - 1) * math.factorial(n - 3)
                    matrix[a, b] = value
    return matrix


def spectral_record(n: int) -> dict:
    a = sp.ones(n) - sp.eye(n)
    c = sp.zeros(n)
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                c[i, j] = 1
    b = a.inv() * c
    lam = sp.symbols("lambda")
    characteristic = sp.factor(b.charpoly(lam).as_expr())
    predicted = sp.factor(lam**2 * (lam - 1) ** (n - 2))
    assert sp.expand(characteristic - predicted) == 0
    u = sp.Matrix([0] + [1] * (n - 1))
    e1 = sp.Matrix([1] + [0] * (n - 1))
    assert b * e1 == sp.zeros(n, 1)
    assert b * u == (n - 2) * e1
    return {
        "B_characteristic_polynomial": str(characteristic),
        "B_eigenvalue_1_algebraic_multiplicity": n - 2,
        "B_eigenvalue_0_algebraic_multiplicity": 2,
        "B_e1": [int(x) for x in b * e1],
        "B_u": [int(x) for x in b * u],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    determinant_checks = []
    for n in range(2, 9):
        actual = int(determinant_hessian_at_identity(n).det(method="domain-ge"))
        predicted = determinant_constant(n)
        assert actual == predicted
        determinant_checks.append({"n": n, "actual": actual, "predicted": predicted})

    t = sp.symbols("t")
    permanent_checks = []
    for n in range(3, 9):
        hessian_line = direct_permanent_hessian_line_matrix(n, t)
        actual = sp.factor(hessian_line.det(method="domain-ge"))
        expected = sp.factor(kappa(n) * (t + n - 3) ** ((n - 2) ** 2))
        assert sp.expand(actual - expected) == 0
        permanent_checks.append(
            {
                "n": n,
                "method": "direct n^2 by n^2 complementary-minor Hessian matrix and exact determinant",
                "constant_Kn": str(kappa(n)),
                "factorization": str(actual),
                "root": str(3 - n),
                "root_multiplicity": (n - 2) ** 2,
                "excluded_power_exponent": n * (n - 2),
                "spectral_crosscheck": spectral_record(n),
            }
        )

    certificate = {
        "schema": "reverse-hessian.uniform-formulas-check.v3",
        "status": "CERTIFIED-COMP finite exact checks; the uniform statements are proved in the paper",
        "determinant_constants_n_2_to_8": determinant_checks,
        "permanent_line_restrictions_n_3_to_8": permanent_checks,
        "multiplicity_sequence_n_3_to_8": [record["root_multiplicity"] for record in permanent_checks],
        "script_sha256": file_hash(Path(__file__).resolve()),
        "nonclaim": "Finite checks through n=8 do not replace the symbolic proof for all n.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "success": True,
                "determinant_n": list(range(2, 9)),
                "permanent_n": list(range(3, 9)),
                "multiplicities": certificate["multiplicity_sequence_n_3_to_8"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
