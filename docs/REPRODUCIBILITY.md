
# Reproducibility

## Quick

```bash
python3 -B 03_REPRODUCE/verify_immutable.py \
  --profile quick --workspace /tmp/reverse-hessian-quick --jobs 1
```

Runs tree validation, manifest verification, security and format checks, status and claims linters, four lightweight module verifiers, and the combined Reverse-Hessian verifier.

## Full

```bash
python3 -B 03_REPRODUCE/verify_immutable.py \
  --profile full --workspace /tmp/reverse-hessian-full --jobs 1
```

Adds fresh Reverse-Hessian and compound regeneration, the modular conormal probe, and deterministic builds of the VP/VNP and synthesis PDFs.

## Heavy

The heavy profile also attempts the Sage catalecticant check. Missing external engines are explicitly recorded under `blocked_not_executed`.

All workspaces must be outside the sealed source tree. The verifier compares the source-tree hash before and after execution.
