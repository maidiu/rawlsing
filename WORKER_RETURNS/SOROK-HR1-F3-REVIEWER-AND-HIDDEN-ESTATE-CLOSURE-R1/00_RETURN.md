# SOROK HR1 F3 — reviewer target and hidden-estate source closure

**Claim grade:** `BOUNDED_SOURCE_RECONCILIATION__ENGINEERING_RED_OR_HOLD__NO_ADOPTION`.

This is a source-free I2 documentary reconciliation. It does not issue native truth, a new semantic rule, an original review grade, or a PRE-MAIN adoption. The three original reviewer cuts are treated as evidence of what those reviewers found; their REDs are preserved, not overridden.

## Identity and custody

- Repository: `maidiu/rawlsing` (private).
- Return branch: `agent/sorok-hr1-three-reviews-hidden-estate-source-close-20261029-r1`.
- Sealed startup: `3fd8dcb3df520806c7aee820e511092863545f4e`.
- Prompt head at start: `1cc63e34ea2ebdf9391198b439c06c3e80e3668a`.
- Actual editor/model: OpenCode / DeepSeek V4.1-Flash.
- Host/worktree: macOS local host; isolated worktree `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/hr1-f3-estate`, based on `1cc63e34…`.
- Read-only sources: immutable RC1 `337896aa995d579e3525588b405d07216709ac15`, independent HR1 `40df1e61fb32f9210839d8ddfa9f8bf9a47d7621`, PRE-MAIN pin `299f41e97a43c67be9cc76a79fa49b48f4e12e54`, original author/reviewer cuts below.
- Write scope: only `WORKER_RETURNS/SOROK-HR1-F3-REVIEWER-AND-HIDDEN-ESTATE-CLOSURE-R1/**`.
- No PRE-MAIN, PR #514/#516, author, reviewer, RC1 or HR1 branch was mutated. No original survey/respondent data, production source, CAN/ADP/SCI05 authority or original rule was read/executed/issued.
- No incumbent worktree was displaced. No process-level lease audit was possible from this shell; the absence of an existing worktree on this branch is the only negative collision check performed.

## FINDING

### 1. G17I — reviewer/author target is exact; engineering RED stands

Reviewer `agent/reviewer-sorok-20261019-g17i-material-historical-life-and-c9-consumer-independent-r1` at `156b84cc8481b65c4196b42574010eb7920d6f44`; document `WORKER_RETURNS/SOROK-20261019-G17I-MATERIAL-HISTORY-INDEPENDENT-R1/00_RETURN.md`, blob `01f2db8920b441ba1456fc269537072e0b5a19d7`, SHA-256 `b208dc74c0f108b487998f01340d1128cbed86e86f61402cea79270a7a7a3471`.

Author target: `agent/rabochii-sorok-20261019-g17-material-history-and-independent-lives-r1` at `90d0eb7925de54635559a879ee76fc1b97b9ff61`. The reviewer copied the exact source blobs into `target_candidate/`:

- `candidate/lab_sgi1/continuation.py` = reviewer `target_candidate/lab_sgi1/continuation.py`, blob `c9318dcf33d041a673cfae15aff8fc51712f53e7`.
- `c9_handoff_consumer.py` = reviewer `target_candidate/c9_handoff_consumer.py`, blob `47e59c12b79c04b05c18e73ad76078a29d0d7b3c`.

Reviewer test `tests/test_g17i_independent.py`, blob `83f17006b22271f17c87f4563608de08395d7a1c`; JUnit `evidence/g17i_independent.xml`, blob `0dec3fafc23d9c19d1575ae960472ffdb5f82060`. Execution is recorded as 11 PASS / 3 RED, 0 errors/skips. The three literal failures are:

- `test_forged_material_event_supplying_cash_must_be_refused` — accepted a forged material packet; receipt records cash `100058`, owner `FAKE_SOURCE_OWNER`, permission `FAKE`.
- `test_future_child_nested_alias_must_be_refused` — returned `COMMITTED` with `joint_material_opportunity.metadata.future_child_personality`.
- `test_c9_forged_material_event_must_be_refused` — `DID NOT RAISE C9Refusal`; record says `ACCEPTED`, cash `100055`.

