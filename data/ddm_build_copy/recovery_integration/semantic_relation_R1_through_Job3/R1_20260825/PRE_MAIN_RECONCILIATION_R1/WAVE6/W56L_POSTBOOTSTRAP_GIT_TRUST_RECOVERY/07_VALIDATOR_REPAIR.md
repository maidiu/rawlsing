# Validator repair

The repaired `validate_enforcement_candidate_from_canonical.py` remains standalone stdlib and preserves the W56I Python isolation barrier.

Material changes:

- removes `_git_cwd()` and every bare `subprocess.run(["git", ...])` call;
- requires explicit `--repository-root` and `--trusted-git-executable` host arguments;
- validates both before the first Git subprocess;
- invokes the exact absolute Git path for every trust-sensitive command;
- constructs a minimal Git environment with no PATH;
- fingerprints the Git executable before and after the gate;
- rejects `.git` gitfiles, symlink/common-dir repository discovery, escaped loose/packed ref storage, replacement refs, grafts, alternates, shallow ancestry state, root mismatch, malformed OIDs, failed object reads, and malformed changed paths;
- invokes every Git command with explicit `--git-dir=<repository-root>/.git` and `--work-tree=<repository-root>`;
- requires full `git fsck --full --no-reflogs --no-progress` object-database integrity before any trust-bearing canonical/ref/object fact is consumed;
- independently re-hashes every returned commit/blob payload with Git object framing and rejects any payload whose computed OID differs from the requested exact OID;
- resolves canonical schema/manifest/evidence paths only from exact authenticated commit/object addresses, with no candidate fallback;
- replaces `merge-base --is-ancestor` and `rev-list --parents` with Python traversal/parsing of authenticated raw commit objects;
- uses NUL-delimited `diff-tree` with explicit external-diff/textconv/rename suppression only after object-database integrity has been established;
- retains the existing canonical authorization/result schema enforcement and exact hostile-audit binding.

The earlier synthetic full ordinary replay and candidate-schema mutation checks remain preserved as W56L pre-terminal evidence. Final VOZHD review subsequently discovered the repository-gitfile/ref-store/object-ID seams recorded in `15_REPOSITORY_METADATA_OBJECT_ROOT_CORRECTION.md` and `16_REF_STORE_AND_OBJECT_ID_AUTHENTICATION_CORRECTION.md`; those later receipts supersede the earlier local seal at those exact grains.

Final local deterministic regressions additionally establish:

- non-isolated invocation still exits `97` before shadowable imports;
- ordinary isolated repository hardening reaches `full_object_database_fsck = PASS`;
- symlinked `.git/refs` is rejected before canonical ref resolution;
- Git's unauthenticated loose-object payload behavior is reproducible in the unpatched primitive;
- the repaired gate rejects the same object-database substitution because full fsck fails;
- the committed validator blob is byte-identical to the locally syntax-checked/tested source.

No local test or receipt constitutes hostile certification or canonical adoption.