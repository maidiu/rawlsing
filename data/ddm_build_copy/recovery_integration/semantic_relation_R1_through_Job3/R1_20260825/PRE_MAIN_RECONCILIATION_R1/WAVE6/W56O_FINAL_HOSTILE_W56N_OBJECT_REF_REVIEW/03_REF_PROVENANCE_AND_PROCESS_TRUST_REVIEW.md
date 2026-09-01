# Ref provenance and W56L process-trust review

## Ref provenance

W56O independently inspected the actual ref resolver rather than accepting W56N's prose summary.

Trust-bearing refs are limited to exact full `refs/heads/...` and `refs/remotes/...` names. `meta()` traverses the pinned `.git` directory using POSIX directory descriptors and `O_NOFOLLOW` for pathname components/final files; metadata nodes must be bounded regular files. Loose refs reject symbolic `ref:` indirection, multiline content, CR contamination, non-ASCII values, whitespace-bearing/malformed values, and anything other than one exact OID.

`packed-refs` is read through the same bounded metadata reader. Its parser rejects malformed records, duplicate names, malformed/orphan peeled lines and malformed OIDs. Resolution then uses only the exact requested full ref.

The loose/packed rule is deterministic and deliberately stricter than normal Git shadowing:

- neither exists -> fail;
- one exists -> use it;
- both agree exactly -> use it;
- both disagree -> fail closed.

Critically, a ref OID is not accepted merely because bounded metadata named it. `resolve_ref()` immediately calls the verified commit reader, so the resulting OID must independently rebind as a commit object before the resolver returns success.

Reftable markers/storage are rejected; symbolic refs are rejected; loose/packed redirection is rejected; replacement refs, grafts, alternates, HTTP alternates and shallow state remain prohibited.

Therefore:

`TRUST_BEARING_REF_VALUES_ORIGINATE_ONLY_FROM_BOUNDED_NONREDIRECTED_REPOSITORY_REF_STORAGE = CLOSED`

`REF_OID_IS_COMMIT_OBJECT_ONLY_AFTER_CRYPTOGRAPHIC_REBIND = TRUE`

## SHA-1 / SHA-256 coherence

Object hash family is selected from exact OID width: 40 hex -> SHA-1/20-byte tree entries; 64 hex -> SHA-256/32-byte tree entries. Verified commit/tree child OIDs must remain in the same family. A mismatched family fails before evidence is trusted. This is consistent with normal SHA-1 and SHA-256 Git object semantics at the supported files-ref storage grain.

## W56L regressions

The successor retains the W56L process boundary:

- only built-in `sys` is imported before the execution-isolation barrier;
- `isolated`, `ignore_environment`, `no_user_site`, `no_site`, and `safe_path` must all be true, requiring the authoritative `python3 -I -S` invocation;
- post-barrier imports are Python stdlib only;
- repository-controlled `sys.path` entries are rejected;
- repository root is an explicit absolute, canonical, non-symlink input;
- `.git` and top-level `.git/objects` are pinned explicitly and common-dir indirection is rejected;
- trusted Git is an explicit absolute, canonical, executable regular file outside the repository with no symlink components;
- the Git executable receives a pre/post SHA-256 + filesystem identity fingerprint;
- child Git environment is reconstructed and contains no inherited PATH;
- system/global Git configuration, replacement objects, lazy fetch, pager/prompt and optional locks are suppressed as before;
- graft, alternate, HTTP-alternate, replacement-ref and shallow state remain fail-closed;
- no Rawlsing runtime/helper import, external diff/textconv authority, or bootstrap escape was introduced.

The W56M object/ref repair is additive to that process boundary rather than a rollback of it.

Host-specific POSIX `dir_fd` / `O_NOFOLLOW` semantics remain an explicit integration-time prerequisite. The code fails closed when those primitives are unavailable; this is an external host precondition, not candidate-controlled authority.

Result:

`W56L_PROCESS_TRUST_REGRESSION = GREEN`