# 01 — Actual baseline ABI, Phase-2 grouped ABI, and current code call graph

**Scope:** sourcefree Phase-1 measurement plus the bounded Phase-2 implementation. No
original35, native source/science, actor, human, Sorok, or protected-merge authority is
claimed. No original35, native source/science, actor, human, Sorok, or protected-merge
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


## Phase-2 grouped execution ABI

The production-first-consumer API now has an optional finite scope:

```
CarrierNeutralResearchExecutor.execute_i03(
    *, query_ref, predicate_ref, group_scope: I03GroupedExecutionScope | None = None
) -> QueryExecutionResult
CarrierNeutralResearchExecutor.execute_i05(
    *, discovery_authority_ref, group_scope: I03GroupedExecutionScope | None = None
) -> ExactBoundedDiscoveryResult
CarrierNeutralResearchExecutor.grouped_i03_scope(
    *, max_groups=64, max_cached_members=500_000
) -> I03GroupedExecutionScope
```

`execute_empirical_query(..., group_scope=None)` and
`execute_exact_bounded_discovery(..., group_scope=None)` propagate the scope.
`execute_issued_workload` creates one owned scope when a workload has more than one
unit, passes it to every Batch query/I05 unit, and clears it in `finally` on success
or error. A single-unit workload keeps the existing unshared path. A caller may also
create a scope explicitly:

```
with executor.grouped_i03_scope() as scope:
    executor.execute_i03(query_ref=q, predicate_ref=p, group_scope=scope)
```

### New call graph on a grouped hit

```
execute_i03
  -> execute_empirical_query
     -> per-operation identity/source/authority/issuance checks (unchanged)
     -> _resolve_release_indices / attested _ReleaseIndex (unchanged)
     -> _evaluate_index_group(..., group_scope=scope)
        -> scope.evaluate(index, query, predicate, plan, profile, registry)
           -> exact _core_key match + fingerprint/index identity check
           -> _materialize_grouped_evaluation(core, plan, profile, registry)
              -> RAW: exact core cells
              -> GOVERNED_WEIGHTED: per-operation _weight_for over denominator members
        -> on incompatibility/fallback: existing unshared loop
     -> _build_fact / _make_execution_replay_ref (unchanged, per operation)
```

On a miss the scope computes `_evaluate_index_group_core`: the exact existing
routing/risk, predicate, and target logic without weights, storing used objects and
authority refs for faithful per-operation provenance. It does not call
`_weight_for`, does not build a fact, and does not persist outside the scope.

### Exact core key

The core is keyed by:

- the attested release index object, release/replay/semantic/source-manifest refs,
  universe ref, and a respondent-identity root;
- risk set ref, risk-set type, source-scope mode, and response-state semantics ref;
- predicate ref and grammar authority ref;
- the complete target plan: target refs, topology, domain, domain replay ref,
  topology/response-semantic authority refs, included states, joint-order
  semantics, and full domain identity;
- exact query authority refs;
- exact authority-registry fingerprint;
- a measure-independent-core marker.

Opt-in runtime successor binding disables grouping and falls back to the existing
unshared path in this bounded diff. Measure/weight/design are not core determinants:
they do not govern the core, and all measure/weight validation and aggregation is
redone per operation. No weighted result or final fact is cached.

### Bounded scope safety

- Maximum 64 groups and 500,000 cached denominator members by default.
- `close()`/context exit/error clears all entries; no process-global or persistent
  store; no independently authoritative retained fact.
- Every hit verifies `core.index is index` and recomputes the exact core
  fingerprint; a mismatch evicts and falls back unshared.
- Cache/index rebuild changes the index object identity and therefore the core key;
  no stale group crosses a rebuild.
- Incompatible release/universe/risk/predicate/target/authority/weight/runtime
  material produces a different key or a conservative fallback.

### Phase-2 measurement and artifact map

- Paired benchmark script: `tools/bench_grouped_phase2.py`.
- Phase-2 summary: `results/phase2_summary.json`.
- Phase-2 commands: `results/phase2_commands.jsonl`.
- Raw paired JSON (untracked checkout-local):
  `.local-logs/pyat-l03-c4/phase2/main_n{200,1000,3000}.json`,
  `small_fixtures.json`.
