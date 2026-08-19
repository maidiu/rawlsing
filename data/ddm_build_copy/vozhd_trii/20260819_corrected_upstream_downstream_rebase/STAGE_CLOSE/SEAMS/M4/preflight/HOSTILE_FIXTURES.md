# M4 PREFLIGHT HOSTILE FIXTURES

**Authority:** `NON_DISPOSITIVE_PREFLIGHT_ONLY`  
**Final M4:** `NOT CLOSED`  
**Fixture posture:** contract-level proof surface; production implementation is not authorized.

These fixtures are derived from the pinned SCR553/SCR554/SCR555-local/SCR556-local/SCR5578 contracts and the accepted S5578C hostile feeder. Cases involving final V555/V556 producer seals are preflight-only until M2/M3 acceptance.

## Fixture result vocabulary

- `PREFLIGHT_PASS` — pinned contract law gives one exact expected outcome now.
- `PREFLIGHT_PASS__FINAL_M2_BINDING_PENDING` — shape is fixed but final V555 seal must come from accepted M2.
- `PREFLIGHT_PASS__FINAL_M3_BINDING_PENDING` — shape is fixed but final V556/V555 participant seal must come from accepted M3.
- `FAIL_CLOSED_REQUIRED` — any final implementation/seam must reject the attack.

## M4P-001 — raw producer directories absent

**Setup:** Build an immutable mixed-root V557/V558 bundle whose roots include one V553 producer object, one V554 F1, one local-shape V555 route and one local-shape V556 higher-order object. Package every required closure leaf or exact immutable hash-bound locator. Remove all raw V553/V554/V555/V556 directories from resolver visibility.

**Attack:** Resolver attempts ordinary query resolution.

**Required:** identical semantic candidate/selection result to the same immutable bundle with directories physically present; zero raw-directory access.

**Preflight:** `PREFLIGHT_PASS__FINAL_M2_BINDING_PENDING` and `PREFLIGHT_PASS__FINAL_M3_BINDING_PENDING` for the final V555/V556 seals. Standalone law itself is fixed.

## M4P-002 — missing positive dependency with surviving ID/hash text

**Setup:** A V554/V555/V556 root retains a referenced dependency ID/hash string but neither packaged bytes nor an exact immutable resolver contract.

**Attack:** Treat the hash text as sufficient closure.

**Required:** `MISSING_REQUIRED_TRANSITIVE_DEPENDENCY` / integrity failure. A hash without resolvable content is insufficient.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-003 — missing negative/limit authority

**Setup:** A root is positive only within a scope whose interpretation also requires a V553 `TEMPORAL_LIMIT`, V554 nonpositive context, or other producer negative/limit object. Omit that negative dependency.

**Attack:** Continue because the positive root bytes are intact.

**Required:** integrity failure. Do not reinterpret omitted negative state as no restriction or as positive absence.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-004 — packaging missing dependency relabeled semantic missing authority

**Setup:** A required producer object should exist and resolve, but its packaged blob is absent.

**Attack:** Return producer `MISSING_AUTHORITY` rather than packaging failure.

**Required:** reject rewrite. Physical missing required dependency is `INTEGRITY_FAILURE`; producer missing-authority semantics require an exact producer object/authority proving that semantic state.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-005 — current/latest authority substituted for historical authority

**Setup:** Root was produced under exact authority version/hash A. Bundle cannot resolve A; current registry exposes newer same-name authority B.

**Attack:** Substitute B.

**Required:** fail closed. No `latest/current/default` substitution.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-006 — mutable or fuzzy locator

**Setup:** Locator contains producer labels/path plus a mutable branch or database key, not an immutable target hash-bound resolution contract.

**Attack:** Resolve to whichever current object best matches labels.

**Required:** locator invalid; no semantic candidate admitted.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-007 — same producer object ID, different hash

**Setup:** Repository contains two objects with the same authoritative producer ID but different object hashes.

**Attack:** Pick newest or first.

**Required:** authoritative identity conflict / integrity failure.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-008 — V555 producer re-ID by locator

**Setup:** Local V555 route tuple is exactly bound. V558 assigns a locator and a V558 reference-graph arc ID.

**Attack:** Downstream treats the locator/arc ID as the semantic route identity and discards the producer tuple.

