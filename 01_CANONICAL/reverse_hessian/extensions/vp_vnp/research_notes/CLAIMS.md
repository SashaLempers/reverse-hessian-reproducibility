# CLAIMS

Status vocabulary: **PROVED**, **CERTIFIED-COMP**, **LITERATURE**, **CONJECTURAL**, **FAILED**, **UNKNOWN**. A claim may have more than one status when a paper proof is accompanied by finite verification.

| Claim | Status | Depends on | Proof location | Script/certificate | Literature source | Risk |
|---|---|---|---|---|---|---|
| Hessian covariance under linear substitution | PROVED | chain rule | paper, Lemma “Hessian covariance” | — | standard | low |
| `det Hess(det_n)=c_n det_n^{n(n-2)}` with the stated constant | PROVED; CERTIFIED-COMP for `2≤n≤8` | Jacobi formula; block determinant at identity | paper, exact determinant identity | `verify_uniform_formulas.py`; `uniform_formulas.json` | Fox (2016) for the relative-invariant context | low |
| Permanent Hessian line restriction on `J_n+(t-1)E_11` | PROVED; CERTIFIED-COMP for listed finite cases | complementary minors; Kronecker determinant | paper, exact line restriction | `verify_uniform_formulas.py`; `uniform_formulas.json` | no identical formula located in the searches; novelty UNKNOWN | medium |
| `D_per,n` is not an `n(n-2)`-th power | PROVED | line restriction and root multiplicity | paper | finite checks only supplementary | — | low |
| `D_det,n` and `D_per,n` are `SL_{n^2}`-polystable | PROVED using LITERATURE criterion | row-column torus, support cone | paper | — | Bürgisser–Ikenmeyer (2017), Prop. 2.8 | medium: referee may request a reformulation of the criterion |
| Uniform reverse-Hessian non-containment | PROVED | power obstruction, polystability, GL/SL closure lemma | paper, Reverse Hessian Obstruction | `uniform_formulas.json` is not the proof | no identical theorem located; absolute novelty UNKNOWN | medium; orientation is opposite to the GCT lower-bound direction |
| Exact ordinary catalecticant ranks in size 3 | CERTIFIED-COMP | exact rational sparse ranks | paper, Reproducible Certification | `certify_catalecticant_ranks.py`; `catalecticant_ranks.json` | — | low |
| Independent modular reconstruction gives the same ranks | CERTIFIED-COMP | clean-room exponent-dictionary engine | paper, Reproducible Certification | `independent_catalecticant_check.py`; JSON and log | — | low |
| Ordinary catalecticant rank loci cannot detect the reverse separation for `n=3` | PROVED + CERTIFIED-COMP | upper semicontinuity plus rank table | paper, Catalecticant Blindness | rank certificates | — | low |
| `D_per,3` is squarefree over `Q` and `C` | CERTIFIED-COMP | exact gcd of first partials | paper, certification appendix | `certify_squarefree_Dper3.py`; `squarefree_Dper3.json` | — | low |
| One-padding-variable factorization `det Hess(l^k g)` | PROVED; CERTIFIED-COMP in small examples | polynomial block determinant via the adjugate and Euler identity | paper, padding section | `transverse_hessian_experiments.py` | no claim of absolute novelty | low |
| Full ordinary Hessian determinant of standard padded permanent is zero for `m>n` | PROVED | existence of unused variables | paper, Padding-collapse theorem | unused-variable finite check | padded model in Mulmuley–Sohoni/Kadish–Landsberg | low |
| The ordinary full Hessian determinant alone yields a super-polynomial determinantal-complexity lower bound | FAILED | padding-collapse theorem | paper, Barrier theorem | — | GCT framework sources | decisive failure |
| Tested SPD ranks separate `D_det,3` from `D_per,3` in the needed direction | FAILED for `(1,1),(2,1),(1,2)` only | exact ranks | research note | `exploratory_flattenings.py`; certificate | shifted-partial literature | finite negative evidence only |
| A Young/Koszul flattening or multiplicity obstruction separates the Hessian orbit closures | UNKNOWN | uncomputed modules | research notes | no certificate | relevant flattening/multiplicity literature | high |
| Reverse Hessian non-containment implies padded-permanent non-containment | FAILED | covariance gives the opposite implication direction | paper, logical map and direction-mismatch warning | — | GCT model | decisive logical mismatch |
| This work proves `VP≠VNP` | FAILED / NOT CLAIMED | would require an unrestricted circuit lower bound absent here | paper, limitations | — | Valiant/GCT literature | prohibited overclaim |
| This work proves `VP_ws≠VNP` | FAILED / NOT CLAIMED | would require super-polynomial determinantal/border-determinantal complexity | paper, logical map | — | Bläser–Ikenmeyer (2025) | prohibited overclaim |
| Absolute novelty of every theorem | UNKNOWN | exhaustive human bibliography and peer review | literature audit | — | sources listed there | medium |
