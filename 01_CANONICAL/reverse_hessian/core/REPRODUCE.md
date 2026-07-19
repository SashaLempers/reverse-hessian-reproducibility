# Reproduction protocol

## Frozen environment

The checked-in certificates were generated with:

```text
Python 3.13.5
SymPy 1.14.0
pytest 9.0.2
PYTHONHASHSEED=0
```

Install and execute:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
./reproduce_all.sh
```

A Dockerfile and GitHub Actions workflow are included.

## Command graph

`./reproduce_all.sh` executes:

```bash
python3 run_all.py
python3 scripts/check_reproducibility.py
python3 -m pytest -q
(cd certificates && sha256sum -c SHA256SUMS.txt)
```

`run_all.py` launches the five independent mathematical reconstructions, then cross-checks and normalizes their outputs. The certificate files intentionally omit times, machines, absolute paths, and timestamps. Runtime diagnostics belong in `logs/` or `runtime_logs/` and are not part of certificate hashes.

## Meaning of certification

`CERTIFIED-COMP` means exact deterministic arithmetic that is reproducible from the supplied source and cross-checked by independent implementations where stated. It does **not** mean a proof checked by Lean, Coq, Isabelle, or another formal kernel.

## Expected mathematical outputs

```text
D_det catalecticants:
1, 9, 45, 165, 270, 270, 165, 45, 9, 1

D_per catalecticants:
1, 9, 45, 165, 414, 414, 165, 45, 9, 1

modular primes:
101, 1009, 32003, 65521

permanent-line root multiplicities, n=3,...,8:
1, 4, 9, 16, 25, 36

Dper3:
degree 9, 9 variables, 55 monomials, gcd(partials)=1
```
