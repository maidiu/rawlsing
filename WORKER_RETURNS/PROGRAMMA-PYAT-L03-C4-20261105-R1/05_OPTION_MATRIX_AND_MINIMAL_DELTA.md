# 05 — Five-test disposition, implemented minimal delta, and option matrix

**Status:** Phase-2 implemented and frozen for independent R03 review. Sourcefree
engineering only. No protected merge, original35, native science, actor/Sorok, or
producer acceptance is claimed.

## Implemented delta (P2)

The smallest warranted W05/P03 delta is now implemented: **bounded execution-local
compatible grouped AND-risk/target core reuse** inside the existing I03 evaluator and
actual first-consumer path.

- Core reuse is limited to measure-independent routing/risk membership, predicate
  truth, exact target cell resolution, and used object/authority material.
- Every operation still builds its own exact native `EmpiricalFact`, provenance,
  dependency refs, and replay; no final-fact or grouped-aggregate memo is used.
- Weighted aggregation and all weight validation remain per operation; no RAW/
  governed-weighted result reuse.
- Incompatible work is never cross-shared. A scope hit requires exact determinant
  compatibility; otherwise the existing unshared path executes.
- The scope is finite, context-managed, nonpersistent, and cleared on exit/error.
- Production scope: `_pre553_query_eval.py`, `pre553_empirical_query.py`,
  `pre553_carrier_execution.py`, plus minimal `pre553_discovery_exact.py` and
  `pre553_issued_workload.py` hooks to make the real I03/I05/Batch path use it.
- `_select_respondent_events` selector v1 ABI is unchanged.

## Five-test historical-function disposition

| Law field | Phase-2 answer |
|---|---|
| `HISTORY` | October W05/P03 grouped-economy capability; current code successor is the attested release-index cache plus compact body lane, now extended at the actual current I03 first consumer. No historical file/engine restoration. |
| `CURRENT_REQUIREMENT` | `ROADMAP:S03.3` / `S-I03`: compatible exact cross-operation sharing; W05/P03. `ROADMAP:S04.1–S04.4` native facts/cells/denominators/replay remain separate. |
| `CURRENT_SUCCESSOR` | **Present and now implemented:** exact release-index reuse, compact physical view, and execution-local compatible core reuse. Per-operation measure/weight, fact, provenance, and replay construction remain preserved. Disposition: **IMPLEMENTED_SCOPED**. |
| `FIRST_CONSUMER` | `CarrierNeutralResearchExecutor.execute_i03` (`pre553_carrier_execution.py:427`), Route-B caller at `pre553_route_b_production.py:582`, and the issued Batch/I05 path. The integration creates one owned scope for multi-unit workloads and passes it to query and I05 units. |
| `AUTHORITY` | Sourcefree engineering only. Per-operation identity/source/index-attestation/authority/issuance/revocation checks remain enabled. No new semantic, source, actor, weight, routing, or scientific authority. |
| `COMPARE_AND_COST` | P2 implemented and measured on identical sealed releases/workload: warm 3.07–3.25× on the compatible synthetic mix, explicit single-op −2.5% to +10.9%, incompatible first pass +0.8% to +3.9% at N=1,000/3,000. P3/P4 not built. |
| `DISPOSITION` | `REUSE_ADAPT` completed for W05/P03; no second semantic engine or persistent canonical copy. |
| `NEXT_WORK` | Independent R03 review of the frozen implementation; then HQ selects protected receiving. No further P3/P4 build from this evidence. |
| `FALSIFIER` | Any changed fact/cell/denominator/typed negative/replay/provenance on a grouped hit, any cross-scope sharing, or failure to produce a material warm-workload economy reverses the disposition. |

## Paired measured result

Identical sealed releases, fixture seeds, operation mix, and instrumentation; one
timed process at a time. Baseline is the unchanged no-scope path. Full
`EmpiricalFact.as_dict()`, fact-ref, and replay-ref equality held for every operation
at every measured size.

