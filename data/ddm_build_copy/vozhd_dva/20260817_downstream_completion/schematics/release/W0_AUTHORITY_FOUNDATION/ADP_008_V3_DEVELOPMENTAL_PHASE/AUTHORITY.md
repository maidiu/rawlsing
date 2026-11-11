# ADP-008 — V3 Developmental / Generation Phase Authority

**Assignment:** W0-04 — ADP-008 / V3 developmental-phase rule  
**Continuation:** minimum-sufficient developmental-phase authority hardening after Vozhd `RETURN_FOR_FIX`  
**Repository:** `maidiu/rawlsing`  
**Branch:** `agent/vozhd-dva-w0-adp-008-v3-developmental-phase`  
**Original exact launch base:** `655da47b9e03ab310ed4b7fa65ceec9b9d04d3bc`  
**Reviewed pre-fix head:** `208cb371211bfe8b3547f673a91a2143cb00b414`  
**RA-R00 authority item:** `MUST-008`  
**Authority ID:** `V3_DEVELOPMENTAL_PHASE_RULE`  
**Authority version:** `1.1.0`  
**Supersedes:** unadjudicated returned draft `V3_DEVELOPMENTAL_PHASE_RULE@1.0.0`  
**Owner:** `V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE`  
**Mode:** authority creation only; no production code; no V3 implementation; no architecture reopening  
**Verdict:** `PASS`  
**CONSUMER_RELEASE_SUFFICIENCY:** `SUFFICIENT`

## 0. Corrected binding holding

The canonical V3 developmental/generation phase interface is **minimum sufficient and history-bearing**.

It has only two universal base identities:

```text
V3DP_GENERATION_PENDING
V3DP_DEVELOPMENT_ACTIVE
```

`V3DP_GENERATION_PENDING` is available only where a governed prospective-generation subject genuinely exists for genealogy/context planning before actor activation.

`V3DP_DEVELOPMENT_ACTIVE` means exactly that a governed V3 actor has been activated and is undergoing open-ended development. It does **not** classify that development into childhood, foundational, transitional, adult, mature, late-life, parent, worker, student, or any other universal human-development slot.

For an active actor with no finer governed segmentation:

```text
base_phase_id = V3DP_DEVELOPMENT_ACTIVE
active_phase_segments = []
```

This is lawful **active unsegmented development**, not a missing value and not an invitation to invent a label.

Finer developmental segments exist only through the versioned `V3_DEVELOPMENTAL_PHASE_REGISTRY` owned by ADP-008. Authority version `1.1.0` contains **zero optional human-development segment entries**. A future segment may exist only when an explicit ADP-008 registry version defines its semantic scope, exact consumers, terminal/runtime need, boundary/admission rule, allowed input authorities, effective-time behavior, provenance and replay contract.

The machine therefore keeps distinct:

```text
chronological age / elapsed time
≠ universal V3 generation/development base state
≠ optional governed phase segment
≠ ContextResolver query purpose (including Phase A / Phase B)
≠ actor developmental state / personality / attractor / biography
```

No universal `FOUNDATIONAL → TRANSITIONAL → OPEN` ladder remains. The prior draft's three active universal epochs are withdrawn as unsupported semantic bloat.

No universal non-age-event witness requirement remains either. A governed phase-segment rule may use age/time, generated causal events, generated runtime facts, lawful derived predicates, or a governed combination, exactly as its registry entry declares. Age/time never acquires unstated psychological, demographic, positional or maturity meaning merely because it is used as a boundary guard.

No unnamed downstream developmental-boundary authority is required. ADP-008 owns the registry and phase-boundary-rule contract. Other already-named authorities may supply their own generated facts or predicates as declared inputs, but they do not acquire developmental-phase semantic ownership.

---

## 1. Governing law and correction basis

This corrected authority remains constrained by the original W0 common law and directly inspected accepted authorities:

- `state/CURRENT_STATE.md`;
- `integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`;
- `integration/IMPLEMENTATION_RELEASE_SYNTHESIS_RULING.md`;
- RA-R00 `schematics/release/RA_R00_RULE_AUTHORITY_IMPLEMENTATION_RELEASE/RESULT.md`;
- RA-R00 `RESULT.json`;
- `integration/V3_COMPLETION_IMPLEMENTATION_RULING.md`;
- TD-R05 `schematics/recalibration/TD_R05_V3_DEVELOPMENTAL_RUNTIME/RESULT.md`;
- TD-R05 `RESULT.json`;
- TD-R07 `schematics/closure/TD_R07_WHOLE_MACHINE_SYNTHETIC_LIFE/RESULT.md`;
- the directly verified historical V3/V2/server archive listed below.

