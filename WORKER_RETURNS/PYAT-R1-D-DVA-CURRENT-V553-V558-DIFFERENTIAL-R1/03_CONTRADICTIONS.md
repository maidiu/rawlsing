# PYAT R1-D — ACTUAL CURRENT CONTRADICTIONS

Exact launch base: `8b8597542af5d24dec4fe92adad4c7bb1147850d`.

## C1 — M3 R2 → M4 V556 schema-version provenance drift

**Status:** `CONCRETE_CURRENT_IMPLEMENTATION_CONTRADICTION`

Current M3 declares:
- `M3_CONTRACT_ID = M3_V555_V556_HIGHER_ORDER_STRUCTURAL_EXACT_SEAM_CONTRACT@2.0.0`
- `SCR556_CONTRACT_ID = SCR556_V556_INTERACTION_TOPOLOGY_EXACT_CONTRACT@scr556.v2`.

Current M4 imports that exact `SCR556_CONTRACT_ID`, but `structural_object_from_m3` materializes the producer wrapper with:
- `schema_id = SCR556_CONTRACT_ID`
- `schema_version = "scr556.v1"`.

The ID says v2 while the adjacent version field says v1. This is not stylistic naming drift; it is a content/provenance contract contradiction at a current producer→consumer seam.

**Disposition:** repair the M3→M4 adapter/version binding under existing authority. No architecture reopening.

## C2 — Accepted V558 resolver law versus current exact-key-only resolver

**Status:** `IMPLEMENTATION_NONCONFORMANCE__NOT_ARCHITECTURE_CONTRADICTION`

Accepted CAN-005/Dva law requires temporal precedence, proxy eligibility, generated-position binding evaluation, native-scope handling, equal-rank law and typed deferment. CAN-007 separately requires static next-context-change and generated-state requery channels.

Current M4 carries the frozen CAN-005 policy ID/version/hash, includes generated binding refs in `ContextQuery`, and declares the relevant logical index classes. But `resolve_v558` currently:
1. indexes only `OBJECT_IDENTITY`;
2. resolves by exact resolution key;
3. verifies transitive closure and permission subsets;
4. does not select among temporal anchors;
5. does not consult ADP-006 proxy eligibility;
6. does not evaluate generated-position predicates;
7. emits no `next_context_change`.

This is a bounded implementation gap against already accepted authority, not a reason to redesign V558.

## Non-contradictions explicitly rejected

- Dva's stale historical statements that V554/V555/V557/V558 were unimplemented are not current contradictions; successor M1/M2/M4/M5 code exists.
- V556 positive fixtures do not contradict the inherited W42 statement that Dva W3 concrete authority returns were stranded. M3 is designed to consume exact supplied authority snapshots and fail closed without them.
- Absence of a current V553 producer does not contradict M1's V553 consumer support; producer and consumer obligations are separate.
