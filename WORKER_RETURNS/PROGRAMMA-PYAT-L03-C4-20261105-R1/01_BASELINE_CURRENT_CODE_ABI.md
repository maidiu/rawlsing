# 01 — Actual baseline ABI and current code call graph

**Scope:** sourcefree Phase-1 measurement only. No production `rawlsing_next` change was
made. No original35, native source/science, actor, human, Sorok, or protected-merge
authority is claimed.

## Identity

- Repository: `maidiu/rawlsing`
- Assigned branch: `perf/programma-pyat-w05-p03-f1f4-grouped-economy-20261105-r1`
- Base commit: `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`
- Binding commission:
  `66cedcdf01cd156d0024419957b5c34832ebf8a5:WORKER_COMMISSIONS/PROGRAMMA_PYAT_F2F4_GF1_RECOVERY_20261105_R1/04_HYB_COMPACT_GROUPED_KWAY_QUERY_BENCHMARK.md`
- Binding protected law:
  `PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_HISTORICAL_FUNCTION_SUCCESSION_AND_WORK_SELECTION_LAW_R1.md`
- Model provider observed at invocation: `opencode-go/deepseek-v4.1-flash`.
- Runner: `/tmp/rawlsing-oct28-p1r1/venv/bin/python` (real path
  `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11-intel64`).
- Python `3.11.3`, macOS `13.7.8`, `Darwin 22.6.0`, `x86_64`, 16 logical CPUs,
  17179869184 bytes physical memory, host `oldMac.lan`.
- pyarrow `22.0.0`, pandas `3.0.6`, pyreadstat `1.3.2`, pytest `9.1.1`.
- No new environment or package was installed. Timed scenarios are single-runner,
  sequential; no parallel timed case was run.

## Current accepted source lineage relevant to this baseline

- `43d2b70ebae4d183aadbd9694624575857fd100f` (PR684, ancestor of the base):
  frozen cached-index attestation and rebuild-on-corruption in `_release_index_for`.
- `cd1e7ccf8419a000817b4a8535879da56c06db98` (PR686, ancestor of the base):
  compact selector reference isolation and frozen selector-v1 handoff.
- `a8c0d4534d275097102a5d1fde547c3c7b320820` (ancestor of the base):
  P1R2 CAS receiving witness.
- Selector v1 is present at the base (`_SELECTOR_CONTRACT_VERSION = 1`). The
  external P1R2 qualification commit `f8e9e1dea9e07e60dc841001a6878d7620338a42`
  is **not** an ancestor of this assigned base; it is external context and was not
  re-run as this worker's qualification.

## Actual first consumer and call graph at the base

The first actual sourcefree I03 consumer is
`CarrierNeutralResearchExecutor.execute_i03`
(`rawlsing_next/pre553_carrier_execution.py:427`).
The Route-B production compositor calls it at
`rawlsing_next/pre553_route_b_production.py:582` inside
`execute_route_b_production` (`:495`). The issued workload path reuses the same
executor through Batch (`rawlsing_next/pre553_issued_workload.py:316,328`) and
the P41 world-binding receiver is exercised by the existing test
`test_universal_world_binding.py::test_same_source_r04_partial_resume_reaches_actual_p41`
(one pass, 67.32 s).

```
execute_route_b_production (route_b:495)
  -> bind_repository_builder -> build_source_backed_c11_repository (sealed C11 release)
  -> binding.executor.execute_i03 (route_b:582)
     -> CarrierNeutralResearchExecutor.execute_i03 (carrier_execution:427)
        -> RuntimeObjectCatalog.resolve_query_exact / resolve_predicate_exact
        -> execute_empirical_query (empirical_query:434)
           -> public identity/hash checks, typed-state checks, condition match
           -> authority closure/fitness checks
           -> _resolve_release_indices (empirical_query:126)
              -> _release_index_for (empirical_query:102) under repository lock
                 -> _build_release_index (query_predicate:63) ONLY on miss/attestation failure
           -> _evaluate_index_group (query_eval:313)
              for each respondent in the cached release index:
                -> _routing_fact_for (query_eval:51)
                -> _eval_predicate (query_predicate:411)
                   -> _select_respondent_events (query_predicate:18)
                -> _weight_for (query_eval:275) for governed weighted measure
                -> _target_configuration (query_eval:253)
                   -> _target_component_value -> _select_respondent_events
           -> _build_fact (query_eval:553)
              -> _make_execution_replay_ref (query_eval:522)
                 -> _cell_projection (query_eval:502)
              -> provenance/dependency/authority construction
```

The actual per-operation repetition is visible in this loop: after the release
index is cached, every operation still runs routing/risk membership, predicate
truth, weight lookup, and target extraction for every respondent, and then
builds its own full fact/replay/provenance material. The derived-cohort
membership compiler is execution-local per predicate
(`_compile_derived_branch_memberships`, `query_predicate:366`), not a
cross-operation cache.

## ABI observed

`CarrierNeutralResearchExecutor.execute_i03(*, query_ref, predicate_ref) -> QueryExecutionResult`

