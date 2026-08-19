# SCR555 HOSTILE TEST ORACLE — V555 ATOMIC ROUTE

## Purpose

This oracle is the acceptance/falsification surface for the SCR555 exact contract. It tests the semantic object, identity, typed states, reference ownership, V556/V557 seams, replay behavior, and any future physical-fusion proposal.

A test marked **FINAL-SEAM** cannot pass until accepted SCR554 canonical F1/B1 identity is available. Every other test is fully specified now.

## Global oracle law

A conforming implementation MUST:

- use exactly one accepted V554 F1 per atomic route;
- apply exact V555 rule/shape authority;
- preserve `SOURCE -> MEDIATION_LOCUS -> RECEIVER` order;
- use the exact seven-field route identity tuple;
- preserve typed positive/negative/valid-empty/missing/deferred/integrity states;
- keep inherited V554 F2 producer-owned by exact reference;
- preserve ADP-003 valid-empty/nonduplication law;
- expose exact V555 route identity as the V556 base edge;
- allow direct V555-to-V557 publication eligibility when V556 adds no required meaning;
- fail closed on missing/mismatched/unknown authority;
- preserve exact replay/reference closure.

## Hostile cases

### H555-001 — Multi-F1 fusion
**Attack:** Two accepted V554 F1s share source/channel/receiver labels and are combined into one V555 route.  
**Required:** Reject. Emit two atomic routes if each separately matches a governed route rule; never one fused route.

### H555-002 — One exact F1, exact first-tranche rule
**Fixture:** One accepted F1 with exact positive structural-mediation permission/state, exact source/channel/receiver refs, and exact active V555 rule/shape.  
**Required:** `ROUTE_CANDIDATE_AUTHORIZED`, subject to successful exact identity resolution.

### H555-003 — StructuralEmpiricalAdmission bypass
**Attack:** Feed an admitted structural fact directly into V555 without an accepted V554 F1.  
**Required:** Reject semantic construction; no route.

### H555-004 — Raw empirical/discovery bypass
**Attack:** Use `EmpiricalFact`, `DiscoveryResultReceipt`, score, query row, or temporal observation directly to infer source/channel/receiver.  
**Required:** Reject.

### H555-005 — No active route-rule match
**Attack:** Valid accepted V554 F1 does not match any exact active V555 route rule.  
**Required:** `NO_GOVERNED_ROUTE_AUTHORITY`; no invented route.

### H555-006 — Required channel absent
**Attack:** First-tranche rule otherwise matches but exact nonnull governed `STRUCTURAL_CHANNEL_REF` is absent.  
**Required:** `NO_GOVERNED_ROUTE_AUTHORITY` unless a stronger integrity/missing-authority state applies.

### H555-007 — Fuzzy channel repair
**Attack:** Exact channel ref is missing but a similar label/embedding/name is available.  
**Required:** Fail closed; no descriptive/fuzzy repair. If an exact-ref corruption is involved, classify as construction/integrity failure rather than structural negative.

### H555-008 — Receiver generalization
**Attack:** Replace exact target receiving structural-position ref with a broader category or matching prose label.  
**Required:** Reject.

### H555-009 — Route role reordering
**Attack:** Serialize or interpret receiver/channel/source in a different semantic order while retaining the same fields.  
**Required:** Different/invalid semantic object; MUST NOT resolve as the canonical route.

### H555-010 — Duplicate same tuple
**Attack:** Same exact seven-field canonical tuple appears twice through duplicate upstream transit/order.  
**Required:** Deduplicate as one canonical route identity.

### H555-011 — Different F1, identical visible route labels
**Attack:** Two exact F1 identities have otherwise identical route-rule/shape/channel/receiver fields.  
**Required:** Two different route identities.

### H555-012 — Collection-order nondeterminism
**Attack:** Present identical canonical route inputs in different row/list/dict/filesystem order.  
**Required:** Same route identity set and same per-route typed results.