| N | cold baseline | cold candidate | warm baseline median | warm candidate median | warm speedup |
|---:|---:|---:|---:|---:|---:|
| 200 | 1.4159 s | 1.3585 s | 1.3433 s | 0.4140 s | 3.25× |
| 1,000 | 6.9096 s | 6.5482 s | 6.4835 s | 2.1123 s | 3.07× |
| 3,000 | 20.9967 s | 20.2396 s | 20.2322 s | 6.2198 s | 3.25× |

Selected N=3,000 warm per-op speedups: 1-target branch 3.00×, weighted 1.97×,
2-target 3.21×, 3-target 3.38×, 4-target 3.56×, forward conditional 3.32×, reverse
conditional 3.39×, XOR 4.81×, minority 3.77×, incompatible risk set 3.46×.

Actual work counters for one warm pass (not timing):

| N | baseline routing / predicate / target / weight | candidate routing / predicate / target / weight |
|---:|---|---|
| 200 | 3,800 / 2,500 / 2,002 / 2,002 | 0 / 0 / 0 / 200 |
| 1,000 | 19,000 / 12,500 / 10,010 / 10,010 | 0 / 0 / 0 / 1,000 |
| 3,000 | 57,000 / 37,500 / 30,030 / 30,030 | 0 / 0 / 0 / 3,000 |

The cold grouped pass built 11 exact cores and had 2 compatible hits for the
13-operation mix. The warm pass reused all 11 cores and materialized 13 separate
facts. This is genuine shared count/routing/predicate/target work, not a final-fact
hash memo.

## Option matrix

| Option | Status | Exactness / authority | Measured evidence | Disposition |
|---|---|---|---|---|
| **P0/P1 current no-scope path** | Present | Exact accepted I03; no new authority | Baseline measured at N=200/1,000/3,000 | **RETAIN** as oracle/fallback |
| **P2 execution-local grouped AND-risk/target** | **IMPLEMENTED** | Exact core determinants; per-operation native fact/replay; per-operation measure/weight; no cross-scope sharing | Warm 3.07–3.25×; cold −3.7% to −5.5% (candidate faster in this rerun, run-noise range); explicit single-op −2.5% to +10.9%; incompatible first pass +0.8% to +3.9% at N=1,000/3,000 | **FROZEN FOR R03 REVIEW** |
| **P3 bitmap/posting index** | **NOT_BUILT** | Would add a second physical access path | No measured benefit; P2 already removes repeated routing/predicate/target work | **NO BUILD** |
| **P4 new persistent body engine** | **NOT_BUILT** | Existing compact Parquet/Zstd lane is regenerable/authenticated | Existing cache HIT/DELETE/CORRUPT/STALE/REVOKED evidence retained | **NO NEW ENGINE** |
| **New semantic engine / canonical copy / scheduler** | Rejected | Collides with current I03/Batch ownership | None | **NO ACTION** |

## W03 / W04 physical-requirement distinction

W03/W04 remain selected physical requirements; this return does not declare them
complete and does not cancel selected capabilities.

- **Existing default in-memory compact realization:** the source-backed builder
  automatically chooses the compact Arrow view when pyarrow is installed. This is
  the current default compact realization, not new in this diff.
- **Optional authenticated compressed persistent acceleration:** Parquet/Zstd
  event-body storage is caller-configured through `RAWLSING_C11_ACCELERATOR_DIR`;
  it is regenerable and authenticated. This diff does not change its default,
  retention, eviction, or storage policy.
- **Fact cost:** per-operation fact construction was not reduced; the instrumented
  counter pass measured candidate fact time +5–9% versus baseline (0.308/0.281 s at
  N=200; 1.565/1.438 s at N=1,000; 4.532/4.219 s at N=3,000), so the economy comes
  from shared routing/predicate/target work, not from altering native fact/replay
  publication.
