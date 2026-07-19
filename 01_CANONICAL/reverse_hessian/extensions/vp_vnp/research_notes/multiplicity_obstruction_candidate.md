# Multiplicity obstruction candidate

## What is established

The no-occurrence results of Ikenmeyer–Panova and Bürgisser–Ikenmeyer–Panova prevent treating mere presence/absence of irreducibles as a general asymptotic solution of the standard GCT problem. Dörfler–Ikenmeyer–Panova show that multiplicity obstructions can nevertheless be strictly stronger than occurrence obstructions in natural Chow/secant-Veronese settings.

## Hessian-image coordinate rings

The relevant rings would be

`C[closure(GL·D_det,n)]` and `C[closure(GL·D_per,n)]`.

The present separation proof does not calculate either ring. It uses polystability and an orbit invariant (“being a high power”), not a certified highest-weight multiplicity gap.

## Candidate search protocol for `n=3`

1. Compute the stabilizers of the two Hessian forms exactly.
2. Use Peter–Weyl to bound multiplicities on the open orbits.
3. Compute low-degree ideals by evaluation/interpolation over several primes.
4. Decompose each ideal degree into `GL_9` highest-weight spaces.
5. Lift every candidate gap to characteristic zero by an exact rational certificate.
6. Distinguish a multiplicity gap from a mere occurrence gap.

## Candidate partitions

No partition `λ` is certified by the present computation. Reporting a guessed partition without a decomposed coordinate-ring calculation would violate the claim discipline. The candidate field is therefore explicitly **UNKNOWN**, not silently omitted.

## Asymptotic relevance

Even a genuine multiplicity gap for Hessian-image orbit closures would not automatically apply to padded permanent orbit closures, because the ordinary full Hessian image of the padded permanent is zero. An asymptotic candidate must first replace the covariant by an anti-padding construction.
