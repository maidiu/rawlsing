# Verified object reader

The repaired validator centralizes trust-bearing object reads in `GitTrust.read_object` / the typed wrappers for commit, tree, and blob.

A read has the following order:

1. Validate the requested OID as exact pure lowercase hex and select SHA-1 for 40 hex digits or SHA-256 for 64.
2. Invoke the already-pinned, fingerprinted Git executable with `cat-file -t <oid>` and require the exact expected type.
3. Invoke `cat-file <expected_type> <oid>` to obtain the exact payload bytes.
4. Independently compute the Git object identity in Python stdlib over `expected_type + " " + decimal byte length + NUL + payload`.
5. Require the recomputed OID to equal the requested OID before returning payload bytes to any caller.

No `cat-file` success bit is itself evidence. The object read becomes authoritative only at step 5.

The defensive fixture reproduces the W56M grain: a loose-object pathname for requested commit X is replaced with a symlink to the compressed object bytes for different commit Y. Raw trusted `git cat-file commit X` succeeds on the fixture host. W56N then independently hashes the returned commit payload and rejects it because it hashes to Y rather than X. The same construction is applied to a blob reached through a verified tree path and is likewise rejected.

Normal loose objects and repositories repacked into packfiles both pass the same reader. SHA-256 repositories are exercised when supported by the trusted fixture Git, proving that the algorithm is selected from the OID width rather than hard-coded to SHA-1.