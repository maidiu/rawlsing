# Verified tree/path resolution

Trust-sensitive governance files no longer use Git revision syntax such as `canonical_commit:path` or `authorization_commit:path`.

`verified_blob_at_path` / `at_path` performs the path resolution itself:

1. read and cryptographically verify the exact commit OID;
2. parse its header only after verification and obtain the exact root-tree OID;
3. read and cryptographically verify the root tree by OID;
4. parse the binary Git tree entries, including the repository hash-width OID bytes;
5. for each intermediate pathname component, require tree mode and read/verify the child tree by its exact OID;
6. for the final component, require a regular blob mode, read the blob by exact OID, and independently rebind the returned bytes to that OID.

Malformed trees, duplicate names, invalid path components, mixed object-ID algorithms, symlink/gitlink governance leaves, missing entries, and object hash mismatches fail closed.

This chain is used for the canonical validator copy, protected-path manifest, canonical authorization/result schemas, immutable authorization JSON, immutable audit JSON, and other trust-sensitive governance bytes consumed by this gate.

The local fixture constructs a nested governance path and verifies that the resolved blob OID exactly matches the OID named by the verified tree. It separately substitutes different compressed bytes behind that requested blob pathname; Git can expose the substituted bytes, but the verified path reader rejects them before returning governance evidence.