- New focused tests: `rawlsing_next/tests/test_pre553_i03_grouping.py` (11 tests).
- Exact Phase-2 parity entries are appended to
  `03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl`; paired costs and scope/counter
  receipts are appended to `02_EXACT_COST_AND_MEMORY_RESULTS.jsonl`.

---

## Phase-3 preparation (artifact-only, no production/test change): W03/W04 physical chain

**State:** preparation while independent R03 reviews frozen implementation
`409be32f7e4b4b961a360be1c8f44a17b5c62173`. No production file, test, cache
default, source, or guide was changed in this preparation. No timed benchmark,
heavy fixture generation, or test suite was executed in this phase.

### Exact current physical consumer chain

The actual current chain at the assigned base is:

```
decode_sav/decode_dta -> PhysicalSourceIncidence.iter_batches/iter_cells
  (pre553_physical_decoder.py:156,209; bounded physical cell stream)
 -> build_source_backed_c11_repository / build_validated_source_backed_c11_release
  (pre553_source_backed_c11_facade.py:601,656; pre553_physical_c11_bridge.py:24)
 -> project_c11_candidate_from_physical_cells
  (pre553_source_backed_c11_facade.py:502)
  -> native RespondentEvent/coordinate/weight Python lists; then tuple(sorted(...))
     at facade:558-560
 -> validate_c11_source_release
  (pre553_c11_ingest.py:743)
  -> full I02 validation; public_objects/internal_records tuples sorted at
     c11_ingest:777-778; sealed C11LogicalRelease
 -> _compact_public_objects
  (_pre553_c11_execution_view.py:239; called from facade:679)
  -> _CompactPublicObjects/_EventLane selectors + immutable Arrow event-body array;
     optional Parquet/Zstd cache at view:289-320
 -> C11Repository._commit_validated / resolve_object_exact
  (pre553_c11_repository.py:115,107)
 -> CarrierNeutralResearchExecutor.execute_i03
  (pre553_carrier_execution.py:430) through Route B
  (pre553_route_b_production.py:495,582) or issued Batch
  (pre553_issued_workload.py:280,335,340)
```

The compact Arrow conversion is explicitly **after** complete I02 validation of a
fully materialized native candidate. The current default therefore is
`full native candidate -> sealed full logical release -> compact execution view`;
it is not a streaming/lazy I02 validation path. That source shape is a potential
cold-construction peak, not by itself proof of a production defect.

### Selected October capability mapping

Reference: `315251451a6d112fb312a6a2e80b096d345c5de6`:
`01_EXECUTIVE_ADJUDICATION.md` §§3–6; `04_TARGET_ARCHITECTURE...` §§H–J;
`05_FULL_WORK_BREAKDOWN...` W03/W04; `06_PERFORMANCE...` cost model and
storage/invalidation; `11_DECISION_AND_OBLIGATION_LEDGER.json` W03/W04/P01/P02.

- **W03/P01:** efficient exact C11 realization/reconstruction and the logical
  repository seam: exact sealed identity, compact/lazy working view, exact
  on-demand object reconstruction, preserved I02 validation/closure/replay,
  no mandatory 7.91 GB new-source derived bundle, memory lifecycle.
- **W04/P02:** hybrid compact respondent-coherent transient plus a default
  regenerable source/decoder/authority/projection/version-keyed compressed
  Parquet/Zstd accelerator with manifests and atomic invalidation, or a
  competent-owner-accepted functionally equivalent physical realization.
- The October `P01`/`P02` entries are design/status records; the `P01-S3`
  journal/streaming build order is **proposed and not launched**. It is not
  adopted here as a mandatory rewrite.

### Function-level present/absent comparison

