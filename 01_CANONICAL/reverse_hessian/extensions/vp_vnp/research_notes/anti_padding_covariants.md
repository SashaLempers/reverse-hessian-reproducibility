# Anti-padding covariants

## Problem exposed by the audit

Padding creates two distinct difficulties:

1. the factor `l^{m-n}` introduces a highly singular hyperplane;
2. embedding into `m^2` variables introduces unused directions, forcing the full Hessian determinant to vanish.

The second obstruction is fatal to the ordinary full Hessian determinant even before one analyzes the singularity along `l=0`.

## Candidate constructions

| construction | definition status | GL-equivariance | survives unused variables? | present status |
|---|---|---:|---:|---|
| active-space Hessian | Hessian on the span of variables actually occurring in `F` | not regular globally; active span jumps | yes on a fixed stratum | CONJECTURAL tool |
| paired transverse Hessian | for a pair `(F,[l])`, dehomogenize/divide by known padding and Hessianize on `V/⟨l⟩` | equivariant for the parabolic stabilizing the pair | yes | formally definable, consequence not proved |
| logarithmic Hessian | Hessian of `log F` on `F≠0` | rational, not polynomial | potentially | UNKNOWN |
| maximal nonzero Hessian minor module | all minors of size equal to active dimension | polynomial family, but size must be selected | yes | promising, untested asymptotically |
| polar/Jacobian incidence scheme | retain the image and degeneracy scheme of the polar map | intrinsic | yes | UNKNOWN |
| apolar multiplication/Koszul maps | use the apolar algebra rather than full ambient Hessian | equivariant | often | small cases not completed |

## Exact paired formula

When the padding direction and active quotient are part of the input, the one-variable factorization gives a canonical trace of `g det Hess(g)` up to a power of `l`. This is a theorem about pairs, not a GL-invariant of an unmarked polynomial. The missing step is to recover the padding line and the active quotient by a regular equivariant construction on an orbit closure.

## Proposed restricted-model theorem target

Let `P` be the parabolic subgroup preserving a line `L⊂V`. On the variety of pairs `(F,L)` with `F∈L^k Sym^d(V/L)^*`, define the transverse Hessian section by the determinant of the quotient Hessian after removing the known factor `L^k`. It is plausible that this section separates paired padded permanents from a suitable paired determinant model. This would be a restricted equivariant-circuit result, not VP versus VNP.

## Current verdict

No polynomial GL-covariant `C_{n,m}` satisfying the central requirement has been proved. The paired/transverse construction is the most concrete continuation, but its descent from marked pairs to ordinary forms is **UNKNOWN**.
