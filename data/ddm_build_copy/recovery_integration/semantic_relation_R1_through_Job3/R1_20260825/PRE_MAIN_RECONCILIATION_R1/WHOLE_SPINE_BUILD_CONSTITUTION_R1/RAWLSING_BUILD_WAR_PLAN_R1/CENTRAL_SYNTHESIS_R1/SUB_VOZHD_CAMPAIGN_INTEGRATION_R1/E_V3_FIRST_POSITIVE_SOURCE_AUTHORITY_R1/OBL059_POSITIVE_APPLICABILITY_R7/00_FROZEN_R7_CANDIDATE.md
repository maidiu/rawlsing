# OBL059 POSITIVE_APPLICABILITY — FROZEN R7 CANDIDATE

Status: `FROZEN_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED`

Worker branch:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r7`

Exact worker start:
`6468d775eb15076e8ca243c95180fdfecb41ce27`

Prospective campaign instruction/adjudication:
`07ad7844e5b817615f3ff371e06e2dcef349b0bd`

Failed frozen R6 candidate retained unchanged:
`5ca7380bd17b3dec271fe5a8c6bf22656f55b647`

R6 review blocker:
`BLOCKER__OBL059_R6_CUSTOM_MAPPING_PACKET_CAN_ESCAPE_VIA_CALLER_CONTROLLED_KEYS_BEFORE_NEGATIVE_RECEIPT`

## R7 repair boundary

Frozen R1 authority accepts general `Mapping` carriers, so R7 preserves that carrier law rather than narrowing it to exact dictionaries.

R7 changes only the outer non-exact-dict Mapping boundary:

- exact dict packets are evaluated by frozen R6 unchanged;
- non-Mapping carriers remain delegated to inherited law unchanged;
- a non-exact Mapping is snapshotted exactly once inside a bounded carrier-traversal boundary;
- if snapshot traversal raises an ordinary `Exception`, R7 returns the existing deterministic `PACKET_MALFORMED` negative receipt from safe frozen input and never consults the carrier again;
- if snapshot traversal succeeds, the resulting exact dict is evaluated by frozen R6 unchanged;
- nested custom values remain governed by the existing R4-R6 exact-built-in projection/isolation law.

The bounded exception handling is confined to caller-controlled outer-carrier traversal. Evaluation of a successful exact snapshot occurs outside that exception boundary, so unrelated implementation errors remain visible.

R7 does not infer applicability from mapping-like resemblance, does not inspect hidden backing attributes after traversal failure, and does not normalize malformed carrier content into identifier strings.

## Frozen executable and producer court

Executable:
`E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL059_POSITIVE_APPLICABILITY_R7/positive_applicability_authority_r7.py`

Producer court:
`E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL059_POSITIVE_APPLICABILITY_R7/governed_bounded_court_r7.py`

The commit containing this manifest, executable, and producer court is the frozen R7 candidate identity. It must not be edited in place after freeze.

## Separation and no-current-effect boundary

`SELF_REVIEW_PERFORMED = NO`

`INDEPENDENT_REVIEW_PERFORMED_BY_R7_REPAIR_WORKER = NO`

No actor activation, ADP-008 transition, ADP-019 occurrence admission, OBL058/OBL060 ownership, current-positive OBL056 entry, OBL055 execution, ENCOUNTER, OEE, project-current applicability, authority-index mutation, SUB-VOZHD E adoption, HQ adoption, or OBL061 authorization is created by this candidate.
