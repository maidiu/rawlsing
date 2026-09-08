# OBL059 R3 — INDEPENDENT REVIEW MATRIX R1

Reviewer role: `RABOCHII_INDEPENDENT_REVIEWER_OBL059_R3_R1`

Reviewer branch:
`agent/rabochii-subv-e-obl059-positive-applicability-r3-independent-review-r1`

Commission start:
`2eedd4456f7dfa61d266eb3efe938d406b96c9fd`

Frozen candidate:
`4fdb897e8a089787d7407197fd49bbd1ef51f2ef`

Bound producer evidence execution:
`860078598cd1376c368177c51b183f651b9c8f45`

Known producer run:
`34197429485`

Prospective campaign instruction/adjudication:
`c7f221d3c07453eebae36e448a52b2e7789ae13c`

Campaign adjudication tree supplied by SUB-VOZHD E:
`1fdf0ccf143942bf4b009c15cabfe2f5c41871e9`

## Independence and freeze law

This matrix is authored by the fresh R3 independent reviewer. It is not the producer court and does not modify the frozen R3 candidate. It is frozen before governed evidence execution. The reviewer has no repair authority.

PASS requires the frozen candidate to survive the full matrix under the governed bounded-court protocol. Any commissioned malformed-input escape, nondeterministic/non-JSON-safe receipt, malformed-to-positive coercion, semantic broadening, unrelated-error masking, jurisdictional defect, or current effect is a FAIL.

## Frozen adversarial families

1. Valid `NONCURRENT_SYNTHETIC` positive control proves the evaluator is not fail-all.
2. Valid `NONCURRENT_SYNTHETIC` negative control proves ordinary negative behavior remains available.
3. Ordinary JSON-safe positive, negative, malformed, missing-field, and extra-field packets remain exactly equal to frozen R2 behavior.
4. At every required-binding position, reject and close `bytes`, `set`, `frozenset`, opaque objects, nested opaque objects, and mixed malformed structures with JSON-safe negative receipts.
5. At every required-binding position, reject and close mappings with non-string/non-JSON-safe keys: `bytes`, tuples, custom opaque keys, and nested key/value combinations.
6. At every required-binding position, reject and close circular lists, circular mappings, mutually recursive containers, deeper cyclic combinations, and shared-reference graphs without recursion escape.
7. Deep nesting beyond the projection ceiling closes deterministically and remains JSON serializable.
8. Opaque objects whose `__repr__` and `__str__` throw or lie are never stringified into identifiers and still close negatively.
9. Hostile mapping/iteration behavior reachable from a malformed required binding must not escape the commissioned diagnostic projection boundary. In particular, a `Mapping.items()` `TypeError` is a commissioned projection exception and must yield a negative receipt rather than escape.
10. Hostile equality/hash objects reachable in diagnostic structures must not be invoked merely to stringify/coerce malformed content positive.
11. Repeated evaluation of equivalent malformed semantic classes is deterministic, including receipt and `proof_sha256`.
12. Distinct malformed structured values that have similar opaque/display components remain distinguishable by structure and never become valid identifiers.
13. Every fallback receipt and diagnostic projection is JSON serializable and preserves all no-current-effect attestations.
14. Wrong actor/world/subject/time/opportunity binding, wrong structural authority/jurisdiction/predicate, stale evidence, and mismatched evidence remain negative.
15. V554, CAN-001, CAN-003, routing, classification narrative, occurrence, permission, witness independence, ADP-010 realization, and narrative plausibility cannot substitute for missing competent required evidence.
16. Project-current scope remains hard negative and creates no current state.
17. No actor creation/activation, ADP-008 transition, ADP-019 occurrence, current-positive OBL056, OBL055 execution, ENCOUNTER, OEE realization, OBL058 permission, OBL060 independence, or authority-index mutation is produced by any review case.
18. A deliberate unrelated internal/programmer error injected only into the ordinary delegated R2 path remains visible rather than being converted into a semantic negative.
19. R3 revision identity and frozen candidate semantics remain exact; review code never mutates the candidate.

## Smallest pre-execution hostile hypothesis

The frozen R3 implementation calls `deepcopy(dict(packet))` before malformed-binding classification, and its fallback projection calls `Mapping.items()` without a local exception boundary. Family 9 therefore specifically tests whether a semantically malformed required binding implemented as a hostile `Mapping` can raise from `items()` during diagnostic projection. This is inside the commissioned matrix because the current adjudication explicitly requires throwing mapping/iteration behavior reachable by diagnostic projection and forbids uncaught projection exceptions after a required binding is already malformed.

No conclusion is frozen here. The terminal is determined only by governed execution.
