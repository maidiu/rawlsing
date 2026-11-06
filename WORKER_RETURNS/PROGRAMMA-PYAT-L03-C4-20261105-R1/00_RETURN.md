# PROGRAMMA PYAT L03 / C4 — Phase-2 implemented grouped economy

**Status:** PHASE-2 COMPLETE / P2 FROZEN / PHASE-3 MEASURED / CAPACITY-MISS GUARD IMPLEMENTED AND MEASURED.
**Preparation commit:** `83fcb4f760b1e150333b34a2e90d8c980661d683`. **Measurement commit:** `a85df66ec93a951d8fd50d751822b70569df94ef`.
**Independent R03:** `e2f6c1649801b42a475ce3d81f3d85a7c5ccb5b3` = `ACCEPT_SCOPED_P2` for frozen `409be32f7e4b4b961a360be1c8f44a17b5c62173`; it does **not** accept the new capacity-miss guard `9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3` or whole L03.
**Branch:** `perf/programma-pyat-w05-p03-f1f4-grouped-economy-20261105-r1`
**Base:** `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`
**Phase-1 checkpoint:** `05a9abccded29dfcf7e27b5febcecb4442c8714d` (artifact `da7be66893217175f9301717c7f1693e6ca89ed8`)
**Previous implementation SHA:** `409be32f7e4b4b961a360be1c8f44a17b5c62173`
**New implementation/test SHA:** `9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3`
**Capacity evidence commit:** `2a41b4682cfbbdc2b5e12ba71d114adb431c670f`
**Model provider observed at invocation:** `opencode-go/deepseek-v4.1-flash`.
**Authority:** sourcefree engineering only. No original35, native source/science,
actor/V3, human, Sorok, protected CAS, or merge authority is claimed.

## Implemented change

The smallest warranted W05/P03 delta is implemented: **finite execution-local
compatible grouped AND-risk/target core reuse** inside the existing I03 evaluator
and actual first-consumer path.

Changed production files (narrow scope):

- `rawlsing_next/_pre553_query_eval.py` — measure-independent exact core
  (`_GroupCore`, `_evaluate_index_group_core`), per-operation measure/weight
  materialization (`_materialize_grouped_evaluation`), exact determinant helpers,
  and an optional `group_scope` hook in `_evaluate_index_group`.
- `rawlsing_next/pre553_empirical_query.py` — `I03GroupedExecutionScope`
  (context-managed, bounded, nonpersistent) and optional `group_scope` on
  `execute_empirical_query`.
- `rawlsing_next/pre553_carrier_execution.py` — `group_scope` on
  `CarrierNeutralResearchExecutor.execute_i03` / `execute_i05`, plus
  `grouped_i03_scope()`.
- `rawlsing_next/pre553_discovery_exact.py` — minimal optional propagation so I05
  candidate query roles reuse the same execution scope.
- `rawlsing_next/pre553_issued_workload.py` — minimal Batch integration: one owned
  scope is created for a multi-unit workload, passed to query and discovery units,
  and cleared in `finally` on success or error.
- `rawlsing_next/tests/test_pre553_i03_grouping.py` — 11 focused tests.

Not changed: source ingestion, compact selector / `_select_respondent_events` ABI
v1, authority semantics, P41, canonical identities, scheduler, default cache
policy, WeightMeasureFact semantics, or any original-source/science owner.

## Semantics and safety

A shared core contains only measure-independent routing/risk membership, condition
truth, exact target cell resolution, and used object/authority material. It never
contains weighted cells, weighted denominators, query-specific facts, or replay
material. Every operation still:

- validates its own query/predicate identity, source binding, index attestation,
  authority/issuance/revocation state, risk/measure/target determinants;
- applies its own RAW/GOVERNED_WEIGHTED measure and weight validation;
- constructs its own exact native `EmpiricalFact`, provenance, dependency refs,
  and replay ref.

