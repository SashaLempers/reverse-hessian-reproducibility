# Contributing

Please open an issue before proposing changes to a mathematical claim or certificate.

A useful report includes:

- the exact release tag and commit;
- the command and environment;
- the claim ID or certificate path;
- the observed and expected SHA-256 or mathematical value;
- a minimal reproducible example.

Pull requests must preserve the separation between proved, computed, known, negative, and open statements. Regenerate `07_MANIFEST` after any accepted source change and run the immutable `quick` profile from an external workspace.
