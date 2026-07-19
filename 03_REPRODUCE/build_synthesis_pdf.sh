
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:?external output directory required}"
case "$OUT" in "$ROOT"|"$ROOT"/*) echo "output must be outside sealed tree" >&2; exit 2;; esac
rm -rf "$OUT"; mkdir -p "$OUT"
cp "$ROOT/01_CANONICAL/synthesis_report/reverse_hessian_status_synthesis.tex" "$OUT/"
cp "$ROOT/01_CANONICAL/synthesis_report/claim_matrix.tex" "$OUT/"
cd "$OUT"
export SOURCE_DATE_EPOCH=1784419200 TZ=UTC LC_ALL=C.UTF-8
if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error reverse_hessian_status_synthesis.tex
else
  pdflatex -interaction=nonstopmode -halt-on-error reverse_hessian_status_synthesis.tex
  pdflatex -interaction=nonstopmode -halt-on-error reverse_hessian_status_synthesis.tex
fi
sha256sum reverse_hessian_status_synthesis.pdf > SHA256SUMS.txt
