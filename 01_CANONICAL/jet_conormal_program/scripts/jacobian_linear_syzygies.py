#!/usr/bin/env python3
"""Exact degree-one syzygy counts for Jacobian generators of det4 and ell*per3."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix
from sparse_poly import det_terms, padded_per_terms, derivative, multiset_monomials

N = 16


def compute(name, poly):
    generators = [derivative(poly, (i,)) for i in range(N)]
    columns = list(multiset_monomials(N, 4))
    column_index = {m: j for j, m in enumerate(columns)}
    data = {}
    row_index = 0
    nonzero_rows = 0
    for generator in generators:
        for variable in range(N):
            row = {}
            for mon, coeff in generator.items():
                key = tuple(sorted(mon + (variable,)))
                row[column_index[key]] = ZZ(coeff)
            if row:
                data[row_index] = row
                nonzero_rows += 1
            row_index += 1
    matrix = DomainMatrix(data, (N * N, len(columns)), ZZ)
    rank = int(matrix.rank())
    zero_generators = sum(not g for g in generators)
    raw_kernel = N * N - rank
    trivial_from_zero_generators = zero_generators * N
    return {
        "form": name,
        "matrix_shape": list(matrix.shape),
        "nonzero_jacobian_generators": N - zero_generators,
        "zero_jacobian_generators": zero_generators,
        "nonzero_rows": nonzero_rows,
        "rank_Q_exact": rank,
        "raw_linear_syzygy_dimension": raw_kernel,
        "trivial_syzygies_from_zero_generators": trivial_from_zero_generators,
        "linear_syzygies_after_removing_zero_generator_summands": raw_kernel - trivial_from_zero_generators,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = {
        "schema": "reverse_hessian.jacobian_linear_syzygies.v1",
        "arithmetic": "exact over Q via DomainMatrix over ZZ",
        "records": [
            compute("det4", det_terms(4)),
            compute("ell_per3", padded_per_terms(3, 4)),
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
