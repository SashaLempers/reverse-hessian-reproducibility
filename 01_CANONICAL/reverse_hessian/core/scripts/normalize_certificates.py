#!/usr/bin/env python3
"""Validate deterministic certificate conventions and rewrite canonical JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

BANNED_KEYS = {"elapsed_seconds", "absolute_path", "hostname", "timestamp", "created_at", "runtime_seconds"}


def walk(value, path="root"):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in BANNED_KEYS:
                raise ValueError(f"non-deterministic key {key!r} at {path}")
            walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk(child, f"{path}[{index}]")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate_dir", type=Path)
    args = parser.parse_args()
    files = sorted(path for path in args.certificate_dir.glob("*.json") if path.is_file())
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        walk(data)
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"success": True, "normalized": [path.name for path in files]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