**Required:** reject. Producer V555 route identity remains canonical.

**Preflight:** `PREFLIGHT_PASS__FINAL_M2_BINDING_PENDING`.

## M4P-009 — V556 producer re-ID and V555 base-edge re-ID

**Setup:** Local V556 object references local-shape exact V555 route participants.

**Attack:** Packaging creates normalized V556 participant IDs and discards canonical V555 route refs.

**Required:** reject; V556 identity and its V555 participant identities remain producer-owned.

**Preflight:** `PREFLIGHT_PASS__FINAL_M3_BINDING_PENDING`.

## M4P-010 — role corruption with target hashes unchanged

**Setup:** Exact closure nodes/hashes are unchanged. Change an edge from `RECEIVER` to `SOURCE`, or otherwise change a producer-declared role.

**Attack:** Claim closure equivalent because target bytes are identical.

**Required:** `REFERENCE_ROLE_CORRUPTION`; closure digest changes and immutable bundle identity must change/fail.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-011 — order-significant participant swap

**Setup:** V555 route or an ordered V556 rule has exact participants and ordinals.

**Attack:** Swap order while keeping the same participant set.

**Required:** semantic order corruption; no equivalent object.

**Preflight:** V555 case `PREFLIGHT_PASS__FINAL_M2_BINDING_PENDING`; V556 case `PREFLIGHT_PASS__FINAL_M3_BINDING_PENDING`.

## M4P-012 — n-ary V556 dyadization

**Setup:** A governed V556 rule requires three exact participant occurrences.

**Attack:** Package two dyads or keep only two participants and call it equivalent.

**Required:** cardinality/role integrity failure. N-ary producer meaning remains n-ary.

**Preflight:** `PREFLIGHT_PASS__FINAL_M3_BINDING_PENDING`.

## M4P-013 — multiplicity collapse

**Setup:** Exact V556 rule permits/requires repeated occurrence of one route identity under distinct multiplicity indices.

**Attack:** Deduplicate repeated ID into one participant.

**Required:** multiplicity/cardinality mismatch.

**Preflight:** `PREFLIGHT_PASS__FINAL_M3_BINDING_PENDING`.

## M4P-014 — partial n-ary object accepted atomically

**Setup:** One required V556 participant cannot resolve; other participants verify.

**Attack:** Publish/resolve the surviving subset as a positive V556 relation/topology.

**Required:** fail closed; no partial positive object, no smaller inferred relation.

**Preflight:** `PREFLIGHT_PASS__FINAL_M3_BINDING_PENDING`.

## M4P-015 — producer context-only permission widened by V557

**Setup:** Producer allows `{REVIEW, CONTEXT}` only.

**Attack:** V557 emits active-causal capability.

**Required:** `INTEGRITY_FAILURE__FORBIDDEN_PERMISSION_WIDENING`.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-016 — V557 permission widened by resolver

**Setup:** V557 allows `REVIEW` only.

**Attack:** Resolver emits `CONTEXT` or `ACTIVE_CAUSAL`.

**Required:** fail closed.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-017 — root permission inherited by restricted dependency

**Setup:** Root may be active-causal; one indispensable dependency is context-only/review-only/denied.

**Attack:** Dependency inherits root capability because it is reachable through the root.

**Required:** reject. Dependency keeps its own permission ceiling; downstream use must narrow/defer/fail accordingly.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-018 — repository presence or READY collection grants permission

**Setup:** Item is present in a valid repository/ready collection but item-level V557 record is missing or denied.

**Attack:** Presence/readiness authorizes use.

**Required:** item denial/missing governance wins; repository presence is nonauthority.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-019 — PSEPF smuggled as structural root

**Setup:** Exact PSEPF ID/hash exists and is immutable.

**Attack:** Register it as a V557 root or V558 StructuralPriorRepository object because it is well-formed and content-addressed.

**Required:** structural-reference-class rejection. Immutability does not change ontology.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-020 — ActorComparatorReceipt / V3EmpiricalPossibilityInput smuggling

**Setup:** Exact comparator receipt or thin V3 possibility-input envelope is available.

**Attack:** Store/resolve as structural prior.

**Required:** reject. These remain outside structural repository semantics.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-021 — provenance reachability used as source pooling authority

**Setup:** Two source universes and their provenance are reachable from one closure graph.

