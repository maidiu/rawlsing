# ANVIL R7 — A0 RETURN (architect A, independent, blind to B)

**Verdict:** `A0_FROZEN` (design only)
**Stage:** A0 / C11_QUERY_DESIGN
**Source cut:** `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`
**Prior tested baseline:** `b830458c3ebfe0a3f0e2d18e516e68b90324c88a`
**Protected head:** `7fc00289dd801d2d0a8ce159986c7595fc27a4d9`
**Design commit (frozen design HEAD):** `79293eb0964c69e5e0a7ded9c20d39d57d179349`
**Design blob:** `217d958e5ef023598139e6397f52e95fbce48f32`
**Design file SHA-256:** `ce7e165a20dac2c99e246c9c6d27c70498359180013e04c0a21685d146a951b8`
**Proof grade:** S0/S1 source-static. No P15, native, source, science, actor, independent-review or protected-adoption claim.

---

## 1. What was actually read

- HQ oath read file at the supplied path, including the user-direction note: the oath was read in full at `PR1098@1341c81d`; the draft is not protected adoption. The earlier H0 missing-oath hold is historical and resolved; it is not treated as a blocker.
- `H0_STAGE.json`, `H0_PROBLEM_FROZEN.json`, protected PYAT CURRENT_PROGRESS JSON/MD, `H0/HISTORICAL_FIVE_TEST_LAW.md`, and evidence for `#997`, `#1006`, `#998`, `#1097`, `#909`, `#960`.
- Actual startup source under `rawlsing_next/` at `cea2d4d3`, including:
  - Q2 handoff and body transport: `pre553_source_i02_handoff.py`, `pre553_source_i02_streams.py`, `pre553_source_saved_body_bridge.py`;
  - S2-B direct I02: `_pre553_direct_i02_sourcefree.py`;
  - S2-C writer/estate: `pre553_source_direct_parquet_estate.py`;
  - S2-D readers: `pre553_direct_estate_i03.py`, `_pre553_query_common.py`, `_pre553_query_eval.py`, `pre553_empirical_query.py`, `pre553_discovery_exact.py`;
  - saved/prepared admission: `pre553_saved_c11_admission.py`, `pre553_prepared_saved_i03.py`;
  - Batch: `pre553_batch_runner.py`, `pre553_saved_workload_integration.py`;
  - legacy repository: `pre553_c11_repository.py`;
  - tests: `test_pre553_prepared_saved_i03.py`, `test_pyat997_s1e_saved_source_bridge.py`, `test_pyat991_s2d_five_readers.py`, `test_pre553_direct_estate_i03.py`, `test_pre553_i03_grouping.py`, `test_pre553_empirical_query.py`, `pyat1001_scale_harness.py`.
- Prior evidence package `WORKER_RETURNS/PYAT_P0_C11_OPERABLE_20261115_R1` at the same cut, used as **historical anchor evidence**, not as new measurement.

No other lane worktree, output, branch or substantive B finding was read.

---

## 2. Sourced findings that change the design

1. **The #997 body iterator is not missing at this cut.** `SourceSavedBodySink` plus `SourceI02BodyTee` already provide a tested one-pass 13-family body bridge into the unchanged S2-C writer. The existing test asserts one source open, one decode, one cell pass, zero full-C11 builds, exact family counts, 14 Parquet members and no surviving SQLite/journal. The honest residual is cost and integration economics, not absence.
2. **The prepared-session candidate is real and measured at tiny/small sourcefree scope.** One index build is reused across four I03 operations and I05 discoveries, with exact fact/projection parity, revocation/restore and condition refusal. Prior evidence reports 1.688× (128 R × 5 Q, 100 ops) and 1.705× (64 R × 30 Q, 20 ops) speedups with exact parity.
3. **The prepared session does not remove the dominant repeated-query cost.** Prior evidence still reports 71,304 row-group reads for 20 prepared operations at 64 respondents (3,565 reads/op). The current reader resolves each side-family member by reading the whole Parquet row group, and each event by row-group reads. At 100k respondents this is the decisive economic risk, not index rebuild.
4. **The Batch prepared path has an exact ABI defect.** `PreparedSavedC11Admission` subclasses `SavedC11Admission`, but `execute_saved_batch` and `BatchExecutionRunner.__init__` use exact `type(...) is SavedC11Admission` guards. Batch therefore rejects the prepared admission and currently rebuilds one session per unit. A two-function owner edit is required for prepared Batch; I03/I05 do not require it.
5. **The frozen S2-C cold open hashes all 14 members on every open.** That is proof cost, not a bug. At 100k it may cost seconds to tens of seconds and must be measured, not hidden.
6. **The 100k/6 GiB failure is real but belongs to an older path.** Old W03/saved-artifact evidence includes ~5.923 GB persistence RSS and a 6.468 GB saved-artifact peak above the 6 GiB cap. The current S2-C/D path is different and unmeasured at 100k; neither success nor failure transfers by assertion.
7. **The complete sealed corpus can be built without C11Repository.** The direct estate and saved admission deliberately avoid the legacy full-object graph. This design keeps that avoidance.

