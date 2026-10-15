# SOROK HQ308 OC2 — Source-free custody prototype repair

**Disposition:** `IMPLEMENTED_SOURCEFREE__89_PASS_6_RED_ON_95__INDEPENDENT_I2_REVIEW_REQUIRED__NO_ADOPTION`.

**Custody:** sealed startup `d300a0c0a409bf33922e60364670025458bf53f1`; OC1 source `19438890e43153e2bc4a1ad271b5e19bcef33e1e`; independent OCR1 source `aba637265bea2358790fea50d0e7abc98141e472`. Only own worker-return paths changed. One Browser/GitHub editor with actual Python 3.13.5 / pytest 9.0.2 / git 2.47.3, no second agent or model/harness switch.

## Executed courts

| Pinned court | OC1 baseline | OC2 now |
|---|---:|---:|
| 31 unchanged OC1 original tests | 31 PASS / 0 RED | **28 PASS / 3 RED** |
| 45 unchanged OCR1 hostiles | 15 PASS / 30 RED | **42 PASS / 3 RED** |
| New 19 OC2 real-entrypoint regressions | Not applicable | **19 PASS / 0 RED** |
| **Combined all 95 (actual pytest)** | — | **89 PASS / 6 FAIL / 0 SKIP, exit 1** |

All 31 original source tests are preserved byte-identically to their pinned inputs: `test_custody_hostiles.py` original Git blob `94ad944997cb9d1a8d6527e91c17416120c5108d`, `test_positive_lifecycle.py` `4b665a2a9d6999071624d580f2d2ae193daf59f4`. All 45 OCR1 test source cases unchanged, Git blob `ef997cab7205df53256b66a5695deeb9c082394f`. Executed JUnit/stdout and executable new regression code are retained in `OC2_EXECUTED_EVIDENCE_COMPACT.tar.xz`; actual statuses, not substituted tests.

## Six retained REDs — do not conceal

**Three contradictory original tests:** `test_h13_ledger_rollback_detected` asserts a rollback succeeds with ledger integrity true, contrary to append-only escrow; repaired API raises `LedgerRollbackError`. `test_h15_missing_signature_in_capsule_refused` expects two signatures to validate without any actual capsule; repaired API refuses. `test_positive_full_role_separated_lifecycle` signs only `{capsule: capsule_id}` rather than the real `capsule.content_digest`; repaired API correctly rejects the nonbinding signature. No editing of the historic authored tests or fake compatibility exceptions.

**Three OCR1 earlier-admission failures:** `A01_revoked_unblind`, `A02_expired_unblind`, `A03_illegal_purpose_unblind` construct an invalid capsule then commit it outside their expected-raise context. The repaired `commit` rejects these invalid capsules immediately, before the test reaches its expected `unblind` assertion. New direct API regression tests demonstrate all three denials at commit. Their historic pytest outcomes remain **RED**, not counted PASS.

## Repaired sourcefree mechanisms

- `EscrowState` validates purpose, revocation, expiry, holder existence/fixture role, release and exposure transitions. Fixture roster `runner1`, `custodian-alice`, `holder` is **not a trusted role issuer**; independently granted fixture-only holders explicitly typed.
- `commit` deep-copies and seals capsule fields; ledger records locally held event preimages and verifies monotonic sequence, operation order and materialized state consistency; `rollback_ledger` refuses mutation. This is not independently anchored, durable or externally tamperproof append-only storage. An adversary with arbitrary Python object access may rewrite all local seals.
- `MockSigner.verify` verifies self-described digest/context/nonce/root; dual-signature gate requires distinct nonconflicting fixture persons, recognized mock fixture roles and equality with real capsule content digest. Credentials publicly derived; **not trusted human signatures or organizational custody**.
- Blind pairing enforces exactly one A/B/C per nonce, unique trial IDs, consistent optional family/case joins and nonempty blocks.
- Test-only packet projection checks use narrow recursive schema, Unicode normalization and bounded lexical denial without false positive for benign `charming`. This does **not** prove semantic noninterference or hide model-inferable truths.

## Evidence, limits, owner action

The real execution bundle includes JUnit and stdout for original and OCR1 baseline, post-repair courts, 19 new regression tests, and combined 95 tests; plus the new executable regression source, environment passport, exact commands/exits. `01_EXECUTION_MATRIX.json` carries counts and the six exact reds; JUnit contains every executed case and traceback. No xfail, no skip, no original-test modification, no tests manufacturing expected exceptions.

OCR1 `C07` persisted cross-process state recovery remains **NOT_REACHED** (no persistence API). Separate **HOLD** on trusted institutional signer registry, real independent sealed custody, external ledger anchor, actual provider/model-use/privacy/spending grants, semantic ownership, population inference and all V3 use. This implementation does **not** accept itself. HQ must resolve six historic test-contract conflicts and commission a distinct independent I2 review.

Required final branch commit SHA is verified through direct remote readback after push and cannot be embedded recursively in this document.
