# SOROK HQ315 OC7 — independent OC6 native custody court

**VERDICT: `REVIEW_PASS_TESTONLY_CUSTODY_WITH_RETAINED_LITERAL_REDS`**
**Acceptance grain:** scoped `TEST_ONLY` sourcefree custody fixtures only.

| | |
|---|---|
| **Reviewer** | Fresh independent I2 sourcefree custody reviewer. **NOT** the OC6 author, **NOT** the OC5E author, **NOT** HQ, **NOT** an institutional custodian or semantic oracle issuer. |
| **Candidate under review** | OC6 `c6cb15d7417595c359571e4525dd0f0fd6c59d1f` |
| **Sealed startup** | `2f9118cd5a0a920a6a4f729289ff2798ca8fbaa3`, verified against direct remote branch HEAD |
| **Branch** | `agent/reviewer-sorok-r3-hq315-oc7-oc6-native-independent-r1` |
| **Original OC5E court** | `67a4f1561cdad40192f00797d66b24fc4cd91589` |
| **Environment** | `LOCAL_DOMINANT` isolated sparse worktree, real Python 3.11.3 / pytest 9.1.1 / Git 2.39.1 |
| **Model / editor** | Step 5 Preview in OpenCode (owner-selected pair). One agent, no helpers, no model or harness switch. |
| **Write terrain** | `WORKER_RETURNS/SOROK-R3-HQ315-OC7-OC6-NATIVE-INDEPENDENT-R1/` only |

---

## 1. Independent reproduction — every author number reproduced exactly

Nothing below is taken from the author return. Each figure comes from this reviewer's own JUnit XML,
counted from the XML rather than from pytest's exit code.

| Phase | Module under test | Cases | PASS | RED | Author claimed |
|---|---|---:|---:|---:|---|
| BEFORE, 349 unchanged | `af2b7e94…` unrepaired OC4 | 349 | **283** | **66** | 283 / 66 ✔ |
| AFTER, 349 unchanged | `4c185c18…` OC6 repaired | 349 | **328** | **21** | 328 / 21 ✔ |
| AFTER + 273 author controls | `4c185c18…` OC6 repaired | 622 | **601** | **21** | 601 / 21 across 622 ✔ |

Per suite (unchanged 349 splits 131 + 36 + 23 + 159):

| Suite | Before | After |
|---|---|---|
| inherited 131 (OC1/OCR1/OC2/OC3) | 121 PASS / 10 RED | **121 PASS / 10 RED — unchanged, identical reason strings** |
| OC4 author 36 | 36 PASS | **36 PASS** |
| OC5 prior predictions 23 | 16 PASS / 7 RED | **23 PASS / 0 RED** |
| OC5E native hostiles 159 | 110 PASS / 49 RED | 148 PASS / 11 RED |
| OC6 author controls 273 | not run in BEFORE | **273 PASS** |

Zero skips, zero errors, zero xfails were introduced by this reviewer.

## 2. Source and import authentication

- Git blob SHA-1 was recomputed from the **true binary preimage** (`b"blob " + len + b"\x00" + bytes`),
  never from transformed presentation text, and cross-checked against `git rev-parse <commit>:<path>`.
- **12/12 closure objects verified, 0 failures.** Two members are `.tar.xz` archive members and were
  **extracted** from the pinned archive blob, not transcribed.
- A reviewer-authored `conftest.py` asserted, at **every pytest session start**, that the module
  actually imported is the pinned one — by absolute path, SHA-256 and Git blob SHA-1 — and aborts the
  whole session on mismatch. Receipts in `observations/{before,after}/import_ledger.jsonl`.
- BEFORE ran against `af2b7e943018077cb36808b5af1cd67704624bec` (29 004 bytes);
  AFTER ran against `4c185c18dbee57603038e97886da8fc4aa834082` (36 648 bytes).
  No shadowing, stale or substituted module contributed to any tally.

## 3. Adjudication of all 21 remaining literal REDs

Every case was classified individually from this reviewer's own evidence. **No RED was edited, xfailed,
suppressed or automatically excused, and no new oracle was issued.** Full table with original before
and after reason strings: `03_RED_ADJUDICATION.md` and `02_FROZEN_EXPECTATION_MATRIX.json`.

