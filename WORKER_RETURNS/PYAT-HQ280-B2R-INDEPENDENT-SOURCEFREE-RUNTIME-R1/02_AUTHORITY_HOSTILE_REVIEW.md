# HQ280 B2-R independent authority review

## 1. Fixture contract versus adopted producer authority

Pinned test lines 30–34 construct `PRODUCER_CONTRACT`, `OWNER`, `PERMISSION_CEILING` and `SNAPSHOT` through G1 fixture helpers. `_m2_b5_view` lines 65–122 registers an `IMMUTABLE_LEARNED_PRODUCT`, builds actual M2 closures/releases and manually supplies a B5 lifecycle subject. M2 `register_producer_subject` (lines 549–585) validates exact structural records; `constitute_release` (lines 660–727) enforces the declared producer and required closure members. Neither generic registration nor successful closure mechanics is an independently accepted C1-issued production contract.

The fixture authority says `hq280-b2-test-only-nonissuer`; the permission tag says `hq280-b2-not-a-grant`. These preimages remain test material. M2's missing exact dependency test passed by refusing `DEPENDENCY_CLOSURE_INCOMPLETE`. This establishes closure enforcement at the fixture's declared grain, not release adoption or service permission.

## 2. Genuine owner-originated technical chain

`OwnerOnlySelectedIngress.serve` (production lines 626–677) validates a data-only request, invokes C1 from owner-held source/authority, requires native supported C1 states, checks retained stratum grain and performs deep expected-identity authentication before source applicability, G2 and F8. `_authenticate` (lines 747–827) checks the closed typed identity set and compares full C1 evidence/provenance. `_build_receipt` binds SA's `replay_identity()` (line 921), canonical replay order separately (line 957), exact source, C1 risk/denominator and F8 result; `authorizing` is false (line 972).

A separate synthetic observation wrapped actual production owner calls without changing source. Both q1 and q2 reached C1, SA, G2, F8 in that order; internal bound-F8 validation invoked G2 again. G2 replay hashes matched the actual captured SA receipts, and F8 hashes matched direct C1. Exact runtime references and original traces are retained in the execution JSON. This is an owner-internal technical authentication chain, not a deployed independent trust root. The owner-held nested source objects remain a named shared-object residual; this court does not establish global immutability or security.

## 3. Exact counts, lifecycle and historical addressability

The four-respondent synthetic XOR source yields q1 denominator 2 with numerators {0:1, 1:1}, and q2 denominator 1 with numerators {0:0, 1:1}. The source C11 release is identical while producer-query, composition, M2-release, selection and origin identities differ. Runtime references, selection receipts and full q1/q2 join material are recorded in `01_ACTUAL_EXECUTION.json`.

B5 exact selected-current q1, supersession to q2, historical q1 event resolution and restoration of the earlier checkpoint all passed. A superseded historical event cannot be relabeled CURRENT, and a claimed unselected C1 cell is refused. Invalidation of q2's producer query affects q2, preserves the unaffected q1 sibling and changes the live selection to NO_CURRENT. q2 remains addressable at its historical event. Checkpoint restoration in this commissioned test is in-process, not independent fresh-process persistence qualification.

The forged provenance case actually substituted C1 evidence provenance and was refused at G1 authentication, with zero F8 evaluator calls. Expected refusals passed as positive technical test results. No earlier failure or accepted-owner defect was observed.

## 4. Test-local join does not create an operative service

`_join` (test lines 186–237) resolves B5 current/as-of receipts, maps the exact selected M2 release back to fixture material, calls the real ingress and composes its own technical result dictionary. It explicitly labels the grade `SOURCE_FREE_DEVELOPMENT_ONLY__NONAUTHORIZING__G0B_NOT_ISSUED`, preserves `authorizing=False`, and produces a separate technical join hash. This dictionary is authored by test code. It does not supply an adopted selected T1/world-service producer, release authority or G0b-use receipt.

## 5. I4 is correctly M1-only

`adapt_m2_release_to_b5` (production lines 936–955) first calls `_validate_contract_for_b5` (lines 663–700). That validator requires `TYPED_DISPOSITION`, then exact `M1_DISPOSITION_PRODUCER_CONTRACT_REF`. The pinned C1 fixture subject triggered the expected typed-disposition refusal. The separate probe kept `TYPED_DISPOSITION` but supplied the test C1 producer contract; it refused with `producer contract does not exactly identify the current M1 disposition owner`. No production patch is warranted. Direct C1 support is not silently substituted for the current public M1 contract.

## 6. Custody and disposition

Exact startup `9b30f37a8c50a1bd043fc8834f7a9caee137587c` directly descends from custody-corrected candidate `a159bff63b779b994d7b1e83f8a2d6a303b81ea2`. All pinned production, fixture and integration-test preimages matched that parent. `.rabochii/return_manifest.json` remained blob `f1f123b1494c38f5d031378bfbdd0d031f697a36`; its task is HQ118, and it was neither overwritten nor used to claim B2 completion. Only three authorized return files are added; no test-only repair occurred.

Return the observed eight-test PASS to HQ for adjudication. EE14 G0b remains HELD and operative use REFUSED; N9 OC05 and N10W remain UNPROVED. No source microdata, production mutation, structural/temporal/actor permissions, model-use grants, V3 or self-adoption. The successful source-free runtime result must not be promoted into those states.
