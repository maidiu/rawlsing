# R0-02 — V555 Mediation Semantics Result

**Worker:** R0-02  
**Status:** COMPLETE_WITH_FINDINGS  
**Branch:** `agent/vozhd-dva-r0-02-v555`  
**Base:** `958983139b8f75dc5cda65d5bf71b376d17820df`  
**Target:** `agent/vozhd-dva-wave0-integration`

## Mission result

The current V555 boundary is not yet a semantically adequate mediation contract. It correctly protects against biography/psyche generation and preserves useful channel names, but it does not preserve enough V554 authority, temporal condition, route identity, or provenance for V556/V3 to reason about mediation causally. There is also a split semantic surface: the final V555 JSON packet and the specialized V555 Parquet artifacts describe different slot sets, while V556 consumes only the packet surface.

Wave-0 production semantics were left unchanged. No diagnostic script was necessary; the defects are directly visible in the current producer/consumer code.

## Current V554 → V555 → V556 flow as observed

### V554 producer surface

`ddm_v554_seed_contract.py` currently produces a comparatively rich bounded-affordance surface:

- `v554_seed_affordance_index.parquet` rows carry `seed_type`, `seed_domain`, `seed_scope`, source pressure/absence/contradiction IDs, source authority lanes, temporal/interpolation status, strength/confidence/specificity/certifiability scores, readiness/use permission, mediation-resolution flags, known absences, stop reasons, and the no-generated-person boundary.
- `v554_required_mediation_slot_index.parquet` names family, household, parent, co-parent, child, carrier/institutional, regional/locality, and school/work/church/neighborhood/media/party mediation requirements.
- `v554_v555_handoff_index.parquet` maps each seed affordance to a handoff lane, an allowed-use flag, a required channel, absences, prohibitions, and generation-ledger requirements.
- demographic/regional slice contracts plus absence, blocker, and prohibition ledgers remain separately available.

### V555 transformation today

`ddm_v555_life_course_mediation.py` reads the V554 readiness report, V554 packet, and V554 seed-affordance index, but does **not** read the V554 required-mediation-slot index, V554→V555 handoff index, demographic/regional slice contracts, or V554 absence/blocker/prohibition ledgers.

Its specialized `_slot_rows()` creates seven universal unresolved slots:

1. household
2. family
3. parent
4. co-parent
5. child
6. carrier
7. regional

Every slot receives the complete list of source V554 seed IDs, but not the per-seed type, scope, permission, temporal status, pressure/contradiction lineage, confidence, or route conditions that distinguish those seeds.

Its specialized register builder then creates household, parent, co-parent, child, and carrier rows only for `seed_rows[:5]`. Those rows preserve a single source seed ID and a negative boundary status, but no route topology or qualifying conditions.

### Split V555 output surface

`ddm_v5_thin_end_to_end.py::_payload_v555()` independently defines a second V555 semantic surface with five packet slots:

- household mediation
- parent transmission
- co-parent transmission
- child absorption/resistance
- institutional carrier mediation

Those packet slots contain small `requires` lists, but omit the specialized builder's family and regional slots. Conversely, the specialized seven-slot Parquet artifact is not the surface later consumed by V556.

`build_thin_layer()` invokes the specialized V555 builder when inputs are ready, but later rewrites the packet path from the generic `packet` object. The terminal packet therefore comes from `_payload_v555()` while readiness/artifact metadata point at the specialized V555 artifact set. V555 consequently has two internally divergent representations of its own mediation contract.

### What V556 receives today

`ddm_v556_pressureflow.py::_pressureflow_rows()` reads only `v555_life_course_mediation_packet.json`. It looks for `payload.mediation_contract.mediation_slots`, then falls back to `payload.mediation_slot_contracts`. It does not read `v555_mediation_slot_contracts.parquet` or `v555_v556_handoff_index.parquet`.

For each packet slot V556 retains only:

