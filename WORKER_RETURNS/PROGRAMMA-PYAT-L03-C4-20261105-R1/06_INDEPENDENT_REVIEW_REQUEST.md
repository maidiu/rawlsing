# 06 — Independent R03 review request against the frozen implementation

**Implementation SHA:** `409be32f7e4b4b961a360be1c8f44a17b5c62173`
**Branch:** `perf/programma-pyat-w05-p03-f1f4-grouped-economy-20261105-r1`
**Base:** `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`
**Phase-1 checkpoint:** `05a9abccded29dfcf7e27b5febcecb4442c8714d`
**Requested grade:** independent sourcefree R03 review of the frozen P2
implementation, measurement, and per-operation exactness.
**Not requested:** protected merge, native/original35 science, actor/Sorok scope,
producer acceptance, or a complete W03/W04 declaration.

## Frozen implementation scope

Review exactly these changed production files at the implementation SHA:

- `rawlsing_next/_pre553_query_eval.py`
- `rawlsing_next/pre553_empirical_query.py`
- `rawlsing_next/pre553_carrier_execution.py`
- `rawlsing_next/pre553_discovery_exact.py` (minimal optional propagation only)
- `rawlsing_next/pre553_issued_workload.py` (minimal owned-scope Batch hook only)
- `rawlsing_next/tests/test_pre553_i03_grouping.py` (11 focused tests)

No source ingestion, compact selector / `_select_respondent_events` ABI v1, authority
semantics, P41, canonical identity, scheduler, or default cache policy was rewritten.

## Required review questions

1. **Actual first-consumer integration.** Confirm grouping is reachable through
   `CarrierNeutralResearchExecutor.execute_i03` / `execute_i05`, the issued Batch
   path, and the minimal discovery hook — not only a benchmark/private-kernel call.
   Confirm single-unit workloads keep the existing unshared path.
2. **Core key completeness.** Check that the core key contains all determinants that
   govern the shared intermediate: exact release/replay/semantic/source-manifest
   refs, universe, respondent identity root, attested index identity, risk set/type/
   source-scope/response-state semantics, predicate + grammar authority, complete
   target plan (targets, topology, domain, included states, topology/response
   authorities, replay/order/domain identity), query authority refs, and exact
   authority-registry fingerprint.
3. **Measure-independent core.** Verify that excluding measure/weight/design from the
   core key is sound because the core contains no weighted result; all RAW/weighted
   aggregation and `_weight_for` validation is recomputed per operation. Flag any
   path where a weighted or raw result is cached/reused across regimes.
4. **Runtime risk issuance.** Confirm the conservative fallback under
   `current_runtime_binding()` is safe and that different query identities with
   query-specific runtime risk issuance cannot cross-share. If the reviewer requires
   contract-keyed sharing instead of fallback, state the exact missing determinant.
5. **Per-operation native fact/replay/provenance.** Verify every operation still
   builds its own exact `EmpiricalFact`, provenance, dependency refs, and replay.
   Confirm no final-fact hash memo, grouped aggregate, or independently authoritative
   retained fact is published.
6. **Actual shared work.** Verify the cold scope builds 11 exact cores with 2 hits
   for the 13-operation mix and that warm counters show baseline routing/predicate/
   target/weight calls collapsing to zero/zero/zero per-operation-weight calls. The
   claim must be actual shared computation, not a label.
7. **Incompatibility and negatives.** Check separate evaluation for different
   releases, universes, risk sets, predicates, target plans, authority registries,
   measures/weights, and runtime bindings; exact parity for special states, zero
   support, unsupported topology, authority DENY, missing/wrong weight, release
   separation, and the `NOT_ADMINISTERED` contract limitation.
8. **Poison/rebuild/cleanup.** Verify stale fingerprint, wrong index identity,
   poisoned core, index rebuild, and scope close/error paths fail closed to the
   unshared path; no wrong `SUPPORTED` fact and no cross-call stale group.
9. **Measurement integrity.** Check identical sealed releases/workload/seeds,
   paired/interleaved baseline vs candidate, separated fixture/cold/query/fact
   costs, CPU/wall/peak-RSS Darwin bytes/index build/scope counters, and honest
   single-operation and incompatible-work costs. Confirm no checksum-only oracle
   was used; full fact material was compared in-process and selected full material
   is retained.
10. **W03/W04 and claim safety.** Confirm the review does not read this as completing
    W03/W04 or canceling the selected compact regenerable capability; confirm the
    existing default in-memory compact realization, optional caller-configured
    Parquet/Zstd persistence, measured compact-memory higher result, cold-construction
    limit, and no production/original35 claim are stated correctly.

## Evidence to inspect

- `00_RETURN.md`, `01_BASELINE_CURRENT_CODE_ABI.md`
- `02_EXACT_COST_AND_MEMORY_RESULTS.jsonl` (Phase-1 + Phase-2 costs/counters)
- `03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl` (Phase-1 + Phase-2 exact parity)
- `04_REPLAY_AND_AUTHORITY_INVALIDATION.md`
- `05_OPTION_MATRIX_AND_MINIMAL_DELTA.md`
- `results/phase2_summary.json`, `results/phase2_commands.jsonl`,
  `results/commands.jsonl`, `results/repeat_summary.json`
