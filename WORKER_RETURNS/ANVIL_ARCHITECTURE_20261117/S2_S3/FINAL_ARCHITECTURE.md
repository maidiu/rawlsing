# FINAL INTEGRATED ARCHITECTURE — conditional candidate

**Status:** `FINAL_CANDIDATE_FROZEN_PENDING_DISTINCT_C`.
**Grade:** `CONDITIONAL_DIRECTION`; author proposal, not acceptance.
**Base frame:** `S1/FRAME.json`,
`7e7bfb9638f23894fd244a703e8a6b88d361f90fafa5b2b10ac78c1f24229913`,
commit `5a619ff9fa79be9183eb4d4378d42f040ef2bd9b` (immutable).
**Frame v2 addendum:** `S1/FRAME_V2_ADDENDUM.json`,
sha256 `aa170d8954a3fc0be99318f4d28399b6f3cb004603ef24d317bb3f475c3ea7ff`.
**Decision:** `S2_S3/FINAL_DECISION.json`; local guard
`PASS_LOCAL_INTEGRATED_DECISION_PENDING_C` (16/16, 118/118). The guard is
structural only; it is not independent C or H1.
**Both specialist returns consumed:** construction `f8c9802…` and query
`a5ea7fd…`, with HQ receiving records. Their exact pins and disagreement are in
`S2_S3/SPECIALIST_ADJUDICATION.md`.

## 1. Selected conditional design

**Prepared-session-first, with conditional construction/recovery repair; durable
locator index held behind measurement.**

### Leg Q — selected first query step

One exact `PreparedSavedC11Admission.open` and one `prepared_i03` context per
exact release/universe/workload. Forward-wire the existing `PreparedI03Session`
into the actual first consumer and into saved Batch units so each unit uses the
same prepared session instead of opening a fresh `DirectEstateI03Session`.
Keep `check_current` before and after every operation and keep per-operation
fact/replay exact.

This removes repeated `S` (index build) within one process, adds no retained
artifact, and creates no new evaluator, authority or format. It is neutral at
N=1 and does not help a one-operation fresh process; that is stated, not hidden.

### Leg C — conditional construction/recovery repair

- Merge the duplicate 3-family Q2 spool and the 13-family bridge journal into
  one bounded private journal.
- Attempt one source-derived Q2 I02 certificate as the sole I02 proof **only if**
  the full physical body/lane/selector proof against Q2 survives for every
  family. If any family or selector cannot be compared without a second
  representation, keep the second certificate exactly as today.
- Replace the current target-mkdir-before-manifest window with a private stage
  and a proven no-clobber claim/lease; publish a completed manifest last; type
  orphans; GC only proven-dead scratch. Do **not** assume a portable atomic
  rename is no-clobber; where rename may replace, use a claim/lease or
  `ORPHAN_REQUIRES_OPERATOR`.
- Keep manifest/member fsync and the existing member-hash proofs.

### Leg D — durable index: not selected now

A durable exact locator index is the only route that removes `S` from a
one-operation fresh open. It is **held**, not adopted, because:

- the cited SQLite session index is 1.30 GB, about 4.19× the 310.16 MB estate;
- the invalidation/rebuild burden under source/currentness/revocation and
  multi-wave use is unproven;
- the actual `S` share relative to `Q` and `O` is unmeasured.

If measurement shows `S` is material and a compact exact encoding can earn its
retained cost, qualify it under the v2 binding/invalidation contract. Otherwise
keep prepared-session + fresh rebuild.

## 2. Architecture path

```
SAV/DTA snapshot
  │ one Q2 decode/projection; native question/option/form/routing/missing,
  │ respondent/occurrence, weights/design, authority/current
  ▼
typed 13-family stream
  │ one bounded private journal; conditional one Q2 I02; full physical proof
  ▼
canonical C11 estate (unchanged body format)
  │ 13 Parquet/Zstd families: body_json once + typed projections + event locator
  │ manifest: source/release/replay/universe/I02 roots, counts, member hashes
  ▼
cold admission H (manifest/I02/member/current)
  │ one prepared session S per exact release/universe/workload
  ▼
existing native I03/I05/F1–F4 evaluators Q
  │ exact fact/replay/risk/denominator/negative
  ▼
exact evidence output O (content-addressed set refs only under identical identity)
  │
  ├── FF01 descriptive ── independent FF02 structural owner
  ├── N9 world / N10E / N10W possibility
  ├── SEAM Other → encounter → access → learned activity / world history
  └── separately governed SOROK actor (consent/access; no source→actor promotion)
```

