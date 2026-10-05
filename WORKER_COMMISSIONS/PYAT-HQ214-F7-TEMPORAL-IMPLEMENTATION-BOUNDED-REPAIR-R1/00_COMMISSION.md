# PYAT HQ214 — F7 TEMPORAL COMPARABILITY IMPLEMENTATION BOUNDED REPAIR — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** Space Bunny semantic-sensitive implementation repair worker  
**MODEL / INTELLIGENCE:** **Space Bunny Max**  
**BRANCH:** `agent/rabochii-pyat-hq214-f7-temporal-implementation-repair-r1`  
**EXACT REPAIR BASE:** `c3db090ff0503963e7914fee740c4b1d17e66cde`  
**CODE-BEARING BASE:** `caf6644a6033fb27c981ff0deb8d6e1b7d3d824e`  
**HOSTILE REVIEW:** `agent/reviewer-pyat-hq213-f7-temporal-implementation-r1 @ 4478e949eb92ec411c5dec9878bb4f23b5cb2c01`  
**REVIEW DISPOSITION:** `F7_TEMPORAL_IMPLEMENTATION_PARTIAL__BOUNDED_REPAIR_REQUIRED`  
**ACCEPTED CONTRACT:** `c57a96897788108db7b194e4e51691d1ca8ab729`  
**CHECKOUT:** SPARSE_REQUIRED  
**ARCHITECTURE REOPEN:** FORBIDDEN  
**SELF-ADOPTION:** FORBIDDEN

Read and obey `PYAT_CONTROL_ROOM/SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md`.

Use the machine's canonical Rawlsing object store. **DO NOT CLONE.** Reuse an exact-branch worktree if present; otherwise create exactly one isolated sparse worktree. Suggested path:

`~/Desktop/Rawlsing_Worktrees/hq214-f7-temporal-repair-r1`

## HQ214 adjudications of the three review ambiguities

These are binding for this repair.

### A. Ordered basis but no lawful delta

Do **NOT** add a thirteenth temporal relation state.

Do **NOT** overload `TEMPORAL_COMPARABLE_NO_DIRECTION`, whose accepted contract meaning remains a lawful partial-order/no-direction case.

If a direction-permitting ordered basis exists but the bound authorized comparison operation cannot produce the required exact delta, the producer MUST fail before emitting a TEMPORAL_RELATION_RECEIPT with a typed input/operation refusal.

The accepted 12-state relation vocabulary remains closed.

### B. comparability_status on refusal states

Set `comparability_status = NOT_COMPARABLE` for every negative/refusal terminal state:
- TEMPORAL_INSUFFICIENT_AUTHORITY
- TEMPORAL_IDENTITY_UNRESOLVED
- TEMPORAL_INSUFFICIENT_ANCHORS
- TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT
- TEMPORAL_MAPPING_MATERIAL_ABSENT
- TEMPORAL_ESTIMAND_MISMATCH
- TEMPORAL_MEASURE_MISMATCH
- TEMPORAL_NONCOMPARABLE
- TEMPORAL_ORDER_UNAUTHORIZED

Only:
- TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION
- TEMPORAL_COMPARABLE_NO_DIRECTION
- TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED

may carry `COMPARABLE`.

### C. no-basis vs higher-precedence failures

The accepted state precedence dominates CFI-03.

`ORDER_UNKNOWN_NONCOMPARABLE` yields TEMPORAL_ORDER_UNAUTHORIZED only when no higher-precedence failure has already been selected.

If a higher-priority authority/identity/anchor/equivalence/mapping/estimand/measure/noncomparability failure exists, emit that higher-priority state and retain the no-basis observation in provenance. Do not raise merely because CFI-03's isolated tuple shape is not the selected terminal state.

## Mission

Repair the implementation to actually realize the accepted F7 contract, not merely its surface vocabulary.

The HQ213 review reproduced fail-open directional claims. Fix the machinery, not the prose.

## Repair 1 — resolve every required authority

Every contract-required authority must be resolved to:
- a positive exact snapshot/ref; or
- a typed fail-closed absence/conflict/scope/hash state.

Presence of a ref string is never enough.

At minimum cover:
- TEMPORAL_COMPARABILITY;
- TEMPORAL_EVIDENCE / temporal identity;
- WEIGHT_DESIGN_ESTIMAND;
- TARGET_USE_PERMISSION;
- UNCERTAINTY_METHOD;
- REPLAY_PROTOCOL;
- NATIVE_CANONICAL_MAPPING_HARMONIZATION when required;
- SOURCE_EQUIVALENCE when cross-universe.

Record every resolution result in provenance.

## Repair 2 — scope TEMPORAL_COMPARABILITY correctly

The new authority is operation-scoped and governed-use-scoped.

