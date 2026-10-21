# E41 — Full qualified F1–F4 empirical production and N10E computed possibility (R41)

**Branch:** `agent/rabochii-pyat-r41-e41-full-f1f4-n10e-empirical-r1`
**Sealed startup:** `c4934fd71120d37a4d06f7c830891e6e97fe4ecf`
**Agent/model:** OpenCode on user's main Mac · DeepSeek V4.1 Flash · Standard effort
**Role:** bounded native implementation worker. NOT HQ, semantic/source issuer, independent
acceptance reviewer, actor or N11/N12 authority.
**Disposition of this return:** SOURCEFREE / RETAINED-quality work at TEST_ONLY grade.
Computed N10E slice evidence and real consumer receipts are produced; **no source,
model-use, original-35 occupancy, N11 or production right is claimed or implied.**

---

## 1. What was actually delivered

1. **Independently frozen expected-use universe** (31 operations across 14 families),
   derived by hand arithmetic on literal frozen source tables *before* any tranche
   execution — `frozen/expected_use_universe.json`
   (`sha256 6545ef2cdda5f9dff0c5053c20c290a1f09120a05a2b22035c05cd220ce1000a`),
   receipt in `frozen/FREEZE_RECEIPT.json`.
2. **Versioned permission-bounded public extension** of the accepted N10E provider:
   `e41_provider_extension.py` (`N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER_EXT@1.1.0`)
   exposing the already-lawful multi-conditioner, I05 exact-bounded discovery and
   MX01R2 recursive routes by delegating to the accepted owners
   (`provide_empirical_possibility_slice` for the direct route — object-identity
   reuse — and `compose_positioned_subject_possibility` for the other routes).
   Provenance/contract: `empirical_slice_provider_contract.md`.
3. **Whole-tranche executor** `e41_tranche.py`: 31/31 operations executed through
   real owners, **0 dropped, 0 unexpected, 0 mismatched** against the frozen
   universe. Artifacts:
   * `artifacts/f1f4_coverage_ledger.json` (per-op expected/actual, counts,
     denominators, predicate roles, grades, held-original-scope block)
   * `artifacts/f2_predictor_surface.json` (F2)
   * `artifacts/f3_branch_alternatives.json` (F3)
   * `artifacts/f4_cloud_joint.json` (F4)
   * `artifacts/computed_slice_evidence.json` (18 producer-derived slices)
   * `artifacts/slice_consumer_receipt.json` (18 real consumer receipts)
   * `artifacts/anti_join_expected_actual.json`
4. **Original E04 client consumption:** the byte-identical vendored original
   `product.nonparent.consume` (`NONPARENT_OPTIONS`) consumes E41-computed slices
   through `e41_e04_service.py`; receipt state `OPTIONS_AND_SOURCE_SUPPORT_PRODUCED`,
   route probability explicitly null, 7 value-reads with exact evidence refs.
5. **Courts + fault witnesses:** `test_e41_tranche.py` — 16/16 PASS
   (JUnit `evidence/e41_junit.xml`), including discriminators (a)–(f) and the
   no-drop, minority-preservation and cold-replay controls. Shared proof gate:
   3/3 claims `BASELINE PASS / TARGET_ASSERTION_FAILED`
   (`evidence/proof_witness.json`), contract `test_e41_tranche.py.proof.json`.
6. **Held original science preserved, not disguised:** `original35` U/E_pre remains
   `UNISSUED_HELD`; 0 authorized original reads this pass; exact LiTS C11 custodian
   blocker and O35B counts carried in the ledger (`held_original_scope`).

## 2. Coverage breadth (F1–F4, N10E)

| Family | Ops | Route(s) exercised | Grade |
| --- | --- | --- | --- |
| AT07 bidirectional direct (F2) | 2 | accepted provider (direct) | sourcefree fixture |
| AT08 attitude conditioning (F2/F4) | 2 | multi-conditioner direct | sourcefree fixture |
| AT09 joint configuration (F4) | 3 | multi-conditioner direct | sourcefree fixture |
| AT10 branches + discovery (F3) | 4 | direct ×3 + I05 discovery | sourcefree fixture |
| AT11 recursive depth-2 (F3) | 1 | MX01R2 recursive | sourcefree fixture |
| AT12 co-travel cloud (F4) | 1 | direct | sourcefree fixture |
| AT13 ranked non-scalar (F4) | 2 | direct | sourcefree fixture |
| AT14–16 typed states (F1/F3) | 9 | owner typed-state projections | sourcefree fixture |
| AT17 successor identity | 2 | accepted provider | adopted freeze |
| AT18 fresh-process replay | 1 | accepted provider + accepted fresh runner | sourcefree fixture |
| AT19 selective invalidation | 1 | join lifecycle owner | sourcefree fixture |
| Learned M01→M1→M2→B5→I4 | 1 | accepted learned-world owner | sourcefree fixture |
| Source-backed physical→C11→I03 | 1 | accepted facade (deterministic parity) | sourcefree fixture |
| Original E04 NONPARENT_OPTIONS | 1 | vendored original client | sourcefree TEST_ONLY |

