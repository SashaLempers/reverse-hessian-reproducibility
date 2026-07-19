#!/usr/bin/env python3
"""Minimal exact sparse-polynomial utilities for determinant/permanent probes."""
from __future__ import annotations
import itertools
from collections import Counter
from typing import Dict, Iterable, Iterator, Sequence, Tuple

Mon = Tuple[int, ...]
Poly = Dict[Mon, int]


def permutation_sign(p: Sequence[int]) -> int:
    inv = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inv & 1 else 1


def det_terms(n: int) -> Poly:
    out: Poly = {}
    for p in itertools.permutations(range(n)):
        mon = tuple(sorted(n * i + p[i] for i in range(n)))
        out[mon] = permutation_sign(p)
    return out


def padded_per_terms(m: int, n: int) -> Poly:
    """ell^(n-m) per_m in n^2 variables; ell is variable 0."""
    if not (1 <= m <= n):
        raise ValueError("require 1 <= m <= n")
    out: Poly = {}
    for p in itertools.permutations(range(m)):
        mon = tuple(sorted((0,) * (n - m) + tuple(1 + m * i + p[i] for i in range(m))))
        out[mon] = 1
    return out


def derivative(poly: Poly, alpha: Mon) -> Poly:
    ac = Counter(alpha)
    out: Poly = {}
    for mon, coeff in poly.items():
        mc = Counter(mon)
        if any(mc[i] < q for i, q in ac.items()):
            continue
        c = coeff
        rem = list(mon)
        for i, q in ac.items():
            v = mc[i]
            for j in range(q):
                c *= v - j
            for _ in range(q):
                rem.remove(i)
        key = tuple(rem)
        out[key] = out.get(key, 0) + c
    return {m: c for m, c in out.items() if c}


def derivative_eval(poly: Poly, alpha: Mon, point: Sequence[int]) -> int:
    ac = Counter(alpha)
    total = 0
    for mon, coeff in poly.items():
        mc = Counter(mon)
        if any(mc[i] < q for i, q in ac.items()):
            continue
        c = coeff
        rem = mc.copy()
        for i, q in ac.items():
            v = mc[i]
            for j in range(q):
                c *= v - j
            rem[i] -= q
        for i, q in rem.items():
            if q:
                c *= int(point[i]) ** q
        total += c
    return total


def multiset_monomials(nvars: int, degree: int) -> Iterator[Mon]:
    yield from itertools.combinations_with_replacement(range(nvars), degree)


def sparse_rank_rows(rows: Iterable[Dict[object, int]], prime: int) -> int:
    """Incremental row rank over F_prime with deterministic pivots."""
    pivots: Dict[object, Dict[object, int]] = {}
    for raw in rows:
        row = {k: int(v) % prime for k, v in raw.items() if int(v) % prime}
        while row:
            lead = min(row)
            base = pivots.get(lead)
            if base is None:
                inv = pow(row[lead], -1, prime)
                row = {k: (v * inv) % prime for k, v in row.items() if (v * inv) % prime}
                pivots[lead] = row
                break
            factor = row[lead]
            for k, value in base.items():
                z = (row.get(k, 0) - factor * value) % prime
                if z:
                    row[k] = z
                elif k in row:
                    del row[k]
    return len(pivots)
