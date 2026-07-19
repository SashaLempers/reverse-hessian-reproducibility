#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
JOBS="${NVSNVP_JOBS:-1}"
if [[ "$JOBS" != "1" ]]; then
  echo "This deterministic wrapper currently executes serially; requested jobs=$JOBS." >&2
fi
bash ./rebuild_all.sh
( cd core && python3 -B scripts/check_reproducibility.py )
( cd extensions/vp_vnp && python3 -B scripts/check_reproducibility.py )
printf '%s\n' 'combined full verification, including both isolated rebuilds: OK'
