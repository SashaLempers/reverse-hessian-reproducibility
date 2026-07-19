# FORENSIC_ARCHIVE_PLAN

The forensically complete layer retains the exact uploaded ZIP, its `.sha256` sidecar, the package-wide inventory, and the internal-manifest audit. Nested historical archives are not expanded again in the final deliverable because the original ZIP already preserves their bytes.

Nothing is silently deleted. Historical degree-5/6 sweeps, SRMT drafts, barrier patches, old certificates and logs remain recoverable from `forensic_archive/reverse_hessian_full_reproducible_package.zip`.

Files with absolute paths or runtime fields are evidence of provenance only; they are not imported into deterministic certificates.
