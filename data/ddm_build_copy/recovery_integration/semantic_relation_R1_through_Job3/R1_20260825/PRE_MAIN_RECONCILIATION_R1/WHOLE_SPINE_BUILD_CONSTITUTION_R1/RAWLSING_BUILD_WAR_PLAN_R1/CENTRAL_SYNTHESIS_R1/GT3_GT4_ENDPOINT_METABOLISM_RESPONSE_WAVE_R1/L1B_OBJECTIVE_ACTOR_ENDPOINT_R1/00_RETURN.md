# GT3/GT4 L1B — OBJECTIVE ACTOR ENDPOINT FOR AN R5 DEMOGRAPHIC FIELD R1

## Terminal

`PASS__GT34_L1B_MINIMAL_OBJECTIVE_ACTOR_ENDPOINT_CANDIDATE_FOR_R5_DEMOGRAPHIC_DEFINED__NO_ADOPTION`

## Execution boundary

Repository:

`maidiu/rawlsing`

Branch:

`agent/rabochii-gt34-l1b-objective-actor-endpoint-for-r5-demographic-r1`

Exact working-ancestry start:

`972f51745bce3e2d491e71772f0b6ead4a78c288`

Immutable instruction ref used as evidence only:

`186d3dc8a7c69155bb240c59f84df1c895fc5666`

Worker:

`L1B — OBJECTIVE ACTOR ENDPOINT FOR AN R5 DEMOGRAPHIC FIELD R1`

Profile:

`SEMANTIC_AUTHORITY`

No implementation.
No adoption.
No PSEPF.
No actor mutation.

---

# 1. Central holding

One clean minimum can be defined:

**R5 field family: chronological age.**

The actor endpoint candidate is:

`V3_OBJECTIVE_CHRONOLOGICAL_AGE_FACT_RULE@1.0.0`

with fact schema:

`V3ObjectiveChronologicalAgeFact@1.0.0`.

Candidate semantic content hash:

`9565b215f59d11be78275a3709591f61bcc92dcd944977b64ba364c951c16c7a`

This candidate is deliberately narrower than a universal demographic initializer.

Its first lawful actor scope is only:

> a generated actor whose exact origin is an accepted ADP-015 `CHILD_GENERATED` event, whose child actor identity is exact, whose actor activation/current identity is exact under ADP-007, and whose birth-generation time and requested reference time are expressed under one exact chronology-capable V3 time basis.

For such an actor, chronological age at one exact reference time is a deterministic objective-biography fact.

It is not:
- belief;
- self-identification;
- structural position;
- prevalence imputation;
- caller assertion;
- a probabilistic demographic draw;
- a developmental phase;
- a personality/type claim.

Root/imported actors without an exact birth-generation anchor are **not** silently assigned age. They return `UNRESOLVED_BIRTH_ANCHOR`.

The candidate therefore closes only the actor-endpoint *contract* needed for a future age comparator. It does not create the R5 empirical endpoint, comparator authority, or any actor fact instance here.

---

# 2. Why age is the minimum

The physically evidenced Afrobarometer R5 demographic coverage inherited by this wave includes:

- sex: 51,587;
- age: 51,143;
- education_level: 51,461;
- income_level: 50,923;
- urban_rural: 51,587;
- religion_label: 51,587.

The frozen source identity is:

- source: `Data/Afro Barometer Round 5.sav`;
- SHA-256:
  `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`;
- rows: `51,587`.

Physical presence is evidence only.

Among these fields, age has the smallest lawful actor-side semantic burden because current accepted V3 already provides:

1. exact generated child origin identity and generation time;
2. exact actor identity/activation;
3. exact V3 causal-time identity;
4. explicit accepted law that chronological age is an independent fact;
5. deterministic replayable history.

No new stochastic population source is needed.

By contrast:

- **sex**: ADP-015 explicitly forbids child `sex_gender` without separate authority, and ADP-007 has no registered sex/gender initial-fact rule;
- **education**: no current objective education-history/fact owner was established;
- **income**: no current objective income fact owner was established;
- **urban_rural**: structural position/location cannot be relabeled as objective demographic truth;
- **religion_label**: belief, accessibility, or structural religion context cannot substitute for objective affiliation/self-identification.

