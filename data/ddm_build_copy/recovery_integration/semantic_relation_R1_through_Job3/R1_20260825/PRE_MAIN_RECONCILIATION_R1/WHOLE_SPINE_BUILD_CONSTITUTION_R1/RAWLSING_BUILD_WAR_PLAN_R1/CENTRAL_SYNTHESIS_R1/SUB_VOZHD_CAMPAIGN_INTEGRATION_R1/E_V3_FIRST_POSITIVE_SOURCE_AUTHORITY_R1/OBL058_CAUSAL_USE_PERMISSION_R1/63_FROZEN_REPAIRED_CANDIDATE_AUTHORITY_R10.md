# OBL058 — CAUSAL_USE_PERMISSION — FROZEN REPAIRED CANDIDATE AUTHORITY R10

## Status

`FROZEN_REPAIRED_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED`

R10 repairs only the public validation-dispatch seam returned by the exactly-one fresh R9 independent review. It preserves the independently confirmed R9 native binding/source-origin control, the R8 native POSIX broker exchange, the R7 native object-generation/lifecycle mechanism, the R6 requester-generation and semantic controls, and the noncurrent-only boundary. This repair worker performs no independent review.

## Exact predecessor

- failed frozen R9 target: `9b293aca913cff7f4d52d9e10dc08fcdb99127d9`
- R9 review terminal: `FAIL__OBL058_R9_INDEPENDENT_REVIEW__MUTABLE_RECEIPT_METHOD_CAN_SUBSTITUTE_NATIVE_DECISION`
- smallest blocker: `BLOCKER__OBL058_R9_PUBLIC_VALIDATOR_DISPATCHES_THROUGH_CALLER_MUTABLE_RECEIPT_CLASS_METHOD_LOOKUP`
- required next property: `REQUIRES__PUBLIC_VALIDATION_TO_INVOKE_THE_VERIFIED_NATIVE_ENTRY_WITHOUT_CALLER_MUTABLE_PYTHON_CLASS_METHOD_DISPATCH`

## R10 identities

- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0`
- R10 mechanism revision: `OBL058_CAUSAL_USE_PERMISSION_PUBLIC_NATIVE_DISPATCH_R10@1.0.0`
- Python surface: `causal_use_permission_candidate_r10.py`
- public-dispatch native source: `obl058_r10_dispatch.c`
- producer court: `test_bounded_repair_r10.py`
- frozen R9 native source-origin and broker/lifecycle implementation reused unchanged through `causal_use_permission_candidate_r9.py` and its verified native core.

The semantic receipt body and source decision law are unchanged. R10 changes only how the original public validation entry reaches the verified native decision method.

## Exact R10 repair

R9 correctly verifies the repository-owned native core, but its Python `validate_receipt()` function performed `receipt._source_validate(...)`. Because `IssuedReceipt` is a Python-defined subclass, ordinary runtime class mutation could replace that lookup target after the native core had been verified.

R10 introduces a small repository-local C extension dedicated to final public validation dispatch. At import time, after the R9 native core has passed its existing source-origin checks, the dispatch extension is itself source-origin validated and then bound once to:

- the exact R10 `IssuedReceipt` type;
- the exact `ExactScope` type;
- the contract error type;
- the exact verified native receipt base type;
- strong references to the native base's genuine `_source_validate` and `_body_json_copy` C method descriptors taken directly from the native base type dictionary.

The exported R10 `validate_receipt` object is the verified built-in C function itself. On each validation it requires the exact configured receipt type, snapshots and validates the exact scope instance dictionary through the generic-object implementation, and invokes the retained native C validation descriptor directly with the receipt and canonical scope dictionary. It does not resolve `_source_validate` through the receipt instance, Python subclass, metaclass, module alias, import cache, or a later Python callable.

The dispatch extension also obtains the receipt body through the retained native body descriptor and checks the broker response authority-instance identifier against the source-issued body before returning `PERMIT` or `DENY`.

Replacing `IssuedReceipt._source_validate`, installing a descriptor/property, replacing instance lookup behavior, rebinding candidate/native/dispatch module aliases, or replacing import-cache entries after genuine binding therefore does not redirect the original public validator object. A caller can of course replace the public module attribute itself, but that creates a different callable; it does not change the behavior of the original R10 public validator.

## Preserved controls

R10 is required to preserve, and the governed producer court is bound to check, the independently confirmed controls: R9 fake native import-cache rejection and C-extension source-origin binding; R8 native POSIX broker exchange independent of Python socket constructors; broker peer/request identity and process-generation checks; endpoint/broker/authority-child loss failing closed; R7 native generation identity and lifetime reservation; weak-reference/finalizer irrelevance; explicit-close revocation and duplicate-close non-authorization; requester-generation/fork parent-child isolation; one frozen positive source basis and unregistered-basis `DENY`; exact five-field scope; field-specific `NONCURRENT_SYNTHETIC` and current-shaped rejection; authority/schema/fixture/proof/authority-instance/content-integrity checks; construction/reconstruction/proxy/copy/serialization rejection; distinct equal-body receipts; cross-scope/cross-module rejection; stable repeated/concurrent validation; surrogate-basis denial; no public source-basis registration; and no project-current effect.

## Separation / no current effect

`SELF_REVIEW_PERFORMED = NO`

`INDEPENDENT_REVIEW_PERFORMED_BY_R10_REPAIR_WORKER = NO`

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

Obtain a green governed producer court against this exact frozen R10 candidate. If green, return it to SUB-VOZHD E. SUB-VOZHD E alone may then commission exactly one fresh distinct independent review of the frozen R10 target.