### 1.1 Post-launch binding interpretive law

The continuation directly inspected, without rebasing or merging unrelated `main` changes:

`data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/integration/RAWLSING_GOVERNING_SPIRIT.md`

at commit:

`d01ec9dd05276d7928ed91e937531fa92da0d28f`.

Its relevant binding interpretation is applied only where the closed architecture left genuine design latitude:

- personhood is becoming, not classification;
- preserve contingent developmental divergence;
- preserve causal history over static convenience labels;
- use minimum sufficient semantic machinery;
- reject both starvation and bloat;
- do not turn runtime representation into hidden human essence.

This interpretive law did not reopen architecture and did not supply unsupported empirical phase semantics. It resolves the ambiguity against the returned draft's universal four-stage ladder.

### 1.2 No parallel-W0 contamination

No other W0 worker result was used as authority before Vozhd adjudication.

---

## 2. ADP-008 jurisdiction

### 2.1 ADP-008 owns

ADP-008 owns exactly:

1. the two universal base phase IDs and their narrow semantics;
2. the `V3_DEVELOPMENTAL_PHASE_REGISTRY` schema/versioning law;
3. optional phase-segment identity and semantics **only when actually entered into an ADP-008 registry version**;
4. phase-segment boundary/admission rule representation;
5. actor-local phase/segment membership transition admission;
6. positive, unresolved, ungoverned, unbound, ambiguous, forbidden and integrity states;
7. phase effective-time semantics;
8. the read-only phase envelope supplied to `ContextQuery` and other V3 consumers;
9. phase-boundary trigger publication to the scheduler without scheduler precedence ownership;
10. replay/provenance and compatibility requirements;
11. prohibition on age/demographic/structural/V2 shortcut phase invention.

### 2.2 ADP-008 does not own

ADP-008 does **not** decide:

- actor initialization or birth-generation facts — `ADP-007 / MUST-007`;
- population distributions, demographic defaults or identity defaults;
- generated positions, position transitions or mobility — `ADP-009`;
- opportunity/encounter/exposure realization — `ADP-010`;
- relationship/household/genealogy recursion — `ADP-015`;
- actor response, orientation, needs, wounds, vitality, causal memory or attractor dynamics;
- hybrid scheduler same-time precedence or slow-process cadence — `ADP-021 / MUST-021`;
- the pure derived-state schedule — `CAN-014`;
- V2 phenomenology, present-life seasons, dialogue, expression or transcript semantics;
- personality or Enneagram identity;
- structural-prior production or resolver proxy selection.

A named neighboring authority may produce a fact or predicate consumed by a registered phase rule. That does not move phase semantics into that neighboring authority.

---

## 3. Required historical archive verification

Required archive: `Rawlsing_code_bundle_staging.zip`.

Mounted upload directly reverified in this continuation:

`/mnt/data/Rawlsing_code_bundle_staging(2).zip`

Expected SHA256:

`953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`

Directly computed SHA256:

`953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`

**SHA verdict:** `EXACT_MATCH`  
**ZIP entries:** `13,138`

Recovered `v3/`, `v2/`, and relevant `server/` material remains continuity / authority-recovery evidence only. Historical archive V5/DDM material has **zero authority** over current V550+ and supplies no current phase semantics.

---

## 4. Historical/current evidence court — preserved

The narrow fix does not disturb the original evidence findings.

### 4.1 Recovered causal clock and state

Direct inspection established:

- `v3/v3_yearly_step_order.yaml`: explicit `timestep: "year"` and ordered causal/derived schedule;
- `v3/core/state.py`: persistent `year` and `age` plus longitudinal actor state, with no canonical terminal developmental-phase authority;
- `v3/engine/yearly_step.py`: increments `state.year += 1` and `state.age += 1`;
- `v3/engine/step_runner.py`: composes annual steps;
- `server/generation/simulation.py`: life generation driven partly by age, including a three-year LLM-band cadence.

**Disposition:** `ADAPT_AS_CADENCE_AND_REPLAY_EVIDENCE_ONLY`.

Annual progression is a useful integration mechanism. It is not developmental ontology.

### 4.2 Recovered age/lifecycle machinery

Direct inspection found mutually noncanonical age/lifecycle schemes:

