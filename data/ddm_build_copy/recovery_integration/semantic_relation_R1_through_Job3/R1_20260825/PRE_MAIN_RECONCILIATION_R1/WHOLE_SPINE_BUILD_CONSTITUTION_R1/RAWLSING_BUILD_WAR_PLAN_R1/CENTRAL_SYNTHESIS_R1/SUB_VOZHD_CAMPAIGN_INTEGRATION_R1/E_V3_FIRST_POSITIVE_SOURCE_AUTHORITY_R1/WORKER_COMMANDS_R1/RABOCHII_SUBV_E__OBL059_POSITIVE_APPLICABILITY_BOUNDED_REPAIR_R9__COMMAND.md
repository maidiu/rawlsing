# RABOCHII SUB-VOZHD E — OBL059 POSITIVE_APPLICABILITY — BOUNDED REPAIR R9 COMMAND R1

ROLE: `RABOCHII BOUNDED REPAIR IMPLEMENTER`

REPORTS TO: `SUB-VOZHD E`

LANE: `E2 / OBL059 — POSITIVE_APPLICABILITY R9 CROSS-NODE CONSISTENCY + NESTED INTEGER RECEIPT TOTALITY REPAIR`

WORKER BRANCH:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r9`

EXACT STARTING HEAD:
`93d80b2949f6a306f168542860bef5b1356f47e9`

FAILED FROZEN R8 CANDIDATE:
`9298b13533d45b885d422ce5d89907406b90d97f`

R8 REVIEW RECOMMENDATION:
`FAIL__DO_NOT_ADOPT_OBL059_R8_CANDIDATE`

R8 REVIEW TERMINAL:
`FAIL__OBL059_R8_INDEPENDENT_REVIEW__SEQUENTIAL_NESTED_SNAPSHOT_CROSS_NODE_CONSISTENCY_NOT_CLOSED`

PRIMARY SMALLEST BLOCKER:
`BLOCKER__OBL059_R8_EARLIER_NESTED_SNAPSHOT_CAN_REWRITE_LATER_CONSUMED_NODE_INTO_POSITIVE`

SECOND GENUINE FINDING:
A successfully snapshotted nested `evidence.actor_activation` containing `actor_id = 10 ** 5000` can reach the correct scope-mismatch semantic result but later raise Python's integer-to-string conversion `ValueError` during negative-receipt proof canonicalization instead of returning the deterministic negative receipt.

This is a repair-only continuation. Do not modify the frozen R8 candidate in place. Produce a new frozen R9 candidate.

## Read first

Read and obey the SUB-VOZHD E campaign charter, inter-campaign orchestration law, the OBL059 R1–R8 candidate/court/review/repair returns needed to understand the lane, the R8 independent-review return at exact starting HEAD `93d80b2949f6a306f168542860bef5b1356f47e9`, and the current SUB-VOZHD E adjudication supplied prospectively as immutable campaign authority.

## Exact repair objective

Close both genuine R8 review findings without widening lawful positive-applicability semantics.

### A. Cross-node semantic consistency

R8 snapshots consumed nested Mapping nodes sequentially. That closes direct nested field-access exceptions, but it does not preserve one consistent semantic view of the packet when an earlier custom carrier has side effects on a later not-yet-snapshotted consumed node.

The review demonstrated an initially negative packet whose `evidence.actor_activation.semantic_owner` was wrong. A valid earlier `opportunity` snapshot changed that later actor-activation node before R8 snapshotted it, causing the final result to become `DIRECT_POSITIVE_APPLICABILITY`.

R9 must ensure that caller-defined behavior during preparation of one consumed nested carrier cannot rewrite another consumed node into a different semantic state that is then accepted as part of the same evaluation.

Architecture selection remains with the worker. A complete pre-capture, immutable working representation, bounded two-phase snapshot, or another design may satisfy the property, but the result must represent one coherent semantic view for all nodes actually consumed by OBL059.

Do not solve this by simply rejecting all custom Mapping carriers that are currently lawfully admitted. Stable lawful carriers must continue to preserve exact-dict meaning where the contract already admits them.

### B. Nested oversized exact-integer negative receipt totality

R9 must also ensure that nested exact integers unsafe for canonical decimal conversion under legal runtime settings are projected to a deterministic JSON-safe diagnostic before any negative-receipt proof encoding that can raise `ValueError`.

The inherited R6/R7 stable-threshold law for oversized top-level required bindings must remain intact and must now cover the relevant nested values that enter negative receipt proof material after successful nested snapshot.

Do not swallow unrelated programmer errors outside malformed-value/receipt-projection boundaries.

## Required direct regressions

The producer court must reproduce and close at minimum:

1. the exact R8 primary case: initially wrong-authority `actor_activation`, valid earlier custom `opportunity` carrier mutates the later actor node during snapshot; result must not become `DIRECT_POSITIVE_APPLICABILITY`;
2. equivalent side-effect orderings across the five consumed nested nodes (`opportunity`, top-level `evidence`, `subject_classification`, `actor_activation`, `developmental_phase`) where one carrier can mutate another consumed node before semantic evaluation;
3. mutations from earlier to later nodes, later to earlier nodes where reachable, and shared/aliased carriers across multiple consumed nodes;
4. stable lawful custom Mapping carriers continue to match equivalent exact-dict positive and negative semantics;
5. successful snapshot remains one-shot with no later consultation of the original custom carrier;
6. failed snapshot remains a deterministic field-specific negative receipt and does not leak caller exceptions;
7. the exact nested oversized-integer review case with `actor_activation.actor_id = 10 ** 5000` returns the correct deterministic negative receipt instead of raising;
8. positive/negative threshold neighbors and oversized positive/negative exact integers in nested receipt-relevant positions;
9. runtime integer conversion settings at `0`, minimum nonzero supported value, larger legal values, repeated transitions, and concurrent changes where inherited law requires totality;
10. nested oversized values inside exact built-in dict/list/tuple/set/frozenset diagnostic structures where inherited projection law reaches them.

## Review-harness observations that are NOT repair requirements

The R8 reviewer explicitly found that ten generic `iter` / `len` helper subfailures did not establish candidate defects because `dict(mapping)` used `keys()` plus indexing and never invoked the deliberately failing `__iter__` or `__len__` methods in those helper shapes.

Do not manufacture semantics around uninvoked methods merely to make those review helper variants fail differently. Test the actual callable surface used by the R9 implementation.

## Preservation law

Preserve independently confirmed R8/R7/R6 behavior, including:

- exact-dict outer packet semantics;
- stable authorized custom outer Mapping equivalence;
- outer snapshot failure -> deterministic malformed negative receipt;
- one-shot outer carrier snapshot with no later re-consultation;
- nested snapshot closure for throwing `keys()` / indexing paths actually used by the implementation;
- stable valid nested Mapping equivalence at all five consumed nodes;
- one-shot nested snapshot/no second consultation;
- deterministic shared one-shot negative handling;
- mappings not admitted by the contract do not gain carrier status by resemblance;
- stable-threshold oversized integer projection and runtime setting/time-of-check closure;
- deterministic proof projection, cycle/shared-reference/depth/breadth protections already present;
- wrong scope, wrong authority, stale evidence and project-current execution remain negative;
- adjacent narrative/routing/classification fields do not substitute for competent evidence;
- unrelated deliberate implementation errors after successful preparation remain visible;
- exact R9 revision identity and frozen-candidate binding;
- no project-current effect.

Do not enter OBL058/OBL060, comparator, PSEPF, OBL032, architecture/topology, sibling-campaign, or project-current semantics.

## Governed R9 court requirements

Freeze the new R9 candidate before governed evidence execution.

The producer court must include at minimum:

- the exact cross-node incorrect-positive R8 regression;
- a bounded matrix of cross-node mutation directions and alias/shared-carrier cases across all consumed nodes;
- stable lawful custom Mapping equivalence and one-shot behavior;
- deterministic failed-snapshot negative results;
- the exact nested `10 ** 5000` negative-receipt regression;
- nested integer threshold boundaries and runtime conversion-setting transitions/concurrency;
- inherited outer Mapping and nested Mapping exception regressions;
- inherited cycle/shared graph and deterministic projection cases relevant to consumed proof material;
- ordinary exact-dict positive and negative controls;
- wrong scope/authority/evidence/current-boundary controls;
- unrelated programmer-error visibility after successful preparation;
- no malformed-to-valid coercion;
- no project-current positive applicability, current-positive OBL056, OBL055 execution, ENCOUNTER, actor activation, occurrence admission, causal-use permission, witness independence, or OEE path.

Record exact candidate, test-surface identities, governed evidence execution, run, job, artifact, ZIP SHA-256 and court terminal.

## Separation of duties

`INDEPENDENT_REVIEW_PERFORMED_BY_R9_REPAIR_WORKER = NO`

Do not commission, perform or claim the fresh independent review of the new R9 candidate. If the producer court is green, return to SUB-VOZHD E. SUB-VOZHD E alone may commission exactly one fresh distinct reviewer against that new frozen candidate.

## Hard prohibitions

Do NOT create project-current positive applicability, causal-use permission, witness independence, actor state, ADP-008 transition, ADP-019 occurrence, ENCOUNTER, OEE, current-positive OBL056 entries, or execute OBL055.

Do NOT claim SUB-VOZHD E adoption or HQ adoption.

## Required durable return

Return a durable repository packet containing the new frozen R9 candidate identity, exact repair description, governed court identities/results, direct regression coverage for both genuine R8 findings, no-self-review attestation, and no-current-effect attestation.

The final return commit headline MUST clearly contain `Return` for repository completion discovery.

Terminal:

`RABOCHII_SUBV_E_OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R9__RETURN_TO_SUB_VOZHD_E`