| # | Classification | n | Disposition |
|---|---|---:|---|
| 1 | Historical original contract / procedural RED | 10 | **OPEN** — unresolved upstream contract conflict, preserved byte-identically |
| 2 | OC5E self-invalidating hole / provenance witnesses | 9 | **SUPERSEDED** — the assertion *is* the vulnerability; closure independently re-attacked and confirmed |
| 3 | Disputed Unicode-confusable OC5E inputs | 2 | **MALFORMED UPSTREAM TEST INPUT** — verified at codepoint level; not a remaining defect |
| — | Genuine remaining OC6 defect | **0** | — |

### 3.1 The two disputed A2 cases — codepoint-level finding

I verified these myself rather than accepting either side's account.

- `[greek-o]` writes `l` + **U+03BF GREEK SMALL LETTER OMICRON** + `wful_answers`. U+03BF is NFKC-stable
  and is a lookalike for **`o`**, but it sits where the denied token `lawful_answers` has an **`a`**.
  Folding yields `lowful_answers` ≠ `lawful_answers`.
- `[mixed-cyrillic]` uses **U+0430** (a), **U+0435** (e) and **U+0455** (dze → `s`). U+0455 is a lookalike
  for **`s`**, but it sits where `answer_key` has a **`w`**. Folding yields `anseers_key` ≠ `answer_key`.

In both cases the substituted character is a real NFKC-invisible homoglyph, but of the **wrong letter**,
so the string is a different Latin word rather than a confusable spelling of the denied token. The other
four cases in that same parametrized test fold exactly onto their targets and are correctly denied.

**The intended attacks are caught when spelled coherently.** I confirmed `l\u03b1wful_answers` (Greek
**alpha**, lookalike for `a`) and `\u0430ns\u051der_key` (Cyrillic komi de, lookalike for `w`) are both
correctly denied, plus 6 further correctly spelled confusables — while 14 safe multilingual / near-miss
strings produced **zero false positives**.

I therefore did **not** widen the fold. Matching arbitrary near-miss spellings is typo/fuzzy-matching
policy with no authority behind it. The genuine open product question is escalated as a typed
`OWNER_HOLD` in `05_OWNER_HOLD_TYPO_TOLERANT_LEAK_GATE_R1.md` with three costed options (`H1`/`H2`/`H3`).

## 4. Independent new adversarial court

Freshly authored by this reviewer from the module's public contract — not copied or derived from the OC6
author controls or the OC5E hostiles.

- **v1 frozen and committed at `4475403ea366b7637fb22f3875efaf1e43b4919f` BEFORE first execution**
  (61 test functions, blob `4ca9028d…`). Result **269 PASS / 5 RED**.
- Those 5 REDs are **preserved** in `observations/after/oc7_adversarial_v1.{xml,log}` and individually
  adjudicated in `04_REVIEWER_SUITE_CORRECTION_LEDGER.json`. **All 5 were my own expectation errors**,
  not OC6 defects — including one genuine test bug of mine (a deep-nesting builder that never increased
  depth, so the guard was never exercised) and one where I had assumed a conflict pair the module never
  declared. Only those 5 expectations changed, each to assert the **stronger** accurate contract.
- **v2 amended: 276 PASS / 0 RED.**

**Discrimination proof.** The same v2 suite was run against the **unrepaired** OC4 blob:
**107 PASS / 169 RED**. It is not trivially green.

| Group | Independent coverage |
|---|---|
| A1 | duplicate aliases at top level and inside `public_projection`; fullwidth / combining / Cf invisible spellings; alias+sibling; three-way alias collision; aliasing an unapproved key must not launder it |
| A2 | 8 correctly spelled homoglyph denials; 14 multilingual & near-miss **false-positive** controls; combining/invisible inside a token; confusables nested in lists and in key position |
| A3 | 6 malformed signature shapes × both positions; typed `SignatureError` never `AttributeError` |
| A4 | bare string role on both signers |
| A5 | 11 holder shapes incl. dict/list/set; typed `IdentityMismatchError` never `TypeError` |
| A6 | 14 string fields × 7 bad values; bool-as-int, zero/negative/float version; NaN/±Inf/bool/negative timestamp; lifecycle flags; commit refuses before any state change; fingerprint rejects coerced keys |
| G6 | **all 18 capsule fields** individually proven to change the full-envelope commitment |
| G7 | three-arm pairing positives plus 10 typed negatives and 4 shape negatives |
| G8 | strict packet projection allowlist; real nesting-depth guard |
| G9 | append-only ledger; post-freeze mutation via `object.__setattr__`; rollback refusal; tamper and truncation detection; double commit/unblind; release ordering; purpose gating |
| G10 | fingerprint determinism, family clone detection, full symmetry sweep of the conflict matrix |

