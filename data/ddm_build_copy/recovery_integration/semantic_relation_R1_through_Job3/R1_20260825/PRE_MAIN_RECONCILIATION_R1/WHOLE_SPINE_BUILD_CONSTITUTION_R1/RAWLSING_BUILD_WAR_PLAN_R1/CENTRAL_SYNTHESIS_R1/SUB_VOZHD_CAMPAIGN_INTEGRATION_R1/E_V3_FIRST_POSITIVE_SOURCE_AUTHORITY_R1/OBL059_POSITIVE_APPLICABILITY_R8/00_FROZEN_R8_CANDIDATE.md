# OBL059 POSITIVE_APPLICABILITY — FROZEN R8 CANDIDATE

Status: `FROZEN_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED`

Worker branch:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r8`

Exact worker start:
`6f7814b0489fb625f72c3e4741ae16b854767efc`

Campaign authority consumed prospectively:
`8137de980fc55c3b65ae94ba5052178bd50d7939`

Campaign tree:
`5799732ef3b3f7efedb370546cd550bd90b89930`

Failed frozen R7 candidate retained unchanged:
`87bb8a7bbdd22085ad0cd759230b9efdc74d3fb5`

R7 review blocker:
`BLOCKER__OBL059_R7_NESTED_MAPPING_FIELD_ACCESS_CAN_ESCAPE_AFTER_OUTER_SNAPSHOT`

## R8 repair boundary

R8 changes only nested `Mapping` nodes actually consumed by the frozen OBL059 scope/evidence evaluator after an exact outer dictionary exists.

The repair preserves R7 outer-carrier law and R6 integer/runtime-setting law.

Before semantic field access, R8 takes a bounded one-shot snapshot of any non-exact `Mapping` found at:

- `opportunity`;
- top-level `evidence`;
- `evidence.subject_classification`;
- `evidence.actor_activation`;
- `evidence.developmental_phase`.

If a snapshot succeeds, the exact dictionary snapshot is used for all later semantic access and the original custom mapping is never consulted again.

If a snapshot raises during its bounded traversal, the affected nested node is replaced with `None` in a safe exact-dict working packet. Frozen evaluation then returns its existing field-specific negative classification, including `OPPORTUNITY_BINDING_MISSING_OR_MALFORMED`, `EVIDENCE_MISSING_OR_MALFORMED`, `STRUCTURAL_CLASSIFICATION_EVIDENCE_MISSING`, `ACTOR_ACTIVATION_EVIDENCE_MISSING`, or `DEVELOPMENTAL_PHASE_EVIDENCE_MISSING` as applicable.

Exact-dict packets with no custom nested mappings remain on the unchanged R7/R6 path. Stable lawful nested mappings therefore preserve the same meaning as their equivalent exact-dict representation.

The exception boundary is confined to one-shot nested snapshot traversal. Unrelated implementation errors after a successful snapshot remain visible.

## Frozen executable and producer court

Executable:
`E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL059_POSITIVE_APPLICABILITY_R8/positive_applicability_authority_r8.py`

Producer court:
`E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL059_POSITIVE_APPLICABILITY_R8/governed_bounded_court_r8.py`

The commit containing this manifest, executable, and producer court is the frozen R8 candidate identity. It must not be edited in place after freeze.

## Separation and no-current-effect boundary

`SELF_REVIEW_PERFORMED = NO`

`INDEPENDENT_REVIEW_PERFORMED_BY_R8_REPAIR_WORKER = NO`

No actor activation, ADP-008 transition, ADP-019 occurrence admission, OBL058/OBL060 ownership, current-positive OBL056 entry, OBL055 execution, ENCOUNTER, OEE, project-current applicability, authority-index mutation, SUB-VOZHD E adoption, HQ adoption, or OBL061 authorization is created by this candidate.
