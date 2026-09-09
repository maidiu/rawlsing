# OBL058 — CAUSAL_USE_PERMISSION — FROZEN REDESIGNED CANDIDATE AUTHORITY R11

## Status

`FROZEN_REDESIGNED_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED`

R11 is an abstraction-level redesign of the validation dispatch/binding boundary. It preserves the verified R9 native source core, native transport, object/requester generation controls, lifecycle controls, semantic receipt law, and noncurrent-only boundary. This worker performs producer implementation and producer verification only; no self-review or independent review is performed.

## Exact predecessor

- failed frozen R10 target retained unchanged: `0d23b02c75783033a4c8087b00721cb73a0924b4`
- R10 review return: `61b3731b0b20ed4ebdbe5918a076674c05cf403d`
- exact blocker: `BLOCKER__OBL058_R10_DISPATCH_VERIFIER_READS_MODULE_DICT_BUT_PUBLIC_VALIDATOR_BINDING_USES_CALLER_MUTABLE_MODULE_ATTRIBUTE_LOOKUP`
- R11 campaign authority: `4bf42274399aea600e28d9b69077dc5d6d3dfefa`

## R11 mechanism

- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0`
- mechanism revision: `OBL058_CAUSAL_USE_PERMISSION_RETAINED_VALIDATION_CAPABILITY_R11@1.0.0`
- Python surface: `causal_use_permission_candidate_r11.py`
- Python surface blob: `eb881597df670a8f13729c3a5affecee1fd331b3`
- native retained-capability source: `obl058_r11_dispatch_capability.c`
- native source blob: `608eab1479ae38a10d5edca2d0c24de22792e82d`
- producer court: `test_bounded_redesign_r11.py`
- producer court blob: `517b537194f1f8cec9b4e58ebbba5f76d1379a48`

## Governing redesign invariant

The exact validation capability that is authenticated is the exact capability retained and later invoked.

R11 authenticates the capability module and captures the exact `establish_capability`, `public_validate`, and descriptor-observation built-in function objects from the same verified module dictionary. Every accepted function must be a genuine CPython built-in function whose immutable `__self__` is the exact verified module object.

The authenticated `establish_capability` function is invoked directly as the captured object. Inside C, it binds the verified native receipt validation/body descriptors and returns the exact `public_validate` built-in obtained from the same C-owned module dictionary. Python requires that returned object to be identical (`is`) to the already-authenticated `public_validate` object. That exact object becomes the retained public validation capability.

No later module attribute lookup chooses the validator. Module-class customization, module `__getattribute__`, ordinary exported-name rebinding, `sys.modules` replacement, aliases, receipt-class method rebinding, descriptor replacement, or Python socket-constructor rebinding cannot substitute a different decision path for an already retained validation capability.

If a cached/loader-produced capability module cannot establish the genuine built-in binding and identity relationship, import fails closed rather than selecting a Python fallback.

## Preserved controls

R11 preserves the previously confirmed controls, including:

- R9 native-core source-origin/import-cache validation;
- R8 native POSIX broker transport and peer/request identity checks;
- requester PID/UID/process-start generation and fork separation;
- native object-generation identity and lifetime reservation;
- ordinary weak-reference/finalizer irrelevance;
- explicit close revocation and duplicate-close non-authorization;
- bounded lifecycle cleanup;
- exact five-field actor/world/subject/time/transition scope binding;
- exact registered source basis and unregistered-basis `DENY`;
- field-specific `NONCURRENT_SYNTHETIC` boundary and current/project-current-shaped rejection;
- authority/schema/fixture/proof/authority-instance/content-integrity law;
- construction/reconstruction/mapping/proxy/JSON/copy/deepcopy/serialization rejection;
- distinct authority instances for equal semantic inputs;
- cross-scope/cross-module separation;
- stable repeated/concurrent validation;
- surrogate-basis denial;
- no public source-basis registration surface;
- no project-current effect.

## Separation / no current effect

`SELF_REVIEW_PERFORMED = NO`

`INDEPENDENT_REVIEW_PERFORMED_BY_R11_REDESIGN_WORKER = NO`

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`CURRENT_ACTOR_OR_RUNTIME_MUTATION = NO`

`OBL055_EXECUTED = NO`

`ENCOUNTER_CREATED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`AUTHORITY_INDEX_EFFECT_CREATED = NO`

`OBL061_UNBLOCKED = NO`

## Required next gate

Run the governed producer court against this exact frozen R11 candidate. If producer-green, return to SUB-VOZHD E for exactly one fresh distinct independent review. Do not self-review and do not commission that reviewer from this worker.
