# Latest Extant V3/V2 Baseline — Binding Recovery Evidence for TD-R05

**Status:** `LATEST_EXTANT_V3_V2_IMPLEMENTATION_DESIGN_BASELINE__MIGRATE_OR_EXPLICITLY_SUPERSEDE`  
**Applies to:** TD-R05 V3 developmental-runtime court and later V2 court  
**Source archive:** user-supplied `Rawlsing_code_bundle_staging.zip`  
**Archive SHA256:** `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`  
**Recovered:** 2026-08-17 by Vozhd Dva

## 0. Evidentiary hierarchy

The archive is an old **whole-project** snapshot because its V5/DDM side predates the accepted TD-R00–TD-R04 V553–V558 architecture. Therefore:

- **The snapshot's V5/DDM bridge material is stale and nonbinding.** Accepted V553–V558 architecture and integration rulings supersede it.
- **The snapshot's V3/V2 subsystem is the latest extant V3/V2 implementation/design available.** It is not a discarded prototype and must not be treated as greenfield inspiration.
- TD-R05 must first reconstruct what the extant V3 actually is, then assign a finite disposition to each substantive mechanism:
  - `RECREATE_AS_IS`;
  - `ADAPT_TO_ACCEPTED_V553_V558_INPUTS`;
  - `SUPERSEDE_WITH_EXPLICIT_REASON`;
  - `DEFER_MISSING_AUTHORITY`;
  - `REMOVE_AS_OBSOLETE_BRIDGE_OR_PLACEHOLDER`.
- Silence is not a disposition. Existing V3/V2 mechanisms may not disappear merely because a cleaner architecture can be imagined.

The governing migration equation is therefore:

`LATEST EXTANT V3/V2 CAUSAL + PHENOMENOLOGICAL DESIGN`
`+ ACCEPTED V553–V558 STRUCTURAL-WORLD / RESOLVER ARCHITECTURE`
`- STALE V5 BRIDGE ASSUMPTIONS`
`- MECHANISMS THAT FAIL TERMINAL-DEMAND / AUTHORITY / NO-BLOAT COURT`
`= RECALIBRATED V3/V2`.

## 1. What the extant V3 already is

The extant V3 is a persistent developmental causal engine, not a thin persona vector.

### 1.1 Persistent `BackboneState`

`v3/core/state.py` stores year-to-year causal state including:

- `year`, `age`;
- macro field / calibration regime / boundary map;
- `strata_salience` and `strata_stack`;
- events and micro-trace;
- **material capacity**: time, money, health, social support, skill, mobility, risk tolerance, legitimacy;
- **psychological capacity**: vitality, aperture, reality anchor, binding, coherence, agency, transmutation;
- reproduction constraints: dependents, housing insecurity, legal status, debt, job insecurity, caregiving load;
- per-domain `A/S/V/Aim`, including **latent Aim** and **expressed Aim** with expression gating;
- multidimensional alienation: distant others, near others, self, moral totality;
- public/private/inner **registers**;
- wound sensitivities: shame, fear, anger, abandonment, control, recognition, loss;
- cracks and structural/psychological buffers with explicit costs;
- frameworks treated as **metabolic operators** with acute/chronic effects, half-life, failure mode, enemy requirement and institutional affinities;
- active relationship/institution **magnets**;
- collective infrastructure and practice stack;
- `PeakRouting`: loop topology, solidarity boundary, harm constraint, rage metabolization, theory-of-change style, coherence, impunity access, appetite profile and hysteresis;
- intensity/capture and style traits;
- ten need axes with `expectation_baseline = entitled | hopeful | forbidden | hopeless`;
- persistent `StrivingObject`s with investment, identity load, feasibility belief, social support, momentum, secrecy and costs;
- positive `GiftShard`s and negative/mixed `DisruptionShard`s;
- epistemic `RuptureShard`s;
- multi-year `MetabolizationProcess` objects with severity, opacity, prediction error, mode, status, plasticity window, narrators, provisional frame, downstream biases and reactivation triggers;
- narration support;
- `pressure_flow_history`, `pressure_flow_memory`, a surface psyche profile and a deliberately non-voice analyst account;
- child model / assumed rules / taboos / what-counts-as-possible;
- autonomy/safety drives and lived conditions;
- stability-threshold inertia.

**TD-R05 implication:** this state model has a presumption of continuity as the latest extant causal design. It must be audited field-by-field, not replaced wholesale by a newly invented actor schema.