- slot name;
- slot channel;
- generic `candidate_dynamics_only` status;
- the V555 slot status string.

It does not receive source seed identity, source pressure/contradiction lineage, temporal conditions, route eligibility, directionality, competing-route identity, buffering/amplification potential, confidence, uncertainty, or mediation-specific provenance.

## Current V555 object-grain inventory

| Surface | Current grain | Useful content | Missing / misleading content |
|---|---|---|---|
| Generic packet | mediation slot | five channel categories plus coarse `requires` labels | no source-seed binding; no route identity; no route state; family/regional absent |
| Specialized Parquet | mediation slot | seven useful stage-level channel categories; explicit unresolved status | all seeds attached to every slot; no per-route qualification |
| Household register | seed × household placeholder, first five seeds only | negative boundary (`not_story`) | arbitrary truncation; no household route condition |
| Parent register | seed × parent placeholder, first five only | parent separated from co-parent | no transmission topology/condition/effect |
| Co-parent register | seed × co-parent placeholder, first five only | useful jurisdiction separation | same starvation as parent |
| Child register | seed × child placeholder, first five only | child absorption kept outside psyche | no developmental-route prerequisites beyond a status label |
| Carrier register | seed × carrier placeholder, first five only | membership-as-fact prohibited | no institution/carrier subtype, access, exposure, or relevance condition |
| Stop ledger | slot | negative boundary | all slots get the same reason; no route-specific blocking reason |
| V556 handoff index | slot | explicit downstream boundary artifact exists | every `allowed_v556_use` is false while V555 simultaneously reports `ready_for_v556 = true`; V556 ignores this index |

## Defect / gap table

| ID | Class | Severity | Defect | Downstream consequence |
|---|---|---:|---|---|
| R0-02-F001 | DEFECT | HIGH | Final packet and specialized V555 artifact expose different slot sets and semantics. | V556 consumes a different contract from the one V555 readiness/artifact metadata advertise. |
| R0-02-F002 | INFORMATION_LOSS | HIGH | V555 ignores V554's mediation-slot index, V554→V555 handoff index, slice contracts, and absence/blocker/prohibition artifacts. | Existing producer distinctions do not constrain mediation construction. |
| R0-02-F003 | SEMANTIC_GAP | HIGH | Current grain is a channel placeholder, not a mediated route with structural source, mediator, receiver constraint, and conditions. | VS-3/VS-4 cannot represent alternative routes, buffering/amplification, or competing developmental possibilities. |
| R0-02-F004 | DEFECT | HIGH | Specialized V555 says `ready_for_v556 = true` while every handoff row has `allowed_v556_use = false`; V556 ignores the handoff index anyway. | Permission semantics are non-operative and contradictory. |
| R0-02-F005 | DEFECT | MEDIUM | Household/parent/co-parent/child/carrier registers use `seed_rows[:5]`. | Row position, not authority or mediation relevance, decides which seeds appear; this creates false emptiness and false representativeness. |
| R0-02-F006 | INFORMATION_LOSS | HIGH | Per-seed temporal status, interpolation status, pressure/contradiction IDs, use permission, uncertainty, and score fields are not attached to V555 routes and do not reach V556. | V556 cannot condition pressure-flow on historical coordinate, contradiction, uncertainty, or source lineage. |
| R0-02-F007 | HAZARD | MEDIUM | Names such as `generated_mediation_slots_only_not_biography`, `channelized_and_generated_not_factual`, and `generated_mediation_only` use “generated” for unresolved structural mediation scaffolds. | Structural possibility and runtime-instantiated generated facts are epistemically blurred even while biography is prohibited. |
| R0-02-F008 | SEMANTIC_GAP | HIGH | V555 has no operative fields for directionality, concurrent/competing routes, amplification, buffering, transmission, deflection, conflict, or blockage potential. | V556 receives generic labels instead of a mediation topology. |
| R0-02-F009 | NO_DEFECT | INFORMATIONAL | Parent/co-parent/child/household/carrier/regional distinctions and the no-biography/no-psyche prohibitions are useful. | These should be retained as channel vocabulary/boundary law rather than discarded in redesign. |