- `v3/engine/striving_objects.py`: proxy striving age brackets and nearest-bracket behavior;
- `v3/engine/effects/metabolization_effects.py`: hard-coded rupture-band ages with stochastic injection;
- `v3/io/identity_to_backbone.py`: age-gated school/college proxies and identity-derived state shortcuts;
- `v3/psyche/channels.py`: wound sensitivities seeded from structural identity and age;
- `v3/tests/test_phase3_activation_gate.py`: “Phase 3” as an implementation milestone, not a human developmental phase;
- `v2/DRIVER_AGE_SCHEMA.md` and `v2/config/driver_age_schema.yaml`: birth/school/adolescence/young-adult/adulthood slots;
- `v2/ENNEAGRAM_EMERGENCE_SYSTEM.md`: useful no-type-at-birth intent mixed with age bands;
- `v2/LIFE_SIMULATION_LAYER.md`: `current_life_phase` presentation/session seasons such as job hunt, burnout, caregiving, activism surge or stable routine.

**Disposition:** `EVIDENCE_ONLY_FOR_AGE_SENSITIVE_RUNTIME_NEED`.

These mechanisms prove that later rules may need explicit chronology/phase predicates. They do not prove a universal phase taxonomy. The mutually inconsistent bands are positive evidence **against** treating any recovered lifecycle partition as terminal authority.

### 4.3 Current repository terrain

At the original exact launch base, no canonical current top-level V3 implementation existed to canonize. The accepted V3 ruling explicitly classified developmental phases as missing runtime-rule authority. This W0 result therefore creates the minimum machine authority needed by the closed architecture; it does not preserve a current production phase implementation.

---

## 5. Universal phase vocabulary — minimum sufficient

Authority `1.1.0` defines exactly two universal base IDs.

| Base phase ID | Canonical meaning | Explicit nonmeaning |
|---|---|---|
| `V3DP_GENERATION_PENDING` | A governed prospective-generation subject may be referenced for generation/context planning, but no V3 actor activation has yet established active actor causal history. | Not a living-person biography; no age, parent, caregiver, household, position, identity, personality, maturity or developmental segment. |
| `V3DP_DEVELOPMENT_ACTIVE` | A governed V3 actor has been activated and is in open-ended developmental causality. | No finer age/life-course segment; no maturity, autonomy, adulthood, legal status, school/work/family role, personality, Enneagram or attractor meaning. |

There is one universal base transition:

```text
V3DP_GENERATION_PENDING
        ↓ governed actor activation under ADP-007
V3DP_DEVELOPMENT_ACTIVE
```

This edge is an interface consequence of actor activation, not an actor-initialization rule. ADP-007 owns whether/how actor activation occurs and supplies the exact activation event/receipt. ADP-008 owns only the phase-state consequence once that named authority has lawfully activated the actor.

An already-active actor imported from a verified checkpoint may start materialization in `V3DP_DEVELOPMENT_ACTIVE` only when its activation/phase history verifies. That is replay, not a bypass.

There is **no universal active-development ladder** after activation.

In particular, authority `1.1.0` contains no universal:

- `FOUNDATIONAL_DEVELOPMENT`;
- `TRANSITIONAL_DEVELOPMENT`;
- `OPEN_DEVELOPMENT`;
- childhood/adolescence/adulthood/late-life phase;
- student/worker/parent/caregiver phase;
- personality/Enneagram phase.

`V3DP_DEVELOPMENT_ACTIVE` already preserves the binding fact that development remains open and path-dependent. No redundant “open development” segment is needed.

---

## 6. Canonical actor phase envelope

The logical phase state is:

```text
V3DevelopmentalPhaseState {
    actor_or_generation_subject_id,
    authority_id,
    authority_version,
    base_phase_id,
    active_phase_segment_refs[],
    status,
    effective_from,
    prior_phase_state_hash,
    provenance_refs[],
    phase_state_hash
}
```

Rules:

1. `V3DP_GENERATION_PENDING` requires `active_phase_segment_refs=[]`.
2. `V3DP_DEVELOPMENT_ACTIVE` with `active_phase_segment_refs=[]` is **lawful active unsegmented development**.
3. Optional phase segments may appear only as exact registry refs under §7.
4. No implementation may fill `active_phase_segment_refs` from prose labels, age tables, demographics or convenience defaults.
5. Multiple segment refs are lawful only when their registry entries do not declare mutual exclusion and the requesting consumer identifies the exact rule/segment namespace it consumes. No global scalar “most mature” segment exists.

This envelope permits the shared interface demanded by V3 runtime, ContextResolver, genealogy and scheduler without forcing a universal human taxonomy.

---

## 7. `V3_DEVELOPMENTAL_PHASE_REGISTRY`

### 7.1 Registry ownership

The registry is owned by **ADP-008 itself**.

No unnamed downstream “developmental boundary authority” exists.

