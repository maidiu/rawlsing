# F2 → future B3 integrated observables v1 (FROZEN pre-B3)

**A test oracle is not a simulation.** The 42 independent cases are synthetic and fixed at F2 source creation. `reference_oracle.evaluate(case)` computes only what evidence and authority allow, never which psychological state *must* ensue. The future B3 integrator MUST NOT implement or call the F2 reference oracle as its causal generator and MUST NOT choose output using the `case['expected']` field. B3 input may ignore `group`, `expected`, `actor.history_label` for causal meanings; those are audit labels, never rules. F2 tests likewise do not import B2/M1.

## Required adapter signature

```python
# Separate, later, independently authorized B3 worker only
# run_case must actually exercise corrected event ingress + M1/CAN008-compatible
# source-free integration; it must not invoke F2 reference_oracle.evaluate.
def run_case(case: dict) -> dict:
    # Native implementation may return a typed NOT_APPLICABLE_TO_THIS_LAB.
    ...
```

Return **actual collected observables** (not expectation names): `case_id`, `status`, `code`, `original_event_hash`, `event_world_hash_after`, `exact_replay`, `new_event_count`, `verified_evidence_refs`, `material_actor_activity`, `accessible_readset`, `independent_offer_refs`, `admissible_routes`, `history_material_hash`, `owner_effect_committed`, `independent_owner_receipt` (only if true), `selected_affect` (only if actor rule actually evidenced), `separate_actor_response_witness` (only if actual), `asserted_culprit_group` (must be null), `issued_production_authority` (must be false). A B3-specific nested 
`admission`, `CAN008_response`, `CAN011_transition`, `ADP016_memory`, `ADP017_access`, `actor_actions`, `world_effects`, `immutable_history`, `decision_receipts` should carry exact identities/rule versions and owner signatures/receipts where lawful. A test-only owner receipt must be labeled **TEST_ONLY**.

`status` / `code` in adapter view are F2 mapped input-custody decisions, NOT native CAN008 state. A native integrated engine may cause a real test-only effect (so `no_mutation` is not asserted for eligible cases); negative/DEFER cases must prove no event/target mutation. Do **not** count an N/A as a PASS. Explicitly report `NOT_APPLICABLE_TO_THIS_LAB` and the exact missing owner: ADP019, ADP015, CAN008 R2, CAN011, ADP016/017, or competence. `reference_oracle.validate_native_receipt` is a partial observable audit; native B3 acceptance additionally requires actual imported module execution, transaction/SQL cold replay, event-ID+payload uniqueness and independent 3rd-party authority evidence.

## Causal/metamorphic red lines

1. Hold world, witnessed caregiver/child actions, access and later events fixed; relabel only `recognized_plan`/`imposed_plan`. **Causal source evaluation and any substantive psychological inference may not change purely because the analyst changes a cosmetic label.** An actual separately owned actor appraisal witness could allow a change, not this label alone.
2. Hold label fixed; change actual independently witnessed enacted caregiver-child task or caregiver capacity to help. The recognized *material* possibility/evidence lineage must change. Do **not** require a specific affect or morally preferred trajectory.
3. Attribution of peer claim is not thief fact or child belief. Hearing is distinct from speech and from propositional assent. Test F2-007/008/009/010.
4. Accepted proposition and affective dismissal may coexist; public mimicry and privately rejected peer claim may coexist; older practical habit and no explicit recall may coexist. Do not collapse channels to scalar or force narrative coherence.
5. Later independent person can pursue another project and refuse. Their refusal closes contact opportunity; does not “heal” or universally harden child. Permit F2-013/014/016 and no-change F2-015/016/041.
6. Original theft event hash always immutable through later generated reinterpretation; only separately owner-issued new lineage versions can be appended, with exact causal parent/time. Never retcon t0.
7. C07 capability only with matched task, actor, scope, time and independent positive/negative observation. UNKNOWN/expired is not ABSENT; contradictory qualified observation -> DEFER/CONFLICT. No sex/age/class/sect/race → psyche shortcuts.
8. Exact `(issuer, actor/event-id, event identity, content hash)` idempotence. Same ID different content -> DENIED before occurrence rows/mutation, not response-only rollback. Test F2-027/028.
9. No P1 model selection → event admission cast; LLM text cannot issue producer grant or durable delta; CAN008 cannot grant CAN011 rights; private motive cannot be accessed automatically; child future never changes preconception parent.
10. No fabricated or forced positive human outcome, no universal individual probability. Stochastic draw only under separately accepted ADP020 semantic and seed/candidate provenance; F2 uses **zero draws**.

## Integration/replay grading

`python -m pytest -q test_heldout.py` tests **only frozen F2 reference**. `python mutation_audit.py` kills known bad fake response families; it does not execute B3. A future B3 runner must execute *every frozen case* against real staged imports and report `PASS/RED/NOT_APPLICABLE` per ID, plus equivalent metamorphic contrasts on native receipts. Treat sourcefree F2 reference successes as preflight, not integration success. F1 original 17 native REDs remain open regardless of F2 grade.
