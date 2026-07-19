
#!/usr/bin/env python3
from __future__ import annotations
import csv, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
errors = []

def rows(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

claims = rows(ROOT / "02_CLAIMS/SCIENTIFIC_CLAIMS_27.csv")
occ = rows(ROOT / "02_CLAIMS/CLAIM_OCCURRENCES_138_VERDICTS.csv")
anchors = rows(ROOT / "02_CLAIMS/PROOF_ANCHORS.csv")
protocols = rows(ROOT / "03_REPRODUCE/PROTOCOLS_27.csv")
ids = {r["claim_id"] for r in claims}
if len(claims) != 27: errors.append(f"claim count {len(claims)}")
if len(occ) != 138: errors.append(f"occurrence count {len(occ)}")
if {r["claim_id"] for r in anchors} != ids: errors.append("proof-anchor claim IDs do not match registry")
if {r["claim_id"] for r in protocols} != ids: errors.append("protocol claim IDs do not match registry")
for r in occ:
    if r.get("canonical_claim_id") and r["canonical_claim_id"] not in ids:
        errors.append(f"unknown mapping {r['occurrence_id']}->{r['canonical_claim_id']}")
for r in claims:
    raw = r.get("evidence_paths", "") or r.get("evidence_path", "")
    if not raw:
        errors.append(f"missing evidence {r['claim_id']}")
    for rel in [x.strip() for x in raw.split(";") if x.strip()]:
        if not (ROOT / rel).is_file():
            errors.append(f"missing evidence path {r['claim_id']}: {rel}")
obj = {
    "schema": "reverse_hessian.claim_linter.v2.1",
    "status": "PASS" if not errors else "FAIL",
    "counts": {"claims": len(claims), "occurrences": len(occ), "anchors": len(anchors), "protocols": len(protocols)},
    "errors": errors,
}
print(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2))
raise SystemExit(0 if not errors else 1)
