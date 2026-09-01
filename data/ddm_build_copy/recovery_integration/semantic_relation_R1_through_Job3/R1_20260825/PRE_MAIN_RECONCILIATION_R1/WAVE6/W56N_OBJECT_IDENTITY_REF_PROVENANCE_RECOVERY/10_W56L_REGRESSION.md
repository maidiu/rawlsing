# W56L regression

W56N is a successor repair, not a rollback of W56L.

Preserved properties exercised by the defensive fixture:

- Python must be invoked with `-I -S`; isolation flags are checked before any non-built-in import.
- No repository-controlled import path is admitted.
- Trusted Git is an explicit canonical absolute executable outside the repository, not a PATH-selected command.
- The child Git environment contains no PATH and suppresses system/global Git configuration, lazy fetch, paging, prompts, replacement objects, and optional locks as before.
- The trusted Git executable is fingerprinted and required to remain stable across execution.
- The repository root, `.git` root, and top-level `.git/objects` root remain explicit/canonical and linked-worktree `commondir` indirection remains rejected.
- replacement refs, grafts, alternates, HTTP alternates, and shallow repositories remain rejected.
- no external diff, textconv, repository helper, Rawlsing runtime import, or bootstrap escape is introduced.

Normal loose-object storage passes. After deterministic repack/prune, normal packed-object storage also passes, proving the new identity rule did not accidentally turn physical loose-object location into authority.

The only intended semantic changes are the W56M closures: object bytes require independent hash rebind, governance paths traverse verified trees, ancestry trusts only verified commits, changed paths derive from verified trees, and trust-bearing refs come from bounded direct files storage rather than Git ref resolution.

Bootstrap remains exhausted. This regression does not reopen W56I/W56J installation semantics.