---

## 3. Selected A0 design

**A0-A: Prepared, Body-Complete Cold Saved Estate (BCPPI)** — compose, adapt, repair:

```text
one Q2 source pass -> SourceSavedBodySink/tee -> frozen write_direct_estate
-> complete 13-family Parquet/Zstd estate + manifest
-> fresh VerifiedDirectEstate + SavedC11Admission.open
-> PreparedSavedC11Admission.prepared_i03()
   -> one execution-local DirectEstateI03Session
   -> A2: extend its existing events/members SQLite with authenticated body_json
   -> native execute_empirical_query (I03)
   -> native execute_exact_bounded_discovery (I05)
   -> Batch: two-function owner edit to reuse the same prepared context
```

A1 is the unmodified prepared session (measured fallback). A2 is the physical
repair that removes respondent-major Parquet row-group amplification by
materialising the already-authenticated event and three I03 side-family bodies
into the existing temporary SQLite index. A2 changes no semantic owner: the
same `_ReleaseIndex`, `_evaluate_index_group_core`, facts, negatives and replay
remain. It grows transient scratch; that is an explicit P15 falsifier.

The 22 H0 cells are mapped to six proposed profiles W-S/W-D/W-R/W-O/W-J/W-X in
`A0_P15_PLAN.json`. These profiles are **not frozen or executed by A0**; the
P15 controller must freeze counters before comparison.

---

## 4. Strongest self-objection

A1 is only an index-rebuild optimization. Its measured 1.7× is real on small
fixtures but does not prove 100k economics; the 3,565 row-group reads/op at 64
respondents is evidence against linear scaling. A2 is unmeasured and may
increase index build time and scratch to the point of disk failure, while still
retaining the writer's body_json/typed-column duplication and second I02
certification. A rival with a persistent compact respondent-major index or a
dense typed substrate could win W-D/W-O, and an eager compact design could win
repeated cold F4. The design must not be promoted to "economical" without
matched 100k P15; A1 must not be called a modern production speedup.

---

## 5. Decision-changing falsifiers (short form)

- process-tree RSS > 6,442,450,944 B at any W-S/W-D/W-X cell;
- retained + scratch over the compact/disk budget, or 100k build unable to
  complete on available disk;
- A1/A2 row-group reads scaling linearly with respondents, or A2 not materially
  improving repeated operations;
- any W-J same-respondent joint denominator/support/projection mismatch;
- routing/risk or typed negative coerced into membership/EMPTY/ZERO;
- second source decode, family/count/absence drift, forged locator/body or
  surviving journal/SQLite in the committed estate;
- served result after revocation or failure to restore;
- Batch exact-type guard not lawfully widened, making prepared Batch a
  conditional non-result;
- W-S build wall materially above the frozen P15 bound;
- invalid source/rights/current callback.

Exact reversers and the 14 candidate-veto receipts are specified in
`A0_DESIGN.md` §8–§10 and `A0_P15_PLAN.json`.

---

## 6. Proof grade and unrun/held limits

- **Executed by A0:** file reading, Git inspection, static source/evidence
  comparison, design authoring, hash/manifest generation. Nothing else.
- **Not executed:** P15, 100k, native tests, performance runs, source/native
  data access, original35, S2/S3, Batch edit, P2, C, H1, reciprocal exchange.
- **Held:** source/science/actor/host rights, protected merge/CAS, independent
  review, model/provider change, other worker outputs, original survey data.
- **No invented receipt:** all performance numbers in the design are labelled
  as sourced anchors, sourced estimates or explicit unknowns.

---

## 7. Next eligible stage

A0 is frozen at design commit `79293eb0964c69e5e0a7ded9c20d39d57d179349`.
After B0 is independently frozen, conduct one bounded A1/B1 reciprocal
critique, then matched P15 under the controller's pre-result frozen plan.
Do not treat this return as permission to build, measure, merge, or claim
first effect.
