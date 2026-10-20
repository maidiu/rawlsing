# ADP-015 — V3 Relationship, Household & Genealogy Authority

**Assignment:** W2-03  
**RA-R00 item:** `MUST-015 / ADP-015`  
**Authority ID:** `V3_RELATIONSHIP_HOUSEHOLD_GENEALOGY_RULE`  
**Authority version:** `1.0.0`  
**Registry:** `V3_RELATIONSHIP_HOUSEHOLD_GENEALOGY_RULE_REGISTRY@1.0.0`  
**Owner:** `V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE`  
**Exact launch base:** `fe52ca60ed00650b0a7b5bf77bab8ac40d53f4d8`  
**Mode:** authority creation only; no production implementation; whole-machine architecture remains CLOSED  
**Verdict:** `PASS`

## 1. Binding holding

ADP-015 governs the V3 causal seam by which independently generated actors may acquire relationship history, form or leave shared households, become parents through an exact child-generation event, and recursively create a new actor whose own initialization and development remain separate authorities.

The canonical recursion is:

```text
Parent 1: independently generated actor history
        \
         -> exact lawful encounter / later causal witnesses
        /
Parent 2: independently generated actor history
        -> governed relationship formation/evolution
        -> governed household/family field where actually formed
        -> governed child-generation event
        -> new child actor identity/ref
        -> child's own ADP-007 initialization
        -> child's own V3 developmental history
```

The constitutional noncollapse is:

```text
ADP-010 ENCOUNTER / EXPOSURE
!= RELATIONSHIP FORMATION
!= RECIPROCITY
!= HOUSEHOLD FORMATION
!= HOUSEHOLD MEMBERSHIP
!= PARENTHOOD
!= CHILD GENERATION
!= CHILD INITIALIZATION
!= CHILD PERSONALITY / TYPE

OBJECTIVE RELATIONSHIP HISTORY
!= ACTOR-PERCEIVED RELATIONSHIP STATE
!= ACTOR ACCESSIBILITY / CLAIM PERMISSION
!= V2 RELATIONSHIP EXPRESSION / SESSION POSTURE

TWO PARENT HISTORIES
!= HOUSEHOLD PERSONA
!= CHILD PERSONALITY MIXTURE
```

Encounter is a prerequisite only where a relationship rule names it. Co-presence, exposure, demographic compatibility, structural similarity, one actor's attachment, V2 tone, transcript persistence, or household plausibility never create a relationship by themselves.

A child is a new generated entity. ADP-015 creates the genealogy event, stable child actor reference and exact parenthood lineage; it does not initialize the child's psyche, infer inherited personality/type, copy a parent's state, or average the parents into a composite actor.

## 2. Governing authority and exact dependencies

Direct accepted dependencies consumed:

1. `ADP-009 / V3_STRUCTURAL_POSITION_GENERATION_MOBILITY_RULE@1.0.0` — exact generated positions may constrain a relationship/household/genealogy rule only when that rule explicitly names them; positions never imply partner compatibility or family role.
2. `ADP-010 / V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0` — exact encounter history may be a formation prerequisite; encounter/exposure never itself asserts relationship, reciprocity, household, sex, conception, parenthood or child generation.
3. `ADP-020@1.0.0` — all causal randomness uses static named `v3.causal.*` streams and exact `JOINT` or `GENEALOGY` scopes; randomness never manufactures a candidate or repairs missing relationship/fertility authority.

Binding higher-order/current law inspected at the exact launch base includes W2 launch law, `CURRENT_STATE.md`, `RAWLSING_GOVERNING_SPIRIT.md`, `TERMINAL_DEMAND_ENVELOPE.md`, `ARCHITECTURE_PASS_LAW.md`, V3 completion, whole-machine closure, implementation-release synthesis, W0 closure, W1 closure, RA-R00 and TD-R05.

