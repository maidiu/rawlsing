# WSC001H — CROSS-SPINE SEAM CONTRACT R1

## Status and ceiling

This is an independent WSC001H candidate contract for central reconciliation.

It does not supersede any A-G seam proposal, because no sibling WSC001 branch was read. It is a compatibility floor derived from current PRE-MAIN plus the WSC000 central fan-in.

`CROSS_SPINE_CONTRACT_CANDIDATE != PROJECT_ADOPTION`.

## 1. Canonical conservation envelope

Every seam request and response must carry or exactly dereference the following fields when applicable.

| field | minimum meaning |
|---|---|
| `object_id` | exact stable identity of the object at its semantic grain |
| `object_type` | exact contract/schema type and version |
| `semantic_owner` | producer/authority that owns the meaning, not the carrier |
| `producer_authority_ref` | exact authority instance governing production |
| `current_selection_ref` | exact lifecycle/current-selection identity when currentness matters |
| `source_identity` | source/wave/context/question/variable identity as required by the producer |
| `universe_scope_risk_set` | exact operation-relevant universe/scope/risk set |
| `relation_or_query_id` | exact semantic relation, query, predicate or interface identity |
| `roles_cardinality_order` | participant role/cardinality/order/multiplicity when meaning-bearing |
| `consumer_id` | named downstream consumer/interface |
| `target_use` | exact use being requested |
| `consumer_permission` | exact permission ceiling for that use |
| `typed_state` | positive, zero, valid-empty, blocked, denied, noncomparable, unresolved, integrity failure, etc. |
| `negative_authority_ref` | exact authority for denial/blocker/abstention where one exists |
| `dependency_refs` | immutable upstream exact refs/hashes sufficient to reconstruct asserted meaning |
| `information_loss` | explicit declaration of compression/model/projection/rendering loss |
| `replay_contract` | deterministic replay/reconstruction procedure + exact historical authority bindings |
| `provenance_hash` | canonical digest over meaning-bearing envelope material |

A consumer may reject fields it does not need. It may not infer omitted authority from presence of adjacent fields.

## 2. Universal transition rule

For any hop `A -> B`:

`B.NEW_MEANING = ONLY_MEANING_EXPLICITLY_OWNED_AND_AUTHORIZED_BY_B`.

All upstream meaning remains owned by upstream producers and is carried by exact reference, lawful dereference, or losslessly preserved projection.

A lawful transition returns exactly one of:

- `POSITIVE`
- `OBSERVED_ZERO`
- `VALID_EMPTY`
- `ZERO_DENOMINATOR_ABSTENTION`
- `UNDEFINED_FOR_OBJECT`
- `OUT_OF_SCOPE`
- `DENIED`
- `UNRESOLVED_AUTHORITY`
- `NONCOMPARABLE` / `NO_TRANSPORT`
- `BLOCKED_EXPLICIT_AUTHORITY`
- `OBSERVABILITY_LIMIT`
- `INTEGRITY_FAILURE`.

No negative state is coercible to a positive value by defaulting, interpolation, nearest-match selection, storage presence, or later chronology.

## 3. Permission monotonicity

Absent a separately governed new authority:

`PERMISSION_OUT ⊆ PERMISSION_IN`.

A seam may narrow target use, scope, risk set, actor class, temporal window, or publication/rendering permission.

It may not widen permission because:

- an object is queryable;
- an object was materialized;
- a physical carrier contains more columns;
- the same label appears elsewhere;
- a downstream model can technically consume it;
- a later commit exists;
- replay succeeds.

## 4. Replay and provenance burden

Replay must prove the asserted **semantic result**, not merely regenerate bytes.

Minimum replay closure includes:

1. exact object/query/relation identity;
2. exact producer authority and current-selection identity;
3. exact source/universe/scope/risk-set bindings;
4. exact permission/target-use identity;
5. exact participant roles/cardinality/order where constitutive;
6. exact dependency refs/content hashes;
7. exact algorithm/rule/contract version;
8. exact negative-state and blocker logic;
9. exact information-loss declaration;
10. deterministic canonicalization/hash of the result.

