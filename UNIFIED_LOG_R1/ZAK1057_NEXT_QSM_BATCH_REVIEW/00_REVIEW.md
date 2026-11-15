# ZAK1057 — independent review of the selected-QSM→Batch boundary

**Review ID:** `ZAK1057:NEXT:QSM_BATCH_REVIEW`.
**Role:** distinct nonauthor documentary reviewer; no subagents; no provider/model change.
**HQ cut:** `81c7b5a05ebc2d16d5729ab6a8b190ce88fc7507`.
**Frozen target:** `ac736ecbf13cb390faf676571a72598d03833847`, `UNIFIED_LOG_R1/ZAK03S_CODEX_CAMPAIGN_R4/`.
**Verdict:** `REVISE_EXACT_DOCUMENTARY_DEFECT`.

## 1. Answer

The source establishes a **missing demonstrated selected-QSM importing/provenance edge** at the inspected cuts, but the return overreaches from that observation into proposed architecture. The factual core survives; the claim that Batch needs a “unit/result slot” and the proposal that the issued envelope needs a QSM field/sub-request are not source-established requirements. Batch already has generic `semantic_input_refs` and `ExecutionOutcome.provenance_refs` that accept arbitrary `ExactRef`s, and the Batch receipt builder already propagates unit semantic inputs into `provenance_refs`. The real missing piece is a **canonical selected-QSM ExactRef/canonical object plus a demonstrated issued-workload carrier/call path**; the concrete schema form is an owner design decision.

Equal empirical facts across different QSM bindings are **not inherently a defect**. The static test shows separate identity/provenance layers, which is consistent with the candidate’s own `selected_binding_first_importing_reader: NOT_PROVED` and `issued_batch_consumption_of_selected_qsm: False`. The return does not call it a bug, and this review does not either.

## 2. Factual claims that survive

1. **Sibling binding.** At `0d90c247`, `SelectedQsmRouteResult` has exactly `route: RouteBProductionResult` and `binding_receipt: Mapping[str, Any]` (blob `d3c6c4e8...`, L94-L98). The receipt carries `qsm_artifact_sha256`, `qsm_row_sha256`, `qsm_rule_id/version`, `qsm_resolution`, `qsm_lookup`, I03/I05 refs and a `binding_root` (L278-L311). The earlier candidate has the same sibling shape (blob `07bd2b2c...`, L93-L96, L260-L300).
2. **Static test assertion.** The test asserts different QSM files/rows produce the same I03 fact ref while `binding_root` and `qsm_resolution` differ (`0d90c247` test blob `5ef5ae47...`, L146-L184, especially L178-L180). Read statically; **NOT EXECUTED**.
3. **No QSM in the route/I03/I05 results.** `RouteBProductionResult` has `source_identity`, `projection_binding_receipt`, `repository_binding`, `c11_release`, `i03_results`, `i05_result`, `object_graph`, `learned_empirical_execution_receipt`, `replay_receipt` (blob `5b28d6c0...`, L153-L164). `I03ExecutionRequest` carries only `query_ref`/`predicate_ref` (L106-L130); `QueryExecutionResult` only query/facts/scope/release (blob `40b1a9c9...`, L105-L122); `ExactBoundedDiscoveryResult` has no QSM field (blob `1b82b6df...`, L127-L142). Survives.
4. **Batch typed refs.** `JOB_KINDS = {"QUERY","DISCOVERY"}` (blob `2d291600...`, L23); `BatchUnitSpec.semantic_input_refs` and `ExecutionOutcome.provenance_refs` require `ExactRef` tuples (L100-L151, L215-L226). The candidate `binding_receipt` is a plain `Mapping` with a hex `binding_root`, not an `ExactRef` (reader L278-L311). Survives.
5. **Issued workload.** `NativeWorkload` has no selected-QSM field; `envelope()` is closed over descriptor/projection/catalog/requests/discoveries/roots; `admit()` compares its hash and `expected_jobs` (blob `28174766...`, L188-L216, L247-L253). `execute_issued_workload` calls `execute_route_b_production` directly and builds Batch units from `workload.requests` with `(r.predicate_ref, workload.decision_ref)` (L280-L367). It does not call `execute_selected_qsm_route_b` and has no selected-QSM parameter. Survives.
6. **No protected QSM consumer / no non-test candidate caller.** `git grep` at 6a finds no protected `SelectedQsm`/`selected_qsm`; at `0d90c247` the only caller is the static test. The learned-world composition consumes `RouteBProductionResult` but projects replay/object-graph refs, not QSM (blob `adbcc331...`, L50, L740-L767, L1043-L1070, L1121-L1126). The non-test issued-workload caller `pre553_native_workload_binding.py` (blob `dac73e48...`, L433) also supplies no QSM binding. Survives as a bounded negative.

