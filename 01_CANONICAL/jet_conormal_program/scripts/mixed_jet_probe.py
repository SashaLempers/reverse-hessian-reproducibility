#!/usr/bin/env python3
"""Exact pointwise mixed-jet flattening ranks for det4 and ell*per3."""
from __future__ import annotations
import argparse, itertools, json
from pathlib import Path
import sympy as sp
from sparse_poly import det_terms, padded_per_terms, derivative_eval, multiset_monomials

N = 16


def flattening(poly, total_order, left_order, point):
    left = list(multiset_monomials(N, left_order))
    right = list(multiset_monomials(N, total_order - left_order))
    matrix = sp.Matrix([
        [derivative_eval(poly, tuple(sorted(a + b)), point) for b in right]
        for a in left
    ])
    return matrix


def record(name, poly, point):
    probes = []
    for total_order, left_order in ((2, 1), (3, 1), (4, 1), (4, 2)):
        matrix = flattening(poly, total_order, left_order, point)
        probes.append({
            "total_order": total_order,
            "split": [left_order, total_order - left_order],
            "shape": list(matrix.shape),
            "rank_Q_exact": int(matrix.rank()),
        })
    return {"form": name, "ambient_variables": N, "point": list(point), "probes": probes}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    det_point = [0] * N
    for i in range(3):
        det_point[4 * i + i] = 1

    per_point = [0] * N
    per_point[0] = 1
    witness = ((-2, 1, 1), (1, 1, 1), (1, 1, 1))
    for i in range(3):
        for j in range(3):
            per_point[1 + 3 * i + j] = witness[i][j]

    result = {
        "schema": "reverse_hessian.mixed_jet_pointwise.v1",
        "arithmetic": "exact over Q via SymPy",
        "records": [
            record("det4_at_rank3", det_terms(4), det_point),
            record("ell_per3_at_uniform_zero", padded_per_terms(3, 4), per_point),
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
