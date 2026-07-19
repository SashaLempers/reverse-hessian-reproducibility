# Literature review and novelty audit

Search date: 16 July 2026. URLs are provided for reproducibility. This audit establishes context and contradictions; it cannot prove absolute novelty.

## Core VP/VNP and GCT

1. Leslie G. Valiant, “Completeness Classes in Algebra,” STOC 1979, pp. 249–261. DOI: `10.1145/800135.804419`. URL: https://doi.org/10.1145/800135.804419
2. Ketan D. Mulmuley and Milind Sohoni, “Geometric Complexity Theory I: An Approach to the P vs. NP and Related Problems,” *SIAM Journal on Computing* 31(2), 496–526 (2001). DOI: `10.1137/S009753970038715X`. URL: https://doi.org/10.1137/S009753970038715X
3. Ketan D. Mulmuley and Milind Sohoni, “Geometric Complexity Theory II: Towards Explicit Obstructions for Embeddings among Class Varieties,” *SIAM Journal on Computing* 38(3), 1175–1206 (2008). DOI: `10.1137/080718115`. URL: https://doi.org/10.1137/080718115
4. Peter Bürgisser, J. M. Landsberg, Laurent Manivel and Jerzy Weyman, “An Overview of Mathematical Issues Arising in the Geometric Complexity Theory Approach to VP ≠ VNP,” *SIAM Journal on Computing* 40(4), 1179–1209 (2011). DOI: `10.1137/090765328`. URL: https://doi.org/10.1137/090765328
5. Markus Bläser and Christian Ikenmeyer, “Introduction to Geometric Complexity Theory,” *Theory of Computing Graduate Surveys* (2025). URL: https://theoryofcomputing.org/articles/gs010/

## No-go and multiplicity results

6. Christian Ikenmeyer and Greta Panova, “Rectangular Kronecker Coefficients and Plethysms in Geometric Complexity Theory,” *Advances in Mathematics* 319, 40–66 (2017). DOI: `10.1016/j.aim.2017.08.024`. URL: https://doi.org/10.1016/j.aim.2017.08.024
7. Peter Bürgisser, Christian Ikenmeyer and Greta Panova, “No Occurrence Obstructions in Geometric Complexity Theory,” *Journal of the American Mathematical Society* 32(1), 163–193 (2019). DOI: `10.1090/jams/908`. URL: https://doi.org/10.1090/jams/908
8. Julian Dörfler, Christian Ikenmeyer and Greta Panova, “On Geometric Complexity Theory: Multiplicity Obstructions Are Stronger than Occurrence Obstructions,” *SIAM Journal on Applied Algebra and Geometry* 4(2) (2020), 354–376. DOI: `10.1137/19M1287638`. URL: https://doi.org/10.1137/19M1287638

**Consequence for this package.** A low-degree or finite occurrence observation cannot be advertised as a general GCT route. Any representation-theoretic continuation must compute multiplicities and must separately address the padding-collapse theorem.

## Orbit closures, fundamental invariants, polystability and boundaries

9. Peter Bürgisser and Christian Ikenmeyer, “Fundamental Invariants of Orbit Closures,” *Journal of Algebra* 477, 390–434 (2017). DOI: `10.1016/j.jalgebra.2016.12.035`. URL: https://doi.org/10.1016/j.jalgebra.2016.12.035
10. Shrawan Kumar, “Geometry of Orbits of Permanents and Determinants,” *Commentarii Mathematici Helvetici* 88(3), 759–788 (2013). DOI: `10.4171/CMH/302`. URL: https://doi.org/10.4171/CMH/302
11. Jesko Hüttenhain and Pierre Lairez, “The Boundary of the Orbit of the 3-by-3 Determinant Polynomial,” *Comptes Rendus Mathématique* 354(9), 931–935 (2016). DOI: `10.1016/j.crma.2016.07.002`. URL: https://doi.org/10.1016/j.crma.2016.07.002
12. Harlan Kadish and J. M. Landsberg, “Padded Polynomials, Their Cousins, and Geometric Complexity Theory,” *Communications in Algebra* 42(5), 2171–2180 (2014). URL: https://arxiv.org/abs/1204.4693

