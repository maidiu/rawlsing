# SOROK HQ313 OC6 — Test-only native custody input-contract repair

**Repository:** `maidiu/rawlsing` (private) · **Role:** bounded sourcefree custody prototype implementation worker
**Branch:** `agent/rabochii-sorok-r3-hq313-oc6-native-input-contract-repair-r1`
**Exact sealed startup:** `e1dee739c22498b22b01f33ec2663d3d6bd33d68` (verified against direct remote HEAD before any edit)
**Model/host:** Muse Spark in the owner's existing Muse-configured OpenCode installation; one authorized LOCAL_DOMINANT isolated sparse worktree; one agent performed the entire repair, all pytest, evidence, commit and push. No Codex, DeepSeek-Harness, helper, editor/model switch or paid calls.
**Python/pytest:** 3.11.3 / 9.1.1, real `subprocess` and `pytest --junitxml`.

## Outcome

The independently demonstrated OC5E input-contract failures are repaired at the
real OC4 entrypoints, the ten historical test-contract REDs are preserved
literally, and no canonical requirement is relaxed.

| | BEFORE | AFTER |
|---|---:|---:|
| **Unchanged 349-case court** | **283 PASS / 66 RED** | **328 PASS / 21 RED** |
| Inherited OC1/OCR1/OC2/OC3 (131) | 121 PASS / 10 RED | **121 PASS / 10 RED — unchanged** |
| OC4 author controls (36) | 36 PASS | **36 PASS** |
| OC5E native hostiles (159) | 110 PASS / 49 RED | 148 PASS / 11 RED |
| OC5 prior predictions (23) | 16 PASS / 7 RED | **23 PASS / 0 RED** |
| **OC6 author controls (new)** | not applicable | **273 PASS / 0 RED** |
| **Grand total** | 283 / 66 | **601 PASS / 21 RED (622 cases)** |

54 of the 56 demonstrated REDs are closed: **47 of the 49 new OC5E REDs** and
**7 of the 7 OC5 predicted** (the two not closed are malformed OC5E inputs,
below).  Zero errors, zero skips, no xfail, no edit, no greenwashing.

## A1–A6 repairs, at the real entrypoints

| Family | Cases | Repair |
|---|---:|---|
| **A1** normalization-equivalent duplicate allowed-field aliases | 10 → 0 | New `_normalized_duplicate_aliases` / `_well_formed_allowed` gate run at **every** dict level. Every extra non-canonical raw spelling of an allowed normalized key is refused. Covers fullwidth / combining / accented siblings under `context`, `note`, `menu`, `public_projection`, `request_id`, `response`. |
| **A2** NFKC-invisible confusable leak tokens | 6 → 2 (residual below) | New bounded, explicitly enumerated `_CONFUSABLE_FOLD` (30 NFKC-invisible Cyrillic/Greek/Armenian homoglyphs, each `len 1 → len 1` ASCII). Scalar values are matched against both the normalized spelling and its confusable fold. Keys are never folded, so an unrecognised key stays fail-closed. |
| **A3** malformed signature objects | 18 → 0 | `require_second_signature` now checks `isinstance(sig, MockSignature)` for both positions **before any attribute dereference**, and raises typed `SignatureError`. |
| **A4** non-enum role | 1 → 0 | `require_second_signature` checks `isinstance(sig.role, Role)` before re-derivation; `MockSigner.__init__` also rejects a non-`Role` role with `TypeError`, which the existing `MockSigner.verify` `except` clause already turns into a fail-closed `False`. |
| **A5** unhashable holder | 3 → 0 | `EscrowState.unblind` checks `isinstance(holder_person_id, str)` (and non-blank) **before** the `holder_roles` dict access, raising typed `IdentityMismatchError`. |
| **A6** capsule field types | 11 → 0 | New `validate_capsule_fields` runs in `capsule_envelope_commitment` **and** `EscrowState.commit`, before any commitment or any state change: 14 identity/digest fields nonempty strings, `version` a positive int, `freeze_timestamp` a finite nonnegative number, `expired`/`revoked` booleans. `semantic_fingerprint` validates string keys. |

## The two A2 residuals are malformed OC5E inputs, not repairs

`test_confusable_leak_token_substitution_must_be_flagged[greek-o]` and
`[mixed-cyrillic]` do **not** spell a denied token even under a perfect
homoglyph fold, so no bounded fold can flag them without fabricating a match:

* `greek-o`: `'l\u03bfwful_answers'` folds to **`lowful_answers`**. U+03BF is a
  homoglyph for **`o`** and was placed where **`a`** belongs, so the string is
  one character short of `lawful_answers`.
* `mixed-cyrillic`: `'\u0430ns\u0435er\u0455_key'` folds to **`anseers_key`**.
  The `w` is simply absent and U+0435 (homoglyph for `e`) sits where `w` belongs.

OC6's author control `test_a2_confusable_leak_token_spelting_refused` uses
correctly spelled equivalents (`c\u03bfntrast_label`,
`expected_r\u0435sult`, `\u0435xp\u0435\u0441t\u0435d_result`, …) and they **are**
refused, so the A2 gate itself is demonstrated. No fold was widened to force
OC5E's two malformed strings green.

