# ADP-007 — V3 Actor Initialization Authority

**Assignment:** W2-02 — ADP-007 / V3 Actor Initialization Authority  
**Repository:** `maidiu/rawlsing`  
**Assigned branch:** `agent/vozhd-dva-w2-adp-007-v3-initialization`  
**Exact launch base:** `fe52ca60ed00650b0a7b5bf77bab8ac40d53f4d8`  
**RA-R00 item:** `MUST-007 / ADP-007`  
**Authority ID:** `V3_ACTOR_INITIALIZATION_RULE`  
**Authority version:** `1.0.0`  
**Initial-fact registry:** `V3_INITIAL_FACT_RULE_REGISTRY@1.0.0`  
**Owner:** `V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE`  
**Mode:** authority creation only; no production code; no V3 implementation; no architecture reopening  
**Verdict:** `PASS`

## 0. Binding holding

Actor initialization creates a **historically accountable beginning**, not a template person.

The canonical sequence is:

```text
lawful generation subject
+ exact Phase-A resolved context/provenance
+ exact lawful nonactor generation inputs
        |
        | ADP-007: deterministic actor entity creation
        v
stable actor_id + ACTOR_ENTITY_CREATED
        |
        | ADP-009 may establish any lawfully required initial structural positions
        | other separately accepted semantic owners may supply explicitly authorized initial facts
        v
sparse admitted initial facts/refs
        |
        | ADP-007: activation court
        v
ACTOR_ACTIVATED
+ immutable sparse initial checkpoint
        |
        | ADP-008 phase consequence
        v
V3DP_DEVELOPMENT_ACTIVE
```

The constitutional noncollapse is:

```text
PHASE_A_RESOLVED_CONTEXT
!= GENERATED_ACTOR_FACT
!= LIVED_HISTORY
!= ACTOR_MEMORY
!= ACTOR_KNOWLEDGE
!= PERSONALITY
!= ATTRACTOR_OR_TYPE

DEMOGRAPHIC_OR_STRUCTURAL_INPUT
!= PSYCHOLOGICAL_INITIAL_STATE

MISSING_INITIAL_VALUE
!= MIDPOINT
!= AVERAGE
!= "NEUTRAL PERSON"

ACTOR_ENTITY_CREATION
!= STRUCTURAL_POSITION_GENERATION
!= ENCOUNTER_OR_EXPOSURE
!= RELATIONSHIP_OR_GENEALOGY
```

Initialization may be **sparse**. An actor may lawfully activate with zero optional domain-initial facts when no accepted rule requires them. Unknown, missing, negative, deferred and valid-empty states remain typed rather than being filled by defaults.

`V3_INITIAL_FACT_RULE_REGISTRY@1.0.0` contains **zero generic domain-initial-fact rules**. The only universal ADP-007 operations are actor entity creation and activation. No personality, type, Enneagram, wound, framework, need profile, relationship, memory, belief, class, religion, ethnicity, gender, language, capacity vector, vitality value, or other domain value is synthesized merely because historical code once put such a field into `BackboneState`.

---

## 1. Governing authority and direct dependencies

### 1.1 W2 common law

The W2 launch register was read at exact base `fe52ca60ed00650b0a7b5bf77bab8ac40d53f4d8`. It binds this cell to authority creation only, forbids sibling-W2 authority consumption, and requires explicit missing/unknown/valid-empty behavior, provenance/replay, hostile fixtures, Governing-Spirit review and consumer sufficiency.

The whole-machine architecture remains closed.

### 1.2 Accepted direct dependencies

This authority consumes only the following accepted direct semantic dependencies:

1. **ADP-008 / `V3_DEVELOPMENTAL_PHASE_RULE@1.1.0`**
   - universal base phases are only `V3DP_GENERATION_PENDING` and `V3DP_DEVELOPMENT_ACTIVE`;
   - ADP-007 owns actor activation and emits its exact event/receipt;
   - ADP-008 owns the phase-state consequence of that activation;
   - no childhood/adolescent/adult/personality phase taxonomy may be inferred.

2. **ADP-009 / `V3_STRUCTURAL_POSITION_GENERATION_MOBILITY_RULE@1.0.0`**
   - ADP-009 begins from an already-created actor with stable `actor_id`;
   - structural prior and prevalence do not create actor position;
   - ADP-009, not ADP-007, owns initial structural-position candidate admission, selection, facts and position events;
   - ADP-007 may preserve returned ADP-009 fact/event refs in the initial checkpoint without re-owning their meaning.

3. **ADP-020 / causal randomness authority `1.0.0`**
   - randomness resolves only already-lawful possibilities;
   - every causal stochastic operation uses a named `v3.causal.*` stream, stable scope, exact candidate/parameter identity, rule/version and replay receipt;
   - no unnamed/global RNG, wall clock, PID, filesystem order, mutable `latest`, library default state or unrecorded model entropy may affect initialization;
   - empty or underauthorized candidate sets consume no draw.

No W2 sibling return was used as authority. In particular, this result does not consume the parallel ADP-015 or CAN-006 results.

### 1.3 Relevant closed architecture

Binding closed architecture establishes:

- V3 receives stage-blind `ResolvedStructuralContext`, not raw V553–V558 directories;
- structural prior is not actor fact;
- Phase A may leave position-conditioned material unresolved;
- V3 generated facts and events are replayable, immutable history;
- parents, relationships and households are generated histories rather than demographic averages;
- no survey, birth state or structural object may directly assign Enneagram-like type;
- missing authority blocks mutation instead of licensing generic psychology.

