# ADP-010 — V3 Opportunity / Encounter / Exposure Realization Authority

**Assignment:** W1-03  
**Repository:** `maidiu/rawlsing`  
**Branch:** `agent/vozhd-dva-w1-adp-010-v3-encounter-exposure`  
**Exact launch base:** `10a8e60f171e3a70bf48336fff73d37040cc1b93`  
**RA-R00 item:** `MUST-010` / `ADP-010`  
**Authority ID:** `V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE`  
**Authority version:** `1.0.0`  
**Registry:** `V3_OEE_REALIZATION_RULE_REGISTRY@1.0.0`  
**Owner:** `V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE`  
**Mode:** authority creation only; no production code; no V3 implementation  
**Verdict:** `PASS`  
**CONSUMER_RELEASE_SUFFICIENCY:** `SUFFICIENT`

## 1. Constitutional holding

ADP-010 governs exactly this actor-specific causal seam:

```text
AVAILABLE -> OPPORTUNITY -> ENCOUNTER -> EXPOSURE
```

No transition may collapse or skip. The binding nonidentity is:

```text
structural availability
!= upstream applicability
!= opportunity
!= encounter
!= exposure
!= V555 route traversal
!= V556 interaction realization
!= actor response / memory / belief / relationship
!= developmental or attractor change
```

`AVAILABLE` is lawful basis in the actor's bounded runtime world, not lived history. `OPPORTUNITY` is a time-bounded actor-specific possibility of contact/access, not contact. `ENCOUNTER` is admitted contact occurrence, not exposure. `EXPOSURE` is an admitted objective presentation/impingement occurrence through an encounter, not absorption, awareness, memory, belief, response, route traversal, relationship, or psychological change.

Nonoccurrence is lawful. No minimum encounter/exposure count, filler event, first-candidate fallback, random/default biography, or schema-driven pseudo-event is authorized.

## 2. Governing law, dependencies, consumers

Inspected binding authority includes W1 common law; `CURRENT_STATE.md`; `RAWLSING_GOVERNING_SPIRIT.md`; whole-machine, implementation-release, W0-closure and V3 completion rulings; RA-R00 `RESULT.md/json`; TD-R05; TD-R07 `RESULT.md/json`; accepted V554/V555/V556 architecture only as upstream possibility/constraint law; and relevant current fail-closed tests.

Exact accepted dependencies consumed:

1. `V3_DEVELOPMENTAL_PHASE_RULE@1.1.0` / ADP-008;
2. `ADP-020@1.0.0` causal randomness.

No sibling W1 result was used. ADP-009 semantics were not consumed.

Exact RA-R00 consumers: `V3-P5`, `V3-P9`. This authority does not itself release either consumer.

Dependency consequences:

- positive actor-side `OPPORTUNITY`, `ENCOUNTER`, or `EXPOSURE` requires `V3DP_DEVELOPMENT_ACTIVE`;
- `V3DP_GENERATION_PENDING` cannot have lived OEE history;
- ADP-008 v1.1.0 supplies no childhood/adult/maturity segments, so ADP-010 cannot invent them;
- randomness may resolve only already-lawful contingency under ADP-020; empty candidate sets consume zero draws and remain empty.

## 3. Jurisdiction

ADP-010 owns the four state meanings; no-skip transition admission; candidate-source/use-permission court; opportunity/encounter/exposure admission; OEE candidate identity supplied to ADP-020; nonoccurrence/negative/empty/unknown/noncomparable/missing/deferred/integrity states; OEE record/event identity; repetition; local temporal parentage; provenance and replay.

ADP-010 does **not** own V554 affordance/applicability; V555 route semantics or ADP-011 route realization; V556 F1/F2 semantics or interaction realization; actor initialization; generated positions/mobility; relationship/household/genealogy; response/metabolization; memory; belief/knowledge; orientation/needs/wounds/vitality; rupture/attractor dynamics; global scheduler precedence; or V2 phenomenology/rendering.

