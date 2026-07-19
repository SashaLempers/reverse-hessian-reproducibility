# Merge report

## Sources

The combined package was built from exactly these input archives:

```text
SHA-256 8a165b082742b4ad04cdb9a7097cdcb400052179b9f9492e72da05aaa8dcb67f
reverse_hessian_nxn_audit_revised_full(1).zip

SHA-256 285d31817abaedd0fb61d0c62f3cd099ceaf3d278283860255e1109f2bb018e1
reverse_hessian_VP_VNP_upgrade(2)(1).zip
```

Exact member listings are stored under `provenance/source_trees/`.

## Strategy

The packages were not flattened into one namespace because fourteen public-repository paths overlap and differ, including `README.md`, `CLAIMS.md`, the workflow, the main runner, uniform-formula scripts, the squarefreeness script, and certificate manifests.

Flattening would silently overwrite evidence. The merge therefore uses two modules:

- `core/`: byte-preserving copy of the audit-revised public repository;
- `extensions/vp_vnp/`: byte-preserving copy of the upgrade public repository, augmented with its `research_notes/` directory.

## Conflict resolution

| Conflict | Decision |
|---|---|
| Mathematical claims shared by both packages | The audit-revised core is canonical. |
| Equal-size orbit result | Preserve the core's stronger two-way incomparability theorem. |
| Squarefree certificate | Preserve both, but treat the core v3 certificate as authoritative. |
| Catalecticant computation | Preserve both; the core's three distinct engines are authoritative for overlapping ranks. |
| Padding and transverse experiments | Preserve in the extension because they are additional material. |
| Main papers | Preserve separately; no automatic textual splice was attempted. |
| License | Use the complete MIT text at the combined root; module-local files are untouched. |
| Workflows and runners | Add combined wrappers; do not overwrite either module's original runner. |
| Runtime caches | Exclude `__pycache__`, `.pytest_cache`, `*.pyc`, and `*.pyo`. |
| Forensic archives | Excluded from the clean bundle to avoid nested duplication; included byte-for-byte in the full-forensic bundle as the two original ZIPs. |

## Verification performed during merge

The following checks completed successfully on the source modules:

- core certificate regeneration;
- core two-fresh-build byte-for-byte reproducibility check;
- core `pytest`: 3 tests passed;
- core certificate SHA-256 verification;
- extension certificate regeneration and internal cross-check;
- extension `unittest`: 5 tests passed;
- extension certificate SHA-256 verification.

The extension's isolated full reproducibility checker is intentionally available through `verify_all_full.sh`; it is much slower than the standard checks.

## Mutable files

Runtime logs are retained inside the modules when present, but they are excluded from the combined SHA-256 manifest because verification commands regenerate them. Deterministic source files, papers, tests, and certificates are covered by `SHA256SUMS.txt`.
