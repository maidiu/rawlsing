# Final-runtime review — detailed findings

**Reviewcut:** `d1a6817b3210880812f68090bcd2b1109ec68ef9`
**Protected start:** `c852d7516e23fcb6cf2215e9be7c5fa268503516`
**Review branch:** `review/sorok-p3-final-runtime-20261106-r1`
**Review evidence:** `WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/evidence/final-independent-review/`

I reviewed the frozen P3 runtime source and actual test/fixture code, then executed the meaningful owner/store/unit suites, the resource case, the primary and stability cases, cold/crash/denial cases, and B/D/F/G cases from the exact test definitions in a `git archive` scratch copy. The scratch had **no runtime/test edits**; diagnostic probes only imported exact modules. No runtime, test, fixture, production, accepted-source or PROGRAMMA file was edited in the review branch.

## 1. Source identity and execution

Runtime hashes at the reviewcut:

```
p3/__init__.py                 873181592c5ef91fc9ad1c1db46b2a2f8e424bff46b2c454992fd39ca5827653
p3/compression.py              49df70d60cbc3b37ec3e484c5a7c64e14ac174faafe8fcaa02e5428c583be4f4
p3/p3_owner.py                 b7b508637258907e4d18df3030b45e040fff83dc6adc992985922e50a9e009f7
p3/projections.py              ca405dda778191537ce38b0b63ff6b6ba8104dcd1ea676d6b458d454b362005b
p3/state_store.py              76e5ee55fd8e5b4c9b0fefa48737644163c7794b687f4c0e342d0eba63eb252a
p3/test_rules.py               27272cd43c26b6aa114ee65c97ca07eb56accecbd440841c29696b98e203b4b4
tests/p3_fixture_support.py    5d2dfa081ae9152cbc3fc955d4f3aebebd5f1205f585bab07f655bdae57e550c
tests/test_p3_vertical_slice.py e969d30181d10879b3cd5b73260e2e52121646614c0582144d46232c178d1a1b
tests/test_p3_owner.py         4f627eba7ae61a8a670523f1e8ac612c14207649b21b4d93545405827475d660
tests/test_state_store.py      313a73fcdbb7e83dcf771f34a6f1fb6f420efed276a4e4996e6e34c9fb7a1e20
run_p3_vertical_slice.py       49450f2f8d40187aba956d0368b72ddc187f1261d13dc047e78ef834eb6f770f
```

The inherited P2Owner remains `fd98a757…`, engine `ba6caa74…`, contracts `9aabbc9f…`, model_cycle `af83f8f1…`. The exact `source-pin-check.json` is in `logs/`.

## 2. Actual executed evidence

| Test | Result |
|---|---|
| `tests/test_p3_owner.py` | **8 passed, 1 skipped in 31.41s** (missing-store guard skip; actual P2/P3 owner formation, later response/control, denial, replay, real child crash) |
| `tests/test_state_store.py` | **51 passed in 0.75s** |
| `tests/test_compression.py` + `test_projections.py` + `test_rules.py` | **36 passed in 8.89s** |
| `test_primary...` | **failed 448.23s at line 106**, after all formation/recruit/control assertions; final batch ID assertion wrong |
| `test_e...` | **failed 231.15s at line 271**, after stability response assertions; intermediate vs final state hash wrong |
| `test_h_cold...` | **failed 243.63s** at direct `owner.realize` after later batches: `P3_REPLAY_STATE_MISMATCH` |
| `test_h_real_process_crash...` | **failed 3.57s** at child `P2_ABSENT_OR_WRONG_SOURCE`; proposal list/tuple fixture |
| `test_b/test_d/test_f/test_g` | **3 failed, 1 passed in 1115.83s**: D passed; B line156 material, F line295 compression HELD, G line323 standpoint clock |
| `test_h_wrong_root...` / `test_h_cross_root...` | **1 passed, 1 failed in 9.63s**: identity/time passed; cross-root replica assumption failed |
| `test_11_resource...` | **passed 235.17s**, but per-record/event bytes 0.0 |
| Same-history diagnostic | FORMATION: 2 records → later `joint_check/private_check`; STABILITY: 0 records → later `inspect_alone` |
| Compression four-event diagnostic | SINGULAR BOUND, REPRESENTATIVE BOUND, ACCUMULATED HELD (`ACTUAL_INTERVAL_UNAVAILABLE`, interval NOT_PERFORMED), RETROSPECTIVE BOUND |
| Compression crash-boundary diagnostic | PSYCH_COMMITTED recovery completed without compression evidence |
| Store result-link diagnostic | forged result accepted; `verify()` True |

## 3. Runtime path actually demonstrated

