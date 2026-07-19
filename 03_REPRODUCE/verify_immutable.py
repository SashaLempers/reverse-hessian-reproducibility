
#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "03_REPRODUCE"))
from treehash import snapshot
from safe_paths import checked_external, safe_rmtree

def run(name, cmd, cwd, logs, env):
    p = subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True)
    (logs / f"{name}.stdout").write_text(p.stdout, encoding="utf-8")
    (logs / f"{name}.stderr").write_text(p.stderr, encoding="utf-8")
    (logs / f"{name}.exit").write_text(str(p.returncode) + "\n", encoding="utf-8")
    return {"name": name, "command": cmd, "working_directory": str(Path(cwd).relative_to(cwd.parents[len(Path(cwd).parts)-1]) if False else Path(cwd).name), "exit_code": p.returncode, "ok": p.returncode == 0}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", choices=["quick", "full", "heavy"], default="quick")
    ap.add_argument("--workspace", type=Path, required=True)
    ap.add_argument("--jobs", type=int, default=1)
    a = ap.parse_args()
    ws = checked_external(a.workspace, ROOT)
    safe_rmtree(ws, ROOT)
    ws.mkdir(parents=True)
    copy = ws / "source_copy"
    shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", ".work", "__pycache__", ".pytest_cache"))
    logs = ws / "logs"; logs.mkdir()
    before = snapshot(ROOT)["tree_sha256"]
    env = os.environ.copy()
    env.update({"PYTHONDONTWRITEBYTECODE":"1", "PYTHONHASHSEED":"0", "LC_ALL":"C.UTF-8", "TZ":"UTC", "SOURCE_DATE_EPOCH":"1784419200", "OMP_NUM_THREADS":str(a.jobs), "NVSNVP_JOBS":str(a.jobs)})
    py = sys.executable
    res = []
    res.append(run("validate_tree", [py, "-B", "03_REPRODUCE/validate_tree.py"], copy, logs, env))
    res.append(run("manifest", [py, "-B", "03_REPRODUCE/verify_manifest.py"], copy, logs, env))
    res.append(run("security_scan", [py, "-B", "03_REPRODUCE/security_scan.py"], copy, logs, env))
    res.append(run("binary_format_tests", [py, "-B", "03_REPRODUCE/binary_format_tests.py"], copy, logs, env))
    res.append(run("status_linter", [py, "-B", "03_REPRODUCE/status_linter.py"], copy, logs, env))
    res.append(run("claims_linter", [py, "-B", "03_REPRODUCE/claims_linter.py"], copy, logs, env))
    res.append(run("compound_package", [py, "-B", "verify_package.py"], copy / "01_CANONICAL/compound_hessian_schur_fitting", logs, env))
    res.append(run("rank_reversal", [py, "-B", "scripts/verify_rank_reversal.py"], copy / "01_CANONICAL/padded_rank_reversal", logs, env))
    res.append(run("asymptotic", [py, "-B", "scripts/verify_asymptotic_obstruction.py"], copy / "01_CANONICAL/asymptotic_quotient_fitting", logs, env))
    res.append(run("jet_package", [py, "-B", "verify_package.py"], copy / "01_CANONICAL/jet_conormal_program", logs, env))
    res.append(run("reverse_quick", ["bash", "verify_all.sh"], copy / "01_CANONICAL/reverse_hessian", logs, env))
    if a.profile in {"full", "heavy"}:
        res.append(run("reverse_full", ["bash", "verify_all_full.sh"], copy / "01_CANONICAL/reverse_hessian", logs, env))
        compout = ws / "compound_full_results"
        res.append(run("compound_full", ["bash", "reproduce_all.sh", str(compout), str(a.jobs)], copy / "01_CANONICAL/compound_hessian_schur_fitting", logs, env))
        res.append(run("conormal_modular", [py, "-B", "scripts/conormal_graph_probe.py", "--out", str(ws / "conormal_graph_modular.json")], copy / "01_CANONICAL/jet_conormal_program", logs, env))
        res.append(run("reverse_extension_pdf_determinism", ["bash", "03_REPRODUCE/build_reverse_extension_pdf.sh", str(ws / "pdf_vp_vnp")], copy, logs, env))
        res.append(run("synthesis_pdf_determinism", ["bash", "03_REPRODUCE/build_synthesis_pdf.sh", str(ws / "pdf_synthesis")], copy, logs, env))
    blocked = []
    if a.profile == "heavy":
        sage_script = copy / "01_CANONICAL/reverse_hessian/extensions/vp_vnp/scripts/independent_catalecticant_check.sage"
        if shutil.which("sage") and sage_script.is_file():
            res.append(run("sage_catalecticant", ["sage", str(sage_script)], sage_script.parent, logs, env))
        else:
            blocked.append("Sage engine or unambiguous Sage script unavailable")
    after = snapshot(ROOT)["tree_sha256"]
    immutable = before == after
    obj = {
        "schema": "reverse_hessian.immutable_reproduction.v2.1",
        "profile": a.profile,
        "status": "PASS" if immutable and all(r["ok"] for r in res) else "FAIL",
        "source_tree_before": before,
        "source_tree_after": after,
        "source_tree_unchanged": immutable,
        "results": res,
        "blocked_not_executed": blocked,
        "jobs": a.jobs,
    }
    (ws / "ATTESTATION.json").write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(obj, ensure_ascii=False, indent=2))
    raise SystemExit(0 if obj["status"] == "PASS" else 1)

if __name__ == "__main__": main()
