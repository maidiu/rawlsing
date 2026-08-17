# Latest Extant V3/V2 Baseline — Recovery Evidence for TD-R05

**Status:** `LATEST_EXTANT_V3_V2_IMPLEMENTATION_DESIGN_EVIDENCE__CONTINUITY_DESIRED__TERMINAL_VISION_SOVEREIGN`  
**Applies to:** TD-R05 V3 developmental-runtime court and later V2 court  
**Source archive:** user-supplied `Rawlsing_code_bundle_staging.zip`  
**Archive SHA256:** `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`  
**Recovered:** 2026-08-17 by Vozhd Dva

## 0. Evidentiary hierarchy

Read first and obey:

`data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/integration/V3_V2_RECOVERY_EVIDENCE_PRIORITY_RULING.md`.

That ruling controls this document. In particular:

- **continuity with extant V3/V2 is desired wherever lossless**;
- **V550+-grounded Rawlsing vision-integrity is absolute**;
- extant V3/V2 is implementation/design evidence and a reuse opportunity, never a constraint on V550+ or the terminal personhood architecture;
- if extant V3/V2 cannot consume the complete accepted structural world without loss, V3/V2 changes;
- if two terminally equivalent solutions exist, prefer continuity and reuse.

The archive is an old **whole-project** snapshot because its V5/DDM side predates accepted TD-R00–TD-R04 V553–V558 architecture. Therefore:

- snapshot V5/DDM bridge material is stale and nonbinding;
- snapshot V3/V2 is the latest extant V3/V2 implementation/design available;
- TD-R05 must understand extant V3/V2 before discarding machinery so capability is not lost through ignorance;
- every substantive mechanism must receive a finite disposition:
  - `REUSE_UNCHANGED_IF_FULLY_COMPATIBLE`;
  - `ADAPT_TO_TERMINAL_ARCHITECTURE`;
  - `REPLACE_WITH_STRONGER_MECHANISM`;
  - `DEFER_MISSING_AUTHORITY`;
  - `REMOVE_AS_OBSOLETE_OR_REDUNDANT`.

Silence is not a disposition. Explicit disposition protects continuity and prevents accidental capability loss. It does not create architectural deference.

The governing equation is:

`WHOLE TERMINAL RAWLSING PERSONHOOD DEMAND`
`+ ACCEPTED MAXIMAL V553–V558 STRUCTURAL-WORLD / RESOLVER ARCHITECTURE`
`+ RECOVERED V3/V2 CAPABILITY EVIDENCE`
`+ CONTINUITY PREFERENCE WHERE LOSSLESS`
`- STALE V5 BRIDGE ASSUMPTIONS`
`- V3/V2 MECHANISMS THAT CONSTRAIN OR DUPLICATE TERMINAL DESIGN`
`- UNGOVERNED / UNDERWIRED / DECORATIVE IMPLEMENTATION ACCIDENTS`
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

**TD-R05 implication:** audit this state model field-by-field. Preserve or adapt fields that remain terminally useful; expand or replace any field/model that cannot realize the complete accepted V550+ structural world or stronger personhood design.

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

**TD-R05 implication:** this ordered-causality / stored-vs-derived / render-nonmutation discipline is a strong continuity candidate. Preserve it if terminally adequate; hybridize or replace it if stronger causality requires doing so.

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
7. next recursion proceeds from updated causal state, not from rendered prose.

`run_llm_band.py` implements the conceptual contract as `Pass 1 (propose events) → score → apply deltas + rupture + magnets → Pass 2 (render)`.

**TD-R05 implication:** adjudicate whether this two-pass architecture is still the strongest design under the full V550+ world, how proposal authority is governed, and whether LLM-assisted event proposal remains lawful under replay/provenance. Reuse it if lossless; strengthen/replace it if necessary. Never collapse rendered V2 output into causal state.

## 4. Pressure-flow as actor-specific lived routing

The extant `v3/psyche/flow.py` already models actor-specific pressure routing as runtime history/memory rather than merely copying structural pressure into a psyche field.

Observed design commitments include:

