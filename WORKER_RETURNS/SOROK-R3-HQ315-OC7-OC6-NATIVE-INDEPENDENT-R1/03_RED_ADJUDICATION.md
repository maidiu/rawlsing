# SOROK HQ315 OC7 — adjudication of all 21 remaining literal REDs

**Reviewer:** fresh independent I2 sourcefree custody reviewer. NOT the OC6 author, NOT the OC5E
author, NOT HQ, NOT an institutional custodian or semantic oracle issuer.
**Candidate under review:** OC6 `c6cb15d7417595c359571e4525dd0f0fd6c59d1f`.
**Method:** each case classified individually from this reviewer's own JUnit evidence, with original
before and after reason strings retained in `02_FROZEN_EXPECTATION_MATRIX.json`.
**No RED was edited, xfailed, skipped, suppressed or automatically excused.** Zero cases were
unclassifiable. Total 21 = 10 + 9 + 2.

## 10 — HISTORICAL_ORIGINAL_CONTRACT_RED

These ten were literal RED **before** the OC6 repair and remain literal RED **after** it, with byte-identical
reason strings in this reviewer's own independent runs. They are pre-existing fixture / procedural /
obsolete content-only-signature conflicts inherited from the original courts (OC1/OCR1/OC2/OC3), not
defects introduced, left behind or papered over by OC6.

This reviewer did **not** edit, xfail or excuse them. They are genuinely unresolved contract conflicts:
the original test oracle and the repaired implementation disagree about an earlier, unadjudicated
question. Closing them requires a competent owner's adjudication of the original contract, not a
custody input repair. **Status: OPEN, owner action required.**

| # | case | before | after |
|---|---|---|---|
| 1 | `test_h13_ledger_rollback_detected` | RED | RED |
| 2 | `test_h15_missing_signature_in_capsule_refused` | RED | RED |
| 3 | `test_signature_binds_content_and_rejects_alien_capsule` | RED | RED |
| 4 | `test_B01_valid_countersignatures_bind_content` | RED | RED |
| 5 | `test_Z03_declared_mock_roster_uses_public_derived_credentials` | RED | RED |
| 6 | `test_A08_mismatched_holder_unblind` | RED | RED |
| 7 | `test_A_capsule_unblind_permission[mod0-A01_revoked_unblind]` | RED | RED |
| 8 | `test_A_capsule_unblind_permission[mod1-A02_expired_unblind]` | RED | RED |
| 9 | `test_A_capsule_unblind_permission[mod2-A03_illegal_purpose_unblind]` | RED | RED |
| 10 | `test_positive_full_role_separated_lifecycle` | RED | RED |

## 9 — SELF_INVALIDATING_OC5E_WITNESS

These nine were literal PASS before the repair and are literal RED after it. Each one **asserts that a
vulnerability exists**, or asserts that the imported module is still the unrepaired pinned OC4 blob.

A test of the form "the hole is observed here" becomes false exactly when the hole is closed. Their new
literal RED is therefore the *expected* consequence of a correct repair, and is itself positive evidence
that the corresponding closure is real.

This reviewer verified each one independently rather than accepting the claim on faith: each family's
hole is independently re-attacked by this reviewer's own newly authored adversarial suite at
`tests/test_oc7_adversarial_v2_amended.py`, and the same suite yields 169 RED against the unrepaired
blob. The expectations are preserved verbatim; no green replacement was written under the same source
identity. **Status: SUPERSEDED EXPECTATION, closure independently confirmed real.**

| # | case | before | after |
|---|---|---|---|
| 1 | `test_alias_holes_are_observed_not_theorised` | PASS | RED |
| 2 | `test_capsule_identity_field_type_hole_is_observed` | PASS | RED |
| 3 | `test_confusable_holes_are_observed_only_for_nfkc_invisible_scripts` | PASS | RED |
| 4 | `test_imported_module_is_the_pinned_oc4_blob` | PASS | RED |
| 5 | `test_malformed_signature_holes_are_observed_as_attributeerror` | PASS | RED |
| 6 | `test_non_enum_role_string_hole_is_observed_as_attributeerror` | PASS | RED |
| 7 | `test_unblind_unhashable_holder_hole_is_observed_as_typeerror[dict]` | PASS | RED |
| 8 | `test_unblind_unhashable_holder_hole_is_observed_as_typeerror[list]` | PASS | RED |
| 9 | `test_unblind_unhashable_holder_hole_is_observed_as_typeerror[set]` | PASS | RED |

## 2 — DISPUTED_MALFORMED_OC5E_INPUT

These two were literal RED before the repair and remain literal RED after it. This reviewer verified
them at codepoint level rather than accepting either side's account:

* `[greek-o]` writes `l` + **U+03BF GREEK SMALL LETTER OMICRON** + `wful_answers`. U+03BF is NFKC-stable
  and is a lookalike for **`o`**, but it occupies the position of the **`a`** in the denied token
  `lawful_answers`. Folding yields `lowful_answers` != `lawful_answers`.
* `[mixed-cyrillic]` writes **U+0430** (a), **U+0435** (e) and **U+0455** (dze -> `s`). U+0455 is a
  lookalike for **`s`**, but it occupies the position of the **`w`** in `answer_key`. Folding yields
  `anseers_key` != `answer_key`.

In both cases the substituted character is a genuine NFKC-invisible homoglyph, but of the **wrong
letter**, so the constructed string is a different Latin word, not a confusable spelling of the denied
token. The other four cases in the same parametrized test fold exactly onto their targets and are
correctly denied.

This reviewer confirms the intended attacks ARE caught when spelled coherently: `l\u03b1wful_answers`
(Greek **alpha**, a lookalike for `a`) and `\u0430ns\u051der_key` (Cyrillic komi de, a lookalike for `w`)
are both correctly denied, together with 6 further correctly spelled confusables.

**These are malformed upstream test inputs, not remaining defects in the fold.** Widening the gate to
catch arbitrary near-miss spellings would be a typo/fuzzy-matching product policy with no authority
behind it, so this reviewer did **not** do it. See `05_OWNER_HOLD_TYPO_TOLERANT_LEAK_GATE_R1.md`.

| # | case | before | after |
|---|---|---|---|
| 1 | `test_confusable_leak_token_substitution_must_be_flagged[greek-o]` | RED | RED |
| 2 | `test_confusable_leak_token_substitution_must_be_flagged[mixed-cyrillic]` | RED | RED |

## Verdict on the 21

| classification | n | reviewer disposition |
|---|---:|---|
| historical original contract/procedural RED | 10 | **OPEN** — unresolved upstream contract conflict, preserved unchanged |
| OC5E self-invalidating hole/provenance witnesses | 9 | **SUPERSEDED** — expectation demonstrably invalidated by a correct closure; closure independently re-attacked and confirmed |
| disputed Unicode-confusable OC5E inputs | 2 | **MALFORMED UPSTREAM TEST INPUT** — not a remaining defect; verified at codepoint level |
| **unclassifiable / genuine remaining OC6 defect** | **0** | — |

**No genuine remaining defect attributable to the OC6 A1-A6 repair was found by this reviewer.**
The 21 retained literal REDs are 10 inherited open contract questions and 11 cases whose literal
assertions are demonstrably invalid, not evidence of an unclosed hole. That is a statement about
*these bounded sourcefree fixtures only*; it is not a claim of universal semantic non-leakage, real
custody, external anchoring or production fitness.

