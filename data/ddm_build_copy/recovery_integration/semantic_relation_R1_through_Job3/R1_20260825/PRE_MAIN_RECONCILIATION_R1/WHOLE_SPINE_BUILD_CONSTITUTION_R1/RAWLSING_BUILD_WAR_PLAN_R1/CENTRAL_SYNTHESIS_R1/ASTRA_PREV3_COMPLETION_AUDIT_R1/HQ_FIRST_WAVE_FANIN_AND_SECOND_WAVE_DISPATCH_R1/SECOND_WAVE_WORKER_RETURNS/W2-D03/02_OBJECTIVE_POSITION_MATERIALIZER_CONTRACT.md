# W2-D03 — Objective Position Materializer Contract R1

## Status

`PASS_CANDIDATE__PREV3_OBJECTIVE_POSITION_PRODUCER_OWNERSHIP_AND_MATERIALIZER_CONTRACT_R1_ONLY__REQUIRES_HQ_ADOPTION`

This artifact freezes the smallest contract candidate needed to close the **owner/materializer-authority grain** for C04-SO-002. It is not production code, does not populate a position world, and does not self-adopt authority.

Candidate identities:

- contract: `PREV3_OBJECTIVE_POSITION_MATERIALIZER_CONTRACT@1.0.0`
- positive fact schema: `PREV3_OBJECTIVE_POSITION_FACT@1.0.0`
- positive state: `POSITION_FACT_AUTHORIZED`
- positive fact identity: `PREV3POS:<semantic_hash(canonical_fact_material)>`

## 1. Governing authority and inherited ceilings

Current HQ second-wave authority adopts the C04 seven-operation docket and specifically authorizes W2-D03 to resolve the objective-position owner/materializer predecessor. C04-SO-002 requires real governed objective entity/actor-indexed position/relation facts with exact identity, provenance, permission ceiling, valid time/as-of basis and replay. C04-SO-003 and C04-SO-007 may depend on exact position refs but may not fabricate them.

Field Forge OBL005 remains current only as:

`FIELD_FORGE_OBL005_CLAIM_BOUNDED_POSITION_ROLE_AUTHORITY_AND_EVIDENCE_CONTRACT@1.0.0`

It is **not** a universal ontology and **not** a runtime classifier. Its positive receipt is exact to source/snapshot/context, actor grain, claim/docket/use, named competent role authority, supporting evidence, issued role/subrole, allowed use, negative ceiling, scope/time, provenance, replay and target-outcome firewall.

The C02 world-root law remains binding:

```text
WORLD_ROOT_OWNER != OBJECTIVE_POSITION_PRODUCER
OBJECTIVE_ACTOR_POSITION != PERSON_STATE
OBJECTIVE_WORLD_VALIDITY != V3_RUNTIME_CURSOR
```

The existing M2/V555 route runtime consumes exact `source_structural_position_ref` and `receiving_structural_position_ref` inside its exact F1 reference closure. It never authorizes D03 to manufacture either endpoint.

## 2. Jurisdiction allocation

There is no universal semantic position oracle.

A concrete positive objective-position fact has **distributed competent ownership**:

1. **Objective-position semantic owner** — the exact competent objective-domain authority that authorizes the asserted position/role meaning at the relevant domain/claim/context grain.
2. **Producer-authority owner** — HQ or an exact delegated objective-domain authority that designates a PRE-V3 materializer for that exact fact class/grain.
3. **Objective-position materializer** — only the exact designated PRE-V3 producer named by `position_producer_authority_ref`. It may hash and emit the fact after validation; it may not invent the position semantics or evidence.
4. **Source/claim evidence owner** — owns the source snapshot/context, exact claim and supporting evidence.
5. **Role-adjudication owner where applicable** — OBL005 or an exact domain-equivalent authority supplies the claim-bounded role receipt; absence of such authority cannot be repaired by labels or geometry.
6. **Valid-time/currentness owner** — owns the objective valid-time basis and currentness decision for the exact assertion.
7. **World-root owner** — binds already-authorized facts into the objective world; never acts as fallback producer.
8. **M2 / Field Forge** — downstream consumers of exact refs under their own operation authority.
9. **V3** — downstream person-side consumer only; no V3 request, subject receipt, runtime cursor or person state can establish PRE-V3 objective truth.

Sub-Vozhd II is the integration/implementation coordinator for this lane, not a substitute semantic owner for every domain.

## 3. Canonical positive input tuple