Accepted downstream boundary consulted, without transferring ownership: `CAN-019 / V2_RELATIONSHIP_EXPRESSION_RULE@1.0.0`. Its binding law remains `ONE_ACTOR_VIEW != RECIPROCAL_RELATIONSHIP_TRUTH` and rendered/session state never creates V3 truth.

No W2 sibling result was used as authority.

### Exact consumers

RA-R00 consumers are:

- `V3-P9` — relationship / household / genealogy runtime integration;
- `V3-P13` — recursive generated-person/genealogy integration.

ADP-015 does not itself release either packet.

## 3. Required historical archive verification

Required archive: `Rawlsing_code_bundle_staging.zip`.

- expected SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`;
- directly computed SHA256 before reliance: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`;
- ZIP entries: `13,138`;
- verdict: `EXACT_MATCH`.

Recovered V3/V2/server material is continuity / authority-recovery / negative-boundary evidence only. Historical V5/DDM has zero authority over current V550+.

Focused recovered-source court executed:

```text
python -m pytest -q \
  v3/tests/test_step_logic.py \
  v3/tests/test_connector_and_field_injection.py

23 passed, 2 SyntaxWarning warnings in legacy v2/data_access.py
```

Passing tests prove recovered implementation continuity only, not terminal relationship or genealogy semantics.

### Direct recovered files inspected

- `v3/systems/reproduction.py` (`6f3a815d...`) — event-driven `dependents`/housing/legal/debt/job/caregiving constraint deltas; **not** partner, fertility, parenthood or child-identity authority.
- `v3/io/parent_baseline_from_behavior.py` (`4e5be644...`) — averages father/mother warmth/authority/material support and defaults missing values to `50`; negative evidence for parent-history collapse/default psychology.
- `v3/core/state.py`, `v3/core/year_record.py`, `v3/io/identity_to_backbone.py` — typed-state/hash continuity and legacy parent-derived child-state shortcuts.
- `v3/V3_UNDERLIES_V2_ARTICULATION.md` (`5a0f1127...`) — useful parents-first direction, but historical demand for concrete inherited identity/country fallbacks is superseded.
- `v2/identity_generator.py` (`e7bfdee7...`) — `generate_parent_identities` creates one shared household demographic context, samples coupled parent ages, enforces a configurable father-older convention, samples WVS education/religion, and `create_persona_identity_from_parents` copies household ethnicity/religion/class/location into the child with fallbacks/random ID/gender.
- `v2/parent_age_model.py` (`ecd8878a...`) — global/configured age-gap mixtures, hard age gates, resampling and story-reason logic; compatibility evidence only.
- `v2/parent_enrichment.py` (`ebf9ba22...`) — historical household/world enrichment; useful only as source-bound context when later consumed through lawful generated actors/rules.
- `v2/parent_type_inference.py` (`b05632d0...`) and `v2/references/PARENT_CHILD_TYPE_SCHEMA.md` (`db1f2392...`) — direct parent-type and parent-type→child-type inference; rejected.
- `v2/PARENT_IDENTITY_PIPELINE.md` (`936ca886...`) — parents-first orchestration continuity with nonterminal demographic/behavior inheritance assumptions.
- `v2/spec.py` (`f7ca16a7...`) — parent behavior sampling and parent-to-meeting/fused-family narrative prompts; narrative is not causal genealogy.
- `server/generation/simulation.py` (`5d68ffe3...`) — historical orchestration generates parent bundle, derives child identity from it, then optionally asks LLM for parent meeting/fused narrative; useful workflow evidence but not terminal causal authority.
- directly coupled tests `test_step_logic.py` and `test_connector_and_field_injection.py`.

## 4. Recovered mechanism dispositions

### `PRESERVE`

- parents-before-child causal direction as a recursion requirement;
- stable typed state / event-history / hash / integrity direction from recovered V3;
- the distinction between material/caregiving constraints and identity/personality;
- source-bound historical household/world context as possible causal input **only after** exact generated parent/household rules admit its use.

### `ADAPT`

