# PYAT C1-03R — REPLAY GRADE / SELECTIVE INVALIDATION / DEPENDENCY CLOSURE — R1

Status: ISSUED__OVERNIGHT_SOURCE_FREE_IMPLEMENTATION

**LAUNCH IN: DeepSeek Harness — DeepSeek V4.1 Flash — Standard mode**

Repository:
`maidiu/rawlsing`

Branch:
`agent/deepseek-pyat-hq146-c1-03r-replay-invalidation-r1`

Exact base:
`bc661188b51e995d9f5d74e55c4e37d2ba358a17`

This base is the HQ-adopted C1-02 source-free AT08–AT13 implementation.

Governing specifications:
- `PYAT_CONTROL_ROOM/OMEGA_VOZHD_ORCHESTRATION_R1/05_C1_EXECUTION_SPEC.md`
- `PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/acceptance/AT18.md`
- `.../AT19.md`
- `.../nodes/N3.md`
- `.../nodes/N9.md`

AT14–AT16 are assigned to a parallel Space Bunny worker.
AT17 remains reserved to N10E.
Do not implement those acceptance families.

## Mission

Implement and prove the C1-03R source-free tranche:

- **AT18 — replay grade**
- **AT19 — selective invalidation**

Use the current lifecycle/replay owners. Do not build a second maintenance system.

## Current owners to reuse

Inspect and prefer unchanged use of:

`rawlsing_next/pre553_authority_maintenance.py`

including:
- `SemanticDeterminantGraph`
- `AuthorityInvalidationReceipt`
- `AuthorityMaintenanceExecutor`

and:

`rawlsing_next/pre553_replay_audit.py`

plus the accepted analytical producer/composition paths from C1-01/C1-02.

Do not modify these accepted lifecycle/replay owners unless a concrete source-free counterexample proves the required C1 analytical dependency cannot be represented or executed by the current contract. If so, stop and return the exact owner gap instead of casually broadening authority.

## AT18 — replay grade

Create an explicit analytical replay-grade contract.

At minimum distinguish:
- `HISTORICAL_EXPLANATION_ONLY`
- `SERIALIZATION_REPLAY`
- `FRESH_PROCESS_PRODUCT_REPLAY`
- `FRESH_EMPIRICAL_RECOMPUTATION`

Names may follow an existing governed vocabulary if one already exists; do not invent duplicate meanings.

For every replay claim in this lane, bind:
- exact retained determinants;
- exact producer path;
- exact authority refs;
- output identity expected;
- actual replay mechanism;
- replay grade;
- limitations.

Positive:
- at least one accepted C1 analytical product must be reconstructed in a **fresh process from retained determinants through the claimed producer/composition path**;
- identity must reproduce exactly at the declared grade.

Hostiles:
- a stored JSON/receipt explanation must not qualify as fresh recomputation;
- serialization/deserialization alone must not qualify as fresh empirical recomputation;
- missing exact determinant or authority must fail closed rather than silently downgrade while still claiming the stronger grade.

## AT19 — selective invalidation

Bind actual C1 analytical products into the current determinant/dependency lifecycle.

Use `SemanticDeterminantGraph` and the current maintenance/invalidation machinery where applicable.

Construct a source-free dependency graph containing, at minimum:
- exact producer/query/predicate or relevant authority determinant;
- composed analytical product;
- generated evidence / consumer result where applicable;
- at least one **unaffected sibling product**.

Mutate exactly one determinant.

Prove:
- all registered affected descendants are invalidated/reidentified/recompiled as governed;
- unaffected sibling remains usable and identity-stable;
- the invalidation receipt distinguishes affected from unaffected refs;
- replacement identity is exact where recompilation succeeds;
- `NO_CURRENT` or equivalent explicit noncurrent state is preserved where lawful replacement is unavailable.

### Missing-edge hostile

Create a deliberately incomplete cross-owner dependency graph.

Require:
- closure claim fails;
- cache/object presence cannot restore authority;
- a product cannot be treated current merely because its bytes remain present;
- the lane does not infer the missing dependency.

This hostile is mandatory.

## Analytical adapter terrain

Preferred bounded new owner:

`rawlsing_next/pre553_analytical_replay_dependency.py`

Its job may be:
- register exact analytical product determinants/dependencies with the current lifecycle owner;
- execute or describe replay at an explicit grade;
- emit analytical replay/invalidation receipts.

It must **not**:
- become a new authority-maintenance owner;
- choose latest/default authority;
- infer semantic lifecycle meaning;
- mutate current selection outside the existing owner;
- invent dependencies from object similarity.

Preferred tests:

`rawlsing_next/tests/test_pre553_analytical_replay_dependency.py`

Optional fresh-process runner:

`rawlsing_next/tests/c1_at18_at19_fresh_process_runner.py`

## Disjoint write law

Do not modify:
- `rawlsing_next/pre553_analytical_composition.py`
- `rawlsing_next/pre553_analytical_state_and_route.py`
- Bunny's AT14–AT16 test/fixture terrain;
- N10E provider implementation/tests;
- `rawlsing_next/pre553_authority_maintenance.py`;
- `rawlsing_next/pre553_replay_audit.py`.

If a current lifecycle owner defect blocks execution, return:
`EXISTING_LIFECYCLE_OWNER_CHANGE_REQUIRED`
with the smallest executable counterexample.

## Required return

Write only:

`WORKER_RETURNS/PYAT-C1-03R-REPLAY-INVALIDATION-R1/**`

Required:
- `00_RETURN.md`
- `01_REPLAY_GRADE_CONTRACT.json`
- `02_FRESH_PROCESS_REPLAY_RECEIPT.json`
- `03_DEPENDENCY_GRAPH_AND_INVALIDATION_RECEIPT.json`
- `04_MISSING_EDGE_HOSTILE.json`
- `05_EXECUTION_RECEIPT.json`
- `06_FINAL_DISPOSITION.json`

## Required courts

At minimum:
- new AT18/AT19 court;
- existing authority-maintenance tests materially relied upon;
- replay-audit tests materially relied upon;
- smallest accepted C1 analytical/composition court required to prove real producer/composed identities.

Do not run the entire repository unless evidence suggests a wider regression.

## Allowed dispositions

- `PASS_C1_03R_SOURCE_FREE_PATCH_READY__INDEPENDENT_REVIEW_REQUIRED`
- `BOUNDED_IMPLEMENTATION_OR_COMPOSITION_GAP`
- `TYPED_AUTHORITY_RESIDUAL`
- `EXISTING_LIFECYCLE_OWNER_CHANGE_REQUIRED`
- `ARCHITECTURE_WARRANT`

## Absolute prohibitions

No raw survey files.
No Candidate A/B/C.
No measured P2X.
No real-source C11.
No C4.
No AT14–AT17 implementation.
No N10E duplication.
No C1-R.
No structural-world/AT31/AT32 completion claim.
No V3 actor/person implementation.
No new semantic/comparability/model authority.
No merge/self-adoption.

## Git completion

When coherent:
1. verify diff from `bc661188...` stays inside this commission;
2. commit all work;
3. push exactly this branch;
4. report final SHA, disposition, terminal, changed files and exact test counts.

Terminal:

`C1_03R_REPLAY_INVALIDATION_RETURNED__HQ_ADJUDICATION_REQUIRED`
