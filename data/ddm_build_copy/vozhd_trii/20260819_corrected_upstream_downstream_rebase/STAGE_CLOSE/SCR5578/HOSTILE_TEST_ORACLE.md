# SCR5578 Hostile Test Oracle

**Contract:** `SCR5578_PUBLICATION_REPOSITORY_RESOLUTION_EXACT_CONTRACT@1.0.0`  
**Execution posture:** normative hostile oracle; production implementation is not authorized by this file.

A future implementation or M4 seam must pass every applicable test. Tests marked `FINAL_SEAM` require the exact accepted SCR553–SCR556 contracts and therefore cannot be honestly executed to final acceptance while those branches remain at the common base.

## A. Mixed publication / no transit filler

| ID | Attack | Required result |
|---|---|---|
| PUB-01 | Exact runtime-authorized V553 object is forced through synthetic V554/V555/V556 wrappers before V557. | `FAIL`: direct V553→V557 root is allowed when producer contract authorizes it. |
| PUB-02 | Exact runtime-authorized V554 object is forced through V555/V556 only for publication. | `FAIL`: direct V554→V557 publication. |
| PUB-03 | Exact V555 route with no V556 meaning is forced into a one-to-one V556 wrapper. | `FAIL`: V555 route publishes directly; V556 wrapper is bloat. |
| PUB-04 | V556 object is re-IDed as a V557 semantic object. | `FAIL_CLOSED__PRODUCER_REOWNERSHIP`. |
| PUB-05 | A V553–V556 object is admitted using only family/name similarity without accepted exact producer contract binding. | `PRODUCER_FINAL_CONTRACT_UNBOUND`. `FINAL_SEAM`. |

## B. Permission monotonicity

| ID | Attack | Required result |
|---|---|---|
| PERM-01 | Producer `ALLOW_CONTEXT_ONLY`; V557 emits `ALLOW_ACTIVE_CAUSAL_CONTEXT`. | `INTEGRITY_FAILURE__FORBIDDEN_PERMISSION_WIDENING`. |
| PERM-02 | Producer `ALLOW_REVIEW_ONLY`; V557 emits context permission. | Fail closed. |
| PERM-03 | V557 permits review only; resolver emits context or active-causal permission. | Fail closed. |
| PERM-04 | Collection is `VALID_NONEMPTY/READY`, one item is denied. | Item denial wins. |
| PERM-05 | Item is present in StructuralPriorRepository but has no admitted V557 governance record. | `ITEM_GOVERNANCE_BINDING_MISSING`. |
| PERM-06 | Active root depends on context-only/review-only/denied dependency. | Dependency retains own permission; no inheritance/widening. |
| PERM-07 | Global readiness score is used as item permission. | Reject; global status is nonauthority. |
| PERM-08 | Repository/index hit is treated as permission. | Reject; presence is not permission. |

## C. Corrected reference classes / ontology firewall

| ID | Attack | Required result |
|---|---|---|
| REFCLS-01 | PSEPF proposed as V557 root or V558 repository object. | `FORBIDDEN_REFERENCE_CLASS_PSEPF_STRUCTURAL_REPOSITORY`. |
| REFCLS-02 | `V3EmpiricalPossibilityInput` proposed for StructuralPriorRepository. | Reject. |
| REFCLS-03 | `ActorComparatorReceipt` proposed as structural prior. | Reject. |
| REFCLS-04 | Raw `EmpiricalFact` proposed as a mixed publication root. | Reject; only producer-declared transitive reference is possible. |
| REFCLS-05 | `StructuralEmpiricalAdmission` is re-owned as V557/V558 semantic identity. | Reject; upstream authority remains canonical. |
| REFCLS-06 | `ReplayReceipt` becomes resolver ranking or runtime prior input. | Reject; audit/replay only. |
| REFCLS-07 | Rendered persona/expression object enters structural repository. | Reject. |

## D. Standalone positive + negative closure