## Proposed minimum complete V555 information contract

The minimum adequate grain is **two objects**, not one universal slot and not a full relationship ontology.

### 1. `mediation_route_candidate`

One row means: *given this bounded V554 structural affordance, this mediation channel is structurally eligible/reviewable/blocked under named conditions*. It does **not** assert that a concrete actor has the mediator, membership, relationship, exposure, or life event.

Required fields:

- identity: `mediation_route_id`, `run_id`;
- upstream binding: `source_seed_affordance_id` and, by reference or carried keys, source pressure/absence/contradiction IDs and authority lanes;
- channel identity: `channel_class`, optional governed `channel_subtype`;
- structural endpoints: `source_scope`, `receiving_scope_constraint`, `directionality` (`structural_source -> mediator_channel -> receiving_position`);
- route authority state: `route_state` = `eligible_structural_route | reviewable_structural_route | blocked_route | not_applicable`;
- temporal authority: `temporal_status`, `interpolation_status`, and the relevant historical/temporal scope or reference;
- potential operation: `effect_potentials_json`, limited to the assignment-required vocabulary (`amplification`, `buffering`, `transmission`, `deflection`, `conflict`, `blockage`), explicitly as **potential**, never realized effect;
- concurrency: `route_group_id` plus optional competing/concurrent route references;
- uncertainty: route confidence/certifiability or direct references to the governing V554 seed values;
- negative authority: `known_absences_json`, `stop_reasons_json`;
- epistemic boundary: `epistemic_class = structural_mediation_possibility`, `runtime_instantiation_status = not_instantiated`.

Channel vocabulary should reuse current governed categories rather than expand freely: household, family, parent, co-parent, child, carrier/institutional, regional/locality, and peer/institutional subtypes where the accepted upstream requirement warrants them. School/work/church/neighborhood/media/party should be governed subtypes of the carrier/institutional route unless Vozhd Dva chooses to preserve them as separate route classes.

### 2. `mediation_route_condition`

One row qualifies a route without turning the qualifier into biography.

Required fields:

- `condition_id`, `mediation_route_id`;
- `condition_type` drawn only from named downstream needs: position, geography/locality, historical coordinate, access/exposure, family/household context, carrier/institutional relevance;
- `condition_scope_or_constraint`;
- `condition_state` = `supported_structurally | required_unresolved | blocked | not_applicable`;
- provenance/source reference;
- confidence/uncertainty or governing V554 reference;
- `epistemic_class = structural_condition_not_runtime_fact`.

A third relationship-object grain is **not yet required**. The route candidate can carry source → mediator → receiving directionality inline. Add a distinct relationship table only if implementation proves that repeated multi-hop edge reuse cannot be represented economically.

## Producer-consumer obligations

### V554 → V555

V555 must preserve, directly or by stable reference:

- seed affordance identity/type/domain/scope;
- source pressure, absence, contradiction, and authority lineage;
- temporal/interpolation status;
- readiness/use permission;
- strength/confidence/specificity/certifiability where they gate route authority;
- mediation-resolution flags;
- known absences and stop reasons;
- V554 required-mediation-slot and V554→V555 handoff semantics.

V555 may transform those into route candidates and route conditions. It must not infer concrete household membership, family relations, parent/co-parent identity, child biography, institutional membership, actor orientation, psyche, or memory.

### V555 → V556

V556 must receive, per route:

- stable route ID and channel/subtype;
- source seed and pressure/contradiction lineage;
- structural source and receiving-position constraints;
- temporal scope/conditions;
- route state and condition states;
- potential amplification/buffering/transmission/deflection/conflict/blockage semantics;
- concurrent/competing route grouping;
- uncertainty/confidence;
- provenance and epistemic class.

