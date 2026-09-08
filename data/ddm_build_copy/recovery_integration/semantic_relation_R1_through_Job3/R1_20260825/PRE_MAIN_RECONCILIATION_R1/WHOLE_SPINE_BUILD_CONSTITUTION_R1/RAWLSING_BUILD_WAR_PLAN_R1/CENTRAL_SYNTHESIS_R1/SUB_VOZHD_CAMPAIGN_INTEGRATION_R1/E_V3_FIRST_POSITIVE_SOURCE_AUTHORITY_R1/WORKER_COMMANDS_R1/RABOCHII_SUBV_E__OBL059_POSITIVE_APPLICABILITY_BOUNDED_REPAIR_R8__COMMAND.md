# RABOCHII SUB-VOZHD E — OBL059 POSITIVE_APPLICABILITY — BOUNDED REPAIR R8 COMMAND R1

ROLE: `RABOCHII BOUNDED REPAIR IMPLEMENTER`

REPORTS TO: `SUB-VOZHD E`

LANE: `E2 / OBL059 — POSITIVE_APPLICABILITY R8 NESTED-MAPPING SNAPSHOT REPAIR`

WORKER BRANCH:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r8`

EXACT STARTING HEAD:
`6f7814b0489fb625f72c3e4741ae16b854767efc`

FAILED FROZEN R7 CANDIDATE:
`87bb8a7bbdd22085ad0cd759230b9efdc74d3fb5`

R7 REVIEW RECOMMENDATION:
`FAIL__DO_NOT_ADOPT_OBL059_R7_CANDIDATE`

R7 REVIEW TERMINAL:
`FAIL__OBL059_R7_INDEPENDENT_REVIEW__NESTED_MAPPING_ACCESS_ESCAPES_NEGATIVE_RECEIPT`

SMALLEST BLOCKER:
`BLOCKER__OBL059_R7_NESTED_MAPPING_FIELD_ACCESS_CAN_ESCAPE_AFTER_OUTER_SNAPSHOT`

This is a repair-only continuation. Do not modify the frozen R7 candidate in place. Produce a new frozen R8 candidate.

## Read first

Read and obey the SUB-VOZHD E campaign charter, inter-campaign orchestration law, the OBL059 R1–R7 candidate/court/review/repair returns needed to understand the lane, the R7 independent review return at `6f7814b0489fb625f72c3e4741ae16b854767efc`, and the current SUB-VOZHD E adjudication from its immutable campaign ref supplied prospectively with this command.

## Exact repair objective

Close only the remaining nested Mapping field-access defect.

R7 successfully bounded the outer non-exact Mapping carrier by taking a one-shot safe snapshot before semantic evaluation. The remaining weakness is that nested values already inside an exact-dict/snapshotted packet can themselves be custom `Mapping` objects and are later consumed directly by inherited scope/evidence checks through caller-defined methods such as `.get(...)`.

R8 must ensure that every nested Mapping node actually consumed by OBL059 scope/evidence evaluation is behind an equivalent bounded deterministic field-access boundary before semantic use.

A lawful implementation may snapshot the required nested Mapping nodes into exact built-in structures once, or use another bounded mechanism with equivalent guarantees. It must not rely on later direct calls to caller-defined Mapping methods during semantic evaluation.

Where an existing valid nested Mapping is semantically admitted by the current contract, its successful bounded snapshot must preserve the same meaning as the equivalent exact-dict representation. A malformed or throwing nested Mapping must fail closed into the existing deterministic negative-receipt path and must not escape an exception.

Do not globally swallow unrelated implementation errors after successful snapshot. Preserve programmer-error visibility outside the malformed-carrier boundary.

## Required direct regressions

The producer court must reproduce and close all three exact R7 review manifestations:

1. exact-dict outer packet with custom Mapping at `opportunity`; inherited field access would raise `RuntimeError("nested-get-failure")`;
2. exact-dict outer packet with custom Mapping at top-level `evidence`; inherited field access would raise;
3. exact-dict outer packet with custom Mapping at `evidence.actor_activation`; inherited field access would raise.

Each must return a deterministic JSON-safe negative receipt under the existing classification law rather than raise.

## Nested carrier surface

Exercise caller-defined methods that could otherwise become executable during nested snapshot/access, including where reachable:

- `keys()`;
- `__iter__`;
- `__getitem__`;
- `get()`;
- `__len__`;
- `items()`;
- `values()`;
- containment;
- equality/order helpers;
- display/representation;
- hashing or convenience methods.

A successful one-shot nested snapshot must not consult the original custom Mapping again later in evaluation.

## Preservation law

Preserve independently confirmed R7/R6 behavior, including:

- exact-dict outer packet semantics;
- successful stable authorized custom outer Mapping equivalence;
- outer snapshot failure -> deterministic malformed negative receipt;
- one-shot outer carrier snapshot with no later re-consultation;
- mapping-like objects that are not authorized Mapping instances do not gain carrier status by resemblance;
- oversized exact integers remain deterministic and JSON-safe;
- the R6 mutable integer-setting/time-of-check closure remains total;
- nested oversized integers remain fail-closed and deterministic;
- deterministic proof projection, cycle/shared-reference/depth/breadth protections already present;
- wrong scope, wrong authority, stale evidence and project-current execution remain negative;
- adjacent narrative/routing/classification fields do not substitute for competent evidence;
- unrelated deliberate implementation errors after successful carrier snapshot remain visible;
- exact R8 revision identity;
- no project-current effect.

Do not enter OBL058/OBL060, comparator, PSEPF, OBL032, architecture/topology, sibling-campaign, or project-current semantics.

## Governed R8 court requirements

Freeze the new R8 candidate before governed evidence execution.

The producer court must include, at minimum:

- the three exact R7 nested Mapping regressions;
- throwing nested Mapping methods across reachable access forms;
- stable valid nested Mapping equivalence to exact dict where admitted;
- one-shot nested snapshot/no second consultation;
- nested Maps inside opportunity/evidence/evidence components actually read by evaluation;
- nested oversized exact integers and threshold controls;
- cycles/shared structures where reachable through admitted built-in containers;
- repeated evaluation determinism;
- inherited outer Mapping R7 regression family;
- inherited R6 runtime integer-limit-change regressions;
- ordinary exact-dict positive and negative controls;
- wrong scope/authority/evidence/current-boundary controls;
- unrelated programmer-error visibility after successful snapshot;
- no malformed-to-valid coercion;
- no project-current positive applicability, current-positive OBL056, OBL055 execution, ENCOUNTER, actor activation, occurrence admission, or OEE path.

Record exact candidate, tests, governed evidence execution, run, job, artifact, ZIP SHA-256 and court terminal.

## Separation of duties

`INDEPENDENT_REVIEW_PERFORMED_BY_R8_REPAIR_WORKER = NO`

Do not commission, perform or claim the fresh independent review of the R8 candidate. If the producer court is green, return to SUB-VOZHD E. SUB-VOZHD E alone will commission exactly one fresh distinct reviewer against the new frozen R8 candidate.

## Hard prohibitions

Do NOT create project-current positive applicability, causal-use permission, witness independence, actor state, ADP-008 transition, ADP-019 occurrence, ENCOUNTER, OEE, current-positive OBL056 entries, or execute OBL055.

Do NOT claim SUB-VOZHD E adoption or HQ adoption.

## Required durable return

Return a durable repository packet containing the new frozen R8 candidate identity, exact repair description, governed court identities/results, direct regression coverage for the R7 nested Mapping blocker family, no-self-review attestation, no-current-effect attestation, and recommendation to SUB-VOZHD E.

Terminal:

`RABOCHII_SUBV_E_OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R8__RETURN_TO_SUB_VOZHD_E`