The passing owner suite and primary core establish the valid actual-P2 chain at TEST_ONLY scope:

- Actual `P2Owner`/S47 root and actor; no independent B1 actor root.
- Formation event writes two `V3MS_MEDIATOR` records for recognized/imposed historical participation.
- Recruit event reads those exact records and computes `joint_check`/`private_check` streams; no native action is enacted (`native_action_performed=False`, `NOT_ISSUED_BY_P3_RULE`).
- A same-history control with formation suppressed (phase STABILITY) leaves the store head at count 0 and later computes `inspect_alone`.
- The owner suite exercises actual cold root reopen, idempotent immediate replay, wrong source/config/rule denial, and real child crash recovery.
- The store suite exercises schema/migration, lossless `V3MS_MEDIATOR/TENSION/PRACTICE` hashes, CAS/head, phases, and cold reopen.
- The resource chain runs two batches of three events, three provider calls, two retrospectives, no between-event model calls, and two P3 records.

This is meaningful producer→store→later-response evidence. It is **not** full P3 A–H acceptance because the frozen full13 is not green and the material findings below remain.

## 4. Material findings

### M1 — Durable result is not linked to its effects receipt (store integrity)

`p3/state_store.py:633` `_validate_result` accepts `result` without an effects receipt link. The checks at lines 669–674 only apply if the `consequences` object contains one of the three optional link keys. `p3/p3_owner.py:600-620` builds `consequences` without any such key; `receipt_ref` is only `P3_PSYCH:<response hash>`.

Independent probe (`logs/store-result-link-gap.log`) reserved/saved/committed an operation, then passed a result with:

- no `effects_receipt_hash`;
- `receipt_ref = "P3:forged"`;
- `accessible = {"forged_actor_surface": True}`.

`store.finish` accepted it, set phase `COMPLETE`, and `store.verify()` returned True. This defeats the promised immutable result/durable-receipt linkage after `PSYCH_COMMITTED`; a caller can replace the actor-visible result and receipt reference, and integrity verification still passes.

**Minimal fix:** P3Owner include `effects_receipt_hash` (or the full effects receipt) in `consequences`; `PsycheStore.finish` require it, verify against the stored effects receipt/response hash and `receipt_ref`, and add an omitted-link negative test. No new theory or gate.

### M2 — Compression evidence can be lost after `PSYCH_COMMITTED`

`p3/p3_owner.py:543-591` `_effect` calls `store.commit_effects` first and then `compression.bind`. The compression envelope is not stored in the effects receipt. On the `PSYCH_COMMITTED` recovery path, `_existing_effect` returns the stored receipt; `_psych_result`/`_result` therefore cannot include compression evidence.

Independent probe (`logs/compression-crash-gap.log`) injected `compression.bind` failure after the effect commit:

```
first exception RuntimeError INJECTED_COMPRESSION_BIND_FAILURE
phase after failure PSYCH_COMMITTED
recovered status REALIZED compression evidence? False
operation phase COMPLETE
```

A crash or exception at that boundary can complete a compression-designated event without its required evidence, silently dropping the evidence exactly where the system is supposed to preserve durable causality.

**Minimal fix:** compute the deterministic compression envelope before `commit_effects` and persist it in the receipt/response, or recompute it on `PSYCH_COMMITTED` and verify its hash before `finish`; add the exact crash-boundary test. Do not fabricate intervals, participants or acts.

### M3 — Resource per-record/event bytes are not actual

`tests/p3_fixture_support.py:477-525` computes `bytes_per_record` and `bytes_per_event` from `db_bytes` only. The actual resource test (`logs/actual-metrics.json`) reports:

```
db_bytes = 4,096
wal_bytes = 1,413,192
db_plus_wal_bytes = 1,417,288
incremental_db_bytes = 0
bytes_per_record = 0.0
bytes_per_event = 0.0
```

The test passes because it asserts only `bytes_per_record is not None`. The §11 storage-cost requirement is not met by the named metric; the WAL holds the actual state.

**Minimal fix:** use DB+WAL/incremental bytes (or checkpoint before measurement), assert positive per-record/event values, and retain main/WAL separately. This is measurement repair, not a new performance gate.

## 5. Frozen full13 test/fixture defects

These failures are exact in the frozen source. Most are not evidence of missing runtime psychology; they are test/fixture errors that must be repaired, not weakened.

