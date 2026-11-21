# SOROK CG-A owner reuse — bounded return

**Contract:** `SOROK-CG-A-OWNER-REUSE-COMPLETE`
**Author branch (local only):** `agent/sorok-cga-owner-reuse-selection-20261111-r1`
**Author cut:** `2be0cf252662ad021571db6f0d38b12c205c56ae` plus this return's uncommitted tree before the delivery commit
**Declared startup:** `1f77f2036427a410429184780ef884ec4f253ad0`
**Author ceiling:** `DELIVERED_PENDING_RECEIVING`
**Engineering verdict:** `SOURCE_EQUIVALENT_SOURCEFREE_REUSE_AND_COLD_LATER_READ_DEMONSTRATED__EXACT_DECLARED_STARTUP_IDENTITY_UNAVAILABLE__CG_BCD_MULTI_ACTOR_MATERIAL_ADAPTER_BUILD_HOLD`
**Science verdict:** `HOLD_NO_NATIVE_CAN_ADP_PYAT_ORIGINAL_ACTOR_ISSUANCE`
**Authority verdict:** `HOLD_NO_ACTOR_RIGHTS_NO_PROTECTED_MERGE_NO_PYAT_MUTATION`

## 1. Preflight and the one material deviation

The declared `STARTUP_SHA` `1f77f2036427a410429184780ef884ec4f253ad0` is not present in the local object database, any local ref, or the GitHub remote visible from this host. The visible GitHub API returns `404`; the configured HTTPS remote returns `403`; branch `agent/sorok-cga-owner-reuse-selection-20261111-r1` did not exist before this return. Reviews #874, #908, #860, #889 and #914 were not reachable and were not touched.

The declared source paths and blobs **do** exist locally at `2be0cf252662ad021571db6f0d38b12c205c56ae`. All four pinned blobs match exactly:

| Declared source | Pinned blob | Blob at `2be0cf25` | Result |
|---|---|---|---|
| `.../developmental_recursion/contracts.py` | `c4ce557cdb6d1e5ad8f3217e72d16a5a91c2a0e8` | `c4ce557cdb6d1e5ad8f3217e72d16a5a91c2a0e8` | exact |
| `.../developmental_recursion/p2_owner.py` | `3160eb157675453c0bfee5f9bd4b400f9c999c17` | `3160eb157675453c0bfee5f9bd4b400f9c999c17` | exact |
| `09_ALREADY_EXECUTED_DEVELOPMENTAL_CODE_AND_REVIEW_DELTA.md` | `c3cdc7c1e151cf3ece8159f7cc384b2359212e6c` | `c3cdc7c1e151cf3ece8159f7cc384b2359212e6c` | exact |
| `.../SOROK-P6-ONE-LIVING-HOUSE-R1/house.py` | `af556c143e7e4eaa2f60a68fa402954091737dd4` | `af556c143e7e4eaa2f60a68fa402954091737dd4` | exact |

The author therefore created an isolated local branch at `2be0cf25`, verified every declared source blob, and executed the source-equivalent obligations there. This is **not** a claim that `1f77...` was used. A receiver requiring the literal startup identity must treat the commit-identity portion as `INCOMPLETE`; a receiver accepting source-content equivalence may evaluate the evidence below. The author did not fabricate a commit, force a ref, or rewrite history.

Model/provider: the local harness identifies DeepSeek V4.1-Flash; MAX reasoning and host quota are not independently verifiable from this process. No provider call, browser, respondent read, Pyat mutation or protected merge was made.

## 2. What was executed

All commands ran in the isolated source-equivalent worktree with `python3 -B -m pytest -q -p no:cacheprovider`.

| Obligation | Evidence command | Result |
|---|---|---|
| `CGA-P3-ABI` | full engine suite | **71 passed** in 278.95 s |
| `CGA-POSITIVE-CAPITAL` | `tests/test_state_store.py` + `tests/test_rules.py` | **57 passed** in 0.63 s |
| `CGA-COLD-LATER-READ` | owned cold-later test `tests/test_cold_later_recruit.py` | **1 passed** in 247.70 s |
| `CGA-COLD-LATER-READ` | existing P3 owner cold/replay/source-restore test | **1 passed** in 280.92 s |
| `CGA-COLD-LATER-READ` | existing P3 formation→later-response/control test | **1 passed** in 445.72 s |
| negative court | wrong identity/source/rule/time, cross-root, real crash | **3 passed** in 14.03 s |
| material later reader | engine material/C9 and cold owner receipt tests | **2 passed** in 260.26 s |
| store ABI | selected common writer/readset `tests/test_selected_common_readset.py` | **3 passed** in 0.10 s |