- recovered “parent bundle” -> two separate generated actor refs plus a shared relationship/household entity with its own history;
- parent-first child creation -> exact genealogy event + new child actor ref, followed by separate ADP-007 initialization;
- parent/household context -> exact provenance-bearing parent and household causal refs, never an averaged household persona;
- recovered `dependents`/caregiving continuity -> downstream material/organismic constraint effects only through the exact target authority, never evidence that a child exists;
- parent meeting narrative direction -> objective relationship formation only from exact generated/admitted causal witnesses; narrative prose may render history later but cannot create it.

### `COMPATIBILITY_ONLY`

- global/configured parent age and age-gap mixture models;
- father-older convention, fixed father/mother gender defaults, minimum parent-age gates and “story reason” logic;
- WVS respondent spouse/parent distributions, shared-household SES/ethnicity/religion/language sampling;
- legacy family names and parent/child display identity fields;
- legacy `ReproductionConstraints` numeric representation and annual delta cap as genealogy semantics;
- LLM parent-to-meeting / fused-family prose;
- any historical household summary object used only as a presentation/migration carrier.

### `REMOVE / REJECT AS TERMINAL AUTHORITY`

- demographic compatibility -> partner selection;
- encounter/exposure -> automatic relationship;
- one shared household demographic row -> both parents' independent histories;
- country/ethnicity/religion/class defaults -> child generated identity;
- random child ID/gender/name as genealogy authority;
- parent behavior default `50`, hopeful baseline and arithmetic parent averaging;
- `infer_parent_type*`, parent Enneagram/type, parent-type→child-type effects and any inherited personality/type mixture;
- ungoverned fertility, marriage, cohabitation, partner-choice or child probabilities;
- model/LLM prose deciding how parents met, what their relationship is, or why a child exists;
- V2 relationship/session/tone state as V3 relationship evidence.

## 5. Exact jurisdiction

ADP-015 owns:

1. shared relationship-entity identity and append-only lifecycle history;
2. exact participant/role/directionality bindings under a governed relationship rule;
3. relationship formation, transition and end admission from exact generated/admitted causal witnesses;
4. actor-specific perceived-relationship state records where an exact relationship rule emits them, without automatic accessibility;
5. household entity identity, lifecycle and objective membership facts/events;
6. genealogy-scope identity and child-generation decision/admission;
7. new child generated-entity reference identity;
8. parenthood lineage facts created by the child-generation event;
9. independent-parent-history anchoring and recursive causal provenance;
10. candidate-set construction and ADP-020 binding for explicitly stochastic relationship/household/generation rules;
11. valid-empty, nonoccurrence, unknown, missing, deferred, negative, asymmetric, ambiguous and integrity outcomes;
12. the generated-life refresh obligation after relationship/household/family binding changes, while exact resolver requery wire semantics remain separately canonicalized.

ADP-015 does **not** own:

- actor creation/initialization state beyond the bare child generated-entity ref (`ADP-007`);
- actor structural position generation/mobility (`ADP-009`);
- opportunity/encounter/exposure (`ADP-010`);
- causal RNG algorithm (`ADP-020`);
- V555/V556 realization, response, organismic/material state, needs, rupture, memory, knowledge/accessibility, orientation or attractor semantics;
- universal sex/gender/age/fertility/reproduction biology;
- relationship trust/intimacy/personality scores;
- actor claim accessibility (`ADP-017` remains separate);
- V2 relationship expression/session posture (`CAN-019`);
- names, rendered family narrative or application/session state.

## 6. Canonical entity contracts

### 6.1 `V3RelationshipEntity`

Required semantic fields:

```text
relationship_entity_id
relationship_rule_id / relationship_rule_version
participant_bindings[] {
  actor_id,
  participant_role_ref,
  role_semantics_hash
}
directionality_kind
establishing_event_id
effective_from
ended_by_event_id | null
objective_state_fact_refs[]
relationship_history_anchor_hash
provenance_refs[]
entity_hash
```

`directionality_kind` is limited to lifecycle structure:

- `JOINT_SHARED` — the rule establishes one shared relationship entity among exact participants; this does **not** imply identical feelings, knowledge, trust or perception;
- `ROLE_ASYMMETRIC_SHARED` — one shared relationship entity with exact noninterchangeable participant roles;
- `DIRECTED_RELATION_RECORD` — only where an exact rule genuinely owns an objective directed relation; the reverse direction is absent unless separately generated.

A relationship kind such as marriage, romance, friendship, alliance, employer, caregiver, etc. is not inferred from labels or demographics. Concrete kind semantics must come from the exact registered relationship rule and are not globally enumerated by v1.

### 6.2 `V3ActorPerceivedRelationshipState`

```text
perceived_state_id
perceiver_actor_id
relationship_entity_id_or_counterpart_ref
relationship_rule_id / version
perceived_component_schema_ref
perceived_component_payload
causal_parent_refs[]
effective_from
superseded_by_ref | null
provenance_refs[]
state_hash
```

This is generated actor-specific relationship state, not objective shared truth. It may conflict with another participant's perceived state or with objective relationship state. No objective->perceived copy occurs automatically.

ADP-015 does not set `actor_accessible=true`. ADP-017 separately governs knowledge/accessibility/claim permission, and CAN-019 may later express only actor-safe components.

### 6.3 `V3HouseholdEntity`

```text
household_entity_id
household_rule_id / version
establishing_event_id
effective_from
dissolved_by_event_id | null
membership_fact_refs[]
shared_generated_context_refs[]
household_history_anchor_hash
provenance_refs[]
entity_hash
```

A household is a shared causal entity, **not a person**. It has membership and shared event/context history; it has no personality, Enneagram/type, belief, voice, single psyche, average orientation or compulsory demographic identity.

### 6.4 `V3HouseholdMembershipFact`

```text
membership_fact_id
household_entity_id
actor_id
membership_role_ref
established_by_event_id
effective_from
ended_by_event_id | null
source_relationship_or_family_refs[]
provenance_refs[]
fact_hash
```

Relationship != household membership. Parenthood != household membership. Child generation does not automatically create co-residence unless the exact household/generation rule explicitly emits a lawful membership effect.

### 6.5 `V3ParenthoodFact`

```text
parenthood_fact_id
parent_actor_id
child_actor_id
parenthood_role_ref
generation_event_id
effective_from
provenance_refs[]
fact_hash
```

The canonical W2 recursion requires two exact lineage parent actors for the base child-generation rule. `PARENT_1` and `PARENT_2` are neutral lineage slots, not gender/personality/biological stereotypes. Household/social caregiving roles remain separate facts and may have different cardinality where separately governed.

### 6.6 `V3GeneratedChildActorRef`

```text
child_actor_id
generated_entity_kind = ACTOR
generation_event_id
genealogy_scope_id
parenthood_fact_refs[]
initialization_state = GENERATION_COMPLETE_INITIALIZATION_PENDING
provenance_refs[]
actor_ref_hash
```

This record contains no personality/type/Enneagram, beliefs, memories, needs, class, religion, ethnicity, language, sex/gender, name or childhood events unless another separately accepted authority lawfully creates those facts. It is the stable identity boundary required so ADP-007 can initialize the child and ADP-020 can later derive independent `ACTOR(child_actor_id)` RNG streams.

## 7. Canonical event contracts and prospective history

Canonical event families are deliberately small:

### `V3RelationshipEvent`

Effect kinds:

- `RELATIONSHIP_ESTABLISHED`;
- `RELATIONSHIP_STATE_TRANSITIONED`;
- `RELATIONSHIP_ENDED`.

### `V3HouseholdEvent`

Effect kinds:

- `HOUSEHOLD_ESTABLISHED`;
- `HOUSEHOLD_MEMBER_JOINED`;
- `HOUSEHOLD_MEMBER_LEFT`;
- `HOUSEHOLD_DISSOLVED`.

### `V3GenealogyEvent`

