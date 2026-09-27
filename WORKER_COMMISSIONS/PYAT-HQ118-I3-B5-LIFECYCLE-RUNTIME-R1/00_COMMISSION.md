# PYAT HQ118 — I3 B5 LEARNED-PRODUCT LIFECYCLE RUNTIME — R1

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-pyat-hq118-i3-b5-lifecycle-runtime-r1`

Exact sealed HQ118 base:

`6cd63ce6cd5bf697f76ff7e62c4681f16c062832`

**AGENT TYPE: SOURCE-FREE CODE IMPLEMENTATION / GITHUB**

## Governing authority

The semantic owner is already current:

`PRE553_LEARNED_PRODUCT_LIFECYCLE_CANDIDATE@1.0.0`

adopted at:

`OBL034 = CLOSED_AT_EXACT_LIFECYCLE_ECONOMICS_GRAIN`.

Read the exact current B5 authority artifacts:

- central HQ adoption `SUB_VOZHD_B_HQ_FANIN_DISPOSITION_R1/00_VOZHD_DISPOSITION.md`
- B5 candidate `01_LEARNED_PRODUCT_LIFECYCLE_CANDIDATE.md`
- B5 machine rules `02_LIFECYCLE_RULES.json`

Also read:

- `PYAT_CONTROL_ROOM/17_HQD118_M01_AND_LEARNED_WORLD_OWNER_ADOPTION.md`
- `PYAT_HQ118_FANIN_R1/01_CROSS_EXAMINATION.md`
- M3 refinement at `e718ae8529bbb194c1f27b474180c8e66bb7f4c4`
  - `01_M3_CONSTITUTION.md`
  - `02_LIFECYCLE_EVENT_SCHEMA.md`
  - `03_CURRENT_SELECTION_LAW.md`
  - `04_SUCCESSION_INVALIDATION_REBUILD_LAW.md`
  - `05_AUTHORITY42_REUSE_CEILING.md`
  - `07_IMPLEMENTATION_CONTRACT.md`
  - `08_HOSTILE_LIFECYCLE_TEST_PLAN.md`

Where M3 wording conflicts with B5 current authority, B5 wins. M3 is implementation-refinement capital only.

## Mission

Implement the current B5 lifecycle authority as a generic source-free learned-product lifecycle runtime.

Preferred write surface:

- `rawlsing_next/pre553_learned_product_lifecycle.py`
- `rawlsing_next/tests/test_pre553_learned_product_lifecycle.py`

You may extract a neutral lower-level exact-ref lifecycle helper from existing authority-maintenance mechanics only if subject-type neutrality is proved and existing owner semantics are unchanged.

Do not alias AuthoritySnapshot types to learned-product types.

## Required B5 capabilities

Implement:

- immutable lifecycle registration;
- lifecycle publication event/state;
- explicit scope-bound current selection;
- explicit no-current state;
- supersession;
- withdrawal/invalidation;
- historical retention;
- historical current-as-of/replay;
- determinant-local transitive invalidation;
- rebuild eligibility/linkage;
- optional-cache lifecycle classification;
- recomputable learned-product payload GC eligibility.

## M3 refinement allowed

Where compatible with B5/P2, use:

- exact LifecycleEvent;
- exact SelectionKey;
- exact CurrentSelectionReceipt;
- exact NoCurrentReceipt;
- exact invalidation/rebuild receipts;
- append-only parent-linked history;
- explicit CURRENT_SELECT / NO_CURRENT;
- selection conflict state;
- exact checkpoint/replay;
- neutral determinant traversal.

## M2 boundary

The runtime should operate on exact learned-product identities/release refs.

Because I2 is a sibling and may not yet exist on this branch, implement against a narrow protocol/interface that can later accept M2 `ReleaseCore` refs without importing sibling code.

Do not invent M2 release semantics.

B5 lifecycle `PUBLISHED` is a lifecycle state/event.

An M2 `PublicationBinding` later represents resolution/locator mechanics only.

## Required hostile tests

At minimum:

1. repository presence != lifecycle registration;
2. registration != publication;
3. publication != current selection;
4. only exact selection receipt creates currentness;
5. no latest/default/newest/semver/file-order currentness;
6. exact NO_CURRENT works;
7. recertification does not silently select;
8. supersession is explicit and nondestructive;
9. withdrawal preserves history and clears/replaces current only through explicit selection-state action;
10. conflicting current selections fail closed;
11. historical current-as-of exact event/checkpoint;
12. determinant-local direct/transitive invalidation only;
13. unrelated products unaffected;
14. cache loss does not invalidate semantic product;
15. semantic determinant change requires rebuild/new product identity from upstream producer, not lifecycle synthesis;
16. rebuild blocker remains typed;
17. GC only for proven recomputable payload and never mandatory history;
18. no source/carrier retirement authority;
19. AuthoritySnapshot != learned product;
20. AuthorityReleaseReceipt != lifecycle current receipt;
21. consumer permission remains separate;
22. exact checkpoint/restart/replay identity;
23. crash/atomic-selection hostile behavior;
24. B5 machine-rule parity for every implemented lifecycle action.

## Hard prohibitions

No raw source.
No real-source execution.
No M1 validation.
No M2 release-core implementation.
No Field Forge mutation.
No source/carrier retirement.
No new lifecycle semantic authority.
No architecture selection.

## Return

Own only:

`WORKER_RETURNS/PYAT-HQ118-I3-B5-LIFECYCLE-RUNTIME-R1/`

Return:
- `00_RETURN.md`
- `01_CHANGED_FILES.tsv`
- `02_B5_RULE_TO_RUNTIME_PARITY.tsv`
- `03_PUBLIC_API_AND_OWNER_RECEIPT.md`
- `04_HOSTILE_TEST_LEDGER.tsv`
- `05_AUTHORITY42_REUSE_OR_NONREUSE_RECEIPT.md`
- `06_M2_INTERFACE_PROTOCOL.md`
- `07_CHECKPOINT_REPLAY_RECEIPT.md`

Success:

`PYAT_HQ118_I3_PASS__B5_LEARNED_PRODUCT_LIFECYCLE_RUNTIME_SOURCE_FREE_GREEN__OBL034_SEMANTICS_PRESERVED`

Block:

`PYAT_HQ118_I3_BLOCKED__B5_PARITY_OR_LIFECYCLE_RUNTIME_CONTRACT_FAILURE__NO_SEMANTIC_WIDENING`
