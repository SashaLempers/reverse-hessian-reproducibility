# PUBLIC_REPO_PLAN

## Included

`paper/`, active `scripts/`, deterministic `certificates/`, `tests/`, `.github/workflows/verify.yml`, `README.md`, `CLAIMS.md`, `CITATION.cff`, `LICENSE`, and `requirements.txt`.

## Publication rule

A public release should be generated from the clean tree, then verified with:

```bash
python run_all.py
python scripts/check_reproducibility.py
python -m unittest discover -s tests -v
```

The degree-5/6 SRMT bundles, nested ZIP files, historical PDFs, runtime logs, and machine-specific paths are excluded. The manuscript must cite certificate filenames but must not treat finite checks as general proofs.

## Recommended release tags

- `v1.0.0-audit`: reproducibility and barrier note.
- A later scholarly tag only after external mathematical review and a human novelty check.
