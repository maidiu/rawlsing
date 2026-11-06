# PROGRAMMA PYAT L03 R03 — independent sourcefree review

**Status:** `ACCEPT_SCOPED_P2_FOR_HQ_RECEIVING` / `WHOLE_L03_NOT_COMPLETE`
**Role:** independent R03 numerical/physical review. I am not the implementation
author, not an original35/source respondent, and not source/actor/human/Sorok
authority. No protected merge, native science, or scientific-owner claim is made.
**Branch:** `review/programma-pyat-l03-r03-grouped-20261106-r1`
**Frozen implementation:** `409be32f7e4b4b961a360be1c8f44a17b5c62173`
**Protected base:** `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`
**Evidence final head:** `f3dcdf4d92d85897e1db360e70445b0cf170e986`
(records only the frozen implementation SHA; the six production/test blobs at
`409be32` are byte-identical at `f3dcdf4d`, verified by blob SHA)
**Binding commission:** `66cedcdf01cd156d0024419957b5c34832ebf8a5`:
`WORKER_COMMISSIONS/PROGRAMMA_PYAT_F2F4_GF1_RECOVERY_20261105_R1/04_HYB_COMPACT_GROUPED_KWAY_QUERY_BENCHMARK.md`
**Seven C4 artifacts:** `WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/`
**Write scope:** this return plus `.local-logs/pyat-l03-r03` only. No production
source, source guide, protected branch, cache policy, or global configuration was
edited.

## Verdict

| Field | Verdict | Independent basis |
|---|---|---|
| Numerical correctness | **PASS** | Independent row-level oracle matched all 13 operations; full `EmpiricalFact.as_dict()`, fact ref, and replay ref equal baseline vs grouped for every operation |
| Economic benefit | **PASS_SCOPED** | N=200 paired warm 3.05–3.09×; author N=1,000/3,000 3.07–3.25× not independently rerun; discovery/capacity-bound path not shown cheaper |
| Actual first consumer | **PASS** | `execute_i03`, `execute_i05`, issued Batch, and P41/issued path all exercise the scope; P41 grouped vs forced-unshared hashes equal |
| W03/W04 completeness | **PARTIAL / WHOLE_L03_NOT_COMPLETE** | Default Arrow compact view and optional authenticated Parquet/Zstd cache exist; economical cold construction/lower peak memory remains unresolved; grouped benchmark used a native tuple release, not the compact source-backed release |
| `R03_DISPOSITION` | **ACCEPT_SCOPED_P2_FOR_HQ_RECEIVING** | No material correctness defect found in the bounded P2 diff; not a whole-L03 pass |
| `NEXT_WORK` | **HQ_RECEIVING_SCOPED_P2; W03/W04 FOLLOW-UP** | Optional bounded capacity pre-check is recommended below; no new engine/architecture bakeoff |

Component verdicts for the C4 review-request fields:

- `IMPLEMENTATION_SCOPE`: **PASS** — exactly five production files plus one test
  file changed under `rawlsing_next/`; the implementation commit also updates its
  own C4 artifacts.
- `CORE_KEY_COMPLETENESS`: **PASS** — release/replay/source-manifest/semantic
  hashes, universe, attested index object, respondent root, risk set/type/source
  scope/response-state semantics, predicate + grammar authority, complete target
  plan (targets, topology, domain, domain replay, topology/response authorities,
  included states, joint order, full domain), query authority refs, registry
  fingerprint, contract/schema version marker, and a measure-independent marker
  are keyed. Occurrence/rank semantics are carried by the exact target topology,
  domain, and sealed event content; they are not a free mutable parameter.
  Measure/weight/design are deliberately excluded from the key and recomputed per
  operation.
- `MEASURE_INDEPENDENT_CORE_SOUNDNESS`: **PASS** — no weighted cell, weighted
  denominator, or final fact is stored in the core; every RAW/GOVERNED_WEIGHTED
  materialization revalidates its own authorities and calls `_weight_for` per
  denominator member. A W2 weight-basis refusal matched the unshared negative.
