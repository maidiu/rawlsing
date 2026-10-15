# SOROK HQ307 OCR1 — independent source-free OC1 custody hostile court

**Terminal disposition: `REVIEW_REVISE__30_INDEPENDENT_EXECUTED_HOSTILE_REDS__ORIGINAL_31_UNCHANGED_GREEN__REAL_ISSUANCE_HOLD`.** No semantic adoption, issuance, production deployment, model call, or human/institutional custody certification.

## 1. Identity, independence, and actual execution

- **Repository:** `maidiu/rawlsing` (private).
- **Role:** one independent I2 Browser/GitHub reviewer, not HQ, OC1 author, semantic issuer, or signer.
- **Reviewer branch:** `agent/reviewer-sorok-r3-hq307-ocr1-custody-hostile-r1`.
- **Directly verified original commission HEAD:** `07130e9a96944dc852a7ddf38c11cc38cf14f75c`; HQ307 parent `9ca0469b6ace374e52db308bb794b16e65f2a578`.
- **Exact OC1 candidate:** `19438890e43153e2bc4a1ad271b5e19bcef33e1e`; author original commission `3b0680c3b342137d334d55f6051b762715a63dd9`.
- **Four unchanged source blobs, verified as Git native SHA-1 (`blob <length>\\0<bytes>`):** `custody_protocol.py` `487a6e5bc40a1d366a375d4916eb759bb997eb2a`; `dummy_corpus.py` `770efe72190e35d1bc34065b5a55c183bf1320f5`; `test_custody_hostiles.py` `94ad944997cb9d1a8d6527e91c17416120c5108d`; `test_positive_lifecycle.py` `4b665a2a9d6999071624d580f2d2ae193daf59f4`.
- **Provenance:** sourcefree exact authorized source files staged in a fresh, isolated Python directory rather than modifying OC1 author's branch. `custody_protocol.__file__` and `dummy_corpus.__file__` resolved into that staged source directory (relative `source/`). Python 3.13.5 / pytest 9.0.2 / git 2.47.3 observed with real pytest and local filesystem. Earlier owner's Python 3.11.3 is *not* this reviewer runtime.
- **Independence limitation:** reviewer read HQ307's earlier source inspection before creating new expectations. `01_PREOBSERVATION_EXPECTATIONS.json` was frozen before running newly authored hostile tests, but is **not blind** to HQ's already exposed defects. It does not claim prior execution preregistration for the OC1 author's one-commit `frozen_negative_expectations.json`.

### Executed suite ledger

| Actual command (`cd source`) | Tests | PASS | RED | Exit |
|---|---:|---:|---:|---:|
| `python -m pytest -q test_custody_hostiles.py test_positive_lifecycle.py --junitxml=../review/original_31_junit.xml` | 31 | 31 | 0 | 0 |
| `python -m pytest -q test_ocr1_independent_hostile.py --junitxml=../review/independent_hostile_junit.xml` | 45 | 15 | 30 | 1 |
| **Actual combined evidence** | **76** | **46** | **30** | partial RED |

Unchanged original tests and source identities were verified **before** the independent tests. Full exact stdout, JUnit (each case and traceback), reviewer test source, first frozen expected matrix, source blob and SHA256 matrix, and reproduction instructions are preserved in `OCR1_EXECUTED_EVIDENCE.tar.xz`. No xfail, skip, test rewriting, test-generated refusal, or candidate repair. `C07` cross-process state restoration is separately **NOT_REACHED** because `EscrowState` exposes no serialization/persistence/reload implementation; it is *not* an executed PASS or RED.

## 2. Decisive real entrypoint counterexamples

**A — escrow, revocation, holder, release (10 RED / 2 PASS):** `EscrowState.unblind` admitted **already revoked, expired, and disallowed-purpose** committed capsules, arbitrary/forbidden-role/unrelated holders, even after an unrelated mock signing ceremony. `EscrowState.release` admitted a subsequently revoked/expired capsule. `record_exposure` admitted an uncommitted capsule and purpose `LIVE_MODEL_REQUEST`. Positive `release` without prior `unblind` and duplicate `release` were correctly refused. RoleAssignment/Person are data classes, not validated by escrow APIs; there is no authorization registry or holder grant. These are **actual sourcefree admission/refusal gaps**, not cryptographic or human-identity conclusions.

**B — mock signature and capsule binding (4 RED / 4 PASS):** `require_second_signature(None, sig1, sig2, digest, ...)` returned `True` for two otherwise valid mock signatures. Changing `capsule.content_digest` to an unrelated value also returned `True`. Changing a signature object's declared `content_digest` while retaining the hash also returned `True` because `MockSigner.verify` reconstructs from caller content/context/nonce without comparing all self-describing signature fields. An arbitrary person can claim a mock role using a publicly derived fixture credential. Context/nonce mismatch, same signer and explicitly conflicting roles were correctly refused. **Real-person, trusted-key and role authority remain unissued; mock impersonation is especially a TEST_ONLY credential ceiling.** The original positive lifecycle signs a digest of `{capsule: capsule_id}`, not the capsule's `content_digest`, making the claimed signature-to-capsule semantics especially weak.

