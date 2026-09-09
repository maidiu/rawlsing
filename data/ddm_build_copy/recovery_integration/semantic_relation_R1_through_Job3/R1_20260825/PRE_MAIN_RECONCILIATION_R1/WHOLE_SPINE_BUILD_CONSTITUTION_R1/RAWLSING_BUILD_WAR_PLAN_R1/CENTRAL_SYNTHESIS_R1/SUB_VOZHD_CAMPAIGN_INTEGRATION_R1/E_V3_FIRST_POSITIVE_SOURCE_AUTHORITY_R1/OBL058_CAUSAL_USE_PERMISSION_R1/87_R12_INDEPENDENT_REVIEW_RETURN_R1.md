# OBL058 — CAUSAL_USE_PERMISSION — R12 FRESH DISTINCT INDEPENDENT REVIEW — RETURN TO SUB-VOZHD E

## Terminal

`RABOCHII_SUBV_E_OBL058_CAUSAL_USE_PERMISSION_R12_INDEPENDENT_REVIEW__RETURN_TO_SUB_VOZHD_E`

State after terminal: `CLOSURE_ONLY`.

## Recommendation

`FAIL__OBL058_R12_INDEPENDENT_REVIEW__NATIVE_CAPABILITY_SOURCE_ORIGIN_NOT_AUTHENTICATED`

Smallest exact blocker:

`BLOCKER__OBL058_R12_CAPABILITY_BOOTSTRAP_TRUSTS_EXPECTED_CACHE_PATH_AND_BUILTIN_BINDING_WITHOUT_AUTHENTICATING_LOADED_NATIVE_BINARY_TO_FROZEN_SOURCE`

Frozen R12 candidate `fe0e3211ac2ae908e92fdc5a0351991747e6cbbb` is not lawful for SUB-VOZHD E adoption consideration.

R12 successfully fixes the R11 public-module lookup problem for an already-issued genuine client: the exact built-in capability object accepted at establishment is retained inside the native `AuthorityClient`, and ordinary later candidate/capability module rebinding, module-class mediation, `sys.modules` replacement, aliases, fresh import-name resolution, receipt-class substitution, and related Python lookup surfaces do not redirect that saved client.

The independent review finds a narrower establishment defect one layer earlier. R12 does not authenticate that a pre-existing native extension at its digest-derived capability-cache path was actually built from the frozen R12 capability source. A different C extension occupying that exact path can satisfy the built-in/binding/path checks, be accepted as the validation capability, and become the exact capability retained by the issued client.

No repair was performed by this reviewer.

## Exact identities

- repository: `maidiu/rawlsing`
- reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r12-independent-review-r1`
- exact review start: `73e88fcba21556d830fc81bab8761087d97e3bbf`
- immutable campaign authority: `2a5f2bedbbfa53944dd8959b818b31b82a32dfa2`
- campaign authority tree: `fad59518bb415bed933619261d5458db07559ab8`
- frozen R12 target reviewed unchanged: `fe0e3211ac2ae908e92fdc5a0351991747e6cbbb`
- mechanism revision: `OBL058_CAUSAL_USE_PERMISSION_AUTHORITY_CLIENT_BOUNDARY_R12@1.0.0`
- producer evidence supplied as context: `d95865abc7c86da8ba64c9106ed11b2c231e0b6c`
- producer run/job supplied as context: `34319175950` / `102361816213`
- independent matrix freeze commit: `dfeb39ca26f06aeb4803f3c3a99f213b0f411230`
- independent matrix blob: `a02f0d14d5b80faec720a002ac5f646d8361227a`
- independent test-surface commit: `dd9e9091b31dc17f9a21c2502ecc97f0c4e39b88`
- independent test-surface blob: `e217018f1739b7302e58f22df2ac23531f09213e`
- governed wrapper commit: `e3b719e1132d536627ae8389df8eac0d2994af77`
- governed wrapper blob: `a069aaabea80a4fef5f344492d156718dac2e154`
- governed court-spec bind / evidence execution: `a4569b18dd7b4aa342610da2e9db274ce4ad5e5f`
- governed court-spec blob: `0c9bb8d7670ac9c9161c9040b434ceb970bd98ee`
- governed evidence packet commit: `c8d5c8573073039f311ba15e1538ef721d44a26f`
- governed evidence packet blob: `cdaea07f0813256912169a8db1050b4000927be5`
- execution-only PR: `#342`, closed unmerged
- PR synthetic merge identity: `61391446d9ce2fa8c4e5fc906e0a8da4f056cd9b`
- final reviewer tip: reported out of band after this terminal commit because a file cannot contain its own immutable commit SHA without changing that SHA

## Independent finding