V556 may transform these into pressure-flow topology and attractor prerequisites. It must not interpret structural eligibility as actual exposure/transmission, or produce finished psyche/Enneagram identity.

## Boundary: structural mediation vs runtime-instantiated mediation

**V555 owns:** statements of the form “this upstream structural affordance may/reviewably may/cannot be mediated through channel X under structural conditions Y, with lineage Z and uncertainty U.”

**V555 does not own:** “this generated person had parent A, lived in household B, attended institution C, absorbed pressure D, resisted caregiver E, or developed response F.” Those are runtime facts/events and remain V3/genealogy jurisdiction.

A V555 route therefore names an **eligible structural pathway**, not a member, relationship, event, memory, biography, or psyche. Runtime may later instantiate a route only after actor/history-specific conditions are generated and satisfied; that instantiated fact must retain an explicit generated-runtime epistemic class distinct from the V555 structural prior.

## Retain / deepen / replace / remove

### Retain

- parent vs co-parent separation;
- household vs family distinction;
- child absorption/resistance as non-psyche mediation vocabulary;
- carrier/institutional and regional/locality categories;
- no-biography/no-psyche/no-membership-as-fact prohibitions;
- stable V554 seed lineage.

### Deepen

- `mediation_slot_contracts` into route candidates + route conditions;
- stop reasons into route/condition-specific negative authority;
- V556 handoff into an operative permissioned contract;
- channel subtyping for governed institution/carrier distinctions;
- temporal/provenance attachment at route grain.

### Replace as primary semantic artifacts

- arbitrary first-five per-channel placeholder registers;
- “all source seed IDs belong to every slot” linkage;
- duplicate generic-vs-specialized slot surfaces;
- universal `unresolved` slots as the only positive mediation representation.

Existing channel-specific registers may survive as **derived views** if useful for audit/debugging, but should not be independent authority surfaces.

### Remove / rename

- rename `generated_mediation_*` structural scaffold states to `structural_mediation_*` / `route_candidate_*` language;
- remove the contradiction between `ready_for_v556` and all-false `allowed_v556_use` by making handoff permission derive from route state and required condition resolution.

## Cross-hooks for Vozhd Dva

1. **V554/V555 seam:** no broad V554 redesign is currently proven necessary. V555 should first consume the already-produced `v554_required_mediation_slot_index.parquet` and `v554_v555_handoff_index.parquet` and preserve stable V554 lineage. If implementation cannot express receiving-position constraints from existing seed scope/domain/pressure references, return that narrow missing endpoint reference to the V554 owner rather than inventing it in V555.
2. **V555/V556 seam:** R0-03/V556 must consume the accepted V555 route/condition contract rather than only generic slot name/channel strings. The current V556 fallback parser and its disregard of the V555 handoff index must be replaced or deepened in the implementation wave.
3. **Thin-end-to-end integration:** Vozhd Dva should adjudicate one canonical V555 packet/artifact surface. The generic `_payload_v555()` packet and specialized `ddm_v555_life_course_mediation.py` artifacts cannot both remain independent authorities.

## Validation / acceptance evidence

- Canonical assignment read in full.
- All 15 canonical read-set files were inspected in the required order, with V554/V555/V556 implementation portions traced at function/field level.
- V554 seed/handoff production fields were traced into V555 consumers.
- Both V555 semantic surfaces were inventoried.
- V556 consumption was traced to the final V555 JSON packet and shown not to consume the specialized slot/handoff Parquets.
- No production file was edited.
- No executable test was required for a specification-only Wave-0 report; the local container also lacks `gh`/a repository checkout, so existing pytest suites were not executed. Existing relevant test files were read as required.

## Recommended Vozhd Dva action

**ACCEPT_FINDINGS_ONLY**, then adjudicate R0-02 together with R0-03/R0-04 and freeze one canonical route/condition seam before Wave-1 V555/V556 implementation.