A materializer MUST receive a complete immutable tuple equivalent to:

```text
schema = PREV3_OBJECTIVE_POSITION_MATERIALIZER_CONTRACT@1.0.0

materializer_implementation_ref
position_producer_authority_ref
position_semantic_authority_ref

entity_or_actor_ref
objective_position_role_identity_ref

source_universe_ref
source_release_ref
source_claim_ref
source_claim_authority_ref
supporting_evidence_refs[]

position_role_receipt_ref | null
position_role_not_applicable_authority_ref | null
target_outcome_firewall_ref | null

applicability_authority_ref
applicability_receipt_ref

permission_authority_ref
allowed_uses[]
negative_ceiling_ref

valid_time_authority_ref
valid_time_basis_ref
currentness_authority_ref
currentness_receipt_ref

provenance_refs[]
dependency_refs[]
replay_authority_ref

predecessor_position_fact_ref | null
```

All `*_ref` values are exact immutable references containing semantic kind, object identity and content hash, or exact authority identity/version/content hash as appropriate. `latest`, `default`, fuzzy aliases and untyped hashes are forbidden.

`position_role_receipt_ref` is required when the asserted position/role is produced through OBL005-style claim-bounded role adjudication. If that adjudication is genuinely inapplicable because the position is directly constituted by another competent objective-domain source/rule, the tuple must carry an exact `position_role_not_applicable_authority_ref`; omission is not silent permission.

## 4. Positive validation law

A materializer may emit `POSITION_FACT_AUTHORIZED` only if all of the following are true:

1. `materializer_implementation_ref` exactly identifies the executing implementation/hash and is covered by the producer authority.
2. `position_producer_authority_ref` names this producer and covers the exact position fact class, source/claim, scope, use and temporal grain.
3. `position_semantic_authority_ref` competently authorizes the exact `objective_position_role_identity_ref`.
4. `entity_or_actor_ref` is an objective identity at the asserted grain and is not merely a V3 subject/person materialization receipt.
5. Source universe, release, claim, authority and supporting evidence resolve exactly and agree.
6. Any required OBL005/domain-equivalent role receipt binds the same actor grain, claim/docket/use, position/role, scope/context/time and supporting evidence.
7. OBL005 target-outcome/result-independence requirements are satisfied whenever the role adjudication is constitutive of the target claim.
8. Applicability is positively established at the exact entity/actor, context and time grain.
9. Requested/declared allowed uses are a subset of source, semantic-owner, producer and permission ceilings.
10. `negative_ceiling_ref` is preserved; absence/missing/noncomparability cannot be promoted to a positive fact.
11. Valid-time and currentness authorities resolve exactly; the currentness receipt covers the asserted position fact at the claimed as-of/interval.
12. Provenance and dependency refs are closed and immutable.
13. Deterministic replay over the same canonical tuple reproduces the same fact identity.
14. No forbidden person-state field or person-side inference is present.

A source name, questionnaire block, coordinate, embedding, geometric region, label/code, recurrence, favorable target result, downstream need, demographic category or shared measurement ancestry cannot satisfy any missing positive condition.

## 5. Canonical fact material and identity

For a positive result, canonical fact material is:

```text
schema
state = POSITION_FACT_AUTHORIZED
materializer_implementation_ref
position_producer_authority_ref
position_semantic_authority_ref
entity_or_actor_ref
objective_position_role_identity_ref
source_universe_ref
source_release_ref
source_claim_ref
source_claim_authority_ref
supporting_evidence_refs
position_role_receipt_ref | null
position_role_not_applicable_authority_ref | null
target_outcome_firewall_ref | null
applicability_authority_ref
applicability_receipt_ref
permission_authority_ref
allowed_uses
negative_ceiling_ref
valid_time_authority_ref
valid_time_basis_ref
currentness_authority_ref
currentness_receipt_ref
provenance_refs
dependency_refs
replay_authority_ref
predecessor_position_fact_ref | null
```

Canonical ordering is required for sets/lists whose semantics are unordered.

Identity:

```text
fact_hash = semantic_hash(canonical_fact_material)
fact_id = PREV3POS:<fact_hash>
fact_ref = {
  kind: PREV3_OBJECTIVE_POSITION_FACT,
  object_id: fact_id,
  content_hash: fact_hash
}
```

Changing the entity, position identity, source/release/claim, authority, evidence, permission, valid-time/currentness, dependency, replay or predecessor material yields a different fact identity. Old facts remain immutable historical evidence; a successor does not rewrite them.