| Test (line) | Observed | Correct minimal repair |
|---|---|---|
| Primary 106 | `final["batch_id"] != second["batch_id"]`; both `batch-000002` | `finish` returns the terminal retrospective for the same pending batch; assert equality or validate retrospective/history hash |
| Primary 61/118 | Control `history_outcomes=()` has no history, not just no record | Hold history fixed and suppress formation/records; my same-history probe gives the correct contrast |
| E 271 | Intermediate stability state hash compared to final owner snapshot after later batches | Capture post-bootstrap snapshot or compare stability record/head |
| Cold 441 | Direct `owner.realize` of completed first operation after later batches demands current-head replay | Use engine history/exact #704 replay semantics; runtime’s refusal is correct |
| Crash 509 | Child `EventProposal(**p["proposal"])` leaves lists for `source_refs`/`participants` | Normalize to tuples as the passing owner crash child does |
| A 131 | `recognized.owner.initial` does not exist on P3Owner | Use `VerticalCase.initial`; source-inspected, not independently executed |
| B 156 | Scheduled event after prior ACTUAL intervals has material_eligible False | Vary legitimate actual material opportunity with fixed psych history; material feasibility is P2-grounded |
| C/G 190/323 | Standpoints built at initial clock passed with later event identity | Update standpoint clock/hash (as `P3Owner._standpoint` does) or build at that clock |
| F 295 | Event-3 interval NOT_PERFORMED; compression correctly HELD | Use actual positive interval/event with material/access; do not force BOUND |
| H cross-root 419 | Left/right `build_case` share default logical root hash; replica not foreign | Construct a truly foreign root or test the replica explicitly; no migrated positive fork |
| Resource test | Passes with zero per-record/event bytes | Assert positive DB+WAL/checkpoint metric |

The author lane is separately repairing these harness defects. This review does not edit them; a corrected exact cut requires a focused recheck.

## 6. Resource and counterfactual disposition

Actual two-batch resource case (TEST_ONLY):

- provider calls 3 / modes BOOTSTRAP, ORDINARY, TERMINAL; batches 3+3; retrospective count 2; no per-event model calls;
- provider context 4,359 bytes; P3 head count 2;
- event latency 1.957, 7.342, 16.487, 24.386, 31.633, 41.283 s;
- batch latency 36.705 s bootstrap, 168.553 s ordinary, 17.271 s terminal; cold open 10.724 s;
- store: 6 targeted queries, 9 full-verify row reads, 161 row reads, 27 row writes, 1 full scan;
- DB 4,096 B + WAL 1,413,192 B; per-record/event metrics invalid (M3).

The same-history FORMATION vs STABILITY probe is the correct contrast for the persisted record effect: formation store head count 2 → later `joint_check/private_check`; stability head count 0 → later `inspect_alone`. The official primary control uses no history and is confounded.

D (contradictory mediators) passed in the B/D/F/G group. Unit projection/activation/rules tests passed 36/36. The actual G/C failure is a stale standpoint clock, not a projection leak; `P3Owner._project` adjusts the standpoint and the owner suite checks the user surface. F's actual failure is the fixture's NOT_PERFORMED interval; compression correctly returns HELD. B's failure is the fixture assuming an interval label changes material feasibility.

## 7. What remains unproven / not run

- Full13 A–H at the frozen cut is not green; the complete author matrix/metrics are not present in the frozen startup. The separate author lane’s later claims are not this review’s execution evidence.
- A/C were source-inspected, not independently executed.
- The corrected exact cut (after harness repairs and M1/M2/M3 fixes) has not been reviewed.
- The actual same-history no-record control is a review diagnostic, not an official accepted test.
- No native CAN/ADP, ADP016/017 memory/claim, original actor/B, human validity, production registry, CAS or protected merge is claimed.

## 8. Commands / logs

All independent logs and reproductions are under `evidence/final-independent-review/logs/` and `reproductions/`:

```
pytest -q tests/test_p3_owner.py                     # 8 passed, 1 skipped
pytest -q tests/test_state_store.py                  # 51 passed
pytest -q tests/test_compression.py tests/test_projections.py tests/test_rules.py  # 36 passed
pytest -q tests/test_p3_vertical_slice.py::test_primary...  # fail line 106
pytest -q tests/test_p3_vertical_slice.py::test_e...        # fail line 271
pytest -q tests/test_p3_vertical_slice.py::test_h_cold...   # fail replay
pytest -q tests/test_p3_vertical_slice.py::test_h_real_process_crash... # fail fixture
pytest -q tests/test_p3_vertical_slice.py::test_b... test_d... test_f... test_g... # D pass, B/F/G fail
pytest -q tests/test_p3_vertical_slice.py::test_h_wrong... test_h_cross_root... # identity pass, cross-root fail
P3_VERTICAL_METRICS_PATH=... pytest -q tests/test_p3_vertical_slice.py::test_11... # pass, metric defect
custom same-history/compression/store-link probes
```

No reviewed runtime/test file was edited. The scratch diff is empty; diagnostic probes and logs are preserved.
