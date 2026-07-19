# Execution report

Date: 16 July 2026.

## Archive integrity and safety

- Supplied SHA-256: `edd1434a10f6cb11c33b2a306b2286b27f61a91b71d79062f1d8d282e99792ee`.
- Computed SHA-256: identical.
- ZIP entries checked: 243.
- Unsafe absolute paths, traversal paths, or symbolic links: none found.
- Extracted source files inventoried: 202.

## Reproduction

The following commands completed successfully in the upgraded package and in the clean public-repository copy:

```bash
python run_all.py
python scripts/check_reproducibility.py
python -m unittest discover -s tests -v
sha256sum -c certificates/SHA256SUMS.txt
```

Results:

- two consecutive root builds produced identical JSON certificate hashes;
- isolated rebuild: `BIT-FOR-BIT REPRODUCIBLE: 8 certificate files`;
- unit tests: 5/5 passed;
- all entries in `certificates/SHA256SUMS.txt`: OK;
- independent exact/modular catalecticant engines agreed at every order and prime;
- exact derivative gcd certificate returned `1` over `Q` for `D_per,3`.

## Mathematical verdict

- **PROVED:** uniform reverse-Hessian non-containment in the equal-size unpadded model.
- **CERTIFIED-COMP:** size-3 catalecticant rank vectors and squarefreeness.
- **PROVED:** full-ambient Hessian collapse for the genuinely padded permanent.
- **FAILED as a VP/VNP bridge:** the proved non-containment has the reverse orientation from the GCT lower-bound target, and the full Hessian annihilates the padded permanent.
- **UNKNOWN:** a canonical anti-padding covariant, Young/Koszul separation, or asymptotic multiplicity gap.
- **NOT CLAIMED:** `VP != VNP` or `VP_ws != VNP`.