### H555-013 — V554 F2 copied into V555
**Attack:** Copy/rename a V554 F2 applicability predicate under a new V555 predicate ID.  
**Required:** Reject as foreign/duplicate jurisdiction. Preserve exact V554 F2 ref only.

### H555-014 — Exact V554 F2 reference
**Fixture:** Route carries exact immutable reference to relevant V554 F2 with no copied semantics.  
**Required:** Lawful. V555 does not claim evaluator ownership or runtime satisfaction.

### H555-015 — Empty route-born predicate registry
**Fixture:** `V555_ROUTE_BORN_PREDICATE_REGISTRY@1.0.0` contains zero predicates.  
**Required:** `VALID_EMPTY`; route family remains lawful.

### H555-016 — Consumer demands filler predicate
**Attack:** V556/V557/implementation requires at least one route predicate and invents one from route labels.  
**Required:** Reject; preserve valid-empty.

### H555-017 — Actor traversal as V555 condition
**Attack:** Route condition tests whether an actor encountered, traversed, believed, resisted, or remembered the route.  
**Required:** Reject as foreign actor/V3 jurisdiction.

### H555-018 — Cross-route V555 predicate
**Attack:** A V555 predicate depends on another route or says route A reinforces/blocks/reroutes route B.  
**Required:** Reject as V556 foreign jurisdiction.

### H555-019 — Effect inferred from route existence
**Attack:** Infer `TRANSMIT`, `BUFFER`, `AMPLIFY`, `DEFLECT`, `BLOCK`, strength, readiness, probability, or weight from channel/route existence.  
**Required:** No authorized effect. Current first-tranche effect state remains `VALID_EMPTY`; numeric semantics forbidden absent separate exact authority.

### H555-020 — V556 duplicate base edge
**Attack:** V556 creates a new one-to-one `PressureFlowEdge`/edge ID for a V555 atomic route.  
**Required:** Reject; V556 must reference the exact canonical V555 route identity.

### H555-021 — V556 reconstructs route from adjacency/shared context
**Attack:** Missing V555 route is inferred from shared endpoint/time/stratum/geography/source/channel/receiver, co-resolution, or storage adjacency.  
**Required:** Reject; no route and no V556 relation absent exact governed objects/authority.

### H555-022 — Additional mediation hop
**Fixture:** Source -> channel A -> intermediate receiver, then intermediate source -> channel B -> final receiver.  
**Required:** At least two atomic V555 routes; any governed composition belongs to V556.

### H555-023 — Direct V555 publication without V556
**Fixture:** `ROUTE_CANDIDATE_AUTHORIZED`, producer permission allows target runtime use, exact reference closure exists, no higher-order V556 meaning is required.  
**Required:** V555 object is eligible to be proposed directly to V557. V557 independently decides admission/use.

### H555-024 — Forced no-op V556 wrapper
**Attack:** Create a V556 object solely because all V555 routes are expected to pass through stage 556 before V557.  
**Required:** Reject as semantic bloat.

### H555-025 — Missing interpretation-critical transitive reference
**Attack:** Route tuple exists locally but exact producer authority/F1/F2 or required upstream reference closure cannot be resolved.  
**Required:** Fail closed; do not infer/repair semantic meaning.

### H555-026 — Mutable/latest/fuzzy reference substitution
**Attack:** Broken exact ref is repaired by latest authority, newest file, label match, default source, or fuzzy locator.  
**Required:** Fail closed.

### H555-027 — Provenance implies source composition
**Attack:** Because two upstream source lineages are both reachable behind routes, infer that they may be pooled/composed or jointly interpreted.  
**Required:** Reject.

### H555-028 — Wall-clock route identity
**Attack:** `created_at` changes route ID or semantic result on replay.  
**Required:** Fail conformance. Audit timestamps may differ only as nonsemantic metadata.

