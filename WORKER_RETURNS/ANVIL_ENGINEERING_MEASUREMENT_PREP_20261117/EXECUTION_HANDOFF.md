# CUT2 MEASUREMENT PREPARATION — EXECUTION HANDOFF

**Status:** `COMPLETE_MEASUREMENT_PREPARATION_NOT_EXECUTED_REALWIDTH`
**Product cut:** `347baec696c8b395d750ac3b9e74417a6490c223`
**Executable code/test commit:** `a13d69cf5636de5541660cd60115f8b61d66261b`
**Baseline:** `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`
**Runner:** `measure_cut1_prepared.py`
**Fixture contract:** `fixture_contract.json`
**Schema:** `MEASUREMENT_SCHEMA.json`
**Smoke evidence:** `evidence/smoke_evidence.json`
**Vendor source pins:** `VENDOR_PINS.json`
**Cut1 G5:** `ACCEPT_SCOPED_PREPARED_SAVED_BATCH_CUT1` at review `092bf29ffa6724d477abb4ccfc770e3bc492250d` against candidate `347baec696c8b395d750ac3b9e74417a6490c223`; sourcefree TEST_ONLY only; code blobs identical to `a13d69c`; no reviewer product changes. Tiny resources are not real width.
**Grade:** sourcefree TEST_ONLY mechanics. No native/original35/source/science/actor/protected acceptance. No 100k/6GiB/real-width/1-10-100 claim.

## 1. Exact cut and changed surface

The three cut1 blobs are identical at `a13d69c` and `347baec`; no other `rawlsing_next` file changed versus `cea2d4d`:

| Path | Git blob | SHA-256 |
|---|---|---|
| `rawlsing_next/pre553_saved_workload_integration.py` | `c568836b7ab1ce88224d4bc5c9de6dca8476a5db` | `54cf978db77cef25a2dc17a0006f63ef13ee13a65708d68d194403a6e7afafee` |
| `rawlsing_next/pre553_batch_runner.py` | `8320f28458fb85aec655d154a2527a161282f56b` | `e8c110ff3a18acec0956bb47c4789312dd49e812c0643875b7a3e13a13415ab1` |
| `rawlsing_next/tests/test_anvil_prepared_saved_batch_cut1.py` | `bf00eb591bdee1087e9a10085d808c1ed2aadf88` | `759a0912aa4bc799b67f68e4a7584412aece06275daaa32c8ac9178758c3371c` |

This harness reads those files and the accepted fixture instrumentation only; it edits no product/test/source/protected file. The existing `PreparedSavedC11Admission`/`PreparedI03Session`, native evaluators, issuer and writer are reused unchanged.

## 2. Runner contract

The runner is self-contained under this return root and vendors the exact pinned `fixture_1006.py`, `query_1006.py` and `court_instrumentation.py` (see `VENDOR_PINS.json`). It never uses a peer worktree, clone or new store.

Modes:

```bash
# deterministic tiny sourcefree fixture/estate (16 respondents, 5 questions)
python3 WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117/measure_cut1_prepared.py --mode prepare

# bounded geometry build (8 respondents, 600 question bindings; not economics)
python3 WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117/measure_cut1_prepared.py --mode prepare --questions 600 --respondents 8 --root WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117/.local-data-600

# one plain SavedC11Admission, one session per operation
python3 .../measure_cut1_prepared.py --mode baseline --out .../evidence/baseline.json

# one PreparedI03Session for the same distinct operations
python3 .../measure_cut1_prepared.py --mode prepared --out .../evidence/prepared.json

# actual cut1 execute_saved_batch, one prepared context for all units
python3 .../measure_cut1_prepared.py --mode batch --out .../evidence/batch.json

# fresh product-exited child process running prepared Batch
python3 .../measure_cut1_prepared.py --mode fresh

# one tiny mechanics smoke (baseline/prepared/batch/fresh) + parity
python3 .../measure_cut1_prepared.py --mode smoke --negatives
```

`--negatives` revokes CURRENT after the measured operations, requires refusal, restores the exact source, and rechecks the restored fact. It is not counted as a distinct operation.

## 3. H / S / Q / O separation

The runner separates the four requested measurable phases without changing math or the v1 ABI:

- **H — admission/member validation:** time `SavedC11Admission.open` / `PreparedSavedC11Admission.open`; temporarily wrap `pre553_source_direct_parquet_estate._hash` to count manifest/member hash calls and bytes. It includes `VerifiedDirectEstate` manifest/member hashing and count/topology checks; it excludes index build and query.
- **S — index build:** `CourtInstrumentation` times `DirectEstateI03Session.__enter__`/`_build`, counts session builds and samples the temporary session directory at exit.
- **Q — existing native evaluator:** wrap `rawlsing_next.pre553_carrier_execution.execute_empirical_query`; for I05 wrap `pre553_prepared_saved_i03.execute_exact_bounded_discovery`. Q is the existing evaluator call, not a new counting path.
- **O — evidence serialization:** time `canonical_json(result.facts)` + `canonical_json(result.release_refs)` after the native result. O is output/fact/replay serialization, not scientific counting.

**Exact limit:** `BatchExecutionRunner` returns receipt refs/states/provenance, not full fact objects. Full fact/risk/denominator/refs/replay parity is measured in `prepared` direct mode on the same estate/catalog/operations; `batch` provides receipt/ref parity. This is a measurement boundary, not a claim that batch facts were separately re-derived. If full batch facts are required, that needs an owner-approved receipt/result extension, not a harness shortcut.

## 4. First single comparable pair

The runner selects five genuinely distinct operations from the accepted query bundle:

| Label | Semantic role |
|---|---|
| `selected_weighted` | selected GOVERNED_WEIGHTED estimand |
| `f2_forward_raw` | F2 forward direction, raw |
| `f2_reverse_raw` | F2 reverse direction, separate denominator |
| `f4_three_raw` | true same-person k>=3 joint |
| `repeated_mr_raw` | repeated/ranked occurrence, not first-value |

No operation is an identical query with a new ID. `selected` raw and `f2_forward` raw would be semantically identical in the accepted bundle, so the selected operation uses the weighted measure variant to preserve distinctness.

The first comparable pair is **baseline one-shot vs prepared direct** on the same estate, catalog and five operations; the batch run uses the same operations and exact release. The fixture is 16 respondents × 5 questions, 54 events, 80 routing facts, 16 weights, 345,134 retained estate bytes and 245,760 B largest observed temporary session component. It includes typed MISSING (B), routed sparse D, two-occurrence MR and true A/B/C k>=3.

## 5. Tiny smoke actually executed (mechanics only)

Command:

```bash
python3 WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117/measure_cut1_prepared.py --mode smoke --negatives
```

Exit 0. The smoke is one tiny sourcefree mechanics run, not matched-performance evidence; it ran while cut1 G5 may be concurrent.

| Mode | Wall s | H admission s | S index s | Q evaluator s (timed ops) | Index builds total / timed ops | Row-group reads | Process-tree peak RSS observed | Output B |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 0.676 | 0.230 | 0.183 | 0.230 | 6 / 5 | 196 | 70,942,720 | 1,885 |
| prepared | 0.550 | 0.238 | 0.064 | 0.226 | 2 / 1 | 136 | 69,197,824 | 1,885 |
| batch | 0.404 | 0.237 | 0.063 | 0.231 | 2 / 1 | 136 | 69,619,712 | 1,170 |
| fresh batch child | 0.400 | 0.243 | 0.063 | 0.221 | 2 / 1 | 136 | 69,124,096 | 1,170 |

The total index-build counts include the mandatory negative/restore probe; `index_builds_measured_operations` excludes it. Baseline = 5 one-shot timed ops + 1 restore; prepared = 1 prepared context + 1 restore; batch = 1 batch context + 1 restore. The prepared Q time is not faster than baseline in this tiny 5-op fixture; the observed structural saving is index-build count (1 vs 5), not a wall-clock performance claim. The fresh child starts product-exited and is separately counted.

Parity observed:

- baseline vs prepared full fact SHA-256: exact for all five operations;
- batch receipt result refs vs baseline fact refs: exact for all five;
- revoked CURRENT: `DirectEstateError: current source/operation authority refused` in baseline, prepared and batch; exact restored fact SHA matches baseline;
- no C11Repository tripwire, no whole-table read, no product edit.

The fresh child started product-exited; the parent passed only paths and the deterministic fixture contract. Parent `RUSAGE_CHILDREN` max RSS `70,459,392 B`; child self-reported `69,554,176 B`. These are tiny-fixture figures, not 100k economics.