An ADP-010 exposure can be consumed later only under the downstream authority that owns the consequence.

## 4. Historical archive court

Required archive: `Rawlsing_code_bundle_staging.zip`.

- expected SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`
- directly computed SHA256 before reliance: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`
- verdict: `EXACT_MATCH`
- entries: `13,138`

Recovered V3/V2/server material is continuity/authority-recovery evidence only. Historical V5/DDM has **ZERO authority** over current V550+.

Directly inspected recovered evidence:

- `v3/engine/event_engine.py`: generic pseudo-random fabricated events; useful identity/conditioning continuity, not terminal encounter semantics;
- `v3/engine/scoring.py`: unnamed `random.Random()` fallback and surprise selection;
- `v3/engine/llm_contract.py`: empty-candidate fallback event creation;
- `v3/engine/run_llm_band.py`: unnamed RNG fallback and first-candidate force selection after empty selection;
- `v3/core/year_record.py`: stable hashing/record continuity;
- `v3/core/generation_integrity.py`: clean/degraded/blocked integrity continuity;
- `v3/core/state.py`, `v3/engine/prompts.py`: life/relationship/opportunity proposal continuity, not authority;
- `v3/systems/attention.py`: overloaded scalar “exposure” variable, explicitly not terminal exposure occurrence semantics;
- `server/generation/simulation.py`: narrative parent-meeting orchestration, not encounter authority;
- `v2/LIFE_SIMULATION_LAYER.md`: consumer/presentation evidence only.

Binding recovery: preserve explicit event/candidate/provenance structure and integrity; remove fabricated empty-set events, first-candidate forcing, unnamed RNG, generic pseudo-biography, and scalar-exposure substitution.

## 5. Exact machine vocabulary

### 5.1 Realization states

- `AVAILABLE` — exact subject/basis is lawfully addressable in the actor's bounded runtime context. Does **not** assert applicability, access, encounter, exposure, or traversal.
- `OPPORTUNITY` — exact actor-specific time-bounded possibility of contact/access exists under a governed basis. Does **not** assert occurrence.
- `ENCOUNTER` — exact contact occurrence is admitted under an open opportunity. Does **not** assert exposure or any downstream effect.
- `EXPOSURE` — exact bounded subject/content/pressure/practice/signal/condition is objectively presented to or impinges on the actor through an encounter. Does **not** assert noticing, understanding, memory, belief, response, traversal, relationship, or development.

Upstream applicability remains separate. An item can be `AVAILABLE` while a separate applicability receipt blocks or defers `OPPORTUNITY`.

### 5.2 Decision states

Exact decision vocabulary:

```text
ADMITTED
NEGATIVE
VALID_EMPTY
NONOCCURRENCE
UNKNOWN
NONCOMPARABLE
MISSING_AUTHORITY
DEFERRED
FORBIDDEN_INFERENCE
INTEGRITY_FAILURE
```

`NEGATIVE` is explicit governed denial. `VALID_EMPTY` means the rule executed and produced zero lawful candidates. `NONOCCURRENCE` means a lawful opportunity did not become encounter, or an encounter did not become exposure, in the evaluated closed scope. `UNKNOWN` is factually unknown. `DEFERRED` may resolve later. `MISSING_AUTHORITY` has no governing rule/input authority. `NONCOMPARABLE` cannot lawfully be evaluated together. `FORBIDDEN_INFERENCE` attempted a prohibited shortcut. `INTEGRITY_FAILURE` is identity/hash/version/provenance/RNG failure.

These states may not collapse to null/zero/generic false.

### 5.3 Event vocabulary

Canonical family: `ENCOUNTER_EXPOSURE_EVENT`.

ADP-010 effect/subkind vocabulary:

```text
OEE_OPPORTUNITY_ESTABLISHED
OEE_ENCOUNTER_OCCURRED
OEE_EXPOSURE_OCCURRED
```

