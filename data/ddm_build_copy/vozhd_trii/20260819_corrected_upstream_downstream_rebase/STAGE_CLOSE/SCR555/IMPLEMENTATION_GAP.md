# SCR555 IMPLEMENTATION GAP — CURRENT V555 VERSUS ACCEPTED EXACT CONTRACT

## Status

This is an implementation-conformance map only.

Current production implementation is **not** semantic authority for SCR555. No production code is modified or authorized by this cell. Divergence recorded here does not reopen the accepted R03 broad topology.

Inspected current module at commanded base:

`data/ddm_build_copy/ddm_v555_life_course_mediation.py`

Blob SHA:

`f41ef8657f5f9fb07f57dc53ebaffadca3bbaf32`

## Executive disposition

The current module materially implements the superseded generic life-course slot/register scaffold rather than the accepted exact one-F1 atomic mediation-route contract.

Disposition:

`IMPLEMENTATION_CONFORMANCE_FAILURE__MIGRATION_REQUIRED_UNDER_LATER_SEPARATE_IMPLEMENTATION_AUTHORITY`

This is **not** `BROAD_TOPOLOGY_CONTRADICTION_FOUND`.

---

## G555-01 — Generic slot scaffold replaces canonical route compilation

Current `_slot_rows()` creates seven predefined mediation slots: household, family, parent, co-parent, child, carrier/institutional, and regional/locality.

The accepted V555 contract does not authorize universal fixed slot fanout. It requires a canonical route only when exactly one accepted V554 F1 matches an exact governed V555 route rule/shape.

**Required future migration:** replace/retire the slot-as-route semantic path with exact ADP-002 route-rule evaluation. Compatibility artifacts may exist only if they are demonstrably nonsemantic views over the canonical route objects and cannot reintroduce slot authority.

---

## G555-02 — Multi-F1 aggregation violates atomic grain

Current slot rows attach `source_v554_seed_affordance_ids_json` containing the broad seed-affordance ID set to each generic slot.

Accepted law is exactly one canonical accepted V554 F1 per V555 route. A set of F1s cannot be the semantic parent of one route merely because they share a run or slot.

**Required future migration:** route compiler consumes one exact canonical F1 reference at a time; duplicate route tuples deduplicate only after exact per-F1 route construction.

---

## G555-03 — Seed truncation creates information loss

Several current register builders enumerate `seed_rows[:5]`.

This is incompatible with the exact route grain because an arbitrary first-five cut can drop otherwise authorized atomic F1-derived routes and cannot be justified by V555 semantic authority.

**Required future migration:** no ungoverned top-k/first-N truncation. Every accepted F1 must receive its exact route-rule decision state.

---

## G555-04 — No canonical seven-field route identity

Current identifiers are primarily run/slot/register-derived strings such as `run_id__slot__...`, `run_id__household__...`, `run_id__parent__...`, and `run_id__handoff__...`.

They do not implement the accepted canonical semantic identity tuple:

```text
EXACT_V554_F1_REF
+ route_rule_id@route_rule_version
+ route_shape_id@route_shape_version
+ channel_structural_role_id
+ EXACT_STRUCTURAL_CHANNEL_REF
+ receiving_constraint_kind
+ EXACT_TARGET_RECEIVING_POSITION_REF
```

**Required future migration:** expose the exact tuple and a deterministic verifiable address/ID. Do not invent a canonical hash algorithm without separate authority; physical hashes remain locators over the semantic tuple.

---

## G555-05 — No exact ADP-002 route-rule decision engine

The current module does not visibly enforce exact `V555_MEDIATION_ROUTE_RULE_REGISTRY@1.0.0` matching, the first-tranche rule/shape, the exact nonnull structural channel requirement, no fuzzy fallback, unknown-version fail-closed behavior, or the exact receiver constraint.

Instead it emits generic unresolved mediation slots/registers.

**Required future migration:** implement the exact authority registry as the sole route-construction decision law.

---

## G555-06 — Typed route states are not represented at accepted granularity

Current output uses broad statuses such as `unresolved`, `generated_mediation_only`, and readiness scores. It does not implement the accepted distinctions among:

- `ROUTE_CANDIDATE_AUTHORIZED`;
- `VALID_EMPTY`;
- `V554_STRUCTURAL_USE_DENIED`;
- `NO_GOVERNED_ROUTE_AUTHORITY`;
- `ROUTE_BLOCKED_BY_GOVERNED_RULE`;
- `ROUTE_STATIC_AUTHORITY_MISSING`;
- `ROUTE_IDENTITY_UNRESOLVED`;
- `DEFERRED_RUNTIME_BINDING_REFERENCED_ONLY`;
- `CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE`.

**Required future migration:** emit exact typed route decisions and preserve them through publication/resolution. Generic unresolved/zero/missing-row substitution is nonconforming.

---

## G555-07 — Readiness scoring has no route-semantic authority

Current code computes bounded readiness/mediation scores using implementation-local constants and availability checks.

