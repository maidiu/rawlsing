# M3 PREFLIGHT HOSTILE FIXTURES

**Authority:** `NON_DISPOSITIVE_PREFLIGHT_ONLY`  
**Scope:** SCR555 -> SCR556 compatibility before final M2-bound literal V555 route-reference import.  
**Final M3 acceptance:** `FORBIDDEN IN THIS ARTIFACT`

These fixtures are contract oracles. They do not modify production code and do not authorize implementation.

## H-M3-001 — V556 route re-ID attack

**Given:** one exact canonical V555 route identity.  
**Attack:** V556 creates a new semantic `base_edge_id` from route labels, a fresh hash namespace, or normalized fields and treats it as the route.  
**Expected:** reject. The exact V555 identity remains the sole base-edge/participant identity. A V556-owned locator may point to it but cannot replace it.

## H-M3-002 — missing route reconstructed from run/slot labels

**Given:** no resolvable V555 canonical route reference; only `run_id`, `mediation_slot_id`, slot/channel labels, endpoint labels, or copied provenance are present.  
**Attack:** reconstruct a route participant.  
**Expected:** no participant reconstruction; fail closed as an unresolvable participant / authority failure. No positive V556 object.

## H-M3-003 — V555 internal order rewritten by V556 ordinal

**Given:** a valid V555 route with internal order `SOURCE -> MEDIATION_LOCUS -> RECEIVER`.  
**Attack:** use V556 participant ordinal to reverse or reorder those internal route roles.  
**Expected:** reject. V556 ordinal applies only to whole-route participant order under the higher-order rule.

## H-M3-004 — unordered relation depends on input order

**Given:** identical exact V555 participants, roles, multiplicities, rule authority, and payload, presented in different file/storage/input order.  
**Expected:** identical V556 semantic identity and outcome under an unordered rule. Canonicalization is by exact route-identity bytes plus higher-order role/multiplicity, never storage order.

## H-M3-005 — ordered relation participant swap

**Given:** an ordered V556 rule with exact route A at ordinal 1 and route B at ordinal 2.  
**Attack:** swap A/B while keeping every other field identical.  
**Expected:** the swapped binding is a different governed candidate or invalid under the rule; it cannot silently canonicalize to the original ordered relation.

## H-M3-006 — cardinality one

**Given:** a governed V556 rule invocation with only one exact V555 route participant.  
**Expected:** `INVALID_PARTICIPANT_SET`; no positive V556 meaning.

## H-M3-007 — one route copied twice to fake the two-route floor

**Given:** one exact V555 route identity appears twice under two aliases or duplicate rows.  
**Attack:** count the duplicates as two distinct routes.  
**Expected:** reject. Same canonical tuple is the same V555 route. Multiplicity does not create a second route identity and cannot satisfy the positive distinct-route floor.

## H-M3-008 — unauthorized same-route multiplicity

**Given:** at least two distinct route participants exist, plus one route is repeated.  
**Attack:** accept repeated occurrence when the V556 rule does not positively authorize same-route reuse.  
**Expected:** `INVALID_PARTICIPANT_SET`.

## H-M3-009 — authorized same-route multiplicity mutates route identity

**Given:** a V556 rule explicitly permits repeated occurrence of one route.  
**Attack:** mint occurrence-specific V555 route identities.  
**Expected:** reject. Occurrences are distinguished only by V556 participant binding/multiplicity metadata; the producer-owned V555 identity is unchanged.

## H-M3-010 — positive V555 route state bypass

**Given:** route state `VALID_EMPTY`, `V554_STRUCTURAL_USE_DENIED`, `NO_GOVERNED_ROUTE_AUTHORITY`, `ROUTE_BLOCKED_BY_GOVERNED_RULE`, `ROUTE_STATIC_AUTHORITY_MISSING`, `ROUTE_IDENTITY_UNRESOLVED`, or integrity failure.  
**Attack:** infer a participant from labels or a surviving locator.  
**Expected:** no positive participant. Preserve the exact upstream state by reference; V556 may emit only its own fail-closed validation outcome.

## H-M3-011 — V555 state renamed as V556 positive state

**Given:** exact upstream `ROUTE_CANDIDATE_AUTHORIZED`.  
**Attack:** copy/rename that state into a V556 `SUPPORTED` relation without evaluating an exact V556 rule over 2..n participants.  
**Expected:** reject. Route authorization is participant eligibility only; it is not higher-order relation authority.