---

## 2. Required historical archive verification

Required archive: `Rawlsing_code_bundle_staging.zip`.

```text
expected SHA256:
953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086

directly computed SHA256:
953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086

verdict: EXACT_MATCH
ZIP entries: 13,138
```

Recovered V3/V2/server material is continuity and authority-recovery evidence only. Historical V5/DDM has **zero authority** over current V550+.

Current repository search at the W2 launch base found no canonical `V3_ACTOR_INITIALIZATION_RULE` and no current `backbone_state_from_identity` implementation. The initialization rule is therefore genuinely missing authority rather than a current implementation to bless unchanged.

---

## 3. Recovered initialization court

### 3.1 Directly inspected recovered sources

| Historical source | SHA256 | Disposition |
|---|---|---|
| `v3/core/state.py` | `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2` | **ADAPT CONTAINER / REJECT DEFAULT CONTENT** |
| `v3/core/generation_integrity.py` | `5265aac2fda4d6e6ac62927353518045f215d7d1916930e19e980b6d77eff214` | **ADAPT PROVENANCE/FAIL-CLOSED DIAGNOSTICS** |
| `v3/core/year_record.py` | `4bbd7518a6ec8bc8dd22758a2f9e876882253dfd59021a998a6d541b23e5cfc2` | **ADAPT CONTENT-HASH/REPLAY PATTERN** |
| `v3/io/identity_from_v2.py` | `37d5dc7126c76f965c9e0ba186676434e4f4bf37d5769a3283147ecfee78e3ea` | **REMOVE AS TERMINAL IDENTITY AUTHORITY** |
| `v3/io/identity_to_backbone.py` | `cb29c9595ac495c3b69b693d4c58a278e9ef1f63a7a8917d8e407920fbd3bdda` | **REPLACE WITH SPARSE RULE-COURTED INITIALIZATION** |
| `v3/io/calibration_from_identity.py` | `dde9fbaf91d403f6086015bdc6492ebcbf890a8a16d992e53e29345f7c931770` | **REMOVE STRUCTURE/DEMOGRAPHY -> ACTOR CALIBRATION SHORTCUT** |
| `v3/io/seed_frameworks.py` | `1d6525207f30591a6d67cb8b79521102fb40848fc9001b96d35e864d147a7582` | **REMOVE DEMOGRAPHIC -> PSYCHE / INVENTED HISTORY** |
| `v3/io/seeds.py` | `1b39139b7430e5e9611851fdbf367c4bee0db0889c2a489c7502f13df8031ed0` | **REPLACE RNG MECHANISM WITH ADP-020; PRESERVE REPRODUCIBILITY INTENT** |
| `v3/io/parent_baseline_from_behavior.py` | `4e5be6448a5b76c413492ec2a83b62d9e9a2247ce131a094727d974a17cf750b` | **REMOVE FROM ADP-007; PARENT/CHILD CAUSALITY BELONGS ELSEWHERE** |
| `v3/tests/test_v5_identity_hydration_attaches_refs_not_beliefs.py` | `77a84634c6520d7310034f7be86c41e8980a671f38af28ef5a52721229bce43e` | **PRESERVE REFS-NOT-BELIEFS DIRECTION** |
| `v3/tests/test_distribution_smoke.py` | `ce75862943a1cd6b25c8545371b7bfb3fc0ed9618d9b280740f3e2cfc4403b45` | **COMPATIBILITY EVIDENCE FOR DIVERGENCE/REPLAY ONLY** |
| `v3/tests/fixtures/identity_minimal.json` | `ef7008ac0d83e7690bd89e96ec683d25d3b784806857a799da2978ba7aa35673` | **LEGACY FIXTURE ONLY; NO DEFAULT IDENTITY AUTHORITY** |
| `v2/identity_generator.py` | `e7bfdee70312e5b9d2e53b29de2c0fabdb4c528ef2c211517c7f81fcd073cc3e` | **REMOVE AS V3 ACTOR-TRUTH OWNER** |
| `v2/PROBABILISTIC_IDENTITY_PIPELINE.md` | `ad2bb0cc966033842a509f760443e1cc33164b56449fd5593604cdfbb194c1b6` | **DISTRIBUTION/CONSTRAINT CONTINUITY ONLY** |
| `v2/IDENTITY_SAMPLING_STRATEGY.md` | `678ed046a23118bccfbd76c4b7a7f3a594d382c4eb4bebc76b474d2f666234ae` | **DISTRIBUTION/CONSTRAINT CONTINUITY ONLY** |
| `v2/COMPLETE_IDENTITY_PIPELINE.md` | `b6264933e9b25f36e5066c687352c9f6b5c4dca699bd089f04df068a7a7b4b0d` | **REMOVE MONOLITHIC PERSON-GENERATION OWNERSHIP** |
| `v2/STRUCTURAL_PERSONA_SCHEMA.md` | `c13a5c446d8b4d92425a8cf26f41aa54c7c08ddc5d0599f4211a73414c361c7a` | **NO STRUCTURAL->PERSONA INITIALIZATION AUTHORITY** |
| `v2/ENNEAGRAM_EMERGENCE_SYSTEM.md` | `95f8876926dda96a33c36925aedacee65645c74863cff68241e6b67457f819ab` | **PRESERVE NO-TYPE-AT-BIRTH INTENT ONLY** |
| `server/generation/simulation.py` | `5d68ffe3bc6902dc60b90625443a03127cf0d04b4eed4327270a3a0226bc78d1` | **REPLACE GENERATION ORCHESTRATION; NO SEMANTIC INITIALIZATION AUTHORITY** |
| `server/routes/start.py` | `01fb7e1f3d5c821280bdfdd7ae83edc3270f733a2594673b8ff151961d85f43f` | **APPLICATION START/SESSION EVIDENCE ONLY** |
| `server/routes/discovery.py` | `c58e940cc605d311d9aba877fe42b7b1086b1793183ee78bd4af56219bb5b910` | **APPLICATION START/SESSION EVIDENCE ONLY** |

