# SYN02-C9-R3 — test-only actor SQL replay and status repair

**Branch:** `agent/sorok-syn02-c9-r3-testonly-idempotency-r1`
**Documentary HQ startup:** `6b31fd3b87f757f1a67b119068c6f8d4198f15f9`
**Role:** fresh independent sourcefree SQL engineering worker; not original RP0-R2 author, RRP0-R2 reviewer, C9/C12 storage owner, C8/SCI05 issuer, HQ, production editor or self-reviewer.
**Scope:** `SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_R2_REVIEW/R3/C9_SQL/` only. No S36/S37/r26e source edit; no C9/C12 production, issued science, owner freeze or F1.1 implementation.
**Evidence grade:** sourcefree local Python/SQLite/pytest; no native C8/C9/C11/C12/A5, real B/world, provider, survey or production DB.
**Outcome:** `C9_R3_TESTONLY_HELPER_REPAIRED__PASS_SCOPED__NOT_OWNER_FROZEN__F1_1_HELD__NO_NATIVE_GRANT`.

## 1. Delivered files

| File | Purpose |
|---|---|
| `schema_actor_r3.sql` | Provenance copy of RP0-R2 actor DDL with a held/final cross-axis CHECK; TEST_ONLY |
| `schema_mirror_r3.sql` | Provenance copy of the proposed C12 actor-mirror sidecar; TEST_ONLY |
| `c9_actor_r3.py` | Test-only actor helper for exact idempotent replay, status separation, requalification, CAS, outbox, mirror readiness |
| `c12_guard_r3.py` | Test-only C12 fork guard policy over actual JOIN-E C12 source; returns `FORK_HELD` on a perception-only suffix; no source edit |
| `tests/test_c9_actor_r3.py` | C9 actor helper tests |
| `tests/test_mirror_r3.py` | Unmirrored/ACK/mirror-held tests |
| `tests/test_c12_guard_r3.py` | Actual C12 clock-11 guard tests |
| `tests/test_s36_readset_r3.py` | Actual S36 seven-table readset unchanged test |
| `tests/conftest.py` | Import path only |
| `00_RETURN.md` | This return |

No RP0-R2 probe, S36/S37/r26e source, original DB, F0-R3 source, RM40 source or production file was edited.

## 2. Engineering repairs

### 2.1 Exact idempotent replay

`c9_actor_r3.publish()` checks `event_attempt.idempotency_key` inside `BEGIN IMMEDIATE` before inserting:

- same key + same request digest returns the exact original receipt, `seq`, version and head state; no new receipt, version, attempt or outbox row;
- same key + different digest raises typed `IDEMPOTENCY_PAYLOAD_CONFLICT` and rolls back;
- a finalized event cannot be finalized again (`EVENT_ALREADY_FINALIZED`);
- a new attempt requires a prior held attempt and a new attempt number; the prior held receipt remains immutable and the new attempt records `prior_attempt_id`.

Own tests: `test_same_key_same_digest_returns_exact_original_without_extra_rows`, `test_same_key_changed_digest_is_typed_conflict_without_mutation`, `test_finalized_event_cannot_rerun_rule_t`, `test_held_requalification_preserves_old_receipt_and_links_prior_attempt`.

### 2.2 Status axes and true nochange

`c9_actor_r3._status_axes()` and `schema_actor_r3.sql` reject:

- `HELD_MISSING_RULE` with `rule_t_status='COMMITTED_CHANGE'` (`STATUS_AXIS_CONFLICT`);
- final `COMMITTED_CHANGE`/`TRUE_NO_CHANGE_EVALUATED` without explicit `rule_t_hash` and `evaluated_readset_hash`;
- final SCI05 denied/held/integrity;
- final with a nonmatching Rule T status.

`TRUE_NO_CHANGE_EVALUATED` requires explicit test rule/readset and leaves `after_semantic_hash == before_semantic_hash`; it is never inferred from `NO_PROPOSAL` or `NO_EVENT`. `test_true_nochange_requires_explicit_rule_and_stays_semantically_equal` proves the positive and the missing-rule refusal.