## H-M3-012 — deferred inherited F2 promoted to satisfaction

**Given:** an otherwise exact V555 route carrying `DEFERRED_RUNTIME_BINDING_REFERENCED_ONLY`.  
**Attack:** V556 asserts the inherited F2 condition is satisfied, evaluates it, or converts it to route/interactions semantics.  
**Expected:** reject. F2 remains V554-owned exact reference-only context.

## H-M3-013 — cross-source composition from common provenance

**Given:** exact V555 routes from distinct source universes with reachable provenance but no operation-specific composition authority.  
**Attack:** compose them into one positive V556 relation.  
**Expected:** no positive semantics. `NONE_BY_DEFAULT`; return the appropriate noncomparable/unknown/denied/conflict state under the exact authorities.

## H-M3-014 — shared endpoint manufactures relation

**Given:** two exact V555 routes share receiver/endpoint but no exact V556 rule authorizes a relation.  
**Expected:** zero positive V556 relation.

## H-M3-015 — shared time/geography/stratum manufactures relation

**Given:** routes overlap in time, geography, or stratum and co-resolve from the same repository.  
**Attack:** infer interaction/topology.  
**Expected:** zero positive V556 relation.

## H-M3-016 — storage adjacency manufactures topology

**Given:** routes are adjacent in a parquet table, graph index, file, bundle, or resolver result.  
**Attack:** treat storage adjacency as a higher-order edge.  
**Expected:** reject.

## H-M3-017 — provenance reachability becomes composition permission

**Given:** every upstream authority/source object is successfully dereferenceable.  
**Attack:** treat successful provenance closure as permission to pool/compose sources.  
**Expected:** reject. Reachability proves origin/interpretation closure only.

## H-M3-018 — additional hop smuggled into V556

**Given:** a proposed structural path adds another source/channel/receiver hop.  
**Attack:** represent the new hop as V556 topology without creating the required new atomic V555 route.  
**Expected:** reject. Each additional atomic mediation hop is another V555 route; V556 owns only governed higher-order relations among routes.

## H-M3-019 — no higher-order meaning but filler V556 wrapper emitted

**Given:** one authorized V555 route is independently eligible for publication and no exact V556 higher-order rule is required.  
**Attack:** create a no-op V556 object solely to forward the route to V557.  
**Expected:** zero V556 objects; preserve direct V555 -> V557 path subject to producer permission and V557 admission.

## H-M3-020 — positive route state treated as publication permission

**Given:** V555 state `ROUTE_CANDIDATE_AUTHORIZED`.  
**Attack:** infer either V556-use permission or V557 publication permission solely from the route state.  
**Expected:** reject. Producer/use permission and V557 admission remain separate gates.

## H-M3-021 — unaccepted M2 worker result used as final M3 authority

**Given:** an M2 seam branch contains a worker-local result claiming acceptance, but parent acceptance has not been supplied to the final M3 adjudicator.  
**Attack:** bind final M3 from branch existence or mutable latest state.  
**Expected:** final M3 remains blocked. Only the parent-accepted M2 authority pin may fill `M3-FM2-01`.

## H-M3-022 — B1 added as an eighth V555 route field

**Given:** accepted M2 eventually proves B1 is required for positive-route permission/replay but SCR555 freezes B1 as not automatically part of the seven-field route identity.  
**Attack:** add B1 to `v555_route_identity_ref` as an eighth semantic member.  
**Expected:** reject unless a higher authority explicitly changes SCR555; M3 preflight has no such authority.

## H-M3-023 — M2 upstream machinery leaks into V556 participant semantics

**Given:** accepted M2 eventually exposes F1/B1 identity, V554 duplicate-equivalence, precedence, and replay authority.  
**Attack:** copy V554 dedup/precedence/F2 machinery into V556 participant identity.  
**Expected:** reject. Final M3 imports only the accepted M2 pin and the literal M2-bound route-reference resolution required to validate the frozen V555 identity.

## H-M3-024 — exact reference changes but visible route labels do not

**Given:** two V555 routes have the same visible source/channel/receiver labels but different canonical F1 identities and therefore different canonical route identities.  
**Attack:** collapse them as one V556 participant.  
**Expected:** reject. Exact canonical route identity, not visible labels, controls equality.

## H-M3-025 — hash match offered against tuple mismatch

**Given:** a locator/hash is claimed to identify a route but dereference reveals a seven-field tuple mismatch.  
**Expected:** fail closed. Hash/locator convenience never excuses semantic tuple inequality.
