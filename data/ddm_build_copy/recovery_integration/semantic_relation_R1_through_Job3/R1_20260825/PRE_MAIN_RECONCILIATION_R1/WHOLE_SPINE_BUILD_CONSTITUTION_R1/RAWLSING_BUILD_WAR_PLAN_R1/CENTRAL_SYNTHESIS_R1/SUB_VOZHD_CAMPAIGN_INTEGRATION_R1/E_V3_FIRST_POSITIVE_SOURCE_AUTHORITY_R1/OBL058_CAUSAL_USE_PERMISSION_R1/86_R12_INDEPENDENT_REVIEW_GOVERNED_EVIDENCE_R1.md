# OBL058 — CAUSAL_USE_PERMISSION — R12 FRESH DISTINCT INDEPENDENT REVIEW — GOVERNED EVIDENCE R1

## Evidence identity

- frozen semantic target: `fe0e3211ac2ae908e92fdc5a0351991747e6cbbb`
- mechanism: `OBL058_CAUSAL_USE_PERMISSION_AUTHORITY_CLIENT_BOUNDARY_R12@1.0.0`
- campaign authority consumed prospectively: `2a5f2bedbbfa53944dd8959b818b31b82a32dfa2`
- exact reviewer start: `73e88fcba21556d830fc81bab8761087d97e3bbf`
- independent matrix freeze commit: `dfeb39ca26f06aeb4803f3c3a99f213b0f411230`
- independent matrix blob: `a02f0d14d5b80faec720a002ac5f646d8361227a`
- independent test-surface commit: `dd9e9091b31dc17f9a21c2502ecc97f0c4e39b88`
- independent test-surface blob: `e217018f1739b7302e58f22df2ac23531f09213e`
- governed wrapper commit: `e3b719e1132d536627ae8389df8eac0d2994af77`
- governed wrapper blob: `a069aaabea80a4fef5f344492d156718dac2e154`
- governed court-spec bind / evidence execution: `a4569b18dd7b4aa342610da2e9db274ce4ad5e5f`
- governed court-spec blob: `0c9bb8d7670ac9c9161c9040b434ceb970bd98ee`

## Governed execution

- workflow: `Rabochii Governed Bounded Court`
- run: `34324458294`
- job: `102378398595`
- workflow conclusion: `success`
- runner: Ubuntu `24.04.4`
- Python / implementation: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.13s`
- court-spec validation: `PASS`
- independent review court: `28 passed in 15.21s`
- bounded-court receipt: `PASS`, exit code `0`
- receipt elapsed seconds: `15.41622`
- receipt semantic candidate: `fe0e3211ac2ae908e92fdc5a0351991747e6cbbb`
- receipt evidence execution: `a4569b18dd7b4aa342610da2e9db274ce4ad5e5f`
- receipt PR synthetic merge identity: `61391446d9ce2fa8c4e5fc906e0a8da4f056cd9b`
- receipt spec SHA-256: `5d864b84cb8b20c2831772ce63904b3c3dab1687403a51d3964af11fa98b4cb6`
- artifact ID: `10093177027`
- artifact ZIP SHA-256: `21e752e017e297e23418a8dcc68298158a78ad5667cd9c961a236e6f33c246f3`
- execution-only PR: `#342`
- PR state after evidence capture: `closed`, `merged = false`

## Semantic finding

Workflow success is evidence-execution status only. The independent semantic disposition is `FAIL`.

Smallest exact blocker:

`BLOCKER__OBL058_R12_CAPABILITY_BOOTSTRAP_TRUSTS_EXPECTED_CACHE_PATH_AND_BUILTIN_BINDING_WITHOUT_AUTHENTICATING_LOADED_NATIVE_BINARY_TO_FROZEN_SOURCE`

R12 does retain the exact built-in capability object it authenticates, and a saved genuine client survives ordinary post-issuance candidate-module rebinding, module-class mediation, capability-module rebinding/mediation, `sys.modules` replacement, aliases, later import-name resolution, receipt-class substitutions, Python socket-constructor replacement, lifecycle/fork/reconstruction controls, repeated/concurrent validation, and the other preserved families exercised by the independent matrix.

The independent review nevertheless reproduces a source-origin failure before establishment. R12 derives the expected capability-extension output path from the SHA-256 digest of `obl058_r12_authority_client.c`, but if that path already exists it does not rebuild or authenticate the loaded binary bytes against the frozen source. `_verify_and_capture_capability` then accepts the module based on exact expected path/origin plus the fact that `establish_authority_client` and `public_validate` are genuine CPython built-in functions bound to that module.

The independent court placed a different C extension at that exact digest-derived path inside a fresh isolated temporary root before importing R12. The substitute was not compiled from frozen R12 capability source. It nevertheless exposed genuine bound CPython built-ins at the required names and returned a callable client whose `retained_capability_identity` matched the accepted built-in `public_validate` object. R12 accepted that module and completed establishment.

Using the resulting accepted client, a genuine source-issued receipt with an unregistered basis—required to produce `DENY` under the frozen authority—returned `PERMIT`. The accepted substituted validation call produced zero increment in the genuine native transport-success counter. The court additionally confirmed that the accepted capability object was a genuine built-in, was bound to the accepted module, reported exact client/capability identity, and occupied the exact path R12 expected.

Therefore the retained-client mechanism is internally consistent with the capability object it accepts, but the establishment step does not prove that this capability is the one built from the frozen R12 native source. Path naming derived from source content is not source-origin authentication of pre-existing bytes at that path. Because the wrong native decision implementation can be accepted before client issuance and then becomes the exact retained capability, the intended authority-client boundary is not established.

## Preserved controls independently exercised

The green reproduction court separately confirms: genuine registered-basis `PERMIT` and genuine unregistered-basis `DENY` under the unmodified R12 implementation; exact authority/schema/mechanism identities; exact retained capability identity for the genuine client; positive and negative native transport traversal; post-creation candidate/capability export rebinding and module-class mediation not redirecting a saved client; `sys.modules`, aliases, reload/fresh import discovery not changing a saved client's decision; receipt method/descriptor/instance/subclass substitution remaining non-authoritative; direct client/receipt construction, mapping/proxy/JSON/copy/deepcopy/serialization remaining non-authoritative; exact five-field scope and registered-basis binding; surrogate/unregistered-basis denial; `NONCURRENT_SYNTHETIC` and project-current rejection boundaries; distinct authority-instance identity for equal semantic inputs; explicit close, duplicate close, stale-receipt and bounded lifecycle accounting; requester-generation/fork rejection with parent survival and child-close separation; Python socket-constructor replacement remaining outside native transport; source/broker loss failing closed; repeated/concurrent stability; ordinary Python R12 capability-cache and R9 native-cache substitutes failing closed; no public registration/current-effect surface; and live genuine positive/negative controls.

Those preserved controls do not cure the reproduced pre-establishment native binary source-origin gap.

## Separation / no-current-effect

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R12_CANDIDATE = 1`

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

`R11_INDEPENDENT_REVIEW_REPEATED = NO`

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

`EXECUTION_ONLY_PR_MERGED = NO`
