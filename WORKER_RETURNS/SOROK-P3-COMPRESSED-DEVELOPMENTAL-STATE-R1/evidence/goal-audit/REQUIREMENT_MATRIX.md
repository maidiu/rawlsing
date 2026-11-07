# P3 original-goal requirement → evidence matrix

**Audit cut:** `16275d03fc4724a694c48ed9d447c4eeadbe25f2`  
**Implementation cut:** `486d42a4aa5dcd449564b95567ae93b59c4679a4`  
**Protected start:** `c852d7516e23fcb6cf2215e9be7c5fa268503516`  
**Branch:** `agent/sorok-p3-goal-audit-20261107-r1`

**Status key**

- **DEMONSTRATED (A/H)** — actual author/HQ execution or durable artifact, not independent acceptance.
- **SCOPED INPUT** — independently reviewed design/ABI input only.
- **PARTIAL** — evidence exists but does not cover the exact original condition.
- **PENDING** — focused independent recheck or corrected execution still outstanding.
- **HOLD** — intentionally not issued; native/science/production authority withheld.

This audit did **not** rerun tests. It verified the current source hashes against the published
combined matrix and read the actual logs/receipts. It is delivery preparation, not
independent review or acceptance.

## 1. Objective sections

| Original requirement | Exact evidence | Status | Limits |
|---|---|---|---|
| §1 sparse, historically dense developmental state; real computational difference, not narrative | `p3/p3_owner.py`, `p3/state_store.py`, `p3/test_rules.py`; combined PRIMARY and A–H matrix; actual formation → two `V3MS_MEDIATOR` records → later `joint_check/private_check` response. `evidence/full-vertical-execution-combined/matrix_summary.json` | **DEMONSTRATED (A/H)** | Sourcefree TEST_ONLY; no native/human personhood. |
| §2 use P3-E1 and P3-S1 as scoped inputs | `E1_INPUT_DISPOSITION.json` (`ACCEPT_SCOPED_TEST_ONLY_B1_COMPATIBILITY_ABI_COST_INPUT`); `S1_INPUT_DISPOSITION.json` (`ACCEPT_SCOPED_TEST_ONLY_H1_H2_H3_DESIGN_INPUT`); E1 review `04f57e03…`, 9 passed; S1 review `7466d37b…` | **SCOPED INPUT** | S1 explicitly did not accept A–E implementation, native science, economy or human validity. |
| §3 preserve settled recursion, #704 and #697/P2; follow P3 sourcepack | `INTEGRATION_CONTRACT.md`; `SOROK_PRODUCT_CONTROL_ROOM/.../P3_RULEBOUND_DEVELOPMENT_SOURCEPACK_R1/00_READ_FIRST.md`; current S39–S47/P2 source paths and hashes in `evidence/inherited-regression/PROTECTED_PINS.json`; engine 71-test suite `71 passed in 286.10s`; cold CLI `cold_verified=true` | **DEMONSTRATED (A/H)** | No new engine; no native law or production adoption. |
| §4 startup/protected/review intake | Current branch starts at evidence cut, protected `c852d751…`; E1 and S1 independent scoped dispositions; final runtime reviewer is distinct nonauthor | **DEMONSTRATED / INPUT REVIEWS** | Current focused recheck of the repaired cut is still pending. |
| §5 P2-root psychological state: typed sparse records, exact root/actor/branch, rule/source/version, causal parents, recoverable transitions, replay/idempotency, wrong-root denial, state hash, cold reopen, later reader | `p3/state_store.py` (normalized SQLite, immutable records, PREPARED→WORLD_COMMITTED→PSYCH_COMMITTED→COMPLETE, CAS/head, lossless kinds/hashes); `p3/p3_owner.py` (composition over unchanged P2Owner, exact root/config, crash recovery); `evidence/storage-abi-repair/`, `evidence/storage/`, `evidence/owner-actual-store-repair/`, combined cold/crash/resource cases | **DEMONSTRATED (A/H)** | M1/M2 repairs are actual at this cut but independent focused recheck is pending. |
| §6 TEST_ONLY rule adapter and later consumer; frozen registry; production positive registry untouched; actual mediator persistence and computed later response; control; source severance | `p3/test_rules.py` exact B1 `mode_for` source hash `478b9897…`; source-bound registry and rules; `tests/test_rules.py:108` exact source severance/restore; combined PRIMARY formation/recruit; `test_rules.production_guard()` in primary | **DEMONSTRATED (A/H) for positive/deny; PARTIAL control** | Official primary control is `history_outcomes=()` (`test_p3_vertical_slice.py:62`), not a same-history/no-record control. A prior d1a diagnostic demonstrated same-history FORMATION vs STABILITY, but it is not the current combined matrix. Source severance is unit-level, not an actual P2 chain execution. |
| §7 compression evidence: actual event, representative episode, accumulated interval, retrospective crystallization; no fabricated acts/multiplier; sidecar only | `p3/compression.py`; `test_f_four_actual_compression_forms_bind_without_fabricated_history` PASS; actual forms `SINGULAR_OCCURRENCE`, `REPRESENTATIVE_EPISODE`, `ACCUMULATED_INTERVAL`, `RETROSPECTIVE_CRYSTALLIZATION`; source/event/window/actor-access checks; unit compression tests | **DEMONSTRATED (A/H)** | TEST_ONLY evidence only; no native memory/claim. |
| §8 conditional activation, plural streams, contradiction, no scalar winner/lifecycle, material versus psychological eligibility | `p3/projections.py` pure `activate`; D PASS (`CONTRADICTION`, two records, no lifecycle); C PASS (same history, two standpoints, same actor); E PASS (stability, no new record); material values read from actual P2 C9 | **DEMONSTRATED (A/H)** | TEST_ONLY read-time activation; no CAN-011 lifecycle. |
| §9 actor/user/objective opacity; no complete ledger; no ADP016/017 without authority; renderer not writer | `project_views`; G PASS (no ledger sentinels; `memory_formation=MISSING_RULE`; `claims_status=DEFER_MISSING_AUTHORITY`); owner `accessible` is actual actor projection; user surface only in `test_only_user_surface` | **DEMONSTRATED (A/H)** | Claims/memory remain held; no native access grant. |
| §10 actual integrated acceptance: two 3–5-event batches, no per-event model calls, earlier state → later response on same P2 root, A–H, cold/crash/failure custody | `evidence/full-vertical-execution-combined/` 13/13 PASS at implementation `486d42a4…`; case logs all `PASS`, `run_matrix.sh`; actual resource case; `evidence/inherited-regression/` 71 passed/286.10s and cold witness | **DEMONSTRATED (A/H) / PARTIAL requirements** | See A–H and known gaps below. |
| §11 measured resource economy: bytes/actor/event/record, targeted vs full reads, context bytes, per-event/batch latency, cold reopen, calls/batch, provenance | `evidence/full-vertical-execution-combined/metrics/resource.json`: 2 batches `[3,3]`, 3 provider calls, 2 retrospectives, 6 event latencies, batch latencies, cold `10.754s`, DB `4096`, WAL `1,536,792`, DB+WAL `1,540,888`, incremental DB+WAL `1,483,200`, bytes/record `741,600`, bytes/event `247,200`, context `4,359`, 6 targeted queries, 1 full verify scan, 9 full-verify row reads | **DEMONSTRATED (A/H)** | Single runtime measurement; no universal performance threshold. |
| §12 scientific/source limits: no native CAN/ADP/O07/ADP016/017/CAN010/independent B/Pyat/N11/N12/C4/C8/C9/C12/human/production | `p3/test_rules.py` `MISSING_RULE`, `production_guard` DENY; `p3/projections.py` claims DEFER; `p3/compression.py` no memory/claim issuance; evidence `final-independent-review` holds; no source/native merge | **HOLD** | Explicitly not a claim of native psychology or human validity. |
| §13 delegation/economy: existing engine, no new engine, bounded sources | `INTEGRATION_CONTRACT`; unchanged S39–S47/P2; current source pins; reuse ledger; no additional engine/scheduler in integrated code | **DEMONSTRATED (A/H)** | B3A/HQ300/M01 are not promoted as owners; see reuse section. |
| §14 independent exact-SHA review before receiving; no self-merge | Prior independent reviewer `final-independent-review/00_RETURN.md` at `d1a681…` returned **REVISE/CONDITIONAL** for M1–M3 and harness/fixture defects; current repairs are in `final-review-repair/M1_M2_REPAIR.json` and combined matrix; focused nonauthor recheck at `16275d03…` is live/pending (`CHECKPOINT.json`) | **PENDING** | No independent acceptance of repaired cut; no PR/merge. |
| §15 full deliverable | See `DELIVERY_DRAFT.md`; source pins in `SOURCE_PINS.json`; evidence in this directory | **DRAFT / NOT ACCEPTED** | Must not be represented as complete or received. |

