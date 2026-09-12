# M3 producer-result firewall repair specification R1

STATUS: `COURT_SPEC_ACCEPTED_FOR_GATE_FIREWALL_IMPLEMENTATION__NOT_YET_RUNTIME_AUTHORITY`

Applies only to the successor implementation of the PRE-V3 M3 higher-order structural producer firewall.

## 1. Defect being repaired

Current M3 positive admission proves exact M2 participant-route conditions, exact active V556 rule authority, and canonicalization/integrity of the produced object. It does **not** prove that the rule's `semantic_payload` belongs to an objective PRE-V3 semantic class.

The current `_contains_forbidden_person_semantics(...)` check is a recursive lexical rejection heuristic over mapping keys. It can reject literal `actor_state` while admitting semantically equivalent aliases such as `psychometric_type`, `motivation`, `preference`, or `psychological_trait`.

A positive result can therefore be content-addressed and replay-stable while still being in the wrong jurisdiction.

## 2. Required repair principle

A positive M3 object MUST be admitted only when its result is bound to an exact, competent, current **objective-world result contract**.

The proof direction is:

`EXACT ACTIVE RULE`
+
`EXACT OBJECTIVE RESULT CONTRACT BINDING`
+
`PAYLOAD CONFORMS TO THAT CONTRACT`
+
`RULE/RESULT BINDING IS CURRENT AND POSITIVE`
=
`M3 POSITIVE ELIGIBLE`

Absence of any term fails closed. Field-name blacklists MUST NOT be used as the positive proof of jurisdiction.

## 3. Required result-contract binding

The implementation successor must version the affected M3 rule/object contract rather than silently reinterpret the existing V1 `actor_independent` semantics.

Each positive-capable active rule must commit, directly or through an opaque authority-bound token, to all of the following semantic material:

1. `result_schema_ref`
   - exact id/version/content-hash reference;
   - no label-only, latest, default, fallback, or fuzzy resolution.

2. `result_semantic_owner_ref`
   - exact competent owner/authority for the result schema and its jurisdiction;
   - current and positive for the exact rule/result use.

3. `semantic_jurisdiction`
   - exact value `PRE_V3_OBJECTIVE_WORLD`.

4. `actor_indexing_mode`
   - exact enum `NO_ACTOR_INDEX` or `OBJECTIVE_ACTOR_INDEXED`.

5. `person_state_semantics`
   - exact value `FORBIDDEN`.

The binding itself must be included in rule identity/content-hash material or be an opaque capability content-addressably bound to that exact rule and evaluation. A caller must not be able to mint the binding by supplying raw labels.

## 4. Objective result-schema requirements

A competent objective result schema must define the allowed structure and semantic class strongly enough that arbitrary mappings cannot self-certify.

At minimum it must constrain:

- field set or typed structural grammar;
- field value types / enum domains where relevant;
- objective semantic class;
- participant/index roles;
- whether actor indexing is absent or objective-only;
- forbidden person-state jurisdiction;
- required exact refs and ref grammar where relevant;
- schema version and content hash.

The canonical payload must validate against the exact schema before `SUPPORTED` can produce a positive object. A mapping that is merely well-formed JSON/Python is not a result schema.

## 5. Person-state exclusion

M3 has zero authority to admit or synthesize, including under aliases:

- personality or psychometric type;
- belief or ideology as subjective state;
- affect;
- appraisal;
- preference;
- motivation;
- subjective disposition;
- psychological trait;
- actor uptake;
- actor interpretation;
- actor response;
- durable person-state;
- developmental/biographical state.

The failure reason is jurisdiction/schema nonconformance, not “the blacklist happened to notice the word.”

If a payload could be legal only after interpreting it as one of these person-state classes, M3 must fail closed.

## 6. Objective actor-indexed positive semantics

The repair MUST NOT equate “contains an actor reference” with “person-state.”