- `PER_OPERATION_FACT_REPLAY_PROVENANCE`: **PASS** — `_build_fact` and
  `_make_execution_replay_ref` ran 13/13 times in the warm counter pass; full fact
  material, provenance refs, dependency refs, and replay refs matched baseline for
  every operation. `_UsedObjectAccumulator` / `_UsedAuthorityAccumulator`
  deduplication and the final canonical ref ordering produced the same
  provenance/authority material as the unshared path.
- `ACTUAL_SHARED_WORK_EVIDENCE`: **PASS** — cold scope built 11 exact cores with 2
  compatible hits; warm counter pass collapsed routing/predicate/target calls from
  `3800/2500/2002` to `0/0/0` and kept `200` per-operation weighted calls at N=200.
  This is shared computation, not a final-fact memo.
- `INCOMPATIBLE_AND_NEGATIVE_PARITY`: **PASS** — different targets, arities,
  conditional directions, XOR/minority conditioners, risk sets, releases,
  universes, authority registries, runtime binding, missing/wrong weight, zero
  support, special typed states, authority DENY, and unsupported topology all
  matched baseline. `SOURCE_INDEXED_MULTI_UNIVERSE` still emits one exact fact per
  universe; `AUTHORIZED_COMPOSITE` with multiple indices bypasses the shared-key
  path. Semantically different respondent/risk/weight/release/authority scopes
  did not cross-publish `SUPPORTED` in the focused or independent checks.
- `POISON_REBUILD_CLEANUP`: **PASS** — five independent core-poison variants
  (`raw_cells`, `fact_state`, `cell_by_respondent`, `used_objects`,
  `used_authority_refs`) were detected and refused; repository index cut rebuilt
  from the sealed release; exact index restore reused only its own core; scope
  close/error cleared state. The fingerprint is an accidental/stale-corruption
  check, not an adversarial recomputed-hash defense (out of the accepted threat
  scope).
- `ISSUED_BATCH_I05_P41_INTEGRATION`: **PASS** — the 100-test focused suite passed;
  the P41 same-source test passed; the issued path created three owned scopes and
  used the scope for query and discovery work; P41 grouped vs forced-unshared
  hashes, view hash, state, and consumer values were identical.
- `PAIRED_MEASUREMENT_INTEGRITY`: **PASS_SCOPED** — my N=200 paired run reproduced
  the direction and rough magnitude; N=1,000/3,000 were only audited in retained
  artifacts; the benchmark release is native `tuple`, so compact source-backed
  timing is not independently established.
- `W03_W04_CLAIM_SAFETY`: **PASS** — the author states W03/W04 as unresolved and
  does not claim native/original35 completion. Completeness remains partial, not
  silently canceled.
- `R03_DISPOSITION`: **ACCEPT_SCOPED_P2_FOR_HQ_RECEIVING**.
- `NEXT_WORK`: **HQ_RECEIVING_SCOPED_P2; W03/W04 FOLLOW-UP**.

## Independent evidence (this review)

Environment: `oldMac.lan`, macOS 13.7.8, Darwin 22.6.0 x86_64, 16 logical CPUs,
17,179,869,184 bytes physical memory; Python 3.11.3, pyarrow 22.0.0, pandas 3.0.6,
pytest 9.1.1; runner `/tmp/rawlsing-oct28-p1r1/venv/bin/python`. All outputs and
TMPDIR under the assigned checkout; no new packages or global config.

Commands and results:

| Check | Result |
|---|---|
| `pytest ... test_pre553_i03_grouping.py` | 11 passed in 5.30 s |
| Focused 8-suite (grouping, empirical query, carrier, compact view, discovery, hostile frontier, Route B, issued custody) | 100 passed in 28.15 s |
| `test_universal_world_binding.py::test_same_source_r04_partial_resume_reaches_actual_p41` | 1 passed in 47.84 s |
| `bench_grouped_phase2.py --scenario main --n 200 --rounds 3` | 3 warm paired rounds, exact parity, 3.05–3.09× |
| Reviewer-authored independent oracle / cut / restore / poison / refusal script | PASS |
| P41 scope probe (owned issued scopes) | 3 scopes; builds/hits used; 64-group cap reached on discovery-bearing scopes |
| P41 grouped vs forced-unshared probe | hashes equal; view hash/state/consumer values equal |
| W03/W04 compact/cache probe | default `_CompactPublicObjects`; env-gated one Parquet slot, 19,333 bytes, reused |

