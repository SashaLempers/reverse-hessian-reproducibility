#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ $# -lt 1 ]]; then echo "usage: $0 /absolute/external/output [jobs]" >&2; exit 2; fi
OUT="$(python3 -B - "$1" "$ROOT" <<'PY'
from pathlib import Path
import sys
out=Path(sys.argv[1]).expanduser().resolve(); root=Path(sys.argv[2]).resolve()
if out in {Path('/'),Path('.').resolve(),root} or root in out.parents or out == root or out.parent == out:
 raise SystemExit('refusing unsafe or in-tree output path')
print(out)
PY
)"
JOBS="${2:-${NVSNVP_JOBS:-1}}"; PYTHON="${PYTHON:-python3}"; CXX="${CXX:-g++}"
if [[ -z "$OUT" || "$OUT" == "/" || "$OUT" == "." || "$OUT" == ".." ]]; then exit 2; fi
rm -rf -- "$OUT"; mkdir -p "$OUT"/{certificates,forensic,logs,young_contractions,bin}
run_logged(){ local name="$1"; shift; set +e; "$@" >"$OUT/logs/$name.stdout" 2>"$OUT/logs/$name.stderr"; rc=$?; set -e; printf '%s\n' "$rc" >"$OUT/logs/$name.exit"; [[ $rc -eq 0 ]] || return "$rc"; }
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS="$JOBS" LC_ALL=C.UTF-8 TZ=UTC
run_logged compound_hessian_r2 "$PYTHON" -B "$ROOT/scripts/compound_hessian_r2.py" --out "$OUT/certificates/compound_hessian_r2_three_primes.json" --max-fitting-s 2 --max-cat-k 2 --prime-count 3
run_logged exact_fitting_s0 "$PYTHON" -B "$ROOT/scripts/exact_fitting_s0.py" --out "$OUT/certificates/exact_fitting_s0.json"
run_logged exact_fitting_s1 "$PYTHON" -B "$ROOT/scripts/exact_fitting_s1.py" --out "$OUT/certificates/exact_fitting_s1.json"
run_logged exact_fitting_s2 "$PYTHON" -B "$ROOT/scripts/exact_fitting_s2.py" --out "$OUT/certificates/exact_fitting_s2.json"
run_logged representation_decomposition "$PYTHON" -B "$ROOT/scripts/representation_decomposition.py" --out "$OUT/certificates/representation_decomposition.json"
run_logged compound_hessian_r3_per "$PYTHON" -B "$ROOT/scripts/compound_hessian_r3_s0.py" --forms z_per3 --out "$OUT/certificates/compound_hessian_r3_per_s0.json"
run_logged r3_det_lower_bound "$PYTHON" -B "$ROOT/scripts/r3_det_lower_bound.py" --target 10000 --out "$OUT/forensic/r3_det_rank_lower_6832_full_witness.json"
run_logged export_young_contractions "$PYTHON" -B "$ROOT/scripts/export_young_contractions.py" --forms both --combo all --outdir "$OUT/young_contractions"
cp "$OUT/young_contractions/young_contractions_manifest.json" "$OUT/certificates/young_contractions_manifest.json"
run_logged compile_schur "$CXX" -O3 -std=c++17 -fopenmp "$ROOT/scripts/schur_sketch.cpp" -o "$OUT/bin/schur_sketch"
SK="$OUT/bin/schur_sketch"; YC="$OUT/young_contractions"
run_logged young_det_S42 "$SK" --input "$YC/det4_poly_poly_sym.bin" --shape 4,2 --index 1 --prime 1009 --buckets 192 --seeds 2
mv "$OUT/logs/young_det_S42.stdout" "$OUT/certificates/young_det_S2_to_S42.json"; : >"$OUT/logs/young_det_S42.stdout"
run_logged young_per_S42 "$SK" --input "$YC/z_per3_poly_poly_sym.bin" --shape 4,2 --prime 1009 --buckets 192 --seeds 2
mv "$OUT/logs/young_per_S42.stdout" "$OUT/certificates/young_per_S2_to_S42.json"; : >"$OUT/logs/young_per_S42.stdout"
run_logged young_det_S51 "$SK" --input "$YC/det4_wedge_cross_sym.bin" --shape 5,1 --index 0 --prime 1009 --buckets 192 --seeds 2
mv "$OUT/logs/young_det_S51.stdout" "$OUT/certificates/young_det_S2_to_S51_modular.json"; : >"$OUT/logs/young_det_S51.stdout"
run_logged young_per_S51 "$SK" --input "$YC/z_per3_wedge_cross_sym.bin" --shape 5,1 --prime 1009 --buckets 192 --seeds 2
mv "$OUT/logs/young_per_S51.stdout" "$OUT/certificates/young_per_S2_to_S51_modular.json"; : >"$OUT/logs/young_per_S51.stdout"
run_logged young_det_S6 "$SK" --input "$YC/det4_wedge_cross_sym.bin" --shape 6 --index 0 --prime 1009 --buckets 192 --seeds 2
mv "$OUT/logs/young_det_S6.stdout" "$OUT/certificates/young_det_S2_to_S6.json"; : >"$OUT/logs/young_det_S6.stdout"
run_logged young_per_S6 "$SK" --input "$YC/z_per3_wedge_cross_sym.bin" --shape 6 --index 0 --prime 1009 --buckets 192 --seeds 2
mv "$OUT/logs/young_per_S6.stdout" "$OUT/certificates/young_per_S2_to_S6.json"; : >"$OUT/logs/young_per_S6.stdout"
run_logged young_det_L251 "$SK" --input "$YC/det4_wedge_same_alt.bin" --shape 5,1 --index 0 --prime 1009 --buckets 192 --seeds 2
mv "$OUT/logs/young_det_L251.stdout" "$OUT/certificates/young_det_L2_to_S51.json"; : >"$OUT/logs/young_det_L251.stdout"
run_logged young_per_L251 "$SK" --input "$YC/z_per3_wedge_same_alt.bin" --shape 5,1 --prime 1009 --buckets 192 --seeds 2
mv "$OUT/logs/young_per_L251.stdout" "$OUT/certificates/young_per_L2_to_S51.json"; : >"$OUT/logs/young_per_L251.stdout"
run_logged exact_per_S51 "$PYTHON" -B "$ROOT/scripts/exact_projected_rank.py" --input "$YC/z_per3_wedge_cross_sym.bin" --partition 5,1 --index 0 --out "$OUT/certificates/exact_per_wedge_cross_sym_51_i0.json"
run_logged exact_det_S51 "$PYTHON" -B "$ROOT/scripts/det_sym51_rep_certificate.py" --input "$YC/det4_wedge_cross_sym.bin" --out "$OUT/certificates/exact_det_sym51_rank36_rep.json"
run_logged verify "$PYTHON" -B "$ROOT/verify_package.py" --root "$ROOT" --results-dir "$OUT"
printf '{"status":"PASS","profile":"full","jobs":%s}\n' "$JOBS" >"$OUT/MASTER_REPRODUCTION_ATTESTATION.json"
