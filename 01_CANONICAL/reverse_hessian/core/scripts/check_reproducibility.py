#!/usr/bin/env python3
"""Rebuild certificates twice in parallel and require byte-for-byte identity."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def hashes(directory: Path) -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.glob("*.json"))
    }


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    canonical = hashes(repo / "certificates")
    with tempfile.TemporaryDirectory(prefix="reverse_hessian_repro_") as temp:
        root = Path(temp)
        outputs = [root / "run1", root / "run2"]
        processes = []
        for index, output in enumerate(outputs, start=1):
            output.mkdir(parents=True, exist_ok=True)
            processes.append(
                subprocess.Popen(
                    [
                        sys.executable,
                        str(repo / "scripts" / "run_all.py"),
                        "--certificate-dir",
                        str(output),
                        "--log",
                        str(root / f"run{index}.log"),
                    ],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            )
        for process in processes:
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                raise RuntimeError(f"fresh rebuild failed\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")
        first, second = (hashes(output) for output in outputs)
        assert first == second, "two fresh rebuilds differ"
        assert canonical == first, "checked-in certificates differ from a fresh rebuild"
    print(
        json.dumps(
            {
                "success": True,
                "byte_for_byte_reproducible": True,
                "two_fresh_rebuilds": True,
                "certificate_sha256": canonical,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