Those fields need additional semantic source/owner law beyond the simple deterministic chronology relation.

Age is therefore not tied with another equally minimal endpoint.

---

# 3. Accepted authority evidence

## ADP-007 — actor identity/activation, not demographic truth

Accepted artifact:

`data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W2_AUTHORITY_CONTRACT_COMPLETION/ADP_007_V3_ACTOR_INITIALIZATION/AUTHORITY.json`

Blob:

`ede5008639e08720b4f72e8b470dfca5bc6fa8df`

Authority:

`V3_ACTOR_INITIALIZATION_RULE@1.0.0`

ADP-007 owns:

- prospective generated-subject admission;
- deterministic actor ID;
- `ACTOR_ENTITY_CREATED`;
- `ACTOR_ACTIVATED`;
- sparse initial checkpoint;
- admission of exact domain initial facts only under separately accepted semantic owners.

Its current registry:

`V3_INITIAL_FACT_RULE_REGISTRY@1.0.0`

has:

`registered_domain_initial_fact_rules = []`

and:

`valid_empty = true`.

ADP-007 further freezes:

> every future domain initial fact requires exact semantic owner + lawful source + constraints + selection authority.

Therefore this worker does **not** widen ADP-007 globally and does **not** add a generic age initial-fact rule there.

Age-at-reference is not an initialization default.

ADP-007 supplies only the exact actor identity/activation endpoint consumed by the candidate.

---

## ADP-015 — exact generated-child origin and generation time

Accepted artifact:

`data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W2_AUTHORITY_CONTRACT_COMPLETION/ADP_015_V3_RELATIONSHIP_GENEALOGY/AUTHORITY.json`

Blob:

`aeac88dfa35ae596d2ec35103b2f71ef72280b81`

Authority:

`V3_RELATIONSHIP_HOUSEHOLD_GENEALOGY_RULE@1.0.0`

ADP-015 owns:

- genealogy scope identity;
- child-generation admission;
- new child generated-entity reference identity;
- parenthood lineage;
- generation event identity/replay.

Its event contract contains:

`V3GenealogyEvent -> CHILD_GENERATED`.

Its child-generation identity explicitly binds:

- genealogy scope;
- parent actor IDs/history anchors;
- relationship/household prerequisites;
- **effective causal time**;
- exact generation trigger refs;
- candidate-selection receipt;
- canonical occurrence index.

It produces:

`V3GeneratedChildActorRef`

with:
- child_actor_id;
- generation_event_id;
- genealogy_scope_id;
- parenthood fact refs;
- initialization pending state;
- provenance;
- actor-ref hash.

ADP-015 explicitly excludes:

- universal sex/gender;
- universal age;
- fertility/reproduction biology;
- demographic inheritance.

That exclusion is respected.

L1B does **not** claim ADP-015 already owns chronological age.

Instead, the candidate consumes ADP-015's exact child-generation event as the objective birth-generation anchor for the narrowly scoped derived biography fact.

---

## ADP-008 — chronological age is already recognized as an independent fact

Accepted artifact:

`data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W0_AUTHORITY_FOUNDATION/ADP_008_V3_DEVELOPMENTAL_PHASE/AUTHORITY.json`

Blob:

`c6564c5c2793e9ed86ec0c5cecbcf84ff6f427d6`

Authority:

`V3_DEVELOPMENTAL_PHASE_RULE@1.1.0`

Its accepted `age_time_law` says exactly:

`chronological_age_is_independent_fact = true`.

It permits age/time to:

- validate chronology;
- be consumed by separately governed V3 rules;
- be recorded for audit/replay.

It forbids age from automatically implying:

- developmental phase;
- maturity;
- autonomy;
- legal status;
- personality;
- ideology;
- family role;
- school/work position;
- attractor state;
- biography beyond the exact age fact.

Replay requires:

`age/time source and chronology version when used`.

This is decisive evidence that a separate narrow chronological-age fact authority is architecturally lawful and does not collapse phase jurisdiction.

---

## ADP-021 — exact causal time exists, but no hidden year unit exists

Accepted artifact:

`data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W1_CRITICAL_AUTHORITY_EXPANSION/ADP_021_V3_HYBRID_SCHEDULER/AUTHORITY.json`

Blob:

`1db081786d2b7d4465a9efa7d69b6a05741b47bc`

Authority:

`V3_HYBRID_CAUSAL_SCHEDULER_POLICY@1.0.0`

The scheduler cursor binds:

- `time_basis_id`;
- `time_basis_version`;
- `current_effective_time`;
- causal history/cursors.

Its law is:

> effective time is monotone; **no universal time unit is defined**.

This prevents the forbidden shortcut:

`scheduler ticks == age years`.

The age candidate therefore accepts a positive value only when the exact referenced time basis supports the candidate chronology profile deterministically.

Opaque/unitless time returns:

`UNRESOLVED_CHRONOLOGY_BASIS`.

---

## CAN-014 — useful materialization mechanism, not the age semantic owner

Accepted artifact:

`data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W0_AUTHORITY_FOUNDATION/CAN_014_V3_DERIVED_SCHEDULE/AUTHORITY.json`

Blob:

`b132265582c8b687d978d7d15611afc1f80ca0d9`

Authority:

`V3_PURE_DERIVED_STATE_SCHEDULE@1.1.0`

CAN-014's registry is currently valid-empty and requires every future output registration to have its own:

- semantic authority ID/version/hash;
- evaluator ID/version/hash;
- evaluator-set identity;
- exact stored inputs;
- replay provenance.

CAN-014 explicitly does **not** own:

- semantic existence of individual derived outputs;
- formulas/taxonomies;
- semantic/evaluator authority.

Its purity law also says:

`may_create_generated_actor_fact = false`.

Therefore CAN-014 cannot be promoted into the actor-age semantic owner.

After future adoption/implementation, it may schedule or materialize a pure age view only under a separate exact registration consuming the age authority and exact evaluator identity.

---

# 4. Candidate authority material

Canonical semantic material:

```json
{
  "schema": "V3_OBJECTIVE_CHRONOLOGICAL_AGE_FACT_AUTHORITY_CANDIDATE@1.0.0",
  "authority_id": "V3_OBJECTIVE_CHRONOLOGICAL_AGE_FACT_RULE",
  "authority_version": "1.0.0",
  "owner": "V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE__OBJECTIVE_CHRONOLOGY_FACT_COURT",
  "jurisdiction": {
    "owns": [
      "objective chronological-age fact semantics for one exact generated actor at one exact reference time",
      "deterministic completed-years derivation under one exact chronology-capable time basis",
      "typed fail-closed age resolution outcomes",
      "immutable fact identity and replay provenance"
    ],
    "does_not_own": [
      "actor identity creation",
      "child generation or genealogy",
      "scheduler time-basis semantics",
      "developmental phase semantics",
      "structural position",
      "education income urbanicity religion sex_gender",
      "belief memory knowledge personality type attractor",
      "empirical R5 coordinate semantics",
      "comparator authority",
      "measurement portability",
      "actor mutation or causal state transition"
    ]
  },
  "v1_actor_scope": {
    "required_origin_class": "ADP015_CHILD_GENERATED",
    "required_child_ref_class": "V3GeneratedChildActorRef",
    "required_generation_event_family": "V3GenealogyEvent",
    "required_generation_event_kind": "CHILD_GENERATED",
    "required_actor_activation": "ADP007_ACTOR_ACTIVATED_OR_EXACT_CURRENT_EQUIVALENT",
    "root_or_imported_actor_without_exact_birth_generation_anchor": "UNRESOLVED_BIRTH_ANCHOR"
  },
  "fact_schema": {
    "schema_id": "V3ObjectiveChronologicalAgeFact",
    "schema_version": "1.0.0",
    "required_fields": [
      "age_fact_id",
      "actor_ref",
      "actor_identity_authority_ref",
      "birth_generation_event_ref",
      "birth_generation_event_effective_time",
      "reference_time_ref",
      "reference_effective_time",
      "time_basis_id",
      "time_basis_version",
      "chronology_profile_id",
      "chronology_profile_version",
      "age_value_completed_years",
      "resolution_state",
      "source_dependency_refs",
      "authority_ref",
      "replay_ref",
      "fact_content_hash"
    ],
    "value_domain": {
      "resolved_value": "NONNEGATIVE_INTEGER_COMPLETED_CHRONOLOGICAL_YEARS",
      "binary_float_forbidden": true,
      "age_band_not_part_of_fact": true,
      "age_label_not_part_of_fact": true
    }
  },
  "chronology_profile": {
    "profile_id": "V3_COMPLETED_CHRONOLOGICAL_YEARS_FROM_GENERATED_BIRTH_V1",
    "profile_version": "1.0.0",
    "accepted_time_basis_requirement": "birth and reference times must share one exact time_basis_id/version whose representation law supports deterministic completed-year chronology without wall-clock or inferred unit",
    "formula": "completed_years_between_exact(birth_generation_event_effective_time, reference_effective_time)",
    "negative_age": "INTEGRITY_FAILURE_REFERENCE_PRECEDES_BIRTH",
    "opaque_or_unitless_time_basis": "UNRESOLVED_CHRONOLOGY_BASIS",
    "wall_clock": "FORBIDDEN",
    "annual_tick_count_as_age": "FORBIDDEN",
    "phase_from_age": "FORBIDDEN"
  },
  "lawful_source_inputs": [
    "exact ADP-015 CHILD_GENERATED event/ref/hash and effective causal time",
    "exact V3GeneratedChildActorRef bound to that generation event",
    "exact ADP-007 actor activation/current actor identity ref",
    "exact V3 reference/effective-use time under a named time basis",
    "exact time_basis_id/version material sufficient for the chronology profile"
  ],
  "resolution_states": [
    "RESOLVED",
    "UNRESOLVED_BIRTH_ANCHOR",
    "UNRESOLVED_CHRONOLOGY_BASIS",
    "UNRESOLVED_REFERENCE_TIME",
    "STALE_REFERENCE_TIME",
    "NEGATIVE_AUTHORITY",
    "OUT_OF_SCOPE",
    "INTEGRITY_FAILURE"
  ],
  "generation_law": {
    "deterministic": true,
    "rng": "FORBIDDEN_NOT_REQUIRED",
    "prevalence_imputation": "FORBIDDEN",
    "caller_assertion_as_truth": "FORBIDDEN",
    "structural_position_as_age_source": "FORBIDDEN",
    "belief_or_self_identification_as_age_source": "FORBIDDEN",
    "fuzzy_crosswalk": "FORBIDDEN",
    "old_fact_rewrite_on_later_reference_time": "FORBIDDEN_NEW_REFERENCE_TIME_MINTS_NEW_FACT"
  },
  "replay_contract": {
    "required_identity": [
      "authority id/version/content hash",
      "actor ref and actor identity authority",
      "ADP-015 generation event ref/hash/effective time",
      "V3GeneratedChildActorRef",
      "ADP-007 activation/current actor ref",
      "reference time ref/value",
      "time basis id/version",
      "chronology profile id/version",
      "resolution state",
      "resolved integer age if any",
      "source dependency refs",
      "canonical serialization version"
    ],
    "same_inputs_same_fact": true,
    "mutable_latest": "FORBIDDEN",
    "filesystem_order": "FORBIDDEN",
    "wall_clock": "FORBIDDEN",
    "retroactive_rewrite": "FORBIDDEN"
  },
  "adp007_relation": {
    "global_adp007_registry_widening": "FORBIDDEN",
    "new_adp007_domain_initial_fact_rule_required": false,
    "reason": "age-at-reference is a chronology-derived objective biography fact, not an initialization default; ADP-007 remains actor identity/activation owner",
    "adp007_may_supply": "exact actor identity/activation reference only"
  },
  "can014_relation": {
    "can014_is_semantic_owner": false,
    "can014_may_schedule_or_materialize_after_separate_registration": true,
    "registration_requires": "this exact semantic authority plus a separate exact evaluator/evaluator-set identity",
    "can014_cannot_create_generated_actor_fact_by_itself": true
  },
  "r5_relation_ceiling": {
    "physical_field": "age",
    "physical_coverage_rows": 51143,
    "source": "Data/Afro Barometer Round 5.sav",
    "source_sha256": "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651",
    "empirical_coordinate_authority_created_here": false,
    "future_comparator_only_if": [
      "exact R5 native AGE variable semantics prove completed chronological years",
      "exact interview/reference time semantics are bound",
      "exact D08 conditioner-use authority is separately accepted",
      "actor fact is resolved at the lawfully aligned reference time",
      "missing/special R5 values remain typed",
      "no age-band or normalization crosswalk is silently inserted"
    ],
    "weakest_future_relation": "EXACT_INTEGER_AGE_EQUALITY_AT_EXACTLY_ALIGNED_REFERENCE_TIME",
    "measurement_portability_claim": "NONE"
  }
}
```