The core key includes exact release/universe/respondent-root identity, the attested
index object, risk set/type/source-scope/response-state semantics, predicate and
grammar authority, complete target plan (target refs, topology, domain, included
states, topology/response authorities, replay ref, order semantics), query
authority refs, and the exact authority-registry fingerprint. Opt-in runtime
successor binding causes a conservative fallback to the existing unshared path.
Measure/weight/design are deliberately **not** core-key determinants because they
do not govern the core; they are applied and validated per operation, and no
weighted result is cached or reused across regimes.

Scope is finite (default max 64 groups / 500,000 cached denominator members),
clears on `close()`/context exit/error, and is never process-global or persistent.
Every hit verifies the cached core fingerprint and index identity; a mismatch,
corruption, capacity bound, or unprovable compatibility falls back to the exact
existing unshared path. Incompatible work is separately evaluated.

## Paired measured results

Identical sealed releases, fixture seeds, operation mix, and instrumentation;
single timed process at a time; baseline is the unchanged no-scope path. `all facts
equal` means full `EmpiricalFact.as_dict()`, fact-ref, and replay-ref equality for
every operation, not checksum-only.

| N | cold baseline | cold candidate | warm baseline median | warm candidate median | warm speedup | single-op candidate Δ | incompatible-first-pass candidate Δ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 200 | 1.4159 s | 1.3585 s | 1.3433 s | 0.4140 s | 3.25× | −2.5% | +2.6% |
| 1,000 | 6.9096 s | 6.5482 s | 6.4835 s | 2.1123 s | 3.07× | +10.9% | +3.9% |
| 3,000 | 20.9967 s | 20.2396 s | 20.2322 s | 6.2198 s | 3.25× | +4.4% | +0.8% |

Warm per-operation speedups at N=3,000: `all_K_raw` 3.00×, `all_K_weighted`
1.97× (weights remain per operation), `all_XY_raw` 3.21×, `all_XYZ_raw` 3.38×,
`all_ABCK_raw` 3.56×, `cond_X1_target_Y` 3.32×, `cond_Y1_target_X` 3.39×,
`xor_condition_target_Z` 4.81×, `minority_branch_target_K` 3.77×,
`risk_S_target_K` 3.46×.

Actual work counts for one warm full pass (instrumented counters, not timings):

| N | baseline routing / predicate / target / weight calls | candidate routing / predicate / target / weight calls |
|---:|---|---|
| 200 | 3,800 / 2,500 / 2,002 / 2,002 | 0 / 0 / 0 / 200 |
| 1,000 | 19,000 / 12,500 / 10,010 / 10,010 | 0 / 0 / 0 / 1,000 |
| 3,000 | 57,000 / 37,500 / 30,030 / 30,030 | 0 / 0 / 0 / 3,000 |

This is actual shared work, not a label or final-fact memo. The cold scope builds
11 exact cores with 2 compatible hits for the 13-operation mix; a later warm pass
reuses 11 exact cores and materializes 13 separate facts. Weight validation remains
per weighted operation; no RAW/weighted result reuse occurs. Fact construction stays
per operation and measured candidate fact time was +5% to +9% versus baseline in the
instrumented counter pass (0.308/0.281 s at N=200; 1.565/1.438 s at N=1,000;
4.532/4.219 s at N=3,000), i.e. not reduced and within a small measured overhead.

## Integration evidence

The issued-workload path was exercised with a real two-query plus discovery
workload through Batch/I05: the candidate scope recorded 2 core builds and 2
core hits across the two queries and discovery candidate roles, and produced
identical output refs, receipts, facts, and discovery receipts versus a closed
scope acting as the unshared baseline. The existing issued-workload custody suite
and the P41 same-source end-to-end consumer test passed at the candidate.

## Focused test evidence

- New grouped suite: **11 passed**.
- Candidate focused suite (grouping + empirical query + carrier + compact view +
  discovery + hostile frontier + Route B + issued custody): **100 passed in
  24.98 s**.
- Candidate P41 same-source test: **1 passed in 50.39 s**.
- Phase-1 65-test receipt and exact frontier evidence are retained in
  `results/commands.jsonl` and `03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl`.
