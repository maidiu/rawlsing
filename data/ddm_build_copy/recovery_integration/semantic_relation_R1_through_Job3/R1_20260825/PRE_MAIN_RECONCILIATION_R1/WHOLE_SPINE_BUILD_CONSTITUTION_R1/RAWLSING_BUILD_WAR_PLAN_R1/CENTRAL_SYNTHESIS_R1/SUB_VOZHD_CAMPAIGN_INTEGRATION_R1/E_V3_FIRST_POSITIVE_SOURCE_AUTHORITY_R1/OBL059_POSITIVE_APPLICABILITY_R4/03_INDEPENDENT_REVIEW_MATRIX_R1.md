# OBL059 R4 — INDEPENDENT REVIEW MATRIX R1

Reviewer role: `RABOCHII_INDEPENDENT_REVIEWER_OBL059_R4_R1`

Review branch:
`agent/rabochii-subv-e-obl059-positive-applicability-r4-independent-review-r1`

Exact start:
`8715c131dd102d5952aa76b6f2549dfbba58cbee`

Frozen R4 candidate:
`830cc0442f34e8b28405006c031cc1d256893a17`

Known producer governed run:
`34230793386` — `success`

Prospective campaign instruction/adjudication:
`f7618257604c362097edb3c78dae8480a9499c4a`

Campaign adjudication tree:
`4f327169d238af9f42a274a5ce30f58ad8436d22`

## Independence and freeze law

This matrix is frozen by the fresh R4 reviewer before governed execution. The reviewer has no repair authority. The frozen candidate is not modified.

PASS requires deterministic negative-receipt construction over the commissioned malformed-binding surface, exact preservation of ordinary applicability semantics, and visibility of unrelated internal errors.

## Independent failure-mode families

1. Valid NONCURRENT_SYNTHETIC positive and negative controls.
2. Exact ordinary JSON-safe R3 positive, negative, and malformed behavior preservation.
3. Custom Mapping required-binding values whose protocol methods raise.
4. Custom sequence/list-like/tuple-like/set-like/bytes-like/iterable/mapping-lookalike required-binding values whose protocol methods raise.
5. Exact built-in containers containing custom objects whose display, hashing, equality, ordering, iteration, or conversion methods raise.
6. Heterogeneous non-JSON mapping keys including bytes, tuple, frozenset, and custom-object keys.
7. Circular lists, circular mappings, mutual recursion, mixed cycles, shared-reference graphs, and repeated aliases.
8. Deep graphs below, at, and beyond the projection ceiling.
9. Breadth-heavy structures and deterministic category/proof behavior.
10. Nested bytes/set/frozenset/opaque combinations at every required binding.
11. Repeated equivalent malformed classes produce identical negative receipts and proof hashes.
12. Structurally distinct malformed shapes remain distinguishable where structure is retained.
13. No diagnostic normalization can create a valid actor/subject/world/time/opportunity identifier.
14. Wrong opportunity scope, wrong authority/source/evidence, stale evidence, and PROJECT_CURRENT remain negative.
15. Classification/routing/occurrence/permission/witness-independence/narrative fields cannot substitute for required evidence.
16. Deliberate unrelated internal TypeError, ValueError, and RuntimeError remain visible.
17. All commissioned negative receipts are JSON serializable and preserve every no-current-effect flag.
18. Exact built-in integer values near and beyond Python's configured integer-to-string conversion ceiling. This independently checks the claim that exact primitives are structurally JSON-safe before canonical encoding. A malformed required binding must still return a deterministic JSON-safe negative receipt rather than fail during proof construction.

## Smallest pre-execution hypothesis

R4 treats every exact `int` as structurally JSON-safe. CPython can reject conversion of an exact integer whose decimal representation exceeds the configured `int` string-conversion limit. If such a malformed required binding is delegated to R3 and the fallback projection returns the same large integer unchanged, canonical proof construction may still fail. This is inside the commissioned malformed-receipt serialization boundary and does not require any change to positive-applicability semantics.

No conclusion is frozen here. The governed execution determines PASS or FAIL.