`AVAILABLE` is a state record, not an event. `NONOCCURRENCE` is a decision receipt, not a pseudo-event.

## 6. Canonical records and identity

`V3OEERealizationRecord` requires:

```text
record_id, actor_id,
authority_id/version, registry_id/version, rule_id/version,
realization_state, subject_ref, parent_record_id,
effective_from, effective_until, time_granularity,
source_candidate_id, source_candidate_replay_hash,
context_or_world_receipt_refs[], applicability_receipt_refs[],
phase_state_ref, position_or_other_constraint_refs[],
causal_witness_refs[], rng_decision_receipt_ref,
event_id, event_effect_kind, prior_ledger_anchor_ref,
provenance_refs[], record_hash
```

Parent law:

```text
AVAILABLE.parent = null
OPPORTUNITY.parent = AVAILABLE
ENCOUNTER.parent = OPPORTUNITY
EXPOSURE.parent = ENCOUNTER
```

No skip is allowed, including at one timestamp. A single already-canonical causal event may carry multiple separately parent-linked OEE effect records when one occurrence truly causes them; semantic records stay distinct and no duplicate pseudo-event is created.

`V3OEEDecisionReceipt` records every evaluation, including nonpositive outcomes, with requested transition, parent, candidate set/hash, exact inputs/negative refs, rule/version, optional ADP-020 receipt, decision state/reason, admitted record/event if any, provenance and decision hash. Nonpositive decisions create no causal event.

OEE record identity is content-addressed over actor; authority/registry/rule versions; state; subject; parent; effective scope/granularity; canonical causal witnesses; candidate replay hash; and RNG decision receipt if any. Domain separator:

`RAWLSING\0ADP-010\0V3_OEE_REALIZATION_RECORD_V1\0`

Canonical JSON follows ADP-020's controlled ordering/NFC/no-hidden-order discipline. Random UUID, wall clock, filesystem order, mutable `latest`, labels and container iteration are forbidden identity sources.

## 7. Rule registry and admissible inputs

`V3_OEE_REALIZATION_RULE_REGISTRY@1.0.0` requires each rule to bind: rule ID/version; transition; exact eligible input authority signatures; epistemic classes/use permissions; phase predicate; applicability and runtime requirements; temporal scope; causal-witness requirements; candidate identity; stochastic policy; negative precedence; repetition; event effect; semantic ceiling; provenance/replay; and rule-content hash.

Core v1 rules:

1. `OEE_CORE_AVAILABLE_BASIS_V1` — exact permitted resolved-context/generated-world basis -> `AVAILABLE` only.
2. `OEE_CORE_OPPORTUNITY_FROM_EXPLICIT_BASIS_V1` — exact actor-specific runtime basis + declared constraints -> `OPPORTUNITY` only.
3. `OEE_CORE_ENCOUNTER_FROM_EXPLICIT_CONTACT_WITNESS_V1` — open opportunity + exact contact witness -> `ENCOUNTER` only.
4. `OEE_CORE_EXPOSURE_FROM_EXPLICIT_PRESENTATION_WITNESS_V1` — encounter + exact presentation/impingement witness -> `EXPOSURE` only.

All four are deterministic witness rules and consume zero RNG draws.

Admissible classes:

- `RESOLVER_DERIVED_CONTEXT`: may establish/constrain `AVAILABLE` and opportunity candidates; selection alone never establishes opportunity/encounter/exposure. Future-proxy evidence time remains future and cannot be backdated into lived history.
- `GENERATED_RUNTIME_FACT` / `ADMITTED_CAUSAL_EVENT`: may serve as opportunity basis, encounter witness or exposure witness only when an exact ADP-010 rule binds that input authority/signature to that use. Labels are not authority.
- structural V554/V555/V556 refs: constraint/possibility references only. They are never encounter/exposure witnesses by themselves.
- negative/limit/missing/noncomparable inputs: may block/qualify/classify, never become positive candidates.

