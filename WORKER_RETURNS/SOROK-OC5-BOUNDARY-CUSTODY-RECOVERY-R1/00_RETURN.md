# SOROK OC5 — bounded custody invariants and 49-RED recovery decision

**Disposition:** `CONDITIONAL_OWNER_SCOPE__REPRODUCED_349_66_AND_159_49__NO_PATCH__OWNER_HOLD`.

The 49 hostile failures are real and independently reproduced. The OC4 commission does not authorize a blind 49-behavior rewrite: it targets the earlier ten OC3 REDs and explicitly disclaims semantic/oracle issuance. No original owner-issued policy for the 49 new alias/confusable/signature-typing/capsule-field rules was found. I therefore preserve all 49 and return an exact owner decision packet, not a fabricated green.

## Identity and host

- Repository: `maidiu/rawlsing` (private).
- Return branch: `agent/sorok-oc5-custody-49-hostile-defect-repair-r1`.
- Sealed startup: `342164a09e10aa70812299c12386ed0923308228`.
- Prompt head: `526c9a15f27809406d4f0a962673a7cc5afe3ded`.
- F3 source return: `6477a89bb9160eba1dd10607c47534fa4dce6cc2`.
- OC5E reviewer: `67a4f1561cdad40192f00797d66b24fc4cd91589`.
- OC4 author: `0caaec590f6a8bf6744f22dc9c948c5fe233bc94`.
- PRE-MAIN pin: `299f41e97a43c67be9cc76a79fa49b48f4e12e54`; the OC4 custody path is **ABSENT** there.
- Host: macOS x86_64 13.7.8; Python 3.11.3; pytest 9.1.1; SQLite 3.40.1.
- Editor/model: OpenCode / DeepSeek V4.1-Flash. No model/harness switch.
- Worktree: isolated return worktree at `.../opencode/oc5-return`; test runtime at `.../opencode/oc5-runtime`. No original author, reviewer, F3, PR #519/#514/#516 or PRE-MAIN tree was modified.
- No process-level lease audit is possible from this shell; no worktree/lease collision was found on this branch, and no original owner worktree was used as runtime.

## FINDING — exact reproduction

Source under test: `custody_protocol.py` Git blob `af2b7e943018077cb36808b5af1cd67704624bec`, SHA-256 `447e5bb738fc49c946a39ca438126e9c2a69d93025600f053662e56f846f9e3a`. Reviewer test: `test_oc5e_native_hostiles.py` Git blob `9837579ebb5b2fbf3a41c967e584a166786e46b9`, SHA-256 `a9faf7ace27d0f3f3cfd1102de5c6c8d6888c12f16c7bbdde8b32bb232b84512`.

| Court | Actual result | Expected |
|---|---:|---:|
| Inherited OC1/OCR1/OC2/OC3 | **131 cases / 121 PASS / 10 RED / 0 errors / 0 skips** | 121 / 10 |
| OC4 author controls | **36 / 36 PASS** | 36 / 36 |
| OC5E native hostiles | **159 / 110 PASS / 49 RED / 0 errors / 0 skips** | 159 / 110 / 49 |
| OC5 prior predictions | **23 / 16 PASS / 7 RED** | 23 / 16 / 7 |
| **Total** | **349 / 283 PASS / 66 RED / 0 errors / 0 skips** | 283 / 66 |

Exact commands are in `01_...json` and `02_...md`. All four JUnit XML files are embedded in `01_...json` with their SHA-256. The ten historical inherited REDs and seven prior OC5 predictions are preserved literally; none was xfailed, skipped, edited or reclassified.

## 49-RED causal clustering

The 49 are not 49 independent behaviors. They reduce to six invariants:

| Cluster | Count | Exact defect | Materiality / owner status |
|---|---:|---|---|
| A1 normalized allowed-field alias multiplicity | 10 | `detect_leakage` compares `set(map(_normalized, value))` to `{"context"}` and the recursive allowlist accepts both aliases; duplicate spellings survive | **Acceptance bypass** of the projection invariant. OC4 intent covers normalization variants but not alias multiplicity; owner rule not issued. |
| A2 confusable leak-token substitution | 6 | `_normalized` NFKC/NFKD-strips but has no confusable skeleton; Cyrillic/Greek/Armenian homoglyph leak tokens are admitted | **Acceptance bypass** of leak detection. No owner-issued confusable threat model. |
| A3 malformed signature object untyped | 18 | `require_second_signature` dereferences `primary_sig.signer_person_id` / `second_sig.signer_person_id` before type checking; raises `AttributeError` instead of `SignatureError` | **Fail-closed**, untyped. Typed API contract needs owner. |
| A4 non-enum role string untyped | 1 | `MockSigner.__init__` reads `role.value` before validating `Role`; plain `str` raises `AttributeError` | **Fail-closed**, untyped. Contract-only. |
| A5 unhashable unblind holder untyped | 3 | `holder_roles.get(holder_person_id)` raises `TypeError` for list/dict/set instead of `IdentityMismatchError` | **Fail-closed**, untyped. Holder contract needs owner. |
| A6 capsule identity field types unvalidated | 11 | `EscrowState.commit` and `capsule_envelope_commitment` accept `version`, `freeze_timestamp`, `schema_version`, `content_digest`, `lawful_set_digest`, `coder_rubric_digest`, `split_assignment_digest` with arbitrary Python types | **Highest-risk acceptance bypass** of exact capsule identity. OC4 intent requires exact identity; type policy not issued. |

