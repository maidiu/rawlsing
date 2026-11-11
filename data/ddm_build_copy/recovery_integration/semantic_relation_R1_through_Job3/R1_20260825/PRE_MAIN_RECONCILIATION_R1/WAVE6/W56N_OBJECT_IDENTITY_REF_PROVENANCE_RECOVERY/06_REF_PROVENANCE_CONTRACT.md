# Ref provenance contract

Required proposition:

`TRUST_BEARING_REF_VALUES_ORIGINATE_ONLY_FROM_BOUNDED_NONREDIRECTED_REPOSITORY_REF_STORAGE`

Refs are mutable names, not content-addressed objects. They therefore do not inherit the object-identity rule.

W56N accepts only the exact full refs used by the predecessor gate under `refs/heads/...` and `refs/remotes/...`. Their values are read directly from the pinned `.git` metadata tree rather than provenance-resolved through Git.

## Loose refs

Each pathname component is opened relative to the already-pinned `.git` directory using POSIX dir-fd/openat-style operations with `O_NOFOLLOW`. Symlinked components or the final ref file fail closed. The final node must be a bounded regular file containing exactly one pure OID, with at most one terminal LF. `ref:` symbolic indirection, additional lines, whitespace-bearing values, malformed OIDs, and special nodes are rejected.

## Packed refs

`.git/packed-refs` is read through the same bounded non-following metadata reader. The parser is strict: malformed records, duplicate names, invalid OIDs, and orphan/malformed peeled records fail closed. Only the exact requested full ref is selected.

## Loose + packed rule

- neither representation present: unresolved / fail;
- exactly one present: use that exact OID;
- both present with the exact same OID: accept deterministically;
- both present with different OIDs: ambiguous storage / fail closed.

No loose-over-packed shadowing is treated as authoritative at the trust boundary; agreement is required when both exist.

The resulting OID still has no commit authority merely because a ref named it. W56N immediately reads and cryptographically verifies that exact commit object before the ref resolver returns success.

Unsupported ref storage (including reftable control/markers), symbolic refs, redirected `packed-refs`, redirected loose refs, and redirected path components are rejected rather than guessed through Git behavior.