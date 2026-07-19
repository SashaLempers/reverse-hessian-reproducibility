
# Reverse-Hessian Reproducibility

[![Verify](https://github.com/SashaLempers/reverse-hessian-reproducibility/actions/workflows/verify.yml/badge.svg)](https://github.com/SashaLempers/reverse-hessian-reproducibility/actions/workflows/verify.yml)

This repository contains the canonical sources, deterministic certificates, tests, and manuscripts for the Reverse-Hessian research program and its VP/VNP-oriented barrier analysis.

## Mandatory non-claims

- This repository does **not** prove `VP != VNP`.
- It does **not** establish a super-polynomial determinantal-complexity lower bound.
- The reconstructed quadratic bound is known in the literature and is not claimed as new.
- Finite computations do not replace general proofs.
- Modular computations are lower bounds over `Q` unless a rational certificate is explicitly provided.
- Reproducibility of a certificate does not by itself establish novelty or peer-reviewed mathematical correctness.

## Active scientific scope

The active registry contains **27 scientific claims** and **138 documented claim occurrences** across five modules:

1. equal-size Reverse-Hessian core;
2. compound Hessian / Schur / Fitting experiments;
3. padded rank reversal;
4. asymptotic quotient-Fitting reconstruction;
5. jet-conormal program.

The Prime multiplicative-walk project has been separated into the standalone repository `SashaLempers/multiplicative-walk-mod-n`.

## Papers

- Core: [`01_CANONICAL/reverse_hessian/core/paper/a_uniform_line_formula_and_hessian_orbit_incomparability.tex`](01_CANONICAL/reverse_hessian/core/paper/a_uniform_line_formula_and_hessian_orbit_incomparability.tex)
- VP/VNP barrier extension: [`01_CANONICAL/reverse_hessian/extensions/vp_vnp/paper/reverse_hessian_VP_VNP_upgrade.tex`](01_CANONICAL/reverse_hessian/extensions/vp_vnp/paper/reverse_hessian_VP_VNP_upgrade.tex)
- Status synthesis: [`01_CANONICAL/synthesis_report/reverse_hessian_status_synthesis.tex`](01_CANONICAL/synthesis_report/reverse_hessian_status_synthesis.tex)

Generated PDFs are convenient release artifacts. The `.tex` sources and exact certificates are canonical.

## Quick verification

Requirements: Python 3.13, SymPy 1.14, a C++17 compiler, GMP development libraries, and Bash.

```bash
python3 -m pip install -r requirements.txt
python3 -B 03_REPRODUCE/verify_immutable.py \
  --profile quick \
  --workspace /tmp/reverse-hessian-quick \
  --jobs 1
```

A successful run reports `PASS` and `source_tree_unchanged: true`.

## Reproducibility levels

- **Quick:** integrity, linters, lightweight module checks, and the combined Reverse-Hessian verifier.
- **Full:** fresh package regeneration, conormal modular probe, and deterministic PDF builds.
- **Heavy:** optional Sage checks when the engine is installed; absence remains explicitly blocked, never silently converted into PASS.

See [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) and [`03_REPRODUCE/README.md`](03_REPRODUCE/README.md).

## Historical and heavy assets

Forensic archives, old mixed claim registries, the initial audit, large witnesses, and runtime logs are release or Zenodo assets, not active branch content. See [`docs/RELEASE_ASSETS.md`](docs/RELEASE_ASSETS.md).

## Citation and license

Use [`CITATION.cff`](CITATION.cff) and cite the exact release tag. Code and repository documentation are available under the MIT License unless an individual manuscript states otherwise.

## Feedback

Please open a GitHub issue with the release tag, command, environment, and certificate hash involved.