## 2. Existing causal-order law

`v3/v3_yearly_step_order.yaml` is explicitly a mechanical sequencing contract whose stated purpose is to prevent circular causality, prevent LLM mutation of the backbone, and make ordering testable.

The extant ordered spine includes:

1. `field_update`;
2. `autonomy_safety_micro_drift`;
3. `event_sampling`;
4. `reproduction_constraints_update`;
5. `capacity_update`;
6. `health_drift_update`;
7. `buffers_update`;
8. `frameworks_update`;
9. `domains_update`;
10. `cracks_and_alienation_update`;
11. `plasticity_and_metabolization_update`;
12. `stability_inertia_dissipation`;
13. `striving_update`;
14. `practice_and_infrastructure_update`;
15. `topology_and_boundary_update`;
16. `attention_and_capture_update`;
17. `strategy_and_signal_effects`;
18. `style_trait_drift`;
19. `render_layer`;
20. later extension `active_magnets_update`.

The contract also distinguishes **stored state** from **derived indices**. Hostage index, agency capacity, health level, insulation, structural lucidity, mis-aim risk, metabolic style, autonomy/safety gaps, alignment, stability threshold and other indices are scheduled derivations rather than silently persisted causal truths.

Existing architecture tests enforce at least:

- render cannot mutate backbone state;
- sampled events cannot directly write domain or peak-routing state;
- the core step order is immutable except governed extensions;
- derived fields are not stored in `BackboneState`.

**TD-R05 implication:** preserve the ordered-causality / stored-vs-derived / render-nonmutation discipline unless a replacement proves stronger terminal necessity.

## 3. Existing LLM/runtime contract

The extant architecture is not “LLM writes a persona.” It explicitly designs two distinct LLM roles around code-owned causal state.

`V3_UNDERLIES_V2_ARTICULATION.md` states the intended relation:

- V3 is the **causal spine**;
- V2 is phenomenology/expression derived from that spine;
- the LLM may propose candidate developments but does not directly mutate backbone truth;
- each recursion interweaves code and LLM rather than running V3 once and rendering only at the end.

The extant intended recursion is:

1. V3 structural/causal update;
2. **Pass 1 LLM:** propose candidate events/magnets/framing shifts from current state;
3. deterministic/code-governed scoring and selection;
4. bounded application of accepted deltas to V3 backbone;
5. derive V2-compatible phenomenology from updated backbone;
6. **Pass 2 LLM:** render narrative/phenomenology only;
7. next recursion proceeds from the updated causal state, not from rendered prose.

`run_llm_band.py` implements the conceptual contract as `Pass 1 (propose events) → score → apply deltas + rupture + magnets → Pass 2 (render)`.

**TD-R05 implication:** the court must adjudicate whether this two-pass architecture survives, how proposal authority is governed, and whether LLM-assisted event proposal remains lawful under replay/provenance requirements. It may not silently collapse the two roles or convert rendered V2 output into causal state.

## 4. Pressure-flow as actor-specific lived routing

The extant `v3/psyche/flow.py` already models actor-specific pressure routing as runtime history/memory rather than merely copying structural pressure into a psyche field.

Observed design commitments include:

- current charge is distinguished from effect strength;
- route application is transactional so failed projection does not partially mutate live state;
- per-domain trace paths preserve exact routing attribution;
- prior grooves/history can alter later channel conductance;
- vitality changes conductance rather than falsifying the existence of current structural charge;
- event context is preserved with pressure-flow snapshots;
- surface/persona account is separated from analyst pressure account;
- pressure-flow history and memory round-trip as persistent runtime state.

The old file carries V5-named bridge assumptions that are now stale. Those inputs must be replaced by accepted `ResolvedStructuralContext` / V555 route / V556 interaction-topology identities.

**TD-R05 implication:** actor-specific realized flow/memory is strong candidate `ADAPT_TO_ACCEPTED_V553_V558_INPUTS`, not a reason to rebuild pressure response from scratch.

## 5. Existing metabolization / rupture architecture

Rupture and metabolization are not one-shot labels in the extant design.

A selected epistemic-rupture event may create:

- a `RuptureShard` carrying violated assumption, domain, opacity, prediction error, status, intrusive-return rate and meaning attempts;
- a `MetabolizationProcess` that persists across years with a mode such as assimilation, accommodation, sealing, collapse, transmutation or mis-aim;
- a plasticity window;
- narrator availability/accuracy/warmth/coercion;
- framework reconfiguration and downstream biases;
- reactivation triggers and persistent/chronic outcomes.

