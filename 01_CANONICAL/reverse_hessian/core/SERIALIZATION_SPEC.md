# Canonical serialization and hashing specification

This file fixes the representation used for every polynomial and direct catalecticant matrix hash.

## Polynomial representation

1. Variable order:
   `x11,x12,x13,x21,x22,x23,x31,x32,x33`.
2. A monomial is a length-9 exponent vector of nonnegative integers.
3. Terms are ordered by descending Python tuple order, which agrees here with the lexicographically descending order returned by `SymPy Poly.terms()` for the fixed variables.
4. A rational coefficient is the two-element list `[numerator, denominator]`, with positive denominator and reduced fraction.
5. The payload is:

```json
[
  [[e11,e12,e13,e21,e22,e23,e31,e32,e33],[numerator,denominator]],
  ...
]
```

6. UTF-8 JSON uses separators `(',', ':')`, no spaces, no terminal newline.
7. SHA-256 is applied to those exact bytes.

## Catalecticant bases

For a weak composition of `d` into `9` parts, the first coordinate is enumerated from `0` to `d`, then the same rule is applied recursively to the remaining coordinates. Rows use degree `a`; columns use degree `9-a`.

## Direct integer matrix representation

For a matrix with `m` rows and `n` columns:

```json
{
  "rows": [
    [[column_index,integer_value], ...],
    ...
  ],
  "shape": [m,n]
}
```

Zero entries are omitted. Entries in a row are sorted by increasing zero-based column index. The object is serialized with `sort_keys=true` and compact separators, then hashed with SHA-256.

For orders `5,...,9`, certificates use the proved transpose/factorial duality and explicitly mark the matrix hash as derived rather than falsely claiming a separately serialized direct matrix.