### 3.2 Recovered mechanism dispositions

#### Typed `BackboneState` / state containers

**ADAPT.** A typed materialized state/checkpoint is useful. The recovered state constructor, however, silently creates semantically populated objects. Canonical initialization must permit sparse/absent domain state and preserve exact source authority.

#### Universal `50` defaults and a “neutral” person

**REMOVE / REJECT.** Recovered fields default to `50.0` across capacity, psychological capacity, wound sensitivity, alienation, registers, magnets, style traits, stratum strength and other domains. `norm_center="middle"` and default coping channels such as `withdraw` / `intellectualize` likewise manufacture a person.

No recovered midpoint, average or ordinary-person baseline has terminal authority.

#### `randomized_seed()`

**COMPATIBILITY_ONLY / REPLACE RNG.** It demonstrates historical intent that different seeds produce divergent actors and the same seed reproduces a run. Its arbitrary uniform `0..100`/subrange distributions are not semantic authority. ADP-020 replaces its `random.Random(seed)` state with named causal streams and exact decision receipts.

#### V2/V3 identity sampling

**REMOVE AS TERMINAL AUTHORITY.** Historical country sampling uses approximate populations, square-root weighting, a default population for absent countries, uniform fallback and module-global randomness. The V2 pipeline then probabilistically chooses ethnicity, SES, religion/language, gender and age, including fallback values and random IDs.

The useful continuity is only this abstract form:

```text
explicit governed distribution
+ exact constraints
+ named causal RNG
-> one lawful generated fact
```

No recovered distribution, fallback or identity chain is automatically governed under ADP-007.

#### `identity_to_backbone`

**REPLACE.** The recovered bridge maps class to money/debt/job insecurity, urbanicity to mobility, minority status to legitimacy, seeds universal autonomy/safety drives, practices, opportunity proxies, wounds, frameworks, cracks, magnets and family/child assumptions. It also defaults absent identity to values such as `middle`, `city`, `dominant`, `female` and `Persona`.

This is exactly the prohibited structure/demography/default-person shortcut.

#### Framework/crack seeding

**REMOVE.** Recovered code derives faith, class, minority and age frameworks, then manufactures crack `origin_year` values in early childhood/adolescence from the current age/year. This retroactively invents developmental history and is forbidden.

#### Parent baseline / child model

**REMOVE FROM ADP-007.** Recovered parent-behavior code averages parent fields, uses `50` defaults and derives child expectations/rules. Another recovered path fills missing child assumptions with claims such as adults being fair or home being safe. Parent/child causal semantics require separately governed generated parent/relationship/genealogy history and may not be created here.

#### V5/upstream attachment refs

**PRESERVE BY REFERENCE.** The recovered test that attaching upstream runtime refs should not mutate identity/backbone content captures a useful direction: upstream structural/context refs remain provenance/constraint inputs rather than actor belief or psyche. The historical baseline content itself is not preserved.

#### Generation integrity diagnostics

**ADAPT.** Preserve explicit source refs, fallback-used flags, impacted-field records and fail-closed status. Remove wall-clock time from semantic identity/replay and remove any assumption that ethnicity/religion/language are mandatory to produce a “complete person.”

#### Snapshot/content hashing

**ADAPT.** Stable canonical hashes and immutable initial checkpoints are required. Python-specific `default=str` serialization is compatibility evidence only; terminal serialization must be explicitly canonical/versioned.

---

## 4. Jurisdiction

### 4.1 ADP-007 owns

ADP-007 owns exactly:

1. admission of a stable prospective-generation subject into V3 actor creation;
2. deterministic `actor_id` derivation and collision/integrity law;
3. `ACTOR_ENTITY_CREATED` event semantics;
4. the actor-created / pending-activation shell state;
5. the generic `V3_INITIAL_FACT_RULE_REGISTRY` contract;
6. admission of optional initial domain facts **only** through explicitly registered semantic authority;
7. initialization constraint evaluation and missing/unknown/negative/deferred behavior;
8. handoff to ADP-020 when a registered initial-fact rule explicitly authorizes stochastic choice;
9. intake-by-reference of ADP-009 initial position facts without re-owning them;
10. `ACTOR_ACTIVATED` event semantics;
11. construction/sealing of the immutable sparse initial actor checkpoint;
12. exact activation receipt supplied to ADP-008;
13. initialization provenance, replay, idempotency and no-retroactive-rewrite law.

### 4.2 ADP-007 does not own

ADP-007 does **not** own:

- structural-prior semantics or ContextResolver selection;
- actor structural-position generation/transition/mobility — ADP-009;
- opportunity, encounter or exposure realization — ADP-010;
- relationship/household/family/genealogy semantics — ADP-015;
- developmental-phase segmentation — ADP-008;
- RNG seed/stream/sampler mechanics — ADP-020;
- material/organismic/vitality, need/expectation/striving, framework/wound/practice, response, rupture, memory, knowledge, orientation or attractor semantics owned by their own authorities;
- personality, type, Enneagram or persona identity at birth;
- a global human demographic distribution;
- prevalence-to-actor probability conversion;
- a caller assertion becoming generated actor truth merely because it is known to the application;
- encounters, relationships, memories, beliefs or childhood history needed only to make a plausible character;
- V2 expression/session/render semantics.

### 4.3 Exact RA-R00 consumers

`MUST-007` is consumed by:

- `V3-P1`;
- `V3-P3`;
- `V3-P4`;
- `V3-P9`.

This authority satisfies only their ADP-007 semantic dependency. Every other MUST/CAN/EXT dependency remains binding.

---

## 5. Initialization input contract

Canonical input is terminally equivalent to:

```text
V3ActorInitializationRequest {
    initialization_request_id,
    initialization_rule_id,
    initialization_rule_version,
    causal_run_id,

    generation_subject_ref,
    generation_subject_hash,
    generation_subject_owner_authority_id,
    generation_subject_owner_authority_version,

    requested_effective_time,

    phase_a_context_ref,
    phase_a_context_hash,
    phase_a_context_status,
    phase_a_selection_record_refs[],
    phase_a_coverage_fidelity_ref,

    lawful_nonactor_generation_input_refs[],
    requested_initial_fact_rule_refs[],
    unresolved_position_requirement_refs[],

    root_seed_record_ref | null,
    integrity_state
}
```

### 5.1 `generation_subject_ref`

A generation subject is an immutable pre-actor subject/request identity. It may be a root generation request or, in future use, an exact subject created by another accepted causal owner.

It is **not** itself the actor, a personality, a household, or an actor fact.

The ref must provide stable identity, owner authority/version, content hash and any lawful causal-parent event refs. Missing or mutable generation-subject identity blocks actor creation.

### 5.2 Phase-A context

Phase-A context is an **input constraint/provenance surface**.

It may:

- supply exact structural/context refs to a registered candidate/constraint rule;
- expose unresolved generated-position requirements for ADP-009;
- constrain a separately governed initialization distribution;
- preserve explicit negative, unknown, denied, noncomparable or valid-empty context.

It may never by itself assert:

- actor membership in class/sect/religion/party/institution/household/family;
- actor experience of a pressure;
- actor belief, memory, orientation, wound or framework;
- actor personality/type;
- an encounter or relationship.

### 5.3 Lawful nonactor generation inputs

These are source-bound facts about the **generation request, prospective-generation subject, causal run or environment**, not actor facts.

Every ref must preserve:

- source authority/version;
- subject binding;
- exact value/hash;
- effective time/scope;
- initialization-use permission where required;
- uncertainty/negative state.

A nonactor input can constrain or nominate a candidate only when an exact registered initialization rule says so. Field-name similarity or “obvious” copying into the actor is forbidden.

---

## 6. Deterministic actor identity and entity creation

### 6.1 Stable actor ID

ADP-007 v1 authorizes no stochastic actor-ID creation.

A conforming deterministic identity is:

```text
actor_id = SHA256(
    "RAWLSING\0ADP-007\0V3_ACTOR_ID_V1\0"
    || canonical_json({
         causal_run_id,
         generation_subject_ref,
         generation_subject_hash
       })
)
```

A display name, geography, demographics, wall clock, random UUID, process order or RNG draw does not participate in actor identity.

Replaying the same verified generation subject under the same causal run returns the same actor identity. The same actor identity paired with a different generation-subject hash is `ACTOR_ID_COLLISION_OR_SUBJECT_REUSE_INTEGRITY_FAILURE`.

### 6.2 `ACTOR_ENTITY_CREATED`

The first ADP-007 event creates only the stable actor entity/shell.

Required semantic fields:

```text
V3ActorInitializationEvent {
    initialization_event_id,
    event_kind = ACTOR_ENTITY_CREATED,
    actor_id,
    causal_run_id,
    effective_time,
    generation_subject_ref/hash,
    causal_parent_event_refs[],
    noncausal_authority_provenance_refs[],
    phase_a_context_ref/hash,
    authority_id/version,
    rule_id/version,
    pre_state_hash,
    event_hash,
    integrity_state
}
```

For a root actor, `causal_parent_event_refs[]` may lawfully be empty. An initial condition is not converted into a fake prior event.

After this event:

```text
actor_entity_state = CREATED_PENDING_ACTIVATION
ADP-008 base phase = V3DP_GENERATION_PENDING
```

The actor has a stable identity but no implied psyche, history, position, relationship, memory or biography.

This created shell is sufficient for ADP-009 to run actor-scoped `INITIAL_BINDING` position courts.

---

## 7. Initial fact registry and fact admission

### 7.1 Registry v1

```text
V3_INITIAL_FACT_RULE_REGISTRY@1.0.0 {
    registered_domain_initial_fact_rules = []
}
```

`VALID_EMPTY` is intentional.

Actor existence/entity creation and activation are base ADP-007 semantics, not entries in the optional domain-fact registry.

A future registered domain-initial-fact rule must define:

```text
V3InitialFactRule {
    initial_fact_rule_id,
    initial_fact_rule_version,
    semantic_fact_kind,
    semantic_owner_authority_id,
    semantic_owner_authority_version,
    actor_fact_schema_ref,
    exact_consumers[],
    allowed_source_classes[],
    allowed_distribution_authority_refs[],
    constraint_specs[],
    required_or_optional,
    explicit_absence_semantics | null,
    deterministic_precedence | null,
    stochastic_selection_contract | null,
    effective_time_rule,
    provenance_requirements[],
    replay_requirements[],
    semantic_ceiling,
    rule_hash
}
```

No implementation/config row creates a rule merely by existing.

### 7.2 Domain semantic ownership

ADP-007 owns **initialization admission and historical placement**, not the domain meaning of every initial fact.

A domain fact may be generated at initialization only when its semantic owner explicitly authorizes:

- the fact kind;
- the source classes;
- the value/candidate semantics;
- any distribution or quantity semantics;
- initialization-time use.

Absent that authority, the field stays missing/unknown/valid-empty. ADP-007 does not invent a generic value domain.

### 7.3 `V3InitialGeneratedFact`

When a registered rule succeeds, emit a fact terminally equivalent to:

```text
V3InitialGeneratedFact {
    initial_fact_id,
    actor_id,
    semantic_fact_kind,
    semantic_owner_authority_id/version,
    initialization_authority_id/version,
    initial_fact_rule_id/version,
    assertion_kind,
    canonical_value_or_target_ref,
    effective_from,
    source_candidate_ref/hash,
    source_context_or_generation_input_refs[],
    constraint_receipt_refs[],
    rng_decision_receipt_ref | null,
    establishing_entity_event_ref,
    provenance_refs[],
    fact_hash,
    integrity_state
}
```

`assertion_kind` may be positive or explicit absence only if the registered semantic owner actually defines that absence. Empty/missing input never silently becomes an explicit negative fact.

---

## 8. Structural-position handshake

ADP-007 and ADP-009 remain noncollapsed.

After `ACTOR_ENTITY_CREATED`, ADP-007 may pass:

- stable `actor_id`;
- exact Phase-A context/SelectionRecord refs;
- exact unresolved generated-position requirement refs;
- exact initialization effective time;
- other lawful constraint refs

to ADP-009.

ADP-009 alone returns `V3StructuralPositionFact` / position event refs or its typed missing/unknown/deferred/negative outcomes.

ADP-007 may preserve those exact refs in activation/checkpoint state.

It may not:

- synthesize a position if ADP-009 returns none;
- convert Phase-A prevalence to an actor position;
- convert an unresolved position requirement to “middle,” “dominant,” “none,” or another convenience value;
- reinterpret a generated position as personality, belief or self-understanding.

There is **no universal ADP-007 rule requiring every possible structural-position dimension to resolve before activation**. If a future initialization rule requires an exact position prerequisite, that requirement must itself be explicit and versioned. Otherwise unresolved position material remains unresolved.

Phase-B V558 binding/requery is a separate contract and is not created here.

---

## 9. Distribution, constraint and RNG law

### 9.1 No built-in demographic distribution

ADP-007 v1 defines no canonical distribution for:

- country;
- region;
- ethnicity;
- class;
- religion;
- language;
- sex/gender;
- age;
- household/family;
- capacity;
- psychological state;
- any personality/type field.

Recovered WVS/Factbook/Joshua Project/EPR/WID sampling and approximate-population formulas are historical evidence only.

### 9.2 Governed distribution input

A distribution may be used only when a separately accepted semantic authority provides a record terminally equivalent to:

```text
GovernedInitializationDistributionRef {
    distribution_id,
    distribution_version,
    semantic_owner_authority_id/version,
    target_initial_fact_rule_id,
    scope,
    effective_time,
    candidate_ids[],
    candidate_replay_hashes[],
    weight_or_probability_contract | null,
    source_evidence_refs[],
    negative/unknown coverage state,
    distribution_hash
}
```

Raw prevalence/frequency is not such a record.

### 9.3 Constraint result states

Initialization constraints return exactly:

- `SATISFIED`;
- `NOT_SATISFIED`;
- `UNKNOWN_INPUT`;
- `DEFERRED_UNBOUND_INPUT`;
- `NEGATIVE_AUTHORITY`;
- `INTEGRITY_FAILURE`.

`UNKNOWN_INPUT` is not false. `DEFERRED_UNBOUND_INPUT` is not absence. Contradictory constraints are not averaged into plausibility.

### 9.4 Candidate court

For each registered fact rule:

1. build candidates only from allowed source classes;
2. verify source authority/version/hash/scope/effective time;
3. evaluate exact registered constraints;
4. preserve unknown/negative/deferred results;
5. produce a canonical admitted candidate set;
6. choose only if exact selection semantics exist.

Selection outcomes:

- **zero admitted candidates**
  - optional rule + lawfully empty source set -> `VALID_EMPTY_INITIAL_FACT`;
  - missing/unknown/underauthorized required input -> deferred/missing, not empty-as-fact;
- **one admitted candidate**
  - deterministic singleton; no entropy draw;
- **multiple admitted candidates + exact deterministic precedence**
  - deterministic selection;
- **multiple admitted candidates + explicit equiprobability**
  - ADP-020 `UNIFORM_CANDIDATE`;
- **multiple admitted candidates + exact governed integer weights**
  - ADP-020 `WEIGHTED_CANDIDATE_INTEGER`;
