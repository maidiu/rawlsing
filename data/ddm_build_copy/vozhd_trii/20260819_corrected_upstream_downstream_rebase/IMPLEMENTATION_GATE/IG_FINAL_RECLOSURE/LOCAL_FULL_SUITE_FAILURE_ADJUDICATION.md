# Local full-suite failure adjudication

Candidate: `b66e282f4185ece6682723bc5e53c1a23534d5f0`

Observed local exact-checkout result: 259 passed, 1 failed.

Failing test:
`rawlsing_next/tests/test_m4_v557_v558_publication_repository.py::test_v556_role_order_cardinality_multiplicity_survives_and_partial_nary_fails_closed`

Observed exception: `ClosureIntegrityError("required positive/negative dependency lacks exact role-preserving edge")`.
Expected test regex: `partial n-ary`.

Adjudication: BOUNDED_IMPLEMENTATION_ORDER_DEFECT__NO_SEMANTIC_CONFLICT.

The malformed partial V556 package is correctly rejected. The defect is validation precedence in `build_v558_repository_bundle`: generic dependency-edge closure is evaluated before `_validate_v556_participant_edges`, making the V556-specific partial-n-ary invariant unreachable for this fixture. The frozen test is retained unchanged. Repair authority is limited to reordering the existing checks so positive supported V556 participant-shape validation executes before the generic declared-dependency loop, while both checks remain mandatory and no acceptance/rejection semantics are widened.

No architecture, contract, test expectation, SPDM authority, legacy runtime, deployment, cutover, or retirement change is authorized.
