# SCR555 EXACT CONTRACT — V555 CANONICAL ATOMIC MEDIATION ROUTE

## 0. Contract status and jurisdiction

This document freezes every V555-local exact-contract burden authorized by the accepted R03 stage-close campaign.

**Local status:** `CLOSED_ALL_INDEPENDENT_BURDENS`  
**Final status:** `WAITING_ONLY_FOR_ACCEPTED_SCR554_CANONICAL_F1_B1_BINDING`  
**Final token until M2 binding:** `SCR555_WAITING_ONLY_FOR_EXACT_FINAL_SEAM`

This contract does not modify production code, reopen D15, reopen the R03 broad DAG, retire any source/artifact, or legislate SCR554/SCR556/SCR5578-owned semantics.

Normative terms `MUST`, `MUST NOT`, `MAY`, and `FAIL CLOSED` are binding inside SCR555 jurisdiction.

---

## 1. V555 semantic object

The canonical V555 producer family is:

`STRUCTURAL_MEDIATION_ROUTE_CANDIDATE`

Its epistemic class is actor-independent structural possibility/prior. It is not an actor fact, encounter, opportunity, traversal, realized event, memory, belief, relationship history, biography, persona, or psyche.

A canonical V555 route MUST consume **exactly one accepted V554 F1**. It MUST NOT consume two or more F1s as one route. It MUST NOT use `StructuralEmpiricalAdmission`, raw `EmpiricalFact`, discovery output, V553 temporal objects, or actor state as a substitute semantic parent.

Additional mediation hops MUST be represented as additional atomic V555 routes. Any governed higher-order relation among those routes is outside this contract and belongs to V556.

---

## 2. Governed route authority

The controlling V555 route authority is:

`V555_MEDIATION_ROUTE_RULE_REGISTRY@1.0.0`

The active first-tranche rule is:

`V555-RR-001-EXACT-UPSTREAM-STRUCTURAL-CHANNEL@1.0.0`

The active first-tranche route shape is:

`V555-RS-001-SOURCE-EXACT-CHANNEL-EXACT-RECEIVER@1.0.0`

Unknown or later V554 authority/rule/signature versions MUST NOT be grandfathered, rematched by similarity, or interpreted through the first-tranche V555 rule. A new governed registry entry is required. Otherwise the route decision is `NO_GOVERNED_ROUTE_AUTHORITY`.

---

## 3. Route grain and ordered roles

The semantic route grain is:

```text
1 accepted exact V554 F1
× 1 exact V555 route rule/version
× 1 exact V555 route shape/version
× 1 exact mediation-locus/channel role
× 1 exact receiving structural-position constraint
```

The ordered route is:

### Ordinal 1 — SOURCE

Binding:

`EXACT_F1_SOURCE_STRUCTURAL_POSITION_REF`

The source reference MUST be the exact producer-governed structural-position reference exposed by the accepted F1 contract where required. Descriptive reconstruction is forbidden.

### Ordinal 2 — MEDIATION_LOCUS

Binding:

`EXACT_F1_STRUCTURAL_CHANNEL_REF`

Role identity:

`V555-LCR-001-EXACT-UPSTREAM-STRUCTURAL-CHANNEL`

The first-tranche rule requires an exact nonnull governed structural-channel reference. V555 MUST NOT invent, label-generalize, infer, or fuzzily repair a channel. Missing required channel authority yields `NO_GOVERNED_ROUTE_AUTHORITY` or a higher-priority integrity/missing state as applicable.

### Ordinal 3 — RECEIVER

Binding:

`EXACT_F1_RECEIVING_STRUCTURAL_POSITION_REF`

Constraint identity:

`V555-RC-001-EXACT-STRUCTURAL-POSITION-REF`

The receiver constraint uses exact-reference equality. It MUST NOT be generalized from prose/labels and MUST NOT assert that a runtime actor occupies or satisfies that structural position.

The order `SOURCE -> MEDIATION_LOCUS -> RECEIVER` is semantic and MUST survive serialization, publication, repository resolution, V556 participation, replay, and any future physical fusion.

---

## 4. Canonical route identity

The canonical semantic identity is the following ordered tuple:

```text
1. EXACT_V554_F1_REF
2. route_rule_id@route_rule_version
3. route_shape_id@route_shape_version
4. channel_structural_role_id
5. EXACT_STRUCTURAL_CHANNEL_REF
6. receiving_constraint_kind
7. EXACT_TARGET_RECEIVING_POSITION_REF
```

### 4.1 Equality law

- Same exact seven-field ordered tuple MUST resolve to the same canonical route semantic identity.
- A second occurrence of the same tuple MUST be deduplicated as the same route; it MUST NOT create a parallel semantic edge.
- A different exact V554 F1 identity MUST create a different route identity even when every visible label, endpoint, channel, time, or geography appears identical.
- Tuple order is constitutive.
- No omitted field may be reconstructed from weaker descriptive data.

### 4.2 Route ID versus route identity

ADP-002 requires deterministic serialization but does **not** create a canonical hash algorithm. Therefore SCR555 freezes the semantic identity as the tuple itself, not as any guessed digest format.

A concrete `route_id`, content hash, URI, database key, or locator MAY be a deterministic collision-safe address for the tuple. Such a physical identifier MUST NOT weaken semantic equality, hide tuple-field disagreement, or become a replacement ontology. An implementation must be able to recover/verify the exact tuple and owning authority behind the address.

---

## 5. Typed route-rule states

A conforming V555 implementation MUST preserve these distinctions.

### 5.1 Positive

`ROUTE_CANDIDATE_AUTHORIZED`

Meaning: exact positive accepted V554 F1 contract, exact active V555 route-rule match, required exact bindings/authority available, and canonical identity resolved.

### 5.2 Valid empty

`VALID_EMPTY`

Lawful examples include:

- accepted F1 input collection is empty;
- no input F1 matches an active V555 route rule and no stronger missing/integrity condition applies;
- an authority-owned optional list is explicitly complete and empty.

Zero routes is not an error when the governed result is valid-empty.

### 5.3 Semantic negative

- `V554_STRUCTURAL_USE_DENIED`
- `NO_GOVERNED_ROUTE_AUTHORITY`
- `ROUTE_BLOCKED_BY_GOVERNED_RULE`

These states MUST NOT be collapsed into one another, into `VALID_EMPTY`, or into missing output.

### 5.4 Missing/unresolved

- `ROUTE_STATIC_AUTHORITY_MISSING`
- `ROUTE_IDENTITY_UNRESOLVED`

Missing exact required identity/reference authority MUST NOT be repaired through label similarity, latest-version fallback, file order, or defaults.

### 5.5 Deferred inherited runtime binding

`DEFERRED_RUNTIME_BINDING_REFERENCED_ONLY`

This records lawful unresolved actor/runtime/genealogy applicability inherited from V554 F2. It is reference-only. It MUST NOT be asserted satisfied and MUST NOT be converted into a V555 route-born predicate. It does not independently block a structurally governed route unless the upstream V554 use decision denies structural use.

### 5.6 Integrity/construction failure

`CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE`

This includes schema/hash/reference/version corruption, invalid build/transport state, forbidden actor-scoped route construction, or fuzzy repair of an exact-ref failure.

Integrity failure MUST NOT be rewritten as a domain-semantic negative.

### 5.7 Precedence ceiling

A conforming decision procedure MUST respect at least this precedence ceiling:

```text
INTEGRITY FAILURE
  > explicit V554 structural-use denial / nonpositive F1
  > governed route-rule match + static authority resolution
  > route identity resolution
  > authorized / governed negative / valid-empty result
```

Unknown authority fails closed.

---

## 6. V554 F2 inheritance: exact-reference-only

V554 F2 meaning predates V555 route creation. Therefore it is never V555 route-born meaning merely because the route consumes an F1 from the same upstream object family.

A V555 route MAY expose a collection such as `inherited_v554_f2_refs` whose members are exact immutable producer references. The field name is V555-local transport syntax; the referenced identity and meaning remain V554-owned.

V555 MUST NOT:

1. copy V554 F2 semantic content into V555-owned predicate content;
2. rename/reword/specialize an F2 and claim a new V555 predicate ID;
3. run a V555-owned evaluator to determine V554 F2 truth;
4. replace an exact F2 reference with a label, description, or inferred condition;
5. assert actor/runtime satisfaction of an inherited deferred condition;
6. discard an interpretation-critical F2 merely because local payload duplication is removed.

Removing duplicate payload is lawful only when exact immutable V554 F2 dereference remains available wherever interpretation/replay requires it.

