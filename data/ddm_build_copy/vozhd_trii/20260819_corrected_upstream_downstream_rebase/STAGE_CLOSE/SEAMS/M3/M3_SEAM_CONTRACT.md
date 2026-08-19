# M3 — V555 -> V556 higher-order structural exact seam contract

**Contract:** `M3_V555_V556_HIGHER_ORDER_STRUCTURAL_EXACT_SEAM_CONTRACT@1.0.0`  
**Authority:** dispositive M3 seam checksum only  
**Result:** `M3_ACCEPTED__SCR556_EXACT_CONTRACT_CLOSED`  
**Broad topology:** unchanged  
**Production implementation:** forbidden

## 1. Seam purpose

M3 performs one job only: bind the already-accepted V555 producer identity/reference semantics into the already-accepted SCR556 higher-order participant boundary.

M3 does not:

- create a new V555 route identity;
- create a new V556 higher-order family or rule;
- add B1 or F2 to the V555 route tuple;
- rewrite source-composition law;
- change typed V556 outcomes;
- make V556 a mandatory forwarding stage;
- modify production code.

The accepted SCR556 waiting state is discharged because its three final upstream bindings are now exact.

## 2. Accepted immutable authority pins

M3 binds exactly:

```text
SCR555 head                 49a9ce7cd830eb670cf1f9d381d4d33e56ddf682
SCR555 EXACT_CONTRACT blob  8926500b7af442c0e07483442047aaad6cdeab63

M2 semantic package head    92128619122886d0ced877a29b42fdb453765246
M2 RESULT.json blob          15ddb28e9fe036f9e5ea5a60a924f549adcccc05
M2 seam-contract blob        cd974b514da5811feab5f7407b64e35cbde0a72c
M2 token                     M2_ACCEPTED__SCR555_EXACT_CONTRACT_CLOSED

SCR556 head                  9cfefc722f51cfab64952f004afef67fe65eb4a5
SCR556 EXACT_CONTRACT blob   f4e8146885b1145b116b173d2d4a148e3d55db4a
```

The later M2 administrative reassignment commit is excluded from the accepted M2 semantic package. Repository comparison proves the current M2 branch is exactly one commit ahead of `92128619122886d0ced877a29b42fdb453765246`, and that delta consists only of `STAGE_CLOSE/SEAMS/M2/00_NEW_ROLE_AND_TASK.md`.

The finite `M3_PREFLIGHT_COMPLETE` return is consumed as non-dispositive preparation only. Its findings have no power to override SCR555, M2, or SCR556.

## 3. Canonical V555 participant identity

SCR556's symbolic participant identity:

```text
SCR555_ACCEPTED_CANONICAL_ROUTE_IDENTITY_REF
```

now resolves exactly to the producer-owned V555 ordered tuple:

```text
1. EXACT_V554_F1_REF
2. route_rule_id@route_rule_version
3. route_shape_id@route_shape_version
4. channel_structural_role_id
5. EXACT_STRUCTURAL_CHANNEL_REF
6. receiving_constraint_kind
7. EXACT_TARGET_RECEIVING_POSITION_REF
```

M2 closes field 1:

```text
EXACT_V554_F1_REF = accepted canonical SCR554 F1_id
```

This seven-field ordered tuple remains the semantic route identity. A deterministic locator/hash/address may point to it, but only if exact immutable dereference reproduces and validates the producer-owned tuple. A locator is lookup machinery, not a replacement ontology.

### Equality law

- same exact seven-field tuple -> same canonical V555 route;
- any different tuple field -> different V555 route;
- a different canonical SCR554 F1 in field 1 -> different route even when channel/receiver and all visible labels coincide;
- hash/locator coincidence cannot excuse tuple mismatch;
- input/file/storage order is not route identity.

### Explicit nonmembers

The following do not become V555 route identity members at M3:

- SCR554 B1;
- inherited V554 F2 IDs or payload;
- V554 duplicate-equivalence/precedence machinery;
- V556 role/order/multiplicity fields;
- repository locator identity.

## 4. V556 participant binding

Every governed V556 evaluation binds `2..n` exact V555 route participant occurrences, subject to the exact V556 rule.

The accepted V556 participant occurrence shape remains:

```text
v555_route_identity_ref
role
ordinal_or_null
multiplicity_index
```

The whole V555 route reference is the participant semantic base. `role`, `ordinal_or_null`, and `multiplicity_index` are V556-owned higher-order relation metadata and never modify the V555 route identity.

### Distinct-route floor

