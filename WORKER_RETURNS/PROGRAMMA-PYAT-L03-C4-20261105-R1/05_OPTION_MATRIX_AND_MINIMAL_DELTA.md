# 05 — Five-test work selection, option matrix, and minimal measured delta

**Status:** Phase-1 measured recommendation only. No production implementation is
included or authorized by this return. P2/P3/P4 candidate implementations are
marked **NOT_IMPLEMENTED / NOT_RUN** where applicable. This is not a complete C4
claim, not a no-extra-code equivalence claim, and not native/original35 science.

## Five-test historical-function disposition

The selected current destination is W05/P03 exact cross-operation sharing
(`ROADMAP:S03.3`, `S-I03`), with W03/P01 sealed C11 realization and W04/P02 compact
regenerable acceleration as adjacent selected capabilities.

| Law field | Phase-1 answer |
|---|---|
| `HISTORY` | October W05/P03 grouped-economy capability; current code successor is the PR684 attested release-index cache plus PR686 compact body lane, not a historical file restoration. Historic actual caller for this measurement is the current `CarrierNeutralResearchExecutor.execute_i03`, not an old V550/V550J body. |
| `CURRENT_REQUIREMENT` | `ROADMAP:S03.3` / `S-I03`: compatible exact cross-operation sharing at the actual first consumer; W05/P03. W03/P01 and W04/P02 remain selected but are not the primary measured gap here. |
| `CURRENT_SUCCESSOR` | Index reuse and attestation are **present** (`_release_index_for`, `_build_release_index` only on miss). Compact Parquet/Zstd event-body view is **present** (`_compact_public_objects`, `_read_bodies`, `_write_bodies`). Per-operation respondent risk/predicate/target/weight recomputation is **not** shared across compatible operations. Derived-branch membership compilation is only execution-local per predicate. Disposition: **PARTIALLY_MISSING**. |
| `FIRST_CONSUMER` | Exact actual reader: `CarrierNeutralResearchExecutor.execute_i03` (`pre553_carrier_execution:427`), called by Route-B production (`pre553_route_b_production:582`), with the issued Batch path and sourcefree P41 test as downstream context. The first consumer demands one exact `EmpiricalFact` + replay per operation, not a merged scientific result. |
| `AUTHORITY` | Sourcefree engineering only. C11 release is sealed and exact; I03 authority is checked per operation; no new source/actor/science/weight/routing grant. Original35, native source release, and P41 native science remain separately held. |
| `COMPARE_AND_COST` | See option matrix below. Current cache/index baseline is measured. Reuse/adapt of the existing evaluator is sufficient for the recommendation; new bitmap index and new persistent body engine are not justified by this baseline. |
| `DISPOSITION` | `TRUE_CURRENT_GAP` for compatible cross-operation sharing at W05/P03; recommendation `REUSE_ADAPT`, not `BUILD_NEW` engine. |
| `NEXT_WORK` | `REUSE_ADAPT` a minimal grouped kernel on the existing cached release index after HQ grants the exact production diff. Do not build a second semantic engine, persistent canonical copy, or new scheduler. |
| `FALSIFIER` | A bounded P2 implementation that preserves all exact facts/replay while reducing measured compatible-workload cost and does not regress single-operation, incompatible-risk, release/universe, authority, weight, typed-state, zero, or replay checks. If P2 cannot produce a material reduction on the actual admitted mix, the recommendation reverses to `NO_ACTION`/defer. |

## Measured baseline used for the decision

All timings are single-runner, sequential, sourcefree synthetic. Clean timings are
without instrumentation. Warm repeats are passes 1–3 on one repository after the
cold-index pass. Four-pass warm ranges are in `results/repeat_summary.json` and
`02_EXACT_COST_AND_MEMORY_RESULTS.jsonl`.

### Release-index reuse is real

| N | index build on first op | warm index lookup (`_release_index_for`) | warm resolve incl. universe scan | index builds after first |
|---:|---:|---:|---:|---:|
| 200 | 0.0765 s | 0.000021 s | 0.00066 s | 0 |
| 1,000 | 0.3814 s | 0.000026 s | 0.00356 s | 0 |
| 3,000 | 1.3441 s | 0.000026 s | 0.00911 s | 0 |

The cache is therefore not the residual gap for repeated operations. The residual
gap is per-operation respondent computation and per-operation fact construction.

