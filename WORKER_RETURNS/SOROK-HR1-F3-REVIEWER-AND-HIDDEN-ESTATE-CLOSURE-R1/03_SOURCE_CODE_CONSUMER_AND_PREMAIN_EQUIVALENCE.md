# Source, code, consumer and PRE-MAIN equivalence

**Scope:** documentary I2 reconciliation at immutable Git objects. No branch code executed by this worker. “Code present” means the named Git blob exists at the named path and, where stated, an independent reviewer test imported or exercised it. It is not proof of semantic correctness, native authority or first product use.

## 1. The three reviewer targets

| Target | Reviewer cut / document | Author cut | Exact source blob(s) | Reviewer test / evidence | Original result |
|---|---|---|---|---|---|
| G17I | `156b84cc…`; `…G17I…/00_RETURN.md` blob `01f2db89…`, SHA-256 `b208dc74…` | `90d0eb79…` (`agent/rabochii-sorok-20261019-g17-…`) | `candidate/lab_sgi1/continuation.py` `c9318dcf…`; `c9_handoff_consumer.py` `47e59c12…`; both byte-identical in reviewer `target_candidate/` | `tests/test_g17i_independent.py` blob `83f17006…`; JUnit `0dec3faf…` | 11 PASS / 3 RED; `REVISE` |
| OC5E | `67a4f156…`; `…OC5E…/00_RETURN.md` blob `9897d7bb…`, SHA-256 `552fca27…` | `0caaec59…` (`agent/rabochii-sorok-r3-hq310-oc4-…`) | `repro/custody_protocol.py` `af2b7e94…`; author test `c139a877…` | `tests/test_oc5e_native_hostiles.py` blob `9837579e…`; JUnit `33efbc31…` | 159: 110 PASS / 49 RED; full 349: 283/66; `REVIEW_REVISE` |
| M04 | `3a993abc…`; `…M04-M03…/00_RETURN.md` blob `5840b2f3…`, SHA-256 `da0386eb…` | `e1f7a74e…` (`agent/rabochii-sorok-r3-hq313-m03-…`) | `candidate/cell.py` `3eb2d02a…`; `candidate/claim_provenance.py` `2434bda6…`; both identical in reviewer `candidate/` | `review/test_falsifiers.py` blob `8add06c6…`; JUnit `2f54f3e3…` | 51 fresh: 41 PASS / 10 FAIL; 587/587 unchanged; 9 historical FAIL; `REVIEW_REVISE` |

The G17I test file is explicitly reviewer-authored and says so in its module docstring. The OC5E court stages the author source by pinned blob and asserts the imported module is that blob (`test_oc5e_native_hostiles.py:62–74`). The M04 candidate blobs match the reviewer’s installed candidate byte-for-byte. These are executed review relationships, not commission-only prose.

### What is present versus what is validated

- G17I: the forged material path is present in `continuation.py:11–29` (payment is read from caller material without owner/permission authentication), the nested future-child bypass in `pipeline.py:88–109` (only top-level packet keys are guarded), and the C9 acceptance path in `c9_handoff_consumer.py:48–78`. The three reviewer assertions fail literally. Semantics beyond those tests are not validated.
- OC5E: the six defect families are present at `custody_protocol.py` `detect_leakage`/`require_second_signature`/`unblind`/`commit`/`capsule_envelope_commitment`; 49 reviewer assertions fail. The ten historical REDs are preserved; the seven OC5 predictions are confirmed natively. Test-only scope, mock signer and source-free corpus remain.
- M04: `claim_provenance.py:123–126`, `:200–226`, `:286–291`, `:339–349` contain the narrow checks that the ten fresh falsifiers defeat. The 587-case published expectation reproduces; the nine historical CAN3 cases remain separate literal FAILs.

No original RED was edited, softened or reclassified by this reconciliation. No original reviewer judgment was upgraded to native/scientific acceptance.

## 2. Outside-294 code/consumer map

The 377 selected tips are unchanged from their RC1 pinned SHAs at current `ls-remote` (2,851 heads; 2,831 in census, +20 names). Nineteen high-impact tips were diff/consumer-screened; 358 remain metadata-only. Presence of a path is not proof of adoption. The high-impact material map is:

| Branch | Material code | PRE-MAIN relation | First consumer |
|---|---|---|---|
| `codex/c12-perception-fork-repair-r1` `68b05865…` | `vendor/j/.../bp4/store.py` `c94cd131…`; `r26e/c12_integrity.py` `402c2b02…` | both paths **ABSENT** at `299f41e9…` | `tests/test_c12_fork_integrity.py` `78626103…`; test-only |
| `agent/opencode-pyat-r95-r06-world-consumer-integration-r1` `b2cfe93c…` | `rawlsing_next/pre553_universal_world_binding.py` `44ac11c9…` | **ABSENT** | `tests/test_universal_world_binding.py` `7095820c…`; CONTEXT structural authority HELD |
| `agent/rabochii-pyat-r3-hq284-l01-…` `c6dba4b7…` | `pre553_selected_world_progressive_contract.py` `e9caea54…`; `r3_s02_seam_witness.py` `408c4700…` | **ABSENT** | seam witness imports the contract; tests |
| `agent/rabochii-prev3-w11-m05-…` `15ab87cb…` | `prev3_objective_structural_topology.py` `f306745b…` | **ABSENT** | branch-local test only |
| `agent/rabochii-pyat-r3-hq292-i01k-…` `5e6e802f…` | `repro/check_i01.py` `81f67816…` (evidence/repro, no product source) | **ABSENT** | branch-local repro courts |
| `integration/prev3-w5-qualified-fanin-r1` `579ed550…` | `f07_second_canary_prev3_admission.py` `06c31220…`; `objective_consumer_bounded_evidence.py` `f30fca20…` | **BLOB-IDENTICAL** to PRE-MAIN; branch not an ancestor | PRE-MAIN tests; non-test F07 consumer not found |
| `agent/rabochii-warplan-gt12-c-…` `d30ca3b6…` | `field_forge_conditional_support.py` `a70decb2…` | **ANCESTOR + BLOB-IDENTICAL** | PRE-MAIN `gt12_c_to_d_relation_bridge.py` + tests |
| `integration/prev3-m3-r2-qualified-r1` `7ab8c40b…` | `m3_v556_higher_order_structural.py` `9a4b26b2…` | **ANCESTOR + BLOB-IDENTICAL** | PRE-MAIN `m4_v557_v558_publication_repository.py`; `pre553_v556_positive_substrate.py` |
| `agent/rabochii-warplan-gt12-d-…` `ab6d775e…` | `wave1_ff_prev3_relation_admission.py` branch `f6d02bf3…` | **ANCESTOR, BLOB DRIFTED** from PRE-MAIN `c5fb675f…` | PRE-MAIN GT12 bridges import the current, later blob |
| `agent/rabochii-wsc002d-gt0-prev3-r1` `a3d0609e…` | `wsc_gt0_prev3_bridge.py` branch `0f3dfcc5…` | **PRESENT, BLOB DRIFTED** from PRE-MAIN `8f237bd5…` | PRE-MAIN `wsc_gt0_end_to_end.py` calls `run_gt0_prev3` |
| `agent/rabochii-prev3-v3-world-context-typed-ingress-constitution-r1` `78e6001f…` | seven Markdown documents; `01_CONSTITUTION…md` `f07b113b…` | document-only | **NONE** |
| `agent/rabochii-warplan-gt12-r1b/gt12-f/vozhd-gt12` | test-only changes | ancestors; test blobs identical | PRE-MAIN tests |
| PFF G1/G2 `f4a61361…` | `03_UNIFIED_V3_PFF…md` `329d9f62…` | document-only | **NONE** |
| `agent/rabochii-pyat-hq280-pv3-d02y-…` `b3796f5c…` | rule-source HOLD documents | document-only | **NONE** |

### Drift and equivalence conclusions

1. **Landed:** GT12-C, GT12-R1B, GT12-F, GT12 central, M3-R2 and the w5 F07/objective modules. GT12-D is landed but its tested source blob has drifted; the current PRE-MAIN bridge uses `c5fb675f…`, not the branch’s `f6d02bf3…`.
2. **Candidate-only:** C12 fork integrity, R95 world binding, HQ284 selected-world runtime, HQ292 I01 repro, W11 topology. They have no PRE-MAIN path or consumer. Do not treat branch-local tests as adoption.
3. **Drifted:** WSC002D’s bridge exists in PRE-MAIN with a different blob. The branch test cannot be used as evidence for the current PRE-MAIN bridge without re-reading the current blob.
4. **Document-only:** PFF G1/G2 and typed-ingress constitution. They may identify semantic gaps, but they issue no rule and have no first consumer.
5. **No native authority:** none of the inspected code proves a first independent B actor, situated uptake/Rule A/T execution, C8 authority, C9/C12 cold reader adoption or A0–A5 continuity.

## 3. Adoption-order perturbation report — TENTATIVE_PLAN_HOLD

This is not an adoption plan. It is the smallest owner-order perturbation that keeps current authority intact:

1. **C12/BP4 owner first.** Decide whether the C12 fork/ancestry candidate is superseded, merged elsewhere or still proposed; identify the intended current reader. C12 reader/writer safety must not be inferred from the branch test.
2. **P41/R05/R06 owner second.** Resolve R95’s `pre553_universal_world_binding.py` against the current P41/R05 source and the held CONTEXT structural authority. Do not adopt the world binding before the P41 pin and R05 coordinator original are owner-confirmed.
3. **PRE-V3/Field Forge owner third.** Dispose of HQ284, W11 and HQ292 candidates; reconcile WSC002D and GT12-D drift against the current PRE-MAIN blobs. These are seam candidates, not new law.
4. **G17/OC5/M03 owners in parallel.** Repair the exact retained REDs against the same assertions. Only then commission a fresh reviewer per repaired cut.
5. **No merger of the 377 or 2,366 remainder.** Finish owner dispositions before any new census, branch adoption or semantic sweep.

Order is perturbed only if an owner produces an exact current source/consumer conflict with this map. A preserved negative or a named HOLD outranks a branch-name claim.

## 4. Smallest unresolved owner lists

- **G17 owner:** authenticate material owner/permission; recursive future-child partition; C9 source authentication.
- **OC4/OC5 owner:** typed malformed-signature handling; alias multiplicity and confusable scanning; unhashable holder typing; capsule field-type validation; holder-registry boundary.
- **M03/M04 owner:** actual first-state/pre-state ancestry; terminal applicable transition; genuine absence vs substituted NONE; atomic restore.
- **C12/BP4 owner:** fork root/prefix verification, legacy-root hold, atomic copy, reader/writer adoption.
- **P41/R05/R06 owner:** pinned runtime, trusted execution context, CONTEXT structural authority disposition.
- **PRE-V3/Field Forge/WSC owner:** HQ284/W11/HQ292 disposition; WSC/GT12-D blob drift; typed-ingress candidate authority.
- **HQ:** route the above; do not adopt; preserve original reviewer and source-owner jurisdiction.

## 5. Outstanding receiver

Incumbent Sorok/PRE-MAIN HQ for intake; separate source-qualified reviewer after this return; original component owners for any repair or adoption. This worker does not self-adopt and does not issue a scientific grade.
