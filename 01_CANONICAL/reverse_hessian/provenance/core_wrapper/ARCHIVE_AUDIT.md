# Archive audit

## Source integrity

The user-supplied source archive was checked against its sidecar checksum:

```text
edd1434a10f6cb11c33b2a306b2286b27f61a91b71d79062f1d8d282e99792ee
```

The computed SHA-256 of `reverse_hessian_full_reproducible_package.zip` matches exactly.

The superseded equal-size package is preserved with the verified SHA-256:

```text
954da1ccce55fbdf0af3020cc0fcf822428a4dc9716b11a83a7c347f60bc1e61
```

## Organization

- `public_repo/`: authoritative corrected paper, scripts, certificates, tests, logs, and reproducibility specifications.
- `forensic_archive/source_packages/`: original input ZIP and checksum.
- `forensic_archive/prior_outputs/`: superseded generated releases and checksums.
- `forensic_archive/audit_material/`: selected historical sources and reports retained for provenance.

No superseded file was silently deleted. `FULL_MANIFEST.txt` and `SHA256SUMS_FULL.txt` enumerate and hash the complete directory. `public_repo/MANIFEST.txt` and `public_repo/SHA256SUMS_PUBLIC.txt` do the same for the publishable repository.

## Safety

The final release archives are created by a deterministic packager from relative paths below their designated roots. Absolute names, `..` traversal components, device files, and symbolic links are rejected. A post-build ZIP integrity and path-safety test is performed before delivery.
