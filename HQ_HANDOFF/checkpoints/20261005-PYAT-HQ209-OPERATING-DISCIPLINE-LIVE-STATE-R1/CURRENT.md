# Pyat HQ209 — operating discipline bound; live worker transport state corrected

Status:
`HQ_OPERATING_DISCIPLINE_BOUND__F7_HD_V556_PUSHED_PENDING_INTAKE__R9_C1_ACTIVE_NOT_RETURNED`

Decision:
`HQD-2026-10-05-209`

Decision record:
`PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ209_OPERATING_DISCIPLINE_AND_LIVE_STATE_CORRECTION_R1.md`

Semantic PRE-MAIN authority remains:
`1f47063c3205a45888b3c55e81e7485943ed1390`

Control-plane decision commit:
`4f4a531c3a28bbc1224ef678204489866ef1c09d`

## Binding operating discipline

- Direct origin branch HEAD is the remote worker-state source of truth.
- Durable handoffs are succession snapshots, not live branch oracles.
- Use only the five lifecycle labels:
  - NEW — NEEDS LAUNCH
  - EXISTING — ACTIVE / NOT YET RETURNED
  - RETURNED LOCALLY — PUSH REQUIRED
  - PUSHED — READY FOR HQ INTAKE
  - ADOPTED / CLOSED
- Never infer local completion from an unchanged remote branch.
- Every user-facing job block must prominently carry AGENT + MODEL / INTELLIGENCE + MACHINE/WORKTREE when known + BRANCH + exact startup/return tip.
- Per machine: one canonical Rawlsing clone/object store; one isolated sparse worktree per concurrent branch.
- No clone-per-worker, no shared checked-out directory between concurrent branches, no worktree recreation, no broad fetch/sparse expansion by default.
- Worker terminal return is commit -> push own branch -> re-fetch/verify -> exact SHA report.
- HQ intakes orthogonal pushed returns immediately rather than waiting for unrelated siblings.

Binding law:
`PYAT_CONTROL_ROOM/SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md`

## PUSHED — READY FOR HQ INTAKE

### F7 temporal contract hostile review
**AGENT:** DeepSeek Harness  
**MODEL / INTELLIGENCE:** **DeepSeek V4.1 Flash**  
**BRANCH:** `agent/reviewer-pyat-hq208-f7-temporal-contract-r1`  
**RETURN TIP:** `f1a0dbbc8491e0d23df9005abd55b83e0261424e`

### H-D / F8 rereconciliation
**AGENT:** Browser/GitHub documentary worker  
**MODEL / INTELLIGENCE:** **GPT-5.6 Sol High**  
**BRANCH:** `agent/rabochii-pyat-hq208-hd-f8-rereconciliation-r1`  
**RETURN TIP:** `6e2649c4d111fd0ec176c9fa29ce1da27ccc448e`

### V556 repair
**AGENT:** Space Bunny  
**MODEL / INTELLIGENCE:** **Space Bunny Max**  
**BRANCH:** `agent/rabochii-pyat-hq206-v556-repair-r1`  
**RETURN TIP:** `3a2dcafe024b2556af1df909deb5452841e45b7c`

V556 is semantic-sensitive production repair and requires final hostile independent review before adoption.

## EXISTING — ACTIVE / NOT YET RETURNED

### R9 repair
**AGENT:** Space Bunny  
**MODEL / INTELLIGENCE:** **Space Bunny High**  
**BRANCH:** `agent/rabochii-pyat-hq207-r9-repair-r1`  
**COMMISSION / REMOTE TIP:** `70ca48345d97f26ac1d7061df2138ab3f14c474c`

### C1 prune
**AGENT:** Space Bunny  
**MODEL / INTELLIGENCE:** **Space Bunny High**  
**BRANCH:** `agent/rabochii-pyat-hq206-c1-prune-r1`  
**COMMISSION / REMOTE TIP:** `32d86985b8af3f2ee175f5a170ee21c7101785b6`

Known local report: C1 is mid-work after an interrupted pre-prune baseline; resume existing worktree, rerun baseline cleanly, continue commission. Do not relaunch and do not merely instruct push.

## Semantic state unchanged

Service-source applicability remains adopted at source-free grain with ceiling:
`ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED`

F8 law:
`F8_DOES_NOT_TRANSFORM_POSSIBILITY_GEOMETRY`

Completeness wording:
`NO_BROAD_MISSING_ONTOLOGY_CURRENTLY_INDICATED__BOUNDED_AUTHORITY_IMPLEMENTATION_QUALIFICATION_RESIDUALS_REMAIN`

Hard holds remain:
- SOURCE_LOCATOR_DISCOVERY
- WARRANT_ISSUANCE
- RAW_SOURCE_ACCESS
- LIVE_C4
- C7_IMPLEMENTATION
- PREV3_TO_V3_ACTOR_IMPLEMENTATION
- HQ182_C4_NON_ADOPTION_HOLD
- HOST_DISK_POLICY_CAPACITY_LIVE_RUN_BLOCKER

No Astra referral.

Next lawful HQ action:
`INTAKE_F7_REVIEW__INTAKE_HD_RERECONCILIATION__INTAKE_V556_REPAIR_AND_BIND_FINAL_HOSTILE_REVIEW__CONTINUE_R9_C1_EXISTING_WORKERS`
