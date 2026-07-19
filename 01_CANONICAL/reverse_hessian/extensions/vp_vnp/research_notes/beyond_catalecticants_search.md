# Beyond ordinary catalecticants

The exact target is the reverse direction `D_det,3 ∉ closure(GL·D_per,3)`. For a rank-type equivariant map, separation requires the determinant-side rank to be strictly larger than the permanent-side rank. Ordinary catalecticants have the opposite inequality.

| test | separates? | degree/order | exact rank det | exact rank per | proof/cert | cost | scalable? |
|---|---:|---|---:|---:|---|---|---|
| ordinary catalecticant `C_0` | no | 0 | 1 | 1 | CERTIFIED-COMP | low | yes |
| `C_1` | no | 1 | 9 | 9 | CERTIFIED-COMP | low | yes |
| `C_2` | no | 2 | 45 | 45 | CERTIFIED-COMP | low | moderate |
| `C_3` | no | 3 | 165 | 165 | CERTIFIED-COMP | moderate | limited |
| `C_4` | no; wrong direction | 4 | 270 | 414 | CERTIFIED-COMP | moderate | limited |
| `C_5` | no; wrong direction | 5 | 270 | 414 | dual certificate | moderate | limited |
| `C_6,…,C_9` | no | dual orders | 165,45,9,1 | 165,45,9,1 | CERTIFIED-COMP | moderate | limited |
| SPD `(k,l)=(1,1)` | no; wrong direction | 1,1 | 65 | 77 | `exploratory_flattenings.json` | moderate | poor |
| SPD `(2,1)` | no; wrong direction | 2,1 | 270 | 369 | same | high | poor |
| SPD `(1,2)` | no; wrong direction | 1,2 | 270 | 369 | same | high | poor |
| Young flattenings | UNKNOWN | uncomputed | — | — | no certificate | high | representation-dependent |
| Koszul flattenings | UNKNOWN | uncomputed | — | — | no certificate | high | representation-dependent |
| apolar multiplication maps beyond graded dimensions | UNKNOWN | uncomputed | — | — | no certificate | high | uncertain |
| syzygies of Hessian hypersurfaces | UNKNOWN | uncomputed | — | — | no certificate | very high | uncertain |
| singular-locus invariants | UNKNOWN | partial squarefree datum only | — | — | squarefree certificate | high | potentially |

## Interpretation

The three shifted-partial tests are finite experiments only. Their ranks again favor `D_per,3`, so the corresponding upper-semicontinuous rank loci cannot prove the reverse non-containment. This does not constitute a new general limitation theorem for shifted partial derivatives. A separate barrier of Efremenko–Landsberg–Schenck–Weyman (arXiv:1609.02103) already rules out the method alone for the standard padded permanent versus determinant in a specified asymptotic parameter range.

Young and Koszul flattenings remain the first principled untested families. A rigorous next computation should decompose the relevant source and target modules, build equivariant maps blockwise, and report exact ranks and representation labels rather than a single aggregate rank.