**Correction forced by the literature.** The equal-size determinant and permanent are already polystable objects with different stabilizers; the manuscript must not present their reverse containment as the central unresolved Valiant problem. Kumar also proves nonnormality phenomena for determinant and padded-permanent orbit closures, so normality cannot be silently assumed.

## Hessians and flattenings

13. Daniel J. F. Fox, “Functions Dividing Their Hessian Determinants and Affine Spheres,” *Asian Journal of Mathematics* 20(3), 503–530 (2016). DOI: `10.4310/AJM.2016.v20.n3.a5`. URL: https://doi.org/10.4310/AJM.2016.v20.n3.a5
14. J. M. Landsberg and Giorgio Ottaviani, “Equations for Secant Varieties of Veronese and Other Varieties,” *Annali di Matematica Pura ed Applicata* 192, 569–606 (2013). DOI: `10.1007/s10231-011-0238-6`. URL: https://doi.org/10.1007/s10231-011-0238-6
15. Yang Qi Guan, “Flattenings and Koszul Young Flattenings Arising in Complexity Theory,” *Communications in Algebra* 45(9), 4002–4017 (2017). DOI: `10.1080/00927872.2016.1253706`. URL: https://doi.org/10.1080/00927872.2016.1253706
16. Klim Efremenko, J. M. Landsberg, Hal Schenck and Jerzy Weyman, “The Method of Shifted Partial Derivatives Cannot Separate the Permanent from the Determinant,” arXiv:1609.02103 (2016). DOI: `10.48550/arXiv.1609.02103`. URL: https://arxiv.org/abs/1609.02103

**Known shifted-partial barrier.** Efremenko–Landsberg–Schenck–Weyman prove that the shifted-partial-derivative method alone cannot exclude the padded permanent `ℓ^{n-m}per_m` from the `GL_{n^2}` determinant orbit closure once `n>2m^2+2m`. The three small SPD computations in this package are only finite confirmations in a different Hessian-image comparison and are not presented as a new general barrier.


## Algebraic natural proofs and restricted lower bounds

17. Joshua A. Grochow, Mrinal Kumar, Michael Saks and Shubhangi Saraf, “Towards an Algebraic Natural Proofs Barrier via Polynomial Identity Testing,” arXiv:1701.01717 (2017). URL: https://arxiv.org/abs/1701.01717
18. Anuj Dawar and Gregory Wilsenach, “Symmetric Arithmetic Circuits,” *Theory of Computing* 21(14) (2025). DOI: `10.4086/toc.2025.v021a014`. URL: https://doi.org/10.4086/toc.2025.v021a014
19. Anuj Dawar, Benedikt Pago and Tim Seppelt, “Symmetric Algebraic Circuits and Homomorphism Polynomials,” ITCS 2026, LIPIcs 362, Article 46. DOI: `10.4230/LIPIcs.ITCS.2026.46`. URL: https://doi.org/10.4230/LIPIcs.ITCS.2026.46
20. Prateek Dwivedi, Benedikt Pago and Tim Seppelt, “Lower Bounds in Algebraic Complexity via Symmetry and Homomorphism Polynomials,” arXiv:2601.09343 (2026). URL: https://arxiv.org/abs/2601.09343
21. Michael A. Forbes, “Low-Depth Algebraic Circuit Lower Bounds over Any Field,” CCC 2024, LIPIcs 300, Article 31. URL: https://doi.org/10.4230/LIPIcs.CCC.2024.31

**Relevance.** Unconditional permanent lower bounds are known in natural symmetric or low-depth models, not for unrestricted VP. A future Hessian-based restricted-model theorem should be compared to these precise models rather than described as a general VP/VNP result.

## Coverage of the mandatory search axes