- current charge distinguished from effect strength;
- transactional route application so failed projection does not partially mutate live state;
- per-domain trace paths preserving routing attribution;
- prior grooves/history altering later channel conductance;
- vitality changing conductance rather than falsifying structural charge;
- event context preserved with pressure-flow snapshots;
- surface/persona account separated from analyst pressure account;
- pressure-flow history and memory round-trip as persistent runtime state.

The old file carries stale V5-named bridge assumptions. Those inputs must be replaced by accepted `ResolvedStructuralContext` / V555 route / V556 interaction-topology identities.

**TD-R05 implication:** this is a strong serendipitous-bridge candidate, but the extant implementation may be retained only if it can consume all accepted route/interaction/topology distinctions without flattening them. Otherwise expand/redesign it.

## 5. Existing metabolization / rupture architecture

Rupture and metabolization are not one-shot labels in the extant design.

A selected epistemic-rupture event may create:

- a `RuptureShard` carrying violated assumption, domain, opacity, prediction error, status, intrusive-return rate and meaning attempts;
- a `MetabolizationProcess` persisting across years with a mode such as assimilation, accommodation, sealing, collapse, transmutation or mis-aim;
- a plasticity window;
- narrator availability/accuracy/warmth/coercion;
- framework reconfiguration and downstream biases;
- reactivation triggers and persistent/chronic outcomes.

The explicit intention is that rupture changes subsequent developmental dynamics through a multi-year process rather than becoming decorative backstory.

**TD-R05 implication:** preserve the terminal capability—event → rupture state → ongoing metabolization → later causal effects → rendered phenomenology. Exact vocabulary, ownership and formulas remain fully open to redesign.

## 6. Expectation baselines and striving

The extant design contains ten need axes:

`attachment, safety, belonging, status, competence, autonomy, meaning, justice, beauty_play, eros_intimacy`.

Each axis may carry an expectation baseline:

`entitled | hopeful | forbidden | hopeless`.

`StrivingObject`s represent persistent investment targets. The intended model allows forbidden/hopeless needs to produce proxy strivings rather than direct pursuit. Events may attach to striving objects through gift/disruption shards and prediction error.

Recovered docs also record **underwiring defects**: baseline/striving state sometimes existed in schema without fully shaping proposal, scoring, or persona surfaces.

**TD-R05 implication:** treat expectation/striving as extant capability evidence. Reuse only if terminally justified and fully wired; strengthen/replace if the total personhood architecture demands more or different state.

## 7. Frameworks, buffers, cracks, alienation, registers and Aim

The extant architecture contains a coherent “metabolic” middle layer between structural condition and rendered personality:

- frameworks modify processing through time rather than acting as static ideological labels;
- buffers have strength and costs;
- cracks carry latent pressure and activation;
- alienation is multidimensional rather than a single ideology score;
- Aim splits latent internal orientation from expressed orientation;
- public/private/inner registers gate expression;
- topology/boundary systems make response conditional on lived state rather than directly on survey categories.

**TD-R05 implication:** these mechanisms are serious continuity candidates, not protected ontology. Reuse/adapt where they remain the strongest realization of terminal personhood; replace where richer V550+ inputs or stronger causal modeling require it.

## 8. Relationship / genealogy relevance

The extant V3 includes `Magnet` state and a `relational_field` projection, while V2 contains life-scaffold and relationship-memory designs. The old V5 bridge also tried to connect relational structure into V3 without adding a tenth stratum.

Accepted architecture now sharpens jurisdiction:

- upstream household/family structural priors remain structural;
- actual parent/partner/household/child histories are generated runtime facts;
- recursive genealogy runs through V3 and re-queries the immutable structural repository with generated bindings.

**TD-R05 implication:** recover useful magnet/relational-field behavior where terminally adequate, but redesign as necessary around generated relationships and `ResolvedStructuralContext`. Never treat upstream family priors as already-lived family history.

## 9. Existing V3→V2 boundary

The extant design explicitly states V3 underlies V2:

