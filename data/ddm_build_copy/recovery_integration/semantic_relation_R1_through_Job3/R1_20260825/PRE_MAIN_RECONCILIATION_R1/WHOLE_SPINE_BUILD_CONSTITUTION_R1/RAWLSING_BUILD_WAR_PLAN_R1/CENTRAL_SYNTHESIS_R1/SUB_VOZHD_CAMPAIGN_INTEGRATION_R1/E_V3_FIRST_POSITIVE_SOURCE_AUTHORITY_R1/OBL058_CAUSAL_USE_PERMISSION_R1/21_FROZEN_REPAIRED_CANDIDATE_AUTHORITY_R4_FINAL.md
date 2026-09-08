# OBL058 — CAUSAL_USE_PERMISSION — FINAL PRE-COURT R4 FREEZE

## Status

`FROZEN_R4_CANDIDATE__READY_FOR_PRODUCER_GOVERNED_COURT__NO_INDEPENDENT_REVIEW`

The earlier R4 freeze commit `ff8be5eb12fafa40b1479355581cccff0a67debd` received no governed evidence execution and is superseded before court by this final R4 freeze. The only change is explicit fail-closed normalization for an uninitialized exact-type `object.__new__` receipt: missing `_body_json` now returns `receipt_not_issued_by_source_authority` rather than allowing `AttributeError` to escape.

No semantic permission rule, scope rule, source basis, process-isolated authority boundary, fixture restriction, or project-current prohibition changed.

## Final R4 contract identities

- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.3.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@4.0.0`
- executable: `causal_use_permission_candidate_r4.py`
- fixture: `NONCURRENT_SYNTHETIC`

## Boundary retained

Authoritative object/body bindings exist only in the separate authority subprocess. Parent-process Python introspection exposes no authoritative ledger alias. The protocol accepts semantic scope/basis input and constructs the authoritative body itself; it exposes no operation for caller-body registration, append, replacement, rebinding, deletion/reinsertion, or generic minting.

The exact commit containing this document and executable is the semantic candidate SHA for the R4 governed court.

`INDEPENDENT_REVIEW_PERFORMED_BY_R4_REPAIR_WORKER = NO`

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`