## 8. Transition/admission court

### `BASIS -> AVAILABLE`

Requires exact subject identity; source authority/version/epistemic class; causal-use permission not denying consideration; actor/runtime context and evaluation time; native-scope/temporal/provenance validity; no integrity failure or forbidden inference.

### `AVAILABLE -> OPPORTUNITY`

Requires exact parent `AVAILABLE`; `V3DP_DEVELOPMENT_ACTIVE`; exact ADP-010 rule; exact actor-specific opportunity-basis receipt; every rule-required applicability condition positive; every required generated runtime binding supplied by its own accepted owner or typed `DEFERRED`/`MISSING_AUTHORITY`; exact temporal scope; complete candidate identity/provenance; and ADP-020 receipt if a future authorized rule is stochastic.

Insufficient alone: same geography, room/locality/household label, time interval, structural source/target, V555 endpoint, institution/category, simultaneous resolver selection, or plausible narrative scene.

### `OPPORTUNITY -> ENCOUNTER`

Requires exact active parent opportunity; active actor phase; exact contact-occurrence witness bound by rule; witness provenance independent of co-presence; all declared preconditions; ADP-020 occurrence decision if stochastic; idempotent event/effect identity.

Opportunity closes without encounter -> `NONOCCURRENCE`, no encounter event.

### `ENCOUNTER -> EXPOSURE`

Requires exact parent encounter; exact bounded exposure subject; exact presentation/impingement witness bound by rule; lawful time during/through encounter; continued structural use/applicability where relevant; ADP-020 decision if stochastic; no response/route/memory/relationship/psychological predicate substituted for exposure witness.

Encounter closes without exposure -> `NONOCCURRENCE`; encounter remains history; no exposure event.

## 9. Candidate-set / RNG law

ADP-010 candidates are content-addressed from transition, actor, subject, parent, effective scope, rule ID/version, canonical witness refs, required constraint receipts, input authority/version identities and causal-use permissions.

ADP-020 candidate fields are exactly compatible with `ADP020_CANDIDATE_SET_V1`: `candidate_id`, `candidate_replay_hash`, ADP-010 authority/version, eligibility/admission receipt hash, and `weight_units` only where separately governed. Default identity mode: `SET_CANONICAL`.

Empty set law:

```text
candidate_count = 0
rng_draws = 0
decision = VALID_EMPTY
fallback_event = forbidden
first_candidate_force_selection = forbidden
```

Reserved streams for future accepted stochastic ADP-010 rules:

```text
v3.causal.adp010.opportunity
v3.causal.adp010.encounter
v3.causal.adp010.exposure
```

Ordinary scope is `ACTOR`. `JOINT` is allowed only if an accepted semantic rule proves a genuinely joint occurrence and a lawful owner supplies the stable joint scope identity.

Future stochastic rules may bind only ADP-020 operations with exact semantics: `BERNOULLI_RATIONAL` with governed numerator/denominator; `UNIFORM_CANDIDATE` only with explicit equiprobability; `WEIGHTED_CANDIDATE_INTEGER` only with exact governed integer weights.

Authority v1 supplies **no universal encounter probability or weights**. Inventing one would violate the no-numeric-semantics/no-randomness-repairs-authority law.

## 10. Repetition and nonoccurrence

Repeated opportunity, encounter and exposure are lawful. Same subject may recur. One encounter may parent multiple distinct exposures when each has a distinct witness/effective identity. Exact replay-identical records deduplicate; changed time/parent/witness/candidate/RNG receipt is a distinct occurrence.

No minimum or maximum count is imposed by ADP-010.

Repetition does not imply intensity escalation, attention/salience, memory, belief, relationship, practice uptake, reinforcement/destabilization, V556-F2 satisfaction, or attractor movement.