**Attack:** Pool/average/link them because both are available.

**Required:** reject. Exact operation-specific composition/linkage authority is mandatory.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-022 — co-resolved V555 routes synthesize V556 meaning

**Setup:** Resolver independently selects two V555 routes sharing endpoint/time/geography; no producer V556 relation exists.

**Attack:** ContextResolver synthesizes an interaction/topology relation.

**Required:** reject `FORBIDDEN_RESOLVER_SEMANTIC_INFERENCE`; co-resolution is not V556 authority.

**Preflight:** `PREFLIGHT_PASS__FINAL_M2_BINDING_PENDING` for exact route identity; topology prohibition is already fixed.

## M4P-023 — nearest/fuzzy repair

**Setup:** Exact required object cannot be resolved. A similar label, nearest time/geography or high embedding similarity candidate exists.

**Attack:** Repair the missing reference.

**Required:** reject. No fuzzy/nearest/score/LLM/embedding repair.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-024 — raw-stage repair

**Setup:** Immutable bundle is missing a required object; raw producer directory contains a matching object.

**Attack:** Resolver opens raw stage and substitutes it.

**Required:** `V558_REPAIR_ATTEMPT` / fail closed.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-025 — network repair

**Setup:** Immutable bundle is incomplete; network service can fetch a newer or same-label object.

**Attack:** Fetch and continue.

**Required:** reject. Network state is not a semantic input.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-026 — partial immutable bundle visibility

**Setup:** Publication or repository manifests claim complete/ready but one required root, closure digest, governance record, locator graph, index or negative manifest is missing/mismatched.

**Attack:** Expose verified subset.

**Required:** `PARTIAL_ATOMIC_PUBLICATION` or equivalent integrity failure.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-027 — empty incomplete index relabeled valid-empty

**Setup:** Required index family is absent/incomplete and returns no hits.

**Attack:** Report producer `VALID_EMPTY`.

**Required:** `REPOSITORY_INDEX_INTEGRITY_FAILURE`; valid-empty requires exact producer-governed empty state.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-028 — valid-empty relabeled integrity failure

**Setup:** Producer explicitly emits governed valid-empty and its closure verifies.

**Attack:** Treat zero roots/result as failed package.

**Required:** preserve valid-empty as successful typed state; no filler object.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-029 — negative state collapsed to null/false/zero

**Setup:** Producer state is negative, unknown, noncomparable or missing semantic authority.

**Attack:** Serialize as null/false/0 and lose type/scope.

**Required:** reject semantic flattening.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-030 — byte-identical objects under distinct producer identities coalesced

**Setup:** Two producer objects have equal bytes but distinct authoritative identities/universes/builds.

**Attack:** Deduplicate semantically by content equality.

**Required:** reject. Hash equality alone never authorizes semantic coalescing across producer identities.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-031 — wall-clock/latest changes identical query result

**Setup:** Same immutable repo/index/query/policy/bindings are resolved twice with different wall clock/current registry state.

**Attack:** Result differs.

**Required:** identical considered set, SelectionRecords, receipt and context hashes.

**Preflight:** `PREFLIGHT_PASS`.

## M4P-032 — final M2/M3 local-contract promotion attack

**Setup:** Preflight local SCR555/SCR556 artifacts exist and are internally coherent.

**Attack:** Final M4 treats their local `WAITING_ONLY_FOR_EXACT_FINAL_SEAM` tokens as accepted final producer bindings without M2/M3 acceptance.

**Required:** reject. Import exact accepted values only through `FINAL_M2_M3_BINDING_SLOTS.json`.

**Preflight:** `PREFLIGHT_PASS`.

## Final execution order after M2/M3 acceptance

Final M4 should rerun, at minimum:

1. M4P-032 with accepted M2/M3 identities to prove no stale local binding remains;
2. M4P-008 through M4P-014 using exact final V555/V556 identities;
3. M4P-001 raw-directories-absent mixed-root fixture;
4. M4P-015 through M4P-018 permission chain;
5. M4P-019 through M4P-025 ontology/provenance/repair firewall;
6. M4P-026 through M4P-031 atomicity/state/determinism checks.

No preflight result substitutes for final M4 acceptance.

`M4_PREFLIGHT_COMPLETE`
