# R0-04 — V557/V558 Runtime Boundary and V3/V2 Consumer Requirements

## Identity

- **Worker ID:** R0-04
- **Branch:** `agent/vozhd-dva-r0-04-runtime-contract`
- **Target PR base:** `agent/vozhd-dva-wave0-integration`
- **Prong:** V557/V558 boundary completion and downstream runtime consumer contract

## Mission

Work backward from Rawlsing's intended runtime destination to determine the minimum information V557/V558 must expose, preserve, and govern. Audit the current renderer/runtime-boundary code and existing V3-consumer tests, then define a bounded V558→V3 and V3→V2 information contract for the implementation wave.

The current repository does **not** contain a canonical finished V3/V2 implementation to copy. Do not invent those systems wholesale. Use the frozen target responsibilities below and current boundary tests/contracts to specify what the V5 pipeline must provide.

Wave 0 is reconnaissance/specification. No broad runtime implementation is authorized.

## System position

`V556 pressure-flow / attractor structural topology → V557 controlled renderer/runtime representation → V558 governed runtime-consumption boundary → V3 temporal/developmental actor engine → V2 phenomenology/conversation`

The central question is: **what must cross V558 so V3 can build an actor without reaching back into raw survey/DDM internals, and what must remain prohibited?**

## Canonical read set — read in order

1. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/README.md`
2. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/CONSTRAINTS_PRIORITIES.md`
3. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/CAPABILITY_MATRIX.md`
4. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/rabochii/WAVE_0/README.md`
5. `data/ddm_build_copy/ddm_v557_renderer_contract.py`
6. `data/ddm_build_copy/compile_v557_thin_layer.py`
7. `data/ddm_build_copy/ddm_v558_runtime_input_gate.py`
8. `data/ddm_build_copy/ddm_v558_runtime_graft_readiness.py`
9. `data/ddm_build_copy/ddm_v558_plus_governance.py`
10. `data/ddm_build_copy/compile_v558_runtime_input_gate.py`
11. `data/ddm_build_copy/compile_v558_numeric_runtime_graft_readiness.py`
12. `data/ddm_build_copy/compile_v558_plus_governance.py`
13. `data/ddm_build_copy/ddm_pipeline_boundary_contract.py`
14. `data/ddm_build_copy/ddm_pipeline_boundary_consumer.py`
15. `data/ddm_build_copy/ddm_pipeline_final_contracts.py`
16. `data/ddm_build_copy/ddm_v5_app_handoff.py`
17. `data/ddm_build_copy/compile_v5_final_runtime_bundle.py`
18. `data/ddm_build_copy/compile_v5_app_handoff_bundle.py`
19. `data/ddm_build_copy/test_w03_v551j_v3_consumer.py`
20. `data/ddm_build_copy/test_w03_v551j_v3_fail_closed.py`
21. `data/ddm_build_copy/tests/test_w05_v551_v3_consumer.py`
22. `data/ddm_build_copy/tests/test_w05_pipeline_boundary_contract.py`
23. `data/ddm_build_copy/tests/test_w05_final_cross_stage.py`

## Frozen downstream target responsibilities

These are context for consumer requirements, not permission to implement them here.

### V3 — causal/temporal runtime

V3 is intended to own actor-specific temporal metabolism and causally attributable state change. It must eventually be able to evolve a generated actor through:

- historically situated structural pressures;
- nine-strata relations and orientation-to-strata;
- carrier/institutional/household mediation;
- position/capacity/reproduction constraints;
- expectations, frameworks, buffers, cracks, alienation;
- pressure-flow routing through lived events/history;
- Enneagram-like attractor formation/reinforcement/destabilization;
- explicit event/state history and provenance of causal mutations.

V3 should not need raw DDM/survey evidence or use V2 prose as causal authority.

### Genealogy/household runtime

Runtime must later support recursive person generation: Parent 1 develops; encounter/partner-space emerges from actual structural and life-course conditions; Parent 2 is generated as an independently coherent actor constrained by plausible encounter; relationship/household history develops; child emerges from intersecting histories and then enters V3.

### V2 — phenomenological/rendering runtime

V2 is intended to express what the actor notices, remembers, calls things, hides, misrecognizes, symbolizes, wants, and can/cannot say; public/private/intimate registers; voice; self-narration; conversation. It must not freely mutate causal state or reinterpret upstream evidence as autobiography.

## Frozen external facts

- V557/V558 must preserve source/generated/rendered separation.
- Raw survey/DDM material must not enter persona prompts as direct autobiographical speech.
- Generated runtime facts may become canonical facts of a simulation while remaining epistemically generated, not source-attested.
- V2 expression is downstream of V3 state/history and does not become source authority.
- User interaction that affects the actor should become an explicit runtime event mediated through V3, not uncontrolled V2 write-back.
- Enneagram-like attractor formation is part of the design; V558 must preserve enough V556 semantics for V3 to realize it.

## Questions to answer

1. What does current V557 actually preserve from V556, and what does it discard or reduce to blocker prose?
2. What does current V558 normalize/expose today?
3. Which fields/states must V558 expose for V3 to operate without raw upstream access?
4. Which provenance/authority/uncertainty metadata must accompany runtime-consumable priors?
5. Should V558 expose a one-shot bundle, queryable prior slices, or both? Answer only at the information/interface-requirement level; do not build a service.
6. What must be forbidden from crossing V558?
7. What minimum V3 state/event inputs are necessary to test V558 adequacy?
8. What minimum V3→V2 state/history interface is needed to keep V2 phenomenological rather than causal?
9. Which existing boundary tests remain useful, and which encode obsolete assumptions?

## Authorized write domain

Wave 0 production semantics are read-only.

Allowed writes:

- worker `RESULT.md` / `RESULT.json`;
- optional diagnostic/reference-consumer tests that do not change runtime behavior and are clearly isolated.

Report paths:

- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/rabochii/WAVE_0/R0_04_RUNTIME_CONTRACT/RESULT.md`
- `.../R0_04_RUNTIME_CONTRACT/RESULT.json`

## Prohibited scope

- No V3 or V2 full implementation.
- No genealogy engine implementation.
- No broad V557/V558 production rewrite.
- No prompt/dialogue/persona generation.
- No relaxation of source-to-generation separation to make runtime easier.

## Required work

1. Trace current V556-facing information through V557 into V558.
2. Inventory current runtime-normalized fields, blockers, and permissions.
3. Identify information starvation relative to the frozen V3 responsibilities.
4. Propose the **minimum V558 runtime information contract** with required types/states/provenance.
5. Propose the **minimum V3 consumer reference assertions** that can validate that contract before V3 is rebuilt.
6. Propose the **minimum V3→V2 boundary requirements** needed to protect causal jurisdiction.
7. Identify obsolete or misleading current boundary assumptions/tests.
8. Return cross-hooks required from V556/V557 or future V3 work.

## Acceptance evidence

`RESULT.md` must include:

- current V557→V558 trace;
- V558 information-preservation gap table;
- proposed V558→V3 contract;
- explicit forbidden-crossing list;
- proposed V3 reference-consumer assertions;
- proposed V3→V2 boundary;
- no speculative full runtime architecture beyond what these contracts require.

## Return format

Use `rabochii/WAVE_0/REPORT_FORMAT.json` exactly for `RESULT.json`.

Open a draft PR against `agent/vozhd-dva-wave0-integration`. Do not merge it.
