#!/usr/bin/env python3
"""Single deterministic entry point for all mathematical certificates."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def append_result(command: list[str], completed: subprocess.CompletedProcess[str], log_lines: list[str]) -> None:
    log_lines.append("$ " + " ".join(command))
    if completed.stdout:
        log_lines.extend(completed.stdout.rstrip("\n").splitlines())
    if completed.stderr:
        log_lines.extend("STDERR: " + line for line in completed.stderr.rstrip("\n").splitlines())
    if completed.returncode != 0:
        raise RuntimeError(f"command failed with return code {completed.returncode}: {' '.join(command)}")


def run(command: list[str], log_lines: list[str]) -> None:
    completed = subprocess.run(command, text=True, capture_output=True, check=False, env={**os.environ, "PYTHONHASHSEED": "0"})
    append_result(command, completed, log_lines)


def run_parallel(commands: list[list[str]], log_lines: list[str]) -> None:
    processes = [
        subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={**os.environ, "PYTHONHASHSEED": "0"})
        for command in commands
    ]
    results = []
    for process in processes:
        stdout, stderr = process.communicate()
        results.append(subprocess.CompletedProcess(process.args, process.returncode, stdout, stderr))
    for command, result in zip(commands, results):
        append_result(command, result, log_lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate-dir", type=Path)
    parser.add_argument("--log", type=Path)
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    certificates = args.certificate_dir or repo / "certificates"
    log_path = args.log or repo / "logs" / "full_run.log"
    certificates.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    python = sys.executable
    scripts = repo / "scripts"
    log_lines = ["reverse-hessian deterministic full run", "PYTHONHASHSEED=0"]

    run_parallel(
        [
            [python, str(scripts / "primary_exact_catalecticants.py"), "--out", str(certificates / "primary_exact_catalecticants.json")],
            [python, str(scripts / "independent_exact_catalecticants.py"), "--out", str(certificates / "independent_exact_catalecticants.json")],
            [python, str(scripts / "independent_modular_catalecticants.py"), "--out", str(certificates / "independent_modular_catalecticants.json")],
            [python, str(scripts / "certify_squarefree_Dper3.py"), "--out", str(certificates / "squarefree_Dper3.json")],
            [python, str(scripts / "verify_uniform_formulas.py"), "--out", str(certificates / "uniform_formulas_n2_to_n8.json")],
        ],
        log_lines,
    )
    run(
        [
            python,
            str(scripts / "crosscheck_certificates.py"),
            "--primary", str(certificates / "primary_exact_catalecticants.json"),
            "--exact", str(certificates / "independent_exact_catalecticants.json"),
            "--modular", str(certificates / "independent_modular_catalecticants.json"),
            "--squarefree", str(certificates / "squarefree_Dper3.json"),
            "--uniform", str(certificates / "uniform_formulas_n2_to_n8.json"),
            "--out", str(certificates / "cross_engine_consistency.json"),
        ],
        log_lines,
    )
    run([python, str(scripts / "normalize_certificates.py"), str(certificates)], log_lines)
    run([python, str(scripts / "write_sha256sums.py"), str(certificates)], log_lines)
    log_lines.append("SUCCESS: every deterministic certificate and all three-engine cross-checks passed.")
    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(json.dumps({"success": True, "certificates": str(certificates), "log": str(log_path)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
