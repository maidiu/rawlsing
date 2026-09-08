# OBL059 POSITIVE_APPLICABILITY — FROZEN R11 CANDIDATE

Status: `FROZEN_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED`

Worker branch:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r11`

Exact worker start:
`4a52282a6747604bcd4e9f8eb04ee378c4a044e8`

Campaign authority consumed prospectively:
`8928043fc28da78c112419e79ab7382228ea2b69`

Campaign tree:
`c7a7e9f25fa28ec9730b765639b3a595dd5a3ba0`

Failed frozen R10 candidate retained unchanged:
`77f80b15d35236d13899df0992943cfc20a08485`

R10 review blocker repaired:
`BLOCKER__OBL059_R10_STABLE_COMPOSED_MAPPING_EQUIVALENCE_REJECTED_BY_SINGLE_BACKING_DICT_REQUIREMENT`

## R11 repair boundary

R11 preserves frozen R10 exactly whenever R10 can already establish its coherent entry view.

Only when R10 cannot reduce a lawful composed Mapping to one direct backing dict, R11 attempts a general semantic fallback. The fallback does not inspect class names or special-case `ChainMap`. It obtains the Mapping's observable contents only in isolated forked child state, requires bounded raw entry-state signatures to remain unchanged across repeated materialization, requires repeated materializations in the child to agree, and requires repeated isolated child snapshots to agree before installing an exact built-in semantic view in the parent working packet.

If a stable coherent view cannot be established, R11 delegates back to R10's deterministic negative handling rather than using partial or live semantics.

This preserves:

- R10's independently successful coherent-entry-view behavior for directly capturable custom Mapping carriers;
- stable composed Mapping semantics including layer composition, precedence and shadowing;
- no type/class/shape inference of positivity;
- child-local isolation of protocol-side state changes;
- deterministic handling when Mapping traversal raises or changes observable entry state;
- R9/R10 oversized-integer and runtime-setting receipt behavior;
- ordinary exact-dict positive and negative semantics;
- all no-current-effect boundaries.

## Frozen files

`OBL059_POSITIVE_APPLICABILITY_R11/positive_applicability_authority_r11.py`

`OBL059_POSITIVE_APPLICABILITY_R11/governed_bounded_court_r11.py`

The commit containing this manifest is the frozen R11 candidate identity. The R11 implementation and producer court must not be edited in place after this freeze.

## Separation

`SELF_REVIEW_PERFORMED = NO`

`INDEPENDENT_REVIEW_PERFORMED_BY_R11_REPAIR_WORKER = NO`

No actor activation, ADP-008 transition, ADP-019 occurrence admission, current-positive OBL056 entry, OBL055 execution, ENCOUNTER, OEE, project-current applicability, authority-index mutation, SUB-VOZHD E adoption, or HQ adoption is created by this candidate.

`OBL061 = HARD_BLOCKED`