- **Selected exact needed function vs economical cold construction/memory:**
  W05/P03 exact sharing is implemented and measured. W03/W04 economical cold
  construction/memory remains unresolved: at N=1,000 the compact run's measured
  peak RSS was 352–384 MB versus 287.7 MB native, and source reacquisition/fixture
  construction dominates cold passes. No production/original35 claim is made.
- **No bundled compact-carrier rewrite:** no measured deficit justified one in this
  diff; the existing compact lane is retained.

## Scope and authority constraints preserved

- Query/predicate identity, source binding, index attestation, authority/issuance/
  revocation checks are never bypassed on a grouped hit.
- Runtime successor binding causes conservative unshared fallback.
- Different releases, universes, risk sets, predicates, target plans, authority
  registries, measures, weights, or runtime bindings do not cross-share.
- Expired/corrupt/wrong-respondent memo, poisoned core, and rebuilt index all
  fail closed to the exact unshared path.
- Every operation publishes its own native fact/replay; no independently
  authoritative retained fact or persistent group cache exists.

## PROGRAMMA_DELTA (ordinary return; not a guide write-through)

- `ROADMAP:S03.3`, `S-I03`, W05/P03: **P2 compatible exact core reuse implemented and
  paired-measured; warm 3.07–3.25× on the synthetic compatible mix with exact
  per-operation facts/replay; single-op and incompatible work honestly bounded.**
- `ROADMAP:S04.1–S04.4`: **no scientific contract change; separate native facts,
  cells, typed zeros, denominators, provenance, replay, weights, and both directional
  products are preserved.**
- W05/P04: **fact/replay/provenance construction remains per operation; no silent
  canonical identity/ABI/version change.**
- W03/P01: **existing sealed C11 exact execution and compact Arrow default realization
  retained; no rewrite.**
- W04/P02: **optional authenticated compressed persistent acceleration retained;
  default/retention/eviction unchanged; economical cold construction/memory remains
  unresolved rather than declared complete.**
- P3/P4: **NOT_BUILT / not warranted by this evidence.**
- Qualified guide write-through remains Pyat HQ's duty; this is not a second guide.
MD

---

# Phase-3 preparation: exact W03/W04 function decision and next proof plan

**State:** artifact-only preparation while independent R03 reviews
`409be32f7e4b4b961a360be1c8f44a17b5c62173`. No production code, test, cache
default, guide, source, or authority was changed or executed in this phase. No
timed benchmark or heavy fixture generation was run.

## Function-level decision

| Requirement | Current input -> typed output | Present current function(s) / first consumer | Exact gap found | Preparation disposition |
|---|---|---|---|---|
| **W03/P01** economical exact sealed C11 realization/reconstruction (`ROADMAP:S03.2`, `S-C11`) | `GovernedC11Projection` + `PhysicalSourceIncidence`/`ExactPhysicalCellStream` -> sealed `C11LogicalRelease` (full native tuples, then `_CompactPublicObjects` when pyarrow installed) -> `C11Repository`/`_ReleaseIndex` -> exact I03 facts/replay | `PhysicalSourceIncidence.iter_batches` (`physical_decoder:156`), `project_c11_candidate_from_physical_cells` (`facade:502`), `validate_c11_source_release` (`ingest:743`), `_compact_public_objects` (`execution_view:239`), exact `_EventLane.materialize`/`resolve_object_exact` (`execution_view:77,95`; `repository:107`), `CarrierNeutralResearchExecutor.execute_i03` (`carrier:430`) | **No exact function gap at the current first consumer.** Cold construction is not streaming/lazy: all native events/coords/weights and sorted public/internal tuples are materialized before compact conversion. This is an **unproven economic cold-memory concern**, not a proven defect. | `PRESENT_COMPOSED_NO_BUILD` for exact function; `EVIDENCE_OR_ABI_READY` for controlled cold-construction economy. Do **not** build journal/streaming now. |
| **W04/P02** default regenerable source/release/authority/version-keyed compact Parquet/Zstd acceleration or competent-owner-accepted equivalent (`ROADMAP:S03.2`, `S-C11`) | sealed compact release + source/decoder/projection/release/replay/member-root + current authorities -> in-memory compact Arrow; optional persistent authenticated Parquet/Zstd event-body slot; or full exact `ParquetC11Carrier` release reconstruction; or R4/R5 components | default `_compact_public_objects` in `build_source_backed_c11_repository` (`facade:679-683`); optional `_cache_directory`/`_read_bodies`/`_write_bodies` (`execution_view:160,178,212`); `ParquetC11Carrier.persist/reopen` (`parquet_carrier:249,279`); R4 writer/reader (`r4_compaction:127,256`); R5 codec (`r5_codec:180`) | **No missing codec/carrier function.** The precise gap is **default activation/policy**: with `RAWLSING_C11_ACCELERATOR_DIR` unset, `_cache_directory` returns `None`, so no persistent Parquet/Zstd slot exists even though the in-memory compact Arrow view is built. `ParquetC11Carrier` is a full logical carrier, not the compact hot view; R4/R5 are components, not a complete release cache. | `PRESENT_COMPOSED_NO_BUILD` for exact capability; `OWNER_DECIDE` for default activation or functional-equivalence acceptance. Do **not** silently cancel the selected capability or declare all W03/W04 complete. |

