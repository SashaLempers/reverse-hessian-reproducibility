# Result reproduction table

| résultat | preuve papier | script | log | hash principal | statut |
|---|---|---|---|---|---|
| uniform determinant Hessian identity | paper, Exact determinant identity | `scripts/verify_uniform_formulas.py` | `logs/full_run.log` | `9f805d77104ee40b2ca7eae5e108f8dc752aa5fa828c46926fd4c92c944bf1c0` | PROVED; finite CERTIFIED-COMP checks |
| `n=3`: `det Hess(det_3)=-2 det_3^3` | paper + exact reconstruction | `scripts/certify_catalecticant_ranks.py` | `runtime_logs/primary_catalecticants.log` | `3aa9ac673aba18a0466740f30df7ee7f96273acba4c33c6be8dbfde4ec11d2c8` | PROVED + CERTIFIED-COMP |
| permanent line restriction | paper, exact line restriction | `scripts/verify_uniform_formulas.py` | `runtime_logs/uniform_formulas.log` | `9f805d77104ee40b2ca7eae5e108f8dc752aa5fa828c46926fd4c92c944bf1c0` | PROVED; finite checks |
| non-power property | paper, root multiplicity corollary | `—` | `—` | `n/a` | PROVED |
| polystability | paper, support-cone proof | `—` | `—` | `n/a` | PROVED using LITERATURE criterion |
| all catalecticant ranks | paper, certification section | `scripts/certify_catalecticant_ranks.py` | `runtime_logs/primary_catalecticants.log` | `3aa9ac673aba18a0466740f30df7ee7f96273acba4c33c6be8dbfde4ec11d2c8` | CERTIFIED-COMP |
| independent modular cross-check | paper, certification section | `scripts/independent_catalecticant_check.py` | `logs/independent_catalecticant_check.log` | `4b88fcb9b5b949d8b7fcb9c0c3768351770113fff945389b5fb6c180f5f8d2c3` | CERTIFIED-COMP |
| squarefreeness of `D_per,3` | paper, appendix | `scripts/certify_squarefree_Dper3.py` | `logs/squarefree_Dper3.log` | `8a9f85b1716f03b1a6ab0fb246a1033627ce7b3fba645716a0d0b992fa525e41` | CERTIFIED-COMP |
| padding factorization and collapse | paper, padding section | `scripts/transverse_hessian_experiments.py` | `runtime_logs/transverse_hessian.log` | `7b5bf5bfaef9f74a7035c1f3c10bad6de8ef176b62c790cc77bf43bef507678d` | PROVED; finite checks |
