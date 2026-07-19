#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
export PYTHONHASHSEED=0

(
  cd core
  python3 -B run_all.py
)
(
  cd extensions/vp_vnp
  python3 -B run_all.py
)
./verify_all.sh
printf '%s\n' 'combined deterministic certificate rebuild: OK'
