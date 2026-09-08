# RABOCHII SUB-VOZHD E — OBL059 POSITIVE_APPLICABILITY — BOUNDED REPAIR R3 COMMAND R1

ROLE: `RABOCHII BOUNDED REPAIR IMPLEMENTER`

REPORTS TO: `SUB-VOZHD E`

LANE: `E2 / OBL059 — POSITIVE_APPLICABILITY R3 NEGATIVE-RECEIPT SERIALIZATION-BOUNDARY REPAIR`

WORKER BRANCH:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r3`

EXACT STARTING HEAD:
`917ee1655f7a4c26277896ef12d788acce15a1c9`

FAILED FROZEN R2 CANDIDATE:
`ff4f7c8a135997a4e4dd0b9dcb405a143fc6f749`

FAILED R2 REVIEW TERMINAL:
`FAIL__OBL059_R2_INDEPENDENT_REVIEW__NON_JSON_MALFORMED_BINDING_FALLBACK_INCOMPLETE`

SMALLEST BLOCKER:
`BLOCKER__OBL059_R2_NEGATIVE_RECEIPT_FALLBACK_COVERS_ONLY_ONE_JSON_ERROR_SHAPE`

This is a repair-only continuation. Do not modify the frozen R2 candidate in place. Produce a new frozen R3 candidate.

## Read first

Read and obey the SUB-VOZHD E campaign charter, orchestration law, complete OBL059 R1/R2 candidate/court/review/repair materials, the R2 independent review return at `917ee1655f7a4c26277896ef12d788acce15a1c9`, and the current SUB-VOZHD E adjudication from its immutable campaign ref supplied with this command.

## Exact repair objective

Close the incomplete malformed/non-JSON negative-receipt boundary without changing positive applicability semantics or widening accepted input.

R2 repaired the original `bytes`/`set`/opaque-object serialization failure only when the thrown exception was a `TypeError` whose text contained one exact phrase. Independent review established that ordinary JSON serialization failures have additional standard shapes.

R3 must ensure that once a required binding has been semantically determined malformed, receipt construction cannot throw merely because the original malformed value cannot be safely JSON-serialized.

At minimum repair both independently reproduced R2 escapes:

1. a malformed required binding containing a mapping with a `bytes` key must return its deterministic `MALFORMED_BINDING:<field>` negative receipt rather than re-raise `TypeError: keys must be str, int, float, bool or None, not bytes`;
2. a malformed circular-list required binding must return its deterministic `MALFORMED_BINDING:<field>` negative receipt rather than re-raise `ValueError: Circular reference detected`.

Do not key correctness to exception-message text. Do not broadly swallow unrelated programmer errors. Prefer a bounded negative-receipt construction path that does not depend on raw malformed object serializability after the semantic malformed-binding reason is already known.

Any diagnostic projection used for proof construction must itself be deterministic, JSON-safe, cycle-safe, and incapable of coercing malformed content into a valid binding.

## Preservation law

Preserve exact R1/R2 behavior for ordinary JSON-safe valid and invalid packets except for the bounded malformed/non-serializable receipt-construction repair.

Preserve:

- exact positive applicability decision semantics;
- exact actor/subject/world/time/ADP-010 opportunity bindings;
- authority and receipt-kind checks;
- wrong-scope/stale/malformed rejection;
- no inference from V554, CAN-001, CAN-003, routing, classification, occurrence, permission, witness independence, ADP-010 realization, or narrative plausibility;
- `PROJECT_CURRENT` issuance hard block;
- no actor creation/activation, ADP-008 transition, ADP-019 occurrence, current-positive OBL056, OBL055, ENCOUNTER, OEE, or authority-index mutation.

Do not broaden ownership into OBL058 or OBL060 and do not alter comparator/PSEPF/OBL032/architecture/topology/sibling lanes.

## Governed R3 court requirements

Freeze the new R3 candidate before governed evidence execution. The bounded repair court must rerun the material R1/R2 controls and include direct regressions for:

- mapping values with non-JSON-safe keys, including `bytes` keys, at every reachable required-binding position;
- circular lists and circular mappings at every reachable required-binding position;
- the original `bytes`, `set`, `frozenset`, and opaque-object malformed cases;
- nested malformed/non-serializable structures;
- deterministic repeated negative receipts for the same malformed semantic input class;
- cycle-safe proof/diagnostic construction;
- no uncaught commissioned `TypeError`, `ValueError`, recursion/serialization exception for malformed-binding cases;
- no malformed value normalized or coerced into positive applicability;
- exact preservation of valid JSON-safe positive and negative controls;
- wrong scope/authority/kind and project-current forbidden-effect controls.

The court must also prove the repair does not become a generic exception-masking wrapper: unrelated deliberate internal/programmer errors outside the commissioned malformed-receipt serialization boundary must not be silently converted into semantic negative receipts.

Record exact candidate, tests, evidence execution, run, job, artifact, ZIP SHA-256, and terminal.

## Separation of duties

`INDEPENDENT_REVIEW_PERFORMED_BY_R3_REPAIR_WORKER = NO`

Do not commission, perform, or claim the fresh independent review of the R3 candidate. If the R3 repair court is green, return it to SUB-VOZHD E. SUB-VOZHD E alone will commission exactly one fresh distinct independent reviewer against the new frozen R3 candidate.

## Hard prohibitions

Do NOT create/activate an actor, execute ADP-008, admit ADP-019 occurrence, own OBL058 permission or OBL060 independence, create ENCOUNTER, realize OEE, execute OBL055, install current-positive OBL056, or create project-current applicability.

Do NOT claim SUB-VOZHD E adoption or HQ adoption.

## Required return

Return a durable repository packet containing the new frozen R3 candidate identity, exact bounded repair description, governed court identities/results, direct regressions for both R2 blockers plus preservation controls, no-self-review attestation, no-current-effect attestation, and recommendation to SUB-VOZHD E.

Terminal:

`RABOCHII_SUBV_E_OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R3__RETURN_TO_SUB_VOZHD_E`
