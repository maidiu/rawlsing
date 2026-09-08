# OBL058 — CAUSAL_USE_PERMISSION — FROZEN REPAIRED CANDIDATE AUTHORITY R9

## Status

`FROZEN_REPAIRED_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED`

R9 repairs only the native-core binding/source-origin seam returned by the exactly-one fresh R8 independent review. It preserves the R8 native POSIX broker exchange, the R7 native object-generation/lifecycle mechanism, the R6 requester-generation and semantic controls, and the noncurrent-only boundary. This repair worker performs no independent review.

## Exact predecessor

- failed frozen R8 target: `50063aa6667371e3de5a19c775b1b0818b2f734a`
- R8 review terminal: `FAIL__OBL058_R8_INDEPENDENT_REVIEW__NATIVE_IMPORT_CACHE_CAN_SUBSTITUTE_SOURCE_DECISION`
- smallest blocker: `BLOCKER__OBL058_R8_NATIVE_IMPORT_CACHE_ENTRY_IS_ACCEPTED_WITHOUT_SOURCE_ORIGIN_VALIDATION`
- required next property: `REQUIRES__R8_NATIVE_CORE_BINDING_TO_VALIDATE_SOURCE_ORIGIN_BEFORE_TRUSTING_PREEXISTING_IMPORT_CACHE_STATE`

## R9 identities

- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0`
- R9 mechanism revision: `OBL058_CAUSAL_USE_PERMISSION_NATIVE_BINDING_MECHANISM_R9@1.0.0`
- Python surface: `causal_use_permission_candidate_r9.py`
- native mechanism reused unchanged from frozen R8: `obl058_r8_native.c` plus its three include parts
- producer court: `test_bounded_repair_r9.py`

The semantic receipt body and decision law are unchanged. R9 changes only how the Python candidate accepts the repository-owned native core.

## Exact R9 repair

R8 returned any pre-existing `sys.modules['_obl058_r8_native']` object directly. An ordinary Python module could therefore imitate the expected names and become the apparent decision source before the genuine native core was loaded.

R9 no longer treats import-cache presence or name/shape as sufficient. Before a cached or newly loader-produced object becomes authoritative, R9 validates all of the following:

1. the module name is exactly `_obl058_r8_native`;
2. the module file and import-spec origin resolve to the exact compiled artifact path derived from the frozen R8 native source bytes;
3. every correctness-relevant module entry point is a genuine CPython built-in module function rather than a Python callable;
4. each such built-in function is non-rebindably bound (`__self__`) to that exact module object;
5. `NativeReceiptBase` is the expected extension type, claims the exact native module, and its source issue/validate/close/body/status entries are genuine C method descriptors.

An ordinary Python module can copy names and values, and can even claim the expected file path, but it cannot create a CPython built-in module function whose C-level binding is that same ordinary module object. A shape-compatible import-cache substitute therefore fails source-origin validation before broker start, issuance, or validation.

R9 also delays insertion of a newly loader-produced native module into `sys.modules` until this source-origin validation succeeds. If Python import/loader attributes are rebound so that a Python module is returned instead of the extension, the same validation fails closed.

After genuine binding, replacing or removing the import-cache entry does not change the retained `_native` reference used by live R9 receipt operations. Reload/reimport surfaces must either rebind to a verified genuine core or fail closed; they cannot substitute a Python decision source.

## Preserved R8/R7 controls

R9 preserves the independently confirmed controls from R8/R7: native POSIX broker exchange independent of Python socket construction; broker peer PID/UID/process-start verification and request identity matching; endpoint/broker/authority-child loss failing closed; native receipt generation identity and C-owned lifetime reservation; weak-reference/finalizer irrelevance; explicit-close revocation and duplicate-close non-authorization; requester process-generation and fork isolation; one-shot source-owned scope/basis/fixture decision; exact five-field binding; one frozen positive basis and unregistered-basis `DENY`; field-specific `NONCURRENT_SYNTHETIC` and current-shaped rejection; authority/schema/fixture/proof/authority-instance/content-integrity validation; construction/reconstruction/proxy/copy/serialization rejection; distinct equal-body receipts; cross-scope/cross-module rejection; stable repeated/concurrent validation; surrogate basis denial; no public source-basis registration; and no project-current effect.

## Producer verification target

The R9 producer court includes direct checks for the exact R8 import-cache finding; preseed before candidate import; cache replacement before issuance and after issuance; reload/reimport and loader substitution; Python transport-constructor replacement; genuine `PERMIT`/`DENY`; lifecycle/fork/close preservation; loss and endpoint fail-closed controls; exact scope/basis/current boundaries; construction and serialization rejection; concurrency; and no-current-effect surfaces.

The governed repository court against the exact freeze commit is the producer evidence of record.

## Separation / no current effect

`SELF_REVIEW_PERFORMED = NO`

`INDEPENDENT_REVIEW_PERFORMED_BY_R9_REPAIR_WORKER = NO`

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`ENCOUNTER_CREATED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`OBL061_UNBLOCKED = NO`

## Required next gate

Freeze this exact R9 candidate, obtain a green governed producer court, and return to SUB-VOZHD E. If accepted, SUB-VOZHD E alone may commission exactly one fresh distinct independent review of the frozen R9 target.