Recorded executions: **146 passed, 0 failed** across the above commands (some tests are intentionally repeated in different commands; this is not a claim of 146 unique tests). Logs are under `evidence/`.

The frozen positive oracle was directly exercised by `tests/test_cold_later_recruit.py`:

1. bootstrap realizes a 3-event batch and the owner store holds two exact sourcefree formation records;
2. the owner/base is closed and reopened on the same root, actor, branch and clock lineage;
3. a later distinct `advance`/recruit decision reads the exact two record hashes, includes them in `readset`, and computes a sourcefree response;
4. `finish` completes the terminal retrospective;
5. a control without the formation records produces `inspect_alone`, and no new record is fabricated by the later recruit.

The existing engine tests additionally prove material interval→later C9 dependence and cold owner receipt survival. The existing P3 cold test proves exact replay and source severance/restore at the owner boundary.

## 3. Exact ABI answer

The generic engine ABI is `StateIdentity(root, actor, branch, clock, state_hash)` + `EventProposal` + `RealizedEvent` + `DevelopmentOwner.snapshot/validate_proposal/realize`, with `BatchEngine` and `RecursionCycle` as the only scheduler. The engine itself does not select an actor, participant tuple, source, operation or psychological rule.

`P2Owner` is a **local P2 adapter**, not the universal P3 root contract. It requires `participants == tuple(root["actor_ids"])`, chooses `self.actor = root["actor_ids"][0]`, accepts only `ADMIT_EVENT`, and limits intervals to `ACTUAL`/`SCHEDULED_ONLY` with a span that cannot cross the event clock.

`P3Owner` composes one `P2Owner` with one `PsycheStore` bound to the same single `(root, actor, branch)`. It adds frozen source/rule/plan/history validation, `PREPARED -> WORLD_COMMITTED -> PSYCH_COMMITTED -> COMPLETE`, and a later `_effect` readset via `PsycheStore.query(project, counterpart, as_of)`. It is the smallest current writer/readset that already satisfies exact identity, versioning, refusal, cold replay and later consumption for **one actor**.

The pinned P6 `house.py` is a real material/world resource reader (`establish`, `read_house`) bound to root, branch, source hash and epoch. It does not provide a dated home/period writer, a second independent actor, or a speech writer for anyone other than the existing actor path.

## 4. Selected common writer/readset

**Selected:** `P3Owner` + `PsycheStore`, with `BatchEngine`/`RecursionCycle` unchanged, and P6 `house.read_house` as the material reader.

- Writer: `PsycheStore.reserve` → `save_world` → `commit_effects` → `finish`.
- Readset: `PsycheStore.query(project, counterpart, as_of)` plus `P2Owner.snapshot()` and `house.read_house(session)`.
- Later consumers: `P3Owner._effect` for the sidecar; the next `RecursionCycle.advance` or later `P3Owner.realize`; P2/S47 `read_c9_conditioning` for native material/C9; P6 `situated.reconsider` for situated decision/speech.
- Version/refusal: store binding, registry hash, source hash, head, plan hash, rule version, causal parents, phase, receipt hash and exact replay are all enforced.
- No new scheduler, no parallel ledger, no new habitus store, no new gate ID.

The exact edge CG-B/C/D still need is **not** a replacement writer. It is a small multi-actor/material adapter around the selected writer. See `02_SELECTED_ABI_AND_CG_BCD_CONTRACT.md`.

## 5. Missing function cards

