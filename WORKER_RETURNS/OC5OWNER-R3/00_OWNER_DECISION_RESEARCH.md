# OC5OWNER-R3 — original custody policy decision research

**Disposition: READY_DOC_OWNER_COURT__ISSUANCE_HELD.** This is an independent I3 source-policy analysis, not an OC4/OC5 source-policy issuance, code patch, native trial, or self-review.

## Exact custody and source readback

- Private repo: maidiu/rawlsing. Assigned branch: research/sorok-r3-oc5-original-source-owner-policy-decision-20261030.
- Sealed startup: 187fdd11963163dab03c7b061e20067ea1f99134. Current commission branch pre-return HEAD: 35b9c3cf1f774145d9387c21fe485b2a0f04e318, five commits ahead and zero behind the seal. The full commission was read on the later assigned branch (blob d91f5fb6b33a069d649836b2fc113c8af3da91e7), not falsely attributed to the earlier startup, where it returns 404.
- OC5 author: e8b127b68c18d05c4d40c059b3aecc00dafc7ce7. OC4 original source commit: 0caaec590f6a8bf6744f22dc9c948c5fe233bc94. Independent OC5E reviewer: 67a4f1561cdad40192f00797d66b24fc4cd91589. Independent F3I: 97dbe712e4cce8fedd1632d9ac64b4e57a0ac25e.
- Exact OC4 implementation: WORKER_RETURNS/SOROK-R3-HQ310-OC4-CUSTODY-TEN-RED-REPAIR-R1/repro/custody_protocol.py, Git blob af2b7e943018077cb36808b5af1cd67704624bec, original reported SHA256 447e5bb738fc49c946a39ca438126e9c2a69d93025600f053662e56f846f9e3a.
- Exact OC5E hostile test: WORKER_RETURNS/SOROK-R3-HQ312-OC5E-EXECUTION-RECOVERY-R1/tests/test_oc5e_native_hostiles.py, Git blob 9837579ebb5b2fbf3a41c967e584a166786e46b9, original reported SHA256 a9faf7ace27d0f3f3cfd1102de5c6c8d6888c12f16c7bbdde8b32bb232b84512.
- This session read immutable GitHub source, original returns and historical JUnit reports. Original SHA256s are attributed to the original runners; no Python, pytest, original survey, native source or provider run was performed by OC5OWNER. Device BROWSER; exact session UI title, actual High effort and both Mac leases are unverified.

## FINDING — original 349-case record

| Prior execution court | Cases | PASS | RED |
|---|---:|---:|---:|
| Inherited OC1/OCR1/OC2/OC3 | 131 | 121 | 10 |
| OC4 author controls | 36 | 36 | 0 |
| OC5E independent hostiles | 159 | 110 | 49 |
| OC5 prior predictions | 23 | 16 | 7 |
| **Total** | **349** | **283** | **66** |

All original courts recorded 0 errors and 0 skips. Their original JUnit SHA256 receipts: inherited 659ed7f298fc4d78dd12df5678de08e7d62f624460d9b876da0c96f55f2c7588; OC4 1cee683d8b3ccbccf18821645540479d1c54c0c62d64a019cfd7e22b3cf87c99; OC5E ac727e498e573136c02f1a61ef76c8965212a7b74564d3fb1c444b136624a2e9; prior predictions 9f6b9d879be4ce875005b3ecfc3909c9e916f403190cce4518bdec90abcd6724. These are original execution evidence, **NOT_RUN** here.

| Family | New REDs | Exact mechanism | Grade |
|---|---:|---|---|
| A6 | 11 | CustodyCapsule version/freeze/schema/digest fields accept arbitrary Python types; canonical snapshot uses JSON default=str, so invalid capsule identity is committed and hashed | Highest-risk acceptance bypass |
| A1 | 10 | Normalized allowed-field aliases coexist; set(map(_normalized, ...)) discards multiplicity | Projection acceptance bypass |
| A2 | 6 | Cyrillic/Greek/Armenian confusables evade normalization-only leak tokens | Conditional lexical bypass pending owner threat model |
| A3 | 18 | Foreign signature objects at either position raise AttributeError before typed SignatureError | Fail-closed, untyped |
| A4 | 1 | Plain-string signature role dereferenced as Role.value causes AttributeError | Fail-closed, untyped |
| A5 | 3 | Unhashable unblind holder passed to dict lookup causes TypeError instead of IdentityMismatchError | Fail-closed, untyped |

