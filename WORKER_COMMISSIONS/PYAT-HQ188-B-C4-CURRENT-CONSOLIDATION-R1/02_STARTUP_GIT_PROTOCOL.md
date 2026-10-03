# HQ188-B — mandatory GitHub startup protocol

This addendum is part of the worker commission.

## Authoritative startup law

The authoritative commission lives on GitHub. Do **not** assume a local checkout, local branch, remembered chat state, or local commission file is current.

Before any commissioned work:

1. Use an existing verified clone of `maidiu/rawlsing`, or create a fresh ordinary clone if needed.
2. Run `git fetch origin` (or the equivalent explicit fetch). Do **not** use a blind `git pull` that may merge or rebase local state.
3. Resolve `origin/agent/rabochii-pyat-hq188-b-c4-current-consolidation-r1`.
4. Treat the exact remote branch tip supplied in the HQ launch directive / current dispatch record as the commissioned startup SHA.
5. Verify the fetched remote worker branch equals that exact SHA.
6. Read `00_COMMISSION.md`, `01_RETURN_PROTOCOL.md`, and this file directly from that exact fetched tip.
7. Create or reuse an isolated worktree for the worker branch at exactly that tip.
8. Verify before editing:
   - local HEAD == exact commissioned startup SHA;
   - `origin/agent/rabochii-pyat-hq188-b-c4-current-consolidation-r1` == exact commissioned startup SHA;
   - no unrelated uncommitted changes exist in the worktree.
9. Only then begin work.

If the remote branch tip differs from the supplied commissioned startup SHA, stop before editing and report the observed SHA to HQ. Do not guess, reset, merge, rebase, or force-push to make it fit.

## Ongoing branch law

- Work only on `agent/rabochii-pyat-hq188-b-c4-current-consolidation-r1`.
- Do not merge/rebase the control branch into the worker branch unless a later HQ commission explicitly authorizes it.
- Fetching is allowed for reading exact evidence refs required by the commission.
- Non-ancestor evidence may be fetched/read by exact ref without changing worker ancestry.
- Preserve the commission ancestry so HQ can compute commits-over-commission exactly.

## Return law

The separate `01_RETURN_PROTOCOL.md` is mandatory. A local-only completion is not returned to HQ. Final return requires a pushed GitHub worker branch and verified remote SHA.

Terminal startup token:
`HQ188-B_GITHUB_STARTUP_VERIFIED`