A positive V556 higher-order evaluation requires at least two distinct canonical V555 route identities.

Duplicate rows or aliases of one route do not create two routes.

Same-route reuse is forbidden unless the exact V556 rule positively authorizes it and separately binds every occurrence. Even when same-route reuse is lawful, it does not mint occurrence-specific V555 identities and does not by itself satisfy the two-distinct-route floor.

## 5. Two separate order domains

V555 has an immutable internal route order:

```text
SOURCE -> MEDIATION_LOCUS -> RECEIVER
```

V556 may separately own an order among whole route participants when the exact higher-order rule says participant order is semantic.

These are different order domains.

A V556 ordinal may not reorder source/channel/receiver inside a V555 route. Conversely, V555 internal source/channel/receiver order does not determine the ordering of participants in a V556 relation.

For unordered V556 rules, canonicalization is based on exact route-identity bytes plus the exact role/multiplicity material required by the rule, never the input/file/storage/resolver order.

## 6. Route-state eligibility

Only:

```text
ROUTE_CANDIDATE_AUTHORIZED
```

is an accepted positive V555 route-bearing state that may proceed to V556 participant validation.

That state is necessary but not sufficient for `SUPPORTED`. V556 still requires:

- exact participant reference validation;
- exact V556 rule authority;
- exact role/order/cardinality/multiplicity compliance;
- required source-composition authority where applicable;
- positive governed evaluation of V556-owned higher-order meaning.

The following V555 states never become positive V556 participation merely because labels, locators, or partial payload survive:

```text
VALID_EMPTY
V554_STRUCTURAL_USE_DENIED
NO_GOVERNED_ROUTE_AUTHORITY
ROUTE_BLOCKED_BY_GOVERNED_RULE
ROUTE_STATIC_AUTHORITY_MISSING
ROUTE_IDENTITY_UNRESOLVED
CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE
```

`DEFERRED_RUNTIME_BINDING_REFERENCED_ONLY` remains V554-owned F2 exact-reference-only context. V556 does not evaluate it, satisfy it, or rename it.

M3 does not invent a second route-state policy. V556 may emit only its already-governed participant-validation or higher-order outcome while preserving the exact upstream state/reference.

## 7. Exact participant validation without reownership

SCR556 already says V555 route identity is opaque producer semantics. M3 reconciles opacity with exact validation as follows:

> V556 may verify that a supplied participant reference resolves exactly to the producer-owned V555 identity and its immutable authority/reference closure. It may not reconstruct, reinterpret, normalize, or replace that identity from its components.

At the V556 seam, exact validation must have or deterministically reach:

- M2-bound `EXACT_V554_F1_REF`;
- exact V555 source/channel/receiver bindings required by the route;
- V555 route-rule ID/version;
- V555 route-shape ID/version;
- exact channel-role and receiving-constraint identity;
- the ordered seven-field route tuple;
- exact V555 typed route state;
- exact V555 owning authority identity/version and immutable seal/reference;
- the accepted M2/SCR555 replay/reference closure required to validate the route.

Fail closed on:

```text
missing dependency
mutable locator
ambiguous reference
unresolvable reference
hash mismatch
version conflict
latest substitution
default substitution
fuzzy match
label repair
```

When the route reference itself cannot be validated, the accepted SCR556 outcome is `UNRESOLVABLE_PARTICIPANT`.

A resolved but noneligible upstream route state remains that exact upstream state and cannot yield positive V556 semantics. M3 does not collapse noneligibility into unresolvability.

## 8. No route reconstruction or re-ID

V556 may not produce a route participant from:

```text
run_id
mediation_slot_id
slot_name
slot_channel
source/channel/receiver labels
endpoint labels
time or geography
shared source or stratum
storage adjacency
co-resolution
provenance reachability
legacy route seeds
```

Nor may it bypass V555 with:

```text
StructuralEmpiricalAdmission
V553 temporal object
V554 basis/F1/B1 object alone
```

The accepted SCR554 F1 is visible inside field 1 of the exact V555 route tuple, but it is not itself a V556 participant. V556 consumes the complete canonical V555 route.

A repository locator is lawful only as an exact resolver to the producer identity. Repository presence never proves or creates route semantics.

## 9. V556 rule authority and higher-order ceiling

Every governed V556 evaluation must resolve one immutable semantic rule authority by exact ID/version/content hash.

That authority alone controls:

- semantic family;
- participant roles;
- participant order policy;
- minimum/maximum cardinality;
- multiplicity;
- same-route reuse;
- source-composition policy;
- allowed typed outcomes;
- producer allowed uses.

