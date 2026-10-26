# Differences from RA-D

**Bottom line:** no material source-identity, test-count, causal-trace or S52-RED error was found. The corrections below are scope/wording corrections; none overturns the engineering acceptance. The scientific and authority holds remain.

## 1. S52 trace declares the wrong root hash — formal REVISE reason

**RA-D artifact:** `ACTUAL_CAUSAL_TRACE.md` §1 states:

> Root: `84687e6f…` (S44 sampled antecedent root; current B state is the sampled root state, not the G18 replay final state)

**Actual:** the S52 probe root is `3bcb21fc22df3255269382ad249f706dd6dd5378cb886af26542991ff516a4f7`:

- RA-D’s own `TEST_SOURCE_AND_LOGS/causal_probe_result.json` root hash is `3bcb21fc…`.
- The reviewer’s independent S52 probe root hash is `3bcb21fc…`.
- RA-D’s S44 entrypoint log root hash is `84687e6f34116693c00243b4c7e7e76fa0f24146b992b372d8920cab153cb930`.

The S44 entrypoint uses `default_bundle(root_seed="11"*32)`; the S52 probe uses `root_bundle("01"*32)`. The trace cites the S44 root for the S52 session.

**Effect:** formal `REVISE` at the proof-path/documentation grain. The material chain, S52 RED, 131 tests and source identities are unaffected. Correct the trace to `3bcb21fc…`; no re-execution is required.

## 2. “Same-person” continuity is narrower than the summary wording

**RA-D disclosure:** `ACTUAL_CAUSAL_TRACE.md` §1 and `00_RETURN.md` §3 disclose that the current B state is the S44 sampled root state (`root 84687e6f…`) and **not** the G18 replay-final state.

**Correction:** the chain is same **actor ID / root / branch** plus G18 object identity, not uninterrupted developmental state carry-forward from the G18 replay final state. The historical STRIVING object is real inside G18; the current material state is a separately generated/sampled root state. `00_REVIEW.md` and `REVIEW_CLAIM_MATRIX.json` therefore grade the chain as `ACCEPT_AT_SOURCEFREE_MATERIAL_GRAIN` with this scope, not as continuous personal history.

**Effect:** narrows the interpretation; does not invalidate the material object-recovery and current-material-eligibility evidence.

## 3. “First missing composer” overstates the software absence if read as a blank sheet

**RA-D wording:** “The first software missing piece is the composer/admission that emits that operation (CAN011 CREATE/TRANSFORM/NO_CHANGE) and the actor-state consumer that admits it” (`ACTUAL_CAUSAL_TRACE.md` §7).

**Correction:** the recovered V3 machine already contains a real transactional pressure-flow composer (`run_pressure_flow_cycle`, `_simulate_domain_routes_transactionally`, `_commit_route_state`, `_update_memory`), and the S44/S45 path already reaches a **test-only** M35 CAN008/CAN011 receiving/commit port with a `NO_CHANGE/NO_PROPOSAL` target. What is missing is a **current event-scoped binding/adapter**, a **current actor state**, and the **concrete issued CAN008/CAN011 rules**, not every composer. The correct wording is “missing current event-scoped composer/admission and unissued concrete owner rules.”

**Effect:** this is a material correction to the V3 reuse judgment, not to the S52 material evidence. It prevents an unnecessary blank-sheet re-specification. See `V3_RECOVER_ADAPT_BOUNDARY.md`.

## 4. The 131-test scope is narrower than “sourcefree engineering” may suggest

**Correction:** five of the 131 are S50 historical V3 fixture tests (`test_source_identities_all_31_exact`, roundtrip/pressure-flow, actual-root hold, cold reopen, fail-closed). They are sourcefree and useful, but they are not current-person integration tests. None of the 131 is an official Astra K case. The 131 count should not be read as K coverage or as proof that the current S52 actor executes V3 psychology.