**C — append-only ledger (5 RED / 1 PASS; 1 NOT_REACHED):** `rollback_ledger(1)` erased UNBLIND+RELEASE after a three-event lifecycle while leaving `released` true; `verify_ledger_integrity()` returned true. Deleting the final event and adjusting `_ledger_seq`, changing an op, duplicating a COMMIT event, or clearing history while retaining state also returned true. Untampered COMMIT→UNBLIND→RELEASE passed. Existing `verify_ledger_integrity` checks sequence ordinality *only*, not append-only history, state congruence, hash-linking, or externally anchored monotonicity. No persistence or cross-process recovery API was reached.

**D — pairing and blind joins (6 RED / 2 PASS):** real `verify_blind_pairing` accepted four rows A,A,B,C under one nonce, unknown XYZ as the three arms, duplicate trial IDs, inconsistent per-block case and family joins, and zero trials. It correctly rejects missing one of three arms and accepts the normal ABC sequence. Set-cardinality is insufficient for the claimed exactly-one-per-arm block even at sourcefree grade. Family/case join validations need an issued schema; current API does not supply one.

**E — leakage (4 RED / 2 PASS):** `assert_no_leakage` admitted zero-width-character variants of `answer_key` and `expected_answer`, and a nested `solution/truth` field carrying a lawful answer; `detect_leakage` falsely flagged benign `charming` solely because it contains `arm`. Literal `hidden_origin` was correctly rejected, and the generator's known model-visible packet was correctly accepted. Lexical denylisting cannot prove semantic noninterference. Nested semantic tests demonstrate the lack of schema validation but are not empirical proof a model can infer secret answers. Future real packet safety needs a strict approved output schema plus protected-source review.

**F — freeze and family (1 RED / 4 PASS):** after `commit`, a caller can replace `escrow.committed[id]` with a capsule carrying a different content digest, and ledger integrity still passes. Duplicate commit for the same ID is correctly refused; exact duplicate family fingerprints are detected. Distinct wording does *not* prove independent family provenance; the positive paraphrase test records this epistemic limit, not a demonstrated semantic clone-detection achievement. The published `frozen_before_execution:true` flag is self-asserted in the author's single returned commit, not independent preregistration proof.

### Test-validity distinction

The original `test_h05_stale_or_revoked_capsule_refused` unconditionally raises `RevocationError` inside the test when its own flag says revoked; it does not force `EscrowState.unblind` to reject. Original `test_h03` compares two digests and never asks escrow to verify source content. Original `test_h13` expressly calls ledger erasure a *legitimate rollback* and accepts `verify_ledger_integrity() == True`. The original suite's **31 PASS is real execution**, but neither that fact nor the author's descriptions establish those three claimed boundaries.

## 3. Claims and authority court

| Claim | Evidence grade | Disposition |
|---|---|---|
| OC1 Python original authored suite executable | 31/31 independently reproduced with exact hashes | `PASS_TEST_ONLY_EXECUTION` |
| Existing denial for missing prior unblind, duplicate release, conflicting signatures, illegal purpose in builder | Actual sourcefree API checks | `PASS_BOUNDED` |
| Revocation/expiry/current role and holder enforcement | Direct unauthorized operations accepted | `RED_IMPLEMENTATION` |
| Two signatures bound to actual capsule | `None` and alien capsule accepted | `RED_IMPLEMENTATION` |
| Immutable, rollback-detecting append-only escrow | Local truncation/tamper passes sequence-only checker | `RED_IMPLEMENTATION` |
| Exact 1:1:1 blinded-pair multiplicity | A,A,B,C accepted | `RED_IMPLEMENTATION` |
| Leak-proof packet/coder firewall | Lexical bypass and false positive | `RED_CLAIM__NEEDS_SCHEMA` |
| Genuine independent signer/role registry, holdout custodian, cryptographic anchor | No such trusted system exists here | `HOLD_REAL_AUTHORITY_NOT_ISSUED` |
| Cross-process ledger persistence/durability | No persistence API | `NOT_REACHED` |
| Family population independence, actual behavioral effects, model-use grant | No real sources, provider, or sampling permission | `HOLD` |

### Verdict

**`REVIEW_REVISE`** for OC1's claimed working synthetic custody enforcement. Preserve 31 original PASS and limited positive helpers, but **do not accept fail-closed revocation, role permissions, actual capsule-signature binding, append-only custody, exact pairing, or leakage noninterference**. These are real defects or overclaims inside the prototype's sourcefree contract. Real external independence, cryptographic trust, protected sealed holdout, legal/semantic issuer rights, external spending/privacy/model grants, and live experiment permission all remain separately unissued, regardless of future synthetic PASS.

**Independent-owner actions:** A separate bounded OC1 implementation worker can repair tests and synthetic gates; define role registry and capsule binding API only as *test fixture* with explicit denied default, forbid original-test rewrites, add held-out actual-entrypoint tests, preserve audit history or refuse rollback with typed error, and validate exactly A/B/C multiplicity/joins and an allowlisted packet schema. After repair HQ commissions a *new* independent I2 review. No direct production/weld/model grant. The competent semantic owner and independent human custodian must separately approve actual lawful sets, independent key custody, trusted signer registry, append-only external ledger and sampling/experiment grants.

## 4. Custody and change isolation

Only the assigned reviewer return directory may be committed; candidate and original oracles untouched. Do not promote the four accidentally tracked OC1 `__pycache__` binaries into signed semantic evidence. Full archive includes all sourcefree exact imported bytes, original+new JUnit/stdout and this report; an optional base64 text transport permits verifiable GitHub upload without altering archive bytes. The reviewer cannot embed its own future Git commit hash; verify branch HEAD after GitHub push.
