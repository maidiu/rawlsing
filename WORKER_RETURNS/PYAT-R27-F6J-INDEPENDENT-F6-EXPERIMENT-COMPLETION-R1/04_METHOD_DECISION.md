# 04 — method decision (prepared recommendation, NOT an HQ instruction)

Role: new distinct independent F6 scientific reviewer (**F6J**). This document is a
prepared recommendation for HQ. It is **not** an HQ decision, **not** a method
accession, and **not** an original F6 semantic issuance. HQ method decision and the
original F6 / 35-wave grants remain **withheld**.

---

## 1. Question put to this court

Is the F6C candidate's heterogeneous target-joint standardization
(`PRE553_TARGET_JOINT_STANDARDIZATION@1`, native S03FO blob
`fc5e37fa5b2f0eb689593b42d95479d1327cb94c`) scientifically sound enough to recommend
for HQ method acceptance?

---

## 2. What this court can and cannot certify

**Can certify (independently reproduced):**

1. **Arithmetic.** All 12 frozen worlds — 10 genuinely new, 2 post-disclosure
   replication — reproduce to the exact rational. 82/82 comparisons against the real
   native producer. The standardization, the covered/uncovered decomposition, the
   source-disagreement bounds and the Fréchet bounds are arithmetically correct.
2. **Refusal behaviour.** Sample, clock, risk, geography, mapping, overlap, policy
   and domain-completeness refusals all fire. Suppressed cells cannot become zeros;
   an omitted category cannot be manufactured as zero; unweighted mass must equal raw
   count; weighted/raw zero support must agree; denominators must conserve.
3. **Honest scientific limits, when read correctly.** The consumer states
   `CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED`, labels sensitivity envelopes as not
   confidence intervals, labels the Fréchet independence scenario
   `scenario_is_measured=False`, carries `NO_CROSS_SURVEY_RESPONDENT_LINKS`, sets
   `sample_size=None`, and refuses self-conditioning as outcome leakage.
4. **Inherited suite.** 24 tests + 11 subtests, 35/35.

**Cannot certify:**

1. **The decision vocabulary.** Falsified (F1/F1b).
2. **The admission seam as authority.** Falsified (F2/A1/A3).
3. **Equiweighting as calibration.** Falsified (F3).
4. **Any confidence-interval reading of the sensitivity envelope.** Falsified (F4).
5. **Minority-representation protection by `minimum_raw_support`.** Falsified (G1).
6. **Any real-source, real-survey, person, actor or cross-survey claim.** Out of scope
   and prohibited.

---

## 3. The decisive tension

The candidate is **arithmetically sound** and **contractually honest in its
limitations text**, yet its **top-level decision token is dishonest** about the one
case that matters most scientifically: no positivity.

On N5 and N6 a target stratum has **no eligible source support at all**. The payload
correctly reports `distribution = None`, `uncovered_target_mass = 1/5` and covered
mass `4/5`. The decision token nonetheless reads `SYNTHETIC_CANDIDATE`. A consumer
that dispatches on `decision` — which is the natural integration point, since it is
the only top-level verdict field — will treat a null-distribution result as a
successful candidate.

This is not a cosmetic label problem. `SYNTHETIC_CANDIDATE` is the field the evidence
graph and downstream gates are expected to key on. It is currently a function of
`test_origin` alone:

```python
out["decision"] = "SYNTHETIC_CANDIDATE" if out["test_origin"] else "INFERRED_CANDIDATE_REQUIRES_REVIEW"
```

It never inspects `candidate["distribution"]`, `uncovered_target_mass`, or any
refusal. **A decision vocabulary that is blind to whether a result exists is not a
decision vocabulary.**

---

## 4. Prepared recommendation

**`CONDITIONAL_RECOMMENDATION__REJECT_AS_IS__RECOMMEND_ACCEPT_AFTER_DECISION_AND_ADMISSION_REPAIR`**

The F6C candidate should **not** be accepted as-is. It should **not** be rejected for
its arithmetic either — the arithmetic is independently reproduced and correct.

Specifically recommended:

**Required before HQ method accession**

1. **Repair the decision vocabulary** so it is a function of coverage and refusal, not
   of `test_origin` alone. At minimum: when `candidate["distribution"] is None` the
   decision must **not** be any `*_CANDIDATE` token. A typed
   `NO_COMPLETE_TARGET_JOINT` / `PARTIAL_IDENTIFICATION_ONLY` outcome is required.
   This is a small, local, testable change.
2. **Stop citing the admission callback as authority.** Either implement real
   owner-admission verification behind the seam, or downgrade every
   `authority_ceiling = EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE` claim to
   `UNVERIFIED_INTEGRATION_BOUNDARY`. The current text already says a callback "is an
   integration boundary, not an authentication implementation" — the evidence graph
   should say the same thing.
3. **Label `minimum_raw_support` accurately** as a stratum-level support threshold and
   remove any implication that it protects minority cells.

**Strongly recommended**

4. Give `mapped:*` evidence nodes an explicit `authority_ceiling`, or state why a
   derived product carries no authority record.
5. Replace the machine-absolute fixture symlink with a repo-relative path so the
   inherited suite is reproducible from the repository alone.
6. Keep the limitations text exactly as-is. It is correct and it is doing real work.

**Not recommended / not warranted**

7. No change to the standardization arithmetic. It is correct.
8. No change to the refusal lattice. It is correct and fail-closed.
9. No change to the Fréchet or conditional self-conditioning refusals. They are
   correct.

---

## 5. Preregistration strength

The commission asks explicitly for an assessment of "weaker author prereg". Recorded
honestly:

* The author's headline values (World A `13/25, 1/10, 1/10, 7/25`; World B `1/5` mass)
  were **publicly disclosed before this court**. They can never be re-used as blind
  pre-freeze predictions. Every use in this return is labelled
  `POST_DISCLOSURE_REPLICATION`.
* The commission records the author **corrected frozen expectations post-freeze**
  (`14/25 -> 19/25`, `31/50 -> 41/50`, `7/50 -> 17/50`). Amending a frozen expectation
  after observing output weakens the preregistration: the amended value becomes a
  post-hoc description, not a prediction.
* F6J independently re-derives **both** the old and the corrected values and finds the
  correction **arithmetically right**. So the correction improves the arithmetic while
  weakening the preregistration. Two separate judgements, both recorded.
* Mitigation: F6J constructed **10 genuinely new worlds** whose values were fixed and
  pushed (`e476ccc090ae0175a540e94c5c382d7e2a8453f0`) before any candidate test output
  was read. Those, and not the author's public numbers, are the genuinely
  preregistered science here.
* The commission's caution is accepted: **this court does not refuse legitimate
  science merely because public headline values spoil a blind freeze.** The public
  numbers are used, labelled, and never passed off as predictions.

---

## 6. Authority boundary

Pure sourcefree science only. **HQ method decision remains withheld.**
No original F6 semantic issuer. No N9. No OC05. No N11. No N12. No actor authority.
No real survey bytes. No cross-survey person. No 35-wave grant. No national
inference. No person, cohort or exposure claim.

This return is a **physically executed scientific verdict with new experimental
falsifiers**, not a method accession. Independent review and HQ acceptance remain
separate, and this court makes neither.
