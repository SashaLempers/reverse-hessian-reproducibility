#!/usr/bin/env python3
"""Modular low-bidegree probe of the unsaturated projective Gauss-graph ideal.

Generators are y_i f_j - y_j f_i, of bidegree (deg(f)-1,1).
The computation is exploratory: modular ranks are rigorous lower bounds over Q;
agreement across primes is not by itself an exact-rank proof.
"""
from __future__ import annotations
import argparse, itertools, json
from pathlib import Path
from sparse_poly import det_terms, padded_per_terms, derivative, multiset_monomials, sparse_rank_rows

N = 16
PRIMES = (1009, 10007, 32003)


def graph_generators(poly):
    grad = [derivative(poly, (i,)) for i in range(N)]
    out = []
    for i in range(N):
        for j in range(i + 1, N):
            row = {}
            for mon, coeff in grad[j].items():
                row[(mon, (i,))] = row.get((mon, (i,)), 0) + coeff
            for mon, coeff in grad[i].items():
                row[(mon, (j,))] = row.get((mon, (j,)), 0) - coeff
            out.append({k: v for k, v in row.items() if v})
    return out


def shifted_rows(generators, x_shift, y_shift):
    x_mons = list(multiset_monomials(N, x_shift))
    y_mons = list(multiset_monomials(N, y_shift))
    for generator in generators:
        if not generator:
            continue
        for xm in x_mons:
            for ym in y_mons:
                row = {}
                for (xmon, ymon), coeff in generator.items():
                    key = (tuple(sorted(xmon + xm)), tuple(sorted(ymon + ym)))
                    row[key] = row.get(key, 0) + coeff
                yield row


def compute(name, poly):
    generators = graph_generators(poly)
    pieces = []
    for x_shift, y_shift in ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2)):
        rows = list(shifted_rows(generators, x_shift, y_shift))
        ranks = {str(p): sparse_rank_rows(iter(rows), p) for p in PRIMES}
        pieces.append({
            "x_shift": x_shift,
            "y_shift": y_shift,
            "number_of_nonzero_rows": len(rows),
            "ranks_mod_p": ranks,
        })
    return {
        "form": name,
        "base_generators_total": 120,
        "base_generators_nonzero": sum(bool(g) for g in generators),
        "pieces": pieces,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = {
        "schema": "reverse_hessian.unsaturated_conormal_graph_probe.v1",
        "status": "exploratory modular lower bounds",
        "primes": list(PRIMES),
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
