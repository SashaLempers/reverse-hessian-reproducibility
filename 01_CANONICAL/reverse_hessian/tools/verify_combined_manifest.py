#!/usr/bin/env python3
"""Verify the deterministic-file SHA-256 manifest of the combined package."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "SHA256SUMS.txt"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    failures: list[str] = []
    checked = 0
    for raw in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        expected, rel = raw.split("  ", 1)
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"MISSING {rel}")
            continue
        actual = sha256(path)
        checked += 1
        if actual != expected:
            failures.append(f"MISMATCH {rel}: {actual} != {expected}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"combined manifest: {checked} deterministic files verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