### Paired N=200 (my run, native C11 release through the real executor)

The runner alternates a full baseline pass and a full grouped pass per round
(paired passes, not per-operation interleaving), using the same sealed release
object and fresh repositories.

| Metric | Baseline (no scope) | Grouped candidate |
|---|---:|---:|
| Cold wall / CPU | 1.3547 s / 1.3522 s | 1.2948 s / 1.2937 s (−4.4% wall) |
| Warm wall, rounds 1/2/3 | 1.2739 / 1.2533 / 1.2663 s | 0.4161 / 0.4107 / 0.4100 s |
| Warm speedup, rounds 1/2/3 | — | 3.06× / 3.05× / 3.09× |
| Single-op explicit scope | 0.1347 s | 0.1458 s (+8.2%) |
| Incompatible first pass (7 ops) | 0.7185 s | 0.7112 s (−1.0%, run noise) |
| Peak RSS (Darwin `ru_maxrss` bytes) | — | 92,553,216 bytes (process high-water) |
| Cold index builds / core builds / hits | 1 / — / — | 1 / 11 / 2 |
| Warm work counters routing/predicate/target/weight | 3800 / 2500 / 2002 / 2002 | 0 / 0 / 0 / 200 |
| Fact/replay construction | 13 / 13 | 13 / 13 |
| Persistent source-cache bytes | 0 (`RAWLSING_C11_ACCELERATOR_DIR` unset) | 0 |

Noise: the single-op and incompatible deltas are small and varied by run
(author: −2.5% to +10.9% single, +0.8% to +3.9% incompatible). I report my run,
not a restatement of the author’s numbers.

### Independent discriminating checks

A reviewer-authored script (not the implementation test) built the same sealed
source and compared baseline vs grouped through `CarrierNeutralResearchExecutor`
against a row-level oracle computed from the fixture rows:

- All 13 operations: exact typed state, raw support/denominator, risk and
  denominator member sets, complete cell projection, weighted cells/denominator,
  fact ref, replay ref, and full fact material matched.
- Same-world cut: removing the repository’s attested index rebuilt it from the
  sealed release; 11 new cores, exact facts; restoring the exact prior index
  object reused its own 11 cores and 2 intra-mix hits without cross-rebuild reuse.
- Poison: five core-field variants were detected by the stored fingerprint and
  refused; no forged `SUPPORTED` fact escaped; restoring the true core resumed
  exact execution.
- Refusal: a W2 query over W-only weights produced the same
  `UNAVAILABLE`/`MEASURE_UNAVAILABLE` fact with and without the scope.
- Zero support and the special MISSING/DK/REFUSAL/IAP/NOT_ASKED fixture matched
  the accepted baseline fact; `NOT_ADMINISTERED` remains absent from the I03
  typed state contract and was not invented.

Refusal receipts (baseline == candidate in each case):

- W2 weight basis: `UNAVAILABLE` / `MEASURE_UNAVAILABLE`, same fact ref.
- Nonpositive predicate grammar: `UNAVAILABLE` /
  `MISSING_REQUIRED_AUTHORITY`.
- Empty exact condition: `ZERO_SUPPORT`.
- Unsupported response topology: `UNRESOLVED` /
  `UNSUPPORTED_RESPONSE_TOPOLOGY`, no core built.

## Limits and honest gaps

1. **Whole L03 is not complete.** W03/W04 economical cold construction and lower
   peak memory are unresolved. The selected physical capability is present:
   default in-memory compact Arrow view when pyarrow is installed, plus optional
   caller-configured authenticated Parquet/Zstd event-body acceleration. The
   remaining physical requirement is economical cold build / peak-memory
   behavior on the real compact source-backed first consumer, not a missing
   semantic API. W03/W04 must not be erased or declared complete by this review.