Lawful nonoccurrence includes no available basis; no lawful opportunity candidate; valid-empty set; opportunity without encounter; encounter without exposure; future governed stochastic negative; negative applicability; deferred binding; or missing semantic authority. No cadence/schema may force an event.

## 11. Temporal / phase / position law

Actor event time is distinct from evidence time, resolver query time and proxy evidence time. No future proxy becomes past lived exposure.

`AVAILABLE`/`OPPORTUNITY` may be point or interval with explicit granularity; no finer time is fabricated. Encounter time must lie within the parent opportunity. Exposure may not precede encounter. Same-time encounter/exposure is lawful only as separate parent-linked semantic records.

Later context, migration or position changes are prospective and never rewrite prior OEE history. ADP-010 owns only its local parent order, not global same-time scheduler precedence. Hidden wall clock has no causal authority.

Universal actor phase precondition is only `V3DP_DEVELOPMENT_ACTIVE`; no lifecycle encounter quotas exist.

A rule may require an exact generated position/runtime binding by stable owner ref. Because ADP-009 is an unadjudicated sibling W1 cell, ADP-010 v1 assumes no position vocabulary or distribution. Geography/prevalence cannot fill a missing position. Required unbound position -> `DEFERRED` if it may lawfully arrive later, otherwise `MISSING_AUTHORITY`. Position constrains access only; it cannot encode personality, propensity, destiny or guaranteed exposure.

## 12. Provenance and replay

Minimum replay tuple preserves actor/causal-run; ADP-010 authority/registry/rule versions and hashes; ADP-008 phase state; exact parent OEE records; runtime repository/resolver selection receipts where used; exact structural refs and use permissions; generated runtime input/event/state receipts; evidence and query/proxy times; full reconstructible candidate set; ADP-020 decision/draw receipts and seed-lineage digests when stochastic; effective time/granularity; causal witness hashes; prior ledger anchor/index/hash; admitted event/effect and OEE record hash; and nonpositive decision receipts.

Replay law:

- identical immutable inputs/rules/candidates/RNG -> identical realization identity;
- changed rule version is semantic-rule divergence;
- changed candidate set is candidate-set divergence;
- changed seed/stream/draw coordinate is random-draw divergence;
- changed context creates a prospective decision, not historical rewrite;
- missing replay provenance blocks; no reseed/label reconstruction;
- V2 rendering is irrelevant to ADP-010 causal replay.

## 13. Forbidden inference/default court

Forbidden: structural row -> opportunity/encounter/exposure; V554 affordance -> lived exposure; V554 applicability -> encounter; V555 route -> traversal/exposure; shared V555 endpoint -> encounter; V556 co-resolution/F2 topology -> lived interaction/repeated exposure; co-location/co-presence -> encounter; opportunity -> encounter by default; encounter -> exposure by default; exposure -> response/absorption/memory/belief/relationship/route/interaction/development/attractor; geography/prevalence -> position -> forced opportunity; age/lifecycle -> encounter quota; empty candidate -> fallback; selected-empty -> first candidate; LLM/narrative plausibility/placeholder -> causal occurrence; future proxy -> past exposure; unnamed RNG -> causal choice; duplicate identity -> duplicate history; missing authority -> heuristic/default/random repair.

## 14. Hostile fixtures

