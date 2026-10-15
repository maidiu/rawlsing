# SOROK HQ309 OC3 — Independent OC2 test-only custody review

**Verdict: `REVIEW_REVISE`.** This is an independent I2 source-free Python court, NOT HQ adoption, independent institutional custody, trusted signer/role issuance, protected holdout, model grant, population inference, or V3 operation.

## Identity and executable provenance

- Reviewer branch `agent/reviewer-sorok-r3-hq309-oc3-custody-independent-r1`, sealed startup `324d63070a47dea920c4fbca433d0177c16ce9cf`. Remote comparison before work: exactly identical, ahead 0/behind 0.
- OC2 pinned author commit `a61d5794271038fb20c94a75eaee401a66613ce9`, verified candidate Git-native blob `f117f380c524db5b1eae0ce280be23f1c4bf2c23`. OC1 pinned `19438890e43153e2bc4a1ad271b5e19bcef33e1e`; OCR1 pinned `aba637265bea2358790fea50d0e7abc98141e472`. The 31+45+19 inherited test sources and modules were verified against their original exact native Git blob IDs. Independent new isolated Python staging; `custody_protocol.__file__` / `dummy_corpus.__file__` both resolved into staged source. Verified Python 3.13.5, pytest 9.0.2, git 2.47.3, actual subprocess and filesystem; direct Git CLI private-host DNS unavailable; authenticated GitHub connector works.
- Reviewer read source and OCR1 known findings before independently freezing expectations *prior to new hostile execution*. Not blind, not externally preregistered. No model/provider calls or protected survey sources.

## Independent real execution

| Court | PASS | FAIL | Total |
|---|---:|---:|---:|
| Unchanged original OC1 | 28 | 3 | 31 |
| Unchanged independent OCR1 | 42 | 3 | 45 |
| Unchanged OC2 regression source | 19 | 0 | 19 |
| **Inherited** | **89** | **6** | **95** |
| **New OC3 actual-API hostiles** | **26** | **10** | **36** |
| **Combined** | **115** | **16** | **131** |

All 131 executed; 0 skips, 0 xfails, pytest exit 1. The pushed `OC3_REMOTE_CORE_EVIDENCE.tar.xz` contains exact JUnit XML for the 131-case combined and 36-case new courts, new 36-case test source, frozen pre-execution expectations, SHA receipts and reproducer. A separate full local evidence bundle includes the three original 95/36/131 stdout and JUnit files, the 131-case JSON matrix and six pinned source files, available as a direct user download; it is NOT asserted to be present in the pushed compact archive. **No posthoc 95/95 green.**

## Six historical REDs: correct refusal at the wrong old assertion

Three unmodified OC1 tests have **unsafe/obsolete expected procedure**:
1. `test_h13_ledger_rollback_detected` calls valid-range destructive rollback and asserts integrity true; OC2 correctly raises `LedgerRollbackError`, leaving ledger intact (OC3 C02).
2. `test_h15_missing_signature_in_capsule_refused` calls `require_second_signature(None,...)` expecting success; OC2 rejects missing capsule with `SignatureError`.
3. `test_positive_full_role_separated_lifecycle` signs a digest over the capsule **ID alone**, not its `content_digest`; OC2 correctly raises `SignatureError`. Actual content-bound positive verified in OC3 B01.

Three unmodified OCR1 `A01/A02/A03` tests construct already revoked, expired or `LIVE_MODEL_REQUEST` purpose capsules, calling `EscrowState.commit()` outside the expected exception context; OC2 now refuses these at **commit**, before unblind, with respectively `RevocationError`, `RevocationError`, `PurposeViolationError`. OC3 A05 confirmed refusal at commit with zero ledger/state writes; A06 committed lawful capsules *first*, then made them revoked/expired/illegal-purpose and confirmed unblind refusal and no ledger progression. These are not admitted bypasses, but the original six remain FAILs in literal pytest.

## Ten NEW independently observed failures — prohibit scoped acceptance

**B02–B04 (material: signature/capsule authority identity).** Existing signatures are accepted on a second capsule with different `capsule_id` but same `content_digest` (B02), after changing purpose to another allowed purpose (B03), and after changing `lawful_set_digest` (B04). OC2's signer binds only content bytes, not capsule ID, purpose or frozen envelope. No human signer is implicated: credentials are openly derived **TEST_ONLY** fixtures.

**C05–C06 (material: false in-process integrity).** After lawful COMMIT→UNBLIND→RELEASE, direct modification of `unblinded[ID]['unblinded_at']` or `unblinded[ID]['capsule_id']` leaves `verify_ledger_integrity()` returning `True`. The checker omits both materialized fields. Basic op tamper and released-state divergence controls still PASS. Neither local in-memory seals nor Git evidence constitute an external immutable journal or persistence proof.

**D04–D05 (lower severity: trial input validation).** All-three-arm blocks with whitespace-only nonce are accepted; a list-valued arm crashes via raw `TypeError` instead of typed `BlindIDPairingError`. The second is a fail-stop/type-hygiene defect, NOT an unauthorized-pairing acceptance. Exact A/B/C and duplicate-ID controls PASS.

**E05–E07 (strict projection/schema leakage).** `assert_no_leakage` accepts integer-valued menu options, list-valued `public_projection.context`, and the otherwise allowed note text `answ\u034fer_key` (U+034F combining grapheme joiner bypasses the candidate's Cf/Cc-only normalization). These show incomplete strict type/schema enforcement and a lexical Unicode alias bypass, not proof that protected real keys or semantic content were released to a model. Safe generated packets and harmless “charming” control PASS.

The new court also includes **three PASS ceiling demonstrations**, not grant evidence: any local fixture caller can self-authorize a holder using `authorize_holder`, unsigned fixture capsules can reach release, and publicly generated signer strings produce valid mock signatures. These guarantee the review is not misread as institutional custody certification. Real signer registry, competent holder issuance and full signed-event gating are missing by design.

## Review disposition and repair frontier

**`REVIEW_REVISE__TEN_EXECUTED_NEW_SOURCEFREE_REDS__SIX_HISTORICAL_CONFLICTS_PRESERVED__NO_ISSUANCE`.** In particular B02–B04, C05–C06, E05–E06 require test-only implementation repair before scoped scientific acceptance; D04–D05 and E07 belong in the same bounded repair. Do not edit, skip or xfail any inherited OC1 31, OCR1 45 or OC2 19. Preserve test-only mock disclaimers, no external calls or grants. Future OC4 reviewer must independently execute all 131 plus its own falsifiers, not self-adopt.

C07 persisted/cold-process custody remains `NOT_REACHED` (no API); no external durable monotonic proof, semantic signer/role issuer, real holdout, population inference, provider/model-use/privacy/spend grant or V3 authorization. Remote independently reproducible core evidence and reproducer are in `OC3_REMOTE_CORE_EVIDENCE.tar.xz`; the separately downloadable full local archive also contains the baseline and all raw logs and the complete matrix. Return cannot contain its own future commit SHA; exact remote verification is performed after push.
