# SOROK P3 selective receiving preparation — return

Status: **BOUNDED RECEIVING PREPARATION COMPLETE / ACCEPTANCE PENDING / NO PR CREATED**.

This is documentation and integration preparation only. It is not independent acceptance, not protected receiving, not a merge, and not a substitute for the live nonauthor focused recheck.

## Exact pins

| Item | Exact identity |
|---|---|
| Protected PRE-MAIN receiving ref | `integration/pre-main-reconciliation-r1` |
| Protected base commit | `c852d7516e23fcb6cf2215e9be7c5fa268503516` |
| Candidate source branch | `agent/sorok-p3-compressed-developmental-state-20261106-r1` |
| Candidate runtime/evidence cut | `16275d03fc4724a694c48ed9d447c4eeadbe25f2` |
| Implementation cut | `486d42a4aa5dcd449564b95567ae93b59c4679a4` |
| Goal-audit cut | `140b585f9b7321984725cf6f38ae95c2cb2bf89c` (`agent/sorok-p3-goal-audit-20261107-r1`) |
| Additive residual-proof cut / selection tip | `036787c1f0c227cdc47828ba521a62b76c57a903` (`agent/sorok-p3-goal-residual-proof-20261107-r1`) |
| Candidate delta | 32 commits, 305 paths from protected base; runtime source unchanged from `16275d03` |
| Proposed receiving branch label | `codex/sorok-p3-selective-receiving-20261107-r1` (not created) |
| Acceptance | `PENDING_EXACT_TARGET_RECHECK_AND_ADDITIVE_RESIDUAL_QUALIFICATION` |
| Protected receiving/merge | `PENDING` / not performed |

`origin/main` is `25830fe7462bb9e29bc4087e6ae14f3f84cec377`, an older ancestor, and is **not** the P3 receiving base. The live protected PRE-MAIN ref is the `integration/pre-main-reconciliation-r1` ref at `c852d751`.

Remote observation from the exact prep worktree:

```text
16275d03fc4724a694c48ed9d447c4eeadbe25f2  refs/heads/agent/sorok-p3-compressed-developmental-state-20261106-r1
140b585f9b7321984725cf6f38ae95c2cb2bf89c  refs/heads/agent/sorok-p3-goal-audit-20261107-r1
036787c1f0c227cdc47828ba521a62b76c57a903  refs/heads/agent/sorok-p3-goal-residual-proof-20261107-r1
c852d7516e23fcb6cf2215e9be7c5fa268503516  refs/heads/integration/pre-main-reconciliation-r1
```

The focused review is locally referenced at `review/sorok-p3-focused-recheck-20261107-r1` at the same `16275d03` cut. No remote review ref/result was observed or ingested; the review remains PENDING and gates PR publication.

## Selective inventory

Machine-readable inventory: `SELECTIVE_INVENTORY.json`.
Reproducible path list: `SELECTIVE_PATHS.txt`.

Counts:

- Candidate delta: **305** paths (292 runtime/evidence + 13 additive goal-audit/residual artifacts).
- Selected payload: **170** paths.
- Excluded: **135** paths, retained byte-identically on the candidate cuts.

Selected categories:

- 7 runtime files: `p3/__init__.py`, `compression.py`, `p3_owner.py`, `projections.py`, `state_store.py`, `test_rules.py`, `run_p3_vertical_slice.py`.
- 9 test/fixture files under `tests/`, including `tests/test_p3_goal_residuals.py`.
- 2 frozen contracts: `INTEGRATION_CONTRACT.md`, `ACTIVATION_OPACITY_CONTRACT.md`.
- 3 required E1 dependency/provenance files: E1 `00_RETURN.md`, E1 `probe/source_pin.json`, and exact vendored `probe/vendor/B1/bfirst.py`.
- 149 retained positive/negative/repair/evidence files under the selected `evidence/` directories, including the final combined matrix, inherited regressions, final independent review negatives, M1/M2 repair, goal audit, goal residual proofs, component owner/store/compression/projection/rule/vertical evidence and resource receipts.

Excluded and retained at the candidate cut (not deleted or rewritten):

- `SOROK_PRODUCT_CONTROL_ROOM` current progress/PROGRAMMA updates (5).
- P3 commissions/coordination/dispositions/mutable progress (26 + 16 + 4).
- Superseded pre-repair full-matrix logs (32).
- Provider-failure custody (3) and terminal-intake coordination (1).
- Intake logs/partials (7).
- E1 candidate return/probe files beyond the runtime dependency (13), E1 independent input review (16), S1 design return/review (12).

Rationale: the receiving PR should carry the runtime, fixtures, dependency and necessary accepting/negative evidence, not the campaign's mutable coordination or superseded partial logs. The excluded files remain exact and reachable on `16275d03`.

## Receiving instructions consulted

- `CROSS_HQ_CONTROL_ROOM/PROGRAMMA/02_CANONICAL_RECEIVING_AND_CODE_CAPITAL.md` at protected `c852d751`: canonical receiving branch is `integration/pre-main-reconciliation-r1`; worker completion is not publication; preserve source/code/negative evidence.
- `PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/RRIF_C3_E4F_SELECTIVE_RECEIVING_20261101.md` at protected `c852d751`: selective receiving uses an exact payload allowlist, exact base/source pins, explicit exclusions, receiving CAS and no protected mutation by the preparing worker.
- `WORKER_RETURNS/SOROK-PROGRAMMA-SELECTIVE-RECEIVING-20261105-R1/00_RETURN.md` at protected `c852d751`: Sorok selective PR preparation records exact base/source hashes, exact changed paths, PR-ready title/body and not-run boundaries; author does not create or merge the PR.
- No `.github/PULL_REQUEST_TEMPLATE.md` or separate root PR template was present; the existing selective-receiving return pattern above is used.