Effect kind:

- `CHILD_GENERATED`.

A single `CHILD_GENERATED` event creates the new child actor ref and the two parenthood facts as effects. Parenthood does not require a duplicate event family. Optional household membership is a separately validated household effect, not an automatic side effect.

All relationship/household transitions are prospective. Ending a relationship, leaving a household or later changing family context never rewrites earlier relationship events, prior memberships, prior parent histories, the generation event, or already-generated child history.

Unchanged ticks produce no pseudo-events.

## 8. Relationship formation/evolution admission law

### 8.1 Formation

A positive relationship formation requires all of:

1. exact stable participant actor IDs;
2. each required participant is an already-generated V3 actor with a valid history anchor;
3. exact `DEVELOPMENT_ACTIVE` or other accepted phase permission required by the relationship rule;
4. exact relationship rule/version;
5. every rule-required ADP-009 position constraint supplied by exact generated fact, never demographics/prevalence;
6. exact ADP-010 encounter record(s) where the rule requires prior encounter;
7. an exact generated/admitted relationship-forming causal witness defined by the rule; co-presence/exposure alone is insufficient;
8. exact participant-role/directionality semantics;
9. candidate/admission integrity and, only if the rule is stochastic, an ADP-020 decision receipt;
10. no negative/forbidden/integrity blocker.

V1 supplies **no universal relationship probability, partner score, compatibility score, marriage probability, intimacy threshold or duration threshold**.

The base deterministic profile `V3REL_EXPLICIT_JOINT_FORMATION_V1` admits a relationship only from an exact rule-bound joint relationship-forming witness plus any declared encounter prerequisites. It consumes zero RNG draws.

### 8.2 Evolution and end

A relationship transition/end requires the exact prior relationship entity/state plus an exact generated/admitted transition witness under a versioned rule. The prior state remains immutable history.

No duration, conflict count, tone, transcript frequency, one actor's perception or V2 session posture automatically changes the objective relationship.

### 8.3 Reciprocity and asymmetry

`JOINT_SHARED` means the objective shared relationship entity exists. It does not mean equal desire, trust, commitment, knowledge, perception or behavior.

One participant's `V3ActorPerceivedRelationshipState` never creates or changes another participant's perceived state. One-sided attachment, belief, attraction, hostility or presumed intimacy never creates reciprocal relationship truth. If a rule establishes asymmetric roles, those roles are explicit and noninterchangeable.

Two contradictory actor-perceived states may coexist indefinitely until causal transitions change them. ADP-015 does not average, vote or synthesize a compulsory shared subjective truth.

## 9. Household law

Household formation is a separate causal admission from relationship formation. A relationship may exist without a household; a household may change membership without ending every relationship.

`V3HH_EXPLICIT_FORMATION_MEMBERSHIP_V1` requires an exact generated/admitted household-forming witness and exact participant/membership effects. It is deterministic and consumes zero RNG draws.

No cohabitation, shared address, marriage label, parenthood, economic similarity, locality or session/application context creates household membership without an exact rule.

A household may reference exact shared constraints/resources/events and exact member actor refs. Those refs remain disaggregated. A household summary/checkpoint may cache them for performance but is never a merged actor state and cannot become child personality authority.

Household/family binding changes are generated-life refresh causes. They may trigger prospective ContextResolver re-resolution through the separately governed generated-life requery seam; resolver output never rewrites the household or actor history.

## 10. Child-generation law

### 10.1 Prerequisites

The base v1 child-generation profile `V3GEN_EXPLICIT_CHILD_GENERATION_V1` requires:

1. exactly two stable independently generated parent actor refs in neutral lineage slots `PARENT_1` and `PARENT_2`;
2. exact immutable parent-history anchor refs for both parents at the generation decision;
3. exact relationship and/or household causal-context refs required by the registered generation rule;
4. an exact generated/admitted generation causal trigger/witness under that rule;
5. any required actor phase, organismic/material or position constraints supplied by their own accepted authorities;
6. exact genealogy candidate identity and admission receipt;
7. ADP-020 receipt only if an explicitly governed stochastic extension is used;
8. no negative, unknown-required, missing-authority or integrity blocker.