Raw counts/denominators: every row of the ledger carries exact expected/actual
cells and denominators (e.g. 54/60 yes, 27/31 P1, 54/60 support, 8/40 oppose,
XOR joint decisive vs flat unary, 3/10–8/8–2/2 branch structure, 2/3 co-travel,
depth-2 cohort 4→2 with Y 1/2).

## 3. Frozen discriminators — actual results

| Discriminator | Court | Result |
| --- | --- | --- |
| (a) eligible op removed from submitted workload | `test_no_drop_discriminator_a_dropped_eligible_operation_is_detected` | RED on the frozen no-drop assertion (`dropped_operations == ['f2.at07.forward']`) |
| (b) condition-value/fact edge severed | `test_discriminator_b_severed_condition_value_edge_reds_named_consumer` | honest positive reaches consumer; false pairing witness ⇒ typed refusal (`ConditionValueRelationMismatch`), no geometry |
| (c) minority mass changed, majority preserved | `test_discriminator_c_...` | majority A unchanged 3/10; minority B 8/8 → 6/8 with distinct composed identity |
| (d) wrong orientation / wrong denominator | `test_discriminator_d_...` ×2 | forward producer + reverse consumer ⇒ typed refusal; wrong-denominator actual flagged (cell + denominator diffs) |
| (e) release revoked/empty | `test_discriminator_e_...` | typed refusal, no evidence fabricated |
| (f) restoration + cold replay | `test_discriminator_f_...` | fresh-process identity EQUAL, 60 denominator, yes=54/no=6 |

## 4. Integration hand-back

* **P41** (generic progressive N10W serving): the extension receipt v1.1 exposes
  route + discovery/recursive refs and coverage state per slice — the exact
  producer-side contract P41 can consume for progressive conditioned serving.
  `artifacts/computed_slice_evidence.json` and `slice_consumer_receipt.json` are
  machine-ingestible (`schema` + per-op refs).
* **A41** (N11 acceptance assembly): `f1_f8_acceptance_matrix.json` rows for all
  F2/F3/F4 cells can cite this return's per-op refs (evidence/composed/consumer
  hashes) and the held-original-scope block verbatim; the F1 substrate rows cite
  the typed-state and source-backed ops.
* **Not** handed over: any original-source occupancy, U/E_pre, model-use,
  selected-world/N9, N10W issuance or production right.

## 5. Exact remaining gaps (finite)

1. **Original-35 U/E_pre remains unissued.** Original LiTS closure still misses all
   15 native C11 `SourceReleaseCandidate` sections; exact custodian delivery
   request already exists at O35B `c714af26a…`. Owner: HQ/custodian.
2. **No measured original survey read this pass** (0 authorized reads): the
   computed tranche is sourcefree/retained-grade only.
3. **F5–F8 remain outside this campaign** (W41/P41/A41 lanes); no selected-world,
   no multi-field composition, no temporal field, no issued N10W.
4. **E04 consumption is TEST_ONLY** through the vendored client; promotion of the
   adapter requires its own competent decision (as E04L/R39I established).

## 6. Environment and cost

See `environment_passport_delta.json`. Provider/model: OpenCode harness,
DeepSeek V4.1 Flash, standard effort. Incremental billed cash: **UNKNOWN**
(user-provided session; no billing telemetry observed). Retries: 2 in-pass
expectation/runner corrections, all visible in commit history.

## 7. Files and verification

All files under `WORKER_RETURNS/PYAT-R41-E41-FULL-EMPIRICAL-F1F4-COMPUTED-POSSIBILITY-R1/`.
Reproduce:

```bash
cd <worktree root>
python3 WORKER_RETURNS/PYAT-R41-E41-FULL-EMPIRICAL-F1F4-COMPUTED-POSSIBILITY-R1/e41_frozen_expectations.py   # re-freeze
python3 WORKER_RETURNS/PYAT-R41-E41-FULL-EMPIRICAL-F1F4-COMPUTED-POSSIBILITY-R1/e41_tranche.py                # run tranche + artifacts
PYTHONPATH=rawlsing_next/tests python3 -m pytest WORKER_RETURNS/PYAT-R41-E41-FULL-EMPIRICAL-F1F4-COMPUTED-POSSIBILITY-R1/test_e41_tranche.py -q
PYTHONPATH=rawlsing_next/tests python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness WORKER_RETURNS/PYAT-R41-E41-FULL-EMPIRICAL-F1F4-COMPUTED-POSSIBILITY-R1/test_e41_tranche.py.proof.json --root . --receipt WORKER_RETURNS/PYAT-R41-E41-FULL-EMPIRICAL-F1F4-COMPUTED-POSSIBILITY-R1/evidence/proof_witness.json
```

**No** original-source grant, production adoption, Sorok actor, N11 or N12 authority
is created by this return.
