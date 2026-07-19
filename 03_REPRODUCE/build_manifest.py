
#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "07_MANIFEST"
EXCLUDE = {"MANIFEST.json", "MANIFEST_SEAL.json", "SHA256SUMS.txt", "FILE_INDEX.csv"}
SKIP_PARTS = {".git", ".work", "__pycache__", ".pytest_cache"}
SKIP_SUFFIXES = {".pyc", ".pyo", ".aux", ".bbl", ".blg", ".fdb_latexmk", ".fls", ".log", ".out", ".synctex.gz"}
MODIFIED = set(subprocess.check_output(
    ["git", "-C", str(ROOT), "diff", "--name-only", "-z", "HEAD", "--"]
).decode("utf-8", errors="surrogateescape").split("\0"))

git_modes = {}
for record in subprocess.check_output(
    ["git", "-C", str(ROOT), "ls-files", "--stage", "-z"]
).split(b"\0"):
    if not record:
        continue
    metadata, raw_path = record.split(b"\t", 1)
    mode, _object_id, stage = metadata.decode("ascii").split()
    if stage != "0":
        raise RuntimeError("manifest generation requires an index without unmerged entries")
    git_modes[raw_path.decode("utf-8", errors="surrogateescape")] = mode

def h(p):
    x = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""): x.update(b)
    return x.hexdigest()

def canonical_bytes(p, rel):
    if rel not in MODIFIED:
        return subprocess.check_output(["git", "-C", str(ROOT), "show", f"HEAD:{rel}"])
    oid = subprocess.check_output([
        "git", "-C", str(ROOT), "hash-object", "-w",
        f"--path={rel}", "--filters", str(p),
    ], text=True).strip()
    return subprocess.check_output(["git", "-C", str(ROOT), "cat-file", "blob", oid])

rows = []
for p in sorted(ROOT.rglob("*"), key=lambda item: item.relative_to(ROOT).as_posix()):
    if not p.is_file(): continue
    rel_path = p.relative_to(ROOT)
    if any(part in SKIP_PARTS for part in rel_path.parts): continue
    if any(p.name.endswith(s) for s in SKIP_SUFFIXES): continue
    if p.parent == OUT and p.name in EXCLUDE: continue
    rel = rel_path.as_posix()
    git_mode = git_modes.get(rel)
    if git_mode is None:
        raise RuntimeError(f"manifest payload is not tracked by Git: {rel}")
    portable_mode = "0o755" if git_mode == "100755" else "0o644"
    data = canonical_bytes(p, rel)
    rows.append({"path":rel, "size_bytes":len(data), "sha256":hashlib.sha256(data).hexdigest(), "mode":portable_mode, "role":"canonical" if rel.startswith("01_CANONICAL/") else "metadata_or_reproduction"})
OUT.mkdir(exist_ok=True)
with (OUT / "FILE_INDEX.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n"); w.writeheader(); w.writerows(rows)
(OUT / "SHA256SUMS.txt").write_bytes("".join(f"{r['sha256']}  {r['path']}\n" for r in rows).encode("utf-8"))
manifest = {"schema":"reverse_hessian.manifest.v2.1", "file_count":len(rows), "payload_bytes":sum(r["size_bytes"] for r in rows), "files":rows}
raw = json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
(OUT / "MANIFEST.json").write_bytes(raw.encode("utf-8"))
seal = {"schema":"reverse_hessian.manifest_seal.v2.1", "manifest_sha256":hashlib.sha256(raw.encode()).hexdigest(), "file_index_sha256":h(OUT / "FILE_INDEX.csv"), "sha256sums_sha256":h(OUT / "SHA256SUMS.txt")}
(OUT / "MANIFEST_SEAL.json").write_bytes((json.dumps(seal, sort_keys=True, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"status":"PASS", "file_count":len(rows), "payload_bytes":manifest["payload_bytes"], "seal":seal}, indent=2))