### Exact first conditions

- **W03/P01 first failure:** none found for exact realization/reconstruction at
  the current sourcefree first consumer. The first falsifier is a controlled
  same-sealed-release run at representative scale that exceeds authorized
  memory/disk/time while still requiring the same exact facts/replay. The observed
  code shape alone does not prove that failure.
- **W04/P02 first failure:** unset `RAWLSING_C11_ACCELERATOR_DIR` -> no persistent
  compressed slot (`execution_view:160-175`); also a legacy in-memory
  `PhysicalSourceIncidence` without a decoder digest -> `physical_binding()` returns
  `None` (`facade:667-680`, `execution_view:292`) -> no persistent body slot even
  with a root. These are configuration/transport conditions, not source truth,
  authority, or canonical-identity defects.

## Default-policy alternatives for HQ (no invented owner acceptance)

The user's no-blanket-cache constraint remains binding. The worker does not select
an owner policy. HQ may choose among:

1. **Keep current opt-in form (no production change).** Default in-memory compact
   Arrow remains; persistent Parquet/Zstd is written only when the caller configures
   a private root. This preserves no-blanket-cache and already provides the exact
   optional capability.
2. **Explicit workload/caller opt-in.** Add a bounded per-workload accelerator
   root/policy parameter with private checkout-local storage, size cap, atomic
   manifest, and selective invalidation. Still no process-global default.
3. **Default private root with bounded retention.** This would satisfy a literal
   “default persistent” reading but conflicts with the current no-blanket-cache
   constraint unless HQ/user explicitly authorizes it. Not recommended by this
   worker from present evidence.
4. **Owner-accepted functional equivalence.** Accept the current default in-memory
   compact realization plus the optional authenticated persistent cache as the
   competent-owner equivalent. This requires the competent owner's decision, not
   this return.

All four leave exact source/authority/ref/replay and per-operation native fact
semantics unchanged. None justifies a new persistent canonical carrier.

## Smallest controlled same-sealed-release comparison

This is a **plan only**. It must not run while the R03 reviewer has the exclusive
timed runner; HQ schedules it after R03 timing returns.

### Fixed inputs

Use existing constructors/fixtures only: one `GovernedC11Projection` and one
sealed release per scale, reused by every variant. Start with the existing small
route-B/source-backed fixture and phase-1 `N=200`, then `N=1000`; run `N=3000` only
if the smaller pair leaves a real decision. Do not use original35 or new
architecture.

### Variants (read-only/benchmark only)