### Warm operation cost and attribution at N=3,000

Selected warm medians (four-pass repeat measurement):

| operation | warm wall median | cold-index first pass |
|---|---:|---:|
| `all_K_raw` (1 target, branch) | 1.2513 s | 2.5766 s |
| `all_K_weighted` (same target/risk/predicate) | 1.5623 s | 1.6260 s |
| `all_K_raw_sibling` (same semantics, different query identity) | 1.2939 s | 1.3109 s |
| `all_XY_raw` (2 targets) | 2.2436 s | 2.3959 s |
| `all_XYZ_raw` (3 targets) | 3.2246 s | 3.4689 s |
| `all_ABCK_raw` (4 targets) | 4.4740 s | 4.0435 s |
| `cond_X1_target_Y` | 1.4708 s | 1.3055 s |
| `cond_Y1_target_X` | 1.4385 s | 1.2848 s |
| `xor_condition_target_Z` | 2.6372 s | 2.2818 s |
| `minority_branch_target_K` | 0.7761 s | 0.6986 s |
| `risk_S_target_K` | 0.9843 s | 0.9039 s |

Attribution on the same mix (instrumented; proportions are the defensible result):

| operation class | risk/routing + predicate + target/weight share of warm op | fact/replay/provenance construction share |
|---|---:|---:|
| compatible 1-target branch operations | 0.615–0.648 | 0.243–0.264 |
| 2/3/4-target branch operations | 0.686–0.720 | 0.200–0.224 |
| forward/reverse conditional | 0.695–0.717 | 0.197–0.227 |
| XOR condition | 0.778 | 0.168 |
| minority branch | 0.715 | 0.195 |
| incompatible risk set | 0.618 | 0.181 |

At N=1,000 the corresponding shareable range was 0.529–0.785 and the
fact-construction share 0.162–0.370; the 2-target instrumentation run had a
large positive wrapper overhead and is not used as an absolute timing. The clean
repeat data is the comparable timing source.

The repeated components are exactly the ones that a grouped kernel can key by an
exact compatible group: release, universe, risk set and risk-set type, measure,
predicate identity, and target plan/domain. The fact/replay/provenance
construction must remain per operation because it is the native `EmpiricalFact`
publication unit; it cannot be replaced by a grouped aggregate.

### Compact physical view at N=1,000 (context, not a controlled A/B)

- one Parquet/Zstd event-body slot: **704,824 bytes**;
- uncompressed event-body JSON: **14,856,000 bytes**;
- cold compact build: **4.2353 s**;
- warm cross-process compact build: **0.8205 s**;
- native event-body view peak RSS: **287.7 MB**; compact run peak RSS: **352.0–383.8 MB**
  (separate processes, includes pyarrow and compact construction; not a memory
  claim in favor of compactness).

The compact view removes native event-body reconstruction work and is an accepted
scoped physical capability, but it does not remove the per-operation
risk/predicate/target iteration. It is not a substitute for W05/P03 sharing.

## Option matrix

