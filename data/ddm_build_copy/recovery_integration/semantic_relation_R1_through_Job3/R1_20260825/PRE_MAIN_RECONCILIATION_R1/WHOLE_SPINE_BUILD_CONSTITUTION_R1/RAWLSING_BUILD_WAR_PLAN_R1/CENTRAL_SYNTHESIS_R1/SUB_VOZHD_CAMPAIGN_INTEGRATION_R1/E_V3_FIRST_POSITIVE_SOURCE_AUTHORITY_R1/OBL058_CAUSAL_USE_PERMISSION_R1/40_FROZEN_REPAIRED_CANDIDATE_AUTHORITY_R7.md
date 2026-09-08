# OBL058 — CAUSAL_USE_PERMISSION — FROZEN REPAIRED CANDIDATE AUTHORITY R7

## Status

`FROZEN_REPAIRED_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED`

R7 repairs only the object-generation retirement defect returned by the exactly-one fresh R6 independent review. It preserves the R6 requester-process generation repair, genuine broker binding, one-shot source decision, source-basis/scope semantics, and noncurrent-only boundary. This repair worker does not perform independent review.

## Exact identities

- failed frozen R6 candidate retained unchanged: `92418a9e13f55464a91c1c9f1deb96977bc294ef`
- R6 review terminal: `FAIL__OBL058_R6_INDEPENDENT_REVIEW__STALE_OBJECT_RECORD_RETIREMENT_NOT_INVARIANT`
- R6 smallest blocker: `BLOCKER__OBL058_R6_OBJECT_RECORD_RETIREMENT_DEPENDS_ON_CALLER_DETACHABLE_WEAKREF_FINALIZER`
- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0`
- R7 mechanism revision: `OBL058_CAUSAL_USE_PERMISSION_OBJECT_GENERATION_MECHANISM_R7@1.0.0`
- Python surface: `causal_use_permission_candidate_r7.py`
- native object-generation core: `obl058_r7_native.c`
- final producer court: `test_bounded_repair_r7_final.py`

The authority and receipt schema remain unchanged because R7 does not change the semantic receipt body or decision law. It changes only the repository-local mechanism that identifies and retains the exact issued object generation.

## Exact R7 repair

R6 used the process-local integer `id(receipt)` as the broker object key and relied on a Python `weakref.finalize` registration to retire that key when the issued object was released. The R6 independent review showed that the cleanup registration itself was inspectable and detachable.

R7 removes that cleanup dependency.

Each R7 receipt now owns a native unsigned object-generation key allocated by a compiled repository-local C extension. The key is not exposed as a Python attribute or getter and cannot be replaced through ordinary Python attribute assignment. The same native object carries the public receipt body, but the body is not authoritative by itself.

After source issuance succeeds, the native module holds a strong lifetime reservation in a C-allocated linked list of raw `PyObject*` references. The reservation is not a Python list/dict/set, is not stored in a weak-reference/finalizer registry, and is not exposed as a mutable module object. Consequently ordinary caller reference release cannot end the issued object generation or permit CPython to recycle its address while broker authority remains live.

Explicit `close()` first retires the broker record and only then releases the native lifetime reservation. Once closed, validation fails even if a caller still holds the Python receipt. A later Python object generation therefore cannot inherit a live broker record from the closed generation.

At interpreter teardown, remaining native reservations are released only after the source module begins teardown; the native deallocator attempts record retirement while the bound broker callable is still retained. This is lifecycle cleanup, not a source of positive authority.

## R6 process-generation control retained

The R7 native generation key is supplied to the unchanged R6 broker protocol as the broker `object_id`. The R6 broker continues to bind every issued record to OS-observed requester PID, UID, and `/proc/<pid>/stat` start-time generation. Therefore a fork-child copy of a receipt carries the same native generation key but presents a different requester process generation and remains rejected.

## Preserved semantic controls

R7 preserves:

- one frozen source-owned positive basis;
- exact actor/world/subject/time/transition binding;
- field-specific `NONCURRENT_SYNTHETIC` namespace enforcement;
- exact current first-canary and project-current-shaped identity rejection;
- unregistered-basis `DENY`;
- no caller-supplied permission boolean or basis kind;
- exact authority/schema/fixture/scope/basis-proof/authority-instance/content-integrity checks;
- constructor/subclass/Mapping/proxy/JSON reconstruction/copy/deepcopy/serialization rejection on ordinary validation paths;
- cross-scope and cross-receipt reuse rejection;
- denial of classification/routing/occurrence/proximity/narrative-like surrogate permission;
- no public source-basis registration surface;
- no project-current effect.

## Authority ceiling / no current effect

This candidate does not create or activate an actor, create positive applicability, admit an occurrence, prove contact-witness independence, create ENCOUNTER, realize OEE, install current-positive OBL056 state, execute OBL055, update project-current authority state, or claim SUB-VOZHD E/HQ adoption.

`INDEPENDENT_REVIEW_PERFORMED_BY_R7_REPAIR_WORKER = NO`

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`ENCOUNTER_CREATED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

## Required next gate

Run the governed producer court against this exact frozen R7 candidate. If green, return it to SUB-VOZHD E for exactly one fresh distinct independent review. Do not self-review.
