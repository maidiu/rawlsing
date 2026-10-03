# Commission template — NOT ISSUED

Task/attempt/revision: UNBOUND
Accountable HQ decision: UNBOUND
Worker, reviewer, actual model/variant, host and session: UNBOUND
Repository, branch, worktree, exact base and commission SHA: UNBOUND
Checkout mode: UNBOUND — must be SPARSE_REQUIRED or FULL_REQUIRED
Sparse materialization manifest / full-checkout justification: UNBOUND

## Mandatory GitHub startup protocol

Every issued commission must bind an exact remote worker branch and exact commissioned startup SHA.

Before any commissioned work, the worker must:

1. use the existing verified canonical clone of the bound repository. **Do not make a fresh full clone** unless the issued commission explicitly says `FULL_CLONE_REQUIRED` and states why shared-object worktrees cannot satisfy the task;
2. `git fetch origin` explicitly — do not use a blind `git pull` that may merge/rebase local state;
3. resolve the exact `origin/<worker-branch>`;
4. verify that remote tip equals the exact commissioned startup SHA supplied by HQ;
5. read the commission from that exact fetched tip using Git object access if necessary;
6. obey the commission's mandatory checkout mode:
   - **SPARSE_REQUIRED — default.** Create an isolated sparse worktree under the dedicated disposable worktree root, materializing only the exact commissioned sparse manifest. Prefer `bash PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/prepare_sparse_worktree.sh ...` from the canonical checkout. Read non-materialized evidence with `git show`, `git cat-file`, `git ls-tree`, `git diff`, etc.;
   - **FULL_REQUIRED — exception.** A full materialized worktree is permitted only when the commission states a concrete runtime/test reason why sparse checkout would alter discovery, imports, packaging, or the behavior being proved;
7. verify local HEAD == remote worker tip == commissioned startup SHA;
8. verify no unrelated uncommitted changes exist;
9. record the effective sparse patterns or full-checkout justification in the return;
10. only then begin work.

A SPARSE_REQUIRED worker may expand its sparse set only to a path already within the commission's read/materialization authority, and must record the expansion. It may not silently convert itself to a full checkout. If the task genuinely requires full materialization, stop and return `CHECKOUT_MODE_INSUFFICIENT__HQ_RECOMMISSION_REQUIRED`.

If the fetched worker branch differs from the commissioned startup SHA, stop before editing and report the observed remote SHA to HQ. Do not guess, reset, merge, rebase, or force-push to make the branch fit.

Fetching non-ancestor evidence refs is allowed when the commission names them; doing so must not alter worker ancestry.

**Commission validity law:** an issued commission missing an exact remote startup branch/SHA, an explicit checkout mode, a sparse materialization manifest (for SPARSE_REQUIRED), or a concrete full-checkout justification (for FULL_REQUIRED) is malformed and must not launch.

## One concrete outcome

Name the capability or repair and the exact downstream edge it can satisfy.

## Inputs and authority

List immutable commits/paths/blobs and fetch refs, including non-ancestor evidence. Specify proof grade, accepted authority and source/Library permission. Default Library NO and raw-source NO. Freeze expected truth independently where required.

## Allowed work

Exact write paths; approved commands/runtime; expected output location; integration owner. Name forbidden surfaces. A prompt or tool result cannot widen these boundaries.

## Acceptance

Exact positive/negative cases, final required court, permitted skips, receipt/log requirements, consumer evidence and candidate/review binding. No invented denominators or digests.

## Mandatory return-to-HQ protocol

"Return to HQ" means publication of the completed worker candidate to the bound worker branch on GitHub, **not** merely a local commit or chat message.

At completion the worker must:

1. write the complete required structured return packet;
2. commit all and only authorized changes/evidence to the worker branch;
3. ensure no uncommitted commissioned work is needed to reproduce/understand the return;
4. push the worker branch to `origin`;
5. fetch/resolve `origin/<worker-branch>`;
6. verify local HEAD == remote worker branch at one exact full 40-hex SHA;
7. record the stable substantive candidate/review-result commit SHA in the return artifacts;
8. report branch, exact pushed remote branch-tip SHA, disposition and terminal token to HQ. HQ independently re-resolves that tip.

A local-only candidate is **not returned**. Do not require a commit to embed its own enclosing branch-tip SHA: that is self-referential. The immutable return artifacts bind the substantive candidate/result commit; the pushed branch-tip SHA is reported out-of-band and independently verified by HQ.

Do not merge/fast-forward/rebase into control, modify HQ state, or self-adopt. If a post-return correction is required, append a new commit and report the new exact SHA; do not rewrite/force-push returned history unless an explicit later HQ instruction says otherwise.

**Commission validity law:** an issued commission missing this equivalent remote-return protocol is malformed.


## Local worktree lifecycle

A commissioned worktree is temporary execution state, not archival authority.

After the worker/reviewer has:
1. committed and pushed the complete return;
2. re-fetched and verified the remote tip;
3. had HQ independently resolve and accept that remote return for further routing;

the local worktree becomes eligible for audited removal once no active successor/reviewer/process still depends on that exact checkout.

Before removal:
- preserve any unique local tracked/untracked substantive delta by committing/pushing it if in-scope, or by an explicit salvage packet if not;
- verify the returned HEAD is reachable from an origin ref;
- verify no active same-user process is using the worktree;
- preserve source/sensitive/unknown local material rather than deleting it;
- remove through `git worktree remove`, not blind `rm -rf`;
- never use worktree cleanup as authority to delete `LOCAL_COURTS`, raw-source estates, user documents, or shared toolchains.

A returned/reviewed worktree must not remain indefinitely merely because it contains disposable caches such as `__pycache__`, `*.pyc`, `.pytest_cache`, or `.DS_Store`. Those are cleanup residue, not preservation authority.

Future commissions must use a dedicated disposable worktree root rather than proliferating historical lane directories inside the canonical checkout.

**Sparse-by-default law:** checkout isolation and repository materialization are separate concerns. The default commissioned worktree is sparse and shares the canonical clone's Git object database. A worker should materialize only the files/directories required for its writes and runtime behavior. Historical/read-only evidence outside that set should normally be read from exact Git objects without checkout. A full working tree is exceptional and must be justified by a concrete behavioral dependency on full-tree materialization.

## Return and stop

Frozen candidate SHA, structured return, claims/limits, tests with exit codes, source operations, unresolved/unreached work, event to HQ. State failure preservation and retry law. A returned PASS is not adoption.

## Wake

Pass-wake, blocker effect, prerequisite dependencies and the exact authority still needed downstream. READY is not COMMISSIONED. All UNBOUND fields must be replaced and validated before launch.