| Option | What it would do | Exactness / authority | Measured evidence | Risk / delta | Disposition |
|---|---|---|---|---|---|
| **P0/P1 current** | Attested release-index reuse + per-operation evaluator/compact view | Exact existing I03; no new authority | 0 index rebuilds after first op; warm op cost and 61–78% shareable components measured | Already present; no new production change | **BASELINE / KEEP** |
| **P2 minimal grouped AND-risk/target kernel** | Execution-local memo keyed by exact compatible group; compute respondent routing/risk, condition, target configuration, and weight once for compatible operations; still build one exact fact/replay/provenance per operation | Reuses existing exact predicate/risk/authority evaluator; no new semantic truth or canonical copy; no cross-release/risk/universe/authority/weight sharing | Measured shareable components 0.615–0.778 of warm op for the compatible classes; fact construction 0.168–0.264 remains per operation | Smallest coherent W05/P03 delta; requires exact parity and single-op non-regression tests; not implemented in Phase 1 | **RECOMMEND AFTER HQ DIFF GRANT** |
| **P3 per-question bitmap/dictionary posting index** | Add per-target posting structures to accelerate routing/target scans | Could be exact, but adds a second physical access path and memory/retention surface | **NOT_IMPLEMENTED / NOT_RUN**; no measured benefit | Larger delta; rebuild/retention and authority-attestation burden; would not remove fact/replay construction and may not beat grouped recompute | **DEFER / NO BUILD NOW** |
| **P4 new persistent Parquet/Zstd body engine** | Add or default a new persistent accelerated body store | Existing compact lane already regenerable and exact; new engine risks a second canonical copy | Existing accelerator measured for cold/warm/delete/corrupt/stale/revoked; `NOT_RUN` for a new engine | No evidence a new engine is needed; default/retention/eviction belongs to W04/P02 owner decision | **NO BUILD / NO DEFAULT CHANGE** |
| **Reuse/adapt/compose existing owners** | Compose accepted C11, I03, compact view, Batch | Exact and already reviewed scoped code | All 65 focused tests passed; 52 baseline facts and 44 same-fact relations exact | No new semantic engine | **PREFERRED FRAME FOR P2** |
| **Repair only** | Fix index/cache defect | Existing attestation already repairs corruption and same-identity faults | Fault repair returned the same fact; cache delete/corrupt/stale rebuilt | No evidence of a remaining cache correctness defect | **NO_ACTION** |
| **New semantic engine / new scheduler / canonical copy** | Separate grouped truth engine | Collides with current I03 ownership and `05_HISTORICAL…` law | None | High; prohibited at this checkpoint | **REJECT / NO_ACTION** |

## Minimal recommended delta for the next authorized phase

The smallest warranted W05/P03 delta is a **P2 execution-local grouped AND-risk/target
kernel inside the existing I03 evaluation path**:

1. Key only on exact compatible material: `(release_ref, universe_ref,
   risk_set_ref, risk_set_type, measure_kind, condition predicate ref, exact
   target plan/topology/domain refs)`.
2. Reuse the existing `_ReleaseIndex`, `_routing_fact_for`, `_eval_predicate`,
   `_weight_for`, and `_target_configuration` semantics; do not add new scientific
   interpretation, weights, routing, or denominator rules.
3. Memoize respondent-level routing/risk membership, condition truth, target
   configuration, and governed weight only for the lifetime of the compatible
   group/execution; do not persist or canonicalize the memo.
4. Still construct the separate exact `EmpiricalFact`, provenance, and replay for
   every operation, including weighted/raw siblings and every target arity.
5. Refuse sharing across incompatible risk sets, releases, universes, authorities,
   weights, or target domains; keep the existing typed states for
   empty/zero/minority/unsupported/refusal cases.
6. Require the bounded P2 implementation to demonstrate exact parity against the
   existing frontier fixtures and the scaled mix, and to show no single-operation
   regression, before independent R03 review.

Do **not** implement P3/P4 in the next diff from this evidence alone. P3 has no
measured benefit and P4 already exists in scoped, env-gated form; enabling default
retention/eviction is a W04/P02 owner decision, not a W05/P03 implementation
shortcut.

## PROGRAMMA_DELTA (ordinary return; not a guide write-through)

Compact observation to attach to the existing IDs after HQ review:

- `ROADMAP:S03.3`, `S-I03`, W05/P03: **baseline measured; current successor has
  attested release-index reuse and compact body lane; residual gap is compatible
  cross-operation respondent/risk/predicate/target/weight recomputation.**
- `ROADMAP:S04.1–S04.4`: **no scientific contract change; all baseline facts and
  frontier oracles are exact; grouped value must still be published as separate
  native facts and replay.**
- W05/P04 (`_make_execution_replay_ref` / `_build_fact` profiling): **fact/replay/
  provenance construction is 0.168–0.264 of warm op at N=3,000 and 0.162–0.370 at
  N=1,000 in the instrumented runs; it must remain per operation.**
- `S-C11`: **compact accelerator HIT/DELETE/CORRUPT/STALE/REVOKED behaviors passed
  exact material parity; no default/retention change proposed.**
- `S-I03`: **actual first consumer is `CarrierNeutralResearchExecutor.execute_i03`;
  issued Batch/I05 and sourcefree P41 test passed; original35/native science
  remains held.**
- Recommended next work: `REUSE_ADAPT` minimal P2 grouped kernel after an HQ-granted
  production diff; `P3` defer/NOT_RUN; `P4` no new build/no default change.
- Qualification/guide write-through remains Pyat HQ's duty; this file is not a
  second guide and does not alter protected statuses.