| ID | Attack | Required result |
|---|---|---|
| CLS-01 | Raw V553–V556 directories removed; all packaged exact dependencies intact. | Same semantic resolution/replay as with directories present; no directory access observed. |
| CLS-02 | One required positive producer object omitted but ID/hash remains. | `MISSING_REQUIRED_TRANSITIVE_DEPENDENCY`; hash alone is insufficient. |
| CLS-03 | Required negative/limit authority omitted. | Integrity failure; do not reinterpret missing positive as absence. |
| CLS-04 | Required QuerySpec/source-universe/risk-set omitted. | Integrity failure. |
| CLS-05 | Required measure/weight/estimand authority omitted. | Integrity failure. |
| CLS-06 | Historical authority version unavailable; current/latest authority exists. | Fail closed; no substitution. |
| CLS-07 | Strong ref resolves to zero targets. | Missing required dependency. |
| CLS-08 | Strong ref resolves to two incompatible targets. | Ambiguous required dependency; no arbitrary choice. |
| CLS-09 | Dependency hash mismatches packaged bytes. | `OBJECT_HASH_MISMATCH`. |
| CLS-10 | Closure walker sees tempting provenance prose naming another object but no semantic reference contract. | Do not follow. |
| CLS-11 | Resolver repairs missing closure from raw-stage directory. | `V558_REPAIR_ATTEMPT`. |
| CLS-12 | Resolver repairs missing closure via network/latest/fuzzy label. | Fail closed. |

## E. Role / cardinality / multiplicity / order

| ID | Attack | Required result |
|---|---|---|
| GRAPH-01 | Target objects unchanged but edge role changed. | `REFERENCE_ROLE_CORRUPTION`; closure digest changes. |
| GRAPH-02 | N-ary participant set dyadized. | `CARDINALITY_MISMATCH` or role corruption. |
| GRAPH-03 | Participant multiplicity collapsed because IDs repeat. | Preserve governed multiplicity; mismatch fails. |
| GRAPH-04 | Order-significant participant ordinals swapped. | `SEMANTIC_ORDER_CORRUPTION`; new digest/bundle identity. |
| GRAPH-05 | Serialization order changes for producer-declared unordered set. | Semantic result unchanged; deterministic canonical bytes only. |
| GRAPH-06 | V558 infers a new relation because separately selected participants share endpoint/time/geography. | `FORBIDDEN_RESOLVER_SEMANTIC_INFERENCE`. |
| GRAPH-07 | Exact V555 route identity is replaced by locator or V556/V557/V558 edge ID. | Reject; producer route ID remains canonical. `FINAL_SEAM` for exact identity. |

## F. Provenance / source plurality

| ID | Attack | Required result |
|---|---|---|
| PROV-01 | Two source universes are transitively reachable; resolver pools them. | Reject: provenance is not composition authority. |
| PROV-02 | Equal labels or denominators are used to infer same universe/risk set. | Reject. |
| PROV-03 | Same displayed mass/measure is used to infer compatible estimand/design. | Reject. |
| PROV-04 | Stronger or higher-support source overrides conflicting/noncomparable source by default. | Reject; preserve source-indexed authority states. |
| PROV-05 | Exact operation-specific composition authority is present and bound. | Composition may occur only within its exact scope; no widening. |

## G. Immutable publication/repository identity

| ID | Attack | Required result |
|---|---|---|
| IMM-01 | Same publication bundle ID, changed content/policy/governance. | `IN_PLACE_MUTATION_ATTEMPT`; new bundle identity required. |
| IMM-02 | Same repository ID, changed locator/index/fidelity/policy hash. | Fail closed; new repository identity required. |
| IMM-03 | Same producer object ID, different object hash. | Identity conflict/integrity failure. |
| IMM-04 | Byte-identical objects under different producer identities are semantically deduplicated. | Reject semantic coalescing. |
| IMM-05 | Partial publication/repository becomes visible because readiness says complete. | `PARTIAL_ATOMIC_PUBLICATION`. |
| IMM-06 | `latest` is used as canonical replay identity. | `MUTABLE_LATEST_IDENTITY_ATTEMPT`. |

## H. Index / resolver determinism

