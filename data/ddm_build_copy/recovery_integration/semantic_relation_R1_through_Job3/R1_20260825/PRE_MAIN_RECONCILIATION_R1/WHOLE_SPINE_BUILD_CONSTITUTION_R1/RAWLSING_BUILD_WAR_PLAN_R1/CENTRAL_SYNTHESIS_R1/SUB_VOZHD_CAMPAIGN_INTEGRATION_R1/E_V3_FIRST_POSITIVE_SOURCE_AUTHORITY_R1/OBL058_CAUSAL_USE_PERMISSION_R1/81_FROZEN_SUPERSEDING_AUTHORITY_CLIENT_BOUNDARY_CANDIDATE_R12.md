# OBL058 — CAUSAL_USE_PERMISSION — SUPERSEDING FROZEN AUTHORITY-CLIENT BOUNDARY CANDIDATE R12

## Status

`FROZEN_REDESIGNED_CANDIDATE__PRODUCER_REEXECUTION_REQUIRED__NOT_PROJECT_CURRENT__NOT_SUB_VOZHD_E_ADOPTED__NOT_HQ_ADOPTED`

This commit supersedes initial frozen R12 candidate `3b6e1f4232ce4dcec503654596c6aaf38de52c1c` solely because the first governed producer court exposed one test-harness exception-type mismatch. The R12 authority-client implementation is unchanged.

## Exact predecessor / first producer execution

- failed frozen R11 target retained unchanged: `c11d7c15626f0d249a3b44b87d5cb46dcfe7feef`
- R11 independent-review return / R12 exact starting HEAD: `b921b140041d9b102bda9a12e14047c626083fca`
- exact R11 blocker: `BLOCKER__OBL058_R11_PUBLIC_VALIDATE_EXPORT_REMAINS_CALLER_MUTABLE_AFTER_CAPABILITY_ESTABLISHMENT`
- campaign authority: `cd96e61c073522383a1315148a5e58aa169d2a1a`
- campaign authority tree: `6e644d347db5c6c64f7b13ff06a750cf68a4c543`
- initial frozen R12 candidate: `3b6e1f4232ce4dcec503654596c6aaf38de52c1c`
- initial evidence execution: `cdb6c00f14ec3672625e6e34b355b3bd717727bb`
- initial governed run/job: `34318836674` / `102360777038`
- initial result: `38 passed, 2 failed` across duplicated collection of 20 distinct court methods
- exact harness mismatch: assignment to read-only `retained_capability_identity` correctly raised `AttributeError`; the producer test required `TypeError`
- implementation behavior implicated by the failing assertion: the identity property was non-writable as required
- all other collected checks passed

The initial candidate is superseded rather than silently changed.

## Corrected producer court

- implementation commit remains: `87452847e67876b1e3103483a45e1667b22d94fb`
- Python candidate blob remains: `307b28f6c6dac96c711732d40b8949c45f1a2db9`
- native authority-client source blob remains: `924f5bbcdffda0d0ce937d365e6bd1a24f73d119`
- original full producer court blob remains: `1517fdd93991a8dd6b2447e653d6c67a3fa124ea`
- corrected producer-court adapter blob: `83692004e5e6d48cf66318051a809879789dd52e`
- correction commit: `95bed48bf42b13931984e5400eef332b189b742c`

The corrected court changes only the expected Python exception class for attempted assignment to the native read-only identity property, from `TypeError` to the actually correct `AttributeError`. It does not weaken the requirement: assignment must still be rejected. No implementation, authority, receipt, scope, source-basis, transport, lifecycle, fork, reconstruction, concurrency, or no-current-effect behavior changed.

## R12 authority-client invariant

The exact source-origin-authenticated validation capability is retained by identity inside the exact native `AuthorityClient` that performs validation. The client's native call slot invokes that retained capability directly. Ordinary later Python module/class/instance/descriptor/alias/import/cache/reload lookup does not select the decision path for an already-issued retained client.

There is no candidate-module `validate_receipt` export. `AUTHORITY_CLIENT` is bootstrap/discovery of the already-issued handle; the ongoing authority-bearing interface is the exact retained client object itself.

## Separation / no current effect

`SELF_REVIEW_PERFORMED = NO`

`INDEPENDENT_REVIEW_PERFORMED_BY_R12_WORKER = NO`

`R11_REVIEW_REPEATED = NO`

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

Run the governed producer court against the exact new frozen candidate SHA containing this packet and the corrected producer-court surface. If producer-green, return to SUB-VOZHD E for exactly one fresh distinct independent review of that new frozen R12 candidate. This worker must not commission or perform that review.

The exact frozen commit SHA is reported out of band because a file cannot contain its own immutable commit SHA without changing that SHA.
