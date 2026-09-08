# OBL059 POSITIVE_APPLICABILITY — FROZEN R6 CANDIDATE

Status: `FROZEN_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED`

Worker branch:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r6`

Exact worker start:
`7aba3186d5fcd6535cde785105f550ca8a0739ec`

Prospective campaign instruction/adjudication:
`77127860ac887810a3dd28219617c305756fad21`

Campaign tree:
`8b73c1df11b744d13c13b9d1e4885c33d1f8dd4b`

Failed frozen R5 candidate retained unchanged:
`9f7e965fbba64ce94239e36f011f7936681b605a`

R5 review blocker:
`BLOCKER__OBL059_R5_RUNTIME_INTEGER_LIMIT_CHANGE_AFTER_CLASSIFICATION_CAN_REOPEN_VALUEERROR`

## R6 repair boundary

R6 changes only malformed-required-binding negative-receipt construction where an exact built-in integer could be classified under one process-global `sys.get_int_max_str_digits()` state and later canonical encoding could observe a stricter state.

R6 does not change positive applicability semantics, accepted identifier forms, actor/subject/world/time/ADP-010 opportunity scope law, evidence ownership, current-state law, or downstream effects.

The repair:

- does not use the mutable current integer-conversion setting to decide whether a malformed exact integer may safely re-enter later canonical encoding;
- uses CPython's immutable minimum supported nonzero decimal-conversion threshold (`sys.int_info.str_digits_check_threshold`) as the safety floor;
- leaves exact integers below that floor on the inherited R5 path, preserving ordinary JSON-safe behavior;
- projects any malformed exact integer that could fail under any legal later conversion setting before delegation;
- applies the same stable rule recursively to exact built-in dict/list/tuple/set/frozenset diagnostics;
- retains bounded sign, bit-length, and binary-magnitude SHA-256 diagnostics with no decimal conversion of oversized values;
- remains total if the process-global conversion setting changes at any point during the same evaluation;
- preserves visibility of unrelated programmer errors outside this malformed-receipt boundary.

## Frozen executable

`E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL059_POSITIVE_APPLICABILITY_R6/positive_applicability_authority_r6.py`

Executable blob:
`9514781522388d314dca8f71b088e243a6e84820`

The commit containing this manifest and executable is the frozen R6 candidate identity. It must not be edited in place after freeze.

## Separation

`INDEPENDENT_REVIEW_PERFORMED_BY_R6_REPAIR_WORKER = NO`

`SELF_REVIEW_PERFORMED = NO`

No actor activation, ADP-008 transition, ADP-019 occurrence admission, OBL058/OBL060 ownership, current-positive OBL056 entry, OBL055 execution, ENCOUNTER, OEE, project-current applicability, SUB-VOZHD E adoption, HQ adoption, or authority-index mutation is created by this candidate.
