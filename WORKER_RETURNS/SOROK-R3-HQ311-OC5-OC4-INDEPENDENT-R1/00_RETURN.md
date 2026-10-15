# SOROK HQ311 OC5 — independent OC4 custody court: HOLD / REVISE
**Disposition:** `REVIEW_REVISE__EXCERPT_REDS__FULL_167_CASE_EXECUTION_HOLD__NO_ADOPTION`.
Independent source-free I2 analysis, NOT OC4 author, HQ, institutional custodian or semantic issuer.

## Exact identities
- Repository: private `maidiu/rawlsing`.
- Reviewer branch: `agent/reviewer-sorok-r3-hq311-oc5-oc4-independent-r1`.
- Directly verified commissioned startup: `57fff604dd88836cfa6d929b02b20d68f6557cda`, parent `95dc53cdc2d1adc7465d5e50915599dceddf9dde`.
- OC4 pinned return: `0caaec590f6a8bf6744f22dc9c948c5fe233bc94`.
- OC4 candidate module native Git blob (connector-verified metadata): `af2b7e943018077cb36808b5af1cd67704624bec`.
- Original OC1: `19438890e43153e2bc4a1ad271b5e19bcef33e1e`; OCR1: `aba637265bea2358790fea50d0e7abc98141e472`; OC2: `a61d5794271038fb20c94a75eaee401a66613ce9`; OC3: `9cd47a829473a6e92392582b4f01f2c564aa5dce`.
- Read the entire commission and Sorok 00_READ_ME_FIRST, 00B, 00C §§3A/3B/5A, 00D and HQ311 intake. Scope remains TEST_ONLY.

## Science outcome and exact evidence boundary
OC4's author reports **121 PASS / 10 FAIL** for the unchanged 131 inherited tests and **36/36 PASS** for OC4-authored controls. The original OC3 reporter provides a prior **115 PASS / 16 FAIL** at OC2. These are **source-derived claims, not independently reproduced OC5 pytest results**. Do NOT promote them to an OC5 verified matrix.

The current Browser environment has real Python 3.13.5, pytest 9.0.2, filesystem, subprocess and Git 2.47.3. GitHub connector read/write functions reach private pinned Git objects; Python shell network DNS does NOT reach github.com and the connector does NOT mount its return into the Python filesystem. The OC1/OCR1/OC2/OC3 source tests and complete OC4 candidate were not staged in a single Python import closure. No original 131, OC4 36, or proposed new OC5 candidate-hostile case was actually run against the native OC4 module. The archival xz bytes were fetched only as connector base64 previews, not mounted and byte-checked in Python. No report may call this 167-case reproduction or native module verification. This is an **execution/staging HOLD**, despite verified availability of the remote textual and binary objects.

**What did execute:** an independently written, isolated reproduction of the exact OC4 packet-leakage checking logic, manually transcribed from the pinned module's visible source (not imported from the native full blob), and frozen six local pytest expectations. `pytest -q test_projection_excerpt.py --junitxml=excerpt_junit.xml` returned exit 1: **2 PASS, 4 FAIL**. The four failures concern **duplicate keys whose spellings normalize to the same permitted field**: fullwidth `ｃontext`, `con\\u034ftext`, accented `CONTÉXT`, and `n\\u034fote`. The source checks a *set* of normalized public keys, which loses multiplicity, and the recursive validator allows both aliases. These are packet-schema ambiguity/extra-payload holes **predicted to reproduce** at the full OC4 `detect_leakage/assert_no_leakage` entrypoints; strictly mark `NATIVE_MODULE_NOT_EXECUTED` until actually confirmed. Positive single-context and existing U+034F sensitive-token controls passed in the isolated excerpt. Local retained SHA256: excerpt `c27cebda5da81bd195329fb682c14973babb50b49d7702fdd5a9e141b8ea1063`, tests `899552819f4c4f9a41b4e0cd42201ba1e4c16ce7c3ab1d97ad099754b08923a1`, stdout `156145797913158faac3d49fdbe2ed2a3914a7e4e4be5e7e9942b156ba90f60c`, JUnit `f4c8de3707553e8c5e3037fec28d2226131e59a43b68364dfa33ba448d7167fc`.
Additionally, source inspection identifies a likely **untyped malformed-primary-signature failure** in `require_second_signature`: dereferencing `primary_sig.signer_person_id` before type checking can raise `AttributeError` rather than `SignatureError`. This is a predicted typed-refusal failure, NOT executed at full-module entrypoint.

