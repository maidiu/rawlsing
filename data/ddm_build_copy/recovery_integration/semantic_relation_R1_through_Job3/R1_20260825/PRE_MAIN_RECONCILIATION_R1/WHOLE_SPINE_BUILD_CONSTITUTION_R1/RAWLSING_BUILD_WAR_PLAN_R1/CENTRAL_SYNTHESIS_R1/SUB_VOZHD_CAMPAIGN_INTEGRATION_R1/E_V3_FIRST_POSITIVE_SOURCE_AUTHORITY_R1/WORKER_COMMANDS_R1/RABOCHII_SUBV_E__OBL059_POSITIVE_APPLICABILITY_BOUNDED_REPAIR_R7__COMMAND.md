# RABOCHII SUB-VOZHD E — OBL059 POSITIVE_APPLICABILITY — BOUNDED REPAIR R7 COMMAND R1

ROLE: `RABOCHII BOUNDED REPAIR IMPLEMENTER`

REPORTS TO: `SUB-VOZHD E`

LANE: `E2 / OBL059 — POSITIVE_APPLICABILITY R7 OUTER PACKET MAPPING-TRAVERSAL REPAIR`

WORKER BRANCH:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r7`

EXACT STARTING HEAD:
`6468d775eb15076e8ca243c95180fdfecb41ce27`

FAILED FROZEN R6 CANDIDATE:
`5ca7380bd17b3dec271fe5a8c6bf22656f55b647`

R6 REVIEW TERMINAL:
`FAIL__OBL059_R6_INDEPENDENT_REVIEW__CUSTOM_MAPPING_PACKET_TRAVERSAL_ESCAPES_NEGATIVE_RECEIPT`

SMALLEST BLOCKER:
`BLOCKER__OBL059_R6_CUSTOM_MAPPING_PACKET_CAN_ESCAPE_VIA_CALLER_CONTROLLED_KEYS_BEFORE_NEGATIVE_RECEIPT`

This is repair-only work. Do not modify the frozen R6 candidate in place. Produce a new frozen R7 candidate. Do not perform or commission its independent review.

## Read first

Read and obey the SUB-VOZHD E campaign charter, orchestration law, OBL059 R1-R6 candidate/court/review/repair returns, the R6 independent review return at `6468d775eb15076e8ca243c95180fdfecb41ce27`, and the current SUB-VOZHD E campaign adjudication supplied prospectively as an immutable ref.

## Exact repair objective

Close only the outer custom-Mapping packet traversal defect returned by the exactly-one R6 independent review.

R6 correctly closes the mutable integer-conversion-setting race for exact-dict packets. The remaining defect is that a non-exact-dict `collections.abc.Mapping` outer packet is delegated into inherited code that eventually executes `dict(packet)`, invoking caller-controlled methods such as `keys()` before a deterministic negative receipt can be constructed.

R7 must ensure that unsupported or malformed outer packet carriers cannot execute caller-controlled mapping protocol behavior before fail-closed classification/receipt construction.

The worker must establish the authorized outer-carrier law from frozen prior authority before choosing the smallest implementation:

1. If non-exact-dict Mapping objects are not an authorized positive carrier, reject/classify them at the outer carrier boundary without invoking caller-defined traversal methods.
2. If prior authority explicitly requires non-exact-dict Mapping carriers to remain acceptable, preserve that requirement through a source-owned safe snapshot/boundary that prevents caller-controlled protocol exceptions from escaping malformed-input handling.
3. Do not silently widen or narrow direct-positive applicability semantics.
4. Do not infer positive applicability from the mere mapping-like shape of a custom object.
5. Preserve the R6 stable malformed-integer design and all already-correct scope/evidence/current-state boundaries.

The implementation must not require caller-defined `keys`, `__iter__`, `__getitem__`, `__len__`, `items`, `values`, `get`, containment, display, hashing, equality, ordering, conversion, or other arbitrary protocol behavior merely to produce the fail-closed outcome for an unsupported/malformed outer carrier.

## Governed producer court requirements

Freeze the new R7 candidate before governed evidence execution. The independent R6 blocker must be directly reproduced and closed.

At minimum cover:

- custom Mapping outer packet with throwing `keys()`;
- throwing `__iter__`, `__getitem__`, `__len__`, `items()`, `values()`, `get()`, and containment independently;
- mapping lookalikes that are not actual Mapping instances;
- positive-looking custom Mapping packets: they must not become positive merely by resemblance or caller protocol behavior;
- custom Mapping whose hidden backing data would contain the exact oversized malformed `actor_id` case;
- exact dict packets containing custom Mapping/custom objects as nested malformed binding values, with deterministic projection and no custom protocol traversal where inherited R4-R6 law requires isolation;
- exact built-in dict/list/tuple/set/frozenset malformed structures, cycles, shared references and depth ceilings;
- R6 fixed safety-threshold edges and the reproduced in-flight runtime conversion-setting changes;
- oversized positive/negative exact integers at all five required bindings and as exact built-in mapping keys;
- deterministic repeated receipts/proofs and distinction for different malformed values;
- ordinary authorized exact-dict positive control and ordinary exact-dict negative controls;
- wrong execution scope, authority/source/evidence/kind/current-boundary rejection;
- no inference from unrelated semantics;
- deliberate internal programmer TypeError/ValueError/RuntimeError outside the malformed carrier/projection boundary remain visible;
- no project-current actor/runtime/OBL056/OBL055/ENCOUNTER/OEE/authority-index effect.

Record exact candidate SHA, executable/test/wrapper/spec identities, governed evidence execution, run/job, artifact, ZIP SHA-256, court result, no-self-review attestation and return terminal.

## Separation of duties

`SELF_REVIEW_PERFORMED = NO`

`INDEPENDENT_REVIEW_PERFORMED_BY_R7_REPAIR_WORKER = NO`

If producer evidence is green, return the new frozen candidate to SUB-VOZHD E. SUB-VOZHD E alone may commission exactly one fresh distinct independent reviewer for that R7 candidate.

## Hard prohibitions

Do not enter OBL058/OBL060 ownership, comparator, PSEPF, OBL032, architecture/topology, sibling campaign, actor activation, ADP-008 execution, ADP-019 occurrence admission, current-positive OBL056 installation, OBL055 execution, ENCOUNTER, OEE realization, or HQ adoption.

`OBL061 = HARD_BLOCKED`

## Required return

Terminal:

`RABOCHII_SUBV_E_OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R7__RETURN_TO_SUB_VOZHD_E`