No edge permits survey observation to become actor private knowledge, opinion
to become institutional power, fictional action to mutate observed C11, a
stratum to become individual identity, or pairwise marginals to substitute for a
true same-person k≥3 joint.

## 3. Why this over the strongest rivals

| Rival | Disposition | Reason |
|---|---|---|
| One-shot admission per operation / per Batch unit | ruled out | pays `S` per operation; actual `execute_saved_batch` opens a fresh session per unit |
| Durable locator index now | held | 1.30 GB retained, 4.19× estate; invalidation/rebuild and `S` share unmeasured; must earn its place |
| One-certificate/one-journal unconditionally | conditional | duplicate certification may carry independent proof value; full Q2 physical proof is the gate, second certificate is the fallback |
| Primary SQLite/DuckDB/Postgres body store | ruled out | new primary authority/ABI and duplicate body; no evidence it fixes the bottleneck |
| W03 full object graph | ruled out | historical >6 GiB peak; whole-graph reconstruction; negative history |
| JSONL/wide-table primary | ruled out | loses typed pruning and family semantics; parse/output amplification |
| Typed/columnar pushdown | held | only if `Q` measured dominant; must feed existing evaluator with exact candidate streams, not a second evaluator |
| Precompute/cache facts | ruled out | open query space, revocation/staleness, 3–5 GB/100 facts; exact set-ref sharing only |

The choice is not a majority vote: it follows the measured/cited cost layers and
the exact proof obligations.

## 4. Proof, nonloss, invalidation and recovery contract

**H (cold admission):** every fresh admission verifies manifest SHA, independent
I02 roots, release/replay/universe, member hashes, family censuses and current
authority. A producer-returned digest is never authority.

**S (prepared session):** one exact release/universe/workload; one index build;
no per-unit rebuild. Sourcefree vs native is a source/authority label; the
native evaluator does execute on sourcefree fixtures, but that is not native
source proof.

**Q/O (per operation):** exact native facts, risk/denominator member refs,
provenance, authorities, replay and negatives. Content-addressed exact set refs
may be shared only under identical population, condition, routing, measure and
wave identity. Forward/reverse F2, weighted/unweighted, missing/routing and
cross-wave sets remain separate. Replay re-executes and compares exact fact
refs; a cached fact is never authoritative.

**Invalidation:** any source/root/release/replay/universe/current/authority/
revocation change refuses or forces rebuild. One exact universe per index or
estate; no cross-wave pooling. F26 remains `K1-CAP-24` / `P4R-R02` /
`PYAT-PC-R11-21`.

**Recovery:** private stage, fsync, no-clobber claim/lease, manifest-linked
completion, typed orphan. A crash at any step must leave no readable incomplete
estate and must never delete/overwrite a completed or another writer’s release.
GC only proven-dead typed scratch. No false portable atomic-rename guarantee.

## 5. Cost model and measurement limits

**Cited witness (sourcefree, cut-specific, not native/100k acceptance):**
writer 3033.723 s; retained 310.16 MB; staging 5.26 GB; temporary I02 4.39 GB;
session index 1.30 GB; one selected query 562.362 s. These are disk/staging
figures, not RSS. The 3.245-events/respondent shape is sparse, not dense width.

**Corrected formulas:**

- one admission reused: `H + N·(S+Q+O)` for one shot per operation; true
  prepared same-process: `H + S + N·(Q+O)`;
- truly fresh each operation: `N·(H+S+Q+O)`;
- durable index: `H + I + N·(Q+O)`.

