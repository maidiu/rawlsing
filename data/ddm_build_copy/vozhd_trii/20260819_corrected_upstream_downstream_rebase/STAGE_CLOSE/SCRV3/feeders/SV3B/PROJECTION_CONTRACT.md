# SV3B — COMPARATOR PROJECTION CONTRACT

**Authority:** `NON_DISPOSITIVE_TO_SCRV3`  
**Scope:** candidate exact seam from an immutable objective actor-fact snapshot to `ActorComparabilityService` and `ActorComparatorReceipt`.  
**Broad topology:** unchanged.

## 1. Governing law

The accepted reverse lane is:

```text
objective generated actor fact refs / exact snapshot
  -> ActorComparabilityService
  -> ActorComparatorReceipt
  -> exact empirical conditioner predicate
  -> PossibilityFieldService / PSEPF
```

`ActorComparabilityService` is a mapper and comparability court. It does not create actor facts, source applicability, PSEPF geometry, actor belief, or V3 developmental state.

## 2. Positive projection requires two authorities

A positive projection requires both:

1. **fact authority** — the exact actor fact exists, is current/effective, immutable and owned by an accepted V3 semantic owner; and
2. **comparator authority** — an exact `ACTOR_EMPIRICAL_COMPARATOR_AUTHORITY` rule identifies how that fact class maps to one empirical coordinate for one source/universe/time/field context.

A fact owner's authority to create a fact is not comparator permission.

A comparator rule cannot manufacture a missing fact.

## 3. Candidate input record

Feeder candidate:

`ActorComparatorProjectionRequest@SV3B-0.1`

Required fields:

```text
projection_request_id
projection_request_schema_version
actor_id
objective_fact_snapshot_ref
objective_fact_snapshot_hash
requested_slot_id
comparator_authority_id
comparator_authority_version
comparator_authority_hash
comparator_rule_id
comparator_rule_version
comparator_rule_hash
empirical_universe_id
empirical_universe_hash
target_coordinate_id
target_coordinate_semantics_hash
source_historical_scope_ref
actor_snapshot_effective_time
temporal_alignment_rule_ref
temporal_alignment_rule_hash
predicate_grammar_authority_ref
predicate_grammar_authority_hash
request_hash
integrity_state
```

The request contains no raw PSEPF geometry, structural repository payload, belief, memory, persona, prompt, response, or source-population imputation.

## 4. Comparator rule contract

Every positive comparator rule must state at least:

```text
rule_id / version / content_hash
allowed_actor_fact_record_type
allowed_actor_fact_semantic_class
allowed_fact_owner_authority_id/version or exact owner family
allowed_fact_scope / role / dimension where needed
empirical_universe scope
empirical_coordinate identity + semantics hash
allowed projection form
actor-time -> source-time alignment rule
multiplicity semantics
normalization/crosswalk authority refs where used
positive result shape
negative / ambiguity / noncomparability behavior
```

No global “same label means same meaning” rule is authorized.

## 5. Allowed projection forms

The D15 comparator authority permits only exact governed forms such as:

- exact value equality;
- versioned normalization/crosswalk;
- range or band containment;
- historically governed geographic hierarchy;
- source-specific construct equivalence;
- temporally conditional equivalence;
- explicit `NOT_LAWFULLY_COMPARABLE`.

Each form must be rule-bound and source/time specific.

Fuzzy semantic similarity, nearest label, nearest geography, nearest cohort, generic embedding similarity, LLM judgment, majority mapping, or population prevalence are not allowed projection forms.

## 6. Generated structural position

`V3StructuralPositionFact` is objective V3 truth when lawfully created by ADP-009, but D15 explicitly denies it generic comparator-key status.

Therefore:

```text
V3StructuralPositionFact exists
DOES NOT IMPLY
may condition survey coordinate
```

A positive mapping is lawful only if the exact comparator rule explicitly names:

- the ADP-009 fact record/dimension;
- its owner authority/version/hash;
- the target source coordinate and semantics;
- the temporal relation;
- the projection form.

Absent that exact rule: `NO_COMPARATOR`.

String equality such as actor position label `urban` and source coordinate label `urban` is insufficient.

## 7. Household / relationship facts

Objective ADP-015 facts may be comparator candidates only through an explicit rule.

Examples:

- `V3HouseholdMembershipFact` may support a source household-membership coordinate if the rule establishes semantic role equivalence.
- `V3ParenthoodFact` may support a parenthood coordinate if separately mapped.
- objective relationship lifecycle facts may support a marital/relationship coordinate only if the relationship kind and source construct are exactly governed.

Forbidden substitutions:

- `V3ActorPerceivedRelationshipState` -> objective relationship coordinate;
- transcript/session tone -> relationship status;
- shared household -> marital status by implication;
- parenthood -> cohabitation/marriage by implication.

## 8. Material / embodied facts

CAN-009 actor state is objective causal state, but its dimensions have bounded semantics that may differ from survey constructs.

Examples:

```text
MATERIAL_MONEY_CAPACITY != survey income by default
MATERIAL_JOB_INSECURITY != employment status by default
MATERIAL_MOBILITY_CAPACITY != migration/travel status by default
ORGANISMIC_VITALITY != health category by default
```

