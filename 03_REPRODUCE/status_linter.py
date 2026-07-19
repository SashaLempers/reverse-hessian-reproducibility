
#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
errors = []
for forbidden in [ROOT / "01_CANONICAL/prime_discovery_source_incomplete", ROOT / "01_CANONICAL/audit_initial"]:
    if forbidden.exists(): errors.append(f"forbidden active directory: {forbidden.relative_to(ROOT)}")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
for phrase in ["does **not** prove `VP != VNP`", "does **not** establish a super-polynomial", "Finite computations do not replace general proofs"]:
    if phrase not in readme: errors.append(f"missing non-claim: {phrase}")
for required in [
    ROOT / "01_CANONICAL/synthesis_report/reverse_hessian_status_synthesis.tex",
    ROOT / "01_CANONICAL/synthesis_report/reverse_hessian_status_synthesis.pdf",
    ROOT / ".github/workflows/verify.yml",
]:
    if not required.is_file(): errors.append(f"missing required file: {required.relative_to(ROOT)}")
obj = {"schema": "reverse_hessian.status_linter.v2.1", "status": "PASS" if not errors else "FAIL", "errors": errors}
print(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2))
raise SystemExit(0 if not errors else 1)
