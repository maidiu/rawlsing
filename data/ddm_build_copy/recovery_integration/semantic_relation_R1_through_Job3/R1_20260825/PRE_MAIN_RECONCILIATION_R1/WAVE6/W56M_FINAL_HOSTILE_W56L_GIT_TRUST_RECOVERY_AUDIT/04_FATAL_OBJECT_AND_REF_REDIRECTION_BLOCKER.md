# Fatal object/ref redirection blocker

Exact blocker:

`FAIL_CLOSED__INTERNAL_GIT_OBJECT_STORE_SYMLINK_REDIRECTION_ALLOWS_OID_BYTES_SUBSTITUTION`

## Why W56L misses it

The exact W56L validator checks symlink components for the externally supplied repository root, `<root>/.git`, and the top-level `<root>/.git/objects` path. It resolves that top-level object directory and requires it to be a directory. It rejects `commondir` indirection.

It does **not** recursively prohibit or otherwise authenticate filesystem indirection beneath `.git/objects`, including a symlink at a concrete loose-object pathname. Repository hardening later checks shallow state, replace refs, top-level worktree/git/common-dir identity, `info/grafts`, and `objects/info/alternates`; none detects the loose-object symlink replay.

Trust-bearing reads are then performed as `cat-file blob <spec>` and `cat-file commit <oid>`. Success output is accepted directly. There is no independent recomputation of the Git object hash over returned raw object type/length/content and comparison to the OID that was requested or derived from the parent object.

On the replay host, Git followed a symlinked loose-object file and returned attacker-controlled bytes under a different requested OID without an error. This is a direct counterexample to W56L's invariant that exact object addressing implies trusted immutable-object bytes after its environment/metadata hardening.

The corroborating ref replay shows the same structural gap under `.git/refs`: an internal ref-file symlink is followed by `rev-parse --verify` and can source the trust-bearing ref value from outside the pinned metadata tree.

## Security consequence

This is not cosmetic repository corruption. The predecessor gate uses these reads to establish:

- its own canonical predecessor blob identity;
- canonical protected manifest bytes;
- canonical authorization and audit-result schema bytes;
- immutable authorization/audit JSON bytes;
- raw commit parent headers used for ancestry/direct-child decisions;
- candidate/audit changed-path jurisdiction through commit/tree objects.

If the execution environment can substitute bytes behind an expected loose-object pathname without the gate rebinding those bytes to their requested OID, the supposedly immutable repository-object authority can be replaced while the trusted Git binary, PATH closure, explicit repository root, top-level `.git/objects` root, config suppression, replacement-ref prohibition, graft prohibition, alternates prohibition, and shallow prohibition all remain satisfied.

This attack requires no second bootstrap, no candidate Python import, no PATH-selected executable, no Git alias, no external diff, no alternates file, no replacement ref, and no kernel semantic failure. It is ordinary filesystem state inside the repository metadata tree that W56L has explicitly treated as canonical repository authority rather than as a trusted external host prerequisite.

Therefore W56L cannot receive either authorized PASS ruling.
