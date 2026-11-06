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