World occurred + actor unseen is held, not converted to true nochange: `test_world_occurred_actor_unseen_is_held_not_true_nochange` stores `OCCURRED`, `NOT_PRESENT`, `NOT_WITNESSED`, `HELD_MISSING_RULE`, no result version.

### 2.3 CAS, target scope and rollback

`test_two_actors_same_local_target_and_stale_cas` proves two actors may share a legacy local target ID without collision; a stale expected head refuses. `test_two_connection_cas_loser_is_stale_not_duplicate` opens two SQLite connections, commits one, and proves the loser has no attempt/ghost. `test_rollback_leaves_no_ghost_version_receipt_or_outbox` fails a transaction after inserts and proves no actor version, receipt, attempt or outbox remains.

### 2.4 Outbox, mirror and C12 held

`tests/test_mirror_r3.py` proves:

- C9 commit with no mirror => outbox `PENDING`, `SYNC_HELD`/not ready;
- exact mirror receipt + CLEAN watermark => PROJECTED then ACKED idempotently, no new actor version;
- held watermark (`SYNC_HELD`) => never CLEAN;
- duplicate/wrong projection is refused by the helper path.

`tests/test_c12_guard_r3.py` imports actual `r26e.c12_integrity.QualifiedC12Store`/`bp4.store.C12Store` read-only. A parent with perception clocks 10 and 11 has no clean fork: `guard_fork()` returns `C12ForkHeld("C12_PERCEPTION_ONLY_SUFFIX")`; no child is created. A parent whose last perception is not beyond the non-perception cut can fork cleanly under this test-only guard. The real C12 source is not edited; the owner decision (patch or hard `FORK_HELD`) remains.

### 2.5 S36 seven-table preservation

`tests/test_s36_readset_r3.py` imports actual S36 at `S36_RETURN` and runs the targetless S36 path. It records the seven-table domain and old receipt, then creates a separate C9 actor DB and publishes a held receipt. Reopening S36 shows the same seven tables, the same old receipt row and no target rows. This is sourcefree and does not alter S36.

## 3. Test commands and results

### Full test run from C9_SQL

```text
cd SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_R2_REVIEW/R3/C9_SQL
S36_RETURN=<actual S36 return> \
JOIN_E_RETURN=<actual JOIN-E return> \
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp \
python3 -B -m pytest -q -p no:cacheprovider tests
```

Own result: **17 passed** (also **17 passed** from `/tmp` with absolute tests path).

Without optional external source environment: **14 passed, 3 skipped**; the skips are the actual C12 guard and S36 readset tests, not false passes.

### Exact source tests exercised

```text
S36 actual: 1 passed  tests/test_s36_readset_r3.py
C12 actual: 2 passed tests/test_c12_guard_r3.py
C9 helper: 12 passed
Mirror:     2 passed
TOTAL:     17 passed with external source env
```

The actual C12 source was read/imported from JOIN-E `7bf2da302996491ddf34b9a039fea47ac982d135`; actual S36 from `8da78d8031a06a4bd7e1297fd713e573299c0860`. No source edit.

## 4. C0–C7 coverage

| Cut | Result |
|---|---|
| C0 proposal only, no B act | `NOT_RUN`; no native world |
| C1 B acted, C8 ambiguous | `NOT_RUN`; C8 owner |
| C2 C8 committed, actor held | covered by held/unseen helper cases at sourcefree grain; no real C8 |
| C3 C9 transaction before commit | `test_rollback_leaves_no_ghost_version_receipt_or_outbox` |
| C4 C9 committed, no C12 mirror | `test_unmirrored_receipt_stays_sync_held_and_ack_is_idempotent` |
| C5 mirror before ACK | same test; ACK idempotent, no new version |
| C6 cold/fork stale/perception loss | `test_actual_perception_only_suffix_returns_fork_held`; helper returns `FORK_HELD`; actual C12 source untouched |
| C7 source/rule change on retry | `test_source_change_replay_is_exact_or_typed_conflict`; same digest exact, changed digest typed conflict |

C1/C2 real world and native C9/C12 remain **NOT_RUN**.

## 5. Source and schema identity

