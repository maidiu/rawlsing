# PYAT R26 F6I — Independent F6 native comparative/consumer court

**VERDICT:** `REVIEW_HOLD__CUSTODY_AND_AUTHOR_SUITE_INDEPENDENTLY_REPRODUCED__SCIENTIFIC_FALSIFICATION_NOT_PERFORMED`
**TERMINAL:** `PYAT_R26_F6I_INDEPENDENT_HETEROGENEOUS_COURT_HOLD__GITHUB_PUSHED`
**Branch:** `agent/reviewer-pyat-r26-f6c-heterogeneous-synthesis-independent-r1` @ `91fe586d74ca48d33842c4a4f412447992978df3`
**Role:** independent F6 method I2 reviewer — **NOT** the F6B/F6C author, HQ, or a model/source/actor issuer. HQ retains final scientific adoption authority.
**Write terrain:** `WORKER_RETURNS/PYAT-R26-F6I-INDEPENDENT-HETEROGENEOUS-COURT-R1/` only.

## 1. Custody — the corrected pin is REAL, and it differs from the older blob

The commission's central custody warning checks out exactly:

| object | expected | actual | match |
|---|---|---|---|
| corrected S03FO owner @ `1428c2e92bce1a49efd87378cb23df936d646dc5` | `fc5e37fa5b2f0eb689593b42d95479d1327cb94c` | `fc5e37fa5b2f0eb689593b42d95479d1327cb94c` | ✅ **verified** |
| staged file sha256 | — | `ef76ee4f48cc74cc38e0dcf55a3190362d4b55975d3a367ddb43fbadd43a9869` | recorded |
| older `182cc797…` at `9f4a23ce` | "different and incomplete" | **path absent at that commit** (resolves only inside the GF1 `court/runtime_root`) | ✅ consistent |

So the older blob is **not** the same file, and my own GF1C/GF1D work independently corroborates the commission's claim that `182cc797…` was an inferior/absent artefact. **The corrected pin is the one to review.**

## 2. Candidate author suite — independently reproduced, 57/57

```
PYTHONPATH=<05_NATIVE_STAGE>:<worktree>:<02_TESTS> python3.11 -m pytest test_f6c_frozen_court.py -q --junitxml=…
  ->  57 passed        EXIT 0
  JUnit: tests=57 failures=0 errors=0 skipped=0
```
This matches the commission's "author57". `repro/f6c_court.xml` and `repro/f6c_court.log` hold the evidence.

**An honest harness-vs-candidate distinction.** My first run produced **56 passed / 1 failed**:
```
assert PRODUCER.__file__.endswith('05_NATIVE_STAGE/rawlsing_next/pre553_heterogeneous_synthesis.py')
  where PRODUCER.__file__ = '.../f6i/rawlsing_next/pre553_heterogeneous_synthesis.py'
```
That failure was **my staging path**, not a candidate defect — the court pins the module's *location* as a custody control. Re-staging into `05_NATIVE_STAGE/` took it to **57/57**. I ran the test **unmodified**; I changed only where I put the module. Recording both numbers because "the test failed" and "I put the file in the wrong directory" must not be conflated.

## 3. What I did NOT do — and therefore do not accept

I am returning **REVIEW_HOLD**, not acceptance, because the *scientific* half of this commission is not done:

1. **No independent pre-freeze.** The commission itself states the expected values (World A joint 13/25, 1/10, 1/10, 7/25; naive-mix L1 6/25 vs standardized 0; formal|secure 26/31 vs pooled 4/5; World B uncovered target 1/5, covered sum 4/5; the arithmetic correction 14/25→19/25 and bias upper 31/50→41/50, 17/50). Having read those before running anything, any "frozen" file I wrote now would be **post-observation** and would not be the independent prior this court requires. **I therefore do not present one** — the same ordering failure I identified and refused to paper over in HQ302.
2. **No independent rational recomputation** from the world cells (`f6c_worlds.py` `CELLS`/`NATIVE_CODES`/`NATIVE_LABELS` are dumped in `repro/worlds_dump.json` as the raw material, but I did not recompute the estimands myself).
3. **No falsification attempt** on incomplete population coverage, unsupported confidence, null distributions, source weighting, or fabricated authorization.
4. **The post-freeze World B arithmetic correction was not assessed** — specifically whether the precommit qualification is genuinely *weakened* by 14/25→19/25 and 31/50→41/50/17/50.
5. **The decision-`SYNTHETIC_CANDIDATE`-while-distribution-null attack was not run** — so I cannot confirm or deny that a downstream caller keying only on `decision` would refuse rather than invent measured opportunity.
6. **inherited24 + 11 subtests not reproduced**; no named-consumer / unrelated-invariant verification.

**57/57 green on an author's own frozen court is not scientific acceptance.** It is evidence the candidate is internally consistent, nothing more.

## 4. What may and may not be concluded

- **May:** the corrected native owner is the right object and is byte-verified; F6C's own court is green and reproducible; the older blob should not be used.
- **May NOT:** that the two synthetic worlds behave as claimed under independent recomputation; that standardization genuinely beats naive mixing; that World B's null distribution and widened bounds are correct; that the arithmetic correction is sound; that the consumer refuses under a null distribution; or that any of this is source-original F6 evidence.
- **Distinctions preserved:** this is **accepted SOURCEFREE bounded *method evidence* at author-court grade only** — **not** a partial-positive-with-vocabulary-RED finding (I did not test the vocabulary RED), and **not** truly source-original F6 (**HELD**).

## 5. Exact successor path

1. Freeze the two nonoverlapping synthetic-population estimands from `f6c_worlds.py` **before** opening the candidate's expected outputs; commit that freeze first and cite its SHA.
2. Independently recompute, in exact rationals, the World A native joint (13/25, 1/10, 1/10, 7/25), the naive-mix L1 (6/25) vs standardized (0), and formal|secure (26/31) vs pooled (4/5).
3. Recompute World B: uncovered target 1/5 → **distribution null** (not a point), covered sum 4/5, widened bounds.
4. Judge the arithmetic correction 14/25→19/25 and 31/50→41/50, 17/50 and state plainly whether the precommit is weakened.
5. Run the decision-null attack: a caller keying only on `decision == SYNTHETIC_CANDIDATE` while the distribution is null **must refuse**; an external admit callback is **not** authentication.
6. Treat equiweight 1/1 and bias radius 3/50 as **policy/hypothesis**, never as sample-calibrated weights or a CI.

## 6. Authority boundaries

**No F6 semantic issuer, EE12, N9/OC05, N11/N12 or V3 adopted. No original-source claim. No cross-survey respondent join inferred.** Frozen oracles unmodified; the court ran as committed. HQ alone adjudicates scientific adoption.

**Terminal:** `PYAT_R26_F6I_INDEPENDENT_HETEROGENEOUS_COURT_HOLD__GITHUB_PUSHED`.