- Grouped tests cover exact parity and actual core sharing; compatible vs
  incompatible keys; weighted-first ordering; special states, zero support,
  unsupported topology, and the `NOT_ADMINISTERED` limitation; poisoned memo and
  index rebuild; runtime-binding fallback; authority DENY; weight missing and
  wrong weight basis; release/universe/registry separation; issued Batch/I05
  integration; single-operation and scope cleanup on error.

## W03 / W04 status distinction

The selected W03/W04 physical requirements are **not** declared complete merely by
this W05/P03 change.

- Current source-backed builder automatically selects the in-memory compact Arrow
  realization when pyarrow is installed; that is the existing default compact
  realization. Persistent Parquet/Zstd acceleration is caller-configured through
  `RAWLSING_C11_ACCELERATOR_DIR` and remains optional/authenticated/regenerable.
- W04/P02's selected exact needed function remains present; this diff does not
  change its default, retention, eviction, or storage policy and does not create a
  second persistent engine.
- Measured compact memory remains higher at the current fixture (N=1,000 compact
  peak RSS 352–384 MB versus native 287.7 MB) and source reacquisition/fixture
  construction dominates cold runs. The economical cold-construction/memory limit
  is therefore explicitly **unresolved**, not canceled.
- W03/P01 exact sealed C11 execution realization remains as measured in Phase 1;
  no new compact-carrier rewrite was bundled.

## Limits stated honestly

- Sourcefree synthetic only; no original35/native science/human/actor/Sorok claim.
- Warm speedups are for the measured compatible synthetic mix; they are not a
  universal 3× claim. Explicit single-operation scope cost was honest and mixed
  (−2.5% at N=200, +10.9% at N=1,000, +4.4% at N=3,000; production does not create a
  scope for single-unit workloads). Incompatible-work first-pass candidate cost was
  +0.8% to +3.9% at N=1,000/3,000 and +2.6% at N=200.
- Cold candidate was faster by 4.2% at N=200, 5.5% at N=1,000, and 3.7% at
  N=3,000 in this rerun (within run-noise range); cold cost still includes exact core
  builds plus per-operation fact materialization.
- Instrumented counters are not clean timings; clean paired timings are separate.
- `NOT_ADMINISTERED` remains outside the C11/I03 typed state contract; no state was
  invented.
- P3 bitmap/posting index and P4 new persistent engine were **not built** and are
  not warranted by these measurements.

## Nested PROGRAMMA delta

Tied to `ROADMAP:S03.3`, `S-I03`, W05/P03/P04 and `ROADMAP:S04.1–S04.4`: P2
compatible exact core reuse is implemented with per-operation native fact/replay
preservation; the measured warm economy is ~3× on the compatible synthetic mix,
explicit single-op overhead −2.5% to +10.9%, and incompatible-work first-pass
overhead +0.8% to +3.9% at N=1,000/3,000. W05/P04 fact/replay construction remains
per operation.
No scientific contract change is proposed. Qualified guide write-through remains
HQ's duty; this is not a second guide.

## Phase-3 measured compact comparison and compact-grouped result

`tools/bench_compact_current.py` ran N=200 and N=1,000 with fresh processes for
V0 (full native), V1 (default compact Arrow), V2-cold and V2-warm (same compact
facade with explicit workload-owned Parquet/Zstd cache). All four variants used the
same sealed source/projection/release; full `EmpiricalFact.as_dict()` material was
equal for every operation, and V2 cold miss/write plus warm HIT were verified.

Compact comparison highlights (sourcefree, tiny synthetic fixture; not all35):

| N | variant | parent wall | validation | compact conversion | query | fact+replay | peak RSS | cache bytes |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 200 | V0 native | 6.18 s | 2.67 s | n/a | 1.70 s | 0.39 s | 63.2 MB | n/a |
| 200 | V1 compact | 6.56 s | 1.94 s | 1.97 s | 1.14 s | 0.29 s | 135.0 MB | n/a |
| 200 | V2 cold | 5.40 s | 1.87 s | 1.04 s | 1.03 s | 0.28 s | 142.2 MB | 318,780 |
| 200 | V2 warm | 4.34 s | 1.78 s | 0.33 s | 1.04 s | 0.28 s | 109.5 MB | 318,780 |
| 1000 | V0 native | 21.29 s | 9.24 s | n/a | 6.15 s | 1.51 s | 153.8 MB | n/a |
| 1000 | V1 compact | 21.76 s | 9.61 s | 2.27 s | 5.28 s | 1.54 s | 263.4 MB | n/a |
| 1000 | V2 cold | 21.55 s | 9.20 s | 2.36 s | 5.17 s | 1.52 s | 272.3 MB | 1,716,950 |
| 1000 | V2 warm | 21.03 s | 9.92 s | 0.74 s | 5.82 s | 1.69 s | 265.7 MB | 1,716,950 |

