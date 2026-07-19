# Axis A — From Hessian separation to lower bounds

## Status summary

- Uniform unpadded reverse-Hessian separation: **PROVED** in the manuscript.
- Compatibility with invertible substitutions: **PROVED** by Hessian covariance.
- Compatibility with arbitrary projections: **FAILED** in the form needed for a functorial orbit invariant; the Hessian of a restriction is a compressed Hessian, not the restriction of the full Hessian determinant.
- Passage through degenerations: the polynomial map `F↦det Hess(F)` is regular, so images of convergent families converge; however the GL covariance has a determinant twist and the converse implication is absent.
- Standard padded permanent: **PROVED** full-Hessian collapse to zero for `m>n`.
- Direction of the proved non-containment: **FAILED for the lower-bound purpose**; it is reverse to the implication furnished by covariant functoriality.
- Asymptotic determinant lower bound from this covariant alone: **FAILED**.

## Lemma A.1 — covariance

For `(g·F)(x)=F(g^{-1}x)`, `D(g·F)=det(g)^{-2}g·D(F)`. Thus original orbit containment implies a corresponding containment after applying the twisted covariant. The reverse implication is not valid in general because a covariant can identify distinct points or vanish.

## Lemma A.2 — one padding variable

For homogeneous `g(x_1,…,x_N)` of degree `d>1` and `k≥1`,

`det Hess_{(l,x)}(l^k g) = -k(k+d-1)/(d-1) · l^{k(N+1)-2} · g · det Hess_x(g)`.

The paper gives a complete polynomial block-determinant proof using the adjugate, with no Hessian-invertibility assumption. This shows that padding does not destroy all Hessian information if the ambient space is restricted to exactly the active variables `(l,x)`.

## The decisive counterexample in the standard GCT ambient space

The standard padded permanent `l^{m-n} per_n` is regarded as a degree-`m` form in `m^2` variables. For `m>n`, it depends on at most `n^2+1<m^2` variables. Every second derivative involving an unused variable is zero; the full Hessian has a zero row and column, hence determinant zero. Therefore its full Hessian image is the zero form.

Since the zero form belongs to the closure of every positive-degree homogeneous GL orbit, no nonzero Hessian-image condition can exclude the padded permanent from a determinant orbit closure. This is an exact barrier for the ordinary full Hessian determinant, not for all differential covariants.

## Small computations

`transverse_hessian_experiments.py` verifies the active-variable formula on three exact examples and verifies the unused-variable collapse on a five-variable example. These checks are **CERTIFIED-COMP** but are not the proof.

## Conclusion

The strongest honest advance on Axis A is a barrier theorem: the full ordinary Hessian determinant cannot by itself be the asymptotic bridge to VP versus VNP in the standard padded model. Any viable continuation must either make the active subspace canonical or use a differential construction that survives redundant ambient variables.

## Direction lemma

Let `C` be a regular equivariant covariant. If `F` lies in the orbit closure of `G`, then `C(F)` lies in the orbit closure of `C(G)` (with the prescribed target action/character). Hence a lower-bound certificate against the determinant must have the form `C(padded permanent) notin closure(GL·C(det_m))`. The established theorem has the reverse form `C(det_n) notin closure(GL·C(per_n))`; it cannot be contraposed into the desired statement.
