# W56L repository metadata / object-root correction

This receipt supersedes the initial W56L local seal only at one newly exposed grain. It does not alter W56I/W56J/W56K history.

## Residual seam found during final VOZHD review

The initial W56L repair used an explicit repository worktree root but still invoked Git with `git -C <repository-root> ...` and then cross-checked `rev-parse --show-toplevel`.

A benign two-repository fixture proved that this was insufficient to pin repository identity. A directory `A` containing a `.git` gitfile that pointed to repository `B` caused:

- `git -C A rev-parse --show-toplevel` to report `A`;
- `git -C A rev-parse HEAD` to return repository `B`'s HEAD.

Therefore the worktree-root cross-check could succeed while trust-bearing refs and objects came from a different object database. The initial W56L seal is superseded at this exact repository-selection/object-database grain.

## Corrective implementation

The predecessor gate now establishes repository metadata identity before the first Git subprocess:

1. the externally supplied repository root must be absolute, canonical, real, and non-symlinked;
2. `<repository-root>/.git` must itself be a concrete canonical directory, not a gitfile or symlink;
3. `<repository-root>/.git/objects` must be a concrete canonical directory and may not be top-level symlink redirected;
4. linked-worktree/common-directory indirection is rejected;
5. every Git subprocess receives explicit `--git-dir=<repository-root>/.git` and `--work-tree=<repository-root>` instead of relying on `-C` discovery;
6. `rev-parse --absolute-git-dir` and `rev-parse --git-common-dir` must both resolve exactly to the pinned `.git` directory;
7. graft/alternate locator probes must remain inside that pinned metadata directory.

The trusted-host prerequisite set is not enlarged. The externally supplied absolute repository root deterministically binds its admissible metadata/object root.

## Benign deterministic verification

A fresh local fixture harness exercised the required eight verification classes after this correction. Host tools used by the fixture were `/usr/bin/git` and isolated Python `/opt/pyvenv/bin/python3`.

| Check | Result | Deterministic observation |
|---|---|---|
| exact declared Git executable | PASS | absolute `/usr/bin/git` produced the ref result while a benign PATH-prepended fake `git` marker never ran |
| inherited executable search | PASS | parent PATH mutation did not affect the explicitly invoked executable |
| inherited Git configuration / selectors | PASS | hostile parent `GIT_DIR`, `GIT_OBJECT_DIRECTORY`, `GIT_NAMESPACE`, global config, HOME, and injected config entries did not alter the explicit repository/ref result under the reconstructed child environment |
| repository identity independent of discovery | PASS | the old `.git` gitfile fixture reproduced cross-repository redirection; the repaired pre-Git root validator rejected the same root because `.git` was not a concrete directory |
| ref / object / ancestry reproducibility | PASS | exact canonical ref bytes, exact `cat-file blob` bytes, raw commit bytes, and Python parent traversal remained identical across parent-environment mutations |
| invalid host prerequisites | PASS | relative Git path, missing Git path, repository-local executable, and symlinked executable were rejected by the trusted-host contract |
| Python isolation invariants | PASS | `-I -S` reported `isolated=1 ignore_environment=1 no_user_site=1 no_site=1 safe_path=True` |
| candidate governance substitution | PASS | candidate-side schema mutation differed from the canonical commit, while exact canonical `cat-file blob <canonical>:schema.json` continued to return the canonical bytes |

`BENIGN_FIXTURE_MATRIX = 8/8 PASS`

No offensive payload or general-purpose evasion mechanism was constructed; all fixtures were local marker/configuration substitutions sufficient only to prove closure or rejection of the relevant degree of freedom.

## Remaining boundary

Host compromise remains outside repository governance: trusted Python, trusted absolute Git, stable OS/process/filesystem semantics, and the externally supplied absolute repository root remain explicit external prerequisites. Independent hostile review of the exact terminal W56L successor remains mandatory before any canonical movement.