## 6. Bounded 600-slot geometry generator (implemented, not real width economics)

`width_fixture.py` is the exact bounded harness addition. It extends the accepted base 5-role fixture with `--questions N` (5..1300) and emits:

- N native `QuestionVariableBinding`s (the accepted A/B/C/D/MR five plus `W0000...` geometry slots);
- one `RoutingEligibilityFact` per respondent per added slot, with `NOT_ELIGIBLE` typed state (not dense responses);
- the accepted base events, coordinates, weights, authorities and A/B/C/MR query bundle;
- the same 13-family `SourcefreeDirectI02Sections` interface and existing `write_direct_estate`/`PreparedSavedC11Admission`/`PreparedI03Session`/`execute_saved_batch` paths.

It does **not** assume 600 columns = 600 events/respondent. A bounded geometry build was executed at 8 respondents / 600 question bindings (not a query/performance matrix):

| Geometry | Respondents | Question bindings | Events | Routing | Weights | Retained | Manifest |
|---|---:|---:|---:|---:|---:|---:|---|
| `fixture_contract_600.json` | 8 | 600 | 27 | 4,800 | 8 | 7,522,473 B | `567122eff5c02dc7dd4379b58ad0aa491c89338c1281ce4524675d8d2e417b4a` |

This proves the generator/13-family writer/geometry build mechanics. It does **not** prove a 600-column query workload, dense events, real-width economics, admission/index cost at scale, or 6 GiB. The 5-question 16-respondent fixture remains the only executed comparable pair. For a real-width pair, use `--questions 600` with a fixed cap and enough respondents to make the intended sparsity realistic, then rerun `baseline/prepared/batch/fresh`; do not call the geometry build production economics. The already-qualified 8R3Q fixture remains the fallback for the smallest mechanics pair.

## 7. Next 1/10/100/fresh-process strategy after cut1 G5

No automatic matrix and no repeats in this turn.

1. Wait for cut1 G5 and an exact accepted code pin/cap; do not reuse a stale SHA.
2. Run one matched pair on the same estate/catalog: baseline vs prepared direct, then batch receipt/ref parity. Fix measurement defects before scaling.
3. If the pair is stable under the fixed resource cap, run 1, 10 and 100 **distinct** operations selected for different target/predicate/direction/k3/weight/occurrence roles. Do not create identical queries with new IDs.
4. Run each scenario as a fresh product-exited child via `--mode fresh`; same-process series is a separate mechanism and must not be conflated with fresh-process open.
5. Record wall/CPU/process-tree RSS/retained/scratch/output/row-group reads/H/S/Q/O; abort on cap; report failures and nonzero exits, not only successes.
6. Do not claim native/original35/source/science/actor or 100k/6GiB/1-10-100 acceptance from a sourcefree fixture.

## 8. Rights, issuer and holds

- Synthetic TEST_ONLY sourcefree fixture only. No original survey/raw respondent data was read, no source read grant was exercised.
- No original governed QUERY issuer, native 100k, source/science/actor authority, protected H1 or production CURRENT is granted or claimed.
- The 29 K3 individual function mappings / 26 NOT_ADOPTED / 14 HELD / F26 exact caller hold and true joint/directional/missing/occurrence negatives remain preserved.
- `#1073/#1083/#1084` corrective code remains unmerged and scientifically distinct; no old branch was merged.
- No product branch merge, no auto-launch, no recurring auto-wake.

## 9. Self-found measurement caveats

- `selected` raw and `f2_forward` raw are semantically identical in the accepted bundle; the harness uses weighted selected to satisfy the distinct-operation rule. This is disclosed, not hidden as a new operation.
- `process_tree_rss_peak_observed_bytes` is max(start, end, `ru_maxrss`), not a continuous sampler; a real run should add an explicit sampler or use the child `ru_maxrss` plus process-tree snapshots.
- H includes manifest/member hashing and admission checks; it is not a pure file-hash microbenchmark.
- S is the existing `_build` cost; Q is the existing evaluator cost; O is serialization. They are not artificially decomposed beyond the existing code boundaries.
- Batch full facts are not returned by the current Batch runner; `batch` parity is refs/receipts, while full fact parity is `prepared` direct on the same estate/catalog/operations.
- The 16-respondent/5-question run has no realistic width/economy; its numbers must not be cited as 100k or matched performance.