| ID | Attack | Required result |
|---|---|---|
| RES-01 | Required logical index missing/incomplete. | `REPOSITORY_INDEX_INTEGRITY_FAILURE`, not valid-empty. |
| RES-02 | Index hit fails object/hash dereference. | Integrity failure. |
| RES-03 | Nearest-time object is selected instead of governed temporal precedence. | Reject. |
| RES-04 | Nearest geography fills missing native scope. | Reject. |
| RES-05 | Score/confidence/similarity chooses equal-rank winner. | Reject. |
| RES-06 | LLM/embedding tie-break is invoked. | Reject. |
| RES-07 | Lexicographically first equal-rank candidate wins semantically. | Reject; lexicographic order is serialization only. |
| RES-08 | Producer authorizes equal-rank multiplicity. | Return full tied set. |
| RES-09 | Singular equal-rank candidates have no governed precedence. | `AMBIGUOUS_EQUAL_RANK_AUTHORITY`. |
| RES-10 | Wall clock changes between identical calls. | Same result and hashes. |
| RES-11 | Filesystem/database iteration order changes. | Same result and hashes. |
| RES-12 | Network exposes a newer producer object. | Ignore/forbid; immutable repository only. |
| RES-13 | Raw stage contains a tempting replacement object. | Resolver may not access it. |
| RES-14 | Empty index is relabeled `VALID_EMPTY`. | Reject unless exact producer-governed valid-empty state exists. |
| RES-15 | Producer unknown becomes zero/false/default. | Preserve `UNKNOWN`. |
| RES-16 | Producer noncomparability is averaged/ordered. | Preserve `NONCOMPARABLE`. |
| RES-17 | Context-only V557 item requested for active causal use. | `REJECTED_PERMISSION_CEILING`. |
| RES-18 | Generated position required but exact binding absent. | `DEFERRED_UNBOUND_GENERATED_POSITION`; no inference from geography/prevalence. |
| RES-19 | Co-resolved V555 participants lack a producer V556 object. | No V556 object may be synthesized. |
| RES-20 | Same exact bundle/query/policy/bindings replayed. | Same selected refs, SelectionRecord hashes, receipt hash and context hash. |

## I. Selection / context / fidelity / refresh

| ID | Attack | Required result |
|---|---|---|
| OUT-01 | Rejected or deferred candidate leaves no SelectionRecord. | Contract failure. |
| OUT-02 | Unresolved semantic key is silently filled. | Contract failure; unresolved key remains typed. |
| OUT-03 | Fidelity scalar is used to override item permission/negative state. | Reject; fidelity is descriptive only. |
| OUT-04 | ResolvedStructuralContext drops preserved negative/noncomparable entries. | Contract failure. |
| OUT-05 | ResolvedStructuralContext creates actor belief/history/persona from selected priors. | Reject semantic promotion. |
| OUT-06 | `next_context_change` is computed from current wall clock with no exact refresh authority. | `REFRESH_AUTHORITY_UNBOUND`; no invented time. |
| OUT-07 | Exact refresh authority/boundaries change but existing context/refresh identity reused. | Integrity failure/new identity required. |
| OUT-08 | Empty semantic request triggers a relevance scan. | Typed valid-empty request only; no scan/invention. |

## J. Physical V557/V558 co-package equivalence

| ID | Attack | Required result |
|---|---|---|
| FUSE-01 | Fused implementation erases boundary between producer permission, V557 permission and resolver permission. | Equivalence proof fails. |
| FUSE-02 | Fused implementation exposes repository object before V557 governance decision/closure verification. | Fail. |
| FUSE-03 | Fused implementation cannot distinguish V557 governance failure from V558 closure/index/resolver failure. | Fail equivalence bar. |
| FUSE-04 | Fused implementation changes producer IDs/hashes or reference roles to internal normalized IDs. | Fail. |
| FUSE-05 | Fused implementation needs raw producer directories although separate contract does not. | Fail. |
| FUSE-06 | Fused implementation passes rowset/status parity but not deterministic replay/permission/negative-state equivalence. | Insufficient proof. |

## K. Exact final-seam tests

All four remain pending until accepted sibling contracts exist.

| ID | Required seam proof | Current expected state |
|---|---|---|
| SEAM-553 | Bind exact V553 object schemas/identity/states/references/publication permission into registry without changing SCR5578 law. | `PRODUCER_FINAL_CONTRACT_UNBOUND` |
| SEAM-554 | Bind exact V554 canonical object/reference identity and negative states. | `PRODUCER_FINAL_CONTRACT_UNBOUND` |
| SEAM-555 | Bind exact one-F1 route identity and producer-owned source/mediation/receiver/reference semantics; locator must preserve it exactly. | `PRODUCER_FINAL_CONTRACT_UNBOUND` |
| SEAM-556 | Bind exact higher-order participant/reference role/cardinality/multiplicity/order semantics while retaining V555 base-route identity. | `PRODUCER_FINAL_CONTRACT_UNBOUND` |
| SEAM-M4 | Run mixed-root standalone raw-directories-absent checksum with all four bound contracts and all item-wise permission chains. | `WAITING_ONLY_FOR_EXACT_FINAL_SEAM` |

No test may turn a missing sibling contract into a guessed schema.

## Oracle endpoint

Until the final seam exists, the lawful stage token is:

`SCR5578_WAITING_ONLY_FOR_EXACT_FINAL_SEAM`
