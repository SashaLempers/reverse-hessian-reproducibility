#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(script: str, output_name: str):
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / output_name
        subprocess.run([sys.executable, str(ROOT / "scripts" / script), "--out", str(out)], check=True, stdout=subprocess.DEVNULL)
        expected = ROOT / "certificates" / output_name
        if json.loads(out.read_text()) != json.loads(expected.read_text()):
            raise SystemExit(f"mismatch: {output_name}")
        return sha256(expected)

def main():
    hashes = {
        "mixed_jet_exact.json": run("mixed_jet_probe.py", "mixed_jet_exact.json"),
        "jacobian_linear_syzygies_exact.json": run("jacobian_linear_syzygies.py", "jacobian_linear_syzygies_exact.json"),
    }
    print(json.dumps({"status": "PASS", "verified": hashes}, indent=2))

if __name__ == "__main__":
    main()
