# Source-owner review and fan-in decision

**Decision:** `HOLD_OWNER_SCOPE__NO_PATCH__REPRODUCTION_AND_DECISION_PACKET_ONLY`.

The OC5 custody module is reproducible and the 49 hostiles are real, but the original owner has not issued the policy needed to repair them. This return preserves the original REDs and asks the owner for five exact decisions. No patch, merge, PRE-MAIN update or adoption is requested.

## Exact cut for owner review

- Repository: `maidiu/rawlsing`.
- Sealed startup: `342164a09e10aa70812299c12386ed0923308228`.
- F3 source return: `6477a89bb9160eba1dd10607c47534fa4dce6cc2`.
- OC5E reviewer: `67a4f1561cdad40192f00797d66b24fc4cd91589`.
- OC4 author: `0caaec590f6a8bf6744f22dc9c948c5fe233bc94`.
- Source: `WORKER_RETURNS/SOROK-R3-HQ310-OC4-CUSTODY-TEN-RED-REPAIR-R1/repro/custody_protocol.py`, Git blob `af2b7e943018077cb36808b5af1cd67704624bec`, SHA-256 `447e5bb738fc49c946a39ca438126e9c2a69d93025600f053662e56f846f9e3a`.
- Hostile test: `WORKER_RETURNS/SOROK-R3-HQ312-OC5E-EXECUTION-RECOVERY-R1/tests/test_oc5e_native_hostiles.py`, Git blob `9837579ebb5b2fbf3a41c967e584a166786e46b9`, SHA-256 `a9faf7ace27d0f3f3cfd1102de5c6c8d6888c12f16c7bbdde8b32bb232b84512`.
- PRE-MAIN `299f41e9…` has no corresponding custody path.
- Reproduction: 349 / 283 PASS / 66 RED; hostile court 159 / 110 PASS / 49 RED; inherited 131 / 121 PASS / 10 RED; OC4 36 / 36 PASS; prior predictions 23 / 16 PASS / 7 RED.

## Owner decisions required

### D1 — A6 capsule identity field types (highest priority, 11 cases)

The owner must define the lawful Python types and accepted derivation for:

`schema_version`, `version`, `content_digest`, `lawful_set_digest`, `coder_rubric_digest`, `split_assignment_digest`, `freeze_timestamp`.

Required answer: exact types, whether legacy forms are supported, and whether mismatch raises `IdentityMismatchError`, `TypeError` or `ValueError`. A6 is the only cluster that accepts invalid identity fields into `EscrowState.commit` and hashes them through a coerced projection.

### D2 — A1 normalized alias multiplicity (10 cases)

The owner must decide whether a packet with two spellings that normalize to the same allowed key (`context` / fullwidth/accented/CJG variant) must be refused, or whether only a single canonical spelling is required. The current `set(map(_normalized, value))` loses multiplicity and the recursive allowlist accepts both aliases.

Required answer: canonical key policy, duplicate-key refusal, and preservation of valid generated packets.

### D3 — A2 confusable threat model (6 cases)

The owner must decide whether Cyrillic/Greek/Armenian homoglyphs of leak tokens are in scope, which scripts/characters are covered, and how benign words are excluded. No owner-issued confusable policy exists; the OC4 commission mentions U+034F normalization but not full homoglyph coverage.

### D4 — A3/A4 typed signature contract (19 cases)

The owner must define the contractual exception for malformed signature objects and non-enum roles. The current paths raise `AttributeError` before `SignatureError`/`ConflictError`; they fail closed but violate typed refusal. Required answer: exception classes, ordering with `ConflictError`, and legacy mock-signature compatibility.

### D5 — A5 holder identity contract (3 cases)

The owner must decide whether unblind holder ids are string-only and whether non-hashable/scalar holders must raise `IdentityMismatchError` before `holder_roles.get`. This is the smallest fail-closed patch but still changes the exception API.

## Proposed fan-in order (only after owner answers)

1. **A6 owner decision and minimal patch** — highest material value; validate capsule identity before `commit`/envelope commitment; rerun all 159 and 349 assertions plus tampered multi-field cases.
2. **A1/A2 owner decision** — only after an explicit projection/confusable policy; preserve valid packets and existing positive controls.
3. **A3/A4/A5 typed-contract patch** — can be a separate small cut; no custody acceptance change.
4. **Fresh independent review of each patched cut** — original reviewer or another qualified owner; this worker does not review itself.
5. **No adoption** until owner accepts the exact source and the post-patch 159/349 evidence. No merge into PRE-MAIN or PR #519/#514/#516 by this return.

## Smallest material first consumer

The current first consumer is the branch-local OC4/OC5 sourcefree custody court (`EscrowState`/`CustodyCapsule` commit, unblind, release, signature and projection paths). That is **not** a Sorok product or native consumer. The smallest future material consumer for Sorok would be a source-qualified C12/BP4 custody integration that uses the owner-approved capsule/signature contract; it does not exist in this evidence.

## What would change this HOLD

- An owner-issued decision answering D1–D5 with exact accepted types, alias/confusable policy and exception classes.
- A bounded patch authored only after those decisions, preserving all 49 original assertions, the 10 historical REDs and the 7 prior predictions.
- Independent execution of the same 159/349 courts plus adversarial helds (malformed after commit, mutation, replay, cold reopen).
- A separate source-qualified reviewer and incumbent HQ intake.

## Three courts

- **ENGINEERING:** `HOLD_OWNER_SCOPE` — exact reproduction; no patch.
- **SCIENCE:** `TEST_ONLY_CUSTODY_FIXTURE_ONLY__NO_NATIVE_PRACTICE_OR_ACTOR_ACQUISITION`.
- **AUTHORITY:** `HOLD` — no owner or source-adoption right transferred; no merge/PRE-MAIN/native claim.

## Final remote SHA

The ordinary push binds this return. The exact 40-hex SHA is verified by direct `ls-remote` and reported in the final response; no self-reference is embedded. No force-push, no PRE-MAIN mutation, no self-adoption.
