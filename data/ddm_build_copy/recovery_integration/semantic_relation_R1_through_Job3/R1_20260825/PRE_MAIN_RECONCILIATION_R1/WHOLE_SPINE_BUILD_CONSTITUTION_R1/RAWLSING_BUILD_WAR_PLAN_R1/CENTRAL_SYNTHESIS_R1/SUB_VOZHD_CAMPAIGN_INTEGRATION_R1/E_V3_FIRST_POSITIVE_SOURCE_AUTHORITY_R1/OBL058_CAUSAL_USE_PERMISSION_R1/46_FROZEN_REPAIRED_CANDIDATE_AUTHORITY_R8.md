# OBL058 — CAUSAL_USE_PERMISSION — FROZEN REPAIRED CANDIDATE AUTHORITY R8

## Status

`FROZEN_REPAIRED_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED`

R8 repairs only the broker identity / decision-path defect returned by the exactly-one fresh R7 independent review. It preserves the R7 native object-generation/lifecycle mechanism and the previously confirmed requester-generation, fork, close, source-basis, scope, receipt-integrity, and noncurrent-only controls. This repair worker does not perform independent review.

## Exact upstream identities

- exact R8 worker start: `ce3a3f9b3a65e396ab29053a8c60504e550dc7fb`
- immutable SUB-VOZHD E campaign authority consumed prospectively: `c5aaf1fc113fe53c202396144c949d57468e1f45`
- failed frozen R7 candidate retained unchanged: `adf20f8ebf7ff0d7fe32f7de94db02574cc2bb3d`
- R7 review disposition: `FAIL__OBL058_R7_INDEPENDENT_REVIEW__MUTABLE_PYTHON_SOCKET_CONSTRUCTOR_CAN_SUBSTITUTE_BROKER_DECISION`
- R7 smallest blocker: `BLOCKER__OBL058_R7_BOUND_BROKER_REQUEST_TRUSTS_MUTABLE_PYTHON_SOCKET_CONSTRUCTOR_FOR_PEER_IDENTITY`
- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0`
- R8 mechanism revision: `OBL058_CAUSAL_USE_PERMISSION_BROKER_TRANSPORT_MECHANISM_R8@1.0.0`
- Python surface: `causal_use_permission_candidate_r8.py`
- native object-generation + broker-transport core: `obl058_r8_native.c`
- producer court: `test_bounded_repair_r8.py`

The semantic authority and receipt schema remain unchanged because R8 does not change the source-owned decision law or receipt body. R8 changes only the repository-local implementation path used to establish broker identity and carry the broker decision.

## Exact R8 repair

R7 retained the R6 Python broker request function. That function dynamically resolved Python's mutable `socket.socket` constructor and accepted peer-credential and response data from the resulting Python object. The R7 independent review showed that ordinary process-local rebinding of that constructor could make an unregistered basis that genuinely returned `DENY` appear to return `PERMIT` without a source-owned broker exchange.

R8 removes Python transport construction from the correctness path.

The R8 native CPython extension now owns both the R7 receipt generation/lifetime reservation and the broker exchange. It starts one dedicated source broker process from the repository sibling `causal_use_permission_candidate_r6.py` using native `fork`/`exec`, records the exact broker PID, UID and `/proc/<pid>/stat` start-time generation, and holds the broker socket pathname in native static state. Issuance, validation and close use native POSIX `socket`, `connect`, `SO_PEERCRED`, `send` and `recv` directly. They do not resolve or call Python's `socket.socket`, `_socket.socket`, a Python constructor alias, or the inherited R6 `_bound_broker_request`.

The native transport serializes the bounded broker request itself and parses the broker's flat canonical response itself. It verifies the exact response request identity before returning any decision to the Python surface. The Python validation wrapper additionally checks that the response authority-instance identity equals the native receipt body's authority-instance identity.

The native broker start operation is one-shot. There is no public transport reconfiguration function. A later caller may stop the broker and thereby force fail-closed behavior, but cannot restart the same native authority transport against a caller-selected peer.

## R7 lifecycle preservation

Each issued receipt still has a native, non-Python generation key and a C-allocated lifetime reservation. Ordinary caller reference release therefore cannot recycle a live issued generation while broker authority remains active. Explicit close retires broker authority first and then releases the native reservation. Duplicate close remains non-authorizing. Ordinary Python weak-reference/finalizer registries do not control correctness.

## R6 requester-generation preservation

The dedicated broker still derives requester PID, UID and process-start generation from the live Unix-domain peer. A forked child therefore cannot validate or close a parent-issued receipt even though the inherited native receipt carries the same generation key. Parent authority remains intact after child rejection.

## Preserved semantic controls

R8 preserves:

- one frozen source-owned positive basis;
- exact actor/world/subject/time/transition binding;
- field-specific `NONCURRENT_SYNTHETIC` namespace enforcement;
- exact current first-canary and project-current-shaped identity rejection;
- unregistered-basis `DENY`;
- no caller-supplied permission boolean or basis kind;
- exact authority/schema/fixture/scope/basis-proof/authority-instance/content-integrity checks;
- direct-constructor, subclass, Mapping/proxy, JSON reconstruction, copy/deepcopy and serialization rejection on ordinary validation paths;
- cross-scope and cross-receipt reuse rejection;
- stable repeated and concurrent same-process validation;
- broker loss and authority-child loss fail closed;
- classification/routing/occurrence/proximity/narrative-like surrogate basis strings remain `DENY`;
- no public source-basis registration surface;
- no project-current effect.

## Producer pre-freeze verification

The exact native C source compiled successfully in the local CPython environment. A local native transport harness confirmed direct source-broker exchange, request-identity checking, native close, and fail-closed post-close behavior. A local R8 producer subset confirmed that replacing Python `socket.socket` and `_socket.socket` does not affect the R8 issue/validate path. The governed repository court remains the evidence of record.

## Authority ceiling / separation

`INDEPENDENT_REVIEW_PERFORMED_BY_R8_REPAIR_WORKER = NO`

`SELF_REVIEW_PERFORMED = NO`

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`CURRENT_ACTOR_OR_RUNTIME_MUTATION = NO`

`OBL055_EXECUTED = NO`

`ENCOUNTER_CREATED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`AUTHORITY_INDEX_EFFECT_CREATED = NO`

`SUB_VOZHD_E_ADOPTION_CLAIMED = NO`

`HQ_ADOPTION_CLAIMED = NO`

`OBL061_UNBLOCKED = NO`

## Required next gate

Freeze this exact candidate and run the governed R8 producer court. If green, return it to SUB-VOZHD E. Do not perform or commission the fresh R8 independent review from this worker.
