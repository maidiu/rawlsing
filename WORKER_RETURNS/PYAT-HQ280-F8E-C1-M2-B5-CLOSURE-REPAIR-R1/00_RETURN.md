# PYAT HQ280 F8E — C1 immutable release binding repair R1 — RETURN

**Terminal:** `HQ280_F8E_SOURCE_FREE_C1_M2_B5_CANDIDATE_REPAIRED_AND_ACTUALLY_TESTED_OR_EXACT_HOLD__NONISSUING`

**Authority:** HQD-2026-10-10-280. Canonical observed `6a8c91d99dca1ae2fd3559ba3c11ee26649e3cd9`; semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` — neither mutated. Branch `agent/rabochii-pyat-hq280-f8e-c1-m2-b5-closure-repair-r1`; sealed startup `6552be7b6e4a92654e98e5562d3e2b6f24d769bd`. Seed candidate `69bb0fc69175b2f6048b00cfa47dc852593798c0`.

**Execution substrate:** Step 5 Preview Free on a local Mac, Python 3.11.3, pytest 9.0.2, in an actual local Git worktree at the sealed tip with importable real owners.

## What was actually done

F8D-R's review was **not** runtime proof (it reported exit 4, zero collected). This return executed the suite for real in a local worktree.

**Baseline at the sealed tip: 14 passed / 1 failed.** The F8D candidate shipped with an already-failing authored test — `q1` and `q2` share one fixture risk-set ref, so its "risk ref swap" was a no-op.

**Before/after proof for the five hostile gaps (real owners, no mocks):**

| Gap | Before | After |
|---|---|---|
| H01 q1/q2 identity from shape | **ACCEPTED** alien `q(C\|A=0)` | REFUSED `CELL_PREDICATE_IDENTITY_MISMATCH` |
| H02 reversed q2 numerator | **ACCEPTED** alien `q(C\|A=1,B=1)` (`[('0',1),('1',0)]` vs honest `[('0',0),('1',1)]`) | REFUSED; order-sensitive frozen oracle is the second guard |
| H03 risk member cross-preimage | **ACCEPTED** rehashed substituted members | REFUSED `RISK_MEMBER_PREIMAGE_MISMATCH` |
| H04 model/walkback authorities | absent from AUTHORITY closure; no authority edge | 6 authority edges; both in M2 AUTHORITY closure and B5 snapshot; `affected()` reaches the product |
| H05 C1-03R graph | 31 determinants vs 22 edges — 9 never traversed | 31 edges for 31 determinants; every determinant is a real edge parent |

**Test result: 23 collected, 23 passed, 0 failed** — the original 15 plus 8 genuinely injected hostile regressions. Adjacent adopted-owner regression suite: **123 passed, 0 failed**.

## Delivery

Committed and pushed to the assigned branch; remote HEAD verified. Exact tip, changed-file list and verdict are reported alongside this return. Tracked writes were limited to the F8D-new candidate module, its test, and the files under `WORKER_RETURNS/PYAT-HQ280-F8E-C1-M2-B5-CLOSURE-REPAIR-R1/`. No adopted runtime owner, root manifest, raw survey, semantic law or canonical file was modified.

## Verdict

`SOURCE_FREE_C1_M2_B5_CANDIDATE_REPAIRED_AND_ACTUALLY_TESTED__FIVE_SOURCE_VISIBLE_DEFECTS_CLOSED_AT_DECLARED_SCOPE__NONISSUING`

The five defects are closed at the candidate's declared source-free scope. This is a **development-grade, nonissuing** repair: operative G0b, model-use, publication, CURRENT selection, G1 serving, independent producer custody and fresh-process replay all remain HELD, and the B5 trust-boundary limitation recorded by F8D-R still stands. No source-authority adoption, no self-adoption, no estate or scientific claim.
