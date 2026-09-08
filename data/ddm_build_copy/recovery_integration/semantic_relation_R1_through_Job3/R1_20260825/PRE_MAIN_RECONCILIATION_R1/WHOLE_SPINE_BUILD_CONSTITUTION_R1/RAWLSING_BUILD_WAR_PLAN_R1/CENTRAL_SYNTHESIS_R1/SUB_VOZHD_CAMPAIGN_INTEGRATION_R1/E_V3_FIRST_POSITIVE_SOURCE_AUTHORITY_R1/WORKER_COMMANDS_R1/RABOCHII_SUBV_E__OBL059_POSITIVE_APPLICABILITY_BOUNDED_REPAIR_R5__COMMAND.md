# RABOCHII SUB-VOZHD E — OBL059 POSITIVE_APPLICABILITY — BOUNDED REPAIR R5 COMMAND R1

ROLE: `RABOCHII BOUNDED REPAIR IMPLEMENTER`

REPORTS TO: `SUB-VOZHD E`

LANE: `E2 / OBL059 — POSITIVE_APPLICABILITY R5 LARGE-INTEGER NEGATIVE-RECEIPT REPAIR`

WORKER BRANCH:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r5`

EXACT STARTING HEAD:
`a728990458a4a909186b99520df6bb1cc9a826f1`

FAILED FROZEN R4 CANDIDATE:
`830cc0442f34e8b28405006c031cc1d256893a17`

FAILED R4 REVIEW TERMINAL:
`FAIL__OBL059_R4_INDEPENDENT_REVIEW__LARGE_INTEGER_NEGATIVE_RECEIPT_CONSTRUCTION_INCOMPLETE`

SMALLEST BLOCKER:
`BLOCKER__OBL059_R4_EXACT_INTEGER_JSON_SAFE_CLASSIFICATION_OMITS_ENCODER_CONVERSION_LIMIT`

This is a repair-only continuation. Do not modify the frozen R4 candidate in place. Produce a new frozen R5 candidate.

## Read first

Read and obey the SUB-VOZHD E campaign charter, orchestration law, all OBL059 R1–R4 candidate/court/review/repair materials, the R4 independent review return at `a728990458a4a909186b99520df6bb1cc9a826f1`, and the current SUB-VOZHD E adjudication from its immutable campaign ref supplied with this command.

## Exact repair objective

Close the exact built-in large-integer malformed-binding receipt-construction gap without changing positive applicability semantics or broadening accepted input.

R4 safely avoids caller-controlled custom protocol behavior, but it treats every exact `int` as structurally JSON-safe. The independent review proved that exact integer `10 ** 5000`, when used as any required binding, is semantically malformed yet can still exceed Python's configured integer-to-string conversion limit during canonical proof encoding.

R5 must ensure that once a required binding is semantically determined malformed, negative-receipt construction remains total and deterministic even when an exact built-in integer cannot be safely converted by canonical JSON encoding.

At minimum the repair must make the R4 review case fail closed at all five required-binding positions:

- `actor_id`;
- `subject_id`;
- `world_id`;
- `time_id`;
- `adp010_opportunity_id`.

The result must be the required deterministic JSON-safe `NOT_DIRECTLY_APPLICABLE` receipt with the exact `MALFORMED_BINDING:<field>` basis, not an uncaught integer-conversion `ValueError`.

Do not depend on decimal string conversion merely to decide whether an integer is safe. Use bounded structural information that itself cannot trigger the configured decimal-conversion limit. Any diagnostic projection for oversized malformed integers must be deterministic, JSON-safe, and must not normalize or coerce the integer into a valid identifier.

## Preservation law

Preserve all R4 controls independently confirmed green:

- exact-built-in-only traversal for malformed diagnostic projection;
- no invocation of caller-controlled Mapping/list/set/tuple/display/hash/equality/order behavior;
- safe handling of hostile custom keys/values nested in exact built-in containers;
- cycles, mutual recursion, shared references, depth/breadth limits;
- bytes, set, frozenset, opaque and mixed malformed structures;
- deterministic repeated negative receipts/proofs and meaningful structural distinction;
- exact ordinary R3 JSON-safe positive/negative/malformed behavior;
- exact actor/subject/world/time/ADP-010 opportunity binding semantics;
- wrong scope/authority/evidence/project-current rejection;
- adjacent-field non-substitution;
- unrelated internal TypeError/ValueError/RuntimeError visibility;
- no malformed-to-positive coercion;
- no project-current effects.

Do not broaden ownership into OBL058 or OBL060 and do not alter comparator/PSEPF/OBL032/architecture/topology/sibling lanes.

## Governed R5 court requirements

Freeze the new R5 candidate before governed evidence execution. The repair court must rerun material inherited controls and include direct regressions for:

- exact integers around and far beyond the runtime decimal conversion boundary;
- positive and negative large integers;
- zero/small/ordinary integers as preservation controls;
- `10 ** 5000` at every required-binding position;
- larger magnitudes than the reproduced case without decimal conversion during safety classification/projection;
- nested oversized integers in exact built-in containers reachable by malformed projection;
- deterministic repeated negative receipts/proof hashes for equivalent oversized-integer malformed inputs;
- safe distinction where required without serializing the full decimal integer;
- no uncaught integer-string-conversion `ValueError` for commissioned malformed-binding cases;
- no malformed oversized integer becoming a valid applicability identifier;
- exact preservation of custom-protocol, cycle/depth, JSON-safe, scope/authority/evidence/current-boundary controls;
- deliberate unrelated programmer errors outside this malformed-receipt boundary remain visible.

Do not solve this by globally weakening Python's safety limit or by installing a process-global runtime setting whose side effects alter unrelated code behavior unless repository governance already explicitly authorizes such a change; prefer a local bounded representation/decision path.

Record exact candidate, tests, evidence execution, run, job, artifact, ZIP SHA-256, and terminal.

## Separation of duties

`INDEPENDENT_REVIEW_PERFORMED_BY_R5_REPAIR_WORKER = NO`

Do not commission, perform, or claim the fresh independent review of the R5 candidate. If the repair court is green, return to SUB-VOZHD E. SUB-VOZHD E alone will commission exactly one fresh distinct independent reviewer against the new frozen R5 candidate.

## Hard prohibitions

Do NOT create/activate an actor, execute ADP-008, admit ADP-019 occurrence, own OBL058 permission or OBL060 independence, create ENCOUNTER, realize OEE, execute OBL055, install current-positive OBL056, or create project-current applicability.

Do NOT claim SUB-VOZHD E adoption or HQ adoption.

## Required return

Return a durable repository packet containing the new frozen R5 candidate identity, exact bounded repair description, governed court identities/results, direct regressions for the large-integer blocker plus preservation controls, no-self-review attestation, no-current-effect attestation, and recommendation to SUB-VOZHD E.

Terminal:

`RABOCHII_SUBV_E_OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R5__RETURN_TO_SUB_VOZHD_E`