- **V0 full native:** call `build_validated_source_backed_c11_release_from_stream`
  (or the existing `build_validated_c11_release`) directly, keep full
  `C11LogicalRelease`, build `C11Repository` + `_ReleaseIndex` + first consumer.
- **V1 current compact:** `build_source_backed_c11_repository` (default
  `_compact_public_objects`), same repository/index/executor.
- **V2 current persistent compact cache:** V1 with a private cache root; cold,
  warm, delete, corrupt, stale, revoked; existing cache tests reused.
- **V3 full exact carrier reconstruction:** `ParquetC11Carrier.persist` on V0,
  `reopen`, `C11Repository`, `_ReleaseIndex`, first consumer.
- **V4 R4/R5 component evidence:** R4 writer/reader exact event reconstruction and
  R5 typed-value roundtrip; component-only, not a full release path.

Every variant uses the same sealed release/workload and the same query/predicate
oracles. No A/B/C architecture comparison.

### Phase isolation and metrics

Separate phases, measured from separate cold processes where RSS is compared:

1. source/fixture construction (`C_source_fixture`) — once, excluded from variant
   comparison;
2. decoder/physical incidence (`C_source`);
3. candidate construction (`C_projection`);
4. complete I02 validation (`C_validate`);
5. compact conversion (`C_cache_build`/`C_compact`);
6. repository/index build (`C_repository`/`C_index`);
7. query execution (`C_query`);
8. native fact/replay/provenance construction (`C_fact`/`C_provenance`).

Record wall, CPU, peak RSS in Darwin bytes, cold/warm, index builds, object/event/
selector counts, event-body JSON bytes, Parquet/Zstd bytes and temp bytes, cache
HIT/DELETE/CORRUPT/STALE/REVOKED counters, and exact fact/ref/replay/provenance
equality. Do not compare a compact run and a native run with different fixture
construction or process setup; phase-1 “compact vs native memory” was explicitly
not a controlled memory proof.

### Cases

Reuse phase-1/2 oracles and existing fixtures for: 2/3/4-target AND joints;
common/routed/asymmetric risk; forward/reverse conditionals; XOR/minority;
observed zero/zero support/valid empty; MISSING/DK/REFUSAL/IAP/NOT_ASKED; unsupported
topology; `NOT_ADMINISTERED` contract limitation; different releases/universes/
authority/weights; cache HIT/DELETE/CORRUPT/STALE/REVOKED; and the actual first
reader `CarrierNeutralResearchExecutor.execute_i03` plus issued Batch/I05/P41
equivalence where affected.

### Acceptance / stop rules

- Any changed fact/cell/denominator/typed negative/provenance/replay vs V0 is RED.
- Cache absence or rebuild may change only cost, never meaning/reachability.
- W03/P01: if controlled cold RSS/time is within accepted bounds, no build; record
  `NO_UNCOVERED_FUNCTION`. Only a demonstrated cold-construction failure justifies a
  bounded streaming/lazy candidate/replay adapter.
- W04/P02: if the current optional persistent cache plus default in-memory compact is
  accepted as functionally equivalent, no build; if default activation is required,
  implement the smallest explicit opt-in/config policy, not a new engine.
- No declaration of complete W03/W04 from a tiny cache-hit fixture or a favorable
  scale alone.

## Minimal allowlist for the next proof

- **Benchmark/test only:** a bounded script under this C4 return/tools using the
  existing V0–V4 constructors and existing first consumer; no production edits.
- **If W03/P01 cold failure is proved:** smallest read-only comparison/adaptation
  candidates are `pre553_c11_ingest.py` and `pre553_c11_repository.py` (streaming
  candidate/replay or lazy exact view). No historical journal resurrection.
- **If W04/P02 default activation is selected:** smallest candidates are
  `pre553_source_backed_c11_facade.py` and `_pre553_c11_execution_view.py`
  (explicit policy/root/config), not `pre553_parquet_carrier.py` or R4/R5 rewrites.