Canonical SHA-256 under repository semantic hash law:

`9565b215f59d11be78275a3709591f61bcc92dcd944977b64ba364c951c16c7a`

No current-selection/adoption effect is claimed.

---

# 5. Exact fact semantics

## Positive fact

Positive state:

`RESOLVED`

Value:

`age_value_completed_years`

must be an exact nonnegative integer.

Meaning:

> the number of complete chronological years elapsed from the exact accepted generated-birth anchor to the exact requested reference/effective-use time under the exact named chronology profile and time basis.

It does not mean:
- maturity;
- developmental phase;
- legal adulthood;
- school/work role;
- household role;
- structural class;
- belief;
- personality;
- actor response propensity.

## Birth-generation anchor

V1 accepts only:

`ADP015_CHILD_GENERATED`.

The candidate does **not** reinterpret generic ADP-007 actor creation time as biological/genealogical birth time for arbitrary actors.

The accepted child-generation event already says one new child actor was generated at one effective causal time.

The candidate owns only the derived chronological-age proposition from that exact origin and a later exact reference time.

## Reference time

Reference time must be:
- exact;
- V3-effective;
- under an exact `time_basis_id/version`;
- replayable;
- not wall clock;
- not mutable latest;
- not inferred from loop count.

A different reference time creates a different fact identity.

Old age facts remain immutable historical facts about their original reference time.

---

# 6. Fail-closed states

`RESOLVED`
- all exact identity, birth anchor, chronology basis and reference-time requirements pass.

`UNRESOLVED_BIRTH_ANCHOR`
- actor exists but no exact accepted ADP-015 child-generation origin is available in V1 scope.

`UNRESOLVED_CHRONOLOGY_BASIS`
- birth and reference times cannot be interpreted under one exact chronology basis capable of deterministic completed-year evaluation.

`UNRESOLVED_REFERENCE_TIME`
- exact requested reference/effective-use time is absent or unavailable.

`STALE_REFERENCE_TIME`
- a fact computed for one reference time is offered for a different required time without lawful recomputation.

`NEGATIVE_AUTHORITY`
- an exact authority/limit denies use or generation.

`OUT_OF_SCOPE`
- actor/source class is outside this V1 authority jurisdiction.

`INTEGRITY_FAILURE`
- ref/hash/actor/event/time-basis/replay mismatch, reference time precedes generated birth, or canonical identity fails.

No negative state is repaired using:
- prevalence;
- modal age;
- cohort average;
- parent age;
- generation phase;
- inferred year count;
- caller assertion;
- fuzzy label matching.

---

# 7. Replay/currentness

Every fact must content-bind:

- candidate authority ID/version/hash;
- actor ref and actor identity authority;
- exact ADP-015 generation event ref/hash;
- generated-child ref;
- generation event effective time;
- ADP-007 activation/current actor ref;
- reference-time ref/value;
- time-basis ID/version;
- chronology profile ID/version;
- typed resolution state;
- integer age when resolved;
- exact source/dependency refs;
- canonical serialization version.

Same exact inputs produce the same fact and hash.

Forbidden replay inputs:

- wall clock;
- filesystem order;
- mutable latest;
- hidden annual loop count;
- runtime incidental ordering;
- prevalence table;
- LLM output;
- V2 rendering.

A later reference time requires a new fact. It never rewrites the old one.

---

# 8. Relation to eventual R5 age coordinate

This worker does not create or promote an R5 empirical coordinate.

Current K1 already proved the accepted R5 PRE553 release exposes only a routing-only `COUNTRY_ALPHA3` coordinate, so a future R5 AGE endpoint still requires separate empirical authority.