Source basis is present, not merely asserted: `continue_person` checks participation/ref equality but adds `material_event['payment_per_actor']` without authenticating the material owner/permission (`continuation.py:11–29`); the pipeline guard inspects only top-level packet keys (`pipeline.py:88–109`); `receive_handoff` accepts the material packet after parent/ref checks and reports `ACCEPTED` (`c9_handoff_consumer.py:48–78`). **Code is present; semantics are not validated here. The reviewer's engineering RED is preserved.** M2/MP remain typed coverage HOLDs; C9 E1/RULE_A/RULE_T/E2 remain HOLD_UNISSUED.

**INTERPRETATION:** The exact G17I target relationship is resolved. It is not a commission or policy review; it is an executed test court with three retained REDs. The author's narrow 13-case positive does not close the alternate-interface failures.

**HQ ACTION:** Return G17 to its implementation owner for authenticated material-source binding, recursive/allowlist future-child partition, and C9 source authentication. Do not adopt G17. Preserve the three REDs and M2/MP/C9 holds.

**OWNER:** G17 implementation author; C9/C9P owners; ADP015/020/CAN008/CAN011 for M2/MP; incumbent Sorok HQ for intake.

### 2. OC5E — reviewer/author target is exact; 49 executed native REDs stand

Reviewer `agent/reviewer-sorok-r3-hq312-oc5e-execution-recovery-r1` at `67a4f1561cdad40192f00797d66b24fc4cd91589`; document `WORKER_RETURNS/SOROK-R3-HQ312-OC5E-EXECUTION-RECOVERY-R1/00_RETURN.md`, blob `9897d7bbbfaf8f6b0e05ab9d93c3eb9eff3b01ed`, SHA-256 `552fca27553af2121c11c43aa7c1f0abd65343d61fd225a2c31920a30c9c5b2a`.

Author target: `agent/rabochii-sorok-r3-hq310-oc4-custody-ten-red-repair-r1` at `0caaec590f6a8bf6744f22dc9c948c5fe233bc94`. The exact reviewed source is `WORKER_RETURNS/SOROK-R3-HQ310-OC4-CUSTODY-TEN-RED-REPAIR-R1/repro/custody_protocol.py`, blob `af2b7e943018077cb36808b5af1cd67704624bec`; author test `repro/test_oc4_repair_controls.py`, blob `c139a877aa4586ec5ab729d333c40037840721d4`.

Reviewer test `tests/test_oc5e_native_hostiles.py`, blob `9837579ebb5b2fbf3a41c967e584a166786e46b9`; JUnit `observations/oc5e_native_hostiles.xml`, blob `33efbc315cc424c377441b0f1f79ee31a5a185bc`. The evidence records 159 hostile cases: 110 PASS / 49 RED, zero errors/skips; the full court is 349 cases, 283 PASS / 66 RED. The 49 new REDs are distributed across A1 normalization-equivalent field alias (10), A2 confusable leak token (6), A3 malformed signature object (18), A4 non-enum role (1), A5 unhashable holder (3), A6 capsule identity field types (11). Representative exact cases: `test_normalization_equivalent_allowed_field_alias_must_be_refused[fullwidth-context]`, `test_confusable_leak_token_substitution_must_be_flagged[cyrillic-a]`, `test_malformed_signature_object_must_fail_typed[primary-object]`, `test_non_enum_role_string_must_fail_typed`, `test_unblind_unhashable_holder_must_fail_typed[list]`, `test_capsule_identity_field_types_must_be_validated[version-str]`.

The same court reproduces the ten historical original REDs and confirms all seven OC5 predictions natively. Verdict token: `REVIEW_REVISE__NATIVE_EXECUTION_RECOVERED__49_NEW_NATIVE_HOSTILE_REDS__7_OF_7_OC5_PREDICTIONS_CONFIRMED_NATIVELY__NO_AUTHOR_REPAIR__TEST_ONLY_ONLY__NO_ADOPTION`.