A new optional developmental segment requires a new accepted ADP-008 registry version or an accepted amendment under the same named authority. Merely adding code, config, a scheduler task, a resolver predicate, an age table or another worker's consumer rule cannot create a developmental phase segment.

Authority `1.1.0` registry payload:

```text
optional_phase_rules = []
```

That empty registry is a complete lawful state.

### 7.2 Optional phase-rule entry

Any future optional phase segmentation must be represented by a record terminally equivalent to:

```text
V3DevelopmentalPhaseRule {
    phase_rule_id,
    phase_rule_version,
    registry_version,
    jurisdiction,
    terminal_or_runtime_need,
    exact_consumers[],
    segment_definitions[],
    transition_definitions[],
    admissible_input_authorities[],
    admissible_input_classes[],
    boundary_predicate_specs[],
    age_time_guard_semantics,
    ambiguity_policy,
    effective_time_rule,
    provenance_requirements[],
    replay_requirements[],
    rule_content_hash
}
```

Each `segment_definition` must include:

- stable namespaced `phase_segment_id`;
- bounded semantic meaning;
- explicit nonmeaning / semantic ceiling;
- exact consumers;
- why the segment is required by terminal composition or a separately governed runtime rule;
- any mutual-exclusion or coexistence relation needed inside that rule's own namespace.

Each `transition_definition` must include:

- transition identity;
- source membership condition, if any;
- target membership condition, if any;
- exact boundary predicate/rule expression;
- exact allowed input authorities/classes;
- effective-time semantics;
- fail-closed result when required inputs are absent/ambiguous;
- provenance/replay requirements.

A phase name that merely “sounds developmentally plausible” is inadmissible.

### 7.3 Who may supply boundary inputs

A registry rule may consume outputs from **already-named authorities whose own jurisdiction genuinely owns those outputs**.

Examples of lawful input ownership include:

- `ADP-007`: actor activation/birth-generation event or fact;
- `ADP-009`: generated position/mobility facts, if a future phase rule explicitly and lawfully needs them;
- `ADP-010`: generated opportunity/encounter/exposure facts, if explicitly required;
- `ADP-015`: generated relationship/household/genealogy facts, if explicitly required;
- other accepted V3 rule authorities: their own generated causal events/facts or versioned derived predicates, when explicitly named by a registry entry.

The supplying authority owns only its source fact/predicate. **ADP-008 remains owner of the developmental-phase segment meaning and boundary admission.**

Structural priors, resolver selections, demographics and V2 artifacts cannot become phase semantics merely by being referenced as context.

---

## 8. Optional phase-segment transition admission

No universal causal recipe is imposed on future phase boundaries.

A phase-segment transition/membership change is lawful only when:

1. the requested `phase_rule_id@version` exists in the active ADP-008 registry version;
2. the requested segment/transition identity exists in that rule;
3. the actor is in `V3DP_DEVELOPMENT_ACTIVE` unless the rule explicitly governs a generation-pending query without asserting actor state;
4. all required inputs come from the exact authorities/classes declared by the rule;
5. the rule's boundary predicate evaluates deterministically under its exact version;
6. no forbidden inference, ambiguity or integrity failure exists;
7. a versioned V3 phase transition/membership record is committed at the effective time.

Allowed boundary ingredients, when explicitly declared by the registry rule, include:

- chronological age or elapsed actor time;
- generated causal event(s);
- generated runtime fact(s);
- a lawful versioned derived predicate with its causal inputs reachable;
- a governed combination of the above.

There is **no universal requirement** for a non-age event witness.

There is also **no universal permission** for age to create developmental meaning. Age/time can be sufficient only because an explicit registry rule says the particular segment boundary is age/time-defined and limits the segment's meaning accordingly.

### 8.1 Runtime boundary evaluation receipt

An actor-specific boundary evaluation is a runtime receipt, not a new semantic authority:

```text
V3DevelopmentalPhaseBoundaryEvaluation {
    evaluation_id,
    actor_id,
    phase_rule_id,
    phase_rule_version,
    segment_or_transition_id,
    evaluated_at,
    proposed_effective_time,
    input_receipts[],
    predicate_receipts[],
    result,
    provenance_refs[],
    evaluation_hash
}
```

The evaluation executes ADP-008 registry authority. It does not delegate phase ownership to an unnamed producer.

### 8.2 Transition/membership record

```text
V3DevelopmentalPhaseTransitionRecord {
    transition_id,
    actor_id,
    authority_id,
    authority_version,
    base_phase_before,
    base_phase_after,
    phase_rule_id_if_segmented,
    phase_rule_version_if_segmented,
    transition_definition_id,
    from_segment_refs[],
    to_segment_refs[],
    effective_time,
    input_receipts[],
    boundary_evaluation_hash,
    prior_phase_state_hash,
    provenance_refs[],
    transition_record_hash
}
```

