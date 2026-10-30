# SOROK R4 OC5ISS — original custody owner ruling or typed STOP

**TERMINAL:** \`STOP_NO_ORIGINAL_OWNER_AUTHORITY__NO_D1_D6_POLICY_ISSUED__NO_IMPLEMENTER_GRANT__NO_ADOPTION\`

**Date:** 2026-10-30. **Repository:** private \`maidiu/rawlsing\`. **Scope:** owner-source identity/delegation gate and bounded sourcefree custody D1–D6 evidence; documentary source review by a **separate analyst**, NOT the competent original OC4/OC5 custody policy issuer, original author, OC5E reviewer, semantic issuer, PRE-MAIN merger or own reviewer. **Branch:** \`research/sorok-r4-oc5-d1-d6-original-owner-source-grant-20261030\` created only for STOP documents, rooted at verified OC5OWNER \`b83f474fa04402dd270fd195ed9e49601b3301d1\`. This branch name and repository write access confer **no original policy authority**.

## Gate A — attempted original-owner/delegation verification

**FINDING:** OC5OWNER at \`b83f474fa04402dd270fd195ed9e49601b3301d1\` explicitly returns \`READY_DOC_OWNER_COURT__ISSUANCE_HELD\`. Its \`WORKER_RETURNS/OC5OWNER-R3/02_MINIMAL_REPAIR_CUT_AND_ORIGINAL_OWNER_APPROVAL.md\` blob **\`1f6635a36c8e170f5f9d55058f042cb3845b7148\`** says **“OWNER_DECISION_REQUIRED — NO POLICY ISSUED”**; each D1–D6 still has \`ORIGINAL_OWNER_NAME [UNKNOWN]\`, \`COMPETENCE_AND_OWNER_GRANT_SHA [NONE_FOUND]\`, \`YES [ ] NO [ ]\`. Its source-policy matrix blob **\`c2acb87470411b5b3ae5510853cfc90f92c856f0\`** reports \`actual_original_A1_A6_grant_found:false\`, with a bounded—not exhaustive—search. Its \`00_OWNER_DECISION_RESEARCH.md\` blob **\`30bc3aab592b1c286b72737a3be7035e83b15d01\`** does not issue rules or identify the competent source owner. \`SESSION_LOCATOR.json\` blob **\`584b2fdb23a3d474038916a4a9c2eeae0606a421\`** identifies a prior independent analyst, not the original issuer.

OC5 author \`e8b127b68c18d05c4d40c059b3aecc00dafc7ce7\` \`00_RETURN.md\` blob **\`a941dd6fe9e926a32896babf360d82b24625508f\`** preserved 49 new REDs and explicitly **refused** an unissued 49-behavior rewrite. OC5E original independent reviewer \`67a4f1561cdad40192f00797d66b24fc4cd91589\` report blob **\`9897d7bbbfaf8f6b0e05ab9d93c3eb9eff3b01ed\`** records TEST_ONLY reviewer execution and expressly no author repair or native signer grant. QF2 \`a93db6bce4832270cf29727233dbfbc5f0312395\` \`00_CONDITIONAL_OWNER_GATE_RESULT.md\` blob **\`d78c4a478eaffb1e57e074aabe1779cf49391339\`** independently stops integration: \`STOP_QF2_ORIGINAL_OWNER_GRANTS_AND_RELEVANT_ACCEPTED_REVIEWS_ABSENT__NOT_MERGED\`. QF2 does not grant OC5ISS policy authority.

**AUTHORITY result:** \`ORIGINAL_OWNER_IDENTITY=NOT_ESTABLISHED\`; \`DELEGATION_DOCUMENT=NOT_FOUND_IN_BOUNDED_SOURCES\`; \`SOURCE_SCOPE_GRANT=NOT_ESTABLISHED\`; \`IMMUTABLE_POLICY_GRANT_SHA=null\`; \`ISSUER_SIGNED_D1_D6_DECISION=null\`; \`REVIEWER_APPROVAL=NOT_ASSIGNED\`; \`PREMAIN_PROTECTED_CAS=HELD\`. No assumption that the GitHub connection, OC4/OC5 code author, OC5E reviewer, OC5OWNER document author, QF2 analyst or the operator is automatically the original issuer.

**INTERPRETATION:** A developer or analyst can recommend a sound defensive API but cannot issue a binding original custody rule by test consensus or a branch commit. **ACTION:** publish this **STOP packet**, not an ersatz owner approval. **OWNER:** incumbent Sorok HQ must name and evidence the competent original OC4/OC5 custody/projection/signature policy issuer or lawful delegate, with exact source version and grant. Only that issuer can supply six versioned YES/NO decisions; distinct original-source reviewer later evaluates the returned decision. No automatic original-owner policy adoption.

## Gate B — exact six questions, explicitly unanswered

| Decision | Original defect/test count | Candidate YES requiring **owner** ruling | Pending original-owner issue |
|---|---:|---|---|
| **D1/A6** identity-field validation | 11 | Reject invalid capsule field types **before** \`capsule_envelope_commitment\`/EscrowState.commit changes; preserve all 18 committed fields | Exact 7 named field types/ranges, strict canonical serializer/version, digests, timestamp units, old-source migration, typed exception |
| **D2/A1** duplicate normalized aliases | 10 | Reject multiple raw spellings of same allowed normalized key, without breaking generated packets | Canonical-only/single-alias policy, Unicode normalization version, nested scope, error precedence |
| **D3/A2** confusable tokens | 6 | Refuse owner-approved finite Cyrillic/Greek/Armenian token map | Exact six codepoints/token forms, mixed-script case, benign multilingual false-positive boundary, migration |
| **D4/A3** signature objects | 18 | Check true \`MockSignature\` types at \`require_second_signature\`, raise \`SignatureError\` for foreign objects | Alternative external structural signer interface, exception precedence vs \`ConflictError\`, legacy/mock compatibility |
| **D5/A4** signature role | 1 | Reject a non-\`Role\` enum, including string \`CUSTODIAN\`, with \`SignatureError\` at dual gate | Direct MockSigner constructor error, optional string migration, order of role-conflict checks |
| **D6/A5** unblind holder | 3 | Deny list/dict/set or non-string/empty holder with \`IdentityMismatchError\`, pre-lookup/no mutation | Source namespace, existing capsule/ledger error precedence, legacy scalar holders, authorized positive |

**These are six candidate YES propositions, not six YES rulings, six NO rulings, or a default implementation permission.** All six \`authority_ruling\` values remain \`UNISSUED_NOT_A_NO\`; neither YES nor NO is asserted on behalf of the original owner. See \`01_D1_D6_VERSIONED_DECISIONS.json\` for fields required from the competent issuer.

## Gate C — original immutable source/test scope

Original OC4 implementation \`WORKER_RETURNS/SOROK-R3-HQ310-OC4-CUSTODY-TEN-RED-REPAIR-R1/repro/custody_protocol.py\` at \`0caaec590f6a8bf6744f22dc9c948c5fe233bc94\`, blob **\`af2b7e943018077cb36808b5af1cd67704624bec\`** directly retrieved by blob, original reported SHA256 \`447e5bb738fc49c946a39ca438126e9c2a69d93025600f053662e56f846f9e3a\`. OC5E reviewer source test \`tests/test_oc5e_native_hostiles.py\` \`9837579ebb5b2fbf3a41c967e584a166786e46b9\`, original reported SHA256 \`a9faf7ace27d0f3f3cfd1102de5c6c8d6888c12f16c7bbdde8b32bb232b84512\`.

Original four JUnit files at OC5E commit were fetched directly with the following blob IDs and headers:

| Original court | JUnit Git blob | Cases | PASS | FAIL |
|---|---|---:|---:|---:|
| inherited OC1/OCR1/OC2/OC3 | \`51a09d112d5768f97f1b1b2cfe053d7af28357b2\` | 131 | 121 | 10 |
| OC4 new positive controls | \`d402d58a0e49fa5ff7afb2d98560876767d136a0\` | 36 | 36 | 0 |
| OC5E new hostiles | \`33efbc315cc424c377441b0f1f79ee31a5a185bc\` | 159 | 110 | 49 |
| OC5 earlier predictions | \`36294268fe94d7e5c83155d58c0959922f1cc22b\` | 23 | 16 | 7 |
| **Original total** | four separate original receipts | **349** | **283** | **66** |

All four headers show **0 errors and 0 skipped**. The original 10 historical REDs are not 10 newly discovered implementation holes; some are old fixture-policy collisions or earlier typed refusals. The prior seven are distinct original OC5 predictions. **No tests were run by OC5ISS**: historical results are attached original reviewer evidence only.

**Critical anti-greenwashing:** The immutable 159 contains observational tests that assert the *holes currently exist*, e.g. \`test_alias_holes_are_observed_not_theorised\`, \`test_malformed_signature_holes_are_observed_as_attributeerror\`, \`test_unblind_unhashable_holder_hole_is_observed_as_typeerror\`. An authorized future repair is expected to make some such before-state PASS tests fail. Do **not** edit, xfail, skip or promise 159/159 or 349/349 green; freeze a **new, explicitly post-policy** normative bank and report old observations and new accepted semantics separately.

## Three courts and stop conditions

**ENGINEERING:** \`SOURCE_TEST_CUSTODY_READBACK_SCOPED\`; 49 failures in six classes recorded; \`NEW_CODE_NOT_AUTHORIZED\`, \`PYTEST_NOT_RUN\`.

**SCIENCE:** \`TEST_ONLY_MOCK_CUSTODY__NATIVE_PERSON_WORLD_AND_REAL_INSTITUTION_HOLD\`; no independent real signer, protected holdout, C07 cross-process or native C12/person consumer established.

**AUTHORITY:** \`STOP_NO_ORIGINAL_OWNER_AUTHORITY\`; no D1–D6 issuance, version, effective date, delegation, reviewer or implementer launch; no PRE-MAIN or protected CAS mutation.

**DONE:** examined original OC5OWNER/OC5/OC5E/QF2 primary cuts, six propositions, original source code and four JUnit headers; returned typed STOP and six-row original-owner required-decision packet. **REMAINING:** locate/authorize actual competent custody policy owner; collect six YES/NO plus versioned source/exception/legacy/effective scope; fresh implementer and separate independent review; real receiving consumer. **CRITICAL BLOCKERS:** missing original issuer identity/immutable grant; unknown policy version; OC5E 49 REDs; no real custody signer or later consumer; QF2 STOP. **LARGEST PRODUCTIVE MOVE:** incumbent identifies owner/delegation and gets D1/A6 identity/serialization issuance first, followed by D2/A1 and D3/A2, then D4–D6 exception contracts. **FLIGHT:** single ChatGPT/GitHub documentary return on isolated research branch, no original worker disturbed, live Mac leases UNKNOWN. **DELTA:** no new science/policy; unequivocal owner STOP plus exact owner-ready decision questions and preserved historical negatives.

**Do not mistake a published STOP return for an owner approval or a grant to patch.** Later original owner-source reviewer and incumbent HQ own their separate judgments.