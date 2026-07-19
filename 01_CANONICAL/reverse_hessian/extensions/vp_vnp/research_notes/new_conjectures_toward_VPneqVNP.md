# New conjectures toward VP versus VNP

These are research targets, not results. Neither is claimed equivalent to `VP≠VNP`.

## Conjecture 1 — Canonical active-space extraction

**Statement.** There exists a finite collection of regular equivariant incidence constructions on forms `F∈Sym^m(C^{m^2})^*` whose value determines, on the padded-permanent orbit, the minimal active subspace of `F` and the transverse Hessian determinant of the induced active form.

**Motivation.** The full Hessian vanishes only because of redundant ambient variables. On a marked active space, the one-padding-variable factorization retains `per_n·D_per,n`.

**Evidence.** The active-space formula is proved; the standard full-Hessian collapse is proved. No evidence is supplied for regular global extraction across orbit-closure boundaries.

**Verified cases.** Only fixed marked decompositions and small symbolic examples.

**Strategy.** Work on an incidence variety of pairs `(F,U)` where `F∈Sym^m U^*`, use Fitting ideals of first derivatives to encode `U`, and seek descent to a finite equivariant object.

**Obstacle.** Minimal active subspaces jump in degenerations; selecting one may be nonregular and nonunique.

**Consequence.** By itself, none. Combined with a uniform separation theorem for the resulting covariant on determinants versus padded permanents, it would give a GCT non-containment. That second statement remains independent.

**Plausibility.** medium-low.

## Conjecture 2 — Transverse Hessian multiplicity gap in the marked model

**Statement.** For a suitable parabolic marked-padding model, there is an explicit polynomially bounded family of partitions `λ(n,m)` whose multiplicity in the coordinate ring of the transverse-Hessian image of the padded permanent exceeds its multiplicity in the corresponding determinant image.

**Motivation.** Multiplicity gaps can be stronger than occurrence gaps, and the marked transverse Hessian avoids the zero-image barrier.

**Evidence.** None beyond the unpadded geometric separation and the exact padding factorization.

**Verified cases.** none.

**Strategy.** Start with `n=3`, decompose low-degree ideals of the paired image, and compare parabolic induction to ambient `GL` modules.

**Obstacles.** no candidate partition; no proof of scalability; no descent to the unmarked model.

**Consequence.** A separation in a natural restricted equivariant model. A consequence for VP versus VNP would require an additional reduction showing that small general circuits can be symmetrized/marked with polynomial overhead; no such reduction is known here.

**Plausibility.** low.
