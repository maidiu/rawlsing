# SOROK REMONT R10 — original ledgers and source repaired together

**2026-11-20 · Executable sourcefree engineering; not native owner or scientific certification.**

**Line of custody:** existing SOROK REMONT draft PR #1171; frozen author R9 HEAD `c4e1295a9ab9c5c5aa2135bb3dc33e19354e316d`; R10 integration source commit `78a502a1c42ad45aa23a3947ffa34817f6c995cb` (this additive test-receipt commit follows it). Original review draft #1182 `7e8cf7d050b59c869f46553e9cd715981f23ba7b` and new-defect repair draft #1183 `79ead983395d01a996fb6eeb5f639fed48dcdf1f` were incorporated into #1171 and closed as **superseded, not merged**.

## What is now in the actual SOROK REMONT original code and ledger

`REMONT/SOROK/OPEN_DEFECTS.json` and `.md`: 69 historical P identities conserved, with all 53 formerly author-repaired records individually advanced to independently reviewed **scoped first-fault sourcefree functional PASS** (independent review receipt #1182; formal independent G5/owner receiving still pending). Original 8 OPEN and 8 PARTIAL unchanged. Two further new defects registered:

- **SR-P070**: persisted world/actor JSON snapshot bytes and extra uncommitted world incorrectly passed complete chain verification. Exact first-source repair is `um_sorok_organism/storage.py`, Git blob `26ea3b17b7689056cec316df230229ad1cb014a9`.
- **SR-P071**: invalid NaN embodied sensor silently bypassed actor-access perception threshold. Exact first-source repair is `um_sorok_organism/constitution.py`, Git blob `1127dc83723e175507c2f351123c11a7f6cca734`.
- **New test module** `tests/test_remont_independent_followons_r10.py`, Git blob `c4dfd179ef3e0ea650bdaff6d8b8d27ea38e1e81`. Three cases, four negative subcases RED on R9, GREEN with R10 source. Two new first-source fixes are **author-local tested but not independently received**, distinct from the original 53 independent scoped review verdict.

**Current 71-P disjoint accounting:** 53 independently reviewed scoped functional PASS; 8 OPEN; 8 PARTIAL; 2 newly author-repaired pending separate independent review. T zero, E six. No native P2–P6/PFF/CAN/ADP/PYAT, production, actor or psychological-science grant; protected branch/current_progress pair unchanged: `HQ_CURRENTNESS_HOLD` on formal source/owner receiving.

## Actually executed from cold review source, reverified for R10

Working tree `review_candidate/` inside the archived independent source was originally extracted from the frozen R9 runnable ZIP, patched at the first-source owners, then the identical new regression-test file installed. All three source/test Git blob hashes verified byte-for-byte against #1171 R10.

- `python -m unittest discover -s tests -v` → **180 PASS / 0 FAIL**. Full transcript: `R10_180_NORMAL.log`.
- `python -O -m unittest discover -s tests -q` → **180 PASS / 0 FAIL**. Transcript: `R10_180_OPTIMIZED.log`.
- `PYTHONPATH=review_candidate python -m unittest -v reviewer_extra reviewer_new_defect` → **20 PASS / 0 FAIL**. Transcript: `R10_20_CROSS_FAMILY_NORMAL.log`.
- Same external test under `python -O` → **20 PASS / 0 FAIL**. Transcript: `R10_20_CROSS_FAMILY_OPTIMIZED.log`.

The 53-ID review, frozen RED evidence, reviewer cross-family source, and complete frozen R9 baseline receipts remain preserved under `REMONT/SOROK/REVIEWS/INDEPENDENT_R9_53_20261120/` in this same PR, not a competing REMONT ledger.

This receipt is a source/test-and-ledger reconciliation, not protected merge accreditation, a claim that a full person exists, or review of the novel P070/P071 patches by an independent second receiver.