**Code is present; semantics are not validated here. The original RED is preserved.** C07 cross-process, real signer/institution, protected holdout, durable external journal and native custody remain NOT_REACHED/HOLD.

**INTERPRETATION:** This is an executed source-free test court, not a policy document. The author's 36 controls pass; they do not cover the 49 alternate-interface failures. The ten historical REDs are procedural/early-refusal/content-only-signature cases, not a weakening of the current law.

**HQ ACTION:** Return to OC4/OC5 implementation owner for typed malformed-signature handling, alias multiplicity/confusable scanning, unhashable-holder typing, capsule field-type validation, and holder-registry boundary treatment. Do not adopt as native custody.

**OWNER:** OC4/OC5 implementation owner; Sorok HQ intake; independent signer/custody owner for any native claim.

### 3. M04 — reviewer/author target is exact; 10 fresh REDs and 9 historical REDs stand

Reviewer `agent/reviewer-sorok-r3-hq314-m04-m03-independent-r1` at `3a993abcc0a9f6bd3a1bb003d298d293be199ea6`; document `WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/00_RETURN.md`, blob `5840b2f3f551903d61ce00654b8b964c0ea3a545`, SHA-256 `da0386ebb565477f3ff304f732e866eeddb3466794930250d068d176e6b900b2`.

Author target: `agent/rabochii-sorok-r3-hq313-m03-claim-selector-provenance-repair-r1` at `e1f7a74e51201b9614bcc578348b4e9db7be7bd3`. Exact reviewed candidate blobs are `candidate/cell.py` `3eb2d02aee8dc840e7cac1f99230d7c69adc2f58` and `candidate/claim_provenance.py` `2434bda6f4b00e6ea5881291f5422227e8045e74`; both match the reviewer's `candidate/` copies byte-for-byte.

Reviewer test `review/test_falsifiers.py`, blob `8add06c66b347e324443c1263771755f6898c7e2`; JUnit `evidence/fresh/junit.xml`, blob `2f54f3e3bc1a750fe87d9e697e324ffe019ae59e`. The fresh 51-case court records 41 PASS / 10 FAIL. The ten failures are:

- 4 × `test_cross_cell_none_owner_cannot_erase_first_committed_belief[NONE|CERTAIN|UNCERTAIN|UNAVAILABLE]`.
- 4 × `test_revoked_or_withdrawn_state_cannot_be_resurrected_by_partial_rollback[{False,True}-{SUPERSEDE_EXACT_RECORD,WITHDRAW}]`.
- 2 × `test_fully_rehashed_transition_requires_actual_prestate_ancestry[{False,True}]`.

The unchanged published expectation reproduces 587/587 PASS; the nine separate historical CAN3 cases remain nine literal FAILs. Cited source is present: `claim_provenance.py:123–126` checks canonical state equality only, `:200–226` verifies internal IDs but not actual pre-state ancestry, `:286–291` treats missing snapshot/active/transition/permission as lawful NONE, and `:339–349` verifies `last_transition_ref` against any matching transition, not terminal applicable descent. Verdict: `REVIEW_REVISE`.

**Code is present; semantics are not validated here. The 10 fresh REDs and 9 historical REDs are preserved.** Real operative owner authority, serial ADP016→ADP017 mediation and human calibration remain HOLD.

**INTERPRETATION:** This is an executed, preregistered reviewer court. It is not a commission-only document. The M03 selector repairs (unknown/after-response) are independently reproduced, but the checkpoint/restore provenance boundary remains unsound.

**HQ ACTION:** Return to M03/M04 implementation owner for authoritative first-state/transition provenance, terminal applicable transition validation and genuine absence handling. Preserve valid ADD/supersession/withdrawal/NONE/replay. Do not adopt M04 or elevate to native science.

**OWNER:** M03/M04 implementation owner; CAN008 response owner; ADP016 memory owner; ADP017 epistemic owner; Sorok HQ intake.

### 4. Outside-294 estate — ranked, partly read, explicitly incomplete