## Independent adjudication of all ten *reported* surviving historical failures
The **six old procedural / oracle conflicts** are:
1. OC1 `h13_rollback`: original test describes destructive valid-range rollback as legitimate, while stricter append-only implementation raises `LedgerRollbackError`; preserving history is the correct policy.
2. OC1 `h15_missing_capsule`: unmodified positive explicitly calls `require_second_signature(None,...)`; a capsule-free positive contradicts full-envelope commitment and should refuse.
3. OC1 `positive_ID_only`: signs only capsule ID as content, not the capsule content digest; refusal is correct.
4. OCR1 `A01_revoked_commit_early`: revocation refusal occurs at commit instead of the older unblind assertion.
5. OCR1 `A02_expired_commit_early`: expiry refusal occurs at commit.
6. OCR1 `A03_bad_purpose_commit_early`: unlawful purpose refusal occurs at commit.
The OC1 h13/h15 source was directly read at original Git ref; the other descriptions are corroborated by pinned OC3/OC4 reports. Full OCR1 test source was not independently executed here. Do not silently xfail or rewrite historical tests.

The **four newly red content-only signature assertions** are:
7. OCR1 `A08_mismatched_holder_unblind_test_setup`: its earlier content-only signing setup now fails before reaching its intended mismatched-holder check.
8. OC2 `signature_binds_content_positive`: directly read original test creates bare `content_digest` signatures and asserts authorized capsule success.
9. OC3 `B01_valid_content_signature_positive`: old positive signs content only.
10. OC3 `Z03_public_mock_credential_positive`: old fixture expectation signs content only.
A signature covering `content_digest` alone cannot prove identity, purpose, lawful-set, version, freeze time, split/coder commitments or other capsule fields. **Do not weaken the canonical commitment** to make these old assertions green. The correct future oracle can distinguish an expected strict refusal from a new full-envelope positive while preserving historical original sources and their literal failures.

## Scope, disposition and owner actions
No 167-case independent acceptance is possible from current executed record. **REVIEW_REVISE / HOLD**: (a) stage pinned full native module, OC1 31, OCR1 45, OC2 19, OC3 36, and OC4 36 in one actual runner; authenticate Git blob IDs, imports and archive bytes; run unchanged 131 and OC4 36, plus reviewer-authored tests; (b) independently confirm/falsify the two new packet-schema/type defects at actual entrypoints; (c) repair only under an appropriately separately commissioned implementer if confirmed; (d) competent owner updates *successor* positive oracles without erasing the ten old literal failures. No automatic trust issuance, protected holdout, external ledger, real grants, original survey source, model/provider permission, C07 cold-process API, V3 or production/canonical adoption. This return is an input to HQ only.

**Exact execution ceiling:** native source/test staging PARTIAL; current full inherited+new runner evidence NOT_EXECUTED. Attached OC5 test file is reviewer-authored but not falsely called executed. Python syntactic compile of a 45-case local OC5 draft passed (sha256 `913ea6daaa7b8dc0e20d8135020fab2b309c234db01affd77f56afdd57396804`); these cases are not graded PASS/RED against OC4. Local JUnit/stdout can be retained via host artifact; they are *excerpt* evidence only. Remote final SHA is recorded by the host after push and direct verification; it cannot be self-referential inside this committed file.