- V3 owns yearly causal dynamics;
- V2 phenomenology—needs, strategies, indices, voice—is derived/rendered from V3 state;
- V2 should not run a competing causal life simulation;
- render code is tested not to mutate backbone state.

`v2/PERSONA_CONVERSATION_ENGINE_SPEC.md` adds a rich conversational layer including life scaffold, life season, today state, interaction context, attention/effort/social-energy gating, standpoint-driven salience, appraisal, boundary filtering, persistent relationship memory, face risk, interruptions, topic gravity, ignorance and response moves. Its central architectural instruction is effectively: **make the LLM a renderer, not the decider**.

The V2 document also contains a later life-simulation integration direction: derive conversation-life container/season from stored simulation history rather than separately generating a second biography.

**Later V2 court implication:** this is valuable extant design evidence. Preserve continuity where it serves the strongest terminal architecture, but V2 remains downstream and cannot constrain V550+ or V3 causal design.

## 10. Existing Enneagram emergence intent

`v2/ENNEAGRAM_EMERGENCE_SYSTEM.md` explicitly says Enneagram type emerges from life-course simulation and is **not assigned at birth**. It describes early imprint, developing needs/strategies/compensation, later pattern deepening, and end-of-simulation inference/matching.

That document predates accepted V556/V3 jurisdiction and may contain obsolete direct-scoring assumptions. Its **intent** is strong recovery evidence; its old formation algorithm is not protected.

TD-R05 must preserve the terminal commitment:

- no birth assignment;
- no survey/category→type shortcut;
- attractor/type meaning comes from generated developmental history;
- structural prerequisites are not the realized attractor.

It must choose the strongest lawful attractor architecture even if that requires replacing the old end-of-run classifier/score.

## 11. Known defects / migration hazards

Do not blindly recreate:

1. **Stale V5 input bridge.** Replace `v5_runtime_input_bundle`, `v5_runtime_input_refs`, old V5 field/pressure-flow wiring and test assumptions with accepted V557/V558 repository/resolver contracts.
2. **Stored-but-underwired state.** Schema presence is not semantic success.
3. **Heuristic/default initialization.** Generic defaults cannot substitute for missing generation authority.
4. **Yearly tick assumption.** Valuable continuity candidate, not sacred. Adjudicate annual vs hybrid/event-driven architecture by terminal causality.
5. **LLM proposal authority.** Bind candidate schemas, code-side admissibility, provenance, deterministic/replay policy and forbidden invention.
6. **Numeric formulas.** Existing 0–100 and scoring formulas are implementation evidence, not automatically governed authority.
7. **Identity-pipeline assumptions.** Reassign generated actor positions/relationships to correct V3/runtime jurisdiction.
8. **Surface psyche / analyst account.** Preserve useful separation if terminally adequate; re-anchor all stale producer mappings.

## 12. Mandatory TD-R05 capability/disposition court

Before finalizing recalibrated V3, TD-R05 must issue an explicit capability and disposition ruling for at least:

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
15. need axes / expectation baselines;
16. striving objects;
17. gift/disruption shards;
18. rupture shards;
19. multi-year metabolization;
20. magnets / relational field;
21. pressure-flow history/memory/grooves/conductance;
22. child model / assumed rules / taboos / possible-world boundary;
23. autonomy/safety drives;
24. stability-threshold inertia;
25. yearly ordered causal spine;
26. stored-vs-derived separation;
27. Pass 1 LLM proposal;
28. deterministic score/apply boundary;
29. Pass 2 render-only role;
30. V3-under-V2 nonmutation contract;
31. life-course Enneagram emergence machinery.

For each, state:
- terminal capability served;
- whether the capability remains required;
- compatibility with complete accepted V550+ semantics;
- whether extant implementation is terminally adequate;
- final disposition;
- replacement-capability proof if changed/removed;
- continuity cost, if any.

## 13. Final law

**Continuity is desired. V550+-grounded Rawlsing vision-integrity is absolute.**

Use extant V3/V2 wherever it already fits or can be adapted without loss. Change it however much is necessary whenever the stronger terminal implementation requires it.
