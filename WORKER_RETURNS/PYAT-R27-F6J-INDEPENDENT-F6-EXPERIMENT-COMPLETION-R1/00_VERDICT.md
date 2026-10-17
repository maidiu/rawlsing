# 00 — F6J independent heterogeneous scientific verdict

**Role.** New distinct independent F6 scientific reviewer (**F6J**).
**Not** the F6C author (`9aa0e7d3a0cf9ab7654ce8e3d5cb15060235a48f`).
**Not** the previous incomplete F6I reviewer (`6d99650bed01eed8365ec38bd888741a88888a45`).
**Not** an original F6 semantic issuer. No N9/OC05, no N11/N12, no actor authority.

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (PRIVATE) |
| Branch | `agent/reviewer-pyat-r27-f6j-independent-heterogeneous-science-completion-r1` |
| Sealed startup | `09a87efc87110cc50c129b02033730ed8feca4e8` |
| Parent canonical | R26F `2f8a7b4d4aadd7f58e87201b738565962ca49d7b` |
| Candidate (F6C) | `9aa0e7d3a0cf9ab7654ce8e3d5cb15060235a48f` |
| Prior reviewer (F6I) | `6d99650bed01eed8365ec38bd888741a88888a45` |
| **Independent freeze** | `e476ccc090ae0175a540e94c5c382d7e2a8453f0` |
| Native S03FO blob | `fc5e37fa5b2f0eb689593b42d95479d1327cb94c` (at `1428c2e92`) |
| Write scope | `WORKER_RETURNS/PYAT-R27-F6J-INDEPENDENT-F6-EXPERIMENT-COMPLETION-R1/` **only** |

---

## 1. Verdict

**`SCIENCE_EXECUTED__ARITHMETIC_AND_NATIVE_RECOMPUTATION_CONFIRMED__DECISION_VOCABULARY_AND_ADMISSION_SEAM_FALSIFIED__SOURCEFREE_ONLY__HQ_METHOD_DECISION_WITHHELD`**

This is a **physically executed** scientific verdict, not a regression report. The
previous F6I court returned `REVIEW_HOLD` after reproducing the 57 author tests and
explicitly listed what it had **not** done. Every item on that list is done here.

| F6I admitted it did NOT do | F6J status |
|---|---|
| independent pre-freeze | **done** — 10 genuinely new worlds frozen and pushed at `e476ccc09` **before** any candidate test output was read |
| rational recomputation | **done** — exact `Fraction` engine, 82/82 comparisons against the real native producer |
| World B null | **done** — no-positivity worlds N5/N6 produce `distribution is None`, covered sum `4/5` |
| arithmetic correction | **done** — `14/25 -> 19/25`, `31/50 -> 41/50`, `7/50 -> 17/50` independently re-derived |
| decision-null attack | **done** — F1/F1b falsified on two independent worlds |
| inherited 24 + 11 | **done** — 35 collected, 35 passed |

---

## 2. What was physically executed

| Court | Cases | Result |
|---|---:|---|
| F6J independent frozen-world rational court | 12 worlds, 82 comparisons | **82/82 match** |
| F6J pre-registered falsifiers | 7 findings | 5 falsified, 2 correctly refused |
| F6J admission + consumer attacks | 7 findings | 3 falsified, 4 preserved |
| F6J new adversarial tests | **53** | **53 passed** |
| Inherited original S03FO suite | **35** (24 + 11 subtests) | **35 passed** |
| F6C author court | 57 | 56 passed, 1 custody-path control |
| F6C author court at candidate-shaped path | 57 | **57 passed** |

The one author failure is the suite's own **custody path-suffix control** (it asserts
the producer module is loaded from the candidate's `05_NATIVE_STAGE/` path). Against
this return's byte-identical staging that control must fail. It is **not** a
candidate defect — confirmed by re-running at the candidate-shaped path and getting
57/57, with both copies verified to the same blob `fc5e37fa`. This is the same
observation F6I made; it is independently reproduced here.

---

## 3. The genuinely new science

**10 of 12 worlds are `PREREGISTERED_NEW_F6J`** — values chosen by this reviewer,
frozen and pushed blind to candidate test output. **2 are
`POST_DISCLOSURE_REPLICATION`** — built from the author's publicly disclosed
headline values and explicitly **not** claimable as blind pre-freeze.

Perturbation axes covered: target-share changes, source weights, domain category
exclusion, minority representation, no-positivity, source swaps.

Every expectation was computed in exact rationals from the published algorithm by an
independent engine that **does not import the native producer**, then checked against
the real native execution.

### The commission's numbers, independently derived

| Commission reference | Independently derived | Verdict |
|---|---|---|
| pooled baseline L1 `6/25` vs correct `0` | `0` | **`6/25` is wrong.** With one source and one stratum, `alpha=1`, `share=1`, so the standardized joint *is* the baseline mapped joint. L1 is exactly 0. |
| conditional `26/31` vs `4/5` | both | **Two different worlds.** Author's public World A yields `26/31`; the F6J new world yields `4/5`. Both are arithmetically correct *for their own world*. Conflating them is an estimand error. |
| null distribution, covered sum `4/5`, widened upper `19/25`, `7/25` | exact | **Confirmed exactly.** `distribution is None`, covered subprobability sums to `4/5`, widened uppers are `19/25` and `7/25`. |
| corrected `14/25 -> 19/25` | exact | **Confirmed.** `14/25 + 1/5 = 19/25`. Omitting the uncovered share understates every upper bound. |
| corrected `31/50 -> 41/50`, `17/50` | exact | **Confirmed.** `31/50 + 1/5 = 41/50`, `7/50 + 1/5 = 17/50`, covered sum `4/5`, on an independent axis topology. |

