# 03 — Alternative, error, sensitivity and holes

All values below are **observed native outputs**, not projections. Exact rational
strings are reported as the producer emitted them.

## 1. What the two worlds actually established

### World A — legitimate overlapping-stratum standardization **PASSES on the science**

| Quantity | Native producer | Naive pooled mixture (my analysis) | Predeclared truth |
|---|---|---|---|
| joint `[secure,formal]` | **13/25** | 2/5 | 13/25 |
| joint `[secure,informal]` | **1/10** | 1/10 | 1/10 |
| joint `[insecure,formal]` | **1/10** | 1/10 | 1/10 |
| joint `[insecure,informal]` | **7/25** | 2/5 | 7/25 |
| L1 error vs truth | **0** | **6/25** | — |
| P(formal \| secure) | **26/31** | 4/5 | 26/31 |

The two universes have *identical pooled* joints, so a pooled mixture reports a
stable `P(formal|secure) = 4/5`. Stratum conditioning to the target's own shares
recovers the truth exactly. This is the legitimate-improvement case the
commission asked for, and it is a genuine quantitative separation, not a
rhetorical one.

The naive mixture is **my comparison computation, explicitly not a producer
output**, and is labelled as such in `02_…json`.

### World B — positivity violation: honest bounds, not a false point **PASSES**

Target declares `remote_territory` (share 1/5) covered by **neither** source.

| Output | Value |
|---|---|
| `candidate.distribution` | **`null`** (no point estimate) |
| `uncovered_target_mass` | **1/5** |
| covered subprobability | **8/25, 2/25, 2/25, 8/25** (sums to 4/5, **not renormalised to 1**) |
| consumer `conditional()` | **`UNAVAILABLE` / `NO_COMPLETE_TARGET_JOINT`** |
| source-disagreement bounds | `[2/25, 19/25]`, `[2/25, 7/25]`, `[2/25, 7/25]`, `[2/25, 19/25]` |
| bias-sensitivity bounds (radius 3/50) | `[1/50, 41/50]`, `[1/50, 17/50]`, `[1/50, 17/50]`, `[1/50, 41/50]` |
| `complementary_binary_bounds(2/5, 2/5)` | lower **0**, upper **2/5**, independence scenario **4/25**, `scenario_is_measured: false` |

The uncovered stratum is **not** renormalised away and **not** zero-filled. It
widens every upper bound and leaves the point estimate unavailable.

## 2. Error and sensitivity structure that actually exists

- **Mapping bias radius** 1/100, **transport bias radius** 1/20, **target-share
  bias radius** 0 → sensitivity half-width 3/50.
- **Sampling variance** is a diagonal plug-in only; covariance is unavailable.
- **Conditional uncertainty is not identified** — `conditional()` returns
  `CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED` and `observed_denominator: None`
  in World A, and refuses entirely in World B.
- The module's own limitation string is explicit: *sensitivity envelopes are not
  confidence intervals*.

## 3. Holes I am not papering over

1. **World B's decision string is `SYNTHETIC_CANDIDATE` even though the
   distribution is `null`.** The `candidate` object exists with
   `covered_subprobability` + bounds, but the decision label reads as a
   candidate. A downstream consumer keying on `decision` alone, without checking
   `distribution is not None`, would mis-handle a positivity violation. I am
   reporting this as a **naming/semantics hole**, not "fixing" it: the decision
   vocabulary is the producer's, and changing it is a semantic-owner act.

2. **`admit` is a callback, not authentication.** With `test_origin=False` and a
   callback returning `True` for everything, the producer emits a candidate with
   decision `INFERRED_CANDIDATE_REQUIRES_REVIEW`. It cannot block. Admission is
   an integration boundary; it is explicitly not an authentication
   implementation, and `real_source_qualification` stays
   `EXTERNAL_REVIEW_REQUIRED`. A caller that treats a truthy callback as
   authorisation would be wrong.

3. **The inherited 24-test suite does not discriminate the corrected blob from
   the superseded one.** Both pass 24/24. The custody correction is real, but the
   inherited suite alone cannot detect it. My added
   `test_delta_omitted_native_category_is_refused_as_manufactured_zero` is the
   test that discriminates, and it is the one a reviewer should check first.

4. **My own frozen arithmetic was wrong once** (World B upper bounds, §4 below).

5. **Equiweighting A and B is a policy choice, not a finding.** `source_weights`
   are set to 1/1 by declaration. Nothing here estimates the best weights, and
   reweighting demonstrably moves the answer (the inherited suite exercises this
   directly).

6. **Both worlds are invented.** No real survey, wave, respondent, design
   validation, or empirical distribution is touched. The `design_variance`
   plug-ins are synthetic multinomial approximations explicitly labelled as not
   qualifying any real survey design.

7. **`minimum_raw_support` is diagnostic, not a pruner.** Raising it to 1000 makes
   `uncovered_target_mass = 1` and `distribution = null`, while all four native
   cells survive verbatim in the baseline. Verified.

8. **Self-conditioning is now caught.** `conditional(b, {"employment_position":
   "formal"}, "employment_position")` returns `DESCRIPTIVE_SELF_CONDITIONING` /
   `OUTCOME_LEAKAGE_TAUTOLOGY`, not a predictive `SUPPORTED_MODEL`. Present only
   in the corrected blob.

## 4. Disclosed frozen-expectation correction

I originally froze World B upper bounds at `14/25` (bias upper `31/50`). That was
**my arithmetic error**: I had failed to add the uncovered stratum's target share
(1/5) to the upper bound of **every** cell. The producer adds `share` to
`upper[k]` for every cell when a stratum has no eligible source, which is the
physically correct behaviour — a missing stratum must widen the bound, not
vanish.

The producer was not modified and no test was relaxed; only my own frozen
expectation was corrected, and the corrected values are the producer's observed
values. This is recorded in
`01_FROZEN_SOURCEFREE_STUDY_WORLDS.json → world_B._frozen_expectation_correction_disclosed`
and in `02_…json → disclosed_post_freeze_corrections`.

Two further post-freeze fixes were bugs in **my fixture builder**, also disclosed:
joint cells were built with `zip` instead of the 2×2 cross-product, and
`design_variance` was keyed by native codes instead of the contract-required
mapped labels.

## 5. No-drop / canonical-order evidence

Inherited S03/S03R/S03FR/S03FO suite: **24/24 PASS, 11 subtests PASS**
(`03_JUNIT/inherited_s03fo_suite.xml`), including
`test_frozen_expected_target_joint`, `test_minority_and_rare_pattern_not_pruned`,
`test_missing_stratum_no_renormalization`,
`test_support_threshold_is_diagnostic_not_rare_cell_pruning`, and
`test_replay_and_irrelevant_source_order`. Declared category order is preserved
end-to-end, and reversing `category_map` insertion order reverses the emitted
`ordered_categories` as S03FO requires.