## 2. A–H counterfactual map

| Case | Exact current test/evidence | Status | Exact limitation |
|---|---|---|---|
| PRIMARY | `test_primary_actual_formation_read_later_and_no_mediator_control` PASS; 3+3 events, formation 2 records, recruit response, 3 provider calls, no between-event calls; combined log | **PASS / PARTIAL control** | Control uses no history (`history_outcomes=()`), not same-history/no-record. |
| A historical difference | `test_a_two_histories_change_later_move_without_demographic_labels` PASS; recognized vs imposed histories; actual record hashes differ; same source hash/actor/root | **PASS (A/H)** | Test fixture, not natural history. |
| B material difference | `test_b_actual_material_opportunity_changes_without_psych_mutation` PASS; actual vs `SCHEDULED_ONLY`; C9 material eligibility and response read independently | **PASS (A/H)** | Controlled fixture; no universal material rule. |
| C interlocutor difference | `test_c_two_standpoints_same_history_without_mutation` PASS; same identity/history, two standpoints; actor surface unchanged; user surface differs | **PASS (A/H)** | Scoped read-only standpoint. |
| D contradiction | `test_d_incompatible_mediators_coexist_and_activate_without_resolution` PASS; two records, activation `CONTRADICTION`, no lifecycle/scalar winner | **PASS (A/H)** | TEST_ONLY sourcefree streams. |
| E ordinary stability | `test_e_stability_event_reveals_without_new_record` PASS; store head/records unchanged; response still computed; next before-state relation asserted | **PASS (A/H)** | No new record claim only. |
| F condensed event | `test_f_four_actual_compression_forms_bind_without_fabricated_history` PASS; all four supported forms bind to actual event/action/perception/interval receipts; no fabricated witnesses | **PASS (A/H)** | TEST_ONLY sourcefree compression evidence. |
| G asymmetric access | `test_g_actor_and_user_views_are_narrower_than_objective_state` PASS; no ledger/private sentinels; actor observed; user claims deferred; objective public view larger | **PASS (A/H)** | No native memory/claim. |
| H failure/custody | identity/time/source/rule denial PASS; cold reopen/replay/config restore PASS; real child crash/recovery PASS; independent root/fork `test_h_cross_root_binding…` PASS | **PASS except true foreign root/fork** | H cross-root test explicitly uses **deterministic replicas with the same root hash** (`test_p3_vertical_slice.py:456-458`) and checks mutated foreign source refs, not an actual independent root/fork migration boundary. Actual source severance/restore is unit-level (`test_rules.py:108`), not a P2 chain case. |

