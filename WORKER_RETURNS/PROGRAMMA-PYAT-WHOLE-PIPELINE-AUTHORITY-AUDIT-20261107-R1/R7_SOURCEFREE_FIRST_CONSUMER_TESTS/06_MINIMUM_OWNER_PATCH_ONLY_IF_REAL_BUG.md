# MINIMUM OWNER PATCH PROPOSAL - T01 REAL DEFECT

## Status
No production patch was made. This is the exact owner-facing proposal required by the commission.

## Proven defect
Synthetic sourcefree C11 release accepted `ALLOW` question semantic/topology authority of wrong kind, wrong operation, and wrong source-universe scope. The first actual source-backed consumer emitted governed `SUPPORTED 2/2` facts under those unfit refs. `DENY` was refused; the defect is positive-authority fitness, not denial handling.

## Root owner
`rawlsing_next/pre553_c11_ingest.py`, `_validate_question_authorities` (around lines 644-659).

Current behavior:
- It resolves every `QuestionVariableBinding.semantic_authority_ref` and `topology_authority_ref`.
- It calls `require_positive_authority` only when `canonical_question_ref_or_typed_absence` is an exact canonical ref, and only for `NATIVE_CANONICAL_MAPPING_HARMONIZATION`.
- Noncanonical question bindings therefore carry only reference-resolution checks.

## Smallest owner patch
For every noncanonical question binding, require exact positive fitness on both the semantic and topology snapshot. At minimum:
- `authority_kind = "SOURCE_SEMANTICS_TOPOLOGY"`
- `object_family = "RespondentEvent@1.0.0"` (and the exact source universe where applicable)
- `source_universe_ref = binding.empirical_universe_ref`
- fail closed as `C11IngestValidationError(IngestDisposition.REJECTED_UNAUTHORIZED_SEMANTIC_PROMOTION, ...)`.

Use `pre553_empirical_authority.require_positive_authority`; do not invent a mutable or latest authority selector. The existing exact snapshot's `governed_operations` should be checked against the exact C11 semantic/topology operation required by the owner. If no exact operation token exists yet, the owner must add an explicit operation binding rather than accepting any operation on a kind/family match; the R7 wrong-operation row is evidence that the current carrier has no such check.

## Defense in depth
`rawlsing_next/_pre553_query_common.py`, `_parse_target_plan` (around lines 351-355) currently checks only `typed_state == "ALLOW"`. Apply `require_positive_authority` for target topology/response refs with exact kind, object family, and source-universe scope. If exact operation is intended, carry an explicit target operation binding; do not infer it from a mutable snapshot.

`rawlsing_next/_pre553_query_eval.py:184-190` currently checks ref presence in the matched event. If the C11 fix is in place, this remains a correct event-binding guard; it does not need to become a second authority-kind parser.

## Required owner tests
1. Valid positive baseline: source-backed C11 question binding resolves, query returns `SUPPORTED` with expected numerator/denominator.
2. Noncanonical question binding with `DENY`: C11 must reject or remain nonpositive; no `SUPPORTED`.
3. Noncanonical binding with wrong-kind `ALLOW`: C11 must reject; no `SUPPORTED`.
4. Noncanonical binding with wrong source-universe/scope `ALLOW`: C11 must reject; no `SUPPORTED`.
5. If operation is represented: wrong-operation `ALLOW` must reject; no `SUPPORTED`.
6. Cold restore: rebuild the valid fixture and reproduce the exact baseline ref.
7. Target-only T02 regression: wrong-kind/operation/scope target authority must remain `UNAVAILABLE 0/0` through the actual event guard.

## Independent review
A separate nonauthor exact-head reviewer must review the proposed owner patch and regression tests. This R7 return is evidence and proposal only; it is not an authorization to merge production changes or to claim native/source issuer authority.