---

## 4. What was falsified

**F1 / F1b — misleading decision vocabulary.** On two independent no-positivity
worlds the native emits `decision = "SYNTHETIC_CANDIDATE"` while
`candidate.distribution is None`, `uncovered_target_mass = 1/5` and covered mass
`4/5`. The decision token asserts a synthetic candidate exists; the payload says the
complete target joint does not. A consumer that keys on the decision token will treat
a null-distribution, no-positivity result as a successful candidate. The label is
**not conditioned on coverage**. This is a systematic property of the decision
vocabulary, not a fixture artefact.

**F2 / A1 / A3 — `admit=True` is not authentication.** With `test_origin=False` an
`admit` lambda returning `True` unconditionally satisfies **both** the
`SOURCE_INDEXED_BASELINE` and `TARGET_JOINT_STANDARDIZATION` gates — 4 invocations,
zero identity, scope, operation or permission verification. The evidence graph then
advertises `authority_ceiling = EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE`. That
"admission" is only as strong as the caller's unverified boolean.
Stronger still: for `test_origin=True` the callback is **never invoked at all** — the
gate is conditional on the caller's own self-declared `test_origin` flag.
The refusal path is genuinely fail-closed against *absence* (`admit=None` refuses
correctly), but fail-open against a *lying* callback.

**F3 — equiweights are not scientific calibration.** `alpha` is a normalized weight
ratio: scaling every weight by a constant leaves the estimate bit-identical
(`3:1 == 30:10`). A quantity invariant to the absolute scale of its inputs cannot
encode a calibration. No design weights, no calibration target, no variance and no
reference distribution enter `alpha`.

**F4 — sensitivity halfwidth `3/50` is not a confidence interval.** With radii
`1/50` each the halfwidth is exactly `3/50` = the sum of three *assumed bias* radii.
It has no sampling reference distribution and no coverage probability. The native's
own limitations text says "Sensitivity envelopes are not confidence intervals".

---

## 5. What survived review (correctly refused or correctly computed)

* **F5 — cross-survey person never invented.** `complementary_binary_bounds(1/2,1/2)`
  returns lower `0`, upper `1/2`, independence scenario `1/4` explicitly labelled
  `scenario_is_measured=False`, `dependence=UNIDENTIFIED`. Bounds match independent
  Fréchet derivation exactly. The candidate's `dependence` string preserves
  `NO_CROSS_SURVEY_RESPONDENT_LINKS`. Correct.
* **F6 — conditional variance unidentified.** The consumer returns
  `CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED`, `observed_denominator=None`, and carries
  no variance field. Correct.
* **Self-conditioning refused.** Outcome-as-conditioning-predicate returns
  `DESCRIPTIVE_SELF_CONDITIONING` / `OUTCOME_LEAKAGE_TAUTOLOGY`, not a predictive
  conditional. Correct.
* **Refusals preserved.** Sample (`DUPLICATE_SAMPLE`), clock (`TIME_NOT_APPLICABLE`),
  risk (`EXHAUSTIVE_DECLARED_JOINT_RISK_SET`, incomplete domain, denominator
  conservation, unweighted mass == raw count, weighted/raw zero mismatch),
  geo (`TARGET_SCOPE_MISMATCH`), mapping (`MAPPING_UNQUALIFIED`,
  `MAPPING_REVIEW_PREIMAGE_MISMATCH`), overlap (`OVERLAP_UNRESOLVED`), zero weights,
  non-`MEASURED_SAME_SURVEY_JOINT` dependence, target shares not summing to one.
* **Arithmetic.** The native reproduces all 12 frozen worlds to the exact rational.
  The producer's standardization arithmetic is sound.

---

## 6. Two further findings not in the pre-registration

**G1 — `minimum_raw_support` is a stratum-level total, not a minority guard.** The
threshold is applied to the stratum's *summed* raw count. A genuine minority cell of
3 respondents inside a stratum of 100 is never pruned by any threshold, and raising
the threshold above 3 leaves the estimate unchanged. The threshold therefore cannot
be described as protecting minority representation; it gates whole-stratum
admission. When a stratum total *does* fall below the threshold the source is
dropped and `alpha` renormalizes onto the survivors, which silently erases that
source's minority pattern entirely.

**G2 — transformed evidence nodes carry no authority ceiling.** The `mapped:*`
evidence-graph nodes have no `authority_ceiling` key at all, while the `native:*`
nodes and `target_joint` do. A derived product therefore has a weaker, not stronger,
authority record than its parent.

**G3 — inherited-fixture transport is not reproducible from the repo alone.** The
candidate resolves the inherited fixture through a git **symlink** whose target is
the machine-absolute path
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-r23-f6c/...`. F6I hit this and
corrected its own staging. F6J stages the real fixture bytes (blob `8e4902df`,
verified identical to the candidate's copy) and records the symlink as a portability
defect.

---

## 7. Authority boundary

Pure sourcefree science only. **HQ method decision remains withheld.** No original F6
semantic issuer, no N9, no OC05, no N11/N12, no actor authority, no real survey
bytes, no cross-survey person, no 35-wave grant. No national inference, no observed
temporal calibration, no person, no cohort estimand.

The F6C candidate's **arithmetic and native implementation are sound and independently
reproduced**. Its **decision vocabulary and its admission seam are not sound** and are
falsified above. Whether that combination is acceptable for method accession is an
**HQ decision this court does not make**.