| ID | Hostile case | Required result |
|---|---|---|
| HF-010-01 | structural V554/V555/V556 object present, no actor-specific transition basis | at most `AVAILABLE`; no lived transition |
| HF-010-02 | same place/time or co-presence only | `FORBIDDEN_INFERENCE` for encounter |
| HF-010-03 | shared V555 endpoint | no encounter inference |
| HF-010-04 | opportunity, no contact witness | `NONOCCURRENCE`; no encounter event |
| HF-010-05 | encounter, no exposure witness | encounter preserved; `NONOCCURRENCE`; no exposure event |
| HF-010-06 | exposure queried as response/memory/belief/relationship/type | no downstream fact without its owner |
| HF-010-07 | zero candidates | `VALID_EMPTY`; zero RNG; zero filler |
| HF-010-08 | legacy empty-set fallback event | reject |
| HF-010-09 | legacy selected-empty first-candidate fallback | reject |
| HF-010-10 | unnamed/global RNG | `INTEGRITY_FAILURE` / ADP-020 violation |
| HF-010-11 | stochastic rule lacks exact p/weights | `MISSING_AUTHORITY`; no draw |
| HF-010-12 | changed candidate set at same draw coordinate | ADP-020 `CANDIDATE_SET_DIVERGENCE` |
| HF-010-13 | actor `V3DP_GENERATION_PENDING` | no lived OEE history |
| HF-010-14 | required position but only geography/prevalence | `DEFERRED`/`MISSING_AUTHORITY`; no inference |
| HF-010-15 | same subject repeatedly exposed at distinct occurrences | distinct records; no escalation inference |
| HF-010-16 | replay-identical exposure submitted twice | idempotent dedupe |
| HF-010-17 | future proxy offered as childhood exposure | `FORBIDDEN_INFERENCE`; preserve evidence time |
| HF-010-18 | later context contradicts old opportunity | history immutable; new context prospective |
| HF-010-19 | exposure precedes encounter | `INTEGRITY_FAILURE` |
| HF-010-20 | encounter outside opportunity scope | no encounter; typed negative/integrity result |
| HF-010-21 | encounter and exposure same timestamp | separate parent-linked records; no collapse |
| HF-010-22 | label says “meeting,” no exact witness binding | `MISSING_AUTHORITY`/`FORBIDDEN_INFERENCE` |
| HF-010-23 | V556 F2 recurrence possibility | no repeated exposure inferred |
| HF-010-24 | schema expects >=1 yearly event | lawful empty/nonoccurrence wins |

## 15. Current terrain

At exact base, repository root contains `README.md`, `data/`, and `section85/`; no current top-level terminal V3 runtime package exists to canonize. `test_w03_v551j_v3_fail_closed.py` and `test_w03_v551j_v3_consumer.py` are upstream V551/V551J tests, not ADP-010 implementation, but directly confirm the current fail-closed style: unresolved/missing authority, wrong versions/hashes and typed empty/not-applicable states are not guessed through.

## 16. GOVERNING_SPIRIT_CHECK

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`.

**Genuine lawful ambiguity:** hard authority fixed the four noncollapsed states and no-filler law, but not whether lawful no-transition should survive only as absence or as an explicit receipt, nor whether one underlying occurrence carrying several OEE effects requires several top-level ledger events.

**Lawful alternatives:** (A) positive opportunity + absence of encounter; (B) positive opportunity + explicit nonoccurrence receipt; (C) one ledger event per positive OEE transition; (D) separate parent-linked OEE semantic records while one already-canonical event may carry multiple ordered typed effects.

**Chosen design:** B over A because explicit nonoccurrence is replayable evidence rather than inference from absence; D over C because it preserves semantic parentage without pseudo-event bloat.

**Decisive principles:** mediation where structure becomes life; historical causality without inevitability; divergent lawful lives from the same field; lawful absence/uncertainty; explicit provenance/randomness; minimum sufficient machinery; downstream vividness never exceeds upstream authority.

## 17. CONSUMER_RELEASE_SUFFICIENCY

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT` for `MUST-010`.

The OEE seam is fully specified for later implementation/consumption when ordinary RA-R00 gates permit. This does not release `V3-P5` or `V3-P9`. The absence of a universal stochastic encounter probability is intentional authority discipline: v1 witness-based realization is complete; any future stochastic domain rule requires an accepted ADP-010 registry amendment with exact ADP-020 parameters.

## 18. Final token

`ADP_010_V3_ENCOUNTER_EXPOSURE_AUTHORITY = PASS`