## 3. Where the return overreaches

**A. “No Batch unit/result slot” is wrong as stated.** `RETURN_VERDICT.json` `missing_edge_vs_engine.missing_edge` says “no Batch unit/result slot.” Batch already has generic `semantic_input_refs` and `provenance_refs`; any `ExactRef` can enter them. The Batch receipt builder includes `unit.semantic_input_refs` in receipt `provenance_refs` and requires completed receipts to contain job/release/input provenance closure (blob `2d291600...`, L470-L535). If a typed selected-QSM `ExactRef` existed, Batch could carry and conserve it **without a new slot or job kind**. The missing piece is the producer-side canonical ref, not the Batch slot.

**B. “Batch would need a unit kind or explicit semantic-input convention.”** A semantic-input convention is enough; a new job kind is not required. `semantic_input_refs` is generic and already part of the unit projection/hash. The return’s “or” includes the correct option, but the “unit kind” alternative is an unnecessary architecture proposal.

**C. “Issued workload would need a QSM field or sub-request in the issued envelope.”** This is one possible architecture, not a source-established requirement. The source shows the issued envelope is closed and hash-checked and that no QSM carrier exists; it does **not** establish that the only lawful form is a QSM field/sub-request. A separately issued exact ref, a new issuer-covered envelope field, or a new generic provenance parameter are all owner design options. The return’s four-part requirement list (00_RETURN §3(a)-(d)) is therefore proposed architecture, not an observation.

**D. “Batch/result representation that preserves the binding as an exact ref or typed receipt.”** The existing Batch representation already preserves any `ExactRef` supplied as a semantic input into receipt provenance. The missing item is the exact ref itself, not a new representation.

**E. “Typed binding object and exact ref” as a “smallest lawful need” is partly right.** It is correct that a canonical exact identity is absent. It is not correct to pair that with “no Batch unit/result slot” or to imply a new Batch slot/job kind. The smallest actual need is: (i) an existing canonical `ExactRef`/object for the selected-QSM binding; (ii) a demonstrated issuer→issued-workload→Batch carrier and call path for it. The exact schema is an owner decision.

## 4. Smallest actual unresolved edge

**No existing canonical selected-QSM binding identity and no demonstrated issued-workload carrier/call path.** The candidate has a plain mapping with a stable `binding_root`; Batch generic slots could carry an `ExactRef` if one were produced; Batch receipts would conserve it; the issued workload lacks a demonstrated way to receive and pass it to the selected-QSM gate. This is an **absent demonstrated wiring / producer-to-consumer edge**, not a missing engine, not a violated empirical-fact contract, and not proof that generic Batch transport is impossible.

## 5. Source checks (exact)