## 3. Reused / declined capital

| Capital | Actual disposition |
|---|---|
| B1 | Exact recovered `mode_for`/scoped mediator semantics are selectively imported under the TEST_ONLY registry (`p3/test_rules.py`; source hash `478b9897…`). B1's isolated child/root store is **not** the P3 root and is not reused as the actor store. |
| P2/S39–S47 | Existing accepted P2/S47 chain reused; 71-test engine suite passes; exact source pins in `evidence/inherited-regression/PROTECTED_PINS.json`. |
| B3A | Sourcefree SQL/readset precedent retained; not adopted as an owner or independently re-executed on the P3 root in this cut. No B3A native claim. |
| HQ300 | In-memory ADP016/ADP017/chain candidate; not a durable P2 owner; not adopted; native memory/claims remain HOLD. |
| M01 | Original V3 `BackboneState`/yearly/render candidate; exact archive bytes unavailable/mismatched; reuse ledger marks it HOLD; no adapter or execution. |
| M25/M29/V3 | Exact historical archive/state closure unavailable/mismatched; not adopted. |
| BP2P4J, S48–S52 | Sourcefree candidates retained; not silently adopted; S48's one-item turn and S50's absent historical B context were declined for this bounded P3 scope. |

## 4. Exact gaps and required disposition