## Dependency check

Machine-readable result: `DEPENDENCY_CHECK.json`.

- Protected base already contains the accepted #704 recursion engine files (`contracts.py`, `engine.py`, `model_cycle.py`, `p2_owner.py`, runner), the S45–S47 projection package and the P2 product fanin package. Their base SHA-256 values match the E1 source pin where pinned.
- The P3 runtime's only missing source dependency is the exact E1 vendored B1 source:
  - path: `WORKER_RETURNS/SOROK-P3-E1-DEVELOPMENTAL-ABI-RECONNAISSANCE-R1/probe/vendor/B1/bfirst.py`
  - SHA-256: `478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3`
  - source pin: E1 `probe/source_pin.json` (`B1` commit `c0f4588c...`, blob `94ffc528...`).
  - It is absent at protected base and is included in the selective payload. This is the exact indispensable source dependency; it is not rewritten or repinned.
- S1 return/review is a design input cited by commit `5a505a91` / `7466d37b`; selected runtime/tests contain no S1 file import, so it is not a runtime dependency and is excluded from the receiving payload.
- No S1 runtime dependency, missing fixture, or cross-worktree private import was found.
- Selected runtime/test blobs at `16275d03` match implementation `486d42a4` exactly (15/15 checked files). The additive commits `140b585f` and `036787c1` add only the goal-audit/residual evidence and `tests/test_p3_goal_residuals.py`; they do not modify runtime source.
- The residual test's existing P2 dependencies (`P2ProductFanin.start(..., seed=...)`, encounter lifecycle, explicit interval flow and later-event continuation) are present at protected base; it imports selected `p3_fixture_support.py` and selected `tests/test_p3_owner.py`. No new runtime dependency is introduced.

## Published evidence and retained negatives

`CANDIDATE_SUMMARY.json` records exact evidence paths and hashes.

- Combined PRIMARY/A-H/resource matrix: **13/13 PASS**, 0 failed, at implementation `486d42a4`; evidence in `evidence/full-vertical-execution-combined/`.
- Inherited engine regression and cold-process compatibility: **71/71**, in `evidence/inherited-regression/`.
- Store/owner M1/M2 repair evidence: **61 passed, 1 skipped**; units **37 passed**; M3 resource metric repaired and matrix-green.
- Final independent review `1686c0b01e6b0b80738eaca89f31bab163fab36a` was **REVISE_CONDITIONAL_FULL_P3** with M1-M3. Its findings, reproductions and logs are retained in `evidence/final-independent-review/`; the repair evidence is in `evidence/final-review-repair/`.
- Goal audit `140b585f9b7321984725cf6f38ae95c2cb2bf89c` maps the original goal sections and records the exact remaining-author limits in `evidence/goal-audit/`.
- Residual proofs `036787c1f0c227cdc47828ba521a62b76c57a903`: **3 author tests passed in 27.14s**. They cover the matched source/history/later-objective-world formation-vs-stability contrast, genuinely distinct seeded P2 roots with foreign-source denial, and actual-chain B1 missing/altered/exact-restore replay. `tests/test_p3_goal_residuals.py` SHA-256 is `7fcd6c48a33b0aecb0f689149b235d714599b50d115f1272a7e06dd2b14260d8`.
- Residual limit retained: the same-history proof uses equal objective world, P2 identity/clock, source, history and later proposal, but the two independently initialized deterministic P2 fixtures have different full `state_hash`; an exact P2 root snapshot/fork/remap API is unavailable. This is not repaired or invented here.
- Resource receipt: 2 batches of 3 events, two retrospectives, 1.5 calls/batch, DB 4,096 B + WAL **1,536,792 B** = **1,540,888 B**; per-record 741,600 B, per-event 247,200 B.
- No test or full matrix was rerun by this preparation. These are published author/HQ receipts, not a new independent acceptance.

## PR package and branch construction

- Draft title/body: `PR_DRAFT.md`.
- Read-only inspection and proposed construction commands: `COMMANDS.md`.
- Exact selected paths: `SELECTIVE_PATHS.txt`.
- Exact remote pins: `REMOTE_PINS.txt`.
- No PR was created, no proposed receiving branch was created, no protected ref was moved, and no code/test/evidence/checkpoint/PROGRAMMA file was edited outside this new evidence directory.

## Remaining required dependency

The distinct nonauthor focused recheck of exact `16275d03` must complete and be ingested as accepted before HQ publishes the selective PR or performs protected receiving. The additive goal-audit and residual-proof artifacts from `140b585f` and `036787c1` also require nonauthor qualification; their author results are not acceptance. Preserve the exact same-history/full-state-hash limit and do not infer a new P2 fork architecture from opaque hash differences. If review fails, stop and repair the exact finding; do not substitute this preparation for acceptance.

## Holds

No native-science, original-human, actor-B, production, CAS, protected-receiving or merge authority is claimed. All prior source/native/science/memory/claim/B/human/production/CAS/protected/merge holds remain.