ADP-015 v1 defines **no universal age floor, fertility window, sex/gender pairing, fecundity rate, conception probability, parity limit, partner-age gap, birth spacing, desired family size, or demographic fertility weight**. If a concrete generation rule needs such semantics and no accepted authority supplies them, child generation is missing/deferred rather than guessed.

The base explicit-trigger profile itself is deterministic and consumes zero RNG draws.

### 10.2 Acyclic child identity

Identity order is:

```text
canonical genealogy decision outcome
-> derive generation_event_id
-> derive child_actor_id from generation_event_id
-> derive two parenthood_fact_id values from generation_event_id + child_actor_id + parent slot
-> assemble final event with child/parenthood refs
-> hash final records
```

`generation_event_id` is content-addressed from authority/registry/rule versions, genealogy scope, exact parent actor IDs, exact parent-history anchors, exact relationship/household prerequisite refs, effective time, exact generation trigger refs, candidate/selection receipt identity and canonical occurrence index. It does not depend on child display fields.

`child_actor_id` uses domain-separated deterministic identity:

```text
SHA256("RAWLSING\0ADP-015\0CHILD_ACTOR_V1\0" || generation_event_id)
```

Random UUID, random integer suffix, name, sex/gender, country, surname, parent order in a mutable container, filesystem order or wall clock may not determine child identity.

### 10.3 Independent-parent-history law

The generation event records **two exact parent history anchors**, not one household aggregate. Parent histories remain independently replayable causal DAG branches. A parent's later development never retroactively changes the historical anchor used for the child's generation event.

A child may later be causally affected by exact parent/relationship/household history only through the child runtime's own accepted rules. No parent state is copied merely because of lineage.

The child receives a new ADP-020 actor scope from `child_actor_id`; it never inherits either parent's mutable random stream. Sibling generation therefore cannot perturb an existing child's actor RNG lineage.

### 10.4 Initialization boundary

After `CHILD_GENERATED`, the new actor is `GENERATION_COMPLETE_INITIALIZATION_PENDING`. ADP-015 stops there.

ADP-007 owns initial actor-state generation. ADP-009 owns any structural position facts it later generates. ADP-010 owns the child's encounters/exposures. No historical V2 “inherit household identity and fill defaults” path is retained as terminal authority.

## 11. Candidate-set and RNG law

Every ADP-015 stochastic decision must begin with an exact finite lawful candidate set whose semantics were created by ADP-015's registered rule, never by demographics or RNG.

Candidate record:

```text
V3RelationshipGenealogyCandidate {
  candidate_id,
  candidate_replay_hash,
  decision_kind,
  rule_id / version,
  participant_or_parent_refs[],
  causal_witness_refs[],
  relationship_household_refs[],
  eligibility_receipt_hash,
  weight_units | null,
  provenance_refs[]
}
```

ADP-020 binding:

- relationship/household multi-actor decisions use exact owner-created `JOINT` scope IDs;
- child-generation stochastic decisions use exact owner-created `GENEALOGY` scope IDs;
- actor-specific downstream decisions after child ID creation use `ACTOR(child_actor_id)`.

Reserved static streams for future explicitly stochastic rules:

```text
v3.causal.adp015.relationship_selection
v3.causal.adp015.household_selection
v3.causal.adp015.child_generation
```

V1 base profiles are deterministic and consume zero draws. A future registered stochastic rule may use only exact ADP-020 operations with complete probability/weight authority. ADP-015 supplies no universal weights or probabilities.

Multiple lawful candidates without exact deterministic precedence, explicit equiprobability or governed integer weights return `RELATIONSHIP_GENEALOGY_SELECTION_AUTHORITY_UNBOUND`; no draw occurs.

