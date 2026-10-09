# HQ256 P02 — P01 committed-state court repair

**DISPOSITION: `NARROW_COURT_REPAIR_COMPLETE__GREEN_AT_COMMITTED_STATE__NOT_ADOPTED`**
**STOP:** `HQ256_P02_RETURNED_FOR_HQ_INDEPENDENT_INTAKE__NOT_ADOPTED`

**Branch:** `agent/space-bunny-pyat-hq256-p01-committed-court-repair-r1`
**Commission tip:** `ea5110f7d26835cccbfabf86173d9815d94ddf74` — verified against live origin ✅
**Exact startup parent:** `23438ab52f16abda5960a075dfca3f4d3396eab5` (the frozen P01 candidate) ✅
**Changed source paths:** **exactly one test file.** Production binder **byte-identical** to P01.

---

## 1. Live sealed HQ256 verified — the branch-local pointer was genuinely stale

The commission warned to use the **canonical live** `LATEST.json`, not the branch-local one. It
was right to:

| source | checkpoint | next_action |
|---|---|---|
| **branch-local** (stale, not authority) | `20261008-PYAT-HQ253-R01-R02-INTAKE-…` | `LAUNCH_HQ253_T01_…` |
| **live control** `b9a48616…` | **`20261008-PYAT-HQ256-R01-N01-RETURNS-P02-N02-ISSUED-R1`** | **`LAUNCH_HQ256_P02_SPACE_BUNNY_AND_N02_BROWSER_SOL_IN_PARALLEL__NO_P01_T1_ADOPTION`** |

Live authority confirms P02 is mine and that **`NO_P01_T1_ADOPTION`** — the quarantine holds.
Semantic PRE-MAIN `1f47063c3…` unchanged.

**R01 review** resolved independently at its commissioned SHA
`7db575466683e9c6511c65656f93e1f41158cffb` (branch `agent/deepseek-harness-pyat-hq255-…`), verdict
`REPAIR_NARROW`: production guard sound; exactly one test defective.

## 2. Defect reproduced first, before any edit

At the clean committed tip, `HEAD` binder blob is `848d2d0e…` while the test asserted the
pre-candidate `4ba00b8e…` → **1 failed, 15 passed, exit 1**.

**Root cause — a self-referential provenance guard.** It read `git rev-parse HEAD:<binder>` and
compared it to the *pre-candidate* baseline. Committing the candidate necessarily moves `HEAD` to
the candidate blob, so the guard could only pass **while the production edit was uncommitted**.
That is exactly how the original "16 passed" was produced. On every committed SHA of the
candidate the court was 15/16 — the guard certified an artefact state that never actually exists.

A provenance guard that cannot pass on the committed artefact it certifies certifies nothing.

## 3. The repair — pinned to fixed commits, never `HEAD`

One test, `test_adopted_binder_baseline_was_the_unmodified_owner`, renamed to
`test_adopted_binder_baseline_is_pinned_to_a_fixed_commit_not_head`:

- **Layer A — git-free, always runs.** The on-disk production file must hash to the recorded
  candidate `sha256 5221d8c2…`; the refusal code must occur exactly once; the recorded baseline and
  candidate blob identities must be distinct.
- **Layer B — git at FIXED commits.** Resolves `428be7595…:<binder>` == `4ba00b8e…` and
  `23438ab52…:<binder>` == `848d2d0e…`. Identical at every HEAD. **Skipped, never failed**, when no
  object store exists.

The baseline is **never** taken from `HEAD`.

## 4. Banked execution

| run | exit | result |
|---|---|---|
| **committed-state new court (the required proof)** | **0** | **16 passed** ✅ |
| four adopted baseline courts | 0 | **199 passed** |
| combined | 0 | **215 passed** |
| wider sweep (f8/applicability/service/C1/source-backed) | 1 | **380 passed**, 9 pre-existing collection errors |

The new court is green at a **clean committed tip**, which the pre-repair court never was. The 9
collection errors are absent `pandas`, absent `pyarrow`, and one absent unrelated harness module —
pre-existing and untouched.

## 5. Negative control — configured to distinguish the no-git artifact

| configuration | exit | result |
|---|---|---|
| production reverted, **git available** | 1 | **10 failed / 6 passed** |
| production reverted, **no-git /tmp** | 1 | **10 failed / 6 passed** |
| candidate present, **no-git /tmp** | 0 | **15 passed / 1 skipped** |

**Reconciling the counts.** R01 reported 10/6 and attributed the tenth failure to a no-git /tmp
terrain artifact, while my P01 run showed 9/7. Both are correct; they differ by exactly the
provenance test, whose outcome depends on whether production is committed. Pre-repair it could
*only* fail. After the repair it **fails meaningfully** when the reviewed candidate is absent from
disk and **passes** when it is present — a genuine discriminator rather than a broken assertion.

In a no-git tree the git-dependent layer now **skips** instead of spuriously failing, which
eliminates the terrain artifact R01 recorded.

## 6. Commission-mandated behaviours verified — no edits made to any other test

- **ExactRef.key set equality preserved** ✅
- **Order insensitivity** ✅ receipt `[A,B]` vs binding `[B,A]` → BOUND
- **Duplicate insensitivity** ⚠️ **confirmed still present**: binding `[A,A]` vs receipt `[A]`
  **binds**, and the duplicate lands in the canonical material (`['perm-A','perm-A']`).
  This is **R01 OBS_01**. **Not fixed** — this lane repairs one test and must not change set
  semantics. Reported for the next owner.
- **Release/permission precedence preserved** ✅ target-use still outranks permission; permission
  precedes release exactly as in the reviewed candidate; release-alone unchanged.
- **No extra authority** ✅ forbidden purposes intact, `grants_no_authority`, no permission
  granted, no model use added.
- **No C1 custody claim** ✅

I also independently confirmed R01's vocabulary claim: the refusal code occurs **0** times in the
baseline blob and **1** time in the candidate.

## 7. Production binder untouched

`git diff --stat` on `pre553_service_f8_source_scope_binding.py` is **empty** after all
negative-control cycling.

| identity | value |
|---|---|
| blob | `848d2d0eedb04b792747e9d6aaa49bb39d108a2c` |
| sha256 | `5221d8c2257ab1e8ec45289a30c57ba9ed4956b8609a890e80343718a6e9c66b` |
| bytes | 56186 |

No production line required adjustment, so no stop-and-request-fresh-commission condition arose.

## 8. Not claimed

Adoption, merge, cutover, T1 serving adoption, EE14 model-use permission, F8 producer custody,
resolution of R01 OBS_01, or resolution of the open HQ253 provenance/authority custody gap.
A separate DeepSeek-Harness rerun is still required for candidate adoption. No self-adoption.