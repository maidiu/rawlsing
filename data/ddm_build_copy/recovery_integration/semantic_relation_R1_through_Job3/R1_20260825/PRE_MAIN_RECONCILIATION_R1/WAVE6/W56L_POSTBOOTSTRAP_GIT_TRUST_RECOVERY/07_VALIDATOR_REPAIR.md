# Validator repair

The repaired `validate_enforcement_candidate_from_canonical.py` remains standalone stdlib and preserves the W56I Python isolation barrier.

Material changes:

- removes `_git_cwd()` and every bare `subprocess.run(["git", ...])` call;
- requires explicit `--repository-root` and `--trusted-git-executable` host arguments;
- validates both before the first Git subprocess;
- invokes the exact absolute Git path for every trust-sensitive command;
- constructs a minimal Git environment with no PATH;
- fingerprints the Git executable before and after the gate;
- rejects replace refs, grafts, alternates, shallow ancestry state, root mismatch, malformed OIDs, failed object reads, and malformed changed paths;
- replaces `git show` with `cat-file blob` exact-object reads;
- replaces `merge-base --is-ancestor` and `rev-list --parents` with Python traversal/parsing of raw exact commit objects;
- replaces textual `git diff --name-only` with NUL-delimited `diff-tree` and explicit external-diff/textconv/rename suppression;
- retains canonical schema/manifest loading and no candidate fallback.

A synthetic full ordinary replay with repaired predecessor canonical, sibling authorization, candidate-descending hostile result, and changed protected path returned:

`EXTERNAL_INTEGRATION_ELIGIBLE = true`

with zero false checks.

A second synthetic attack weakened candidate-side hostile schemas and supplied an invalid audit mode; the repaired predecessor still returned `AUDIT_RESULT_SCHEMA_VALID=false`, `AUDIT_MODE_HOSTILE_INDEPENDENT=false`, and integration ineligible because the live-canonical schemas remained authoritative.