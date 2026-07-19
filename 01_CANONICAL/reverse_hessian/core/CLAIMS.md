# Claims table

| Claim | Status | Depends on | Proof location | Script / certificate | Literature | Risk |
|---|---|---|---|---|---|---|
| Hessian covariance | PROVED | Chain rule | Paper, Lemma 2.1 | none | classical | low |
| Relative-covariant transfer, including the zero-image case | PROVED | covariance, polynomial continuity, central scalars | Paper, Proposition 2.3 | none | none needed | low |
| `det Hess(det_n) = c_n det_n^(n(n-2))` | PROVED | Jacobi formula and determinant of the Hessian form at the identity | Paper, Theorem 3.1 | `uniform_formulas_n2_to_n8.json` is only a finite check | classical relative-invariant context; no priority claim | low |
| Permanent line formula with multiplicity `(n-2)^2` | PROVED | complementary minors, explicit spectrum of `A^{-1}C` | Paper, Theorem 3.2 | `uniform_formulas_n2_to_n8.json` checks `n=3,...,8` | exact priority UNKNOWN | medium: hidden antecedent possible |
| `D(per_n)` is not an `n(n-2)`-th power up to scalar | PROVED | line formula and root multiplicity | Paper, Corollary 3.3 | finite checks only | none needed | low |
| Closedness of the power cone | PROVED | projective Veronese image | Paper, Lemma 3.4 | none | standard | low |
| Polystability of both Hessian forms | PROVED using LITERATURE | Bürgisser-Ikenmeyer Proposition 2.8; explicit torus-character and support checks | Paper, Proposition 4.1 | none | Bürgisser-Ikenmeyer (2017) | medium: referee may request another GIT review |
| Hessian-image orbit closures are incomparable for every `n>=3` | PROVED | power cone, nonpower, polystability, closed-orbit lemma | Paper, Theorem 1.1 | none | priority UNKNOWN | medium: novelty not certified |
| Original equal-size determinant/permanent orbit closures are incomparable | LITERATURE + PROVED COROLLARY | transfer theorem; independently published stabilizers and polystability | Paper, Corollary 6.1 and following remark | none | Bürgisser-Ikenmeyer (2017), classical stabilizers | **not new** |
| Full ambient Hessian of the padded permanent vanishes for `m>n` | PROVED | unused variable gives a zero Hessian row/column | Paper, Proposition 7.1 | none | none needed | low |
| `D(per_3)` has 55 monomials and gcd of first partials equal to 1 | CERTIFIED-COMP | exact reconstruction over `Q` | Paper, Section 8 | `squarefree_Dper3.json` | none | low |
| `D(per_3)` is squarefree over `Q` and `C` | PROVED from CERTIFIED-COMP input | derivative-gcd criterion and field extension | Paper, Section 8 | `squarefree_Dper3.json` | standard algebra | low |
| SymPy factorization over `Q` returns one degree-9 factor | CERTIFIED-COMP | exact `factor_list` | Paper, Section 8 | `squarefree_Dper3.json` | none | no claim of absolute irreducibility |
| Catalecticant vectors are `(1,9,45,165,270,270,165,45,9,1)` and `(1,9,45,165,414,414,165,45,9,1)` | CERTIFIED-COMP | three distinct engines | Paper, Section 8 | three catalecticant JSON files and `cross_engine_consistency.json` | none | not a formal proof-assistant certificate |
| Ordinary catalecticant rank loci do not separate in the tested direction for `n=3` | PROVED + CERTIFIED-COMP | coordinatewise rank inequality | Paper, Section 8 | rank certificates | standard semicontinuity | limited to ordinary rank loci |
| Padded-permanent lower bound | FAILED for this ambient Hessian route | padding barrier | Paper, Section 7 | none | GCT context | no positive claim |
| `VP != VNP` | UNKNOWN | missing asymptotic reduction | Paper, Sections 1 and 7 | none | standard GCT literature | no claim |
| Bibliographic novelty of the line formula or Hessian theorem | UNKNOWN | specialist priority search required | Paper, abstract and Section 10 | none | finite search is insufficient | no novelty adjective authorized |
