
# Reproduction profiles — v2.1

Run all profiles from the repository root and place the workspace outside the sealed tree.

## Quick

```bash
python3 -B 03_REPRODUCE/verify_immutable.py --profile quick --workspace /tmp/reverse-hessian-quick --jobs 1
```

## Full

```bash
python3 -B 03_REPRODUCE/verify_immutable.py --profile full --workspace /tmp/reverse-hessian-full --jobs 1
```

## Heavy

```bash
python3 -B 03_REPRODUCE/verify_immutable.py --profile heavy --workspace /tmp/reverse-hessian-heavy --jobs 1
```

The verifier copies the source tree into an external mutable workspace, records stdout/stderr/exit code for each step, and verifies that the original source hash is unchanged. Optional external engines remain explicitly blocked when absent.