---

## 7. Route-born predicate authority and valid-empty law

The exclusive current route-born authority is:

`V555_ROUTE_BORN_PREDICATE_RULE@1.0.0`

Registry:

`V555_ROUTE_BORN_PREDICATE_REGISTRY@1.0.0`

Current status:

`VALID_EMPTY`

Registered predicate count:

`0`

A future predicate can enter this family only if it passes every ownership condition:

1. undefined before the exact canonical V555 route exists;
2. property/constraint of one exact route in isolation;
3. depends on exact route-local bindings;
4. not a V554 F2 restatement, rename, copy, specialization-by-copy, or re-evaluation;
5. no actor event/state/history dependency;
6. no multiple-route/V556 relation or prerequisite meaning;
7. separately accepted immutable owning rule/evaluator/argument schema.

A consumer's desire for a nonempty predicate list is never authority. `VALID_EMPTY` MUST survive publication and resolution as a positive authority state.

### 7.1 Unary route-local effects

The current first-tranche route rule authorizes no unary effect entries. `TRANSMIT`, `BUFFER`, `AMPLIFY`, `DEFLECT`, `BLOCK` are potential vocabulary only, not current semantics. No strength, readiness, probability, buffer/amplification magnitude, or combination weight is authorized.

---

## 8. V555 -> V556 seam

V555's canonical route identity is the sole canonical semantic base edge for V556 participation.

When V556 creates a governed interaction/topology object:

- it MUST reference the exact V555 route identity as participant/base edge;
- it MUST NOT mint a one-to-one replacement semantic edge for the same route;
- it MUST NOT infer a missing V555 route from shared context;
- it MUST preserve the V555 producer identity and route-local producer references.

The following never prove a V556 relation or recreate a V555 route:

- shared source;
- shared channel;
- shared receiver;
- shared endpoint;
- adjacency;
- time overlap;
- common stratum;
- common geography;
- co-resolution;
- storage adjacency;
- provenance reachability.

An additional mediation hop is another V555 route. Governed jointness among routes belongs to V556.

---

## 9. Direct V555 -> V557 publication eligibility

V556 is conditional, not mandatory transit.

A V555 route MAY be proposed directly to V557 when:

1. V555 state is `ROUTE_CANDIDATE_AUTHORIZED`;
2. the exact producer use-permission ceiling permits the intended runtime publication/use;
3. no V556 higher-order semantic transformation is required for the semantic object being published;
4. interpretation-critical producer/reference closure is exact;
5. V557 independently admits the object/use under its own governance.

V555 MUST NOT claim that producer authorization equals V557 publication authorization. V557 may narrow or deny. V555 also MUST NOT fabricate a V556 wrapper solely to preserve stage numbering.

---

## 10. Exact-reference locality

### 10.1 Must be carried or exactly bound at the route boundary

The route boundary MUST make the following exact material available without semantic reconstruction:

- `EXACT_V554_F1_REF`;
- exact source structural-position ref when required;
- exact structural-channel ref;
- exact target receiving-position ref;
- route rule ID/version;
- route shape ID/version;
- channel structural-role ID;
- receiving constraint kind;
- canonical ordered identity tuple;
- typed route decision state;
- exact V555 owning authority ID/version and immutable authority seal/reference.

These may be represented as immutable exact references rather than copied producer payload.

### 10.2 V554 F2 locality

Relevant F2 crosses only as exact immutable producer reference. Its semantic payload/evaluator remains at the producer authority or an immutable standalone closure copy controlled by that authority; V555 does not re-own it.

### 10.3 Normally transitive ancestry

Absent an exact future V555 rule that promotes a producer-owned field into a route-rule argument, these are normally transitive ancestry rather than independent V555 route-choice inputs:

- `EmpiricalQuerySpec`;
- `EmpiricalFact`;
- `StructuralEmpiricalAdmission`;
- V551/V551J identities;
- V552 structural fact;
- V552J association/admission/use-permission refs;
- V553 temporal key/observation/relation/limit refs;
- measure/weight/estimand authority;
- respondent-grain substrate identity.

They MUST remain exactly dereferenceable where required for producer interpretation/audit/replay, but need not be copied into every V555 object.

### 10.4 Fail-closed reference rule