Demographic similarity, geographic proximity, shared religion/class/ethnicity, parent age, survey prevalence, narrative plausibility and LLM judgment may not be normalized into partner/fertility weights.

## 12. Valid-empty, unknown, missing and failure behavior

Canonical decision/status vocabulary includes:

- `RELATIONSHIP_FORMED`;
- `RELATIONSHIP_TRANSITION_COMMITTED`;
- `RELATIONSHIP_ENDED`;
- `HOUSEHOLD_FORMED`;
- `HOUSEHOLD_MEMBERSHIP_COMMITTED`;
- `HOUSEHOLD_DISSOLVED`;
- `CHILD_GENERATED`;
- `RELATIONSHIP_CANDIDATES_VALID_EMPTY`;
- `HOUSEHOLD_CANDIDATES_VALID_EMPTY`;
- `CHILD_GENERATION_VALID_EMPTY`;
- `RELATIONSHIP_NONOCCURRENCE`;
- `CHILD_GENERATION_NONOCCURRENCE`;
- `RELATIONSHIP_INPUT_UNKNOWN`;
- `HOUSEHOLD_INPUT_UNKNOWN`;
- `GENEALOGY_INPUT_UNKNOWN`;
- `RELATIONSHIP_RULE_NOT_GOVERNED`;
- `HOUSEHOLD_RULE_NOT_GOVERNED`;
- `CHILD_GENERATION_RULE_NOT_GOVERNED`;
- `RELATIONSHIP_DEFERRED_UNBOUND_INPUT`;
- `HOUSEHOLD_DEFERRED_UNBOUND_INPUT`;
- `GENEALOGY_DEFERRED_UNBOUND_INPUT`;
- `RELATIONSHIP_NEGATIVE_AUTHORITY`;
- `HOUSEHOLD_NEGATIVE_AUTHORITY`;
- `GENEALOGY_NEGATIVE_AUTHORITY`;
- `RELATIONSHIP_GENEALOGY_SELECTION_AUTHORITY_UNBOUND`;
- `AMBIGUOUS_SAME_TIME_RELATIONSHIP_TRANSITION`;
- `BLOCKED_ENCOUNTER_TO_RELATIONSHIP_SHORTCUT`;
- `BLOCKED_DEMOGRAPHIC_PARTNER_INFERENCE`;
- `BLOCKED_RECIPROCITY_INFERENCE`;
- `BLOCKED_HOUSEHOLD_PERSONA_COLLAPSE`;
- `BLOCKED_PARENT_OR_CHILD_TYPE_INFERENCE`;
- `BLOCKED_V2_TO_V3_RELATIONSHIP_PROMOTION`;
- `BLOCKED_OUTSIDE_ADP015_JURISDICTION`;
- `INTEGRITY_FAILURE`.

`VALID_EMPTY` is a successful ruled evaluation with zero candidates/outcomes. It creates no filler relationship, household or child and consumes zero RNG draws.

`UNKNOWN` is not negative authority. `MISSING_RULE` is not nonoccurrence. `NONOCCURRENCE` never fabricates an event. One parent's unknown perception does not erase an objective relationship record, and an objective relationship does not fill an unknown perceived state.

## 13. Recursive provenance and replay

Every relationship/household/genealogy event must preserve enough immutable lineage to replay without mutable lookup:

- authority ID/version and registry hash;
- exact rule ID/version/content hash;
- actor/generated-entity IDs;
- exact participant roles and directionality;
- exact ADP-010 encounter refs where required;
- exact ADP-009 position refs where required;
- exact generated/admitted causal witness IDs/hashes;
- exact prior relationship/household entity/history hashes;
- parent actor history anchors at generation time;
- relationship/household prerequisite refs;
- candidate-set ID/hash and selection receipt;
- ADP-020 root/scope/stream/decision receipts where stochastic;
- effective causal time and scheduler invocation/order refs;
- generated event/fact/entity IDs and hashes;
- generated-binding refresh receipts where later canonicalized;
- integrity/provenance refs.

