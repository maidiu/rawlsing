# Bounded nonblocking friction

W56O found no integrity defect that can convert unverified bytes, ancestry, changed-path jurisdiction, or ref state into a false PASS. Two bounded issues should nevertheless remain explicit.

## F1 — changed-tree entry budget is incomplete

W56N declares both `MAX_TREES` and `MAX_ENTRIES` for bounded changed-path traversal. The recursive `leaves()` enumerator increments and enforces the entry counter, but ordinary pairwise `tree_diff()` constructs and compares `tree_entries()` for both sides without incrementing `budget[1]` for those pairwise entries.

A deliberately enormous but cryptographically valid tree can therefore impose more pairwise entry-processing work than the declared `MAX_ENTRIES` bound suggests. The tree-object recursion counter remains bounded, and every tree/commit/blob consumed remains cryptographically verified.

Security disposition:

- false object identity: **NO**;
- false ancestry: **NO**;
- false path set: **NO**;
- false ref provenance: **NO**;
- unauthorized integration path: **NO**;
- candidate-controlled availability pressure / possible resource exhaustion: **YES**.

This is denial-of-service hardening, not a false-authorization primitive. It is therefore preserved as bounded nonblocking friction and should be repaired in the next ordinary enforcement-hardening successor rather than silently ignored.

## F2 — protocol operation-list documentation lags the safer implementation

`GOVERNANCE_ENFORCEMENT_CHANGE_PROTOCOL.md` still contains the W56L-era allowed-operation-family list mentioning `rev-parse --verify`, trust-bearing `diff-tree`, and `for-each-ref` replacement probing. W56N's executable no longer delegates trust-bearing ref resolution or changed-path authority through those operations; it uses bounded direct ref storage plus verified tree construction instead.

The stale list does not cause the executable to invoke those older authority seams and does not weaken the new code path. It is documentation drift that future maintainers should reconcile after lawful installation.

## Integration-time external prerequisite

The bounded ref reader intentionally requires POSIX `dir_fd`, `O_DIRECTORY`, and `O_NOFOLLOW`. The target host must satisfy those semantics at the post-installation probe. If not, the gate fails closed. W56O does not convert an untested external host into repository authority.

Overall friction disposition:

`BOUNDED_NONBLOCKING_FRICTION_ONLY__NO_FALSE_AUTHORIZATION_PATH_FOUND`