## The nine by-design flips (PASS → RED)

These are the OC5E *hole witnesses*: they assert that the defect is present, so
a correct repair necessarily invalidates them. They are the expected, honest
consequence of the repair — not regressions.

| Test | Family | Why it flips |
|---|---|---|
| `test_alias_holes_are_observed_not_theorised` | A1 | asserted every alias packet yields `[]` |
| `test_confusable_holes_are_observed_only_for_nfkc_invisible_scripts` | A2 | asserted every confusable yields `[]` |
| `test_malformed_signature_holes_are_observed_as_attributeerror` | A3 | asserted raw `AttributeError` |
| `test_non_enum_role_string_hole_is_observed_as_attributeerror` | A4 | asserted raw `AttributeError` |
| `test_unblind_unhashable_holder_hole_is_observed_as_typeerror[list,dict,set]` | A5 | asserted raw `TypeError` |
| `test_capsule_identity_field_type_hole_is_observed` | A6 | asserted all six malformed capsules commit |
| `test_imported_module_is_the_pinned_oc4_blob` | provenance | asserts the imported blob is the **unrepaired** pin `af2b7e94…`; a legitimate repair necessarily changes the staged blob to `4c185c18…` |

## What is preserved

* **The ten historical original REDs remain literally failing**, byte-for-byte:
  six procedural / early-refusal (`LedgerRollbackError`, `real capsule argument
  required`, `signature does not bind capsule content`, two
  `RevocationError`s at commit, `PurposeViolationError: LIVE_MODEL_REQUEST`) and
  four content-only mock-signature positives (`full signed capsule envelope
  identity missing or mismatched`). No edit, rewrite, skip, xfail or
  special-case; no `None`-capsule path was introduced.
* **Full-capsule commitment binding all 18 original fields** still holds and
  still refuses substitution of every field.
* **Append-only escrow** and all existing typed refusals are unchanged:
  `rollback_ledger` always refused; inactive capsules refused at `commit`
  before any state change; purpose discipline; three-arm pairing; malformed
  `EscrowState.commit` inputs.
* Author control `test_a6_all_eighteen_capsule_fields_still_bind_the_envelope`
  re-proves the full-capsule binding after the repair.
* **No claim of universal semantic non-leakage.** `detect_leakage`'s docstring
  states it is a lexical/schema gate; `test_a2_no_claim_of_universal_semantic_non_leakage`
  asserts paraphrases, keyboard-substitutions and non-token confusables are
  still admitted, and that legitimate multilingual text (CJK, Cyrillic word,
  Greek word, accented Latin) is not refused by fiat.

## Source identity and write discipline

| Item | Value |
|---|---|
| Pinned candidate commit | `0caaec590f6a8bf6744f22dc9c948c5fe233bc94` |
| Pinned OC4 source git blob SHA1 | `af2b7e943018077cb36808b5af1cd67704624bec` (matched at stage time) |
| Pinned OC4 source SHA256 | `447e5bb738fc49c946a39ca438126e9c2a69d93025600f053662e56f846f9e3a` |
| Repaired staged blob SHA1 | `4c185c18dbee57603038e97886da8fc4aa834082` |
| Repaired staged SHA256 | `ca85b844994e5ce6fd9e7a21c0f210d08b6d5e7519c63ac09d7dd8a9516fd90b` |
| Pinned OC4 directory edited? | **No** — read-only reference provenance; only the staged copy changed |
| All 9 other staged objects | blob SHA1 re-verified identical to their pins (2 are sealed-archive members) |

BEFORE-phase courts ran the **unrepaired pinned blob** (`imported blob is
pinned blob: True`); AFTER-phase courts ran the repaired blob. The 349-case
court is byte-identical in both phases; only the source under test differs.

## Files

| Path | Purpose |
|---|---|
| `repro/stage_source.py` | blobs-verifies and stages the sealed closure from named commits |
| `repro/apply_repair.py` | applies the A1–A6 repairs to the staged copy only (9 anchored edits) |
| `repro/run_court.py` | executes the court, writes per-case JUnit + matrices (phase `before`/`after`) |
| `repro/adjudicate.py` | per-case before/after adjudication |
| `repro/build_passport.py` | sanitized 00D passport + provenance |
| `tests/test_oc6_input_contract_controls.py` | 273 author controls |
| `repro/custody_protocol.py` | the repaired candidate source |
| `freezes/01_STAGED_SOURCE_MANIFEST.json` | per-object blob/SHA256 manifest |
| `observations/*.xml`, `*.log` | original JUnit + stdout per court, both phases |
| `observations/case_matrix_before.json`, `case_matrix_after.json` | full per-case matrices |
| `observations/before_after_adjudication.json` | per-case adjudication |
| `environment_passport_delta.json` | 00D passport, covers, provenance, HOLDs |

**Candidate only.** A distinct independent OC7 I2 review is required after this
return; adoption remains with the competent owner. No real signer institution,
protected holdout, semantic issuance, external model-use grant, V3/N12,
production/CURRENT/PRE-MAIN edit or adoption is claimed.