| Capability piece | Current actual function / ABI | Input -> typed output | Actual first consumer | Preparation finding |
|---|---|---|---|---|
| Bounded physical cell stream | `PhysicalSourceIncidence.iter_batches(batch_size)` / `iter_cells(batch_size)` (`physical_decoder:156,209`); `ExactPhysicalCellStream` (`facade:249`) | source snapshot + layout -> tuple[`PhysicalCell`] batches, exact row/slot ordinals | `build_validated_c11_release` / facade builder | **Present**; decoder does not retain a complete cell-object universe for chunk-capable readers. |
| Governed candidate construction | `project_c11_candidate_from_physical_cells` (`facade:502`) | physical cells + `GovernedC11Projection` -> `C11SourceReleaseCandidate` | I02 validation | **Present but full-candidate materialized**: events/coords/weights are Python lists/tuples; no streaming candidate. |
| Complete I02 validation | `validate_c11_source_release` (`ingest:743`) via `build_validated_c11_release` (`physical_c11_bridge:24`) | candidate -> sealed `C11LogicalRelease`, exact public/internal tuples, `ReplayManifest` | `build_source_backed_c11_repository`; exact object consumers | **Present**; full public tuple sorted at `ingest:777-778`. |
| Compact execution view | `_compact_public_objects` (`execution_view:239`) | sealed release -> `_CompactPublicObjects`/`_EventLane` selectors + Arrow event-body array, or `None` if pyarrow absent | `build_source_backed_c11_repository:679`; I03 index/event selection | **Present and default when pyarrow is installed**; not a lazy I02 admission mechanism. |
| Exact on-demand object reconstruction | `_EventLane.materialize` (`execution_view:77`), `_EventLocator.materialize` (`:95`), `_CompactPublicObjects.__getitem__` (`:142`), `C11Repository.resolve_object_exact` (`repository:107`) | exact ref -> full `RespondentEvent`/canonical object; absent/ambiguous ref fails closed | repository consumers, `_ReleaseIndex`, first reader where exact object needed | **Present** for the compact release; exact event and non-event resolution is available. |
| Logical repository seam | `C11Repository._commit_validated` (`repository:115`) | sealed release -> exact ref map/repository; `staged = dict(self._objects)` copy at `:127` | all I03/I05/Batch consumers | **Present exact function**; full dict staging/copy remains an economic concern, not a demonstrated consumer failure. |
| Default compact Arrow | `build_source_backed_c11_repository` always attempts `_compact_public_objects` (`facade:679-683`) | sealed release -> in-memory compact view | first consumer | **Present**; this is the current default in-memory compact realization. |
| Optional persistent compressed compact cache | `_cache_directory` (`execution_view:160`), `_read_bodies` (`:178`), `_write_bodies` (`:212`), key at `:294-307` | sealed compact release + source/decoder/projection/release/replay/member-root + current authorities -> authenticated Parquet/Zstd event-body slot | `build_source_backed_c11_repository` when env/root configured | **Present optional**, not default; env unset means no persistent cache. |
| Exact full logical carrier | `ParquetC11Carrier.persist` (`parquet_carrier:249`), `reopen` (`:279`) | sealed full `C11LogicalRelease` -> canonical Zstd Parquet relations; exact full release reconstruction | carrier/direct-session consumers, not default I03 hot view | **Present and exact**, but it is a full logical carrier, not the compact analytical hot view; using it as default would duplicate full C11 state. |
| R4 typed event table | `R4RespondentEventWriter` (`r4_compaction:127`), `R4RespondentEventReader.reconstruct` (`:256,286`) | `RespondentEvent` stream -> compact typed Parquet event rows -> exact `RespondentEvent` | event-table/query consumers; tested exact reconstruction | **Present component**; event-only, not a complete release/replay carrier. |
| R5 typed value codec | `R5TypedValueCodec.encode/decode` (`r5_codec:180,195,239`) | typed Python value -> versioned typed carrier -> exact value | physical decoder normalization and typed carriers | **Present component**; not a release/cache owner. |

### W03/P01 exact function decision

- **No exact function-level gap was found for the current first consumer.** The
  physical stream, governed candidate, complete I02 validation, sealed release,
  compact execution view, exact on-demand event resolution, repository exact lookup,
  and `CarrierNeutralResearchExecutor.execute_i03` are all present and composed.
- The selected *economy* claim is **not proved**: the current cold path materializes
  all native events/coords/weights before validation (`facade:502,558-560`), then
  materializes sorted public objects (`ingest:777-778`), then compacts. Without a
  controlled same-release measurement this is an **unproven potential cold-memory
  peak**, not a mandatory rewrite.
- **Disposition:** `PRESENT_COMPOSED_NO_BUILD` for exact W03/P01 function;
  `EVIDENCE_OR_ABI_READY` only for cold construction economy. A streaming/lazy I02
  adapter or journal is **not** justified by code shape alone.
