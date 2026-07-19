#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate_dir", type=Path)
    args = parser.parse_args()
    paths = sorted(path for path in args.certificate_dir.glob("*.json") if path.is_file())
    content = "".join(f"{digest(path)}  {path.name}\n" for path in paths)
    (args.certificate_dir / "SHA256SUMS.txt").write_text(content, encoding="utf-8")
    print(f"wrote {len(paths)} certificate hashes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