A comparator rule may map an exact dimension only if a source-specific construct-equivalence authority proves the mapping for the requested use/time. Numeric-scale resemblance is not authority.

## 9. Missing generic demographic facts

D15 names candidate families such as age/time, sex/gender, education, language, religion/sect self-identification, ethnicity, income, employment and occupation. That list is an eligibility frontier, not a V3 fact registry.

At the inspected accepted authority base:

- ADP-007 has an empty generic domain initial-fact registry;
- ADP-015 explicitly does not supply universal sex/gender/age semantics;
- no generic accepted V3 owner was located for education, language, religion/sect self-identification, ethnicity, income, employment status or occupation.

Thus source coordinates in those families return `ACTOR_PROPERTY_MISSING` or `NO_COMPARATOR` unless a separately accepted objective fact owner exists for the actor and an exact comparator rule maps it.

## 10. Hard-prohibited actor-side sources

The projection court must reject these as objective comparator facts:

- `ActorEpistemicStateSet`, beliefs, knowledge, uncertainty, nonknowledge;
- `GeneratedMemoryState` or recall state;
- persona, voice, V2 phenomenology, expression plan, rendered output;
- simulated response or response move;
- `V3ActorPerceivedRelationshipState` as a substitute for objective relationship truth;
- structural context / `ResolvedStructuralContext`;
- PSEPF itself;
- source-coordinate labels;
- population prevalence or modal category;
- caller/user assertion content merely because ADP-019 admitted the occurrence of the assertion.

## 11. Typed result states

Authoritative D15 comparator result states remain:

- `ACTOR_PROPERTY_MISSING`;
- `NO_COMPARATOR`;
- `AMBIGUOUS_COMPARATOR`;
- `TEMPORAL_NONCOMPARABLE`.

Feeder candidate also requires fail-closed integrity states before those semantic outcomes:

- `COMPARATOR_REQUEST_INTEGRITY_FAILURE`;
- `SNAPSHOT_HASH_MISMATCH`;
- `FACT_OWNER_AUTHORITY_MISSING`;
- `COMPARATOR_AUTHORITY_MISSING`;
- `COMPARATOR_RULE_HASH_MISMATCH`;
- `SOURCE_COORDINATE_SEMANTICS_MISMATCH`.

No integrity/missing state may be converted to a negative actor fact or a default coordinate value.

## 12. Positive receipt

A positive `ActorComparatorReceipt` must bind:

```text
actor_id
objective_fact_snapshot_ref/hash
exact actor fact ref/hash + fact owner authority
effective actor time
comparator rule id/version/hash
empirical universe id/hash
empirical coordinate id/semantics hash
source/historical scope
exact temporal alignment result
exact resolved predicate AST/hash
match cardinality
semantic transformation/crosswalk refs if any
receipt identity/hash
```

The receipt proves only:

> this exact actor fact set lawfully maps to this exact empirical conditioner under this rule/source/time context.

It does not prove source applicability for the eventual reverse field; `SERVICE_SOURCE_APPLICABILITY_AUTHORITY` remains separate.

## 13. Multi-property conditioning

When multiple objective properties are requested, positive comparator receipts produce one exact conjunction over respondent-coordinate incidence.

Required law:

```text
same-respondent conjunction
!= multiplication of independent marginal probabilities
```

If one required property is missing, ambiguous, noncomparable or unauthorized, the exact conjunction is not silently weakened by dropping that property.

Any optional-property semantics must be explicit in the query/comparator authority.

## 14. Source applicability remains separate

Comparator success does not authorize a source universe for reverse inference.

After a positive comparator result, `SERVICE_SOURCE_APPLICABILITY_AUTHORITY` may still return a typed nonapplicability/noncomparability result. No broader/regional/global source may be substituted merely because a local source fails.

## 15. Receipt downstream role

`ActorComparatorReceipt` has one direct semantic role: exact possibility-field production.

In V3:

```text
ActorComparatorReceipt = transitive provenance / replay only
```

Forbidden:

- standalone V3 comparator prior collection;
- comparator score -> actor propensity;
- comparator mapping -> actor identity/persona;
- comparator result -> V2 expression semantics.

## 16. Replay

Comparator replay binds:

- exact objective snapshot ID/hash;
- actor fact refs/hashes and fact-owner authorities;
- comparator rule ID/version/hash;
- source universe + coordinate semantics;
- temporal alignment rule;
- predicate grammar authority;
- exact projection result / predicate AST;
- implementation version where algorithmically relevant.

Forbidden replay dependencies:

- mutable latest authority;
- hidden wall clock;
- current source catalog in place of historical universe identity;
- row/file order;
- fuzzy remapping;
- network lookup not content-bound;
- LLM judgment.

## 17. Parent acceptance invariant

SCRV3 should preserve this exact order:

```text
owned fact existence/currentness
-> comparator rule eligibility
-> exact projection
-> typed receipt
-> separate source applicability
-> field production
```

No earlier or later stage may re-own an omitted gate.
