# OBL058 — CAUSAL_USE_PERMISSION — R10 FRESH DISTINCT INDEPENDENT REVIEW R1 — RETURN TO SUB-VOZHD E

## Terminal

`RABOCHII_SUBV_E_OBL058_CAUSAL_USE_PERMISSION_R10_INDEPENDENT_REVIEW__RETURN_TO_SUB_VOZHD_E`

State after terminal: `CLOSURE_ONLY`.

## Recommendation

`FAIL__OBL058_R10_INDEPENDENT_REVIEW__DISPATCH_MODULE_ATTRIBUTE_MEDIATION_CAN_SUBSTITUTE_PUBLIC_VALIDATOR`

Smallest exact blocker:

`BLOCKER__OBL058_R10_DISPATCH_VERIFIER_READS_MODULE_DICT_BUT_PUBLIC_VALIDATOR_BINDING_USES_CALLER_MUTABLE_MODULE_ATTRIBUTE_LOOKUP`

Frozen R10 candidate `0d23b02c75783033a4c8087b00721cb73a0924b4` is not yet lawful for SUB-VOZHD E adoption consideration. R10 does close the R9 mutable receipt-class validation lookup on the ordinary genuine path, but its new dispatch-module verifier and its later public-validator binding do not observe the same immutable surface.

No repair was performed by this reviewer.

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
- independent test-surface blob: `73b8285e3ce6aaafa0b484001266b1dbbc7ba277`
- governed wrapper blob: `bad85ecc23d1abc73ffcac4eee8c6b58fb528351`
- governed court-spec blob: `8d2088690d1da11b4f2598e6f36ab76f9060ed6a`
- governed evidence execution: `8f310099751e137249a9cb0c3836231c096cbdb5`
- governed evidence packet commit: `f36f3c689785fd514e24da51e848b355f9813f6f`
- governed evidence packet blob: `319417dd799009223b3dc22463b2f4069a4220c1`
- execution-only PR: `#333`, closed unmerged
- PR synthetic merge identity: `11543aeb1e72c412b67f843e3e8fec2eeef81cd5`
- final reviewer tip: reported out of band after this terminal commit because a file cannot contain its own immutable commit SHA without changing that SHA.

## Independent finding

R10's dispatch verifier checks the genuine extension module's underlying dictionary entries and confirms that the expected names point to built-in functions bound to that module. That closes an ordinary plain-Python lookalike.

The later binding step, however, retrieves `_dispatch.bind_contract` and `_dispatch.public_validate` through ordinary module attribute lookup. Python module objects allow their `__class__` to be changed to a `ModuleType` subclass with custom attribute handling. A genuine repository-built extension module can therefore keep the genuine built-in functions in its underlying dictionary while ordinary attribute lookup returns a different Python callable for `public_validate`.

The independent governed check loaded the genuine R10 dispatch extension from the exact expected compiled artifact path, changed only its ordinary Python module class before candidate import, and retained the genuine built-in functions unchanged in the module dictionary. R10's verification passed. Genuine contract binding also completed. The later `_dispatch.public_validate` lookup then returned an ordinary Python function.

A genuine receipt was issued using an unregistered synthetic basis whose native source decision is `DENY`. The substituted public validator returned `PERMIT`, and the native transport-success counter increased by zero during that validation. This establishes that the public decision was substituted after the verifier accepted the genuine module object.

Smallest required next property:

`REQUIRES__R10_DISPATCH_BINDING_TO_RETAIN_THE_VERIFIED_BUILTIN_FUNCTION_OBJECTS_FROM_THE_SAME_VERIFIED_MODULE_DICTIONARY_WITHOUT_LATER_CALLER_MUTABLE_MODULE_ATTRIBUTE_LOOKUP`

This reviewer does not prescribe an implementation. Any changed candidate is a new semantic target and must follow whatever bounded repair/review sequence SUB-VOZHD E lawfully commissions.

## Governed independent evidence

- workflow: `Rabochii Governed Bounded Court`
- run: `34292774781`
- job: `102282728359`
- workflow conclusion: `success`
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

The green workflow is a reproduction court for the blocker. The blocking check intentionally asserts the observed substituted public-validator behavior, so green execution confirms semantic FAIL rather than PASS.

## Preserved R10 controls

This FAIL is narrow. The independent court separately confirmed that the saved genuine R10 public validator is not redirected by `IssuedReceipt._source_validate` replacement, descriptors, or receipt `__getattribute__`; post-binding candidate/module aliases and import-cache replacement do not redirect the saved validator; plain Python dispatch-module lookalikes reject; genuine registered-basis `PERMIT` and unregistered-basis `DENY` advance native transport evidence; explicit close revokes validation and duplicate close does not restore authority; bounded issue/close cycles return lifetime accounting to baseline; forked positive/negative copies reject and child close does not retire parent authority; ordinary construction, `object.__new__` where reachable, subclass, mapping/proxy, JSON reconstruction, copy/deepcopy and serialization remain non-authoritative; equal semantic inputs retain distinct authority-instance identities; exact five-field cross-scope and registered-basis binding remains correct; project-current-shaped inputs reject; surrogate bases deny; repeated/concurrent genuine validation remains stable; and no public source-basis registration/current-effect surface appears.

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

No central, PRE-MAIN, main, campaign, sibling-lane, or frozen-candidate branch was moved by this reviewer.

## Return Beacon completion

The accompanying `.rabochii/return_manifest.json` is committed in the same final branch-tip commit as this return packet. It truthfully declares `FAIL`, `CLOSURE_ONLY`, durable required outputs, completed governed evidence, no required/background work remaining, and review/repair separation under `RABOCHII_RETURN_MANIFEST@1.0.0`.

Exact terminal:

`RABOCHII_SUBV_E_OBL058_CAUSAL_USE_PERMISSION_R10_INDEPENDENT_REVIEW__RETURN_TO_SUB_VOZHD_E`
