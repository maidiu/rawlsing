# SOROK OC5ISS R4 — implementer grant or owner HOLD

**DISPOSITION:** \`IMPLEMENTER_NOT_AUTHORIZED__STOP_NO_ORIGINAL_OWNER_AUTHORITY\`. This document is a **negative grant receipt**, not a conditional permission that becomes effective automatically.

## 1. Why there is no implementer grant

The exact required original authority chain is incomplete:

1. **Person/institution or competent original source owner:** \`UNKNOWN\`. No verified identity/responsible organization, competence to define original OC4/OC5 custody semantics, or legitimately authorized delegate.
2. **Delegation and scope:** \`NOT_PRODUCED\`. No immutable original owner-delegation source pointer, Git blob/commit of signed scope or institution owner proof. Connecting to private GitHub or a user launching a reviewer prompt is not a source-policy grant.
3. **The six choices:** D1–D6 \`UNISSUED_NOT_YES_OR_NO\`; no owner-specified schema, normalization/confusable policy, exception classes, serializer, old capsules or effective versions.
4. **Independent review:** no separate original-source reviewer has reviewed or adopted *issued* policy. OC5E's prior independent engineering review of TEST_ONLY code is not a reviewer signature on unissued D1–D6.
5. **Actual first native consumer:** none. Sourcefree OC4/OC5 tests call \`EscrowState.commit/unblind\`, \`capsule_envelope_commitment\`, \`require_second_signature\`, \`detect_leakage\` and \`assert_no_leakage\`. No original real signer/institution, C12/BP4 protected writer→reader→later person consumer, cross-process C07 or native authority is evidenced.
6. **Protected integration:** QF2 \`a93db6bce4832270cf29727233dbfbc5f0312395\` explicitly returned \`STOP_QF2_ORIGINAL_OWNER_GRANTS_AND_RELEVANT_ACCEPTED_REVIEWS_ABSENT__NOT_MERGED\`; neither PR nor PRE-MAIN authority activated.

**Owner action:** incumbent Sorok/PRE-MAIN HQ must identify the original OC4/OC5 policy authority (or provably authorized delegate), require its original grant, and obtain **six independent YES/NO answers with a fully versioned scope**, not a self-report by an analyst. Only then commission a new implementer, keeping roles separated. If no such original issuer exists, competent governance must explicitly establish one through proper process; this review cannot invent or appoint it.

## 2. Conditional future scope — not operative without the grant

**Sources pinned for eventual sourcefree S2 worker:**

- \`WORKER_RETURNS/SOROK-R3-HQ310-OC4-CUSTODY-TEN-RED-REPAIR-R1/repro/custody_protocol.py\`, author commit \`0caaec590f6a8bf6744f22dc9c948c5fe233bc94\`, Git blob \`af2b7e943018077cb36808b5af1cd67704624bec\`.
- \`WORKER_RETURNS/SOROK-R3-HQ312-OC5E-EXECUTION-RECOVERY-R1/tests/test_oc5e_native_hostiles.py\`, reviewer commit \`67a4f1561cdad40192f00797d66b24fc4cd91589\`, test blob \`9837579ebb5b2fbf3a41c967e584a166786e46b9\`.
- OC5E frozen dependency closure \`freezes/01_STAGED_SOURCE_MANIFEST.json\` at the reviewer cut, not independently restaged by this Browser session.
- Source policy: **currently NONE**. Do not prefill with OC5OWNER's candidate D1–D6 yes propositions or treat mock signer as original custody issuer.

**Exact technical entrypoints and six original negative groups** (future only if issued):

| Decision | Source function(s) | Existing exact test node | Current failures | Conditional eventual engineering action |
|---|---|---|---:|---|
| D1/A6 | \`capsule_envelope_commitment\`, \`EscrowState.commit\` | \`test_capsule_identity_field_types_must_be_validated\` | 11 | validate owner-approved field types/serializer before hash/commit/ledger; preserve 18-field signature |
| D2/A1 | \`_normalized\`, \`detect_leakage\`, \`assert_no_leakage\` | \`test_normalization_equivalent_allowed_field_alias_must_be_refused\` | 10 | owner-approved alias multiplicity at every specified mapping, correct exception |
| D3/A2 | \`detect_leakage\` | \`test_confusable_leak_token_substitution_must_be_flagged\` | 6 | finite exact owner-issued codepoint/token table, benign boundary |
| D4/A3 | \`require_second_signature\` | \`test_malformed_signature_object_must_fail_typed\` | 18 | guard foreign objects before attribute access, preserve role separation/full envelope |
| D5/A4 | \`MockSigner\`/dual-signature \`require_second_signature\` | \`test_non_enum_role_string_must_fail_typed\` | 1 | owner-issued role coercion or rejection and typed error boundary |
| D6/A5 | \`EscrowState.unblind\`, \`authorize_holder\` | \`test_unblind_unhashable_holder_must_fail_typed\` | 3 | owner-issued holder namespace/error before map lookup and no state change |

**Prohibited ahead of issuance:** editing original OC4 protocol, OC5 author results, OC5E original tests, source-native data, any current owner/worker branch, original semantic/CAN/ADP/Pyat/SCI05 source, PRE-MAIN/main, PR514/516/519/521, protected CAS or publishing a NEW policy as though original. No fresh implementer started here. No implementation code or local S2 tests run.

## 3. Historical test bank and “green” fallacy

Sourcefree original JUnit at OC5E commit:

\`\`\`text
inherited_131.xml           131 cases: 121 PASS / 10 FAIL
oc4_new_36.xml               36 cases:  36 PASS /  0 FAIL
oc5e_native_hostiles.xml    159 cases: 110 PASS / 49 FAIL
oc5_prior_predictions.xml    23 cases:  16 PASS /  7 FAIL
TOTAL                        349 cases: 283 PASS / 66 FAIL
\`\`\`

All headers 0 errors/skips, direct Git readback. The ten old historical tests and seven OC5 prediction failures remain original immutable artifacts. **Frozen PASS tests documenting defects must remain byte-unchanged even if corrected implementation later makes them fail.** For example, old observed-hole tests expect \`AttributeError\` or \`TypeError\`; future *owner-issued* standard may require \`SignatureError\` or \`IdentityMismatchError\`. The conflict must be displayed as a **legitimate before/after oracle delta**, not engineered into a 159/159 or 349/349 pass. Post-policy acceptance tests are separately preregistered/frozen before implementation.

The exact original reviewer runner's staged-source command family (NOT_RUN here), after validating the pinned import closure:

\`\`\`sh
export PYTHONPATH="$PWD" PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
python3 -m pytest -q test_custody_hostiles.py test_positive_lifecycle.py test_ocr1_independent_hostile.py test_oc2_regressions.py test_oc3_independent_hostile.py --tb=line --import-mode=importlib -p no:cacheprovider --junitxml=inherited_131.xml
python3 -m pytest -q test_oc4_repair_controls.py --tb=line --import-mode=importlib -p no:cacheprovider --junitxml=oc4_new_36.xml
python3 -m pytest -q test_oc5e_native_hostiles.py --tb=line --import-mode=importlib -p no:cacheprovider --junitxml=oc5e_native_hostiles.xml
python3 -m pytest -q test_oc5_prior_predictions.py --tb=line --import-mode=importlib -p no:cacheprovider --junitxml=oc5_prior_predictions.xml
\`\`\`

These are commands for a **future authorized, qualified S2 worker**, *not* executions by OC5ISS. The original OC5OWNER decision source \`02_MINIMAL_REPAIR_CUT_AND_ORIGINAL_OWNER_APPROVAL.md\` already identifies the required source-guard fault injection and fresh post-policy tests. Preserve those plans as recommendations, not permission.

## 4. Required original owner grant format (not issued here)

A future competent original owner must supply a **separate** durable signed/versioned policy artifact, containing:

- Verified identity/capacity, delegating principal and original source authority; exact immutable grant SHA, source chain and competence.
- **Six distinct** D1–D6 YES/NO judgments, each with approved alternative if NO; precise accepted types, aliases, Unicode tables, exception precedence, mock/external-signer limits, legacy migration, cut-scoped effects.
- Applicable original source blob \`af2b7e94...\`, source universe and version; effective/admission date/time, revoked/expired behavior and future review.
- Actual first sourcefree consumer, source qualification and TEST_ONLY/non-native ceiling; explicitly separate real external custody and later Sorok C12/BP4 consumer, if any.
- Named **different** reviewer, original owner acknowledgment and immutable proof; HQ-approved integration/CAS route only after qualified reviewer return.

Until those fields are honestly present, **implementer-grant status stays DENIED_BY_MISSING_PRECONDITION**, not a final substantive NO on any of the six proposed policy changes.

## 5. Three courts / finite route

**ENGINEERING:** exact source/test map accepted scoped, execution \`NOT_RUN\`, source implementation blocked.
**SCIENTIFIC:** sourcefree test-only, independent real signer/person-world \`HOLD\`.
**AUTHORITY:** \`STOP_NO_ORIGINAL_OWNER_AUTHORITY\`, no implementer commission or PRE-MAIN CAS.

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| Six original policy choices unanswered | Technical source fixes can alter custody legal/semantic behavior | Original issuer supplies signed versioned six-decision policy | Competent original custody policy owner, via Sorok incumbent |
| All 49 new hostile cases source-confirmed | Test failure not equivalent to law issuance | Keep prior JUnit/test bytes and owner-approved acceptance split | OC4/OC5 original author, later independent reviewer |
| Native signer/consumer unproved | Mock test passes do not make a protected escrow | Exact real custody and C12/BP4 first consumer after source issuance | Custody/source and C12/BP4 original owners |
| QF2 STOP | No conditional merge right conferred | Keep no-merge/no-CAS; route owner evidence | PRE-MAIN incumbent |

**DONE:** refused original owner grant without identity/delegation; stated exact conditional patch boundaries and original test record. **REMAINING:** real owner decisions, separate implementer, pre-frozen post-policy tests, independent reviewer and product consumer. **BLOCKERS:** missing source issuer, six unanswered versions and compatibility contracts, QF2 STOP. **LARGEST MOVE:** owner-issued D1/A6 source and serialization first. **FLIGHT:** no new implementation launch or S2 worker interference. **DELTA:** explicit denial receipt without a fabricated policy signature.