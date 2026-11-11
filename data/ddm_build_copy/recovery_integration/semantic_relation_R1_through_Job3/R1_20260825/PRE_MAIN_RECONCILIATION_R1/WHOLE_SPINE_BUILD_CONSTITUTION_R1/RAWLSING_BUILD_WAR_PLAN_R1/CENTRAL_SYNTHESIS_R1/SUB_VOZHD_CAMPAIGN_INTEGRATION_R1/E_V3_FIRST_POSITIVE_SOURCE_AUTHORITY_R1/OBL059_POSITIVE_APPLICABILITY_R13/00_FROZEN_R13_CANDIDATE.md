# OBL059 POSITIVE_APPLICABILITY — FROZEN R13 CANONICAL-INPUT CANDIDATE

Worker branch:
`agent/rabochii-subv-e-obl059-positive-applicability-canonical-input-boundary-r13`

Exact start:
`e893cc78a0e5c4ba93c1dd8d35235cf946a8e30c`

Campaign authority:
`cd96e61c073522383a1315148a5e58aa169d2a1a`

Campaign tree:
`6e644d347db5c6c64f7b13ff06a750cf68a4c543`

Failed frozen R12 target retained unchanged:
`6962ab0bdb2f66cc266b0e88b5ff5016b361a9a1`

R12 review blocker addressed:
`BLOCKER__OBL059_R12_CUSTOM_PARENT_PATH_RESOLUTION_CAN_REWRITE_NESTED_ENTRY_VIEW_IN_CHILD`

## R13 boundary

R13 moves OBL059 authority evaluation behind an explicit immutable canonical-input contract.

The decision function accepts only an exact built-in tuple with schema:
`OBL059_CANONICAL_POSITIVE_APPLICABILITY_PACKET@R13`.

Canonical payload values are recursively tagged exact built-ins. Required opportunity, evidence, subject-classification, actor-activation and developmental-phase structures must thaw to exact dictionaries before semantic evaluation.

Raw dictionaries and arbitrary custom Mapping objects are not direct positive-authoritative inputs to the OBL059 decision function. The decision function rejects them deterministically without traversing caller-defined Mapping methods.

An explicit upstream representation adapter is provided for lawful source fixtures. The adapter is not called by the decision layer and does not transfer source-fact ownership into OBL059.

Once canonicalization has completed, all authority-relevant input traversal in OBL059 is over exact built-in structures only.

## Candidate-side blobs

Candidate executable blob:
`1dc206afcd25315f406fade7f8a3b72c378dfcd0`

Producer court blob:
`7e99d74748825f34165ef001f4d859c68a9b22b7`

`SELF_REVIEW_PERFORMED = NO`

`INDEPENDENT_REVIEW_PERFORMED_BY_R13_WORKER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

No project-current state, current-positive entry, actor transition, OBL055 execution, encounter, OEE, or authority-index effect is created by freezing this candidate.
