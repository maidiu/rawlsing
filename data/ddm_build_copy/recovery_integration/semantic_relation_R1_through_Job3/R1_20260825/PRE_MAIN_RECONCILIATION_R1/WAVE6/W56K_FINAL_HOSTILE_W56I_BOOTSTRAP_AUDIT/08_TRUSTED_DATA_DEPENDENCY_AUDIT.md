# Trusted data dependency audit

## G9 — FAIL despite correct locator design

Static design is otherwise strong:
- `canonical_text(live, rel)` uses `git show <live>:<rel>`;
- canonical schemas/manifests are loaded only through that exact live commit locator;
- authorization/audit evidence uses immutable `commit:path` references;
- no candidate-worktree schema/manifest fallback is present.

However every one of those exact-object reads is mediated by the same bare PATH-resolved `git` executable. A hostile shim can fabricate output for `rev-parse`, `show`, `cat-file`, `merge-base`, `diff`, `hash-object` and branch-tip queries. Therefore the string form `<live>:<path>` is not sufficient to prove that the bytes came from Git's object database when the executable implementing the query is not itself outside candidate/environment control.

The data-addressing closure is correct; the executable that vouches for the address is not closed.

`G9 = FAIL_TRUSTED_GIT_OBJECT_READER_PROVENANCE_UNCLOSED`.