| Claim | Commit/path | Blob | Lines |
|---|---|---|---|
| Candidate sibling binding receipt | `0d90c247:rawlsing_next/pre553_zak03s_selected_qsm_reader.py` | `d3c6c4e8a32398a3c4977ed287684bd95d058df3` | L94-L98, L278-L311 |
| Earlier candidate sibling shape | `ad17076c:rawlsing_next/pre553_zak03s_selected_qsm_reader.py` | `07bd2b2c88787e8b2091e652c677864be2ba5244` | L93-L96, L260-L300 |
| Static A/B test assertion | `0d90c247:rawlsing_next/tests/test_pre553_zak03s_selected_qsm_reader.py` | `5ef5ae473420dd314256898e44c10cb3b9821741` | L146-L184 (L178-L180) |
| Route B result fields | `6a5c12f0:rawlsing_next/pre553_route_b_production.py` | `5b28d6c0c4f9bc032088cf660834ad574b8c8446` | L106-L164 |
| I03 result fields | `6a5c12f0:rawlsing_next/_pre553_query_common.py` | `40b1a9c974332db64d10b95d87682fd04be95063` | L105-L122 |
| I05 result fields | `6a5c12f0:rawlsing_next/pre553_discovery_exact.py` | `1b82b6df993bf14afa5e78782d988cba6e76b668` | L127-L142 |
| Batch typed refs and receipt conservation | `6a5c12f0:rawlsing_next/pre553_batch_runner.py` | `2d291600b9a10c56d9c6f6de7f7d619f6c52e829` | L23, L100-L151, L215-L226, L470-L535 |
| Issued workload envelope/call path | `6a5c12f0:rawlsing_next/pre553_issued_workload.py` | `28174766f61a15f7296f575d615462d6410cfcb6` | L188-L216, L247-L253, L264-L277, L280-L367 |
| Projection binding receipt is a mapping | `6a5c12f0:rawlsing_next/pre553_carrier_execution.py` | `ee9b3af02bfca9238eb72ea45d94073d47769a07` | L194-L221 |
| Non-test issued-workload caller | `6a5c12f0:rawlsing_next/pre553_native_workload_binding.py` | `dac73e484f8619088f5c6701b2b6991c07540f3b` | L365-L443 |
| Learned-world alternate consumer | `6a5c12f0:rawlsing_next/pre553_learned_world_composition.py` | `adbcc3316920c708580097dfe9f5aef4c9ca82fb` | L50, L740-L767, L1043-L1070, L1121-L1126 |
| ExactRef definition | `6a5c12f0:rawlsing_next/pre553_empirical_objects.py` | `a61365b994e5c3c50de0f598fcf40e90abf757b6` | L280-L303 |

## 6. Omission challenge

Searched `binding_root|binding_receipt|SelectedQsmRouteResult|projection_binding_receipt|semantic_input_refs=` at `0d90c247` and `6a5c12f0`. Result: `binding_root` is consumed only by the candidate reader and its static test; existing `projection_binding_receipt`/`repository_executor_binding_receipt` are generic **projection/repository** mappings produced by Route B, not selected-QSM bindings; no protected `semantic_input_refs` producer passes a QSM binding. The non-test issued-workload caller `pre553_native_workload_binding.py` was not named in the return but supplies no QSM. This does not overturn the return; it confirms the missing edge is a producer/carrier edge, not a Batch slot gap.

## 7. Proof ceilings

S1 static documentary only. The candidate test is read, not executed. No runtime, adoption, native/scientific/actor/source issuance, security defect, missing-engine claim, or implementation authority. The bounded negatives do not exclude dynamic/external callers or differently named artifacts. The prior I04 constructor investigation is not reopened; no adapter is designed here.

**Terminal:** `REVISE_EXACT_DOCUMENTARY_DEFECT__CORE_EDGE_SURVIVES__BATCH_GENERIC_SLOTS_AND_RECEIPT_CONSERVATION_EXIST__QSM_FIELD_OR_UNIT_KIND_IS_PROPOSED_ARCHITECTURE__SMALLEST_EDGE_IS_CANONICAL_QSM_EXACT_REF_AND_DEMONSTRATED_ISSUER_BATCH_CARRIER`.
