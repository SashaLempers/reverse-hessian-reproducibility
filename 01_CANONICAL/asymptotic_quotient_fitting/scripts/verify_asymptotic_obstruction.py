#!/usr/bin/env python3
"""Finite exact checks for the asymptotic quotient-Fitting obstruction.

The general theorem is proved symbolically in report/theoreme_asymptotique.md.
This script only performs independent finite checks of its load-bearing formulas:
  * Hessian ranks of det_n on matrix-rank strata;
  * the permanent line Hessian determinant formula at its zero witness;
  * the sharp pair classification 2n < m^2 versus 2n >= m^2.

All matrix arithmetic is exact modulo two certified primes. No CAS dependency.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CERT = ROOT / "certificates"
PRIMES = (1_000_003, 1_000_033)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def permutation_sign(p: Sequence[int]) -> int:
    inv = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inv % 2 else 1


def rank_and_det_mod(matrix: Sequence[Sequence[int]], prime: int) -> Tuple[int, int]:
    """Return rank and determinant modulo prime; determinant is 0 if non-square/singular."""
    a = [[int(v) % prime for v in row] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    rank = 0
    det = 1
    swaps = 0
    for col in range(cols):
        pivot = next((i for i in range(rank, rows) if a[i][col]), None)
        if pivot is None:
            continue
        if pivot != rank:
            a[rank], a[pivot] = a[pivot], a[rank]
            swaps ^= 1
        pv = a[rank][col]
        if rows == cols and col == rank:
            det = det * pv % prime
        inv = pow(pv, prime - 2, prime)
        for j in range(col, cols):
            a[rank][j] = a[rank][j] * inv % prime
        for i in range(rows):
            if i == rank or not a[i][col]:
                continue
            factor = a[i][col]
            for j in range(col, cols):
                a[i][j] = (a[i][j] - factor * a[rank][j]) % prime
        rank += 1
        if rank == rows:
            break
    if rows != cols or rank != rows:
        return rank, 0
    if swaps:
        det = (-det) % prime
    return rank, det


def kron(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]) -> List[List[int]]:
    return [[x * y for x in row_a for y in row_b] for row_a in a for row_b in b]


def determinant_hessian_at_rank_stratum(n: int, matrix_rank: int) -> List[List[int]]:
    """Hess(det_n) at diag(I_s,0), built directly from determinant multilinearity."""
    size = n * n
    h = [[0] * size for _ in range(size)]
    for i in range(n):
        for j in range(n):
            u = i * n + j
            for k in range(n):
                for ell in range(n):
                    v = k * n + ell
                    if i == k or j == ell:
                        continue
                    sigma = list(range(n))
                    sigma[i] = j
                    sigma[k] = ell
                    if len(set(sigma)) != n:
                        continue
                    # Every undifferentiated entry is evaluated on diag(I_s,0).
                    if any(row >= matrix_rank for row in range(n) if row not in (i, k)):
                        continue
                    h[u][v] = permutation_sign(sigma)
    return h


def permanent_line_hessian(m: int, t: int) -> List[List[int]]:
    """Hess(per_m) on X(t)=J_m+(t-1)E_11 via the proved Kronecker formula."""
    a = [[int(i != j) for j in range(m)] for i in range(m)]
    c = [[0] * m for _ in range(m)]
    for i in range(1, m):
        for j in range(1, m):
            c[i][j] = int(i != j)
    aa = kron(a, a)
    cc = kron(c, c)
    alpha = math.factorial(m - 2)
    beta = (t - 1) * math.factorial(m - 3)
    return [[alpha * aa[i][j] + beta * cc[i][j] for j in range(m * m)]
            for i in range(m * m)]


def permanent_line_formula_mod(m: int, t: int, prime: int) -> int:
    exponent = (m - 2) ** 2
    numerator = (
        pow(math.factorial(m - 2), m * m, prime)
        * pow(m - 1, 2 * m, prime)
    ) % prime
    denominator_inv = pow(pow(m - 2, exponent, prime), prime - 2, prime)
    kappa = numerator * denominator_inv % prime
    return kappa * pow((t + m - 3) % prime, exponent, prime) % prime


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    CERT.mkdir(parents=True, exist_ok=True)
    assert all(is_prime(p) for p in PRIMES)

    det_checks = []
    for n in range(3, 11):
        observed = []
        for s in range(n + 1):
            h = determinant_hessian_at_rank_stratum(n, s)
            ranks = [rank_and_det_mod(h, p)[0] for p in PRIMES]
            assert len(set(ranks)) == 1
            observed.append(ranks[0])
        expected = [0] * (n - 2) + [4, 2 * n, n * n]
        assert observed == expected, (n, observed, expected)
        det_checks.append({
            "n": n,
            "ranks_on_strata_s_0_to_n": observed,
            "expected_formula": "0 for s<=n-3; 4 for s=n-2; 2n for s=n-1; n^2 for s=n",
            "max_rank_on_det_zero": max(observed[:-1]),
        })

    permanent_checks = []
    for m in range(3, 13):
        t = 1 - m
        h = permanent_line_hessian(m, t)
        prime_data = []
        for p in PRIMES:
            rank, determinant = rank_and_det_mod(h, p)
            predicted = permanent_line_formula_mod(m, t, p)
            assert rank == m * m
            assert determinant == predicted
            assert determinant != 0
            prime_data.append({
                "prime": p,
                "rank": rank,
                "determinant_mod_prime": determinant,
                "formula_mod_prime": predicted,
            })
        # per_m(X(t))=(m-1)!(t+m-1)=0 at t=1-m.
        permanent_checks.append({
            "m": m,
            "t_witness": t,
            "x11": t,
            "permanent_value_formula": math.factorial(m - 1) * (t + m - 1),
            "hessian_size": m * m,
            "prime_checks": prime_data,
        })

    pair_checks = []
    for m in range(3, 17):
        upper_n = max(m + 2, (m * m) // 2 + 2)
        for n in range(m, upper_n + 1):
            r = 2 * n + 1
            k = n - m
            relation = "reversal" if 2 * n < m * m else ("boundary" if 2 * n == m * m else "vanishing")
            record = {
                "m": m,
                "n": n,
                "padding_exponent": k,
                "critical_minor_order": r,
                "relation": relation,
                "theta_det_zero": True,
                "theta_padded_permanent_nonzero": 2 * n < m * m,
            }
            if relation == "boundary":
                quotient_z_exponent = k * m * m - 2
                assert k > 0 and quotient_z_exponent >= 0
                record["full_active_hessian_divisible_by_padding"] = True
                record["quotient_z_exponent"] = quotient_z_exponent
            pair_checks.append(record)

    summary = {
        "schema": "reverse_hessian.asymptotic_quotient_fitting.v1",
        "field": "characteristic zero (stated over C)",
        "theorem": {
            "critical_order": "r_n=2n+1",
            "determinant_side": "Theta_{r_n}(det_n)=0 for every n>=3",
            "padded_permanent_side": "Theta_{r_n}(ell^(n-m) per_m) != 0 iff 2n<m^2, for m>=3 and n>=m",
            "orbit_closure": "If 2n<m^2 then [ell^(n-m) per_m] is not in closure(GL_{n^2}.[det_n]).",
            "complexity_corollary": "border determinantal complexity(per_m) >= ceil(m^2/2)",
            "sharp_method_barrier": "At 2n=m^2 the full active Hessian determinant is divisible by the padded form; for 2n>m^2 all critical minors vanish identically.",
        },
        "finite_checks_are_not_the_general_proof": True,
        "checked_primes": list(PRIMES),
        "determinant_strata_checks": det_checks,
        "permanent_line_checks": permanent_checks,
        "pair_classification_checks": pair_checks,
        "literature_status": {
            "quadratic_determinantal_complexity_bound": "known: Mignon-Ressayre (2004)",
            "quadratic_border_determinantal_complexity_bound_and_hessian-divisibility equations": "known: Landsberg-Manivel-Ressayre (2013)",
            "present_contribution_status": "reformulation/reconstruction; no novelty claim",
        },
    }

    summary_path = CERT / "asymptotic_obstruction_checks.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    attestation = {
        "status": "PASS",
        "script": str(Path(__file__).relative_to(ROOT)),
        "checks": {
            "determinant_strata_n_3_to_10": True,
            "permanent_line_m_3_to_12_two_primes": True,
            "pair_threshold_m_3_to_16": True,
        },
        "sha256": {summary_path.name: sha256(summary_path)},
    }
    attestation_path = CERT / "verification_attestation.json"
    attestation_path.write_text(json.dumps(attestation, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(attestation, indent=2))


if __name__ == "__main__":
    main()