Canonical census `315251451a6d112fb312a6a2e80b096d345c5de6` records 2,831 branches / 2,743 distinct tips. Current `ls-remote` observed 2,851 heads (+20 names since census). RC1/HR1 record 294 literal, 168 heuristic, 2,369 unselected; 377 unselected tips have significant changed-path hits; 3 were detailed by RC1; 2,366 unselected rows remain without detailed source read.

All 377 selected tips are currently unchanged from their RC1 pinned SHAs. This audit diff/consumer-screened 19 of the 377, including the three RC1 material cuts and 16 additional high-impact tips. The remaining 358 of 377 were metadata-ranked but not deep-read; the 2,366 baseline remainder is not semantically cleared.

High-impact observations:

- `codex/c12-perception-fork-repair-r1` @ `68b058656254234f0af02df2a592aa6f8c6a8bd2`: C12 fork integrity changes `vendor/j/candidate/vendor/bp4/bp4/store.py` blob `c94cd131…` and `r26e/c12_integrity.py` blob `402c2b02…`; first consumer is `tests/test_c12_fork_integrity.py` blob `78626103…`. No equivalent path exists at PRE-MAIN `299f41e9`; candidate-only.
- `agent/rabochii-pyat-r3-hq284-l01…` @ `c6dba4b7…`: selected-world runtime adds `pre553_selected_world_progressive_contract.py` blob `e9caea54…` and consumer `r3_s02_seam_witness.py` blob `408c4700…`; absent from PRE-MAIN; tests are the only first consumer.
- `integration/prev3-w5-qualified-fanin-r1` @ `579ed550…`: `f07_second_canary_prev3_admission.py` `06c31220…` and `objective_consumer_bounded_evidence.py` `f30fca20…` are byte-identical to PRE-MAIN. Branch is not an ancestor, so content landed by another path; non-test consumer of F07 was not found.
- `agent/rabochii-warplan-gt12-c-ff-conditional-support-r1` @ `d30ca3b6…`: `field_forge_conditional_support.py` `a70decb2…` is merged (branch ancestor of PRE-MAIN) and imported by `gt12_c_to_d_relation_bridge.py` and tests.
- `agent/rabochii-wsc002d-gt0-prev3-r1` @ `a3d0609e…`: branch `wsc_gt0_prev3_bridge.py` `0f3dfcc5…` differs from PRE-MAIN `8f237bd5…`; PRE-MAIN first consumer `wsc_gt0_end_to_end.py` calls `run_gt0_prev3`. Drift is real; no adoption inferred.
- `agent/opencode-pyat-r95-r06-world-consumer-integration-r1` @ `b2cfe93cee85`: R95 candidate `pre553_universal_world_binding.py` `44ac11c9…`, first consumer test `7095820c…`; absent from PRE-MAIN. CONTEXT structural authority remains HELD in the author return.
- PFF G1/G2 doc at `f4a61361…`, blob `329d9f62…`, is a semantic-gap reconciliation, no code/first consumer. Typed-ingress constitution at `78e6001f…`, blob `f07b113b…`, is candidate prose only, no code/consumer. Both are source documents, not law issuance.
- HQ280 D02Y and W11 M05 are HOLD/document or candidate-only; not production consumers.

**INTERPRETATION:** The outside estate is not empty, but most of the 377 are documentation/data returns. The material code risk clusters in C12 fork/custody, selected-world runtime, GT12/M3 landed seams, WSC bridge drift and R95 world binding. None of the candidate-only code is in PRE-MAIN. No current first consumer proves native/world/science authority.

**HQ ACTION:** Prioritize owner review in this order: C12 fork integrity (reader/writer safety), R95 world binding (first-consumer boundary), HQ284 selected-world runtime, W11/HQ292 typed seam candidates, then WSC bridge drift. Do not batch-adopt. Require the owner to state whether each candidate is superseded, merged by another path, or abandoned.

**OWNER:** C12/BP4 owner; P41/R05/R06 owner; PRE-V3 seam owners; Field Forge/GT12 owner; WSC owner; Pyat world owner; Sorok HQ intake.

## DONE

