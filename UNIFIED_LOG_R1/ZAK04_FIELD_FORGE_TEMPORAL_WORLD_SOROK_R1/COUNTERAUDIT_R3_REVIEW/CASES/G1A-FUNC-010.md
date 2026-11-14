# G1A-FUNC-010 — two distinct historical V551J certifications, one selected caller

**Inherited T owner:** G1-A. This is a corrected cross-reference, **not a newly discovered T**. Old source commit `25830fe7462bb9e29bc4087e6ae14f3f84cec377`: `ddm_v551j_certification.py` blob `21791659d4446b4c61097fdf6786f1bdae2aeeae`; compiler blob `2df97875172778c3f4616c0799c08667b57db407`. Modern protected commit `6a5c12f04323d74001f9632063ec907f4fc4468e`: `pre553_j_role_certification.py` blob `d96e0b1230b38c59ba4fa7716d6dfd3b9fdbe889`. Evidence R3:EV:010:* and operations R3:OP:010:*.

## Original computation and use

### Called v2.2.3 path — R3:OP:010:V223

**Inbound:** (i) candidate packet DataFrame, keyed `packet_id` and `pattern_id`, with status fields `joint_semantic_authority_status`, `joint_support_status`, `denominator_separation_status`, `runtime_use_class`, etc.; (ii) component DataFrame grouped by packet and ordered `item_order`, with distribution IDs and exact question/response/polarity matches; (iii) `validation_report` dict whose candidate/component contract booleans must both hold. See R3:SH:010:V223_IN and source L23–60.

**Transformation:** group components, compute 22 named booleans, then `certified=all(gates.values())`; select `CERTIFIED_JOINT_RELATION_EVIDENCE` if all pass, `REVIEW_REQUIRED_COMPONENT_GAP` if and **only if** the sole failed gate is `pattern_support_gate`, otherwise `BLOCKED_PACKET_CONTRACT`. Set explicit future V552J linkage booleans only on certification, recompute packet contract hash, and emit tuple `(finalized,certified,audit,rejection)`. See R3:EV:010:CANONICAL / :SUPPORT.

**Crucial negative capital:** `forbidden_inference_gate` at L57 is unconditionally `True`. This *local named gate* cannot reject a forged forbidden claim; the separate `permission_boundary_gate` does inspect forbidden downstream permission flags. Do not infer global absence of upstream protection. See R3:EV:010:NOOP and R3:EDGE:010:FORBIDDEN_NOOP.

### Alternate review-surface path — R3:OP:010:REVIEW_ALT

**Inbound:** `candidate_trace` and `review_surface` with packet/source/authority status and `forbidden_claim_ids_json`. **Actual checks:** `_gate_results` L201–236 requires three named prohibitions (nonperson-belief, noncausal, nonruntime-psyche), checks required temporal/orientation/pressureflow mediation flags, and refuses nonempty downstream leakage fields including `actor_absorption`. **Outputs:** certified index, audit, rejection, readiness report; unlike the canonical function it is not the one called by the inspected compiler. See R3:EV:010:ALT / :CALL. It has different schemas and cannot be folded into canonical v2.2.3 OP.

## Illustration — fields and opposing branches (NOT a test)

Assume all other original required fields/gates satisfy their contracts:

`candidate.packet_id="P"; pattern_id="joint-pattern"; joint_support_status="supported"; denominator_separation_status="PASS"; runtime_use_class="not_runtime_consumable"`, with two matched ordered exact component rows and validation_report `candidate_contract_valid=True, component_contract_valid=True`. Under those assumptions, V223 returns a certified packet and V552J linkage markers. Changing only `joint_support_status="insufficient"` produces support-only review; setting `ready_for_v553=True` additionally produces a general blocked packet. Critically, populating `forbidden_claim_ids_json` **does not affect the V223 `forbidden_inference_gate`**, but the alternate builder directly examines that field. Not executed; these illustrate source branches, not proof of reachable selected production bundles.

## Old reader and modern contrast

`compile_v551j_joint_evidence_packets.py#L1320–1328` directly invokes **V223** and writes compatibility `v551j_certified_packet_index.parquet` at L1542–1549. The alternate function is imported but not used at the inspected callsite. No native V552J first-consumer run is proven. Modern `j_component_certification_validator` at protected L1257 constructs M1 validator results from an exact J family/item role channel with six-token role vocabulary and six contribution classes, **not an identical packet certificate**. Its content-addressed/authority and negative states may be reusable, but not a substitute for V223 identities/support/denominator/forbidden-leak behaviors without a source-qualified paired case. See R3:EV:010:MODERN.

## Disposition / next owner decision

Retain both old implementations and distinguish selected compiler path, no-op false-safety flag, support-only vs blocked, modern J contribution and still-unproved packet-to-reader succession. G1-A owns historical T; ZAK04 the interface; J/M1 source/science issuer any actual permission. Smallest authorized research next: inspect a selected real packet, full runtime-authorized gates and same-grain M1 outcome/first reader, with negative contrast. **No tests or authority issued here.**
