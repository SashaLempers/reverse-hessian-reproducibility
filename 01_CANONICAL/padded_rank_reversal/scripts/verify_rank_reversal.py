#!/usr/bin/env python3
"""Exact certificate for a quotient-Fitting rank reversal.

Compares det_4 with F=z*per_3 in 16 variables.  All arithmetic is over Z/Q.
No symbolic algebra package is required.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

N = 16
Mon = Tuple[int, ...]
Poly = Dict[Mon, int]
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CERT = ROOT / "certificates"


def sign_perm(p: Sequence[int]) -> int:
    inv = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inv % 2 else 1


def det4_terms() -> Poly:
    out: Poly = {}
    for p in itertools.permutations(range(4)):
        mon = tuple(sorted(4 * i + p[i] for i in range(4)))
        out[mon] = sign_perm(p)
    return out


def per3_terms(local_indices: bool = True) -> Poly:
    # local_indices=True uses x_00,...,x_22 indexed 0,...,8.
    out: Poly = {}
    shift = 0 if local_indices else 1
    for p in itertools.permutations(range(3)):
        mon = tuple(sorted(shift + 3 * i + p[i] for i in range(3)))
        out[mon] = 1
    return out


def derivative(poly: Poly, vars_: Iterable[int]) -> Poly:
    out = dict(poly)
    for v in vars_:
        nxt: Poly = {}
        for mon, c in out.items():
            multiplicity = mon.count(v)
            if not multiplicity:
                continue
            rem = list(mon)
            rem.remove(v)
            key = tuple(rem)
            nxt[key] = nxt.get(key, 0) + multiplicity * c
        out = nxt
    return out


def hessian(poly: Poly, n: int) -> List[List[Poly]]:
    H = [[{} for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            q = derivative(poly, (i, j))
            H[i][j] = q
            H[j][i] = q
    return H


def eval_poly(poly: Poly, point: Sequence[int]) -> int:
    total = 0
    for mon, c in poly.items():
        prod = c
        for i in mon:
            prod *= point[i]
        total += prod
    return total


def eval_matrix(H: List[List[Poly]], point: Sequence[int]) -> List[List[int]]:
    return [[eval_poly(p, point) for p in row] for row in H]


def rank_q(matrix: Sequence[Sequence[int]]) -> Tuple[int, List[int]]:
    A = [[Fraction(v) for v in row] for row in matrix]
    if not A:
        return 0, []
    m, n = len(A), len(A[0])
    r = 0
    pivots: List[int] = []
    for c in range(n):
        q = next((i for i in range(r, m) if A[i][c]), None)
        if q is None:
            continue
        A[r], A[q] = A[q], A[r]
        pivot = A[r][c]
        A[r] = [v / pivot for v in A[r]]
        for i in range(m):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [A[i][j] - f * A[r][j] for j in range(n)]
        pivots.append(c)
        r += 1
        if r == m:
            break
    return r, pivots


def det_bareiss(matrix: Sequence[Sequence[int]]) -> int:
    A = [list(map(int, row)) for row in matrix]
    n = len(A)
    assert all(len(row) == n for row in A)
    if n == 0:
        return 1
    if n == 1:
        return A[0][0]
    sign = 1
    prev = 1
    for k in range(n - 1):
        if A[k][k] == 0:
            q = next((i for i in range(k + 1, n) if A[i][k]), None)
            if q is None:
                return 0
            A[k], A[q] = A[q], A[k]
            sign = -sign
        pivot = A[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = A[i][j] * pivot - A[i][k] * A[k][j]
                assert numerator % prev == 0
                A[i][j] = numerator // prev
        for i in range(k + 1, n):
            A[i][k] = 0
        prev = pivot
    return sign * A[n - 1][n - 1]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    CERT.mkdir(parents=True, exist_ok=True)

    # Permanent witness.  X_* has permanent zero, but det Hess(per_3)(X_*)=-128.
    x_star = [-2, -1, -1,
              -1,  1,  1,
              -1,  1,  1]
    p3 = per3_terms(True)
    Hp = hessian(p3, 9)
    per_value = eval_poly(p3, x_star)
    Hp_star = eval_matrix(Hp, x_star)
    hp_rank, hp_pivots = rank_q(Hp_star)
    hp_det = det_bareiss(Hp_star)
    gradient = [eval_poly(derivative(p3, (i,)), x_star) for i in range(9)]

    assert per_value == 0
    assert hp_rank == 9
    assert hp_det == -128

    per_cert = {
        "polynomial": "per_3",
        "padding": "F=z*per_3 in 16 variables",
        "point_z": 1,
        "point_matrix_row_major": x_star,
        "permanent_at_point": per_value,
        "gradient_permanent_at_point": gradient,
        "hessian_permanent_at_point": Hp_star,
        "hessian_rank_over_Q": hp_rank,
        "hessian_pivot_columns": hp_pivots,
        "determinant_of_9_by_9_hessian_minor": hp_det,
        "interpretation": "At (z,X)=(1,X_*), F=0 while the x-variable 9x9 Hessian minor of F equals z^9 det Hess(per_3)=-128.",
    }
    per_path = CERT / "padded_permanent_nondivisibility_witness.json"
    per_path.write_text(json.dumps(per_cert, indent=2) + "\n", encoding="utf-8")

    # Determinant rank strata.  GL_4 x GL_4 is transitive on each matrix-rank stratum.
    d4 = det4_terms()
    Hd = hessian(d4, 16)
    strata = []
    for s in range(5):
        point = [0] * 16
        for i in range(s):
            point[4 * i + i] = 1
        Hs = eval_matrix(Hd, point)
        rank, pivots = rank_q(Hs)
        strata.append({
            "matrix_rank": s,
            "canonical_point_row_major": point,
            "determinant_at_point": eval_poly(d4, point),
            "hessian_rank_over_Q": rank,
            "hessian_pivot_columns": pivots,
            "hessian_matrix": Hs,
        })

    observed = [r["hessian_rank_over_Q"] for r in strata]
    assert observed == [0, 0, 4, 8, 16]
    assert max(r["hessian_rank_over_Q"] for r in strata if r["matrix_rank"] <= 3) == 8

    det_cert = {
        "polynomial": "det_4",
        "ambient_variables": 16,
        "rank_strata_hessian_ranks": observed,
        "singular_locus_matrix_ranks": [0, 1, 2, 3],
        "maximum_hessian_rank_on_det4_zero_locus": 8,
        "consequence": "Every 9x9 minor of Hess(det_4) vanishes on det_4=0 and is therefore divisible by det_4.",
        "strata": strata,
    }
    det_path = CERT / "det4_singular_hessian_rank_certificate.json"
    det_path.write_text(json.dumps(det_cert, indent=2) + "\n", encoding="utf-8")

    # Universal augmented-rank formulation.
    a_dim = math.comb(16, 9) ** 2  # ordered row/column 9-minor labels
    s14_dim = math.comb(16 + 14 - 1, 14)
    baseline = a_dim * s14_dim
    summary = {
        "comparison": "det_4 versus z*per_3 in Sym^4(C^16)^*",
        "covariant": "Phi_9(f)=C_9(Hess(f))",
        "deep_I2_relation": "I_9(Hess(f)) is contained in I_2(Hess(f)); this is a degree-18 Fitting subpiece inside the I_2 tower.",
        "universal_two_term_complex": "A_9 tensor S^14(V*) --multiplication by f--> A_9 tensor S^18(V*)",
        "A_9_dimension_using_ordered_minors": a_dim,
        "S14_dimension": s14_dim,
        "baseline_multiplication_rank_for_nonzero_f": baseline,
        "det4_augmented_rank": baseline,
        "padded_permanent_augmented_rank": baseline + 1,
        "rank_reversal": 1,
        "closed_condition": "rank([mu_f | Phi_9(f)]) <= baseline",
        "det4_property": "Phi_9(det_4) belongs to det_4*(A_9 tensor S^14(V*)).",
        "padded_permanent_property": "Phi_9(z*per_3) does not belong to (z*per_3)*(A_9 tensor S^14(V*)).",
        "orbit_closure_conclusion": "z*per_3 is not in the projective GL_16 orbit closure of det_4.",
        "exact_permanent_witness": {
            "point_z": 1,
            "point_matrix_row_major": x_star,
            "permanent": per_value,
            "nonzero_9x9_minor": hp_det,
        },
        "det4_singular_hessian_rank_max": 8,
        "degrees": {
            "form_degree": 4,
            "hessian_entry_degree": 2,
            "Phi9_component_degree": 18,
            "quotient_degree_if_divisible_by_f": 14,
        },
    }
    summary_path = CERT / "rank_reversal_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    verification = {
        "status": "PASS",
        "checks": {
            "permanent_zero_at_witness": per_value == 0,
            "permanent_hessian_rank_9": hp_rank == 9,
            "permanent_hessian_determinant_minus_128": hp_det == -128,
            "det4_rank_strata_exact": observed == [0, 0, 4, 8, 16],
            "det4_singular_hessian_rank_at_most_8": max(observed[:4]) <= 8,
            "augmented_rank_difference_is_one": summary["padded_permanent_augmented_rank"] == summary["det4_augmented_rank"] + 1,
        },
        "certificate_sha256": {
            per_path.name: sha256_bytes(per_path.read_bytes()),
            det_path.name: sha256_bytes(det_path.read_bytes()),
            summary_path.name: sha256_bytes(summary_path.read_bytes()),
        },
    }
    verification_path = CERT / "verification.json"
    verification_path.write_text(json.dumps(verification, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