| Axis | Sources checked | Audit conclusion |
|---|---|---|
| VP vs VNP; Valiant permanent vs determinant | Valiant (1979); BLMW (2011); Bläser–Ikenmeyer (2025) | The unrestricted VP/VNP problem must not be conflated with weakly-skew/determinantal complexity. |
| GCT I/II and padded orbit closures | Mulmuley–Sohoni (2001, 2008); Kadish–Landsberg (2014) | The standard target uses `ell^(m-n) per_n` in `m^2` variables. |
| Occurrence no-go results | Ikenmeyer–Panova (2017); Bürgisser–Ikenmeyer–Panova (2019); Gesmundo–Ikenmeyer–Panova (2017) | Broad occurrence strategies do not yield the required asymptotic lower bounds, including in a padding-free matrix-powering reformulation. |
| Multiplicity obstructions | Dörfler–Ikenmeyer–Panova (2020); Ikenmeyer–Kandasamy (2020) | Multiplicities can be stronger in other orbit-closure comparisons, but no candidate partition is certified here. |
| Fundamental invariants and polystability | Bürgisser–Ikenmeyer (2017) | Used for the support-cone/polystability framework; it does not create the missing asymptotic reduction. |
| Determinant/permanent orbit geometry and boundary | Kumar (2013); Hüttenhain–Lairez (2016) | Nonnormality and the explicit `3x3` boundary constrain overclaims about closures. |
| Hessian determinants | Fox (2016) plus searches on Hessian covariants in GCT | No source found with the exact four-result combination in this package; novelty remains UNKNOWN. |
| Catalecticants, Young/Koszul flattenings | Landsberg–Ottaviani (2013); Guan (2017) | Ordinary rank flattenings are certified blind here; Young/Koszul alternatives remain uncomputed. |
| Shifted partial derivatives | Efremenko–Landsberg–Schenck–Weyman (2016) | Known asymptotic padding barrier is distinct from the finite Hessian-image computations here. |
| Algebraic natural proofs | Grochow–Kumar–Saks–Saraf (2017) | Any proposed efficiently recognisable property must be tested against largeness/usefulness barriers. |
| Chow, secant and Veronese varieties | Landsberg–Ottaviani (2013); Dörfler–Ikenmeyer–Panova (2020) | These provide the closest successful multiplicity/flattening comparison settings, not a permanent lower bound. |
| Symmetric circuits, homomorphism polynomials, immanants (2025–2026) | Dawar–Wilsenach (2025); Dawar–Pago–Seppelt (2026); Dwivedi–Pago–Seppelt (2026) | Strong unconditional lower bounds and immanant classifications exist in symmetric restricted models, not unrestricted VP. |
| Recent low-depth lower bounds | Forbes (2024) and the cited constant-depth literature | These are restricted-model results and do not validate an unrestricted Hessian claim. |

Additional checked sources:

22. Fulvio Gesmundo, Christian Ikenmeyer and Greta Panova, “Geometric Complexity Theory and Matrix Powering,” *Differential Geometry and its Applications* 55, 106–127 (2017). DOI: `10.1016/j.difgeo.2017.07.001`. URL: https://doi.org/10.1016/j.difgeo.2017.07.001
23. Peter Bürgisser, Christian Ikenmeyer and Jesko Hüttenhain, “Permanent versus Determinant: Not via Saturations,” *Proceedings of the American Mathematical Society* 145(3), 1247–1258 (2017). DOI: `10.1090/proc/13310`. URL: https://doi.org/10.1090/proc/13310
24. Christian Ikenmeyer and Umangathan Kandasamy, “Implementing Geometric Complexity Theory: On the Separation of Orbit Closures via Symmetries,” STOC 2020; arXiv:1911.03990. URL: https://arxiv.org/abs/1911.03990
25. Fulvio Gesmundo and J. M. Landsberg, “Explicit Polynomial Sequences with Maximal Spaces of Partial Derivatives and a Question of K. Mulmuley,” arXiv:1705.03866 (2017). URL: https://arxiv.org/abs/1705.03866
26. Anuj Dawar, Benedikt Pago and Tim Seppelt, “Symmetric Algebraic Circuits and Homomorphism Polynomials,” arXiv:2502.06740 (2025), ITCS 2026. The paper explicitly studies immanant families in the symmetric model. DOI: `10.4230/LIPIcs.ITCS.2026.46`. URL: https://doi.org/10.4230/LIPIcs.ITCS.2026.46

## Novelty verdict

No searched source states the exact combination of the permanent line restriction, the reverse-Hessian non-containment, catalecticant blindness, and the padding-collapse theorem. This is not proof of novelty. The status remains **UNKNOWN** pending specialist review and broader database searches.