Forbidden replay behavior:

- `latest`, `default`, `nearest`, fuzzy or best-effort authority selection;
- substituting a newer source for historical authority;
- treating repository presence as permission;
- reconstructing a broader semantic object than the one originally authorized.

## 5. SOURCE / CURRENT EMPIRICAL -> PRE-FF compatibility

### Semantic producer/owner
Current source-native producer plus exact source/candidacy/routing authority at its admitted grain. J01-A and C06 Contract@2 are delegated current surfaces, not global semantic owners.

### Consumer
PRE-FF governed empirical/query/discovery services.

### Minimum input identities
- exact source/wave/context/question/variable or source-structure identity;
- exact current source/candidate identity where required;
- exact C06 route/applicability identity where required;
- exact source relation kind;
- exact same-unit/respondent incidence if the query requires joint information;
- exact weight/denominator/estimand identity if the operation requires them;
- target-use permission.

### Minimum output identity
A producer-preserving `EmpiricalFact`, exact query result, exact discovery receipt, exact route/applicability result, or typed nonpositive result.

### Permissions
No source relation, respondent link, route entry, or source presence grants measurement portability, pooling, global composability, or structural admission.

### Typed negatives
Preserve unresolved C06 rows, source gaps, nonapplicability, valid emptiness, zero denominator, denied use, and integrity failures without fabrication.

### Existing reuse
`pre553_empirical_objects.py`, `pre553_empirical_query.py`, `pre553_empirical_authority.py`, `pre553_source_relations.py`, `pre553_source_equivalence.py`, discovery assets, replay audit, J01-A and Contract@2.

### Forbidden inferences
- marginals -> joint distribution;
- respondent identity -> global composability;
- common label -> measurement equivalence;
- source availability -> use permission;
- historical denominator -> current routing authority.

### Open gates
`OBL012;OBL016;OBL029;OBL030;OBL033`.

### GT0-compatible minimum
Use the bound real current source-structure fact `F0 = cssu.r1.afrobarometer.r1.005b474d6eb4253cb166` from `ba23b0f...` / blob `16edf3f...`. PRE-FF may query/reference its exact source-native relation identity, but may not infer respondent answer values or executable jointability from the source-structure record.

## 6. PRE-FF -> FIELD FORGE compatibility

### Semantic producer/owner
Upstream producer remains owner of empirical facts. FIELD FORGE may own only its separately authorized actor-independent structural-observatory relation/interface identity.

### Consumer
FIELD FORGE R2 structural-observatory interface.

### Minimum input identities
- exact upstream fact or lawful dereference;
- explicit typed relation or query identity;
- exact empirical unit/scope/risk set;
- consumer permission and negative authority;
- immutable dependency/provenance closure;
- deterministic replay/reconstruction law.

### Minimum output identity
A FIELD-FORGE-owned actor-independent relation/query/reference receipt whose payload retains exact producer refs and declares any information loss.

A direct producer-preserving reference receipt is sufficient for GT0 when no stronger FIELD FORGE relation is required. It does not re-own the upstream fact.

### Permissions
No universal geometry, local respondent carrier, configuration table, profile dictionary, graph, motif, or master payload is required.

### Typed negatives
Include `UNDEFINED_FOR_OBJECT`, `NO_TRANSPORT/NONCOMPARABLE`, `BLOCKED_EXPLICIT_AUTHORITY`, `OBSERVABILITY_LIMIT`, `INTEGRITY_FAILURE`.

### Existing reuse
Canonical FIELD FORGE R2 adopted-authority capsule; PRE553 exact query/replay machinery.

