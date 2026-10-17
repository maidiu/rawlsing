# PYAT R28 F6K — F6 decision and admission authority repair

**OUTCOME:** `F6K_TYPED_HOLD__SIX_DEFECTS_LOCATED_AND_MAPPED__NO_REPAIR_CODE_SHIPPED`
**TERMINAL:** `PYAT_R28_F6K_DECISION_ADMISSION_REPAIR_HOLD__GITHUB_PUSHED`
**Branch:** `agent/rabochii-pyat-r28-f6k-decision-admission-consumer-contract-repair-r1` @ `813742d970d5484a53b7eac2fa3ba2fa76297432`
**Role:** original F6C productive author continuation — **NOT** an F6J/F6L independent reviewer or HQ.
**Write terrain:** `WORKER_RETURNS/PYAT-R28-F6K-F6-DECISION-ADMISSION-REPAIR-R1/` only.

## 1. I did not ship the repair, and I will not pretend otherwise

The commission asks for **actual repaired code** across six defects plus execution of three native/author/adversarial suites. **This return contains no repaired code.** My working budget for this lane was exhausted while locating the material across three separate branches. I am not going to emit a plausible-looking patch that I did not run, and I am not going to emit a test-green claim I cannot substantiate.

## 2. What F6J's own verdict establishes (the authority for these repairs)

`WORKER_RETURNS/PYAT-R27-F6J-INDEPENDENT-F6-EXPERIMENT-COMPLETION-R1/00_VERDICT.md`:

> `SCIENCE_EXECUTED__ARITHMETIC_AND_NATIVE_RECOMPUTATION_CONFIRMED__DECISION_VOCABULARY_AND_ADMISSION_SEAM_FALSIFIED__SOURCEFREE_ONLY__HQ_METHOD_DECISION_WITHHELD`

So the split is unambiguous and must be preserved exactly as the commission instructs:

- **CONFIRMED and to be preserved:** the quantitative arithmetic and the genuine native producer recomputation.
- **FALSIFIED and to be repaired:** the **decision vocabulary** and the **admission seam**.

F6J's evidence set available at `825b2d8050b550f1d52d3129883584fee2ef36c2`:
- `01_STAGED_NATIVE/rawlsing_next/pre553_heterogeneous_synthesis.py` (pinned native)
- `02_FROZEN/01_NEW_FROZEN_INDEPENDENT_WORLDS.json` (independent frozen worlds)
- `02_RATIONAL_RECOMPUTATION.json` (the confirmed arithmetic)
- `03_NATIVE_TESTS_AND_CONSUMER_ATTACKS.md` (the falsifications)

*(Note: F6J's commit `825b2d80` itself carries only `05_REMOTE_VERIFICATION.json` as a delta — the verdict and evidence live in its branch tree, not in that one commit. Successors must stage the **tree**, not just the commit delta.)*

## 3. Exact repair map — defect → file → required change

All five code-bearing artefacts are reachable at the R28 startup; the **native producer is NOT in `rawlsing_next/`** at this commit (confirmed `ABSENT`), it is staged inside F6C's return.

| # | defect (from commission) | file | required repair |
|---|---|---|---|
| 1 | **unsafe complete-candidate decision when target distribution is null** | `PYAT-R23-F6C…/02_TESTS/f6c_worlds.py` (decision path) | when the target distribution is **null**, the decision must **refuse / degrade to bounds**, never return a complete-candidate verdict. A caller keying only on `decision` must not be able to read a null distribution as a measured opportunity. |
| 2 | **unverified `admit=True` owner claims** | F6C consumer/admission seam | `admit` must be an **owner-verified** fact, not a caller boolean. An external admit callback is **not authentication**. |
| 3 | **caller-controlled `test_origin` authority bypass** | F6C consumer | `test_origin` must not be settable by the caller to obtain authority; origin must come from the pinned native provenance, not a parameter. |
| 4 | **missing mapped-evidence authority ceilings** | F6C consumer | mapped evidence must carry and enforce its authority ceiling; a mapped/proxy input must not inherit measured-grade authority. |
| 5 | **incorrect minority-support claims** | `f6c_worlds.py` / court | minority support must be preserved and reported honestly (no-drop), not claimed as satisfied when the cell is under-supported. |
| 6 | **machine-absolute fixture dependency** | `02_TESTS/test_f6c_frozen_court.py` (custody case) | the court pins an **absolute-ish path** (`05_NATIVE_STAGE/...`) — the very assertion that produced my 56P/1F in F6I. It must resolve the pinned blob by **identity (blob/sha)**, not by machine-specific location. |

## 4. What must be PRESERVED (do not "fix" these)

Per the commission and F6J: the **verified quantitative arithmetic**; the **genuine native producer**; **correct incomplete-coverage bounds**; **genuinely separate target/source worlds**; the **Fréchet dependence limitations**; and **uncertainty explicitly not being a confidence interval**. Equiweight 1/1 and bias radius 3/50 remain **policy/hypothesis**, never sample-calibrated weights or a CI.

## 5. Exact successor execution plan

1. Stage the F6C **tree** (`9aa0e7d3…`) and the F6J **tree** (`825b2d80…`) — not just commit deltas.
2. Run **inherited native 35** (`02_TESTS/test_pre553_heterogeneous_synthesis.py`) against the pinned native producer; record import sha256 and NUL preimages.
3. Run **F6C author 57** (`test_f6c_frozen_court.py`) — expect `05_NATIVE_STAGE` custody behaviour; repair defect #6 first so the suite is machine-portable.
4. Run **F6J's frozen scientific/adversarial suites** as the falsification baseline for defects #1–#5.
5. Implement the six repairs, then re-run all three suites plus **new downstream consumer attacks** on defects #1 and #2 specifically.
6. Produce **changed-world / unchanged-world receipts**: the World B null-coverage case must *change* behaviour (refuse/bound) while the confirmed World A arithmetic stays *byte-stable*.

## 6. Authority boundaries — unchanged

**No new original F6 source authority, no semantic issuer, no N9, OC05, N11/N12 or actor grant.** No frozen oracle modified. **Independent F6L review is required** for any repair I or a successor produces; I do not self-accept. HQ retains method adjudication.

**Terminal:** `PYAT_R28_F6K_DECISION_ADMISSION_REPAIR_HOLD__GITHUB_PUSHED`.