**Must-fix for custody safety:** A6, A1, A2 (27 cases). A6 is highest risk because invalid identity fields are committed and hashed through a coerced projection. A1/A2 matter if model-visible packet keys/tokens are a custody boundary.
**Fail-closed contract-only:** A3, A4, A5 (22 cases). They already refuse the input; the defect is exception typing/telemetry, not custody acceptance.
**Branch-local policy:** A2 and the exotic A5 holder forms are not required by the basic sourcefree path unless the owner adopts that threat model. A3/A4/A5 are not reasons to block the valid SAY/commit path, but they are part of a typed API contract.

## INTERPRETATION — why no patch

The OC4 commission authorizes the **earlier ten OC3 REDs** and states the author is "not semantic/oracle issuer." The 49 OC5E hostiles are independently authored tests, not owner-issued rules. The owner-issued target list does not specify:

- whether duplicate normalized aliases must be refused and which normalization family is authoritative;
- whether confusable/homoglyph tokens are in scope and how benign words are excluded;
- which exception types are contractual for malformed signatures and holders;
- which Python types are lawful for each `CustodyCapsule` identity field and whether legacy forms are supported.

The OC4 return itself records a principled compatibility collision over content-only signatures requiring "a competent future owner." The OC5E review is not the owner. PRE-MAIN has no custody path. Implementing the 49 would invent a custody issuer/policy or silently change acceptance semantics. That is prohibited.

A partial patch for A3/A4/A5 (22 fail-closed typing cases) is technically small but still changes the owner's exception API without an owner-issued contract. It would leave the high-risk A1/A2/A6 acceptance bypasses untouched and could create a misleading partial green. A patch for A6/A1/A2 changes material custody/projection semantics and is exactly what requires owner scope. Therefore **no patch is applied**.

## Proposed smallest owner-qualified cuts (not applied)

1. **A5-typed-holder** (3 tests): reject non-string/non-hashable holder before `holder_roles.get`, raise `IdentityMismatchError`; smallest fail-closed contract test. Owner decision: is holder identity a string-only namespace?
2. **A3/A4-typed-signature** (19 tests): `isinstance` checks before attribute access, raise `SignatureError`/`ConflictError`; no acceptance change. Owner decision: exact exception contract and mock/legacy compatibility.
3. **A6-capsule-field-validation** (11 tests): validate `CustodyCapsule` fields before commit/envelope commitment; highest material value, but owner must define accepted types and legacy policy.
4. **A1-normalized-alias-multiplicity** (10 tests): count normalized keys and refuse duplicate aliases; preserve single allowed fields and generated packets. Owner must confirm alias policy.
5. **A2-confusable-skeleton** (6 tests): owner must first adopt a confusable threat model; then add a scoped skeleton scan.

Only after owner decisions should a bounded implementer patch be authored and independently reviewed. No 49-case blind rewrite.

## Three courts

- **ENGINEERING:** `HOLD_OWNER_SCOPE` — exact 349/66 and 159/49 reproduction; no patch. The 49 are preserved; 10 historical and 7 predictions remain literal.
- **SCIENCE:** `TEST_ONLY_CUSTODY_FIXTURE_ONLY__NO_NATIVE_PRACTICE_OR_ACTOR_ACQUISITION`.
- **AUTHORITY:** `HOLD` — original OC4/OC5 custody/source owner retains all rule, exception and adoption rights. No merge, PRE-MAIN, PR #519/#514/#516, native issuer or production claim.

## First actual consumer

The first consumer is the sourcefree OC4/OC5 custody test court: `EscrowState`/`CustodyCapsule` commit, unblind, release, signature and projection paths exercised by the 159-case hostile bank. There is **no production or native consumer**. A future Sorok consumer requires an owner-issued capsule/signature contract and a real C12/BP4 integration; branch-local tests alone are not material custody.

## DONE / REMAINING / CRITICAL BLOCKERS / LARGEST PRODUCTIVE MOVE / FLIGHT / DELTA

- **DONE:** exact four-court replay; 349/66 and 159/49; JUnit and source hashes; six-cluster mapping of all 49; historical 10 and prior 7 preserved; PRE-MAIN absence checked; five proposed owner-qualified cuts documented.
- **REMAINING:** owner decisions on A6 field types, A1 alias policy, A2 confusable threat model, A3/A4/A5 exception contract; then a scoped patch and independent review.
- **CRITICAL BLOCKERS:** no owner-issued custody/signature/projection policy for the 49; A6 invalid identity fields are accepted; A1/A2 projection bypasses are accepted; A3/A4/A5 are fail-closed but untyped.
- **LARGEST PRODUCTIVE MOVE:** owner decides A6 field-type contract first, then A1/A2 projection policy; only then commission a minimal patch and rerun the same 159/349 assertions.
- **FLIGHT:** sourcefree local Git/Python only; no source/native/PRE-MAIN mutation, no patch, no adoption.
- **DELTA:** OC5 recovery is bounded to a reproduced defect map and owner decision packet, not a 49-fake-fix green.

## Owner next action

Original OC4/OC5 custody/source owner (and distinct reviewer) must answer the five decisions in `03_SOURCE_OWNER_REVIEW_AND_FANIN_DECISION.md`. Incumbent Sorok HQ logs this evidence before any scoped fan-in. No self-adoption.

## Final remote SHA

The ordinary push binds this return. Its exact 40-hex SHA is verified by direct `ls-remote` and reported in the final response; a commit cannot contain its own final SHA. No force-push, no PRE-MAIN mutation.
