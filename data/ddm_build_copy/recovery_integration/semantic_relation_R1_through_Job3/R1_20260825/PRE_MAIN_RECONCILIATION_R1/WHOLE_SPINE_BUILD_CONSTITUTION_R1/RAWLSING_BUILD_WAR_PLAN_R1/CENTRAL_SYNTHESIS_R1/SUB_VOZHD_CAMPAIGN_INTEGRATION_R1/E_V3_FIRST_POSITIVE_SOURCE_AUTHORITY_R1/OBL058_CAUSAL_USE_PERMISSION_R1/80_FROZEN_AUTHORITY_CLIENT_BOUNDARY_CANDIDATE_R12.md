# OBL058 — CAUSAL_USE_PERMISSION — FROZEN AUTHORITY-CLIENT BOUNDARY CANDIDATE R12

## Status

`FROZEN_REDESIGNED_CANDIDATE__NOT_PROJECT_CURRENT__NOT_SUB_VOZHD_E_ADOPTED__NOT_HQ_ADOPTED`

R12 is the bounded public-contract redesign commissioned after the single R11 independent review. It preserves the verified R9 native source core and the R11 exact authenticated validation capability, but moves the persistent validation contract onto a retained native authority-client object.

## Exact predecessor and commission

- failed frozen R11 target retained unchanged: `c11d7c15626f0d249a3b44b87d5cb46dcfe7feef`
- R11 independent-review return / exact R12 starting HEAD: `b921b140041d9b102bda9a12e14047c626083fca`
- exact R11 blocker: `BLOCKER__OBL058_R11_PUBLIC_VALIDATE_EXPORT_REMAINS_CALLER_MUTABLE_AFTER_CAPABILITY_ESTABLISHMENT`
- R12 campaign authority: `cd96e61c073522383a1315148a5e58aa169d2a1a`
- R12 campaign authority tree: `6e644d347db5c6c64f7b13ff06a750cf68a4c543`
- R12 implementation commit: `87452847e67876b1e3103483a45e1667b22d94fb`

R11 has already consumed exactly one independent review. This R12 worker does not review frozen R11 again.

## R12 mechanism

- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0`
- mechanism revision: `OBL058_CAUSAL_USE_PERMISSION_AUTHORITY_CLIENT_BOUNDARY_R12@1.0.0`
- Python bootstrap/receipt surface: `causal_use_permission_candidate_r12.py`
- Python surface blob: `307b28f6c6dac96c711732d40b8949c45f1a2db9`
- native authority-client source: `obl058_r12_authority_client.c`
- native source blob: `924f5bbcdffda0d0ce937d365e6bd1a24f73d119`
- producer court: `test_authority_client_boundary_r12.py`
- producer court blob: `1517fdd93991a8dd6b2447e653d6c67a3fa124ea`

## Governing authority-client invariant

The exact source-origin-authenticated validation capability lives inside the exact retained authority client that performs validation.

The verified R12 extension module yields exact genuine built-in `establish_authority_client` and `public_validate` objects. Establishment is invoked through the exact authenticated built-in object and receives the exact already-authenticated `public_validate` object. Native establishment independently verifies that identity against the extension module's own dictionary, binds the verified native receipt descriptors, and stores a strong reference to that exact `public_validate` object inside a native `AuthorityClient` instance.

The `AuthorityClient` is a non-subclassable, non-constructible, non-copyable, non-serializable native object with no instance dictionary. Its native `tp_call` slot invokes the retained capability object directly. No ordinary later Python module/class/instance/descriptor/alias/import/cache/reload lookup selects the decision path for that issued client.

The candidate module exports `AUTHORITY_CLIENT` only as bootstrap/discovery of the already-issued handle. There is deliberately no module-level `validate_receipt` export. Consumers retain the exact client and invoke that client directly; fresh module-name resolution is not part of the ongoing validation contract.

If the verified native client/capability bundle cannot be established, import fails closed. A Python substitute cannot become a genuine retained authority client because the native client type cannot be constructed or subclassed from Python and only native establishment creates instances carrying the authenticated capability.

## Preserved controls

R12 preserves the previously closed properties, including:

- genuine registered-basis `PERMIT` and unregistered-basis `DENY`;
- exact actor/world/subject/time/transition scope and exact source-basis binding;
- R9 native source-origin/import-cache controls;
- native POSIX broker transport independent of ordinary Python socket constructors;
- requester process generation, fork isolation and parent/child authority separation;
- explicit close, duplicate close, stale-receipt rejection and bounded lifecycle cleanup;
- reconstruction/subclass/mapping/proxy/JSON/copy/deepcopy/serialization rejection;
- distinct authority-instance identities for equal semantic inputs;
- `NONCURRENT_SYNTHETIC` and current/project-current-shaped exclusions;
- repeated/concurrent validation stability;
- source/broker loss failing closed;
- no public source-basis registration surface;
- no project-current effect.

## Separation / no current effect

`SELF_REVIEW_PERFORMED = NO`

`INDEPENDENT_REVIEW_PERFORMED_BY_R12_WORKER = NO`

`FROZEN_R11_CANDIDATE_MODIFIED = NO`

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

Run the governed producer court against this exact frozen R12 semantic candidate. If producer-green, return to SUB-VOZHD E for exactly one fresh distinct independent review of this new frozen R12 candidate. This worker must not commission or perform that review.