**Corrected evidence estimate:** 2 × 100,000 refs at 150–250 bytes is
30–50 MB per fact before provenance; 100 facts is 3–5 GB. Actual cardinality
and serialization are unknown. The 1.69–1.70× four-operation author report is
not a measured 100-op asymptote; any `S/Q` inference is hypothetical.

**Not measured/claimed:** native dense 100k 600–1,300 slots; process-tree
≤6 GiB; cold 1/10/100 native; production retained/scratch/output; durable-index
retained/invalidation; one-certificate full Q2 proof; native source rights.

## 6. One actionable first-consumer handoff — corrected D4 grades

### Direct prepared path — executed sourcefree

**ABI:** `rawlsing_next/pre553_prepared_saved_i03.py::PreparedI03Session.execute_i03`
via `PreparedSavedC11Admission.open`.
**Positive:** four distinct sourcefree operations (selected, F2 forward, F4 3+,
raw) return exact fact-ref parity with the one-shot baseline; one `_build` for
the workload (direct prepared test court).
**Negative:** revocation after preparation refuses; condition mismatch refuses;
changed member/root refuses.
**Restore:** exact manifest/I02/source restore reproduces the same fact
projections.
**Grade:** `EXECUTED_SOURCEFREE_DIRECT_PATH_3_OF_34` — valid direct prepared
session evidence, **not** the named Batch/wrapper path. Logs:
`RUNS/prepared_saved_i03.txt` (3 passed), `RUNS/direct_estate_i03.txt` (7 passed),
`RUNS/saved_native_first_consumer.txt` (24 passed).

### Wrapper/Batch path — proposed, not wired

**Named ABI:** `execute_saved_i03` / `execute_saved_i05` /
`execute_saved_batch`, plus `BatchExecutionRunner(saved_mode=True)`.
**Actual exact-type boundaries:** `pre553_saved_workload_integration.py` lines
42, 54 and 94 require `type(admission) is SavedC11Admission`;
`pre553_batch_runner.py` line 406 requires
`type(repository) is SavedC11Admission`. `PreparedSavedC11Admission` is rejected.
Moreover, `SavedC11Admission.execute_i03/i05` open a fresh
`DirectEstateI03Session`, so merely relaxing the type check would not reuse the
prepared session.
**Minimal owner-routed protocol:** an explicit prepared-session-aware adapter
(not generic `isinstance` relaxation), exact `PreparedSavedC11Admission`
whitelist, one prepared context per release/universe/workload threaded through
Batch units, per-unit `check_current`, exact fact/replay/negative, exact restore.
Owner: S2-D saved admission + BatchExecutionRunner owners; separate implementer
step.
**Grade:** `PROPOSED_NOT_WIRED`.
**Witness for the defect:** `WORKER_RETURNS/ANVIL_ARCHITECTURE_C_20261117/WITNESS/test_prepared_abi.py`
2 passed; both named paths reject the prepared subclass.

## 7. Remaining finite obligations

1. Owner-approved prepared-session-aware first-consumer/Batch adapter; one
   `_build` through the actual wrapper/Batch, four-operation exact parity,
   revocation/current refusal, exact restore. Current grade
   `PROPOSED_NOT_WIRED`.
2. Construction one-journal/one-certificate only after full physical proof
   against a **source-derived** Q2 certificate; second-certificate fallback
   mandatory otherwise. Q2 must not originate from a re-parsed transport
   journal.
3. Recovery repair with no-clobber claim/lease; crash-injection proof.
4. `#1006` H/S/Q/O measurement on one authorized real-width workload: 1/10/100
   same-process and 10 fresh-process, fact/replay parity, retained/scratch/RSS/
   output.
5. Durable index only if `S` material and compact exact encoding/binding/
   invalidation/retained-size gate passes; currently `HELD_NOT_SELECTED`.
6. Batch/NORMAL/resume shared-file owner ACKs.
7. Same distinct C recheck of this corrected candidate; then, only if accepted,
   competent H1.

All 26 NOT_ADOPTED, 14 HELD, 52/24/21 navigation, F26, native/source/science/
actor, 100k/6 GiB/1-10-100, F5–F8/N9/N10W/SEAM/SOROK remain held.
