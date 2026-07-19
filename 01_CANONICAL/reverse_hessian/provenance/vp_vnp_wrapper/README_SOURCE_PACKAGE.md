# Reverse Hessian VP/VNP upgrade

This package audits and upgrades the supplied reverse-Hessian archive. It contains a paper, exact scripts, deterministic certificates, tests, a public-repository projection, and a byte-preserving forensic copy of the original ZIP.

## Main mathematical status

- **PROVED:** uniform reverse-Hessian separation in the equal-size unpadded model, in the reverse orientation from the GCT lower-bound target.
- **CERTIFIED-COMP:** complete `n=3` ordinary catalecticant ranks, independent modular reconstruction, and squarefreeness of `D_per,3`.
- **PROVED:** the full ordinary Hessian determinant vanishes on the standard genuinely padded permanent; therefore this covariant alone does not yield the standard GCT lower bound.
- **UNKNOWN:** any asymptotic anti-padding multiplicity obstruction.
- This package does **not** prove `VP≠VNP`.

## Reproduce

```bash
python -m pip install -r requirements.txt
python run_all.py
python scripts/check_reproducibility.py
python -m unittest discover -s tests -v
```

The first command rebuilds all deterministic certificates. Runtime metadata is written only to `runtime_logs/`. The second command rebuilds in an isolated temporary directory and checks byte-for-byte equality.

## Layout

- `paper/`: LaTeX source, bibliography and compiled PDF.
- `scripts/`: active deterministic and exploratory scripts.
- `certificates/`: machine-readable outputs and SHA-256 manifest.
- `research_notes/`: archive audit, literature audit, axes A–E, failures and verdict.
- `public_repo/`: clean release projection.
- `forensic_archive/`: original ZIP and provenance files.