The record is V3 causal/runtime truth about phase membership. It is not a structural prior, demographic label, personality state or V2 rendering.

---

## 9. Age and elapsed-time law

Chronological age and elapsed actor time are independent chronological facts.

ADP-008 `1.1.0` defines **no universal human-development age cutoffs**.

Age/time may:

1. validate chronology;
2. be queried directly by another governed V3 rule when that rule owns an age-sensitive condition;
3. serve as an explicit phase-boundary guard or even the complete boundary basis **only when an ADP-008 registry entry explicitly defines that boundary**;
4. be recorded on phase evaluation/transition receipts for audit and replay;
5. yield a scheduler trigger time when an accepted registry rule makes a future boundary deterministically knowable.

Age/time may not:

1. select a developmental segment through an implicit `if age then human phase` table;
2. revive recovered birth/school/adolescence/adulthood slots as aliases;
3. imply maturity, autonomy, legal status, personality, ideology, family role, school/work position, attractor state or biography unless a separately governed authority owns that exact fact;
4. repair an ungoverned requested phase distinction.

Required invariants:

```text
known age + no registered segment rule
= V3DP_DEVELOPMENT_ACTIVE with no segment

known age + requested unregistered "adolescent"/"adult" segment
= PHASE_SEGMENT_NOT_GOVERNED

registered age/time-defined segment rule + satisfied exact guard
= lawful segment transition/membership under that rule only
```

Thus an age-only boundary is neither universally forbidden nor universally meaningful. Its semantics are bounded by the exact registered rule.

---

## 10. Decision and fail-closed states

| State | Meaning |
|---|---|
| `ACTIVE_OR_GOVERNED_PHASE` | Universal base state is verified; actor is either lawfully active-unsegmented or has exact governed segment membership(s). |
| `TRANSITION_APPLIED` | A universal activation edge or registered segment transition passed exact rule/integrity checks and was committed. |
| `PHASE_UNRESOLVED` | The relevant base phase or an already-governed required membership cannot be lawfully established from verified history. |
| `PHASE_SEGMENT_NOT_GOVERNED` | A consumer requests a finer developmental distinction for which the active ADP-008 registry contains no governing rule/segment. No substitute label is invented. |
| `PHASE_BOUNDARY_UNBOUND` | A governed segment rule exists, but a boundary input required by that rule is not yet bound/known. Current lawful phase state remains unchanged. |
| `AMBIGUOUS_PHASE_TRANSITION` | Two non-identical incompatible phase transitions/memberships survive under the same governing rule/effective time and the rule supplies no lawful resolution. |
| `BLOCKED_INVALID_PHASE_TRANSITION` | Requested base or segment transition is not admitted by the exact registered rule. |
| `BLOCKED_FORBIDDEN_PHASE_INFERENCE` | Structural, demographic, legacy-age-band, V2, personality/type or other forbidden material is offered as phase semantics/authority outside a registered rule. |
| `INTEGRITY_FAILURE` | Actor/rule/version/hash/prior-state/input/predicate/provenance validation fails. |

Exact duplicates with the same authoritative identity and content hash may deduplicate. Row order, lexical order, arrival order, mutable `latest`, or scheduler queue order may never invent semantic precedence.

Crucially:

```text
PHASE_SEGMENT_NOT_GOVERNED
```

is a correct terminal answer. It does not force the universal active phase to null and does not block phase-independent runtime work.

---

## 11. Effective-time semantics

Universal base phase and each governed phase-segment membership are history-bearing.

- `V3DP_GENERATION_PENDING` begins only when a governed prospective-generation subject exists.
- Governed actor activation at `T` ends generation-pending status and establishes `V3DP_DEVELOPMENT_ACTIVE` at `T`.
- Optional segment memberships occupy intervals or event-indexed states exactly as their registry rule defines.
- A committed segment transition at `T` changes only the memberships named by that rule; it does not rewrite unrelated actor state.
- Future age/time boundaries are noncausal until the runtime reaches/evaluates the governed boundary and commits the transition.
- Event/fact-based boundaries remain unbound until their declared input occurs or becomes available.
- Late evidence, changed policy or a new registry version may not silently backdate or relabel committed phase history.
- Correction or migration requires explicit replay/reconstruction under the exact old/new rule versions; prior hashes remain audit-visible.
- Wall-clock time may never mutate phase state.

---

## 12. ContextResolver / query-purpose interaction