Replay never follows mutable `latest`, current parent state, filesystem order, transcript text or current household summary in place of the historical refs stored with the event.

Recursive genealogy is a finite causal DAG. A parent actor may itself have a genealogy event and parent refs. A child may later become a parent. Future descendant events cannot alter earlier ancestor events or IDs.

## 14. Hostile fixture court

At minimum, implementations must prove:

1. unrelated co-presence -> no relationship;
2. exact ADP-010 encounter without relationship-forming witness -> no relationship;
3. exposure without relationship rule -> no relationship;
4. demographic/religious/class similarity -> no partner candidate authority;
5. one-sided attachment/perception -> no reciprocal truth;
6. one actor says “we are close” -> other actor's perceived state unchanged;
7. contradictory parent/partner views coexist without averaging;
8. objective relationship may exist while one actor's perceived state is unknown;
9. relationship does not automatically create household;
10. shared address/application context does not create household membership;
11. household entity has no personality/type/voice;
12. relationship end preserves earlier history;
13. household departure preserves earlier membership history;
14. two independently developed parents remain separate DAG branches at child generation;
15. child generation creates a new actor ref, not a parent-state blend;
16. child receives no Enneagram/type/personality from either parent;
17. shared parent ethnicity/religion/class row cannot directly populate child identity;
18. parent-type inference path is rejected;
19. missing fertility/generation rule -> no child;
20. valid-empty child generation -> zero child events and zero RNG draws;
21. multiple child/partner candidates without selection authority -> no draw/no winner;
22. ungoverned fertility probability -> fail closed;
23. deterministic explicit generation trigger -> child generation with zero RNG draws;
24. child actor ID stable under replay and independent of display name/gender;
25. sibling generation does not perturb prior child's actor RNG stream;
26. V2 affectionate/hostile wording -> no V3 relationship transition;
27. transcript/session persistence -> no trust/intimacy/relationship fact;
28. child household membership is absent unless explicitly established;
29. later parent state change cannot rewrite generation-time parent history anchors;
30. same-time incompatible relationship transitions without precedence -> fail closed;
31. fixture-only synthetic parent/child records cannot leak into production truth;
32. unchanged scheduler tick creates no pseudo relationship/household/genealogy event.

## 15. Governing-Spirit court

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`.

Genuine lawful ambiguity: represent a family/household as one convenient merged “family profile/persona,” or as a shared causal entity whose membership/history references independently generated actors and permits actor-specific contradictory/perceived states.

Chosen design: **shared relationship/household entities + independent actor histories + perspective-bound perceived relationship states + explicit genealogy events**.

Tie-break principles:

- genealogy and relationships as histories of generated persons rather than demographic synthesis;
- contradiction and multiplicity without forced coherence;
- mediation rather than structure/demography -> family biography;
- actor opacity rather than reciprocity/knowledge inference;
- dynamic history over static family classification;
- causal provenance and recursive replay;
- generative openness for divergent parents/children;
- minimum sufficient machinery without a household super-person.

The Governing Spirit supplied no partner choice, fertility rate, parent age, sex/gender rule, relationship kind, parenting style, child trait, type, belief, or desired family outcome.

## 16. Consumer release sufficiency

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT_FOR_MUST_015_BLOCKER`.

ADP-015 fully specifies the relationship/household/genealogy semantic authority required by RA-R00 without inventing missing fertility or initialization semantics.

It does **not** globally release `V3-P9` or `V3-P13`. At minimum:

- same-wave ADP-007 actor initialization is not consumed and remains independently adjudicated;
- `EXT-007` / standalone V558 repository-resolver production and implementation packets remain independent gates;
- exact future resolver generated-life requery wire canonicalization remains separate;
- any future concrete stochastic fertility/partner-selection rule must provide its own exact parameters under this registry and ADP-020 rather than use a legacy default.

No production implementation is authorized by this authority file.

## 17. Final token

`ADP_015_V3_RELATIONSHIP_GENEALOGY_AUTHORITY = PASS`
