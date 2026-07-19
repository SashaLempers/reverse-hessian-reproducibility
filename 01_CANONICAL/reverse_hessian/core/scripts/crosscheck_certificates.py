#!/usr/bin/env python3
"""Reject the run unless the three catalecticant engines agree exactly."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--exact", type=Path, required=True)
    parser.add_argument("--modular", type=Path, required=True)
    parser.add_argument("--squarefree", type=Path, required=True)
    parser.add_argument("--uniform", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    primary = load(args.primary)
    exact = load(args.exact)
    modular = load(args.modular)
    squarefree = load(args.squarefree)
    uniform = load(args.uniform)

    assert primary["rank_vectors"] == exact["rank_vectors"] == modular["rank_vectors"]
    for name in ("Ddet", "Dper"):
        assert primary["polynomial_sha256"][name] == exact["polynomial_sha256"][name]
        assert primary["polynomial_sha256"][name] == modular["polynomial_sha256"][name]
    assert squarefree["Dper3_polynomial_sha256"] == primary["polynomial_sha256"]["Dper"]
    for order in range(5):
        for name in ("Ddet", "Dper"):
            p_hash = primary["rows"][order]["matrix_sha256"][name]
            e_hash = exact["rows"][order]["matrix_sha256"][name]
            m_hash = modular["rows"][order]["forms"][name]["integer_matrix_sha256"]
            assert p_hash == e_hash == m_hash
    scripts = {
        "primary": primary["script_sha256"],
        "independent_exact": exact["script_sha256"],
        "independent_modular": modular["script_sha256"],
    }
    assert len(set(scripts.values())) == 3
    assert uniform["multiplicity_sequence_n_3_to_8"] == [1, 4, 9, 16, 25, 36]

    certificate = {
        "schema": "reverse-hessian.cross-engine-consistency.v3",
        "status": "PASS",
        "three_distinct_engine_script_sha256": scripts,
        "polynomial_hash_agreement": {
            "Ddet": primary["polynomial_sha256"]["Ddet"],
            "Dper": primary["polynomial_sha256"]["Dper"],
        },
        "direct_integer_matrix_hash_agreement_orders": [0, 1, 2, 3, 4],
        "rank_vectors": primary["rank_vectors"],
        "modular_primes": modular["primes"],
        "squarefree_Dper3_gcd_partials": squarefree["gcd_all_partials_over_Q"],
        "line_formula_multiplicities_n_3_to_8": uniform["multiplicity_sequence_n_3_to_8"],
        "script_sha256": file_hash(Path(__file__).resolve()),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"success": True, "three_distinct_engines": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