- **multiple admitted candidates without selection authority**
  - `DEFERRED_INITIAL_SELECTION_AUTHORITY`; no draw.

### 9.5 ADP-020 binding

Every stochastic initial-fact rule must declare a static stream under:

```text
v3.causal.initialization.*
```

The exact stream name is part of that rule's versioned semantics.

Because actor identity is created deterministically before optional fact selection, actor-specific initialization draws use:

```text
scope_kind = ACTOR
scope_id   = exact actor_id
```

No ADP-007 v1 rule authorizes a stochastic pre-actor-ID draw or a `RUN`-scope workaround for identity creation.

If the actor-entity event is the latest committed event, it anchors subsequent initialization draws under ADP-020. Missing root-seed metadata, stream registration, candidate identity or decision coordinate blocks the stochastic mutation.

Different lawful root seeds may produce divergent outcomes from the same structural context where an exact rule genuinely authorizes stochastic selection. Same root seed + same rule/candidate/constraint state reproduces the same outcome.

---

## 10. Activation and sparse initial checkpoint

### 10.1 Activation preconditions

`ACTOR_ACTIVATED` requires:

1. verified `ACTOR_ENTITY_CREATED`;
2. stable actor identity;
3. verified initialization request and effective time;
4. all ADP-007 rules marked `required` either resolved or lawfully satisfied;
5. no unresolved integrity failure;
6. exact refs to every admitted optional initial fact;
7. exact ADP-009 position refs that were actually generated, if any;
8. every stochastic decision accompanied by a valid ADP-020 receipt.

Optional missing facts do not block activation.

### 10.2 `ACTOR_ACTIVATED`

The activation event records:

```text
event_kind = ACTOR_ACTIVATED
actor_id
entity_creation_event_ref/hash
effective_time
admitted_initial_fact_refs[]
adp009_initial_position_fact_refs[]
initial_fact_decision_receipts[]
rng_decision_receipts[]
unresolved_optional_state_records[]
authority/rule versions
pre_activation_state_hash
event_id/event_hash
integrity_state
```

The event does not claim that its referenced structural positions were experienced, remembered or understood.

ADP-008 consumes this exact activation event/receipt and materializes the phase consequence:

```text
V3DP_GENERATION_PENDING -> V3DP_DEVELOPMENT_ACTIVE
```

No finer developmental segment is implied.

### 10.3 `V3InitialActorCheckpoint`

After activation, materialize:

```text
V3InitialActorCheckpoint {
    checkpoint_id,
    actor_id,
    causal_run_id,
    entity_creation_event_ref/hash,
    activation_event_ref/hash,
    developmental_phase_state_ref/hash,
    admitted_initial_fact_refs[],
    initial_position_fact_refs[],
    unresolved_unknown_missing_records[],
    source_phase_a_context_ref/hash,
    authority_registry_versions[],
    rng_receipt_refs[],
    causal_ledger_head_ref/hash,
    canonical_serialization_version,
    checkpoint_hash,
    integrity_state
}
```

A checkpoint is a materialized state/replay boundary, **not another event**.

`VALID_EMPTY_INITIAL_DOMAIN_STATE` is lawful: the actor may have identity, activation and an initial checkpoint while `admitted_initial_fact_refs[]` is empty and while no optional position fact exists, provided no exact required rule says otherwise.

---

## 11. Missing / unknown / negative / deferred / valid-empty law

Canonical decision/status states include:

- `ACTOR_ENTITY_CREATED_PENDING_ACTIVATION`;
- `ACTOR_ACTIVATED`;
- `VALID_EMPTY_INITIAL_DOMAIN_STATE`;
- `VALID_EMPTY_INITIAL_FACT`;
- `UNKNOWN_INITIAL_FACT_VALUE`;
- `MISSING_GENERATION_SUBJECT_AUTHORITY`;
- `MISSING_PHASE_A_CONTEXT`;
- `MISSING_INITIAL_FACT_RULE_AUTHORITY`;
- `MISSING_GOVERNED_DISTRIBUTION`;
- `DEFERRED_UNBOUND_INITIAL_INPUT`;
- `DEFERRED_INITIAL_SELECTION_AUTHORITY`;
- `DEFERRED_REQUIRED_POSITION_BINDING`;
- `NEGATIVE_INITIAL_FACT_AUTHORITY`;
- `ACTIVATION_BLOCKED_REQUIRED_INITIAL_FACT`;
- `INTEGRITY_FAILED`.

Rules:

1. **Missing** means a required source/rule/distribution is absent. It is not an actor property.
2. **Unknown** means the lawful source cannot establish the value. It is not midpoint or neutral.
3. **Negative authority** remains negative only inside the semantic rule that owns the negative statement.
4. **Deferred** means a later lawful input/authority may resolve the court; no fallback value is permitted.
5. **Valid-empty** means the rule expressly allows no fact/value to be instantiated. It is not missing and does not need filler.
6. An optional unknown/missing value may coexist with actor activation.
7. A required unresolved value blocks only when a registered initialization rule explicitly marks it required.
8. No status may be repaired by an LLM, demographic stereotype, “most common” value, first candidate, midpoint, or nearest neighbor.

---

## 12. Anti-demographic-destiny proof

The allowed information flow is:

```text
Phase-A structural/context material
        |
        +--> exact candidate/constraint refs under a registered rule
        |
        +--> exact unresolved position requirements -> ADP-009
        |
        +--> provenance retained by reference

never:

Phase-A / demographics -> actor psyche
```

