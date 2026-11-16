# PYAT HQ209 — operating discipline and live worker-state correction — R1

Date: 2026-10-05

Status:
`HQ_OPERATING_DISCIPLINE_BOUND__DIRECT_REMOTE_STATE_TRUTH__SHARED_STORE_SPARSE_WORKTREES__USER_VISIBLE_JOB_IDENTITY_REQUIRED`

This is a **control-plane / operating-law decision**, not a new semantic PRE-V3 authority adoption.

## Holding

HQ binds the following as mandatory Pyat operating discipline:

1. **Direct origin branch HEAD is the remote-state source of truth.**
   Commission records, code-search results, and durable handoff prose may identify lanes but must not be used to infer whether a return has been pushed.

2. **Worker lifecycle vocabulary is exact.**
   - `NEW — NEEDS LAUNCH`
   - `EXISTING — ACTIVE / NOT YET RETURNED`
   - `RETURNED LOCALLY — PUSH REQUIRED`
   - `PUSHED — READY FOR HQ INTAKE`
   - `ADOPTED / CLOSED`

   `RETURNED LOCALLY — PUSH REQUIRED` requires explicit worker/session evidence of local terminal completion. An unchanged remote branch is insufficient.

3. **Every user-facing dispatch/status block must co-locate operational identity.**
   Prominently include AGENT, MODEL / INTELLIGENCE, MACHINE when known, WORKTREE when known, BRANCH, and exact commission/startup or return tip.

4. **Local concurrency uses shared Git objects, isolated worktrees.**
   Per machine: one canonical Rawlsing clone/object store; one isolated sparse worktree per concurrently active branch. Workers do not create a clone per job and do not share one checked-out working directory concurrently.

5. **Prepared worktrees are resumed, not recreated.**
   No clone, broad fetch, sparse-scope expansion, branch switching, merge, or rebase unless explicitly commissioned. Historical evidence outside sparse scope should use exact Git-object reads where practical.

6. **Return means pushed-and-verified, not merely locally complete.**
   Worker completion protocol is commit -> push commissioned branch only -> re-fetch/verify exact remote tip -> report exact SHA.

7. **HQ intake begins as soon as an orthogonal return is pushed.**
   Resolve exact tip, verify ancestry, inspect changed paths, read required return evidence, determine hostile-review requirement, then adjudicate. Do not wait for unrelated siblings.

8. **Handoff snapshots do not replace live reconciliation.**
   `CURRENT_HANDOFF.md` and immutable checkpoints preserve succession state. A fresh HQ must reconcile their named worker edges against direct origin HEADs before operational claims.

## Bound operating documents

- `PYAT_CONTROL_ROOM/SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md`
- `PYAT_CONTROL_ROOM/00_READ_ME_FIRST.md`
- `PYAT_CONTROL_ROOM/13_FRESH_HQ_FULL_GROK_PROTOCOL.md`
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/HQ_START_HERE.md`
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/README.md`
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/CURRENT_HANDOFF.md`

## Live transport-state correction at decision time

Direct origin resolution:

- F7 hostile review — **PUSHED / READY FOR HQ INTAKE**
  - AGENT: DeepSeek Harness
  - MODEL / INTELLIGENCE: **DeepSeek V4.1 Flash**
  - branch: `agent/reviewer-pyat-hq208-f7-temporal-contract-r1`
  - return: `f1a0dbbc8491e0d23df9005abd55b83e0261424e`

- H-D/F8 rereconciliation — **PUSHED / READY FOR HQ INTAKE**
  - AGENT: Browser/GitHub documentary worker
  - MODEL / INTELLIGENCE: **GPT-5.6 Sol High**
  - branch: `agent/rabochii-pyat-hq208-hd-f8-rereconciliation-r1`
  - return: `6e2649c4d111fd0ec176c9fa29ce1da27ccc448e`

- V556 repair — **PUSHED / READY FOR HQ INTAKE**
  - AGENT: Space Bunny
  - MODEL / INTELLIGENCE: **Space Bunny Max**
  - branch: `agent/rabochii-pyat-hq206-v556-repair-r1`
  - return: `3a2dcafe024b2556af1df909deb5452841e45b7c`
  - mandatory final hostile independent review remains required before adoption.

- R9 repair — **EXISTING / ACTIVE / NOT YET RETURNED**
  - AGENT: Space Bunny
  - MODEL / INTELLIGENCE: **Space Bunny High**
  - branch: `agent/rabochii-pyat-hq207-r9-repair-r1`
  - remote: `70ca48345d97f26ac1d7061df2138ab3f14c474c`

- C1 prune — **EXISTING / ACTIVE / NOT YET RETURNED**
  - AGENT: Space Bunny
  - MODEL / INTELLIGENCE: **Space Bunny High**
  - branch: `agent/rabochii-pyat-hq206-c1-prune-r1`
  - remote: `32d86985b8af3f2ee175f5a170ee21c7101785b6`

No semantic adoption is performed by this control-plane decision.

Existing service-source authority ceiling, F8 law, hard holds, and no-Astra status remain unchanged.

Terminal:

`PYAT_HQ209_OPERATING_DISCIPLINE_BOUND__LIVE_WORKER_STATE_CORRECTED`