No accepted SCR555 authority permits readiness score to select a route, repair authority, supply route effect, or replace typed negative states.

**Required future migration:** any retained readiness score must be explicitly nonsemantic operational telemetry. It may not influence route identity, authorization, typed result, V556 relation authority, or publication permission unless separately governed.

---

## G555-08 — V554 F2 exact-reference-only contract is absent

Current legacy packet/register surface does not implement the accepted explicit separation:

```text
V554 F2 semantic meaning -> exact V554-owned reference only
V555 route-born predicate -> separately authorized ADP-003 meaning only
```

**Required future migration:** preserve relevant exact F2 producer references without copying/renaming/re-evaluating F2 semantics in V555.

---

## G555-09 — ADP-003 valid-empty route-born registry is absent

Current module does not expose the accepted `V555_ROUTE_BORN_PREDICATE_REGISTRY@1.0.0` valid-empty state or its strict ownership/evaluator firewall.

**Required future migration:** represent valid-empty explicitly. Do not populate route predicates from legacy slot labels, downstream consumer need, actor state, or route existence.

---

## G555-10 — Legacy channel labels are not accepted exact structural-channel refs

Current generic slot/channel values such as `household`, `family`, `parent`, `co_parent`, `child`, `carrier`, and `regional` are implementation labels. They are not authority to substitute for `EXACT_F1_STRUCTURAL_CHANNEL_REF` under the accepted first-tranche rule.

**Required future migration:** use the exact producer-governed structural channel reference carried by the accepted F1. No label rematch.

---

## G555-11 — V556 handoff does not express exact base-edge reuse

Current module writes a `v555_v556_handoff_index` keyed by legacy slot-derived handoff IDs and sets `allowed_v556_use` in the legacy scaffold, while accepted law requires V556 to consume the exact canonical V555 route identity as its base edge/participant.

EP555/SI-R02 evidence also records that the current downstream terrain mints separate pressure-flow-style identities rather than proving direct route-ID reuse.

**Required future migration:** V556 participant/base-edge references are exact canonical V555 route IDs/tuples; no one-to-one reminting.

---

## G555-12 — Direct V555 -> V557 publication path is not the controlling current model

Current code primarily presents V555 as a V556 handoff layer. Accepted R03 law permits independently runtime-authorized V555 routes to publish directly to V557 when no V556 higher-order meaning is required.

**Required future migration:** publication plumbing must not force a synthetic V556 wrapper. V557 independently governs runtime publication/use.

---

## G555-13 — Current V553 reads are not generic direct V555 semantic parents

The current module directly inspects several V553 artifacts/reports alongside V554 input. Under the accepted contract, V553 temporal lineage may remain important upstream of the accepted F1, but it is not automatically an independent V555 route-choice parent.

**Required future migration:** V555 route derivation consumes the accepted exact V554 F1/reference envelope plus exact V555 authority. Earlier V553/query/admission lineage remains producer-owned/transitive unless an exact future V555 rule explicitly names a producer field as a route argument.

---

## G555-14 — Replay identity is not separated cleanly from nonsemantic timestamps

Current artifacts include `created_at = utc_now()` widely. Timestamps are legitimate audit metadata, but accepted route replay forbids wall clock from affecting semantic route identity or decision result.

**Required future migration:** canonical route tuple/result/replay checksum excludes nonsemantic wall-clock/order entropy. Audit timestamps must be clearly segregated.

---

## G555-15 — Exact SCR554 F1/B1 seam cannot yet be implemented

The final M2 F1/B1 identity contract is intentionally absent because SCR554 has not yet returned an accepted stage-close result.

**Required future migration:** do not freeze production field names/schema/hash assumptions for canonical F1/B1 until accepted SCR554 supplies the exact contract. Bind the eight slots in `SEAM_HANDOFF.json` verbatim first.

This is a final-seam dependency, not a reason to delay or weaken the V555-local contract.

---

## Required future conformance suite

Any later implementation campaign should, at minimum:

1. construct fixtures for every case in `HOSTILE_TEST_ORACLE.md`;
2. prove one-F1 atomic route construction with exact ADP-002 matching;
3. prove exact tuple identity/dedup/different-F1 separation;
4. prove typed negative/valid-empty/missing/integrity preservation;
5. prove V554 F2 reference-only behavior and ADP-003 valid-empty semantics;
6. prove direct V556 base-edge reuse with no re-ID;
7. prove direct V555-to-V557 publication path without V556 filler;
8. prove exact immutable reference closure with producer directories absent where standalone packaging promises that capability;
9. prove replay under reordered input/nonsemantic timestamps;
10. if physical fusion is proposed, satisfy every equivalence obligation in `EXACT_CONTRACT.md`, not just rowset parity.

## Closure

Current V555 code is nonconforming to the accepted stage-close exact contract but supplies no counterexample to the R03 broad topology.

No code changes are authorized here.

`IMPLEMENTATION_GAP_RECORDED__NO_PRODUCTION_IMPLEMENTATION_PERFORMED`
