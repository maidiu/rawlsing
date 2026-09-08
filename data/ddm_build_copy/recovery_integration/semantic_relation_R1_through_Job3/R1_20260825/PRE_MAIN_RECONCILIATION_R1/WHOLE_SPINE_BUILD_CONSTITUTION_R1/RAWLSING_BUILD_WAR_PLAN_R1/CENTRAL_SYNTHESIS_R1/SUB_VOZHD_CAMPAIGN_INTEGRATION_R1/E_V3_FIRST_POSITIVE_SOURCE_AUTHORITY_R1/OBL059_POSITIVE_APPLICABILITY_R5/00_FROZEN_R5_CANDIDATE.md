# OBL059 POSITIVE_APPLICABILITY — FROZEN R5 CANDIDATE

Status: `FROZEN_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED`

Worker branch:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r5`

Exact worker start:
`a728990458a4a909186b99520df6bb1cc9a826f1`

Prospective campaign instruction/adjudication:
`1c0f767126cc479c31ddcdc521fa64fa26efbe4f`

Campaign tree:
`b71a64304b63086da16841bd6e6aafba34ad3b01`

Failed frozen R4 candidate retained unchanged:
`830cc0442f34e8b28405006c031cc1d256893a17`

R4 review blocker:
`BLOCKER__OBL059_R4_EXACT_INTEGER_JSON_SAFE_CLASSIFICATION_OMITS_ENCODER_CONVERSION_LIMIT`

## R5 repair boundary

R5 changes only negative-receipt construction after a required binding has already been determined semantically malformed and an exact built-in integer cannot be safely rendered under the runtime's configured decimal integer conversion limit.

R5 does not change positive applicability semantics, accepted identifier forms, exact actor/subject/world/time/ADP-010 opportunity binding law, evidence ownership, scope law, or any project-current effect.

The repair:

- reads `sys.get_int_max_str_digits()` without changing it;
- decides exact-int decimal renderability using integer comparison against `10 ** limit`, with no decimal conversion;
- preserves zero/small/ordinary exact integers through frozen R4 unchanged;
- projects oversized malformed exact integers to a bounded JSON-safe diagnostic containing sign, bit length, and SHA-256 of the exact binary magnitude;
- never normalizes a malformed integer into a string identifier;
- retains R4's exact-built-in-only traversal and custom-object isolation;
- retains R4 cycle/depth handling and no-current-effect receipt fields;
- leaves unrelated programmer exceptions outside this boundary visible.

## Frozen executable

`E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL059_POSITIVE_APPLICABILITY_R5/positive_applicability_authority_r5.py`

Executable blob:
`04cb331af0d7e0d4d14db901ecf79eb0d736bfe3`

The commit containing this manifest and executable is the frozen R5 candidate identity. It must not be edited in place after freeze.

## Separation

`INDEPENDENT_REVIEW_PERFORMED_BY_R5_REPAIR_WORKER = NO`

No actor activation, ADP-008 transition, ADP-019 occurrence admission, OBL058/OBL060 ownership, current-positive OBL056 entry, OBL055 execution, ENCOUNTER, OEE, project-current applicability, SUB-VOZHD E adoption, or HQ adoption is created by this candidate.