A schema with `actor_indexing_mode=OBJECTIVE_ACTOR_INDEXED` may lawfully describe an actor's institutional position, legal/material constraint, objective opportunity, membership/role in an objective structure, or objective world consequence attached to an actor identifier, provided the exact competent schema/authority says so and the payload contains no subjective uptake, appraisal, preference, motivation, trait, or other V3-owned realization.

Positive actor-indexed objects must carry their indexing mode explicitly in the versioned contract/object representation.

## 7. Disposition of existing `actor_independent`

The current V1 object invariant requires `actor_independent is True`.

That representation may not be silently redefined to mean both “no actor index” and “objective actor-indexed but nonpsychological.” GATE-FIREWALL must use a versioned successor contract/schema that represents the distinction explicitly.

Acceptable successor semantics include an explicit pair such as:

- `actor_indexing_mode = NO_ACTOR_INDEX | OBJECTIVE_ACTOR_INDEXED`;
- `person_state_absent = true`;

or an equivalent owner-approved typed representation. Exact field names remain implementation-level; the semantic distinction is mandatory.

## 8. Lexical heuristic disposition

The current forbidden-token scan may be removed if exact schema/authority validation subsumes it safely, or retained as defense-in-depth.

If retained:

- it MUST NOT be positive authorization;
- it MUST NOT reject an otherwise lawfully schema-bound objective actor-indexed result solely because an objective field contains `actor`;
- it MUST NOT be advertised as the semantic firewall.

## 9. Identity / replay requirement

For every positive M3 object, object identity/replay material must commit to:

- exact active rule identity;
- exact result-schema identity;
- exact semantic-owner/authority identity or binding hash;
- semantic jurisdiction;
- actor-indexing mode;
- canonical payload.

Changing the result schema, semantic owner, jurisdiction, or actor-indexing mode must change the replay/object identity.

## 10. Failure-state requirements

The successor must fail closed as follows:

- malformed exact schema/owner/binding ref -> integrity failure;
- exact supplied ref unavailable or hash/version mismatch -> integrity failure;
- exact object exists but authority is nonpositive/stale/out-of-scope -> typed nonpositive authorization/currentness result;
- payload fails exact result schema -> result-contract/schema nonconformance; no positive object;
- actor-indexed payload under `NO_ACTOR_INDEX` -> schema nonconformance;
- person-state payload under either indexing mode -> schema/jurisdiction nonconformance;
- no exact result binding -> no positive object.

No negative case may be converted into `SUPPORTED` by defaulting to a generic result schema.

## 11. Contract-drift protections outside M3

### PRE553 exact relation refs

A caller that supplies an exact relation ref that cannot be resolved has an integrity failure. Do not weaken this to an authorization error just to satisfy stale tests.

### relation-M1 producer uses

The shared M4 relation-M1 boundary must continue to reject raw caller-selected `producer_allowed_uses`.

The positive route must use a governed wrapper that derives adopted authority and supplies the sealed, evaluation-bound producer-use binding. The existing GT12 typed wrapper is the current positive control.

## 12. Implementation authority ceiling

GATE-FIREWALL may make only the smallest code/test/schema changes needed to implement this specification and align the three stale regression expectations.

It has zero authority from C07 to:

- alter the PRE-V3/V3 jurisdictional border;
- add psychological/person-state production to PRE-V3;
- create a universal driver/type terminal;
- weaken source relation exactness;
- weaken M4 producer-use authority;
- launder objective opportunity into subjective uptake;
- reject all actor identifiers categorically.

## 13. Qualification matrix

Implementation is not PASS until all hostile vectors in `03_HOSTILE_CASES.json` satisfy their expected outcomes, plus:

- original lawful structural M3 controls remain positive under exact schema binding;
- objective actor-indexed controls are positive under exact objective schema binding;
- the three regression-drift rows in `02_ERROR_AND_CALLER_CONTRACT_DISPOSITION.tsv` are resolved without production guard weakening;
- targeted tests pass;
- full relevant PRE-V3 regression passes;
- an independent hostile court verifies the implementation rather than relying on producer self-attestation.

Until then, the existing audit STOP on broad M3 firewall qualification remains.