V2 warm removes most compact-conversion cost, but total wall remains dominated by
validation/query/fact and is not materially better than V0 at this fixture. The
compact path is higher RSS at both sizes; phase-1's cross-setup memory comparison is
not used as a controlled claim.

Compact-release grouped measurement reused the same fixture/release and actual
first consumer (not a native tuple benchmark):

| N | cold no-scope / grouped | warm no-scope median | warm grouped median | speedup | single-op Δ | incompatible-first Δ | oracle |
|---:|---:|---:|---:|---:|---:|---:|---|
| 200 | 1.576 / 1.284 s | 1.422 s | 0.593 s | 2.40× | +47.9% | −3.6% | PASS |
| 1000 | 6.774 / 6.228 s | 6.724 s | 2.656 s | 2.53× | +9.0% | +25.4% | PASS |

Grouped counters on the compact source-backed release reduced routing/predicate/
target calls from 22,001/13,428/10,294 to 2/2/2 at N=1,000 (the 2 are the unsupported
negative fallback); weight calls fell from 10,294 to 1,715. Capacity fallback with
`max_groups=1` was exact but slower (+46.8% at N=200, +60.8% at N=1,000), so fallback
economy is **unproven**. R03's P41 82–92 fallbacks remain a nonblocking limit, not
authority to rewrite production.

No extra bitmap/index, new carrier, persistent truth, blanket cache default, or
owner acceptance was introduced. Delete/corrupt/stale/revoke remain existing-test
coverage and were **NOT_RUN** here. No N=3000 was run; N=200/1,000 resolved the
comparison.

### Capacity-miss guard (new implementation/test)

The measured capacity-full duplicate was fixed only in
`I03GroupedExecutionScope.evaluate` at implementation/test SHA
`9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3`: an exact early guard skips core
construction on a cache MISS when the group cap is reached or already-cached
denominator members have reached the member cap. The HIT path remains before the
guard, so full-capacity cores still reuse. When the prospective member size is
unknown, the existing post-build member fallback remains; no eviction/LRU,
capacity-default, or prospective-size estimate was added.

N=200 compact same-release paired capacity-full result, 3 interleaved rounds:

| case | miss median wall | core build attempts | core builds | early capacity fallback | exact facts |
|---|---:|---:|---:|---:|---|
| before (early guard disabled) | 0.3383 s | 2 | 1 | 0 | PASS |
| after (current guard) | 0.2001 s | 1 | 1 | 1 | PASS |
| no-scope | 0.1989 s | n/a | n/a | n/a | PASS |

The full-capacity HIT remained reusable (`core_hits=1`), and the unsupported/member
bound cases remain honest fallbacks. This narrows the capacity-full duplicate only;
it does not claim a whole-L03 or production-scale completion.

## Read next

1. `01_BASELINE_CURRENT_CODE_ABI.md` — Phase-1/2 ABI and Phase-3 measured chain/result.
2. `02_EXACT_COST_AND_MEMORY_RESULTS.jsonl` — Phase-1/2/3 costs and scope/counter receipts.
3. `03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl` — exact parity and selected full fact material.
4. `04_REPLAY_AND_AUTHORITY_INVALIDATION.md` — replay/authority/cache/grouped negatives.
5. `05_OPTION_MATRIX_AND_MINIMAL_DELTA.md` — implemented delta, W03/W04 matrix, measured disposition.
6. `06_INDEPENDENT_REVIEW_REQUEST.md` — R03 acceptance context and Phase-3 evidence.
