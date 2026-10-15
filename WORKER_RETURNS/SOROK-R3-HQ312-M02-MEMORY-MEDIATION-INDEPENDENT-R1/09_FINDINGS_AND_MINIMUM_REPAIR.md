# Blocking findings and minimum next author edge

Both observations are reproduced against unchanged M01 source and confirmed in a separate fresh interpreter. The appropriate final token is `REVIEW_REVISE`. They share an outer selected-claim provenance gap; they are not two independently counted psychological mechanisms or evidence of a production endpoint exploit.

## R1 — unresolved checkpoint claim selector becomes absence

Source: M01 `repro/cell.py` lines 52–56 and 112–124, exact commit `02187a14e75ff30dd953d3c7185d689b80e62304`.

`checkpoint()` includes `claim_id` separately from the owner state, and `restore()` accepts that outer field without checking it against the first event or the verified canonical claim. `read_owner()` looks up `state_sets[self.claim_id]`; if the selected snapshot is absent it leaves Ye at AMPLIFY. It never distinguishes a legitimate existing canonical claim with no stance from an unresolved/foreign selected claim.

In `test_checkpoint_claim_selector_cannot_downgrade_existing_belief_to_absence`, the actual owner store contains an accessible BELIEF and its current permission. The complete owner state and hash, both event identities/times and actual history remain unchanged. Restoring a checkpoint with an unknown selected claim is accepted; the later graph changes Ye from REROUTE to AMPLIFY. The existing BELIEF was not withdrawn by any owner transition. Expected refusal does not occur.

Evidence: `evidence/independent/observations/checkpoint_claim_selector_probe.json`, raw independent/corroboration JUnit, and `evidence/independent/actual_function_calls.json`.

## R2 — future epistemic state can condition an earlier response

Source: M01 `repro/cell.py` lines 88–124 and 127–140. The later read checks that its time is after E1, but does not validate the selected claim/active effect's scope, source event and effective time against E1/E2.

The test actually admits a new finite-rule feedback event at 1999-01-20, binds a canonical claim through the native owner, and applies its BELIEF through the native state transition. Selecting that claim allows the earlier 1998-11-20 response to emit REROUTE. The store, claim hashes, event admission and permission are genuine fixture objects; their valid formation does not authorize this backward-time use.

`evidence/selector_isolation.json` supplies a stronger paired follow-up: both cells have identical complete owner state/hash, history, event/time and source code. Only the outer selected claim differs. The original E1 claim gives AMPLIFY; selecting the future claim gives REROUTE. No response function is replaced, no desired-response argument is passed, and no result is fabricated. This is an adversarial selector test, not a lawful positive treatment arm.

Evidence: `evidence/independent/observations/future_claim_provenance_probe.json`, `evidence/selector_isolation.json`, fresh-process corroboration and actual function traces.

## Scope and smallest repair

The public later-call signature does not accept arbitrary mediator labels or refs, which is a useful boundary. The exposed Cell checkpoint/restore and mutable selection metadata are weaker than the owner-state hash. This review does not assume arbitrary Python code/OS compromise, and does not turn trusted internal rollback into a claimed public production serializer. The precise claim is that the candidate's own outer Cell selection is not authenticated or causally scoped when read; the commission explicitly required hostile claim/time/state-provenance checks.

A separate author should bind the selected canonical claim to the first committed transaction and its actor/event/time/rule scope, preserve that binding across checkpoint/restore, and validate it before treating a missing stance as lawful absence. Check selected transition/source effective times against the response cut. Invalid selection or missing provenance must refuse/defer with rollback. Preserve the valid NONE arm: an existing correctly bound canonical claim with no applied stance may still yield AMPLIFY. Do not broadly deny absence or edit the original tests to manufacture a pass.

Re-execute the original 413, the exact frozen 36-arm matrix, these literal new falsifiers and all nine historical REDs. Competent source/rule/conditioning/destination owners, production registry issuance and independent acceptance remain separate. This reviewer performed no author repair, canonical change or adoption.
