#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT_EXCLUDES = {".work", "runtime_logs"}


def canonical_bytes(root: Path, relative: str, path: Path, modified: set[str]) -> bytes:
    if relative not in modified:
        return subprocess.check_output(
            ["git", "-C", str(root), "show", f"HEAD:{relative}"]
        )
    object_id = subprocess.check_output(
        [
            "git",
            "-C",
            str(root),
            "hash-object",
            "-w",
            f"--path={relative}",
            "--filters",
            str(path),
        ],
        text=True,
    ).strip()
    return subprocess.check_output(
        ["git", "-C", str(root), "cat-file", "blob", object_id]
    )


def tracked_entries(root: Path) -> list[tuple[str, str]]:
    output = subprocess.check_output(
        ["git", "-C", str(root), "ls-files", "--stage", "-z"]
    )
    entries = []
    for record in output.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, _object_id, stage = metadata.decode("ascii").split()
        if stage != "0":
            raise RuntimeError("tree hash requires an index without unmerged entries")
        relative = raw_path.decode("utf-8", errors="surrogateescape")
        if Path(relative).parts[0] in ROOT_EXCLUDES:
            continue
        entries.append((relative, mode))
    return sorted(entries)


def snapshot(root: Path) -> dict[str, object]:
    root = root.resolve()
    modified = set(
        subprocess.check_output(
            ["git", "-C", str(root), "diff", "--name-only", "-z", "HEAD", "--"]
        )
        .decode("utf-8", errors="surrogateescape")
        .split("\0")
    )
    rows = []
    for relative, mode in tracked_entries(root):
        path = root / relative
        data = canonical_bytes(root, relative, path, modified)
        if mode == "120000":
            target = data.decode("utf-8", errors="surrogateescape")
            rows.append({"path": relative, "type": "symlink", "mode": mode, "target": target})
        elif path.is_file():
            rows.append(
                {
                    "path": relative,
                    "type": "file",
                    "size": len(data),
                    "mode": mode,
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
        else:
            raise FileNotFoundError(f"tracked path is missing or unsupported: {relative}")
    raw = json.dumps(
        rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return {
        "root_label": root.name,
        "file_count": sum(row["type"] == "file" for row in rows),
        "entry_count": len(rows),
        "tree_sha256": hashlib.sha256(raw).hexdigest(),
        "entries": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = snapshot(args.root)
    text = json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
