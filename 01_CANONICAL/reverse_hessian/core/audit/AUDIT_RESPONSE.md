# Response to the independent audit

The audit verdict is accepted as a major-revision constraint.

## Mathematical repairs inserted

1. **Zero Hessian image in the transfer principle.** The proof now treats `D(p)=0` first: covariance and continuity force `D(f)=0`. Only then is the nonzero twisted-orbit lemma invoked.
2. **Spectrum of `B=A^{-1}C`.** The paper now defines
   `W={x:x_1=0, sum_{i>=2}x_i=0}` and `u=(0,1,...,1)^T`, proves `B|_W=I`, `Be_1=0`, and `Bu=(n-2)e_1`, and derives the complete algebraic spectrum.
3. **Distinct row-column characters.** The paper explicitly varies two row parameters, or two column parameters, to separate every pair of characters `a_i b_j`.
4. **Convergence of central scalars.** From `a_k^e -> L != 0`, the proof now states boundedness and boundedness away from zero, extracts a convergent subsequence, and identifies its nonzero limit as an `e`-th root of `L`.

## Novelty correction

The earlier phrase calling original equal-size determinant/permanent incomparability a central new deduction has been removed. It is now a corollary included for completeness and accompanied by the explicit observation that the published stabilizer and polystability results already imply it.

The paper's main theorem contains only the two Hessian-image noncontainments. The exact priority of the permanent line formula and of this Hessian-orbit formulation remains `UNKNOWN`. No statement uses `new`, `first`, or `revolutionary` as a proved bibliographic fact.

## Reproducibility correction

The earlier package contained no executable scripts and used the same script hash for two JSON files presented as independent outputs. The revised repository contains:

- a primary exact script;
- a separately written exact clean-room script;
- a pure-Python modular script importing neither SymPy nor the other engines.

The three script hashes are different. `cross_engine_consistency.json` rejects the run unless all polynomial hashes, direct integer matrix hashes, and ranks agree. The environment, one-command workflow, JSON normalization rules, and canonical polynomial/matrix serialization are now explicit.

## Scope retained

The audit's central negative conclusion is retained without dilution: this is not a padded GCT obstruction, not a determinantal lower bound, and not a result proving `VP != VNP`.