| ID | Missing function | Exact current evidence | Disposition |
|---|---|---|---|
| MFC-1 | `RootParticipantAdapter`: one root, non-fixed participant set, per-event focal actor | `p2_owner.py:45-47` requires exact `root["actor_ids"]` tuple and selects `[0]`; `PsycheStore` binding is one `(root, actor, branch)` | **BUILD**. Do not generalize P2 by silent mutation; add a root-level adapter that routes per-actor sidecars and returns a deterministic composite `StateIdentity`. |
| MFC-2 | `HomePeriodWriter/Reader`: dated material home/period | `house.py:151-165` writes `world.resources["p6_house"]` with `epoch` and object `history`; `read_house` at `206-228` verifies root/branch/source/epoch. No `from_clock/to_clock/home_ref/actors` period record | **ADAPT/BUILD**. Add a sourcefree `home_period` world resource; it is included in P2 `snapshot` material hash through `vars(s.world())`. |
| MFC-3 | Independent mother speech writer/reader | P6 `situated.py:35-49` reads only perceptions for actor `A`; `situated.py:222-227` calls `session.product.say(text, actor="A")`. No second-speaker admission | **BUILD**. Add a speaker-bound `SPEECH` admission using the existing P6/P2 event writer; do not substitute user view or model prose. |
| MFC-4 | `SidecarDecisionReadset`: a situated later decision that reads `PsycheStore` | `p3_owner.py:548-604` queries the sidecar only inside `P3Owner._effect`; `situated.py:134-230` builds a decision packet from world/house/actor state but never queries `PsycheStore` | **ADAPT**. Add a read-only query and a `readset` binding to the existing `situated.reconsider` packet; keep the single owner writer. |
| MFC-5 | `PW-01..12` named functional definitions | Not found in `PROGRAMMA_SOROK`, `WORKER_RETURNS`, `WORKER_COMMISSIONS`, or sourcepack 09 by exact `PW-01`/`PW-12` search | **NOT_LOCATED**. No definitions were invented. The twelve explicit mission functions are mapped in `02_SELECTED_ABI_AND_CG_BCD_CONTRACT.md`. |

## 6. Frozen negatives

| Negative | Status | Evidence |
|---|---|---|
| wrong root/actor/branch/clock | **PASS** refusal before effects | `test_h_wrong_root_actor_branch_time_source_rule_version_refuse_before_effects`; store `test_reopen_rejects_wrong_binding_registry_source_and_schema` |
| dynamic participant spoof | **PASS** refusal before effects | `p2_owner.py:84` exact participant tuple; store actor-local query |
| stale clock | **PASS** refusal | `P2_EVENT_CLOCK_NOT_FUTURE`, `BATCH_EVENT_TIMES_NOT_FORWARD`, store `STALE_PSYCHE_HEAD` |
| partial pre-refusal write | **PASS** rollback | store `test_one_bad_target_rolls_back_all_records`, `test_bad_record_targets_do_not_mutate` |
| double operation after crash | **PASS** | engine crash/idempotency tests; `test_h_real_process_crash_after_base_before_psych_commit` |
| model retrospective fabricated memory | **PASS** held/refused | engine `test_bootstrap_rejects_fictitious_memory`, `test_provider_mutation_is_held...` |
| omitted world readset | **PASS** refusal | store `test_commit_requires_world_then_commits_and_replays`; engine material/C9 tests |
| unadmitted hypothetical target | **PASS** refusal | store `test_bad_record_targets_do_not_mutate`; P3 plan/source/rule validation |
| MISSING_RULE misread as NO_CHANGE | **PASS** preserved | engine `test_held_and_missing_rule_are_preserved_and_never_become_no_change`; P3 response `MISSING_RULE` |
| source removal | **PASS** refusal/restore | `test_wrong_version_and_exact_source_severance_refuse_and_restore`; P3 cold test source restore |
| second independent actor | **NOT_RUN / BUILD HOLD** | no current function; MFC-1/MFC-3 |
| dated home/period | **NOT_RUN / BUILD HOLD** | no current function; MFC-2 |
| actual C9/E2 performed action after P3 response | **NOT_RUN** | P3 response is `NOT_ISSUED_BY_P3_RULE`; native E2 is not in this runtime |

## 7. What this return does not claim

- It does not claim the declared `1f77...` commit, branch or PR existed or was used.
- It does not claim a GitHub PR: push is blocked by remote `403`; the branch is local only.
- It does not claim native CAN008 Rule A, CAN011 Rule T, O05/O07/O15, ADP016/017, Pyat N9/N10W, C12, actor rights, respondent licence, human validity or production authority.
- It does not claim B1/B3A/HQ300/M01/C9RI are native science; their historical statuses and negatives remain.
- It does not claim CG-B/C/D are implemented; it selects the smallest ABI and identifies the exact missing adapter.

## 8. Receiving

The author result SHA is the commit created from this local branch after this file set is staged. A separate non-author exact-source reviewer must verify the frozen HEAD, the source pins, the cold command and the first-consumer behavior. No same-principal approval is claimed. Because the exact declared startup identity is unavailable, the receiver must choose either:

- `INCOMPLETE_EXACT_STARTUP_IDENTITY`, preserving the source-equivalent evidence as advisory; or
- `SOURCE_EQUIVALENT_RECEIVING`, explicitly accepting `2be0cf25` + the verified blob equality as the effective cut and recording the deviation.

The author does not select that disposition.
