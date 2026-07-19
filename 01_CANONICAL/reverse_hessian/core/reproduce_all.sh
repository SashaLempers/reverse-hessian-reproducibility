#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONHASHSEED=0
python3 -B run_all.py
python3 -B scripts/check_reproducibility.py
python3 -B -m pytest -q
(cd certificates && sha256sum -c SHA256SUMS.txt)