### H555-029 — Hash equality masks tuple mismatch
**Attack:** Physical locator/hash matches while a canonical identity field/reference differs or cannot be verified.  
**Required:** Fail closed.

### H555-030 — Rowset parity offered as physical-merge proof
**Attack:** Proposed fused V554/V555 implementation produces same final row count/rows but does not prove typed negatives, exact authority, V556 base-edge identity, direct V557 path, or replay equality.  
**Required:** Reject fusion proof as insufficient.

### H555-031 — Physical merge drops a typed state
**Attack:** Fused implementation maps `ROUTE_STATIC_AUTHORITY_MISSING`, `ROUTE_IDENTITY_UNRESOLVED`, denied, and valid-empty to one absent row.  
**Required:** Reject physical equivalence.

### H555-032 — Physical merge preserves all semantic/replay obligations
**Fixture:** Integrated implementation proves all eighteen obligations in `EXACT_CONTRACT.md` before every consumer.  
**Required:** Semantic contract permits physical co-execution/fusion in principle; this SCR does not itself authorize production implementation.

### H555-033 — Legacy generic slot scaffold
**Attack/terrain:** Current V555 creates generic household/family/parent/co-parent/child/carrier/regional slots, attaches broad seed sets, and truncates several seed-driven registers.  
**Required:** Classify as implementation nonconformance to accepted atomic route contract, not as semantic authority and not as broad-topology contradiction.

### H555-034 — Unknown future V554 signature
**Attack:** New/unknown V554 signature is treated as equivalent to one of the first-tranche accepted signatures based on field similarity.  
**Required:** `NO_GOVERNED_ROUTE_AUTHORITY`; new exact V555 registry authority required.

### H555-035 — Deferred V554 runtime binding treated as route denial
**Attack:** A structurally authorized route with an inherited deferred runtime/genealogy F2 reference is suppressed merely because runtime satisfaction is unresolved.  
**Required:** Preserve `DEFERRED_RUNTIME_BINDING_REFERENCED_ONLY`; do not assert satisfaction. Route remains structurally governed unless V554 structural-use authority itself denies use.

### H555-036 — Deferred V554 runtime binding treated as satisfied
**Attack:** Route existence is used to mark inherited V554 runtime/genealogy applicability satisfied.  
**Required:** Reject.

### H555-037 — FINAL-SEAM: missing accepted SCR554 F1/B1 contract
**Fixture:** SCR554 stage-close branch has no accepted contract beyond the common base.  
**Required:** `SCR555_WAITING_ONLY_FOR_EXACT_FINAL_SEAM`; fill no guessed F1/B1 identity fields.

### H555-038 — FINAL-SEAM: exact accepted SCR554 binding arrives
**Fixture:** Accepted SCR554 supplies the eight required F1/B1 binding slots with immutable exact identity/equality/replay law and no contradiction.  
**Required:** Bind verbatim; verify exactly-one-F1 route parent and replay; M2 can elevate the cell to `SCR555_EXACT_CONTRACT_CLOSED` without reopening independent V555 burdens.

### H555-039 — FINAL-SEAM: SCR554 contract contradicts frozen broad law
**Attack:** Accepted sibling contract would require multi-F1 route identity, direct admission->V555 bypass, F2 reownership, or another contradiction of frozen R03 topology.  
**Required:** Do not self-repair. Escalate under `SCR555_BLOCKED_AUTHORITY_CONFLICT` or `BROAD_TOPOLOGY_CONTRADICTION_FOUND` as actually supported.

## Acceptance condition

All non-final-seam cases H555-001 through H555-036 are closed by the exact contract and evidence. H555-037 currently applies because the sibling contract is absent. H555-038 is the only lawful normal transition to final local closure. H555-039 is reserved for an actual future contradiction, not presumed.

Current oracle disposition:

`ALL_INDEPENDENT_HOSTILES_CLOSED__ONLY_EXACT_SCR554_F1_B1_FINAL_SEAM_PENDING`
