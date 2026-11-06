# PROGRAMMA PYAT L03 / C4 — Phase-2 implemented grouped economy

**Status:** PHASE-2 COMPLETE / P2 IMPLEMENTED AND FROZEN / PHASE-3 COMPARISON DRIVER PREPARED, NOT RUN.
**Preparation commit:** `__PREP_SHA__` (artifact-only; frozen implementation remains `409be32f7e4b4b961a360be1c8f44a17b5c62173`).
**Branch:** `perf/programma-pyat-w05-p03-f1f4-grouped-economy-20261105-r1`
**Base:** `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`
**Phase-1 checkpoint:** `05a9abccded29dfcf7e27b5febcecb4442c8714d` (artifact `da7be66893217175f9301717c7f1693e6ca89ed8`)
**Implementation SHA:** `409be32f7e4b4b961a360be1c8f44a17b5c62173`
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

## Phase-3 preparation: compact physical comparison driver (NOT RUN)

`tools/bench_compact_current.py` is prepared and tiny-smoke checked. It performs a
same-sealed-source/release/projection comparison, not an architecture bakeoff:

- **V0:** full validated native `C11LogicalRelease` + `C11Repository` + actual
  `CarrierNeutralResearchExecutor.execute_i03`.
- **V1:** existing default compact Arrow facade (`build_source_backed_c11_repository`).
- **V2-cold / V2-warm:** same compact facade with an explicit workload-owned private
  existing Parquet/Zstd cache root. V2 uses an `ExactPhysicalCellStream` with a
  non-empty `decoder_metadata_digest`; the coordinator verifies cold miss/write and
  warm HIT. A legacy in-memory `PhysicalSourceIncidence` with
  `physical_binding=None` is explicitly not used as a cache HIT.

Each variant runs in a **fresh process**; the coordinator runs variants sequentially
and compares **full `EmpiricalFact.as_dict()`** (cells, refs, provenance, replay) per
operation against V0. N=200 and N=1,000 are separately invocable. Tiny N=3 smoke
passed with exact facts, equal release/source identity, and V2 cold miss/write plus
warm HIT.

**Timings are NOT_RUN here.** The R03 reviewer owns the timed runner. HQ may run the
following after R03 releases it:

```sh
RUNNER=/tmp/rawlsing-oct28-p1r1/venv/bin/python
TMPDIR="$PWD/.local-logs/pyat-l03-c4/tmp" PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 "$RUNNER" WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py   --mode compare --n 200 --outdir .local-logs/pyat-l03-c4/compact_compare/n200
# then n=1000 with a distinct outdir
```

Cold/warm are included. Delete/corrupt/stale/revoke remain covered by existing
functional cache tests, referenced in `04_REPLAY_AND_AUTHORITY_INVALIDATION.md`;
they are **NOT_RUN** in this preparation. No extra bitmap/index, new carrier,
persistent truth, blanket cache default, or owner acceptance is introduced.

## Read next

1. `01_BASELINE_CURRENT_CODE_ABI.md` — Phase-1 ABI, Phase-2 grouped ABI, W03/W04 chain.
2. `02_EXACT_COST_AND_MEMORY_RESULTS.jsonl` — Phase-1/2 costs; Phase-3 driver NOT_RUN.
3. `03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl` — exact parity and Phase-3 NOT_RUN status.
4. `04_REPLAY_AND_AUTHORITY_INVALIDATION.md` — replay/authority/cache/grouped negatives.
5. `05_OPTION_MATRIX_AND_MINIMAL_DELTA.md` — implemented delta, W03/W04 matrix, driver plan.
6. `06_INDEPENDENT_REVIEW_REQUEST.md` — R03 request against the frozen implementation.