**Preserved positives:** OC4's original 36 stay 36/36; the authentic capsule-bound two-signer pair still
verifies; full 18-field envelope binding holds.

## 5. Independent finding against the pinned candidate's evidence

At the pinned `c6cb15d7`, the return's `observations/` tree is flat and every retained JUnit/stdout file
carries `# phase: after` — `oc5e_native_hostiles.xml` records `failures="11"`, not the BEFORE `49`. The
BEFORE per-case matrix is present but has **no BEFORE JUnit/stdout behind it**, because both phases
wrote to the same filenames.

This does not change any verdict: this reviewer regenerated BEFORE evidence independently, and the
numerics reproduce exactly. It is recorded as an **evidence-completeness defect in the candidate's
return presentation**, not a custody defect, and it is disclosed rather than quietly absorbed.

## 6. Scientific verdict

**`REVIEW_PASS_TESTONLY_CUSTODY_WITH_RETAINED_LITERAL_REDS`**, at the grain of bounded sourcefree
custody fixtures only.

Accepted on this evidence:
- All 54 demonstrated REDs closed by OC6 are independently confirmed closed (47 OC5E + 7 OC5).
- All six A1–A6 closures survive independent adversarial re-attack at true native entrypoints.
- The ten historical REDs are preserved, byte-identical, with identical reason strings — not papered over.
- Zero genuine remaining defect attributable to the OC6 repair.

Not accepted, and not claimed:
- Any real signer institution, institutional custodian, or externally verified role.
- Universal semantic non-leakage or noninterference. The gate is a **lexical/schema fixture gate**.
- An externally anchored ledger. `EscrowState._event_proofs` lives in the same Python process as the
  state it protects and is not an independent protected store; a process that can mutate state can
  recompute proofs.
- Any cross-process persistence API (C07 is absent).
- Original respondent source, protected holdout, external model-use grant.
- Production, V3, N12, CURRENT or PRE-MAIN admission.

**Open for the competent owner:** the 10 historical contract REDs, and the `OWNER_HOLD` on whether the
leak gate should ever become typo-tolerant.

This reviewer does not adopt its own work. Any acceptance beyond this scoped TEST_ONLY verdict is the
competent owner's decision.

---

## 7. Artifact map

| Path | Purpose |
|---|---|
| `02_FROZEN_EXPECTATION_MATRIX.json` | per-suite before/after tallies, all 21 REDs with original reason strings, reviewer verdicts |
| `03_RED_ADJUDICATION.md` | human-readable adjudication of all 21 |
| `04_REVIEWER_SUITE_CORRECTION_LEDGER.json` | the 5 corrections to my own preregistered suite, with reasoning |
| `05_OWNER_HOLD_TYPO_TOLERANT_LEAK_GATE_R1.md` | typed owner hold on leak-gate policy |
| `environment_passport_delta.json` | `SOROK_WARM_ENVIRONMENT_PASSPORT_R1`, sanitized |
| `freezes/01_PREREGISTERED_EXPECTATIONS.json` | preregistration frozen **before** first execution |
| `observations/before/*` | BEFORE-phase JUnit + stdout + import ledger (349 cases) |
| `observations/after/*` | AFTER-phase JUnit + stdout + import ledger (622 + adversarial) |
| `observations/_stage_ledger.json`, `_stage_oc6_ledger.json` | 12/12 blob-authenticated closure objects |
| `tests/test_oc7_independent_adversarial.py` | frozen v1 suite, preserved unmodified |
| `tests/test_oc7_adversarial_v2_amended.py` | amended v2 suite |
| `repro/` | staging, court runner, import-authentication conftest |
