# R0-02 — V555 Mediation Semantics and Downstream Requirements

## Identity

- **Worker ID:** R0-02
- **Branch:** `agent/vozhd-dva-r0-02-v555`
- **Target PR base:** `agent/vozhd-dva-wave0-integration`
- **Prong:** V555 mediation semantics

## Mission

Audit the current V554→V555→V556 chain and define the smallest semantically adequate V555 completion model that later pressure-flow, household/genealogy, and developmental runtime can consume. The worker must distinguish **structural mediation affordances and channels** from generated biography or actor psychology.

Wave 0 is reconnaissance/specification. Do not implement a broad new V555 engine. The objective is to give Vozhd Dva a concrete, code-grounded contract for the implementation wave.

## System position

`V554 bounded structural/seed affordances → V555 mediation topology/conditions → V556 pressure-flow / attractor topology → V3 actor-specific developmental realization`

V555 must answer how structurally derived pressure may be mediated through carriers, institutions, households, family routes, locality, peers, etc., under conditions, without pretending those mediators are already concrete generated facts.

## Canonical read set — read in order

1. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/README.md`
2. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/CONSTRAINTS_PRIORITIES.md`
3. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/CAPABILITY_MATRIX.md`
4. `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/rabochii/WAVE_0/README.md`
5. `data/ddm_build_copy/ddm_v554_seed_contract.py`
6. `data/ddm_build_copy/compile_v554_thin_layer.py`
7. `data/ddm_build_copy/ddm_v555_life_course_mediation.py`
8. `data/ddm_build_copy/compile_v555_thin_layer.py`
9. `data/ddm_build_copy/ddm_v556_pressureflow.py`
10. `data/ddm_build_copy/compile_v556_thin_layer.py`
11. `data/ddm_build_copy/ddm_pipeline_final_contracts.py`
12. `data/ddm_build_copy/ddm_v5_build_standard.py`
13. `data/ddm_build_copy/ddm_v5_thin_end_to_end.py` — only V554→V556 portions.
14. `data/ddm_build_copy/tests/test_w05_final_cross_stage.py`
15. `data/ddm_build_copy/test_w06_downstream_typed_state_watchers.py`

## Frozen external facts

- Current `main` is the implementation frontier.
- V555 is not authorized to instantiate concrete parents, co-parents, children, households, institutions, biographies, memories, or psyche.
- V555 must nevertheless carry enough semantics for later runtime to generate realistic mediation rather than generic labels.
- Family/household/carrier mediation is part of the intended Rawlsing causal architecture.
- Orientation-to-strata and later pressure-flow depend on mediation conditions; V555 cannot collapse all mediation into one undifferentiated route.
- Generated runtime facts remain epistemically distinct from survey/source evidence and structural priors.

## Upstream contract

Treat V554's current bounded affordance contract as the producer surface. Determine what information is present, how much V555 currently retains, and which upstream distinctions are needed to condition mediation.

## Downstream obligations

V555 must eventually support V556/V3 reasoning about at least:

- mediation channel/type identity;
- eligible/available mediation routes rather than asserted memberships;
- conditions on route plausibility (position, geography, historical coordinate, access/exposure, family/household context, carrier/institutional relevance, etc. where supported);
- amplification, buffering, transmission, deflection, conflict, or blockage potential;
- directionality between structural source, mediator, and receiving position;
- multiple concurrent/competing mediation paths;
- uncertainty/confidence and source lineage;
- explicit distinction between structural possibility and generated runtime fact;
- enough information for later parent/co-parent/child transmission to be generated lawfully rather than baked in upstream.

Do not settle V556's full pressure-flow ontology. Identify only what V556 needs from V555.

## Current implementation questions to answer

The current V555 contains generic slots such as household, family, parent, co-parent, child, carrier, and regional/locality mediation, with unresolved statuses. Determine:

1. which of these are useful stage-level categories;
2. which are too coarse to support downstream causal work;
3. what semantic attributes each mediation object must carry;
4. whether one mediation object grain is sufficient or whether typed route/condition/relationship objects are needed;
5. what information from V554 is currently discarded or detached;
6. which current fields falsely imply more or less authority than they actually have.

## Authorized write domain

Wave 0 production semantics are **read-only** for this worker.

Allowed writes:

- worker cell result files only;
- optional diagnostic scripts/tests **only if** they do not change production behavior and materially strengthen evidence for a finding.

Worker report files:

- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/rabochii/WAVE_0/R0_02_V555/RESULT.md`
- `.../R0_02_V555/RESULT.json`

## Prohibited scope

- No broad edits to `ddm_v555_life_course_mediation.py` in Wave 0.
- No V554/V556 production changes.
- No actor-specific parent/child psychology, biography, memories, relationships, or generated household facts.
- No Enneagram assignment.
- No source-specific ontology branches.

## Required work

1. Trace representative V554 affordance information into V555.
2. Enumerate the current V555 object grains and statuses.
3. Trace what V556 receives from V555 today.
4. Identify semantic starvation, information loss, false precision, false emptiness, and conflated jurisdictions.
5. Propose the **minimum complete V555 information contract**: object grains, required fields, authority/provenance semantics, and states.
6. Map each proposed V555 element to a named downstream need rather than introducing speculative machinery.
7. State which current V555 structures can be retained, deepened, replaced, or removed.
8. Return any necessary cross-hooks to V554 or V556 without editing those stages.

## Acceptance evidence

`RESULT.md` must include:

- current V554→V555→V556 flow as observed;
- current V555 object-grain inventory;
- defect/gap table;
- proposed minimal V555 contract;
- producer-consumer obligations;
- explicit boundary between structural mediation and runtime-instantiated mediation;
- no ungrounded ontology expansion.

## Return format

Use `rabochii/WAVE_0/REPORT_FORMAT.json` exactly for `RESULT.json`.

Open a draft PR against `agent/vozhd-dva-wave0-integration`. Do not merge it.
