# PROGRAMMA PYAT L03 / C4 — Phase-1 measured checkpoint

**Status:** PHASE-1 COMPLETE / AUTHOR CHECKPOINT ONLY / PRODUCTION NOT CHANGED.
**Branch:** `perf/programma-pyat-w05-p03-f1f4-grouped-economy-20261105-r1`
**Base:** `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`
**Checkpoint SHA:** `da7be66893217175f9301717c7f1693e6ca89ed8`
**Model provider observed at invocation:** `opencode-go/deepseek-v4.1-flash`.
**Authority:** sourcefree engineering measurement only. No original35, native
source/science, actor/V3, human, Sorok, protected CAS, or merge authority. No
`rawlsing_next` production file was modified.

## What was actually measured

The actual first consumer `CarrierNeutralResearchExecutor.execute_i03`
(`rawlsing_next/pre553_carrier_execution.py:427`) was run on existing synthetic
C11 constructors and fixtures, with the actual sealed release index, attested
index reuse, exact I03 facts, exact replay refs, compact Parquet/Zstd lane, Route-B
composer, issued Batch/I05 path, and the existing sourcefree P41 test.

- **65 focused tests passed** across six commands: 32 empirical-query, 4
  carrier-execution, 8 compact-view, 14 hostile-frontier, 6 issued-workload
  custody, and 1 same-source P41 end-to-end (67.32 s). All exits 0.
- **52 baseline exact facts** (13 operations × N=200/1,000/3,000 native plus the
  N=1,000 compact view) passed the independent synthetic oracle with exact
  states, raw/weighted numerators/denominators, full cells, risk/denominator
  member identities, and fact/replay refs.
- **44 same-fact relations passed**: sibling-query identity (same numbers,
  distinct facts/replay), raw vs governed-weighted sharing only the denominator,
  target siblings sharing risk/predicate but not cells, exact 1/2/3/4-target
  domains, forward/reverse conditional separation, XOR/no-lower-order-signal
  retention, minority retention, and incompatible-risk-set separation.
- **14 frontier fixtures** reproduced their declared oracles exactly, including
  XOR zero-unary, Simpson reversal, routing asymmetry, raw/weighted divergence,
  observed zero vs zero support, MISSING/DK/REFUSAL/IAP/NOT_ASKED, source-indexed
  disagreement, noncomparable multi-universe, ordered/ranked/repeated topology,
  and the 4-way bounded joint.
- **Replay/authority negatives**: identical replay refs; replay mismatch refusal;
  cached-index fault repair with identical fact; authority DENY refusal; missing
  release binding/typed refusal; missing weight typed refusal; release/universe
  index separation; risk-set result separation.
- **Accelerator behaviors**: HIT/DELETE/CORRUPT/STALE/REVOKED all exact-material
  equal; stale/revoked paths never reused as authority. No default/retention
  change was made.

## Exact baseline cost highlights

Single runner, sequential, sourcefree synthetic; clean timings are without
instrumentation. `ru_maxrss` is Darwin bytes and a process high-water mark.

| N | fixtures events | index build first op | warm `all_K_raw` median (4 passes) | peak RSS native |
|---:|---:|---:|---:|---:|
| 200 | 1,600 | 0.0765 s | 0.0983 s (single-pass sibling; first op 0.1722 s incl. index) | 78.4 MB |
| 1,000 | 8,000 | 0.3814 s | 0.4548 s | 287.7 MB |
| 3,000 | 24,000 | 1.3441 s | 1.2513 s | 1,322.9 MB |

Warm repeats at N=3,000: `all_XY_raw` 2.2436 s, `all_XYZ_raw` 3.2246 s,
`all_ABCK_raw` 4.4740 s, `cond_X1_target_Y` 1.4708 s, `cond_Y1_target_X`
1.4385 s, `xor_condition_target_Z` 2.6372 s, `minority_branch_target_K`
0.7761 s, `risk_S_target_K` 0.9843 s. First-operation cold-index cost at N=3,000
was 2.5766 s for `all_K_raw`; index rebuilds after that were zero.

