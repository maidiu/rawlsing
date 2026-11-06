# PROGRAMMA PYAT L03 R03 — Phase-3 compact evidence assessment

**Status:** `ACCEPT_SCOPED_PHASE3_EVIDENCE`; `W03_W04_ECONOMICAL_COMPACT = NOT_FULFILLED`;
`WHOLE_L03_NOT_COMPLETE`
**Reviewer:** same independent R03 reviewer as published review
`e2f6c1649801b42a475ce3d81f3d85a7c5ccb5b3`. Not the implementation author, not an
original35/source/actor/human/Sorok authority. No protected merge, native science,
or scientific-owner claim.
**Frozen implementation:** `409be32f7e4b4b961a360be1c8f44a17b5c62173`
**Author phase-3 evidence head:** `141df637d49281fa1d33fa6ad275e09f0f6bd9d4`
**Author measurement commit:** `a85df66ec93a951d8fd50d751822b70569df94ef`
**Production/tests:** unchanged at `409be32` (verified: all six production/test
blobs are identical at `409be32`, `a85df66e`, and `141df637`).
**Original P2 acceptance preserved:** `ACCEPT_SCOPED_P2` for the bounded grouped
core remains in force; this phase-3 addendum neither extends it to whole L03 nor
re-reviews future code.

## Scope

Assessed only the new author compact phase-3 evidence:

- `results/compact_current_summary.json`
- `results/compact_current_commands.jsonl`
- new `compact_current_*` entries in `02_EXACT_COST_AND_MEMORY_RESULTS.jsonl`
  and `03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl`
- updated `00`, `01`, `05`, `06`
- `tools/bench_compact_current.py` and `tools/finalize_compact_current.py`

No source, test, guide, cache-policy, or protected branch was edited. No timed
measurement, heavy fixture run, N=3000 run, or capacity-guard repair review was
performed. The reviewer did not wait for or review the separately assigned
capacity-guard repair code; that future frozen repair review remains outstanding.

## Verdict

| Field | Verdict | Basis |
|---|---|---|
| Phase-3 evidence integrity | **PASS_SCOPED** | Driver logic, summary/JSONL consistency, selected full facts reviewed; full per-op sidecars remain untracked author files (evidence boundary below) |
| V0/V1/V2 compact comparison exactness | **PASS** | Same source/projection/release; full fact material/digests/refs/replay equal; V2 cold miss/write and warm HIT verified |
| Compact peak RSS / total-wall result | **PASS_AS_MEASURED** | Compact RSS is higher than native; warm cache reduces compact conversion but not materially total wall at N=1,000; N=200 total-wall delta is single-run/small-N noise |
| Compact grouped economy | **PASS_SCOPED** | Warm medians 2.40× (N=200) / 2.53× (N=1,000), full-oracle PASS, exact facts; round-1/round-noise and overhead caveats below |
| W03/P01 exact current function | **PASS** | Source-backed compact first reader is present/composed; no exact function/source/authority gap found |
| W03/W04 economical compact capability | **NOT_FULFILLED** | One proven first-reader physical deficit: compact cold/peak-memory economy worse than native, warm cache does not materially improve total wall at N=1,000 |
| W04 default persistent acceleration | **COMPETENT-OWNER BOUNDARY** | Optional env-gated exact Parquet/Zstd capability present; default activation is a policy decision, not a missing codec/engine; no blanket default |
| Whole L03 | **NOT_COMPLETE** | Functional evidence exists, but selected economical compact/cold-memory/default capability is not fulfilled |
| Capacity-guard repair | **NOT_REVIEWED / NOT_RETURNED** | Concurrently assigned author repair has not returned; no imaginary code reviewed |
| Phase-3 disposition | **ACCEPT_SCOPED_PHASE3_EVIDENCE; W03/W04 INCOMPLETE** | No source change authorized; preserve accepted P2 scope and negative evidence |
| Next work | **COMPETENT-OWNER W03/W04 DECISION + FUTURE FROZEN CAPACITY-REPAIR REVIEW** | No new architecture court/default-policy invention |

## Claims verified

### V0/V1/V2 exact comparison (N=200, N=1,000)

- Same sealed source SHA, projection identity, and C11 `release_ref` across V0
  (native), V1 (default compact Arrow), V2-cold, V2-warm.
- V2 uses the actual `ExactPhysicalCellStream` with non-empty
  `decoder_metadata_digest`; the legacy in-memory-incidence path is not used as a
  cache HIT.
- The driver writes full `fact.as_dict()` per operation and compares the full
  lists, including authority refs, dependency/provenance refs, cells, fact ref,
  and replay ref. It is not a checksum-only oracle.
- I independently checked the retained summary and `02` JSONL: 104
  `compact_current_query` rows (13 ops × 4 variants × 2 sizes), zero mismatches in
  `exact_fact_material_sha256`, `fact_refs`, `replay_refs`, or typed states
  against V0. The selected full `raw_Y` facts for V0/V1/V2-warm and grouped
  baseline/candidate are exactly equal as full dictionaries.