1. **Same-history no-record control — PARTIAL.** The official primary control at
   `tests/test_p3_vertical_slice.py:62` uses `history_outcomes=()` (no history).
   The prior nonauthor diagnostic at `evidence/final-independent-review/reproductions/same_history_control.py`
   showed FORMATION→2 records→`joint_check/private_check` versus
   STABILITY→0 records→`inspect_alone`, but it is not an independent execution at
   the current `16275d03…` cut and is not one of the 13 matrix cases. This is an
   original §6/§10 control premise, not a new gate.
2. **True foreign root/fork — PARTIAL.** `test_h_cross_root_binding_is_refused_not_migrated`
   asserts that left/right are deterministic replicas with the same logical root
   hash and tests mutated foreign source fields. It does not instantiate a truly
   different actual P2 root/fork and prove refusal/non-migration. Original §10H
   asks for independent roots/forks.
3. **Source severance/restore in the actual P3 chain — UNIT-ONLY.** Exact B1 source
   severance/restore is proven in `tests/test_rules.py:108`; the 13 matrix contains
   no actual P2 source-severance/restore case. This is weaker than an actual
   producer→store→reader source fault test.
4. **Independent focused recheck — PENDING.** The earlier independent review
   (`d1a681…`) returned REVISE/CONDITIONAL. Current M1/M2/M3 repairs are actual and
   full13 is green, but the focused nonauthor recheck at `16275d03…` is the
   acceptance dependency. No independent acceptance or PR is claimed.

## 5. Actual source verification

Current files match the published matrix source hashes:

| Path | SHA-256 |
|---|---|
| `p3/p3_owner.py` | `e735ada798533a8f568739e823767bb2e2b4272c3c03d84dc2cd47f73cf65df1` |
| `p3/state_store.py` | `173d4d6d3e94580804cac90039a01bfe6e3adfffcda9e806a56132b10ecc06bf` |
| `p3/compression.py` | `49df70d60cbc3b37ec3e484c5a7c64e14ac174faafe8fcaa02e5428c583be4f4` |
| `p3/test_rules.py` | `27272cd43c26b6aa114ee65c97ca07eb56accecbd440841c29696b98e203b4b4` |
| `p3/projections.py` | `ca405dda778191537ce38b0b63ff6b6ba8104dcd1ea676d6b458d454b362005b` |
| `run_p3_vertical_slice.py` | `1a895a4b68ae190679827197d2c58591afd0985c3ee30387bba1432b8d145462` |
| `tests/p3_fixture_support.py` | `7c3490178921c0765c8dfd42c9fb3f39d0c4696d2d048340094d746120b958eb` |
| `tests/test_p3_vertical_slice.py` | `0501754503a2af007154494654ed7f1edf5957e91ae56892949392f51b39c7ff` |
| `tests/test_p3_owner.py` | `40ac01033ab367d601a6ddcd43bd913928fc5933a26b3c734697376816aeafe1` |
| `tests/test_state_store.py` | `03429d6d1803ed2c5d0a4038d2a7d529b375c33b7d43a41bf9fb9e44abdc8344` |

The combined matrix source hashes match the current files above for every file it
names. `matrix_summary.json` commit is `486d42a4…`; current evidence cut
`16275d03…` is a descendant. All thirteen case logs are `status=PASS`,
`exit=0`.

## 6. Audit execution boundary

No tests, fixtures, source, checkpoint, PROGRAMMA, production registry, or
accepted engine files were modified by this audit. This is a documentation-only
return; it does not rerun the matrix and does not convert author/HQ evidence into
independent acceptance.