The explicit architectural intention is that rupture changes subsequent developmental dynamics through a multi-year process rather than becoming a decorative backstory sentence.

**TD-R05 implication:** preserve the causal distinction between event, rupture shard, ongoing metabolization process, derived phenomenology and rendered narrative. Exact state vocabulary/update formulas remain open to court.

## 6. Expectation baselines and striving

The extant design contains ten need axes:

`attachment, safety, belonging, status, competence, autonomy, meaning, justice, beauty_play, eros_intimacy`.

Each axis may carry an expectation baseline:

`entitled | hopeful | forbidden | hopeless`.

`StrivingObject`s represent persistent investment targets. The intended model allows forbidden/hopeless needs to produce proxy strivings rather than direct pursuit. Events may attach to striving objects through gift/disruption shards and prediction error.

The recovered docs are unusually valuable because they also record **underwiring defects**: at different points baseline/striving state existed in schema but was not fully included in Pass 1, scoring, or persona surfaces. Later audit tables record partial wiring. Therefore existence in state is not proof that the mechanism fully shaped behavior.

**TD-R05 implication:** expectation/striving is a real extant design commitment but must be audited for causal necessity, generation authority and complete flow. Do not either delete it silently or accept schema presence as proof of successful semantics.

## 7. Frameworks, buffers, cracks, alienation, registers and Aim

The extant architecture contains a coherent “metabolic” middle layer between structural condition and rendered personality:

- frameworks modify processing through time rather than acting as static ideological labels;
- buffers have strength and costs;
- cracks carry latent pressure and activation;
- alienation is multidimensional rather than a single ideology score;
- Aim is split between latent internal orientation and expressed orientation;
- public/private/inner registers gate expression;
- topology and boundary systems make response conditional on lived state rather than directly on survey categories.

**TD-R05 implication:** these mechanisms deserve explicit preservation/supersession rulings. The new nine-strata / V555/V556 topology should feed them only through actor-specific generated history, never by direct prior→psyche assignment.

## 8. Relationship / genealogy relevance

The extant V3 includes `Magnet` state and a `relational_field` projection, while V2 contains life-scaffold and relationship-memory designs. The old V5 bridge also tried to connect relational structure into V3 without adding a tenth stratum.

The accepted architecture now sharpens the jurisdiction:

- upstream household/family structural priors remain structural;
- actual parent/partner/household/child histories are generated runtime facts;
- recursive genealogy must run through V3 and then re-query the same immutable structural repository with generated bindings.

**TD-R05 implication:** recover useful magnet/relational-field dynamics, but rebuild their structural input seam around generated relationships and `ResolvedStructuralContext`. Do not treat upstream family priors as already-lived family history.

## 9. Existing V3→V2 boundary

The extant design explicitly states that V3 underlies V2:

- V3 owns yearly causal dynamics;
- V2 phenomenology—needs, strategies, indices, voice—is derived/rendered from V3 state;
- V2 should not run a competing causal life simulation;
- render code is tested not to mutate backbone state.

`v2/PERSONA_CONVERSATION_ENGINE_SPEC.md` adds a rich conversational layer including life scaffold, life season, today state, interaction context, attention/effort/social-energy gating, standpoint-driven salience, appraisal, boundary filtering, persistent relationship memory, face risk, interruptions, topic gravity, ignorance and response moves. Its central architectural instruction is effectively: **make the LLM a renderer, not the decider**.

The V2 document also contains a later life-simulation integration direction: derive conversation-life container/season from stored simulation history rather than separately generating a second biography.

**Later V2 court implication:** the conversation system is latest extant design evidence and must likewise be recovered/adapted, not regenerated generically. TD-R05 must preserve the V3 state/history needed to support it without allowing V2 to become causal authority.

## 10. Existing Enneagram emergence intent

`v2/ENNEAGRAM_EMERGENCE_SYSTEM.md` explicitly says Enneagram type emerges from life-course simulation and is **not assigned at birth**. It describes early imprint, developing needs/strategies/compensation, later pattern deepening, and end-of-simulation inference/matching.

That document predates the accepted V556/V3 jurisdiction and may contain old direct-scoring assumptions. Its **intent** is binding recovery evidence; its old formation algorithm is not automatically binding.

TD-R05 must preserve the core commitment:

- no birth assignment;
- no survey/category→type shortcut;
- attractor/type meaning comes from generated developmental history;
- structural prerequisites are not the realized attractor.

But it must re-adjudicate whether an end-of-run “match to type wisdom / score each type” classifier is still lawful, or whether the V3 attractor should instead be a persistent dynamical state whose eventual label is a downstream interpretation.

## 11. Known defects / migration hazards in the extant system

The snapshot itself documents several areas that must not be blindly recreated:

1. **Stale V5 input bridge.** `v5_runtime_input_bundle`, `v5_runtime_input_refs`, V5 field/pressure-flow wiring and V5 test names are obsolete structural-input plumbing. Replace with accepted V557/V558 repository/resolver contracts.
2. **Stored-but-underwired state.** Several fields existed in state/JSON without participating sufficiently in proposal, scoring, or phenomenology. Recreate only with an explicit causal-flow proof.
3. **Heuristic/default initialization.** Some mechanisms could default to generic 50s / `hopeful` / thin maps when authority was absent. New architecture requires explicit missing-authority handling where generation rules are absent.
4. **Yearly tick assumption.** Existing engine is yearly. TD-R05 must decide whether annual recursion remains semantically valuable, becomes a hybrid event/tick scheduler, or survives as a coarse integration step; it may not remove it merely because event sourcing sounds cleaner.
5. **LLM proposal authority.** Existing Pass 1 relies on LLM-proposed candidate events. The new court must bind candidate schemas, code-side admissibility, provenance, deterministic seed/replay policy and forbidden semantic invention.
6. **Numeric formulas.** Existing 0–100 state and update/scoring formulas are implementation evidence, not automatically governed authority. Preserve formulas only where their rationale/authority survives court; otherwise classify them as calibration/implementation authority gaps rather than deleting the underlying state need.
7. **Identity-pipeline assumptions.** Old docs sometimes assign identity generation to V2/parent pipelines. Accepted architecture now requires generated actor positions/relationships to be explicitly V3/runtime-owned where they are runtime facts. Recover the intended inheritance/genealogy behavior while reassigning jurisdiction correctly.
8. **Surface psyche / analyst account.** The separation is valuable; any V5-specific naming or mappings must be re-anchored to the new producer/resolver model.

## 12. Mandatory TD-R05 baseline-disposition court

Before proposing a replacement V3 object model, TD-R05 must issue an explicit disposition for at least these extant mechanisms:

1. persistent `BackboneState` pattern;
2. material capacity;
3. psychological capacity vector;
4. reproduction constraints;
5. domain A/S/V/Aim with latent/expressed Aim;
6. multidimensional alienation;
7. registers;
8. wound sensitivities;
9. cracks;
10. buffers and buffer costs;
11. frameworks as metabolic operators;
12. collective infrastructure;
13. practice stack;
14. peak routing / loop topology / solidarity boundary;
15. intensity/capture;
16. style traits;
17. expectation baselines;
18. striving objects;
19. gift/disruption shards;
20. rupture shards;
21. multi-year metabolization processes;
22. narration support;
23. active magnets;
24. child model / assumed rules / taboos / possible-world model;
25. autonomy/safety drives and conditions;
26. stability-threshold inertia;
27. pressure-flow history and memory;
28. relational-field projection;
29. ordered yearly mutation spine;
30. stored-state versus derived-index separation;
31. Pass 1 candidate-proposal role;
32. code scoring/selection/bounded application;
33. Pass 2 render-only role;
34. V3→V2 nonmutation boundary;
35. life-course-derived Enneagram emergence;
36. V2 conversation life scaffold / today state / attention budget / relationship memory as downstream consumer demand.

For every `SUPERSEDE` or `REMOVE` verdict, state what terminal capability replaces the mechanism and why the accepted architecture can still produce the intended person without it.

## 13. Presumption for TD-R05

The presumption is **migration, not demolition**.

Accepted V553–V558 changes what V3 is allowed to receive as structural authority. It does not, by itself, erase the accumulated V3 model of how a person metabolizes, remembers, resists, reproduces, refracts, or is changed by that world.

The court should expect a result shaped like:

`Recovered V3 causal organism`
`+ ResolvedStructuralContext input seam`
`+ explicit generated-event / genealogy / replay authority`
`+ corrected attractor-formation jurisdiction`
`- stale V5 bridge`
`- underwired/decorative state`
`- ungoverned shortcuts`
`= terminal V3`.
