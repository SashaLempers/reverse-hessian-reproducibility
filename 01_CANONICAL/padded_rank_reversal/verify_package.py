#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

# Rebuild mathematical certificates.
proc = subprocess.run([sys.executable, str(ROOT / "scripts" / "verify_rank_reversal.py")], cwd=ROOT)
if proc.returncode:
    raise SystemExit(proc.returncode)

verification = json.loads((ROOT / "certificates" / "verification.json").read_text())
assert verification["status"] == "PASS"
assert all(verification["checks"].values())

manifest = ROOT / "SHA256SUMS.txt"
if manifest.exists():
    for line in manifest.read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        path = ROOT / rel
        if rel in {"certificates/verification.json", "SHA256SUMS.txt"}:
            continue
        assert path.is_file(), rel
        assert sha(path) == digest, rel

print("PASS: exact mathematical certificates and package files verified")