The accepted `ContextQuery.developmental_or_generation_phase` interface is bound to a read-only `V3DevelopmentalPhaseState` projection.

It carries:

- universal `base_phase_id`;
- ADP-008 authority version;
- exact active governed segment refs relevant to the query, if any;
- phase-state hash;
- or an explicit fail-closed phase state.

Resolver **Phase A** / **Phase B** are query purposes/binding modes, not developmental phase IDs or segment rules:

```text
ContextQuery.query_purpose
≠ ContextQuery.developmental_or_generation_phase
```

ContextResolver may:

- use a supplied verified base phase or exact governed segment ref as a predicate input where a producer/runtime rule explicitly requires it;
- continue phase-independent resolution while optional segmentation is absent;
- return a phase-required object as unbound/deferred where an exact governed phase membership is unresolved.

ContextResolver may not:

- infer phase from age, query purpose, geography, structural priors, prevalence or demographics;
- mint an optional segment because an upstream object has an age/lifecycle label;
- choose a “closest” registered segment;
- advance V3 phase state.

If a resolver/consumer asks for a named segment that is not in the active ADP-008 registry, the authority result is `PHASE_SEGMENT_NOT_GOVERNED` (or a transport-level equivalent preserving that exact meaning), not a guessed phase.

A committed registered phase transition may trigger prospective re-resolution where phase-conditioned predicates exist. ADP-008 supplies the changed fact; resolver semantics remain read-only.

---

## 13. Genealogy interaction

One universal base-state law and the same versioned registry contract apply independently to every generated person.

A prospective child may lawfully be represented as `V3DP_GENERATION_PENDING` once the genealogy/generation authority has created the prospective generation subject. ADP-008 does not create that subject.

After the child's governed actor activation under ADP-007, the child becomes `V3DP_DEVELOPMENT_ACTIVE` with no optional segments unless an exact ADP-008 registry rule independently admits one for that child.

Forbidden:

- parent base phase → child base phase copying;
- parent segment → child segment copying;
- household/cohort/culture/demographic label → child phase;
- parent phase → parent personality inference;
- phase → relationship/household/reproduction fact.

A parent's governed phase segment may be consumed by a later genealogy rule only if that named rule explicitly declares it as an input. The parent remains the source of its own generated phase history; the child receives no phase by inheritance.

Genealogy remains `ADP-015` jurisdiction.

---

## 14. Hybrid scheduler interaction

ADP-008 can publish a **phase-boundary trigger candidate** only when the active registry rule makes a future boundary time lawfully knowable from already-authorized inputs.

A trigger candidate is terminally equivalent to:

```text
V3PhaseBoundaryTriggerCandidate {
    actor_id,
    phase_rule_id,
    phase_rule_version,
    transition_definition_id,
    trigger_time,
    trigger_basis_hash,
    provenance_refs[]
}
```

Examples:

- a registered age/time boundary may expose a deterministic future trigger time;
- an event-based boundary exposes no invented future time and is evaluated when the relevant event/fact arrives;
- an ungoverned phase distinction exposes no trigger.

The scheduler consumes the trigger candidate but does not own or reinterpret phase semantics.

ADP-008 does **not** decide:

- same-time event precedence;
- ordering against resolver `next_context_change`;
- ordering against encounter/move/relationship events;
- slow-process maintenance cadence;
- annual integration cadence;
- checkpoint cadence;
- event queue ordering.

Those remain `ADP-021 / MUST-021` jurisdiction.

---

## 15. Replay, provenance and versioning

Phase state must be reproducible from V3 causal/runtime history plus immutable phase-registry versions.

Required replay identity includes:

- actor/generation-subject ID;
- ADP-008 authority ID/version;
- exact registry version/content hash;
- actor-activation receipt for the universal base transition;
- ordered phase transition/membership record IDs, hashes and effective times;
- phase-rule IDs/versions/content hashes for optional segments;
- exact source fact/event/derived-predicate receipts consumed by each boundary evaluation;
- age/time source and chronology version when age/time is used;
- named RNG provenance only if an input-producing authority lawfully used randomness;
- repository/resolver receipts only when a registry rule explicitly uses them as context.

A checkpoint may cache base phase and segment memberships but is not independent authority. If checkpoint phase state disagrees with replayed phase history or registry identity: `INTEGRITY_FAILURE`.

A new ADP-008 registry version cannot retroactively classify old history without an explicit versioned migration/replay rule.

Forbidden hidden inputs:

- wall clock;
- filesystem order;
- mutable `latest`;
- unversioned age-band tables;
- implicit demographic defaults;
- ad hoc consumer phase strings.

---

## 16. Exact consumers