Formally:

```text
generated_initial_fact
requires
(
  registered_initial_fact_rule
  AND exact semantic owner
  AND exact lawful source/candidate
  AND satisfied constraints
  AND exact selection authority if choice is non-singleton
  AND ADP-020 receipt if stochastic
)
```

Therefore no mapping of the following form exists under ADP-007 v1:

```text
country -> personality
class -> capacity/drive/belief/personality
religion -> framework/piety/meaning state
ethnicity/minority -> wound/trust/alienation
urbanicity -> mobility psyche
sex/gender -> personality/type
age -> maturity/personality/crack/history
demographic bundle -> Enneagram/type
```

The initial domain-fact registry is empty, so no hidden demographic-to-psychological rule can execute.

The same lawful Phase-A context may therefore yield:

- the same sparse initialization under deterministic/no-choice rules;
- different lawful initialized facts under an explicitly governed stochastic rule and different root seeds;
- unresolved/missing values where no distribution authority exists.

Structural context constrains possibility; it does not contain the finished person.

---

## 13. No invented prehistory

Initialization cannot backdate a generated event merely to make the actor seem developed.

Forbidden examples include:

- assigning a childhood crack `origin_year = birth_year + N`;
- creating a mother/father magnet without generated parents/relationship history;
- creating “home was safe/unsafe” assumptions;
- seeding school/friend/community encounters from age;
- creating a wound from class/minority/religion;
- populating memory or belief from biography text;
- attaching a relationship because a role label exists;
- treating Phase-A pressure as an already experienced event.

If initialization begins an already-older actor whose pre-initialization life history is required, that history must come from exact generated/imported causal-history authority with immutable provenance. ADP-007 does not synthesize it retrospectively.

---

## 14. Replay, provenance and immutability

### 14.1 Replay identity

A complete initialization replay binds:

- `V3_ACTOR_INITIALIZATION_RULE@1.0.0`;
- `V3_INITIAL_FACT_RULE_REGISTRY@1.0.0`;
- causal-run identity;
- generation-subject ID/hash/owner authority;
- exact requested effective time;
- Phase-A context/SelectionRecord/fidelity IDs and hashes;
- lawful nonactor input IDs/hashes/authority versions;
- actor-ID derivation scheme/version;
- actor entity-creation event ID/hash;
- every initial-fact rule/version and candidate-set hash;
- every constraint receipt;
- every ADP-009 initial position fact/event ref used;
- every ADP-020 root/stream/decision/draw receipt used;
- activation event ID/hash;
- ADP-008 resulting phase-state ref/hash;
- canonical serialization version;
- initial checkpoint hash.

Same immutable inputs + same accepted rule versions + same RNG lineage reproduce the same actor ID, initialization decisions, events and checkpoint.

### 14.2 Forbidden replay inputs

None of the following may alter semantic initialization:

- hidden wall clock;
- filesystem/database row order;
- mutable `latest`;
- process/PID/thread order;
- random UUID;
- unnamed/global RNG;
- Python hash seed;
- unrecorded network lookup;
- LLM/model completion;
- V2 rendered prose/session state;
- legacy default constructors.

### 14.3 No retroactive rewrite

Committed initialization events, facts and initial checkpoint are immutable historical records.

Later:

- mobility;
- context change;
- relationship formation;
- memory formation/forgetting;
- developmental phase changes;
- organismic change;
- attractor formation;
- migration;
- changed implementation or rule versions

must append prospective generated history. They may never edit initialization to make later life appear inevitable or to “correct” the starting person.

A new authority version may change how **future** actors initialize. Replaying an old actor uses the exact historical version that produced it.

---

## 15. Numeric/default disposition

ADP-007 defines **no universal numeric initial-state scale**.

Quarantined / compatibility-only, with semantic use denied unless a separate accepted semantic authority independently supplies the exact quantity contract:

- `Capacity.* = 50`;
- `PsychologicalCapacity.* = 50`;
- `WoundVector.* = 50`;
- `AlienationVector.* = 50`;
- register/gate/load `50` values;
- `Magnet.intensity = 50`;
- style/personality trait `50` values;
- `norm_center = "middle"` / `uniqueness_norm = 50`;
- stratum-strength `50` values;
- autonomy/safety universal constants such as `65` / `68`;
- class-to-money/debt/job-insecurity lookup tables;
- urbanicity-to-mobility lookup;
- minority-to-legitimacy lookup;
- approximate-population default and square-root country weights;
- default `middle`, `city`, `dominant`, `female`, `Persona`, `US`;
- default coping channels;
- default child assumptions;
- recovered age/religiosity/class thresholds;
- arbitrary uniform ranges from `randomized_seed`;
- 50/50 gender fallback;
- random internal IDs.

No recovered number becomes lawful merely because it was deterministic or stored in a typed field.

---

## 16. Hostile fixtures