The actor endpoint established here is designed so the eventual comparator can use the weakest possible relation:

`EXACT_INTEGER_AGE_EQUALITY_AT_EXACTLY_ALIGNED_REFERENCE_TIME`

**only if** a later empirical endpoint court proves all of the following:

1. exact R5 native AGE variable identity;
2. exact source question/coordinate semantics;
3. source-native value domain;
4. exact missing/special values;
5. exact respondent/routing semantics;
6. exact interview/reference-time semantics;
7. age means completed chronological years at that reference time;
8. exact D08 conditioner-use authority;
9. exact single-source/release/currentness;
10. exact actor/R5 reference-time alignment.

If R5 age is banded, transformed, top-coded, age-at-last-birthday under a different timing convention, or otherwise nonidentity, exact equality is **not** authorized.

That would require a separately named field-specific crosswalk/temporal rule.

No measurement-portability theorem is created or consumed.

---

# 9. Why this is objective biography

The fact depends only on:

- exact generated actor identity;
- exact generated child-origin event;
- exact causal time;
- exact chronology law.

It does not depend on:
- what the actor believes;
- what the actor remembers;
- how the actor self-identifies;
- structural classification;
- survey prevalence;
- inferred demographic similarity;
- rendered biography.

It is therefore an objective generated-biography fact.

The fact can be unknown/unresolved without filling the gap.

---

# 10. Why other R5 fields are not equal minima

## Sex

ADP-015's `V3GeneratedChildActorRef` explicitly forbids `sex_gender` without separate authority.

Its recovered/historical fixed-gender defaults are rejected.

ADP-007 has no current sex/gender domain rule.

A lawful sex endpoint would therefore require a new substantive generation/source owner beyond the endpoint contract itself.

## Education

No accepted objective generated education-history authority was found.

Education cannot be inferred from age, phase, class, household, structural position or survey prevalence.

## Income

No accepted objective generated actor income fact owner was found.

Structural class/material conditions are not exact income.

## Urban/rural

ADP-009 structural position/location cannot be relabeled into demographic residence/urbanicity.

A new objective residence/locality biography owner and source law would be required.

## Religion label

Belief/knowledge/accessibility are not objective religious affiliation/self-identification.

Structural or source religion context is not actor religion truth.

A separately owned objective affiliation/self-identification history would be required.

Thus age is uniquely minimal.

---

# 11. ADP-007 registry ruling

The correct first home is **not** a generic new ADP-007 domain initialization entry.

Reason:

- age changes with reference time;
- it is deterministically derived from generated history;
- it is not an initialization default;
- ADP-007 must remain actor creation/admission owner.

Therefore:

`new_adp007_domain_initial_fact_rule_required = false`.

If a later implementation chooses to cache age at activation for an ADP-015 newborn, that cached value does not enlarge ADP-007 semantics and does not replace the age authority.

---

# 12. Exact downstream prerequisite still open

This PASS defines only the actor endpoint candidate.

The future comparator path still needs:

1. accepted source-native R5 AGE PRE553 coordinate authority;
2. explicit D08 conditioner-use permission;
3. exact temporal alignment between actor age reference time and R5 interview/source reference time;
4. field-specific comparator authority;
5. comparator resolver/replay.

No comparator or empirical predicate is created here.

---

# 13. Disposition

One lawful minimum exists and does not require architecture redesign.

It is the objective chronological-age fact for ADP-015-generated child actors under exact chronology-capable time.

Candidate:

`V3_OBJECTIVE_CHRONOLOGICAL_AGE_FACT_RULE@1.0.0`

Candidate semantic hash:

`9565b215f59d11be78275a3709591f61bcc92dcd944977b64ba364c951c16c7a`

Fact:

`V3ObjectiveChronologicalAgeFact@1.0.0`

No adoption.
No implementation.
No fact instance generated.
No PSEPF.
No actor mutation.

`PASS__GT34_L1B_MINIMAL_OBJECTIVE_ACTOR_ENDPOINT_CANDIDATE_FOR_R5_DEMOGRAPHIC_DEFINED__NO_ADOPTION`