RA-R00 direct implementation consumers of `MUST-008`:

- `V3-P1`;
- `V3-P4`;
- `V3-P7`;
- `V3-P9`.

Authority/interface consumers:

- `ADP-007` actor initialization, consuming the universal base-state consequence of its own actor activation;
- `ADP-009` generated position/transition/mobility rules, only where an accepted future rule explicitly consumes a governed phase ref;
- `ADP-010` encounter/opportunity/exposure rules, same constraint;
- `ADP-015` relationship/household/genealogy rules;
- `ADP-021` hybrid causal scheduler, consuming only trigger candidates / committed phase facts;
- `ContextResolver` / `ContextQuery` as a read-only phase predicate interface;
- later V3 age/development-gated rules that explicitly name either chronology or an exact governed ADP-008 phase segment.

V2 is not a phase-authority consumer. V2 life seasons cannot define or mutate V3 phase.

---

## 17. Compatibility law

1. Recovered `age` and `year` remain chronology/cadence data.
2. Legacy V2 birth/school/adolescence/young-adult/adulthood bands are not aliases.
3. V2 `current_life_phase` seasons are not aliases.
4. The returned draft IDs `V3DP_FOUNDATIONAL_DEVELOPMENT`, `V3DP_TRANSITIONAL_DEVELOPMENT`, and `V3DP_OPEN_DEVELOPMENT` have **no accepted authority** and must not be used as compatibility aliases.
5. No adapter may map an age band to a phase segment absent an exact active ADP-008 registry entry.
6. No structural prior may be relabeled as developmental phase.
7. Later checkpoint imports require verified base-phase/segment transition history and exact registry versions.
8. No implementation may mint phase-segment strings outside the active registry.
9. No phase or segment ordinal may become a maturity/personality score unless a future authority explicitly and separately owns such a value; ADP-008 does not.
10. Changes in dependency, health, capacity, household, work, relationship or social status are their own actor facts and do not automatically create a phase segment.
11. No death/end-of-life phase is created here.
12. `V3DP_DEVELOPMENT_ACTIVE` is intentionally open-ended; the runtime does not need a terminal “open development” label to prove development remains open.

---

## 18. Hostile fixtures

| Fixture | Hostile case | Required outcome |
|---|---|---|
| `HF-008-01` | Active actor reaches legacy cutoff 18; registry contains no matching segment rule. | Remain `V3DP_DEVELOPMENT_ACTIVE` with no segment; requested finer distinction returns `PHASE_SEGMENT_NOT_GOVERNED`. |
| `HF-008-02` | Consumer requests old `V3DP_TRANSITIONAL_DEVELOPMENT`. | `PHASE_SEGMENT_NOT_GOVERNED`; returned draft ladder has no authority. |
| `HF-008-03` | Age known but universal base-phase history missing/invalid. | `PHASE_UNRESOLVED`; age cannot reconstruct base phase. |
| `HF-008-04` | Structural/demographic category says “adult/adolescent.” | `BLOCKED_FORBIDDEN_PHASE_INFERENCE`. |
| `HF-008-05` | V2 `current_life_phase=burnout_phase` offered as V3 phase. | `BLOCKED_FORBIDDEN_PHASE_INFERENCE`. |
| `HF-008-06` | Annual tick increments age/year with no registered phase rule. | Base phase and segment set unchanged. |
| `HF-008-07` | Future ADP-008 registry rule explicitly defines an age-only bounded segment; exact age guard is satisfied. | Segment may lawfully enter/transition under that rule; no maturity/personality/biography inference beyond the registered semantic ceiling. |
| `HF-008-08` | Same age threshold is crossed without any registered phase rule. | No segment transition; `PHASE_SEGMENT_NOT_GOVERNED` if requested. |
| `HF-008-09` | Registered event/fact-based phase rule exists but required input has not occurred/bound. | `PHASE_BOUNDARY_UNBOUND`; current lawful phase state unchanged. |
| `HF-008-10` | Two incompatible same-time segment transitions survive under one rule with no governed resolver. | `AMBIGUOUS_PHASE_TRANSITION`; no first-row/queue-order winner. |
| `HF-008-11` | Child phase/segment copied from parent, household or cohort. | `BLOCKED_FORBIDDEN_PHASE_INFERENCE`; child phase history is independent. |
| `HF-008-12` | Resolver Phase A/B supplied as developmental phase. | `BLOCKED_FORBIDDEN_PHASE_INFERENCE` or schema rejection; query purpose remains orthogonal. |
| `HF-008-13` | Scheduler receives a known boundary time and directly mutates phase without ADP-008 evaluation/commit. | Reject; scheduler trigger is not phase authority. |
| `HF-008-14` | Checkpoint carries a segment missing from the referenced registry version. | `INTEGRITY_FAILURE`. |
| `HF-008-15` | Late evidence/new registry version silently reclassifies prior years. | Reject in-place rewrite; explicit replay/migration required. |
| `HF-008-16` | Historical archive V5/DDM lifecycle material offered as current authority. | `BLOCKED_FORBIDDEN_PHASE_INFERENCE`; archive V5/DDM has zero authority. |
| `HF-008-17` | Consumer invents ad hoc segment string because its field requires non-null phase. | `PHASE_SEGMENT_NOT_GOVERNED`; universal active-unsegmented state remains valid. |
| `HF-008-18` | Named authority supplies a generated position/relationship/event fact to a registered phase rule. | Fact may be consumed only as declared input; phase meaning remains owned by ADP-008. |
| `HF-008-19` | Derived predicate is used but its producing rule/version or causal parents are unreachable. | `INTEGRITY_FAILURE`; no transition. |
| `HF-008-20` | Exact duplicate transition record ID/hash appears twice. | Safe deduplication; no duplicate causal membership change. |