Any interpretation-critical dependency that is missing, mutable, ambiguous, unresolvable, hash/version mismatched, conflicting, repaired by label, substituted by `latest`, or supplied by fuzzy/default fallback causes fail-closed behavior. Provenance reachability proves origin, never source-composition permission.

---

## 11. Replay contract

For a fixed exact accepted F1/F1-B1 binding, exact route authority/rule/shape, exact ordered bindings, exact relevant inherited refs, and exact authority bundle, V555 MUST deterministically produce the same semantic route identity and typed decision state.

The following MUST NOT affect semantic route identity/result:

- wall-clock timestamp;
- filesystem order;
- list/dict iteration order;
- row order when duplicate canonical tuples are equivalent;
- RNG;
- LLM judgment;
- fuzzy matching;
- mutable latest/default versions.

Audit timestamps may exist as nonsemantic metadata, but replay comparison must exclude them from route semantic identity.

If an implementation uses a route hash/ID, replay MUST verify it against the canonical tuple and exact authority/reference closure; hash equality alone cannot excuse a tuple/reference mismatch.

---

## 12. Physical fusion/recompute equivalence theorem

A future implementation may eliminate a separately materialized V555 stage only if it proves exact equivalence before every direct or indirect consumer.

The proof MUST establish:

1. exact accepted V554 F1 exists as a distinguishable semantic parent before route derivation;
2. accepted SCR554 F1/B1 binding is reproduced exactly;
3. exactly one F1 is consumed per route;
4. exact ADP-002 authority/rule/version/shape applies;
5. exact source/channel/receiver refs are used without repair;
6. same seven-field ordered canonical route identity exists;
7. source/locus/receiver role order is exact;
8. no structural direction is reconstructed from temporal-delta direction;
9. all typed positive/negative/valid-empty/missing/unresolved/deferred/integrity states are preserved one-to-one;
10. inherited V554 F2 remains exact-reference-only;
11. ADP-003 route-born ownership and valid-empty registry survive;
12. every interpretation-critical upstream authority/reference remains exact and deterministic to dereference;
13. V556 sees the exact same V555 route identity as base edge/participant;
14. V555 direct V557 publication remains possible without V556 filler;
15. actor-independent ceiling is preserved;
16. producer and downstream permission ceilings are preserved or narrowed, not widened;
17. identical fail-closed behavior occurs under missing/mismatched/unknown authority;
18. semantic object, identity, typed state, consumer behavior, and replay equality are proved.

Rowset parity, final aggregate equality, byte count, cache removal, module count, process count, or storage convenience are individually and jointly insufficient unless they imply the full proof above.

---

## 13. M2 final seam — deliberately unbound

Final SCR555 acceptance depends on accepted SCR554 canonical F1/B1 identity. The sibling branch currently has no stage-close commits beyond the common base, so no accepted contract exists to bind.

M2 MUST fill these slots from accepted SCR554 verbatim:

1. SCR554 accepted result head SHA and result token;
2. canonical F1 reference schema/authority identity and immutable seal;
3. canonical F1 identity tuple/order/equality law;
4. canonical F1 positive state and structural-mediation use-permission binding;
5. canonical B1 reference schema/authority identity and immutable seal;
6. canonical B1 identity tuple/order/equality law;
7. exact F1 <-> B1 binding/cardinality relation;
8. exact V554 authority/rule/signature references required to replay the F1/B1 binding.

SCR555 MUST NOT guess or rename those upstream fields.

B1 is not independently added to the seven-field V555 route identity by this contract. If accepted SCR554 makes B1 constitutive of the exact F1 reference, that fact arrives through the exact F1 reference contract at M2; otherwise V555 does not invent a new identity component.

If the accepted SCR554 contract contradicts any frozen R03 broad law or makes exactly-one-F1 route identity impossible, M2 must stop under the appropriate authority-conflict/topology-contradiction procedure. Otherwise the seam is a deterministic binding/checksum.

---

## 14. Closure statement

All V555-local exact semantics, negative states, reference ownership, V556/V557 boundaries, replay obligations, and physical-minimality proof obligations are closed.

The only remaining reason this cell does not emit `SCR555_EXACT_CONTRACT_CLOSED` is the intentionally unresolved exact SCR554 F1/B1 final seam.

Current cell token:

`SCR555_WAITING_ONLY_FOR_EXACT_FINAL_SEAM`