The genuine R12 implementation behaves correctly under its ordinary runtime path. The independent court confirms genuine registered-basis `PERMIT`, genuine unregistered-basis `DENY`, exact authority/schema/mechanism identities, exact retained capability identity, positive and negative native transport traversal, and non-redirection of a saved client after ordinary Python export/class/cache/name changes.

The blocker is source-origin authentication of the R12 capability extension before client establishment.

R12 computes the expected output filename from the SHA-256 digest of `obl058_r12_authority_client.c`. If that output path already exists, R12 skips compilation. Its verification then checks the module name, file/origin path, exact module dictionary, and that `establish_authority_client` plus `public_validate` are genuine CPython built-in functions bound to that exact loaded module.

The independent court created a fresh temporary root, placed a different C extension at that exact expected output path before importing R12, and gave that extension genuine bound CPython built-ins with the required names. Its establishment function returned a callable client whose `retained_capability_identity` exactly matched its own accepted `public_validate` object. The candidate accepted the module and issued that client.

A genuine source-issued receipt carrying an unregistered basis—therefore required to evaluate `DENY`—then returned `PERMIT` through the accepted client. The genuine native transport-success counter did not increment during that call. The accepted capability still passed R12's path, built-in, binding, and retained-identity checks.

Thus R12 can retain the exact capability it authenticated while authenticating the wrong native implementation. The authority-client retention boundary is correct only conditional on capability authenticity; the capability-bootstrap source-origin boundary is not sufficient to establish that authenticity.

Required next property:

`REQUIRES__R12_CAPABILITY_ESTABLISHMENT_TO_AUTHENTICATE_THE_LOADED_NATIVE_BINARY_TO_THE_FROZEN_CAPABILITY_SOURCE_BEFORE_ISSUING_THE_RETAINED_CLIENT`

This reviewer does not prescribe a repair architecture. Any changed candidate is a new semantic target and must follow whatever bounded repair/redesign and fresh-review sequence SUB-VOZHD E lawfully commissions.

## Governed independent evidence

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

The green workflow is a reproduction court for the blocker. The independent source-origin test intentionally asserts the observed acceptance of the different native capability and its `PERMIT` result for a genuine unregistered-basis receipt. Green execution therefore confirms semantic `FAIL`; it does not imply semantic PASS.

## Preserved R12 controls

This FAIL is narrow. The independent court separately confirms the ordinary genuine `PERMIT`/`DENY` path; exact retained capability identity; post-issuance candidate/capability module rebinding and module-class mediation not redirecting the saved client; `sys.modules`, aliases, fresh imports and reload resolution not changing the saved client's result; receipt method/descriptor/instance/subclass substitution remaining non-authoritative; R9 ordinary Python import-cache controls remaining closed; Python socket-constructor replacement remaining outside native transport; broker loss failing closed; explicit close revocation, duplicate-close non-restoration, stale rejection and bounded lifecycle accounting; requester process-generation/fork rejection with parent survival and child-close separation; direct construction/reconstruction/mapping/proxy/JSON/copy/deepcopy/serialization remaining non-authoritative; distinct authority-instance identities for equal semantic inputs; exact five-field scope and registered-basis binding; surrogate/unregistered basis denial; `NONCURRENT_SYNTHETIC` and project-current boundary preservation; repeated/concurrent stability; no caller peer/decision metadata authority; no public source-basis registration surface; and live positive/negative controls.

## Review count / separation

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R12_CANDIDATE = 1`

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

`R11_INDEPENDENT_REVIEW_REPEATED = NO`

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

No central, PRE-MAIN, main, campaign, sibling-lane, producer, frozen-candidate, R11, or unrelated authority branch was moved by this reviewer.

## Required next gate

Return this FAIL to SUB-VOZHD E. Do not commission a second review of frozen R12 candidate `fe0e3211ac2ae908e92fdc5a0351991747e6cbbb`.

Any successor must be a newly commissioned bounded repair or redesign addressing source-origin authentication of the R12 capability binary before retained-client issuance, followed by whatever fresh-review sequence SUB-VOZHD E lawfully commissions for the new frozen candidate.

## Return Beacon completion

The accompanying `.rabochii/return_manifest.json` is committed in the same final branch-tip commit as this return packet and declares the completed `FAIL` outcome, `CLOSURE_ONLY`, durable required outputs, completed governed evidence, no required/background work remaining, and review/repair separation under `RABOCHII_RETURN_MANIFEST@1.0.0`.

Exact terminal:

`RABOCHII_SUBV_E_OBL058_CAUSAL_USE_PERMISSION_R12_INDEPENDENT_REVIEW__RETURN_TO_SUB_VOZHD_E`
