#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [[ $# -ne 1 ]]; then echo "usage: $0 /absolute/external/workspace" >&2; exit 2; fi
OUT="$(python3 -B - "$1" "$ROOT" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]).expanduser().resolve(); r=Path(sys.argv[2]).resolve()
if p in {Path('/'),r} or r in p.parents or p.parent==p: raise SystemExit('unsafe workspace')
print(p)
PY
)"
rm -rf -- "$OUT"; mkdir -p "$OUT/a" "$OUT/b"
SRC="$ROOT/01_CANONICAL/reverse_hessian/extensions/vp_vnp/paper"
for d in "$OUT/a" "$OUT/b"; do
 cp "$SRC"/*.tex "$SRC"/*.bib "$d"/
 (cd "$d" && env SOURCE_DATE_EPOCH=1784332800 FORCE_SOURCE_DATE=1 TZ=UTC LC_ALL=C.UTF-8 latexmk -pdf -interaction=nonstopmode -halt-on-error reverse_hessian_VP_VNP_upgrade.tex >latexmk.stdout 2>latexmk.stderr)
done
sha256sum "$OUT/a/reverse_hessian_VP_VNP_upgrade.pdf" "$OUT/b/reverse_hessian_VP_VNP_upgrade.pdf"
cmp "$OUT/a/reverse_hessian_VP_VNP_upgrade.pdf" "$OUT/b/reverse_hessian_VP_VNP_upgrade.pdf"