- **Do not touch without measured deficit:** `pre553_parquet_carrier.py`,
  `pre553_r4_compaction.py`, `pre553_r5_codec.py`, compact selector ABI v1,
  authority/source/permission semantics, or canonical identities.
- **No resurrection:** historical `pre553_r5_compact_carrier.py` /
  `pre553_r5_c11.py` are absent at this branch and are not a build ticket; the
  current compact Arrow view, `ParquetC11Carrier`, R4 and R5 are the present
  successors/components.

## PROGRAMMA_DELTA addendum

- `ROADMAP:S03.2`, W03/P01: **exact function present/composed; controlled cold
  construction economy unproven; no mandatory streaming/journal rewrite.**
- `ROADMAP:S03.2`, W04/P02: **exact compact/carrier/codec capability present;
  default persistent activation is a policy/owner decision, not a missing engine.**
- `S-C11`: **source/authority/ref/replay types unchanged; cache presence never grants
  authority; no blanket default.**
- `ROADMAP:S03.3`, W05/P03/P04: **phase-2 grouped implementation and per-operation
  fact/replay cuts retained unchanged.**
- No guide write-through, protected merge, native/original35/science/Sorok claim, or
  production change is made by this preparation.

## Prepared driver and directly executable commands

The prepared driver is `tools/bench_compact_current.py`. It is a same-source
current physical-function comparison, not a new architecture bakeoff:

- V0 full validated native release/repository/actual I03.
- V1 existing default compact Arrow facade.
- V2-cold/V2-warm same compact facade with an explicitly workload-owned private
  existing Parquet/Zstd cache under the requested output directory.

Each variant is a separate fresh subprocess. The coordinator compares full native
`fact.as_dict()` material per operation against V0, requires equal source/projection/
release identity, and requires V2 cold miss/write + warm HIT. N=200 and N=1,000 are
separately invocable. Timings were run for N=200/N=1,000 after R03 released the timed runner; N=3 smoke is not a benchmark.

Commands for HQ after the R03 timed-runner release:

```sh
RUNNER=/tmp/rawlsing-oct28-p1r1/venv/bin/python
TMPDIR="$PWD/.local-logs/pyat-l03-c4/tmp" \
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
"$RUNNER" WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py \
  --mode compare --n 200 --outdir .local-logs/pyat-l03-c4/compact_compare/n200

TMPDIR="$PWD/.local-logs/pyat-l03-c4/tmp" \
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
"$RUNNER" WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py \
  --mode compare --n 1000 --outdir .local-logs/pyat-l03-c4/compact_compare/n1000
```

The driver reports phase wall/CPU, whole-process Darwin `ru_maxrss` bytes with an
explicit non-attribution note, source/cache bytes, selector/index/fact/replay build
counts, and per-operation exact facts. Delete/corrupt/stale/revoke are existing-test
coverage and remain NOT_RUN here.

Compact grouped commands on the same prepared fixture/release:

```sh
"$RUNNER" WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py \
  --mode grouped --n 200 --rounds 3 --outdir .local-logs/pyat-l03-c4/grouped_compact/n200
"$RUNNER" WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py \
  --mode grouped --n 1000 --rounds 3 --outdir .local-logs/pyat-l03-c4/grouped_compact/n1000
```

### Driver evidence status

- Syntax: `python -m py_compile` **PASS**.
- Tiny functional smoke: N=3 `--smoke` **PASS** with full fact equality for V1,
  V2-cold, V2-warm against V0, equal source/projection/release identity, V2 cold
  miss/write, and V2 warm HIT. Smoke is explicitly not a benchmark.
