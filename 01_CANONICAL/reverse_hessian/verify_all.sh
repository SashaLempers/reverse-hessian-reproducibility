#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
export PYTHONHASHSEED=0

python3 -B tools/verify_combined_manifest.py

(
  cd core
  python3 -B -m pytest -q
  (cd certificates && sha256sum -c SHA256SUMS.txt)
)

(
  cd extensions/vp_vnp
  python3 -B -m unittest discover -s tests -v
  sha256sum -c certificates/SHA256SUMS.txt
)

python3 -B tools/verify_combined_manifest.py
printf '%s\n' 'combined integrity and test verification: OK'