- Both refs resolve by exact preimage from `RuntimeObjectCatalog`; no latest,
  default, fuzzy, or hash-inversion lookup exists.
- `query.condition_predicate_ref` must exactly equal the supplied predicate ref.
- `QueryExecutionResult` carries `query_ref`, ordered `facts`, `source_scope_mode`,
  and canonical `release_refs`.
- Each `EmpiricalFact` carries typed state, exact raw numerator/denominator,
  exact weighted fraction fields, complete cell projection, risk/denominator
  member refs, provenance/dependency refs, replay ref, and source/measure/risk
  scope fields.
- A missing bound release fails at executor construction; a missing exact release
  at query resolution becomes a typed `UNAVAILABLE` fact, never a fallback.

`execute_i05(*, discovery_authority_ref)` remains the separate discovery consumer;
the Route-B production path and the issued-workload test path were exercised, but
I05 is not the W05/P03 grouped-query target.

## Release-index cache and authority behavior

`C11Repository` owns `_i03_release_indices`, `_i03_index_attestations`, and
`_i03_index_lock` (`rawlsing_next/pre553_c11_repository.py:79-84`).

- Index key: `(release.release_ref, universe_ref)`.
- On hit, `_release_index_for` validates the cached index object identity plus
  11 attested payload fields (`release`, `universe`, `respondents`,
  `events_by_respondent`, `coordinates_by_respondent`, `routing_by_respondent`,
  `weights_by_respondent`, `source_relations`, runtime authorities, runtime
  repository, runtime predicate grammar authority).
- On any attestation failure, the index is rebuilt only from the sealed I02
  release under the repository lock. A cache entry never grants source authority.
- The index is a source-release/universe view, **not** a risk-set, weight, or
  query-result cache. Risk selection, authority validation, weights, target
  topology, and facts remain per-operation.
- The compact accelerator (`_CompactPublicObjects`, Parquet Zstd event-body lane)
  is derived from the same sealed release and authenticated to exact event refs.
  It is keyed by source/decoder/projection/release/replay/member-root material
  and is regenerable. Its storage root is env-gated by
  `RAWLSING_C11_ACCELERATOR_DIR`; no default-on or retention-policy change was
  made.

## Exact benchmark construction

All scenarios reuse accepted test constructors and fixtures:
`rawlsing_next/tests/test_pre553_empirical_query.py::_build_source`, `_predicate`,
`_query`, `_branch_predicate`, `_query_authority`; the hostile frontier pack
`rawlsing_next/tests/pre553_query_frontier_fixtures.py`; the Route-B fixture in
`test_pre553_route_b_production.py`; the issued-workload custody fixture in
`test_universal_workload_custody.py`; and the C11 execution-view cache tests.

Synthetic source shape (scaled variants of the same constructor):

| N respondents | events | routing facts | coordinates | weights | event-body JSON bytes |
|---:|---:|---:|---:|---:|---:|
| 200 | 1,600 | 3,200 | 200 | 200 | 2,966,400 |
| 1,000 | 8,000 | 16,000 | 1,000 | 1,000 | 14,856,000 |
| 3,000 | 24,000 | 48,000 | 3,000 | 3,000 | 44,568,000 |

The source has eight questions (`A,B,C,K,X,Y,Z,U`) with exact deterministic
0/1 patterns, including `K = A xor B xor C`, `Z = X xor Y`, a coordinate, and
governed weights `1+(i mod 4)`. Two risk sets are present: `R` = all respondents;
`S` = even-index respondents. No invented source meaning, weight rule, routing
grant, or scientific estimand is introduced; these are test-only constructors.

The 13-operation mix per size covers:
- compatible repeated work: `all_K_raw`, `all_K_weighted`, `all_K_raw_sibling`;
- target siblings: `all_X_raw`, `all_Z_raw`;
- 2/3/4 target respondent-linked operations: `all_XY_raw`, `all_XYZ_raw`,
  `all_ABCK_raw`;
- forward/reverse conditional: `cond_X1_target_Y`, `cond_Y1_target_X`;
- XOR/no-lower-order signal: `xor_condition_target_Z`;
- minority branch: `minority_branch_target_K`;
- incompatible risk set: `risk_S_target_K`.

Existing-fixture coverage additionally includes XOR zero-unary, Simpson reversal,
same marginals/different joint, response-position conjunction, response/response
cotravel, routing asymmetry, raw/weighted divergence, observed-zero vs zero-support,
MISSING/DK/REFUSAL/IAP/NOT_ASKED, source-indexed disagreement, multi-universe
noncomparability, ordered/ranked/repeated topology, and the 4-way bounded joint.

## Measurement method and caveats

- Clean timings: `time.perf_counter()` wall and `time.process_time()` CPU around
  each `execute_i03` call; `gc.collect()` before each operation. No profiler or
  wrapper was active in the clean passes.
- Peak RSS: `resource.getrusage(RUSAGE_SELF).ru_maxrss` on Darwin, reported in
  bytes. It is a process high-water mark, not per-operation resident-set sampling.