- **First actual failure:** none in the current sourcefree first-consumer function.
  The first falsifier would be a controlled same-sealed-release run at representative
  scale that fails authorized memory/disk/time while the exact same facts/replay are
  required; that would justify a bounded streaming candidate/replay adapter.

### W04/P02 exact function decision

- The exact **codec/carrier capabilities** are present: default in-memory compact
  Arrow (`_compact_public_objects`), optional authenticated Parquet/Zstd event-body
  cache with strict key/atomic write/read validation and HIT/DELETE/CORRUPT/STALE/
  REVOKED behavior, full exact `ParquetC11Carrier.persist/reopen`, R4 typed event
  table, R5 typed value codec.
- The **default persistent compressed acceleration** is not present as a default:
  `_cache_directory()` returns `None` when `RAWLSING_C11_ACCELERATOR_DIR` is unset
  (`execution_view:160-175`), so no persistent Parquet/Zstd slot is written; the
  in-memory compact Arrow view is still built. This is the precise first gap.
- `ParquetC11Carrier` is not a substitute for the selected compact hot view: it
  persists full public/internal objects and reconstructs a full logical release; it
  is compatible exact reconstruction/carrier, but making it default would create a
  second full persistent carrier. R4/R5 are components, not a complete release cache.
- **Disposition:** `PRESENT_COMPOSED_NO_BUILD` for the exact compressed/regenerable
  capability (optional), with `OWNER_DECIDE` for whether default activation or
  functional-equivalence acceptance is required. This is a policy/default-delivery
  decision, not a missing codec/engine. No blanket cache default is asserted.
- **First actual failure:** env/root unset means no persistent slot; a legacy
  in-memory `PhysicalSourceIncidence` without a decoder digest also yields
  `physical_binding() is None` (`facade:667-680`, `execution_view:292`), so no
  persistent body slot even with an env root. Both are configuration/transport
  conditions, not source truth or authority defects.

### Legacy/current and carrier comparison

- Historical A/R5 `pre553_r5_compact_carrier.py` and `pre553_r5_c11.py` are **not
  current files** at this branch. Their absence alone is not a gap: current
  `_compact_public_objects`, `ParquetC11Carrier`, R4 and R5 already cover distinct
  present functions. Do not resurrect the historical symbols by name.
- `ParquetC11Carrier` is current, exact, and tested for persist/reopen, corruption,
  stale root, direct DuckDB session, and exact public/internal/replay equality. It
  is compatible with the current sealed release. It is **not** the compact I03 hot
  view and must not be conflated with it.
- R4 is current, exact for `RespondentEvent` reconstruction, and tested; it is an
  event-table component. R5 is current and tested for typed values. A future
  bounded adapter from R4/R5 into the compact view is possible only if a controlled
  measurement proves the existing event-body lane is deficient; no such deficit is
  shown here.

### Phase-3 prepared comparison driver

`tools/bench_compact_current.py` is the prepared, directly executable driver for
the unresolved W03/W04 economy question. It reuses the current physical chain and
first consumer, not a new framework:

- V0 = `build_validated_source_backed_c11_release_from_stream` (full native sealed
  release) + `C11Repository` + `CarrierNeutralResearchExecutor.execute_i03`.
- V1 = `build_source_backed_c11_repository` with the existing default compact Arrow
  `_CompactPublicObjects`.
- V2-cold / V2-warm = the same V1 facade with an explicit workload-owned private
  Parquet/Zstd cache root. The source is an `ExactPhysicalCellStream` with non-empty
  `decoder_metadata_digest`; the coordinator asserts cold miss/write and warm HIT.
  Legacy in-memory `PhysicalSourceIncidence` (`physical_binding=None`) is not used
  as a cache HIT.

The driver runs each variant in a fresh subprocess, reuses one fixture builder and
the same sealed source/projection/release, records phase wall/CPU and whole-process
Darwin `ru_maxrss` bytes, and compares **full fact material** (`fact.as_dict()`)
including cells, refs, provenance, and replay against V0. N=200 and N=1,000 are
separate commands. Tiny N=3 smoke is `SMOKE_ONLY_NOT_BENCHMARK`; no timing conclusion
is drawn.