The require/resolve path must bind:
- exact comparison operation identity;
- exact governed_use_id;
- exact anchor/pair scope as required by existing authority machinery;
- authority hash/scope integrity.

Make AUTHORITY_HASH_MISMATCH and AUTHORITY_SCOPE_MISMATCH reachable receipt reasons.

No generic positive TEMPORAL_COMPARABILITY receipt may authorize arbitrary operations or uses.

## Repair 3 — exact anchor/observation cardinality

Enforce exactly:
- 2 `anchor_refs`;
- 2 observation refs;
- one observation bound to each anchor.

3+ anchors must refuse before any positive temporal receipt can be minted.

## Repair 4 — bind comparability requirements

`comparability_requirements_ref` is REQUIRED.

Resolve/use it rather than accepting it as decorative metadata.

Each relevant surface result must enter:
- `comparability_requirement_results`;
- provenance;
- deterministic state selection.

## Repair 5 — compute/bind delta under an authorized operation

Do not accept a caller-minted delta as dispositive.

The producer must bind an exact authorized comparison/difference operation and derive or validate the exact delta against the bound observations/quantity surface.

Directional state requires that exact operation result.

If a lawful ordered comparison cannot yield the required exact delta, apply HQ214 adjudication A: typed pre-receipt refusal, no 13th state.

## Repair 6 — emit the accepted closed receipt contract

The production receipt must faithfully carry the accepted fields, including:
- quantity_surface;
- delta where lawful;
- uncertainty_state;
- intervening_span_state;
- governed_use_id;
- authority_snapshot_refs;
- provenance;
- exact authority resolutions;
- comparison operation identity;
- canonical projection rule.

Do not silently rename/drop required contract fields.

Receipt remains module-local/content-addressed:
- no PUBLIC_OBJECT_FAMILIES change;
- no STATE_FAMILIES change;
- relation_state is not CanonicalSemanticObject.typed_state.

## Repair 7 — activate or remove prior-F7 mapping

If `prior_f7_state` remains an input, the accepted map must actually participate in derivation.

Otherwise remove that input and document that historical prior-state compatibility is handled outside this producer.

Do not retain decorative state-mapping machinery.

## Repair 8 — cross-universe detection must be material-derived

Do not gate cross-universe behavior on a caller boolean alone.

Determine cross-universe status from the bound anchors/source-universe refs and require an exact positive SOURCE_EQUIVALENCE result covering the actual pair.

The temporal module may consume but never mint or broaden SOURCE_EQUIVALENCE.

## Repair 9 — backfill and court authenticity

Replace self-referential backfill tests with live checks against the frozen `FORBIDDEN_BACKFILL_TARGET_STATES`.

Repair weak/vacuous courts:
- no broad `pytest.raises(Exception)`;
- no decorative authority fixtures;
- no tautological prior-state map test;
- no self-description-only receipt/public-object tests.

Add hostile witnesses for all three HQ213 blocking findings and all major findings.

## Power ceiling unchanged

No:
- F8 consumption/conditioning/source selection;
- cause/event/mechanism;
- continuity/interpolation/midpoint;
- trend/rate/trajectory;
- rupture production;
- pooling/linkage/equivalence creation;
- currentness;
- scalar temporal pressure;
- actor/person inference.

## Qualification

Re-run:
- focused temporal court;
- exact relevant authority/source-relation courts;
- before/after bounded regression slice with exact failure-ID delta;
- cross-process replay stability.

Run focused court twice if practical.

Environment classification must remain exact and truthful.

## Required return

Write only under:
`WORKER_RETURNS/PYAT-HQ214-F7-TEMPORAL-IMPLEMENTATION-BOUNDED-REPAIR-R1/`

Required:
- `00_RETURN.md`
- `01_AUTHORITY_RESOLUTION_AND_SCOPE_REPAIR.json`
- `02_RECEIPT_STATE_AND_DELTA_REPAIR.json`
- `03_NONCOLLAPSE_AND_POWER_CEILING.json`
- `04_COURT_AND_REGRESSION_RESULTS.json`
- `05_FINAL_DISPOSITION.json`

Allowed dispositions:
- `F7_TEMPORAL_IMPLEMENTATION_REPAIR_COMPLETE__READY_FOR_FINAL_HOSTILE_REREVIEW`
- `F7_TEMPORAL_IMPLEMENTATION_REPAIR_PARTIAL__NAMED_DEFECT`
- `F7_TEMPORAL_IMPLEMENTATION_REPAIR_REVEALS_AUTHORITY_CONFLICT`

Commit, push only this branch, re-fetch/verify origin HEAD, report exact SHA.

Terminal:
`HQ214_F7_TEMPORAL_IMPLEMENTATION_REPAIR_RETURNED__FINAL_HOSTILE_REREVIEW_REQUIRED`
