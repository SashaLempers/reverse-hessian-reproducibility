# Reverse Hessian: combined audited core and VP/VNP extension

This repository combines two source packages without mixing their evidentiary status:

1. `core/` is the audit-revised, reproducible equal-size theorem package. It is the **canonical source** for all overlapping exact formulas, orbit-closure claims, size-three certificates, and reproducibility procedures.
2. `extensions/vp_vnp/` preserves the later padding, transverse-Hessian, shifted-partial/flattening, and multiplicity-obstruction investigations. Its positive theorems and finite computations remain useful, while its programmatic directions remain explicitly exploratory.

The merge is modular on purpose. No exploratory result is promoted to a theorem by being placed beside the audited core, and the two manuscripts are retained separately rather than mechanically spliced into a misleading single paper.

## Canonical mathematical content

For every `n >= 3`, with `D(f) = det Hess(f)` on `M_n(C)`, the core proves

```text
D(det_n) not in closure(GL_{n^2} . D(per_n)),
D(per_n) not in closure(GL_{n^2} . D(det_n)).
```

It also proves the exact determinant and permanent line formulas, certifies the complete size-three catalecticant data with three distinct engines, and records the failure of the full ambient Hessian determinant after genuine padding.

The extension adds, among other items:

- the one-active-padding-variable Hessian factorization;
- exact transverse-Hessian experiments;
- finite shifted-partial/flattening tests;
- explicit anti-padding and multiplicity-obstruction research programs;
- documented failed directions and scope limitations.

## What is not proved

This combined repository does **not** prove:

- padded-permanent orbit-closure noncontainment in the standard GCT model;
- a super-polynomial determinantal-complexity lower bound;
- an asymptotic representation-theoretic obstruction;
- `VP != VNP` or `VP_ws != VNP`.

See `CLAIMS.md`, `core/CLAIMS.md`, and `extensions/vp_vnp/CLAIMS.md`.

## Verification

The checked-in environment is:

```text
Python 3.13.5
SymPy 1.14.0
pytest 9.0.2
PYTHONHASHSEED=0
```

Install the frozen dependencies, then choose the desired verification level:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

./verify_all.sh       # fast: tests, internal hashes, combined manifest
./rebuild_all.sh      # regenerate both deterministic certificate sets
./verify_all_full.sh  # slow: also perform both isolated byte-for-byte rebuilds
```

## Layout

- `core/` — exact audit-revised public repository and primary paper.
- `extensions/vp_vnp/` — VP/VNP-oriented extension, second paper, experiments, and research notes.
- `provenance/` — source archive hashes, exact member lists, and selected wrapper-level audit documents.
- `tools/` — combined-package integrity checker.
- `MERGE_REPORT.md` — conflict-resolution and precedence rules.

## Source archive identities

```text
8a165b082742b4ad04cdb9a7097cdcb400052179b9f9492e72da05aaa8dcb67f  reverse_hessian_nxn_audit_revised_full(1).zip
285d31817abaedd0fb61d0c62f3cd099ceaf3d278283860255e1109f2bb018e1  reverse_hessian_VP_VNP_upgrade(2)(1).zip
```

The separately distributed full-forensic bundle also contains byte-identical copies of both source ZIP files.
