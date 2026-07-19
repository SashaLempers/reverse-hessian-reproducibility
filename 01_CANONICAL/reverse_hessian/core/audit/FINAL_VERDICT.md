# Final audit-revised verdict

## PROVED

- Hessian covariance and the zero-safe transfer principle.
- The uniform determinant Hessian identity.
- The permanent test-line formula for every `n>=3`, with the spectrum of `A^{-1}C` proved explicitly.
- The nonpower property.
- Polystability of both Hessian forms after a complete verification of the published support-cone criterion.
- Both noncontainments between the equal-size Hessian-image orbit closures.
- The padding barrier for the complete ambient Hessian determinant.

## LITERATURE

The equal-size incomparability of the original determinant and permanent is already an immediate inference from published stabilizer descriptions and polystability. It is not a novelty claim in this revision.

## CERTIFIED-COMP

Three scripts with distinct hashes reproduce the size-three polynomial hashes and catalecticant matrices. Two exact engines and a pure-Python modular engine agree on all ranks. Exact computation also gives 55 monomials for `Dper3`, one degree-9 factor over `Q` with multiplicity one, and gcd of all partial derivatives equal to 1.

## FAILED

The complete ambient Hessian determinant cannot transfer the theorem to the standard padded permanent: it vanishes because of unused ambient variables.

## UNKNOWN

- Bibliographic priority of the exact permanent line formula.
- Bibliographic priority of the Hessian-orbit incomparability formulation.
- A padding-resistant covariant yielding an asymptotic lower bound.
- `VP != VNP`.