## 5. `candidate.recruited=true` is not actor recruitment or choice

**Correction:** in `s52/session.py`, `recruited` is set when the current relevance is `RELEVANCE_WARRANTED/FACILITATES` and the candidate is conditional. It is a candidate-level relevance-recruitment flag. The S39 receipt still has `selected_option=""` and `selection_status=OPEN_CHOICE_SET`. It must not be reported as an actor-selected or motivated action.

## 6. The controlled performer does not require the S39 selected option

**RA-D says:** the controlled performer is a test port, not an actor-selected action (`ACTUAL_CAUSAL_TRACE.md` §5; `00_RETURN.md` §5).

**Strengthening:** the source confirms it. `s52/performer.py` checks canonical candidate, generation repertoire and candidate feasibility, but does **not** require `selection_status=UNIQUE_SELECTED` or `selected_option=PAID_PARTICIPATION`. A controlled call can perform while the S39 choice remains open. This is stronger evidence that the paid performance is not an actor choice, and it should be preserved in any downstream summary.

## 7. S50 fixture precision: no striving objects, all-hopeful baseline

**RA-D says:** S50 executes a historical V3 fixture; actual root is held; `fixture_only:true`; `actual_person_commit:false`.

**Precision:** the fixture entrypoint reports `striving_count=0` and an expectation baseline that is `hopeful` on every axis. The V3 `striving_objects` field is therefore empty in the executed fixture. The G18 `STRIVING` event is a different object and is not automatically the V3 `StrivingObject`. The recovered V3 machine is executable historically, but this particular fixture does not demonstrate a populated V3 striving-object computation, and its initialization is legacy policy.

**Effect:** supports RA-D's “fixture-only” scope; prevents reading the V3 fixture as a current-person striving computation.

## 8. S52 verifier RED is in an unaccepted component and is not the development path

**Confirmation, not correction:** the defect is real and reproduced warm and cold. The `S52Session.verify()` postcondition check is skipped when a later canonical episode exists (`s52/session.py:299–311`). The S52 component is unaccepted; the defect is not repaired, adopted or used as psychological evidence. It should be fixed separately by the S52 owner.

## 9. S44/S45/S47 claims confirmed

The independent entrypoints reproduce RA-D's key values: S44 first event `REQUEST_TOOL` with target `NO_CHANGE`; S45 `say=HELP_INVITE`, `do_help=HELP_ACCEPT`, `attend=NO_CHANGE`; S47 actual `objective_material_eligible=false`, target `NO_CHANGE`, provider calls 0. No correction.

## 10. No source-identity correction

The 183/183 `.py` check, the five ancestor divergences, the S50 31/31 identities, the external G18/JOIN-E/language hashes and the imported-module origins all reproduce. The reviewed S52 cut is a modified superset; it must not be described as the accepted ancestor cut. RA-D already says this; the review confirms it independently.

## 11. Wording recommended for the incumbent HQ adoption note

Use:

> Engineering evidence is accepted at the S52 sourcefree material grain: exact source identity, 131 focused tests, G18 object identity, current material eligibility, conditional option, controlled material mutation and later material consumer. The S52 verifier RED is confirmed in an unaccepted component. No actor-owned current psychological formation, selected action or durable CAN011 transition is proved. The recovered V3 machine is an executable historical reservoir and a targeted event-scoped adaptation seam, not a blank sheet; concrete CAN008/CAN011 issuance remains with the competent scientific owners. No native grant.

Do not use:

- “the actor chose the paid action”;
- “historical striving drives current relevance”;
- “the V3 machine already runs the current person”;
- “K8 passed”;
- “the batch recursion is implemented”;
- “the S52 performer is an independent counterpart.”

**Verdict on differences:** `REVISE` is required for one proof-path correction (the S52 trace root hash). The rest are scope/wording and V3 reuse-boundary clarifications; the engineering evidence otherwise reproduces. Scientific and authority remain `HOLD`.