### Forbidden inferences
- producer fact -> FIELD/CAPITAL/HEGEMONY/HOMOLOGY/PRESSURE/MECHANISM;
- coordinate -> relation authority;
- same label/shared ancestry -> transport;
- information breadth -> claim sufficiency.

### Open gates
Claim-specific PRA/TTAR/estimand/weight/transport/strong-noun authority, plus `OBL005;OBL006;OBL040;OBL041;OBL042;OBL043` when a GT0 claim actually requires them.

### GT0-compatible minimum
Carry F0's exact source-native matrix-grid relation only as an actor-independent producer-preserving FIELD FORGE reference/relation receipt. Preserve the explicit ceiling `SOURCE_NATIVE_RELATION != EXECUTABLE_J != ACTOR_FACT`; use no strong noun and no transport.

## 7. FIELD FORGE -> PRE-V3 compatibility

### Semantic producer/owner
FIELD FORGE owns only the exact actor-independent relation/interface it constituted. Upstream empirical objects remain producer-owned. PRE-V3 producers own only separately admitted new temporal, affordance/equivalence, route, higher-order, publication or resolution meaning.

### Consumer
PRE-V3 structural admission and V553/V554/V555/V556/V557/V558 logical producers.

### Minimum input identities
- exact FIELD FORGE object/ref;
- exact upstream producer refs;
- exact structural target/use;
- exact admission authority;
- map/comparator/transport authority if cross-context comparison is required;
- typed negative and permission ceiling.

### Minimum output identity
An exact structural-admission result and, only where separately lawful, a V553/V554/V555/V556 object or V557/V558 publication/resolution entry.

Zero V556 objects is lawful.

### Permissions
Publication/resolution does not re-own producer semantics and does not select a physical repository winner.

### Typed negatives
`VALID_EMPTY`, `UNDEFINED_FOR_OBJECT`, `NONCOMPARABLE`, `BLOCKED_EXPLICIT_AUTHORITY`, denied publication/use, integrity failure.

### Existing reuse
`pre553_structural_admission.py`; `m1_temporal_v554_admission_dedup.py`; `m2_v555_atomic_route.py`; `m3_v556_higher_order_structural.py`; `m4_v557_v558_publication_repository.py`.

### Forbidden inferences
- FIELD FORGE relation -> downstream strong semantic noun;
- stage adjacency -> mandatory physical transit;
- publication -> semantic ownership;
- V556 topology -> realized actor history.

### Open gates
`OBL002;OBL003;OBL004;OBL034;OBL035;OBL036`, plus any claim-specific map/measurement/transport authority.

### GT0-compatible minimum
Because F0 proves source structure rather than respondent answer content, PRE-V3 must preserve it as a producer prerequisite/reference and return `UNDEFINED_FOR_OBJECT` or a narrower typed blocked/empty state for any requested actor/world structural assertion that requires unavailable empirical content. No V556 object is required.

## 8. PRE-V3 -> V3 compatibility

### Semantic producer/owner
PRE-V3 owns actor-independent structural possibility. V3 alone owns generated actor-indexed realization/history.

### Consumer
V3 developmental runtime / positive-transition owner.

### Minimum input identities
- exact generated-subject comparator identity;
- exact predicate ancestry;
- exact positioned-subject empirical possibility result;
- exact structural object/ref;
- exact transition/metabolism authority;
- exact target actor/generated-subject identity;
- causal parent/effective-time identity if a mutation is authorized.

### Minimum output identity
Either:
- a separately authorized V3 causal event/state transition; or
- explicit `DENY_ZERO_EFFECT` / typed blocked state with no actor mutation.

### Permissions
Empirical/structural authority never self-authorizes actor belief, identity, memory, encounter, action, choice, response or development.

### Typed negatives
`VALID_EMPTY`, `NONCOMPARABLE`, `UNRESOLVED`, `FAIL_CLOSED`, `DENY_ZERO_EFFECT`, missing positive-transition authority.

### Existing reuse
`source_backed_positioned_subject_possibility.py`; `v3_psepf_zero_positive_guard.py`.

