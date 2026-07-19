from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "certificates"


def load(name: str):
    return json.loads((CERT / name).read_text(encoding="utf-8"))


def test_three_engines_are_distinct_and_agree():
    primary = load("primary_exact_catalecticants.json")
    exact = load("independent_exact_catalecticants.json")
    modular = load("independent_modular_catalecticants.json")
    assert primary["rank_vectors"] == exact["rank_vectors"] == modular["rank_vectors"]
    assert len({primary["script_sha256"], exact["script_sha256"], modular["script_sha256"]}) == 3
    for form in ("Ddet", "Dper"):
        assert primary["polynomial_sha256"][form] == exact["polynomial_sha256"][form]
        assert primary["polynomial_sha256"][form] == modular["polynomial_sha256"][form]


def test_expected_rank_vectors():
    primary = load("primary_exact_catalecticants.json")
    assert primary["rank_vectors"]["Ddet"] == [1, 9, 45, 165, 270, 270, 165, 45, 9, 1]
    assert primary["rank_vectors"]["Dper"] == [1, 9, 45, 165, 414, 414, 165, 45, 9, 1]


def test_squarefree_and_line_formula():
    squarefree = load("squarefree_Dper3.json")
    uniform = load("uniform_formulas_n2_to_n8.json")
    assert squarefree["gcd_all_partials_over_Q"] == "1"
    assert squarefree["monomial_count"] == 55
    assert squarefree["line_restriction_at_J3_plus_t_minus_1_E11"] == "64*t"
    assert uniform["multiplicity_sequence_n_3_to_8"] == [1, 4, 9, 16, 25, 36]