Attribution at N=3,000: the measured risk/routing + predicate + target/weight
share of a warm operation was 0.615–0.648 for compatible one-target branch
operations, 0.686–0.720 for 2/3/4-target branch operations, 0.778 for the XOR
condition, and 0.618 for the incompatible risk set. Fact/replay/provenance
construction was 0.168–0.264. These are component shares, **not achieved
speedups**.

Compact N=1,000 context: one event-body slot was **704,824 bytes** against
**14,856,000 bytes** of uncompressed event-body JSON; cold compact build
4.2353 s, warm cross-process build 0.8205 s with a hit and no write. This is the
existing scoped compact physical view, not query grouping.

Route-B compact fixture: cold 0.4794 s, warm hit 0.0771 s, delete 0.0838 s,
corrupt 0.0701 s, stale new slot 0.0754 s, original slot after stale 0.0766 s;
all exact material equal; 17,963 bytes per slot, 35,926 bytes with the stale
second slot.

## Bounded measured recommendation

The smallest warranted W05/P03 delta is a **P2 execution-local grouped
AND-risk/target kernel** inside the existing I03 evaluator, keyed only on exact
compatible `(release, universe, risk set/type, measure, predicate, target
plan/domain)` material. It would reuse the existing routing/risk, predicate,
weight, and target semantics, memoize their respondent-level results for the
compatible group, and still build a separate exact `EmpiricalFact`, provenance,
and replay for every operation. It must preserve typed states, zeros, minority
branches, weights, authority, and no-cross-scope sharing.

Do **not** build a new bitmap/posting index (P3) or a new persistent body engine
(P4) from this evidence. P3 is NOT_IMPLEMENTED/NOT_RUN and has no measured
benefit. P4's compact regenerable Parquet/Zstd lane already exists in scoped,
env-gated form; default/retention/eviction is a W04/P02 owner decision, not part
of this change.

The production diff for P2 is **NOT YET AUTHORIZED**. HQ must select the minimal
kernel and grant the bounded production diff; independent R03 is requested after
the frozen implementation, not for this baseline.

## Limits stated honestly

- Sourcefree synthetic only. No original35 source metadata, permission, native
  science, human, actor, or Sorok claim.
- N=3,000 is a bounded probe, not a scalability or cost estimate for all35.
- Cold-start includes synthetic fixture construction (89.85 s of the 130.79 s
  N=3,000 clean parent wall); it is not a production cold-start claim.
- Attribution is instrumented and nested; negative instrumentation/run-noise
  deltas occurred, so component proportions rather than absolute instrumented
  seconds are used. Clean repeat timings are separate and in
  `results/repeat_summary.json`.
- `NOT_ADMINISTERED` is not a C11/I03 response/routing state; the nearest actual
  evidence is a binding-level `FIXTURE_TARGET_NOT_ADMINISTERED` refusal and the
  separate universal-grammar vocabulary. No I03 fact was invented for it.
- P2/P3/P4 are NOT_IMPLEMENTED/NOT_RUN where stated; this is not complete C4, not
  a no-extra-code equivalence claim, and not a tiny-fixture equivalence claim.

## Nested PROGRAMMA delta

Tied to `ROADMAP:S03.3`, `S-I03`, W05/P03/P04 and `ROADMAP:S04.1–S04.4`: the
current successor has exact attested index reuse and the compact physical lane;
the measured remaining W05/P03 gap is compatible cross-operation respondent/
risk/predicate/target/weight recomputation. Fact/replay construction remains per
operation. No scientific contract change is proposed. The qualified guide
write-through remains HQ's duty; this return is not a second guide.

## Read next

1. `01_BASELINE_CURRENT_CODE_ABI.md` — callgraph, ABI, index/cache, commands.
2. `02_EXACT_COST_AND_MEMORY_RESULTS.jsonl` — process/op/cache/repeat/test costs.
3. `03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl` — exact facts and parity.
4. `04_REPLAY_AND_AUTHORITY_INVALIDATION.md` — replay/authority/cache negatives.
5. `05_OPTION_MATRIX_AND_MINIMAL_DELTA.md` — five-test disposition and choice.
6. `06_INDEPENDENT_REVIEW_REQUEST.md` — independent review scope/questions.