Thus 27 acceptance-bypass cases (A6/A1/A2) and 22 already-fail-closed exception-typing cases (A3–A5). These are six root problems, not 49 separate policy issuances. The ten inherited historical REDs comprise six procedural/early-refusal contract collisions and four content-only mock-signature positives superseded by stronger full-capsule signing. All ten remain literally RED; the seven older prediction REDs also stay intact and must not be double-counted into the new 49.

**Post-patch oracle trap:** the currently passing OC5E tests also include descriptive observations that the holes exist (e.g. test_alias_holes_are_observed_not_theorised, test_malformed_signature_holes_are_observed_as_attributeerror, and three TypeError holder observations). A correct patch will turn some of those PASS snapshots RED. Preserve all frozen test bytes and report baseline witnesses separately from a newly owner-issued post-policy normative suite. Do not promise 159/159 or 349/349 green.

## INTERPRETATION — where authority actually stops

- OC1 sourcefree custody return 19438890e43153e2bc4a1ad271b5e19bcef33e1e proposed semantic owner/custodian separation, but expressly had no real institutional signer, independent protected holdout or real oracle approval.
- OC2 a61d5794271038fb20c94a75eaee401a66613ce9 and OC3 independent reviewer 9cd47a829473a6e92392582b4f01f2c564aa5dce retained six historical REDs; cross-process C07 was NOT_REACHED because no persistence API exists in this sourcefree module.
- OC4 commission blob c5d1b1e1a12cda58f484b365fed8fe614cad7053 authorized ten OC3 sourcefree fixes and explicitly denied semantic/oracle issuance by the author. It called for full capsule identity and Unicode U+034F checks, but did not issue A1 alias multiplicity, A2 confusable scripts, A6 type/range/migration, or A3–A5 exception contracts. OC4 returned four content-only compatibility REDs for future competent owner judgment.
- OC5 declined an unissued 49-behavior rewrite; OC5E conducted TEST_ONLY native review, not policy issuance or adoption; F3I corroborated source and JUnit without rerunning pytest. QF1 68e49f92d5b9f0859d08847ee108684ddfd193ca held original owner-code review, PR519/CAS, native/person and host/model gates.
- No applicable original signed A1–A6 owner decision was found in the bounded cited sources, control rules, registry or current Sorok progress. This is not an exhaustive claim about every archived branch, unmounted Library document or Mac session. Repo write permission and mock-signature hashes are not scientific or policy ownership.

**Missing real function:** a qualified original custody/projection/signature policy owner must take the exact OC4 capsule and tests, decide lawful Python types and canonical serialization, Unicode aliases/confusable tokens, typed signature/holder denial and backward compatibility, then emit one versioned signed owner-policy contract consumed by a separate implementer. Present first actual consumer is only the sourcefree OC4/OC5 pytest court exercising commit/unblind/release/signature/leakage. No actual production Sorok C12/BP4/actor consumer was demonstrated; future material adoption requires an authorized writer→reader→same-person consumer edge and negative severance proof, plus separate native source/science grants.

## ACTION — accountable owner

1. Incumbent Sorok HQ identifies and verifies the competent original custody/source-policy issuer (not the OC4/OC5 author, OC5E reviewer, OC5OWNER analyst, or GitHub login by default), and collects the six YES/NO propositions in 02_MINIMAL_REPAIR_CUT_AND_ORIGINAL_OWNER_APPROVAL.md with exact policy grant/version evidence.
2. Only after original owner choice does HQ authorize a new isolated implementer at exact source/test blob refs, preserving original negatives and testing sourcefree positive and fault controls. One distinct reviewer later assesses exact returned SHA; no self-review or automatic PRE-MAIN adoption.
3. Protected owners retain CAN/ADP/Pyat/SCI05/C8/C9/C12, source use, actual holdout/signing, PR and canonical CAS. QF2 cannot launch from this document.

**ENGINEERING:** documentary source and historic native-test record verified as attributed; new execution NOT_RUN; patch HELD. **SCIENTIFIC:** TEST_ONLY fixture, no original B/world/actor/practice, real oracle or human signer. **AUTHORITY:** OWNER_DECISION_REQUIRED; no grant, merge or canonical CAS.

**DONE:** source/test custody, six-family mechanism map, original records, owner propositions and handoff. **REMAINING:** owner issuance, bounded patch, new post-policy tests, independent review and real receiving edge. **CRITICAL BLOCKERS:** absent owner policy and QF2 gates, A6/A1/A2 bypasses, original Mac session locator unavailable. **LARGEST MOVE:** resolve A6 types/canonical commitment, then A1/A2 acceptance rules. **FLIGHT:** Browser/GitHub only, no Mac/process/PR/PRE-MAIN/user source mutation. **DELTA:** finite owner decision court instead of speculative implementation. Exact final commit cannot self-reference and will be reported after remote readback.