### Forbidden inferences
- prevalence/probability -> individual prediction;
- positioned-subject possibility -> actor fact;
- proxy -> exact fact;
- exact fact -> actor belief;
- route existence -> route realization.

### Open gates
`OBL031;OBL032`; measurement/transport authority only when actually required.

### GT0-compatible minimum
The present baseline path is zero-effect. If no exact accepted positive-transition authority exists, the PSEPF guard must return `DENY_ZERO_EFFECT` and V3 state/history/RNG/scheduler remain unchanged.

## 9. V3 -> mediation -> V2 compatibility

### Semantic producer/owner
V3 owns generated truth/history and causal memory. Separate mediation owners must govern accessibility/recall, first-person claim permission and any situated phenomenology. Rendering owns wording only.

### Consumer
M6 actor-safe ingress, then bounded renderer/V2.

### Minimum input identities
- exact actor/generated-person identity;
- exact V3 claim/truth ref;
- exact accessibility/currentness binding;
- first-person permission;
- exact semantic-plan/render authority;
- scope ceiling and receiver snapshot;
- replay closure.

### Minimum output identity
One of:
- actor-safe claim/projection and separately admitted render plan;
- nonrenderable decision;
- blocked render outcome.

### Permissions
System-known truth is not actor knowledge. Actor-accessible truth is not automatic first-person permission. A permitted claim is not an automatic rendering plan.

### Typed negatives
concealed/inaccessible/noncurrent/unknown/uncertain/contradictory, denied first-person claim, deferred missing authority, nonrenderable, `BLOCKED_NAMED_AUTHORITY_REQUIRED`.

### Existing reuse
`m6_actor_safe_expression.py`; `render_bounded_expression.py`.

### Forbidden inferences
- V3 truth -> actor recall;
- memory -> present accessibility;
- accessibility -> first-person permission;
- permitted claim -> phenomenology;
- phenomenology -> wording;
- rendered text/session persistence -> V3 causal state.

### Open gates
Named owners for situated phenomenology/disclosure/semantic planning and positive render-plan authority where absent.

### GT0-compatible minimum
Because the GT0 PRE-V3 fact has zero actor effect under the current PSEPF guard, M6 must not manufacture a first-person claim from it. Rendering therefore returns a blocked/nonrendered result rather than text asserting the source fact as actor knowledge.

## 10. V2 -> V3 typed return compatibility

### Semantic producer/owner
The V2/render/session layer owns only its local output/event representation. V3 causal owner alone decides whether an observed in-world interaction becomes generated history.

### Consumer
V3 causal admission.

### Minimum input identities
- exact observable interaction type;
- exact actor/world participants;
- exact effective time;
- exact observation provenance;
- exact causal admission authority;
- exact parent/cursor/state fingerprint.

### Minimum output identity
An admitted V3 causal event or explicit no-effect/denied result.

### Forbidden inference
Transcript storage, narration, tone, rendered wording or session persistence is not causal history by default.

### GT0-compatible minimum
GT0 does not require a return event. Its V2 terminal is blocked/nonrendered, so the return path is `VALID_EMPTY/NO_EVENT`.

## 11. Compatibility theorem for central fan-in

Any A-G seam proposal is compatible with this H-lane cross-check if and only if it:

1. preserves the conservation envelope or an information-equivalent exact projection;
2. does not transfer semantic ownership through physical transit;
3. does not widen permission without new authority;
4. preserves typed negative states;
5. pins replay to exact authority/currentness/dependencies;
6. declares information loss;
7. preserves the PRE-V3/V3 actor firewall;
8. preserves V3 truth/memory/accessibility/claim/phenomenology/rendering separation;
9. keeps V2 noncausal absent typed V3 readmission;
10. leaves global physical topology unselected.

A seam can be narrower than this contract. It cannot be semantically weaker at any of those boundaries without an explicit competent override.