- Raw paired JSON (untracked checkout-local):
  `.local-logs/pyat-l03-c4/phase2/main_n{200,1000,3000}.json`,
  `small_fixtures.json`
- `tools/bench_grouped_phase2.py`, `tools/finalize_phase2.py`

## Suggested independent commands

Use the verified runner; no new packages or `/tmp` redirects.

```sh
RUNNER=/tmp/rawlsing-oct28-p1r1/venv/bin/python
TMPDIR="$PWD/.local-logs/pyat-l03-c4/review-tmp" \
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
"$RUNNER" -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_i03_grouping.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py \
  rawlsing_next/tests/test_pre553_c11_execution_view.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py \
  rawlsing_next/tests/test_pre553_query_frontier_hostile.py \
  rawlsing_next/tests/test_pre553_route_b_production.py \
  rawlsing_next/tests/test_universal_workload_custody.py
```

Then rerun the P41 consumer and one paired benchmark (N=200 first; N=1000/3000 only
if the smaller pair is acceptable):

```sh
TMPDIR="$PWD/.local-logs/pyat-l03-c4/review-tmp" \
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
"$RUNNER" -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_universal_world_binding.py::test_same_source_r04_partial_resume_reaches_actual_p41

TMPDIR="$PWD/.local-logs/pyat-l03-c4/review-tmp" \
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
"$RUNNER" WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_grouped_phase2.py \
  --scenario main --n 200 --rounds 3 \
  --output .local-logs/pyat-l03-c4/review-grouped-n200.json
```

## Expected independent verdict fields

- `IMPLEMENTATION_SCOPE`: PASS / REVISE / UNKNOWN
- `CORE_KEY_COMPLETENESS`: PASS / REVISE / UNKNOWN
- `MEASURE_INDEPENDENT_CORE_SOUNDNESS`: PASS / REVISE / UNKNOWN
- `PER_OPERATION_FACT_REPLAY_PROVENANCE`: PASS / REVISE / UNKNOWN
- `ACTUAL_SHARED_WORK_EVIDENCE`: PASS / REVISE / UNKNOWN
- `INCOMPATIBLE_AND_NEGATIVE_PARITY`: PASS / REVISE / UNKNOWN
- `POISON_REBUILD_CLEANUP`: PASS / REVISE / UNKNOWN
- `ISSUED_BATCH_I05_P41_INTEGRATION`: PASS / REVISE / UNKNOWN
- `PAIRED_MEASUREMENT_INTEGRITY`: PASS / REVISE / UNKNOWN
- `W03_W04_CLAIM_SAFETY`: PASS / REVISE / UNKNOWN
- `R03_DISPOSITION`: ACCEPT_FOR_HQ_RECEIVING / REVISE_MATERIAL / MORE_EVIDENCE
- `NEXT_WORK`: `HQ_RECEIVING` / `BOUNDED_REPAIR` / `NO_ACTION`

## Phase-3 preparation note

This preparation adds only `tools/bench_compact_current.py` and documentary
comparison/plan sections in `01`/`05` (plus ordinary status entries in `00`/`02`/
`03`/`04`). It does not alter the frozen implementation
`409be32f7e4b4b961a360be1c8f44a17b5c62173`, production source, numerical tests,
authority, source, guide, or the independent R03 scope. Timed comparison runs are
**NOT_RUN** here; HQ schedules the driver after R03 releases the timed runner.

## Phase-3 measurement context

R03 is complete at `e2f6c1649801b42a475ce3d81f3d85a7c5ccb5b3` with
`ACCEPT_SCOPED_P2` for frozen `409be32f7e4b4b961a360be1c8f44a17b5c62173`; that
acceptance does **not** extend to whole L03. Phase-3 then ran the prepared compact
comparison and compact-grouped measurement without changing production/tests:
V0/V1/V2-cold/warm full-fact parity and V2 cache HIT passed, and compact-release
grouped no-scope vs scope passed exact cold/warm/single/incompatible/capacity checks
with independent row oracle PASS. Timings are sourcefree synthetic N=200/N=1,000
only; no N=3000/all35 claim. Capacity fallback was exact but slower and is unproven.
No new independent review is requested for this measurement-only phase; HQ retains
the R03-scoped acceptance record and may use these artifacts as supporting evidence.

## Capacity-miss guard note

A new implementation/test SHA `9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3` follows
the measured capacity-full duplicate repair. It is **not** covered by R03
`e2f6c1649801b42a475ce3d81f3d85a7c5ccb5b3`, which remains scoped to
`409be32f7e4b4b961a360be1c8f44a17b5c62173`. The narrow guard preserves HIT reuse,
per-query validation/identity/authority gates, and exact no-scope facts; unknown
prospective member size keeps the post-build fallback. No new review is requested
here; HQ may schedule one separately if it accepts the new code.