Missing, ambiguous, mutable-latest, label-selected, hash-mismatched, or conflicting-unresolved rule authority cannot produce positive semantics.

V556 remains higher-order only. It owns:

```text
V556_INTERACTION_RELATION
V556_TOPOLOGY
V556_ATTRACTOR_PREREQUISITE
```

A proposed additional atomic source/channel/receiver hop is another V555 route, not something V556 may smuggle into topology.

## 10. Source composition remains NONE_BY_DEFAULT

No semantic relation or composition is created by common context.

The following are never sufficient alone:

- shared source label;
- shared endpoint/receiver;
- shared channel;
- shared time;
- shared geography;
- shared stratum;
- storage adjacency;
- co-resolution;
- common labels;
- transitive provenance reachability.

Positive cross-source higher-order semantics require exact operation-specific authority covering the exact source universes, exact participant bindings, exact rule/operation, and exact compatibility/composition scope.

The accepted typed outcomes remain:

```text
SUPPORTED
VALID_EMPTY
DENIED
NONCOMPARABLE
UNKNOWN_AUTHORITY
CONFLICTING_AUTHORITY
INVALID_PARTICIPANT_SET
UNRESOLVABLE_PARTICIPANT
```

M3 creates no ninth state and no new precedence among the eight.

## 11. Typed-state preservation

`SUPPORTED` means the exact V556 rule evaluated positively under all required authorities.

`VALID_EMPTY` means the rule lawfully evaluated to empty/none. It is not missing data, denial, noncomparability, or silent omission.

`DENIED`, `NONCOMPARABLE`, `UNKNOWN_AUTHORITY`, and `CONFLICTING_AUTHORITY` remain distinct authority outcomes.

`INVALID_PARTICIPANT_SET` means a resolved participant set violates governed participant constraints.

`UNRESOLVABLE_PARTICIPANT` means an exact V555 participant reference cannot be deterministically resolved/validated without forbidden reconstruction.

Missing positive output has no implicit semantic meaning.

## 12. No filler and publication

If no exact governed V556 higher-order meaning is required:

```text
ZERO_V556_OBJECTS
```

The canonical V555 route may still proceed directly to V557 subject to V555 producer authority/permission ceiling and independent V557 publication/use governance.

V556 is not a mandatory wrapper. `ROUTE_CANDIDATE_AUTHORIZED` is not itself V557 publication permission, and V556 cannot widen either producer or V557 permission.

## 13. Replay

M3 seam validation is pinned to the exact accepted M2/SCR555/SCR556 blobs above.

V556 semantic replay preserves SCR556's accepted identity material:

- contract version;
- semantic family;
- exact V556 rule authority refs/hashes;
- exact participant binding sequence or rule-canonical multiset;
- exact composition authority refs/hashes where required;
- semantic payload;
- typed outcome.

The M2 pin is an exact seam-validation authority proving what the V555 participant reference means. M3 does not copy the M2 package into V556 semantic payload.

Identical immutable inputs must replay to identical identity/state. Unordered input permutation is inert. Ordered participant swap follows the exact rule and may change semantic identity or invalidate the candidate. Latest/fuzzy/default repair is forbidden.

## 14. Freshness guard

M2 declared itself stale if M1 later required a material SCR554 contract change.

M1 is now accepted and pins:

```text
SCR554 head = b5d745ac70c833324c8be0addf6c08ad72372263
```

which is exactly the SCR554 head accepted by M2. M1 reports no harmonization and no stage branch merge/rebase. Therefore M2 is not stale at this M3 close.

If a later higher authority materially changes SCR554 so that M2 must be re-adjudicated, M3 becomes transitively stale until the new M2 result is re-bound here.

## 15. Closure effect

All three SCR556 final upstream bindings are closed:

```text
SCR555_CANONICAL_ROUTE_IDENTITY_REFERENCE   BOUND
SCR555_ROUTE_STATE_ELIGIBILITY_FOR_V556     BOUND
SCR555_ROUTE_REFERENCE_CLOSURE               BOUND
```

No independent SCR556 rule/topology/composition/state holding changes.

The final stage transition is therefore:

```text
SCR556_WAITING_ONLY_FOR_EXACT_FINAL_SEAM
-> SCR556_EXACT_CONTRACT_CLOSED
```

and the M3 return is:

`M3_ACCEPTED__SCR556_EXACT_CONTRACT_CLOSED`
