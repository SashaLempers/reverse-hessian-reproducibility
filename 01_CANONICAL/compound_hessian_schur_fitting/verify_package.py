#!/usr/bin/env python3
"""Verify the packaged certificates or a freshly reproduced result directory."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

EXPECTED = {
    "cat_det": [1, 16, 136],
    "cat_per": [1, 10, 55],
    "fit_det": [625, 5312, 27608],
    "fit_per": [166, 1908, 12156],
    "young": {
        "young_det_S2_to_S42.json": 136,
        "young_per_S2_to_S42.json": 55,
        "young_det_S2_to_S51_modular.json": 36,
        "young_per_S2_to_S51_modular.json": 18,
        "young_det_S2_to_S6.json": 136,
        "young_per_S2_to_S6.json": 55,
        "young_det_L2_to_S51.json": 120,
        "young_per_L2_to_S51.json": 45,
    },
    "r3_per": 849,
    "r3_det_lower": 6832,
}


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def records_by_form(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {record["form"]: record for record in data["forms"]}


def certified_rank(cert: dict[str, Any]) -> int:
    results = cert["results"]
    require(bool(results), "Young certificate has no result")
    values: list[int] = []
    for result in results:
        ranks = result["ranks"]
        require(bool(ranks) and len(set(ranks)) == 1, f"inconsistent sketch ranks: {ranks}")
        values.append(int(ranks[0]))
    # Scan certificates may contain tableau representatives on which the map
    # vanishes.  Any nonzero representative of the unique LR type yields the
    # block rank; the stored certificate records the maximum over the scan.
    return max(values)


def verify_results(results: Path) -> None:
    cert = results / "certificates"
    forensic = results / "forensic"

    r2 = records_by_form(load(cert / "compound_hessian_r2_three_primes.json"))
    cat_det = [x["rank_over_Q_exact"] for x in r2["det4"]["catalecticants"]]
    cat_per = [x["rank_over_Q_exact"] for x in r2["z_per3"]["catalecticants"]]
    require(cat_det == EXPECTED["cat_det"], f"det catalecticants: {cat_det}")
    require(cat_per == EXPECTED["cat_per"], f"per catalecticants: {cat_per}")
    require(r2["det4"]["compound_nonzero_coordinates"] == 4032, "det nonzero coordinates")
    require(r2["z_per3"]["compound_nonzero_coordinates"] == 540, "per nonzero coordinates")

    fit_det: list[int] = []
    fit_per: list[int] = []
    for s in range(3):
        d = load(cert / f"exact_fitting_s{s}.json")
        by_form = {record["form"]: record for record in d["records"]}
        fit_det.append(int(by_form["det4"]["rank_Q_exact"]))
        fit_per.append(int(by_form["z_per3"]["rank_Q_exact"]))
    require(fit_det == EXPECTED["fit_det"], f"det Fitting pieces: {fit_det}")
    require(fit_per == EXPECTED["fit_per"], f"per Fitting pieces: {fit_per}")

    rep = load(cert / "representation_decomposition.json")["records"]
    require(rep["2"]["intersection"] == [[[6, 2], 1]], "r=2 Schur intersection")
    require(rep["3"]["intersection"] == [[[8, 2, 2], 1]], "r=3 Schur intersection")
    require(rep["4"]["intersection"] == [[[10, 2, 2, 2], 1]], "r=4 Schur intersection")

    contraction_manifest = load(cert / "young_contractions_manifest.json")
    require(len(contraction_manifest) == 12, "expected 12 polarized contraction records")
    require({r["form"] for r in contraction_manifest} == {"det4", "z_per3"}, "contraction forms")
    require(len({(r["form"], r["contraction"]) for r in contraction_manifest}) == 12, "duplicate contraction record")
    generated = results / "young_contractions"
    if generated.is_dir():
        for record in contraction_manifest:
            binary = generated / record["file"]
            require(binary.is_file(), f"missing generated contraction: {record['file']}")
            digest = hashlib.sha256(binary.read_bytes()).hexdigest()
            require(digest == record["sha256"], f"contraction SHA-256 mismatch: {record['file']}")

    for filename, expected in EXPECTED["young"].items():
        actual = certified_rank(load(cert / filename))
        require(actual == expected, f"{filename}: expected {expected}, got {actual}")

    exact_per = load(cert / "exact_per_wedge_cross_sym_51_i0.json")
    require(exact_per["rank_Q_exact"] == 18, "exact permanent S2->S51 rank")
    exact_det = load(cert / "exact_det_sym51_rank36_rep.json")
    require(exact_det["conclusion_rank_Q_exact"] == 36, "exact determinant S2->S51 rank")
    require(exact_det["symmetric_symmetric_highest_weight"]["projected_zero"], "killed 100-dim summand")
    require(exact_det["exterior_exterior_highest_weight"]["projected_nonzero"], "nonzero 36-dim summand")

    r3_per = load(cert / "compound_hessian_r3_per_s0.json")["records"][0]
    require(r3_per["rank_Q_exact"] == EXPECTED["r3_per"], "r=3 permanent rank")
    r3_det = load(forensic / "r3_det_rank_lower_6832_full_witness.json")
    require(r3_det["rank_mod_p_lower_bound"] == EXPECTED["r3_det_lower"], "r=3 determinant modular rank")
    require(r3_det["rank_Q_lower_bound"] == EXPECTED["r3_det_lower"], "r=3 determinant Q lower bound")
    require(len(r3_det["witness_generator_labels"]) == EXPECTED["r3_det_lower"], "r=3 pivot witness count")

    print("Scientific certificate checks: PASS")
    print(f"  catalecticants det/per: {cat_det} / {cat_per}")
    print(f"  Fitting degrees 4..6: {fit_det} / {fit_per}")
    print("  Young ranks det/per: 136/55, 36/18, 136/55, 120/45")
    print("  r=3 degree-6 span: det >= 6832, padded permanent = 849")


def verify_manifest(root: Path) -> None:
    manifest = root / "SHA256SUMS.txt"
    require(manifest.exists(), "missing SHA256SUMS.txt")
    checked = 0
    for raw in manifest.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        digest, relative = raw.split("  ", 1)
        path = root / relative
        require(path.is_file(), f"manifest file missing: {relative}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == digest, f"SHA-256 mismatch: {relative}")
        checked += 1
    print(f"Package SHA-256 checks: PASS ({checked} files)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--results-dir", type=Path)
    parser.add_argument("--skip-manifest", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    results = (args.results_dir or root).resolve()
    if not args.skip_manifest:
        verify_manifest(root)
    verify_results(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
