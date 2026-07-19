# Final verdict

## What survives

1. **PROVED:** a uniform reverse-Hessian orbit-closure separation in the equal-size, unpadded model, subject to the written polystability criterion and closure lemma. Its orientation is the reverse of the covariant non-containment needed for a padded GCT lower bound.
2. **CERTIFIED-COMP:** exact size-3 catalecticant ranks from a rational engine, independently reconstructed modulo three primes.
3. **CERTIFIED-COMP:** exact squarefreeness of `D_per,3` by a rational gcd.
4. **PROVED:** an exact one-padding-variable Hessian factorization.
5. **PROVED:** a padding-collapse barrier: the ordinary full Hessian determinant of the standard padded permanent is zero for every genuine padding `m>n`.

## What does not survive

- No proof of `VP≠VNP` or `VP_ws≠VNP`.
- No super-polynomial determinantal-complexity lower bound.
- No separation of standard padded orbit closures via the ordinary full Hessian determinant.
- No certified Young/Koszul or multiplicity obstruction.
- No claim of absolute novelty without external peer review.

## Research contribution

The package is strongest as a rigorous positive/negative pair: an explicit Hessian-image separation exists in the unpadded testbed, ordinary catalecticant and tested shifted-partial rank measures miss it, and the same full Hessian construction provably collapses in the standard padded GCT model. This identifies exactly why the current result does not cross the bridge to VP versus VNP and isolates the need for a canonical anti-padding covariant.

## Decisive logical diagnosis

For a regular equivariant covariant, original padded containment implies image containment. Therefore the useful target statement would place the padded-permanent image outside the determinant-image closure. The proved theorem instead places the determinant Hessian image outside the permanent Hessian-image closure. This direction mismatch already blocks the complexity inference in the unpadded model; the full-ambient padding collapse then annihilates the permanent-side image entirely.
