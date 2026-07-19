#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export SOURCE_DATE_EPOCH=1784160000
name=a_uniform_line_formula_and_hessian_orbit_incomparability
for _ in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error "$name.tex" >/dev/null
done
rm -f "$name.aux" "$name.log" "$name.out"
