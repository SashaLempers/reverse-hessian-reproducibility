# Reverse Hessian — asymptotic quotient-Fitting obstruction

This package turns the fixed comparison `det_4` versus `z*per_3` into the
uniform family

`det_n` versus `ell^(n-m) per_m`, for `m>=3`, `n>=m`.

Main statement:

- the critical Hessian-minor order is `r=2n+1`;
- the augmented quotient-Fitting rank is larger by exactly one on the padded
  permanent iff `2n<m^2`;
- therefore the border determinantal complexity is at least `ceil(m^2/2)`;
- the same invariant provably stops separating at and beyond `2n=m^2`.

The asymptotic lower bound is known (Landsberg--Manivel--Ressayre, following
Mignon--Ressayre). This package makes no novelty claim. It provides a direct
reconstruction in the rank-augmented language developed in the preceding
experiments.

Run:

```bash
python3 scripts/verify_asymptotic_obstruction.py
```

Read `report/theoreme_asymptotique.md` for the symbolic proof.