| Artifact | SHA-256 |
|---|---|
| `schema_actor_r3.sql` | `e89ba413ca0e8e0025f5864cccad2cb5d11a35dc769a95d0a09658b52e303db4` |
| `schema_mirror_r3.sql` | `ade6b213bd3e4c6de4665df2ec84bc62f14d968d88cfc46b67fba784c4cd8377` |
| `c9_actor_r3.py` | `2c22b8bfbba2399b20e8e19b4dc5cb35ca3437e9f0893f768be0453a9038cbb0` |
| `c12_guard_r3.py` | `62007798dd5229a4d30726407bc335a77225d643d50cac9b35d789e9d23cfbf3` |
| `tests/test_c9_actor_r3.py` | `abc7757ab1c4ca2f1dbc0068bce8b554cfc80d2327a7b6afa0c6e77359b37c36` |
| `tests/test_mirror_r3.py` | `09e085b3895829803e9c7bb06628218a82601c3a43f782ea8af433cc6bb7214b` |
| `tests/test_c12_guard_r3.py` | `743fe0fe83498cb42fcb3784e7595cd3a91a706813078e1e768b221903197fdf` |
| `tests/test_s36_readset_r3.py` | `56a1a0173ee90504a738cf0e85a71d3e17da516774bfc416c6524c80d668eec9` |

The actor schema is a provenance copy of RP0-R2 `schema_actor.sql` SHA-256 `05edec71...` with an added held/final `CHECK`. The mirror schema is a provenance copy of `schema_mirror.sql` SHA-256 `8b0e9f4c...`. Neither is owner-frozen or production.

Actual read-only source used by the guard/readset tests:

- C12 base `bp4/store.py` at JOIN-E `7bf2da3`: SHA-256 `bb7bd721...`, relevant lines 135–143 (`_last_clock` excludes perception), 323–367 (`fork`), 353–360 (root hash excludes perception).
- C12 verifier `r26e/c12_integrity.py`: SHA-256 `534780fe...`, lines 31–64 (row preimages, no branch-root/perception-cut check).
- S36 `candidate/transaction.py` at `8da78d8`: SHA-256 `d8d5d36f...`, lines 73–89 (seven tables), 115–126 (all-table readset), 288–292 (before snapshot), 362–370 (additive checks).

No S36/S37/r26e source was edited.

## 6. Three courts

**ENGINEERING — `ACCEPT_SCOPED_TESTONLY`.** The helper now passes exact replay, typed conflict, status-axis, requalification, CAS, target scope, rollback, outbox/mirror and actual-source C12/S36 tests at sourcefree grain. It is not a live C9/C12 implementation and not owner-freezable.

**SCIENCE — `HOLD / NO_CHANGE`.** No CAN008/CAN011 Rule A/T, SCI05 admission, memory/formation law, true-nochange law or native person is issued. Test rule hashes/readsets are test fixtures only.

**AUTHORITY — `HOLD / NO_NATIVE_GRANT`.** No C9/C12 storage-owner freeze, C8/world source, Pyat C11/C12/A5, provider account or production permission is granted. The actual C12 fork source remains owner-held; this return only proves a test-only guard policy and cannot replace the owner patch/guard.

## 7. Future consumer and owner gate

- **First actual future consumer:** C9 actor-aware E2 semantic read after an accepted C12/actor receipt; C12 fork/open/cold consumes the owner guard; C8 remains the independent world source.
- **C12 owner:** choose/qualify the perception-inclusive transactional patch or hard `FORK_HELD`; current actual C12 source is not clean.
- **C9 owner:** freeze actor schema/path, one writer, CAS/receipt/outbox/idempotency/status; this helper is not implementation.
- **C8/CAN/ADP/SCI05/product owners:** independent world/B receipt, Rule A/T, actor-safe memory, implicit-half2 hold and irreversible batch policy remain separate.
- **F1.1:** **not authorized.** A distinct bounded hostile technical review and competent owner adoption are required.

**Remote SHA:** verified after commit/push and reported in the handoff; not embedded here because self-embedding changes the commit. No self-adoption.
