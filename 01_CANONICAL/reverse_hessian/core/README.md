# Reverse Hessian: audit-revised equal-size theorem

This repository is the major-revision response to the independent audit of the earlier `reverse_hessian_nxn_theorem` package.

## Mathematically proved in the paper

For every `n >= 3`, with `D(f) = det Hess(f)` on `M_n(C)`:

```text
D(det_n) not in closure(GL_{n^2} . D(per_n)),
D(per_n) not in closure(GL_{n^2} . D(det_n)).
```

The proof uses the exact identities

```text
D(det_n) = (n-1)(-1)^((n-1)(n+2)/2) det_n^(n(n-2)),
D(per_n)(J_n + (t-1)E_11) = K_n (t+n-3)^((n-2)^2),
K_n = ((n-2)!)^(n^2) (n-1)^(2n) / (n-2)^((n-2)^2).
```

The original equal-size determinant/permanent incomparability is retained only as a corollary and is **not claimed as new**. Published stabilizer and polystability results already imply it.

## Not proved

This repository does not prove a padded-permanent orbit-closure noncontainment, a determinantal-complexity lower bound, an asymptotic obstruction, or `VP != VNP`. The complete ambient Hessian determinant vanishes on the standard padded permanent when unused ambient variables are present.

## Computational reconstruction

Three distinct scripts independently reconstruct the size-three Hessian pair and catalecticants:

1. `scripts/primary_exact_catalecticants.py` — SymPy exact engine;
2. `scripts/independent_exact_catalecticants.py` — clean-room exponent dictionaries and independent polynomial determinant;
3. `scripts/independent_modular_catalecticants.py` — pure Python, no SymPy, with custom sparse elimination modulo `101, 1009, 32003, 65521`.

The three script SHA-256 values are different. The engines agree on polynomial hashes, direct integer matrix hashes for orders `0,...,4`, and the complete rank vectors.

## Reproduce

Environment used to create the checked-in certificates:

```text
Python 3.13.5
SymPy 1.14.0
pytest 9.0.2
```

Run:

```bash
./reproduce_all.sh
```

The command rebuilds all deterministic certificates, performs two fresh byte-for-byte rebuilds, runs the tests, and checks `certificates/SHA256SUMS.txt`.

See:

- `paper/a_uniform_line_formula_and_hessian_orbit_incomparability.pdf`
- `CLAIMS.md`
- `REPRODUCE.md`
- `SERIALIZATION_SPEC.md`
- `audit/AUDIT_RESPONSE.md`
