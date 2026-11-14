# G1A-FUNC-022 — V558+ governance, V557→V558 schema mismatch, and modern M4 conditional use

Old source `25830fe7462bb9e29bc4087e6ae14f3f84cec377`: V557 renderer blob `7ad1dba128537e6b769617cec7de8220f4139e72`, V558 input gate `bb160ca3fd05bf9b404090f379be06d192cb918e`, V558+ governance `99bb369b5463a9b7a68c0b1f3d84368337d1d51b`, CLI compiler `b092270f223d20d09b98103f26db46fd2a7b8cc5`. Modern M4 `m4_v557_v558_publication_repository.py` blob `8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360` at `6a5c12f04323d74001f9632063ec907f4fc4468e`. Inherited G1A-FUNC-022, no new T.

## Historical input and shape flaw

Completion-grade V557 produces a packet `payload.renderer_input_contract`, `payload.runtime_wiring_contract`, `payload.source_to_generation_separation_ledger` and render blockers; `ready_for_v558=True` and `ready_for_runtime_consumption=False`. But the V558 normalizer requires **also** nonempty `payload.future_consumer_notes` and `payload.app_wiring_boundaries` to set `v558_handoff_requirements_present=True` (L287–315). Those keys are not in completion-grade V557 packet at L195–263. This is a source-verified producer/consumer shape mismatch, confirmed by Dva R0-04 §1.6 L114–118. The normalizer still generates statuses, but the handoff requirement cannot be declared complete merely because the V557 packet exists. R3:EV:022:V557/:V558_GATE/:DVA.

## Old V558+ actual produced capital

`build_v558_plus_governance` reads V558/graft readiness and governance state, builds runtime gate, generation-permission ledger, evaluator contracts/results, V3 adapter contracts, memory policy/ledger, narrative policy/ledger and readiness reports. `_generation_permission_rows` L335–360 allows only bounded constraint-preserving review; style/dialogue/memory generation are blocked. **Every branch** of `generated_unit_index` L956–964 receives `rows=[]`, `row_count=0`, `generated_unit_count=0`. This is *governance knowledge*, not a model of lived actor memory. Historical compiler L33–44 actually calls V558+ builder; native run and V3 first reader are unproved. R3:EV:022:OLD_GOV/:COMPILER.

## Illustration (not an executed run)

Suppose V557 payload has `renderer_input_contract={...}`, `runtime_wiring_contract=[...]`, `source_to_generation_separation_ledger=[...]`, but no `future_consumer_notes` or `app_wiring_boundaries`. Under that partial shape, V558's `handoff_requirements_present=all([...])` is false even if the three present inputs are nonempty. A V558+ governance return can still contain a memory policy row saying write forbidden and a generated index with zero entries. A policy row does not become actor recollection. This illustrates the code contract and not an actual production sample.

## Modern M4 really does more than mere sourcefree context

Protected M4 defines permission atoms `REVIEW`, `CONTEXT`, `ACTIVE_CAUSAL` and state `ALLOW_ACTIVE_CAUSAL_CONTEXT` (L53–109). `StructuralObject` keeps producer family, typed state, source stage, allowed uses and required/negative dependency refs. `govern_v557` enforces `allowed_uses ⊆ producer_allowed_uses ∩ state_ceiling`; `build_v558_repository_bundle` checks content-addressed index/role/dependency closure; `resolve_v558` has an actual conditional positive branch `SELECTED` only where each dependency permits requested use, otherwise named `PERMISSION_DENIED`, `UNRESOLVED_EXACT_KEY`, `INTEGRITY_FAILURE` or `AUDIT_ONLY_NOT_CONTEXT`. These are **implemented code paths**, not source-native execution or authority grant, and they do *not* produce person memories. See R3:EV:022:M4_*.

## Disposition / future decision

Historical generation policy and zero generated units are retained as valuable negative knowledge; old V557/V558 contract mismatch remains a separate loss. Modern structural dependency and active-causal conditional guards have different, potentially stronger operation, without proven original source issuer or actor first reader. No supersession/retirement. Exact future decision: a competent structural/source owner must qualify a real V556 input and authority/use ceiling and trace an actual selected M4→N9/Sorok consumer; separately decide historical missing V557 notes contract. No engineering in this review.