- Cold index: first operation on a fresh repository; warm: later operations on
  the same repository. Four-pass repeat measurements at N=1,000 and N=3,000 use
  pass 0 cold-index and passes 1–3 warm.
- Attribution: a separate pass wraps the existing top-level functions
  (`_routing_fact_for`, `_eval_predicate`, `_weight_for`,
  `_target_configuration`, `_evaluate_index_group`, `_build_fact`,
  `_make_execution_replay_ref`, `_cell_projection`, `_resolve_release_indices`,
  `_release_index_for`, `_build_release_index`, and authority/selector counters).
  Component times are inclusive and some are nested. Instrumented totals are
  reported alongside clean totals; the difference is the measured instrumentation
  and run-noise delta. Negative deltas occurred because a later process was
  faster than the clean pass; component **proportions** are the defensible result,
  not absolute instrumented seconds.
- Cold-start wall includes interpreter import and synthetic fixture construction.
  Fixture construction dominates the scaled runs (for example, 89.85 s of the
  130.79 s N=3,000 clean parent wall) and is not a production cold-start claim.
- No original35 scalability, MB, dollar, or speedup claim is made. N=3,000 is a
  bounded synthetic probe, not an estimate of the 35-source estate.
- Raw measurement JSON was moved outside the tracked return to
  `.local-logs/pyat-l03-c4/raw-results/` to respect the disk cap; the required
  exact facts and costs are in `02_EXACT_COST_AND_MEMORY_RESULTS.jsonl` and
  `03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl`, with scripts in `tools/`.

## Exact commands

All commands used the verified runner and TMPDIR/cache under the assigned checkout.
Selected exact commands and exits:

| label | exact command (runner abbreviated `$PY`) | exit | summary |
|---|---|---:|---|
| tests_empirical_query | `$PY -m pytest -q -p no:cacheprovider --basetemp .local-logs/pyat-l03-c4/tmp/pytest-empirical rawlsing_next/tests/test_pre553_empirical_query.py` | 0 | 32 passed in 0.74 s |
| tests_carrier_execution | `$PY -m pytest -q -p no:cacheprovider --basetemp .../pytest-carrier rawlsing_next/tests/test_pre553_carrier_execution.py` | 0 | 4 passed in 0.31 s |
| tests_c11_execution_view | `$PY -m pytest -q -p no:cacheprovider --basetemp .../pytest-view rawlsing_next/tests/test_pre553_c11_execution_view.py` | 0 | 8 passed in 3.66 s |
| tests_query_frontier_hostile | `$PY -m pytest -q -p no:cacheprovider --basetemp .../pytest-frontier rawlsing_next/tests/test_pre553_query_frontier_hostile.py` | 0 | 14 passed in 0.66 s |
| tests_universal_workload_custody | `$PY -m pytest -q -p no:cacheprovider --basetemp .../pytest-custody rawlsing_next/tests/test_universal_workload_custody.py` | 0 | 6 passed in 17.87 s |
| tests_p41_same_source | `$PY -m pytest -q -p no:cacheprovider --basetemp .../pytest-p41 rawlsing_next/tests/test_universal_world_binding.py::test_same_source_r04_partial_resume_reaches_actual_p41` | 0 | 1 passed in 67.32 s |

The exact full command lines and scenario commands are in
`results/commands.jsonl`; scenario logs are in `.local-logs/pyat-l03-c4/logs/`.

## Contract limitation: NOT_ADMINISTERED

C11/I03 has typed response/routing states including `MISSING`, `DK`, `REFUSAL`,
`IAP`, and `NOT_ASKED`, but it has no `NOT_ADMINISTERED` I03 response/routing
state. `NOT_ADMINISTERED` appears outside this C11/I03 query contract, for
example as a binding-level refusal `FIXTURE_TARGET_NOT_ADMINISTERED` when a
fixture target is absent from the projection
(`rawlsing_next/pre553_native_workload_binding.py:127,529,586`) and in the
separate universal-grammar administration vocabulary. Therefore no I03 fact was
invented for it at this checkpoint. This is a precise contract limitation, not a
scientific omission and not an authorization to add a new state.

## Artifact map

- `00_RETURN.md` — compact checkpoint return.
- `01_BASELINE_CURRENT_CODE_ABI.md` — this file.
- `02_EXACT_COST_AND_MEMORY_RESULTS.jsonl` — process/op/cache/issued/repeat/test costs.
- `03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl` — exact baseline facts, oracle
  relations, frontier fixtures, replay/authority invalidation, cache parity.
- `04_REPLAY_AND_AUTHORITY_INVALIDATION.md` — replay/authority/cache negatives.
- `05_OPTION_MATRIX_AND_MINIMAL_DELTA.md` — five-test disposition, options,
  recommendation, PROGRAMMA delta.
- `06_INDEPENDENT_REVIEW_REQUEST.md` — independent review request.
- `tools/` — reusable benchmark worker/driver/finalizer.
- `results/commands.jsonl`, `results/repeat_summary.json` — command receipts and
  warm-repeat statistics.