- Verified exact local objects and reviewer/author cuts for G17I, OC5E and M04.
- Resolved each target to source blob, reviewer test blob, execution evidence and original RED/HOLD.
- Distinguished executed tests from commissions/policy documents.
- Ranked the 377 significant outside-294 tips; inspected 19 at diff/consumer level; preserved the 358/2,366 remainder.
- Compared selected source paths with PRE-MAIN and recorded landed, drifted, absent and candidate-only states.
- No PRE-MAIN/adoption mutation, no native/scientific issuance, no source execution by this worker.

## REMAINING

- 358 of the 377 significant tips were not deep-read; their ancestry and first consumers remain UNKNOWN.
- The 2,366 unselected rows without detailed source read remain semantically incomplete.
- No original survey/respondent source was opened.
- HR1 `02` records a Sorok08 R1/R2 source-custody anomaly (`1715511b…` / `a574db23…` / `857dfed1…`); this reconciliation did not re-adjudicate it.
- Reviewer independence is documentary only; no reviewer re-execution by this worker.
- The exact final remote SHA can only be reported after the ordinary push (self-reference excluded).

## CRITICAL BLOCKERS

- G17 forged-material and nested-future-child paths remain accepted at source.
- OC5E's 49 malformed/alias/capsule-type REDs remain open.
- M04's 10 checkpoint/provenance REDs remain open.
- WSC PRE-MAIN bridge drift is unresolved.
- C12/R95/HQ284 candidates have no PRE-MAIN consumer or owner adoption.
- No native B/world, Rule A/T, C9/C12 reader, or A0–A5 source authority is established.

## LARGEST PRODUCTIVE MOVE

Have the three original component owners repair the exact retained REDs, then commission one fresh reviewer per repaired cut against the same assertions. In parallel, have the C12/BP4 and R95/P41 owners decide whether their candidates are superseded, merged elsewhere, or still proposed. Do not start a new 377-branch semantic sweep before those owner dispositions.

## FLIGHT

`F3_ESTATE = REVIEWER_TARGETS_RESOLVED_ENGINEERING_RED + OUTSIDE_294_RANKED_PARTIAL_READ + AUTHORITY_SCIENCE_HOLD`.

## DELTA

- `+` exact reviewer→author→source→test→RED/HOLD chains for G17I/OC5E/M04.
- `+` explicit 2,831/2,845/2,851 census drift and 377 unchanged tip check.
- `+` 19-tip diff/consumer inspection with 358 remaining.
- `+` PRE-MAIN equivalence/drift for selected code paths.
- `-` no source or semantic acceptance.
- `-` no 377/2,366 completeness claim.
- `-` no adoption, rule issuance or native person claim.

## Acceptance grades

- **ENGINEERING:** `RED_OR_HOLD` — three targets resolved; G17I 3 RED, OC5E 49 native REDs, M04 10 fresh REDs + 9 historical REDs; outside estate partial.
- **SCIENCE:** `HOLD` — no automatic source-to-law elevation; no native B/world, Rule A/T, C9/C12 reader or A0–A5 human result.
- **AUTHORITY:** `HOLD` — original reviewer scopes and owner jurisdiction preserved; no PRE-MAIN adoption; no self-acceptance.

## Reviewer needed

A separate source-qualified reviewer must audit this return, the three target chains and the 19-tip sample. This worker cannot review its own work. Incumbent Sorok/PRE-MAIN HQ owns routing and any adoption decision.

## First real consumer

- G17I/OC5E/M04: first real consumer is the original component owner's repaired source plus a new independent reviewer; no product consumer is proved here.
- Outside estate: first real consumer is branch-local tests for C12/R95/HQ284; GT12/M3 consumers are PRE-MAIN source; WSC PRE-MAIN consumer exists but the branch blob has drifted; no native/product consumer is proved.

## Outstanding receiver/owner

Incumbent Sorok/PRE-MAIN HQ (intake and routing), G17 implementation owner, OC4/OC5 implementation owner, M03/M04 implementation owner, C12/BP4 owner, P41/R05/R06 owner, PRE-V3/Field Forge/WSC owners, and a separate independent reviewer.