- V2-cold read miss/write and V2-warm read HIT are true; the same cache file list
  is reused.

Measured comparison (whole-process Darwin `ru_maxrss` bytes; MB here =
bytes/1,000,000, as in the author table):

| N | Variant | Parent wall | Peak RSS | Cache bytes | Compact conversion |
|---:|---|---:|---:|---:|---:|
| 200 | V0 native | 6.18 s | 63.2 MB | — | — |
| 200 | V1 compact | 6.56 s | 135.0 MB | — | 1.97 s |
| 200 | V2 cold | 5.40 s | 142.2 MB | 318,780 | 1.04 s |
| 200 | V2 warm | 4.34 s | 109.5 MB | 318,780 | 0.33 s |
| 1,000 | V0 native | 21.29 s | 153.8 MB | — | — |
| 1,000 | V1 compact | 21.76 s | 263.4 MB | — | 2.27 s |
| 1,000 | V2 cold | 21.55 s | 272.3 MB | 1,716,950 | 2.36 s |
| 1,000 | V2 warm | 21.03 s | 265.7 MB | 1,716,950 | 0.74 s |

The compact path is ~1.7× native peak RSS at N=1,000. Warm cache reduces compact
conversion from 2.27 s to 0.74 s but total wall is roughly flat versus V1/V0
(21.03 vs 21.76/21.29 s). The N=200 V2-warm total wall is 30% below V0 in this
single fresh-process run; there are no repeated comparison rounds, so that small-N
difference is not a stable economy claim. The N=1,000 comparison is the stronger
result and does not show material total-wall benefit.

### Compact grouped economy (actual compact source-backed release)

The grouped measurement uses `build_source_backed_c11_repository(...)` and the
actual `CarrierNeutralResearchExecutor.execute_i03`, not a native tuple benchmark
or private kernel label. It includes 16 operations (1/2/3/4 targets, both
conditional directions, XOR, minority, routed/asymmetric risk, typed missing M,
zero support, unsupported ordered target, valid ordered target, weighted/raw and
siblings).

| N | Cold no-scope / grouped | Warm no-scope median | Warm grouped median | Headline speedup | Warm round speedups | Single-op Δ | Incompatible Δ | Capacity Δ | Oracle |
|---:|---:|---:|---:|---:|---|---:|---:|---:|---|
| 200 | 1.576 / 1.284 s | 1.422 s | 0.593 s | 2.40× | 2.38, 2.40, 2.22 | +47.9% | −3.6% | +46.8% | PASS |
| 1,000 | 6.774 / 6.228 s | 6.724 s | 2.656 s | 2.53× | 1.97, 2.57, 2.48 | +9.0% | +25.4% | +60.7% | PASS |

- Full facts are equal for cold, every warm round, single-operation, incompatible
  first pass, and capacity fallback; the row oracle checks 16 operations and
  reports no errors.
- Counters at N=1,000 reduce routing/predicate/target calls
  22,001/13,428/10,294 → 2/2/2; weight calls 10,294 → 1,715. The two residual calls
  are the unsupported negative fallback. This is actual shared work, not a
  final-fact memo.
- The headline speedups are medians of three warm rounds. N=1,000 round 1 is only
  1.97×; rounds 2–3 are 2.57×/2.48×. N=200 rounds are 2.38×/2.40×/2.22×. The
  measurement is paired but the first warm round and small-N noise matter.
- Warm per-op timings include `gc.collect()` and full `fact.as_dict()`
  materialization/hash for equality on both baseline and candidate. Function
  counters are a separate pass. The timings are therefore not fully
  uninstrumented, but the overhead is applied to both paths and the counters
  confirm the work reduction.
- Single-operation overhead on the compact path is much larger than the native
  phase-2 result (+47.9% at N=200, +9.0% at N=1,000), and incompatible-first cost
  at N=1,000 is +25.4%. These are honest measured regressions, not overclaimed.
- Capacity fallback was probed with `max_groups=1` and two operations: exact but
  +46.8%/+60.8% slower. This is a forced budget probe, not default behavior. The
  earlier P41 observation of 82–92 capacity fallbacks per discovery-bearing scope
  remains a nonblocking limit; the separately assigned capacity-guard repair has
  not returned and was not reviewed.

## W03/W04 engineering disposition

### Current composed exact function — present

- W03/P01 exact source-backed first-reader function is present and composed:
  physical stream → governed candidate → complete I02 validation → sealed
  release → compact view → exact I03 facts. V0/V1/V2 full facts, source,
  projection, release, refs, and replay are equal on the small synthetic
  N=200/1,000 fixture.
- W04/P02 exact optional capability is present: default in-memory compact Arrow
  when pyarrow is installed, optional authenticated env-gated Parquet/Zstd
  event-body cache, plus `ParquetC11Carrier`/R4/R5 components. No missing
  codec/engine was found.