- N=200/N=1,000 compact comparison: **MEASURED**; V0/V1/V2 exact full-fact parity, V2 cold miss/write and warm HIT.
- Compact grouped N=200/N=1,000: **MEASURED**; exact cold/warm/single/incompatible/capacity parity, independent oracle PASS.
- W03/W04 economic conclusion: **MEASURED_SCOPED**; sourcefree fixture only, no all35 production equivalence.
- W04 default policy: **OWNER_DECIDE**, alternatives in the Phase-3 section above; no blanket default added.


## Measured compact comparison and compact grouped result

The prepared driver ran successfully at N=200 and N=1,000. All V0/V1/V2 variants
used the same sealed source/projection/release; full fact, cell, denominator/risk
refs, provenance, and replay material matched exactly. V2 used a non-empty decoder
binding and passed cold miss/write and warm HIT checks.

Compact comparison (fresh process per variant; whole-process Darwin peak RSS):

| N | V0 native | V1 compact | V2 cold | V2 warm | V2 cache bytes | peak RSS V0/V1/V2-warm |
|---:|---:|---:|---:|---:|---:|---:|
| 200 | 6.18 s | 6.56 s | 5.40 s | 4.34 s | 318,780 | 63.2 / 135.0 / 109.5 MB |
| 1000 | 21.29 s | 21.76 s | 21.55 s | 21.03 s | 1,716,950 | 153.8 / 263.4 / 265.7 MB |

The warm cache removes most compact-conversion time (1.97→0.33 s at N=200;
2.27→0.74 s at N=1000), but total wall remains dominated by I02 validation, query,
and per-operation fact/replay. Compact RSS is higher than native at both sizes. This
is a sourcefree synthetic fixture result, not all35 production equivalence.

Compact grouped measurement on the same compact release (actual first consumer,
not native tuple):

| N | cold no-scope / grouped | warm no-scope / grouped median | speedup | single-op Δ | incompatible-first Δ | oracle |
|---:|---:|---:|---:|---:|---:|---|
| 200 | 1.576 / 1.284 s | 1.422 / 0.593 s | 2.40× | +47.9% | −3.6% | PASS |
| 1000 | 6.774 / 6.228 s | 6.724 / 2.656 s | 2.53× | +9.0% | +25.4% | PASS |

Counters confirm actual work reduction at N=1,000: routing/predicate/target calls
22,001/13,428/10,294 → 2/2/2, weight 10,294 → 1,715; the two residual calls are the
unsupported negative fallback. Capacity fallback with `max_groups=1` was exact but
slower (+46.8% N=200, +60.8% N=1,000), so fallback economy is unproven. R03's 82–92
P41 fallbacks remain a nonblocking limit; no capacity repair was made.

**Disposition:** W03/P01 exact current composition is demonstrated with no exact
function gap; cold-construction economy remains fixture-limited and not a production
claim. W04/P02 exact compact/cache/carrier functions are demonstrated at sourcefree
scope; default activation remains explicit-policy/owner decision, not blanket cache.
No extra index/carrier/truth engine was added.

## Capacity-miss guard delta (new implementation/test)

**Implementation/test SHA:** `9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3` (based on
the earlier measured compact/grouped work; R03 acceptance `e2f6c164...` remains
limited to `409be32f7e4b4b961a360be1c8f44a17b5c62173`).

The only change is an early capacity guard in `I03GroupedExecutionScope.evaluate`:
on a cache MISS, if the group cap is already reached or cached denominator members
already reach the member cap, return the existing unshared fallback before building
the duplicate core. HITs occur before the guard and remain usable. Unknown prospective
member size still uses the existing post-build fallback. No eviction/LRU/new estimate,
capacity default, index/carrier, cache policy, or broader optimization was added.

N=200 paired capacity-full result (3 interleaved rounds): before early guard
0.3383 s, after 0.2001 s, no-scope 0.1989 s; all exact facts/refs/replay equal. Before
core attempts/builds/early fallbacks = 2/1/0; after = 1/1/1; full-capacity HIT
reused. Focused grouping suite 15 passed. The new code is not covered by the
original R03 acceptance and is not a whole-L03 completion.