2. **Grouped benchmark is native, not compact.** The retained N=200 summary says
   `release_public_objects_class: "tuple"`. The speedup is therefore demonstrated
   on the native C11 index, not the compact source-backed release. Compact parity
   is exercised by the c11-execution-view/Route-B/custody tests, but compact
   grouped timing is not independently measured here.
3. **N=1,000/3,000 were not rerun.** I audited the retained per-op parity and
   cost artifacts (39 phase-2 op entries = 13 ops × 3 sizes, plus pass/selected
   full-fact entries) and reran N=200 only, as commissioned. Author N=1,000/3,000
   numbers remain author claims.
4. **Raw untracked C4 logs were not present in the assigned checkout.** The
   `.local-logs/pyat-l03-c4` raw JSON referenced by the author was absent; I used
   the tracked `02`/`03` JSONL, `results/*.json`, and focused reruns. The full
   N=200 raw JSON is retained locally at
   `.local-logs/pyat-l03-r03/evidence/review-grouped-n200.json`; only its compact
   summary is committed.
5. **Capacity behavior is safe but not economical under discovery pressure.**
   In the P41 issued path, discovery-bearing scopes reached `max_groups=64` and
   recorded roughly 82–92 `capacity_fallbacks` per scope while still producing
   exact output. The capacity check happens after a full core build, so a
   capacity miss performs a discarded full core computation before falling back
   to the unshared path. This is a performance limitation, not a wrong-fact
   defect. A narrow follow-up would check/evict before building (or account for
   risk members, not only denominator members) and pair-measure a discovery-heavy
   workload. No source repair is required for scoped acceptance.
6. **Fingerprint scope.** The core fingerprint detects stale/poisoned cache fields
   within the accepted in-process corruption model. It is not a defense against
   an attacker who can recompute the fingerprint after arbitrary cache mutation;
   that is outside the commissioned same-UID threat scope.

## PROGRAMMA_DELTA (ordinary return)

- `ROADMAP:S03.3`, `S-I03`, W05/P03: **scoped P2 exact execution-local grouped
  measure-independent core reuse is numerically exact in the reviewed synthetic
  scope; warm compatible-query economy reproduced at N=200 (3.05–3.09×), with
  N=1,000/3,000 retained-author-only.**
- `ROADMAP:S04.1–S04.4`: **no scientific contract change; separate native facts,
  cells, typed zeros, denominators, provenance, replay, weights, and directional
  products preserved.**
- W05/P04: **fact/replay/provenance construction remains per operation; no final
  fact memo, no grouped aggregate publication, no canonical identity/ABI change.**
- W03/P01: **existing sealed C11 execution and default compact Arrow realization
  retained; no rewrite claimed.**
- W04/P02: **optional authenticated compressed persistent acceleration retained;
  default/retention/eviction unchanged; economical cold construction/memory and
  compact grouped timing remain open.**
- P3 bitmap/posting index and P4 new persistent engine: **NOT_BUILT / not
  warranted by this evidence.**
- Disclosure: **ACCEPT_SCOPED_P2, not a whole-L03 pass; W03/W04 incomplete.**
  Qualified guide write-through remains Pyat HQ’s duty; this is not a second
  guide.

## Artifact map

- `01_SCOPE_AND_EVIDENCE.md` — exact files, blobs, reviewed artifacts, method.
- `02_EXACT_COMMANDS_AND_RESULTS.jsonl` — command/result receipts.
- `03_INDEPENDENT_CHECKS.md` — oracle, cut/restore, poison, refusal, P41, W03/W04.
- `04_LIMITATIONS_AND_REPAIR.md` — capacity observation and narrow follow-up.
- `evidence/` — compact machine-readable reviewer evidence; the 6.8 MB full N=200
  raw JSON stays local-only and is not committed.