- This is **not** a declaration of full functional equivalence or production
  readiness; it is a small-fixture, sourcefree exactness result.

### Selected economical compact capability — one proven first-reader deficit

**The compact source-backed first reader is not economical in cold construction /
peak memory.** At N=1,000, same sealed source and first consumer, the compact
path peaks at 263.4 MB (V1), 272.3 MB (V2-cold), or 265.7 MB (V2-warm) versus
153.8 MB native. Warm persistent conversion reduces compact-conversion time
(2.27→0.74 s) but total wall remains roughly flat versus native/V1 (21.03 vs
21.29/21.76 s). The cold path still materializes the full native
candidate/validation object set before producing the compact view; the cache
accelerates body reading, not the cold peak.

That is the single precise remaining first-reader physical deficit for the
selected economical compact/hybrid goal. It is proven on the small synthetic
fixture; it is not proven at original35/production scale. The smallest next
proof, if HQ requires the economy claim, is a bounded same-sealed-release
cold/warm compact-vs-native run at representative scale with an explicit
peak-memory/cold-time budget, not a new engine. No streaming/lazy rewrite is
authorized by this assessment.

### Default persistent acceleration — competent-owner boundary

With `RAWLSING_C11_ACCELERATOR_DIR` unset, `_cache_directory()` returns `None`;
the default in-memory compact view still exists, but no persistent Parquet/Zstd
slot is written. If the selected W04 requirement demands default persistent
activation, that is an explicit policy/default decision for the competent owner,
not a missing codec/engine and not a reviewer grant. The latest no-blanket-cache
constraint remains binding; this review does not invent or activate a default.
If functional equivalence plus optional caller-configured cache is accepted, the
exact function is present; the unresolved item is the economy deficit above,
not a missing API.

### Capacity guard repair

The concurrently assigned capacity-guard repair is **not returned**. I did not
inspect imaginary code, wait, or extend scope. The phase-3 capacity probe above
is measurement evidence only; the future frozen repair review remains
outstanding.

## Evidence boundary

- The author’s full per-operation fact sidecars (`v0_facts.jsonl`,
  `v1_facts.jsonl`, `v2-*_facts.jsonl`, grouped cold baseline/candidate files)
  are untracked paths in the author workspace and were absent from this checkout.
  I reviewed the driver’s full-list comparison logic, the retained summary/JSONL
  per-query hashes/refs/replay, and the selected full `raw_Y` facts (V0/V1/V2-warm
  and grouped baseline/candidate), which are exactly equal. I did **not**
  independently inspect every full per-op provenance byte for all 13 comparison
  operations; that is the exact evidence boundary, not a checksum-only oracle.
- No N=3,000, original35, production, or cross-machine measurement was performed.
- The compact comparison is one fresh-process run per variant; grouped mode has
  three warm rounds. No reviewer timed run was performed in this phase.
- No native/original35, scientific, Sorok, actor/human, or production claim is
  made.

## PROGRAMMA_DELTA (ordinary return; not a guide write-through)

- `ROADMAP:S03.2`, W03/P01: **exact source-backed compact first-reader function is
  present/composed on the small fixture; selected economical cold/peak-memory
  capability is NOT fulfilled. One precise deficit: compact peak RSS ~1.7× native
  at N=1,000 with no material total-wall economy from the warm cache.**
- `ROADMAP:S03.2`, W04/P02: **exact optional compact/Parquet-Zstd capability is
  present and authenticated; default persistent activation is a competent-owner
  policy boundary under no-blanket-cache-default, not a missing engine.**
- `ROADMAP:S03.3`, W05/P03/P04: **accepted P2 scope, per-operation facts/replay, and
  negative evidence are preserved. Compact grouped warm medians 2.40×/2.53× are
  scoped measurement evidence; they do not extend the acceptance to whole L03.**
- Capacity fallback: **exact but slower; forced `max_groups=1` probe +46.8%/+60.8%;
  P41 capacity-pressure limit remains; future frozen capacity-guard repair review
  outstanding.**
- W03/W04: **not declared complete; default regenerable capability not erased; no
  new default policy, cache-policy grant, architecture court, or scientific owner.**
- No production/source/test/guide/protected merge, native/original35/Sorok/human
  claim, or new measurement owner is created.

## Artifact map

- `01_EVIDENCE_REVIEW.md` — commits, unchanged blobs, driver review, measurement
  classification, evidence boundary.
- `02_COMMANDS_AND_NOT_RUN.jsonl` — read-only commands and explicit NOT_RUNs.
- `03_W03_W04_DISPOSITION.md` — detailed W03/W04 table and one-deficit statement.
- `evidence/phase3_compact_extract.json` — compact extraction of author
  comparison/grouped metrics.
- `evidence/phase3_jsonl_consistency.json` — 104-row per-query hash/ref/replay
  consistency audit and grouped equality flags.
- `evidence/phase3_selected_full_fact_equality.json` — selected raw_Y full-fact
  equality and provenance summary.
