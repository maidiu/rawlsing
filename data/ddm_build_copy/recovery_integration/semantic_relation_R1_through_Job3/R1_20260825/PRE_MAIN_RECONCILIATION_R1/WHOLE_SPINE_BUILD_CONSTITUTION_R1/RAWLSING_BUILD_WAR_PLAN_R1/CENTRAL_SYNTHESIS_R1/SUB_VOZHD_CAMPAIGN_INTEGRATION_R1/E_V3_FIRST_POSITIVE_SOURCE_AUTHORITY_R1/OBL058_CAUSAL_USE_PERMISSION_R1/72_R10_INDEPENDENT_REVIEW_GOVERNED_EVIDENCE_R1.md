# OBL058 — CAUSAL_USE_PERMISSION — R10 FRESH DISTINCT INDEPENDENT REVIEW — GOVERNED EVIDENCE R1

## Semantic disposition

`FAIL__OBL058_R10_INDEPENDENT_REVIEW__DISPATCH_MODULE_ATTRIBUTE_MEDIATION_CAN_SUBSTITUTE_PUBLIC_VALIDATOR`

Smallest exact blocker:

`BLOCKER__OBL058_R10_DISPATCH_VERIFIER_READS_MODULE_DICT_BUT_PUBLIC_VALIDATOR_BINDING_USES_CALLER_MUTABLE_MODULE_ATTRIBUTE_LOOKUP`

The governed review court reproduces one exact ordinary-Python boundary mismatch. R10 verifies the genuine dispatch extension's underlying `module.__dict__` entries, but after verification the candidate obtains `_dispatch.bind_contract` and `_dispatch.public_validate` through ordinary module attribute lookup. A genuine dispatch extension module can retain the real bound C functions in its underlying dictionary while a normal `ModuleType` subclass mediates ordinary attribute access. The verifier therefore sees the genuine C functions while the later `public_validate` lookup can return an ordinary Python substitute.

In the independent reproduction, a genuine repository-built R10 dispatch extension was loaded from the expected compiled artifact path. Only its ordinary Python module class was changed before candidate import. The actual module dictionary remained unchanged and contained the genuine built-in functions. Candidate import passed source/binding verification and genuine contract binding completed, but the later ordinary `_dispatch.public_validate` lookup returned a Python function. An unregistered-basis receipt whose native source law is `DENY` then produced public `PERMIT` with zero additional native transport evidence.

No frozen candidate file was modified and no repair was performed.

## Exact identities

- repository: `maidiu/rawlsing`
- reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r10-independent-review-r1`
- exact review start: `19059045b1e9b7d1a4dd6cef7734e3bfd766611a`
- immutable campaign authority: `bd2184a56745e71aa10d7c1ca148ab564e044f4e`
- campaign authority tree: `7ddb5f110e2579f9272b77199dd5acae86194e8b`
- frozen R10 target reviewed unchanged: `0d23b02c75783033a4c8087b00721cb73a0924b4`
- producer evidence supplied as context: `466e0daa58588a30f33b21e484dd48824c400273`
- producer run/job supplied as context: `34289798372` / `102273571721`
- independent matrix freeze commit: `6818a0f28d9d6f0c2fccb237935ae8195141f829`
- independent matrix blob: `23715571f1ff4ef7f90587b7786cdf168581060f`
- independent test surface blob: `73b8285e3ce6aaafa0b484001266b1dbbc7ba277`
- governed wrapper blob: `bad85ecc23d1abc73ffcac4eee8c6b58fb528351`
- governed court-spec blob: `8d2088690d1da11b4f2598e6f36ab76f9060ed6a`
- governed evidence execution: `8f310099751e137249a9cb0c3836231c096cbdb5`
- execution-only PR: `#333`, closed unmerged
- PR synthetic merge identity: `11543aeb1e72c412b67f843e3e8fec2eeef81cd5`

## Governed court

- workflow: `Rabochii Governed Bounded Court`
- run: `34292774781`
- job: `102282728359`
- conclusion: `success`
- runner: Ubuntu `24.04.4`
- Python / implementation: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.05s`
- court-spec validation: `PASS`
- independent review court: `36 passed, 38 subtests passed in 4.77s`
- bounded-court receipt: `PASS`, exit code `0`
- receipt semantic candidate: `0d23b02c75783033a4c8087b00721cb73a0924b4`
- receipt evidence execution: `8f310099751e137249a9cb0c3836231c096cbdb5`
- artifact ID: `10081973082`
- artifact ZIP SHA-256: `195a6fb895a8a211a188fe23515697f35d55999b24b4b880165b2dcfddc12ff0`

The workflow is green because the blocking check intentionally asserts the reproduced state. Green execution therefore confirms the semantic FAIL rather than implying PASS.

## Preserved controls observed independently

The same governed review separately confirmed that, on the ordinary genuine binding path, the saved native validator is not redirected by `IssuedReceipt._source_validate` replacement, descriptors, or receipt `__getattribute__`; post-binding candidate/module aliases and import-cache replacement do not redirect the saved validator; plain Python dispatch-module lookalikes are rejected; genuine `PERMIT` and unregistered-basis `DENY` advance native transport evidence; explicit close revokes validation and duplicate close does not restore authority; bounded issue/close cycles return lifetime accounting to baseline; forked positive/negative copies reject and child close does not retire parent authority; ordinary construction/reconstruction/subclass/mapping/proxy/JSON/copy/deepcopy/serialization forms remain non-authoritative; equal semantic inputs retain distinct authority-instance identities; exact five-field cross-scope and registered-basis binding remains correct; project-current-shaped inputs reject; surrogate bases deny; repeated/concurrent genuine validation remains stable; and no public source-basis registration/current-effect surface appears.

## Review count / separation

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R10_CANDIDATE = 1`

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

`EXECUTION_ONLY_PR_MERGED = NO`

## No-current-effect attestation

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
