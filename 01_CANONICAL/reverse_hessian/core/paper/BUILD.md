# PDF build

The checked-in PDF was built with pdfTeX from TeX Live 2025/dev.

```bash
export SOURCE_DATE_EPOCH=1784160000
pdflatex -interaction=nonstopmode -halt-on-error a_uniform_line_formula_and_hessian_orbit_incomparability.tex
pdflatex -interaction=nonstopmode -halt-on-error a_uniform_line_formula_and_hessian_orbit_incomparability.tex
pdflatex -interaction=nonstopmode -halt-on-error a_uniform_line_formula_and_hessian_orbit_incomparability.tex
```

The source suppresses volatile PDF dates, trailer IDs, and pTeX information. Auxiliary files are not part of the release.
