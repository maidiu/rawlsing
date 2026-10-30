# Replay, patch decision and unchanged oracles

## 1. Exact source and test custody

- `custody_protocol.py`: `WORKER_RETURNS/SOROK-R3-HQ310-OC4-CUSTODY-TEN-RED-REPAIR-R1/repro/custody_protocol.py`, Git blob `af2b7e943018077cb36808b5af1cd67704624bec`, SHA-256 `447e5bb738fc49c946a39ca438126e9c2a69d93025600f053662e56f846f9e3a`.
- OC5E reviewer test: `WORKER_RETURNS/SOROK-R3-HQ312-OC5E-EXECUTION-RECOVERY-R1/tests/test_oc5e_native_hostiles.py`, Git blob `9837579ebb5b2fbf3a41c967e584a166786e46b9`, SHA-256 `a9faf7ace27d0f3f3cfd1102de5c6c8d6888c12f16c7bbdde8b32bb232b84512`.
- OC4 author test: `.../repro/test_oc4_repair_controls.py`, Git blob `c139a877aa4586ec5ab729d333c40037840721d4`.
- Inherited tests: OC1 `94ad9449…` / `4b665a2a…` / dummy corpus `770efe72…`; OCR1 archive `9725b39e…`; OC2 `402f04ef…`; OC3 archive `068b1583…`; OC5 prior `588f91c7…`.
- The staging script verified every file's Git blob and SHA-256 before execution. No original test was edited.

## 2. Actual commands and exits

All runs used the staged source as `PYTHONPATH`, with `PYTHONHASHSEED=0` and `PYTHONDONTWRITEBYTECODE=1`, `--import-mode=importlib`, `-p no:cacheprovider`, and per-court `--junitxml`.

```sh
python3 -m pytest -q test_custody_hostiles.py test_positive_lifecycle.py \
  test_ocr1_independent_hostile.py test_oc2_regressions.py \
  test_oc3_independent_hostile.py --junitxml=inherited_131.xml
# exit 1; 131 tests; 121 passed; 10 failed; 0 errors; 0 skipped

python3 -m pytest -q test_oc4_repair_controls.py --junitxml=oc4_new_36.xml
# exit 0; 36 tests; 36 passed; 0 failed; 0 errors; 0 skipped

python3 -m pytest -q test_oc5e_native_hostiles.py --junitxml=oc5e_native_hostiles.xml
# exit 1; 159 tests; 110 passed; 49 failed; 0 errors; 0 skipped

python3 -m pytest -q test_oc5_prior_predictions.py --junitxml=oc5_prior_predictions.xml
# exit 1; 23 tests; 16 passed; 7 failed; 0 errors; 0 skipped
```

**Total: 349 tests / 283 passed / 66 failed / 0 errors / 0 skipped.** Every JUnit XML is embedded in `01_49_RED_CAUSAL_INVARIANT_CLUSTERING.json` with its SHA-256 (`inherited_131` `659ed7f2…`, `oc4_new_36` `1cee683d…`, `oc5e_native_hostiles` `ac727e49…`, `oc5_prior_predictions` `9f6b9d87…`).

## 3. Preserved historical negatives

The ten inherited REDs remain literal and unchanged:

1. `test_h13_ledger_rollback_detected`
2. `test_h15_missing_signature_in_capsule_refused`
3. `test_positive_full_role_separated_lifecycle`
4. `test_A_capsule_unblind_permission[mod0-A01_revoked_unblind]`
5. `test_A_capsule_unblind_permission[mod1-A02_expired_unblind]`
6. `test_A_capsule_unblind_permission[mod2-A03_illegal_purpose_unblind]`
7. `test_A08_mismatched_holder_unblind`
8. `test_signature_binds_content_and_rejects_alien_capsule`
9. `test_B01_valid_countersignatures_bind_content`
10. `test_Z03_declared_mock_roster_uses_public_derived_credentials`

They are procedural/early-refusal or content-only-signature compatibility conflicts, not the 49 hostiles. They must not be erased to make a green count.

The seven prior OC5 predictions remain literal:

- `test_malformed_signature_fails_typed[bad0|12|bad2]` (A3 overlap)
- `test_duplicate_normalized_keys_refused[packet0|packet1|packet2|packet3]` (A1 overlap)

## 4. Patch decision

**NO PATCH APPLIED.** No source, test, oracle, assertion or expected count was changed. The 49 remain 49 RED.

Reason: the original OC4 commission authorizes the earlier ten OC3 RED repair and explicitly says the author is not a semantic/oracle issuer. The 49 OC5E hostiles are independent reviewer-authored tests. No owner-issued rule was found for:

- duplicate normalized-key/alias policy;
- confusable/homoglyph threat scope;
- exact typed exceptions for malformed signatures or holders;
- legal Python types for `CustodyCapsule` identity fields and legacy compatibility.

The OC4 return itself names a content-only signature compatibility collision requiring a future competent owner. PRE-MAIN has no custody path. A patch would therefore invent policy or create a misleading partial green. The correct next step is owner decision, then a scoped patch under separate review.

## 5. Proposed minimal owner-qualified cuts (not applied)

| Cut | Cases | Proposed assertion | Owner question |
|---|---:|---|---|
| A5-typed-holder | 3 | non-string/hashable holder refused with `IdentityMismatchError` | Is holder identity a string-only namespace? |
| A3/A4-typed-signature | 19 | malformed signature/role refused with `SignatureError`/`ConflictError` before attribute access | Exact typed API/legacy mock contract? |
| A6-capsule-fields | 11 | invalid schema/version/content/lawful/rubric/split/freeze types refused before commit/envelope commitment | Exact field types and legacy policy? |
| A1-normalized-alias | 10 | duplicate normalized keys refused; single allowed fields and generated packets preserved | Is duplicate alias refusal required? |
| A2-confusable-skeleton | 6 | scoped confusable leak-token scan | Is a confusable threat model adopted? |

The smallest testable **fail-closed** cut is A5 (3 cases); the highest material value is A6 (11 acceptance bypasses); A1/A2 are packet-leak policy. None is implemented without owner permission.

## 6. RUN / NOT_RUN

- **RUN:** 131 inherited, 36 OC4, 159 OC5E, 23 prior predictions; source/blob staging; JUnit capture.
- **NOT RUN:** native CAN/ADP/SCI05/C11/C12, production deployment, real signer institution, protected holdout, external durable anchor, C07 cross-process, any patch.
- **NOT CLAIMED:** no sourcefree green without the 49; no native custody; no actor/person science; no adoption.

## 7. FINDING / INTERPRETATION / HQ ACTION / ACCOUNTABLE OWNER

**FINDING:** The 49 are six source invariants, not 49 independent policies. A6 (11), A1 (10) and A2 (6) are acceptance bypasses; A3/A4/A5 (22) are fail-closed untyped refusals.

**INTERPRETATION:** The custody protocol is recoverable as a bounded sourcefree test object only after owner policy. The current 349/66 reproduction is exact; the high-risk cluster is capsule identity and projection parsing, not the fail-closed error wording.

**HQ ACTION:** Obtain owner decisions on A6 and A1/A2 first, then authorize a minimal patch (A6, A1/A2 as approved) and rerun the same 159/349 assertions. A5/A3/A4 can follow as a typed-contract cut. No blind 49 patch, no adoption.

**ACCOUNTABLE OWNER:** Original OC4/OC5 custody and source-signature owner; independent source reviewer; incumbent Sorok HQ intake. No self-adoption.