---

## 19. Consumer release sufficiency

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT`.

`MUST-008` is closed without a new unnamed semantic authority because ADP-008 itself now owns the complete minimum contract:

- two universal base identities;
- lawful active-unsegmented behavior;
- an explicitly empty optional-segment registry in `1.1.0`;
- the machine contract by which future ADP-008 versions may add only consumer-justified segments;
- allowed boundary input classes without a universal witness recipe;
- age/time semantic ceilings;
- exact boundary/transition admission and fail-closed behavior;
- resolver/query-purpose separation;
- genealogy separation;
- scheduler trigger/nonownership law;
- effective-time, provenance and replay requirements.

A future consumer that asks for a finer phase distinction not present in the accepted registry is correctly blocked/deferred by `PHASE_SEGMENT_NOT_GOVERNED`. That is **not** a failure of MUST-008 and does not force invention of a phase.

This does **not** globally release V3 implementation. Each consumer remains gated by all other RA-R00 dependencies, including as applicable `MUST-007`, `MUST-009`, `MUST-010`, `MUST-015`, `MUST-020`, `MUST-021`, `CAN-006`, `CAN-007`, `CAN-009..011`, `CAN-014`, and `EXT-007`.

---

## 20. Final authority statement

### THIS AUTHORITY OWNS

- `V3DP_GENERATION_PENDING`;
- `V3DP_DEVELOPMENT_ACTIVE`;
- lawful active-unsegmented development;
- `V3_DEVELOPMENTAL_PHASE_REGISTRY` and all future optional phase-segment semantics admitted through its accepted versions;
- phase-rule boundary/admission contract;
- actor-local phase evaluation and transition/membership receipts;
- effective-time, replay, hash and provenance law;
- read-only phase interface used by resolver and named V3 consumers;
- scheduler phase-boundary trigger publication without scheduler precedence;
- rejection of ungoverned age/demographic/structural/V2 phase invention.

### THIS AUTHORITY DOES NOT OWN

- actor initialization;
- population/default phase segmentation;
- position generation;
- encounters/exposure;
- genealogy rules;
- actor psychology, maturity or attractor formation;
- scheduler precedence/cadence;
- V2 phenomenology/expression.

### PHASE-BOUNDARY OWNERSHIP LAW

**ADP-008 owns developmental-phase semantics and boundary admission.** Named neighboring authorities may supply their own exact facts/predicates only when an ADP-008 registry rule declares them. No unnamed downstream phase authority is required or permitted.

### RECOVERED MACHINERY VERDICT

- yearly ordered causal spine: **ADAPT** as cadence/integration continuity;
- stored age/year chronology: **PRESERVE AS SEPARATE CHRONOLOGY**;
- legacy age/lifecycle gates: **EVIDENCE ONLY / DO NOT CANONIZE**;
- identity/structural-prior → developmental-state shortcuts: **REJECT**;
- V2 life seasons: **V2-ONLY NEGATIVE EVIDENCE**;
- no-type-at-birth life-course intent: **CONTINUITY INTENT ONLY**, not phase vocabulary;
- returned universal `FOUNDATIONAL → TRANSITIONAL → OPEN` ladder: **WITHDRAWN / NOT AUTHORITY**;
- returned universal non-age-witness requirement: **WITHDRAWN / REPLACED BY PER-RULE BOUNDARY CONTRACT**.

`ADP_008_V3_DEVELOPMENTAL_PHASE_AUTHORITY = PASS`