# Independent audit findings incorporated into this release

This file records the substantive findings supplied with the major-revision request. It is a summary, not a replacement for the auditor's original files.

## Reproduced mathematical outputs

The auditor independently reconstructed:

```text
det Hess(det_3) = -2 det_3^3
det Hess(per_3)(J_3 + (t-1)E_11) = 64 t
```

The reported `Dper3` data were: degree `9`, `55` monomials, one degree-9 factor in the exact factorization over `Q`, and gcd of the first partial derivatives equal to `1`.

The reported catalecticant vectors were:

```text
Ddet: 1,9,45,165,270,270,165,45,9,1
Dper: 1,9,45,165,414,414,165,45,9,1
```

The line formula was directly reconstructed through `n=8`, with multiplicities:

```text
1,4,9,16,25,36 = (n-2)^2.
```

## Required proof repairs

The audit required explicit treatment of:

1. the case `D(p)=0` in the transfer principle;
2. the spectrum of `B=A^{-1}C`;
3. pairwise distinctness of the row-column torus characters;
4. extraction of a nonzero convergent subsequence from convergence of `a_k^e`.

All four repairs are now in the paper.

## Required novelty correction

The audit observed that published stabilizer and polystability results already imply the original equal-size determinant/permanent incomparability. The earlier novelty language was therefore removed. The only potential priority question retained is the exact permanent line formula and the Hessian-image formulation, both classified as `UNKNOWN`.

## Required reproducibility correction

The audit found that the earlier ZIP omitted the scripts and that two nominally independent JSON outputs shared one script hash. This release supplies three scripts with distinct hashes, a frozen Python environment, a one-command workflow, and a canonical serialization specification.

The auditor-reported hashes for its own independent artifacts were:

```text
independent_check.py:
a531f2ce555f1edea4e6f0c3e7190f8fdb726f3ae7e74c1cbf18bd926b0cfb63

independent_check_results.json:
e357c0e81a8018aa15eac513b318bfb750ef011d3ad77d2570c8620e3136a78f
```

Those raw external audit artifacts were not mounted in the active build filesystem and are therefore not falsely duplicated in this archive.