## 6. Typed nonpositive result law

The materializer must fail closed with a typed state and no positive `PREV3POS:` fact when the corresponding requirement is not proved.

`EXPLICIT_NEGATIVE_OBJECTIVE_POSITION` is permitted only as a decision/negative-fact disposition backed by exact competent negative proposition authority and evidence; it is never inferred from failed positive proof. `UNAVAILABLE` is an explicit source/input availability state and never means false.

Frozen D03 result vocabulary:

```text
POSITION_FACT_AUTHORIZED
EXPLICIT_NEGATIVE_OBJECTIVE_POSITION
UNAVAILABLE
VALID_EMPTY
MISSING_POSITION_PRODUCER_AUTHORITY
MISSING_POSITION_SEMANTIC_AUTHORITY
MISSING_ROLE_AUTHORITY
MISSING_SOURCE_OR_CLAIM_AUTHORITY
MISSING_REQUIRED_EVIDENCE
IDENTITY_UNRESOLVED
APPLICABILITY_UNRESOLVED
USE_DENIED
MISSING_VALID_TIME_AUTHORITY
CURRENTNESS_UNRESOLVED
STALE_OR_HISTORICAL_NONCURRENT
NONCOMPARABLE
OUT_OF_SCOPE
INTEGRITY_FAILURE
```

Nonpositive state is evidence about the materialization decision, not the opposite objective fact. In particular:

```text
MISSING != FALSE
UNRESOLVED != NOT_POSITION
STALE != OPPOSITE_POSITION
NONCOMPARABLE != NEGATIVE_POSITION
VALID_EMPTY != UNIVERSAL_NEGATIVE
```

An explicit negative objective position assertion needs its own competent negative authority/evidence at that exact proposition grain; D03 does not infer it from failed positive proof. `UNAVAILABLE`, missing, stale and noncomparable states likewise remain nonpositive.

## 7. M2 / Field Forge handoff

D03 creates no route and no opportunity/constraint interpretation.

For C04-SO-003, an exact positive `fact_ref` may occupy the M2 closure fields:

- `source_structural_position_ref`
- `receiving_structural_position_ref`

only if the exact M2 route/shape/closure authorities independently authorize that use. D03 does not satisfy or bypass M2's route authority, F1 closure, structural channel ref, producer allowed-use proof or publication authority.

For C04-SO-007, exact position refs may be determinants of objective constraints/opportunities only under separately authorized claim-specific structural rules. They never prove actor uptake, interpretation, belief, preference, response, knowledge or development.

## 8. World/release and V3 firewall

The world root may include, publish, index or resolve an exact D03 position fact after normal publication/repository law. It cannot repair a missing position producer, semantic owner, source claim, time authority or currentness receipt.

Likewise:

```text
V3_SUBJECT_RECEIPT != OBJECTIVE_POSITION_FACT
V3_RUNTIME_CURSOR != OBJECTIVE_POSITION_VALIDITY
PERSON_STATE != POSITION_EVIDENCE
DEMOGRAPHIC_COORDINATE != OBJECTIVE_POSITION_FACT
```

The objective position fact may be actor-indexed without PRE-V3 owning the person.

## 9. Replay / invalidation

Replay keys include every canonical determinant listed in section 5. Same tuple -> same identity.

When a determinant is superseded, expires or is invalidated:

- preserve the old fact as historical immutable evidence;
- evaluate the exact affected fact under current owner/time authority;
- emit a separately identified successor only when the full positive tuple validates;
- propagate invalidation through explicit dependency refs only;
- do not perform a global actor reset;
- do not ask V3 to repair PRE-V3 currentness.

## 10. What this closes and what remains open

D03 candidate-closes the **GAP-PREV3-014 owner-allocation/materializer-contract predecessor** at the returned contract grain, subject to HQ adoption/narrowing.

It does **not** close GAP-PREV3-015 production/population. No generic materializer implementation or real source-backed position corpus is produced here.

Bounded successor candidate:

`PREV3_OBJECTIVE_POSITION_MATERIALIZER_IMPLEMENTATION_AND_REAL_SOURCE_POPULATION_R1_ONLY`

That successor may begin only after competent adoption/narrowing of this contract and must prove at least one real source-backed positive row plus typed nonpositive controls, deterministic replay, invalidation/currentness behavior and downstream exact-ref use without person-state leakage.

Successor gate: `GATE-POSITION-PRODUCTION`.
