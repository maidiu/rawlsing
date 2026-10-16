# PYAT SHARED-STORE SPARSE WORKTREE EXECUTION LAW — R1

Status: BINDING DEFAULT FOR ALL NEW PYAT COMMISSIONS
Scope: local worker execution on any machine hosting multiple concurrent Rawlsing jobs

## Core topology

The normal PYAT local execution topology is:

1. ONE canonical Rawlsing clone/object store per machine.
2. ONE isolated Git worktree per concurrently active worker branch.
3. Each worker worktree is sparse-scoped to the smallest lawful working set required by its commission.
4. All worker worktrees share the canonical repository's Git object database.
5. A worker pushes ONLY its own commissioned branch.

This is the default. A worker must not create a fresh clone merely because it needs a separate branch or sparse checkout.

Multiple workers MUST NOT operate concurrently in the same checked-out working directory. Isolation is by worktree, not by duplicate repository clone.

## Concurrency law

There is **no fixed project-wide worker or reviewer slot count**.

HQ SHALL maximize safe orthogonal concurrency when:
- prerequisites are independently satisfied;
- write terrain does not overlap in a way that creates branch-level semantic collision;
- independent review remains independent;
- host resources are adequate;
- the user has an available execution surface.

A numerical slot limit from an older activation packet is routing history, not current law.

Do not serialize a ready critical-path lane merely because two other implementation workers are active. Conversely, do not parallelize two writers over the same semantic owner merely to maximize tab count.

A read-only hostile review may normally proceed alongside implementation workers when its candidate is frozen and its review independence is preserved.

## Commission requirement

Every new commission intended for local execution MUST prominently specify:

- AGENT
- MODEL / INTELLIGENCE
- MACHINE, when assigned
- BRANCH
- EXACT COMMISSION / STARTUP TIP
- CHECKOUT: SPARSE_REQUIRED
- exact prepared worktree path, when HQ-authorized infrastructure has already prepared one

If the exact local worktree path is known, the commission should begin with wording equivalent to:

> Your governed sparse worktree has already been prepared and verified by HQ-authorized infrastructure bootstrap.
>
> DO NOT recreate it.
> DO NOT clone.
> DO NOT fetch broadly.
> DO NOT change sparse scope.
> DO NOT switch branches.
> DO NOT merge or rebase.
>
> cd <EXACT_WORKTREE_PATH>
>
> Verify:
>
> git branch --show-current
> git rev-parse HEAD
> git status --short
>
> The branch and HEAD must match the commission exactly before mutation begins.

If a prepared worktree path is NOT supplied, the worker must not infer that it is authorized to clone a new repository. It must use an already-authorized shared-store worktree if one is available, or report that local worktree bootstrap is required.

## Startup verification

For a fresh commissioned worker whose worktree has not yet been mutated:

- git branch --show-current MUST equal the commissioned branch.
- git rev-parse HEAD MUST equal the exact commissioned startup tip.
- git status --short MUST be clean.
- the worker must not reset, merge, rebase, force-checkout, or otherwise hide a mismatch.

For a RESUMED worker:

- preserve existing local work;
- do NOT reset merely because HEAD no longer equals the original commission tip;
- first report current branch, HEAD, status, and whether there are local commits or uncommitted changes;
- continue from the existing lawful worktree state if it is clearly the same commissioned lane.

## Sparse-scope law

Workers must not broaden sparse scope merely to inspect historical evidence.

Historical evidence outside the sparse checkout should be read from the shared canonical object store using exact Git-object operations where practical, including:

- git show <commit>:<path>
- git cat-file
- git ls-tree
- git diff <base>..<head> -- <path>

A broader sparse scope may be authorized only when the commission itself requires working-tree access to those paths.

## Fetch / network law

Do not perform broad or repeated fetches by default.

A worker may perform the minimum fetch required to resolve its own commissioned remote branch or exact evidence commit when the local object store lacks it. It must not fetch all branches/tags as routine setup.

No worker may pull, merge, or rebase another worker branch into its own lane unless explicitly commissioned.

## Push law

At completion:

1. commit only the worker's lawful changes;
2. push only the commissioned branch;
3. re-fetch or otherwise verify the remote branch tip;
4. report the exact pushed SHA and return disposition.

A worker must not self-adopt into integration/control.

## Environment law

Python/Node/tool environments are not Git worktrees and should not be duplicated per branch unless isolation is actually required.

Where a governed or qualification environment is shared, commissions should point to the exact shared environment path and provenance.

If an exact governed environment named by a commission is missing:

- do NOT silently recreate it and call the replacement governed;
- use an explicitly authorized reconstruction only when permitted;
- report its exact interpreter/package provenance;
- label reconstructed execution as reconstructed evidence, not governed certification;
- do not block unrelated Git worktree progress unless the missing environment is genuinely a qualification prerequisite.

## Failure law

The absence of a worktree is an infrastructure/bootstrap issue, not authorization to clone.

A startup SHA mismatch, wrong branch, dirty unexpected state, or missing shared environment must be surfaced truthfully. Do not destroy existing local work to force the expected state.

## Default commission footer

All future PYAT commissions should carry or incorporate this rule:

SHARED_STORE_WORKTREE_REQUIRED:
- use the HQ-authorized sparse worktree for this branch;
- do not clone;
- do not recreate an existing worktree;
- do not broaden sparse scope;
- do not use the same working directory concurrently with another branch;
- share the canonical repository object store;
- push only this commissioned branch.
