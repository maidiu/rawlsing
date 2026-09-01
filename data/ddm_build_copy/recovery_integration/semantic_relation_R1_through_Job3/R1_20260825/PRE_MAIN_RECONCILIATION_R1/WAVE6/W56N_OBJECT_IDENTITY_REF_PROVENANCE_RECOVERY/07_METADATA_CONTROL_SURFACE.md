# Metadata control surface

W56N reviews only metadata that can alter the trust semantics actually used by the predecessor gate.

Bounded direct metadata reads cover:

- `.git/config` for repository-format, object-format, and ref-storage controls;
- `.git/packed-refs` and the exact loose full refs used for canonical/audit branch resolution;
- reftable storage markers/control, which are unsupported and fail closed;
- `info/grafts`;
- `objects/info/alternates` and `objects/info/http-alternates`;
- `shallow`;
- replacement-ref storage.

The direct metadata reader requires the already-pinned `.git` directory, POSIX directory-file-descriptor traversal, `O_NOFOLLOW`, regular bounded files, and no `..`/absolute path escape. A trust-controlling metadata path that is symlinked or otherwise redirected cannot become input.

Repository storage controls are limited to the supported SHA-1/SHA-256 object formats and files-based refs. Unsupported repository format/ref storage is rejected instead of delegated to undocumented fallback behavior.

W56L's existing Git-side regression checks for exact worktree/git/common-dir identity are retained. `commondir`, grafts, alternates, replacement refs, and shallow state remain prohibited. Lazy object fetch remains disabled.

W56N does not recursively distrust unrelated `.git` metadata. Nor does it impose pathname uniqueness below `.git/objects`: object bytes are governed by cryptographic identity, whereas ref/control bytes are governed by bounded metadata provenance. This separation is intentional.