| ID | Attack | Required outcome |
|---|---|---|
| H007-01 | same Phase-A context + same exact rules/seed lineage replayed | same actor ID, events, facts and checkpoint |
| H007-02 | same Phase-A context + an explicitly stochastic lawful fact rule + different root seeds | divergent lawful values may occur; both remain within admitted candidates |
| H007-03 | same Phase-A context but no stochastic selection authority | no invented divergence; deterministic/empty/deferred result only |
| H007-04 | fact rule requires a population distribution but none is governed | `MISSING_GOVERNED_DISTRIBUTION`; no fallback |
| H007-05 | country offered directly as personality/psyche | reject forbidden inference |
| H007-06 | class offered to initialize capacity/drive through recovered lookup | reject absent separate exact semantic rule |
| H007-07 | religion/religiosity offered to seed faith framework | reject |
| H007-08 | age offered to seed identity-search framework or backdated crack | reject invented psyche/history |
| H007-09 | minority status offered to seed wound/institutional trust | reject |
| H007-10 | Phase-A structural pressure copied as lived event/memory | reject epistemic/causal collapse |
| H007-11 | no optional domain fact rules apply | activate with `VALID_EMPTY_INITIAL_DOMAIN_STATE` if required gates pass |
| H007-12 | missing semantic value filled with `50` | reject default; preserve missing/unknown |
| H007-13 | missing country filled with `US` / `middle` / `city` / `dominant` | reject fallback |
| H007-14 | unspecified gender filled with `female` or 50/50 draw without governed rule | reject |
| H007-15 | random UUID/internal random integer used as actor identity | reject; deterministic actor ID required |
| H007-16 | module-global/unnamed RNG selects initial fact | block / `INTEGRITY_FAILED` |
| H007-17 | ADP-007 directly selects an initial class/sect/party position | reject; ADP-009 owns position generation |
| H007-18 | ADP-009 returns unresolved position and caller substitutes common value | reject; unresolved remains unresolved |
| H007-19 | no exact initialization rule requires unresolved position | unresolved position may coexist with activation; no default |
| H007-20 | parent/partner/relationship/household invented to complete actor | reject neighboring authority theft |
| H007-21 | “Adults are fair / home is safe” child assumptions used as initial facts | reject invented belief/history |
| H007-22 | later mobility/relationship/context change rewrites initial checkpoint | reject retroactive rewrite |
| H007-23 | LLM fills any missing initial state | reject; model has no semantic authority |
| H007-24 | contradictory constraints are averaged into a plausibility score | reject; preserve exact states / fail closed |
| H007-25 | optional registered fact has lawfully empty candidate set | `VALID_EMPTY_INITIAL_FACT`; no filler |
| H007-26 | required registered fact has missing/unknown source | `ACTIVATION_BLOCKED_REQUIRED_INITIAL_FACT` or typed defer |
| H007-27 | generation-subject ID reused with conflicting hash | `ACTOR_ID_COLLISION_OR_SUBJECT_REUSE_INTEGRITY_FAILURE` |
| H007-28 | hidden wall clock or mutable `latest` alters selection/ID | `INTEGRITY_FAILED` |
| H007-29 | ADP-020 coordinate reused for changed candidate/rule identity | propagate RNG coordinate/replay integrity failure |
| H007-30 | sibling-W2 ADP-015/CAN-006 return offered as authority before adjudication | reject sibling authority consumption |
| H007-31 | recovered V5 identity hydration ref is attached | preserve as opaque/source-bounded ref only; it does not create beliefs/psyche |
| H007-32 | historical type/Enneagram assigned at birth | reject categorically |

---

## 17. GOVERNING_SPIRIT_CHECK

**Status:** `APPLIED_AS_TIE_BREAK_ONLY`.

Hard authority already fixes:

- structural prior is not actor fact;
- ADP-009 owns generated positions;
- ADP-008 owns phase semantics while ADP-007 supplies activation;
- ADP-020 owns causal randomness;
- demographics may not become psychological identity;
- Enneagram/type may not exist as a birth essence;
- missing authority must fail closed.

The genuine lawful ambiguity was the grain of initialization:

1. instantiate a broad legacy-like “complete starting person” so every later subsystem has non-null state; or
2. create the minimum stable actor entity, provide an explicit rule court for any independently authorized initial facts, preserve lawful unknown/valid-empty values, and let generated history create the person over time.

Chosen: **2**.

Tie-break principles:

- personhood is becoming rather than classification;
- structural constraint without psychological essentialism;
- mediation rather than structure-to-psyche shortcuts;
- lawful absence rather than graceful hallucination;
- enough openness for divergent lives under the same structural field;
- dynamic history over static trait vectors;
- explicit accountable randomness;
- minimum sufficient machinery without starvation or duplicated ownership.

The Governing Spirit supplied **no demographic distribution, no psychological initial value, no personality semantics and no desired outcome**.

---

## 18. CONSUMER_RELEASE_SUFFICIENCY

**Status:** `SUFFICIENT_FOR_MUST_007_SEMANTIC_DEPENDENCY__NO_PRODUCTION_RELEASE`.

This result fully defines ADP-007's bounded semantic responsibility for the RA-R00 consumers:

- `V3-P1`;
- `V3-P3`;
- `V3-P4`;
- `V3-P9`.

If Vozhd accepts this result, `MUST-007` is closed as a semantic-authority dependency.

This does **not** release those implementation packets:

- `V3-P1` still has the separately scheduled generated-position binding canonicalization `CAN-006` and packet/release gates;
- `V3-P3`, `V3-P4`, and `V3-P9` retain their other MUST/CAN/EXT dependencies;
- ADP-015 genealogy remains a separate W2 authority and was not consumed;
- physical V558/EXT and later runtime integration gates remain independently binding.

The authority is therefore complete in jurisdiction while the machine remains correctly dependency-gated.

---

## 19. Final token

`ADP_007_V3_ACTOR_INITIALIZATION_AUTHORITY = PASS`
