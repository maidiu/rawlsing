# 03 — native tests and consumer attacks

Role: new distinct independent F6 scientific reviewer (**F6J**). Everything below was
physically executed against the pinned native S03FO
(blob `fc5e37fa5b2f0eb689593b42d95479d1327cb94c`, verified at `1428c2e92`, older
`182cc797` deliberately **not** used).

---

## 1. Test transport and its defects

| Artifact | Blob | Source |
|---|---|---|
| `pre553_heterogeneous_synthesis.py` | `fc5e37fa5b2f0eb689593b42d95479d1327cb94c` | candidate `05_NATIVE_STAGE/`, byte-identical to `01_STAGED_NATIVE/` |
| `pre553_empirical_objects.py` | `a61365b994e5c3c50de0f598fcf40e90abf757b6` | repo `rawlsing_next/`, byte-identical at sealed startup |
| `test_pre553_heterogeneous_synthesis.py` (inherited 24) | `07f405033e4703b1a0ddc710cffd529383561d1f` | candidate `02_TESTS/run/` |
| `test_f6c_frozen_court.py` (author 57) | `3cbb15f7a7d0a2edea09c2ee26709c3afb769344` | candidate `02_TESTS/` |
| `f6c_worlds.py` | `52c3dfe30dd807d79a67761a37c7d79214caacdd` | candidate `02_TESTS/` |
| `01_FROZEN_SOURCEFREE_STUDY_WORLDS.json` | `85d142c0e431457545ed1788e936614e01585525` | candidate return root |
| `fixtures.py` (inherited) | `8e4902df9ef9e6fa63e8e28617543257b8d40b28` | candidate `00_SOURCES/S03/repro/` |

**Transport defect G3.** The candidate resolves the inherited fixture through a git
symlink at `02_TESTS/run/WORKER_RETURNS/PYAT-R3-S03-F6-HETEROGENEOUS-SYNTHESIS-R1`
whose target is the **machine-absolute** path
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-r23-f6c/WORKER_RETURNS/PYAT-R23-F6C-NATIVE-F6-COMPARATIVE-CONTINUATION-R1/00_SOURCES/S03`.
The repo alone cannot reproduce the inherited suite. F6J stages the real fixture
bytes (blob `8e4902df`, identical to the candidate's copy) at the relative location
the test computes, and records the symlink as a portability defect.

---

## 2. Courts executed

| Court | Collected | Passed | Failed | Errors | Exit |
|---|---:|---:|---:|---:|---:|
| Inherited original S03FO suite (24 tests + 11 subtests) | 35 | 35 | 0 | 0 | 0 |
| F6C author court, pinned to F6J staging | 57 | 56 | 1 | 0 | 1 |
| F6C author court, candidate-shaped path | 57 | 57 | 0 | 0 | 0 |
| F6J new adversarial court | 53 | 53 | 0 | 0 | 0 |
| F6J frozen-world rational court | 12 worlds | 82/82 comparisons | 0 | 0 | 0 |

The single author failure is
`test_custody_imported_module_is_the_corrected_pinned_blob`, which asserts
`PRODUCER.__file__.endswith("05_NATIVE_STAGE/rawlsing_next/pre553_heterogeneous_synthesis.py")`.
F6J deliberately pins the import to its **own** byte-verified staging, so the path
suffix differs while the **bytes are identical** (both `fc5e37fa`). Re-running at the
candidate-shaped path gives 57/57. This is a custody-location control, **not** a
candidate defect — the same conclusion F6I reached, independently reproduced.

---

## 3. Pre-registered falsifiers

All seven were frozen and pushed at `e476ccc090ae0175a540e94c5c382d7e2a8453f0`
**before** any candidate test output was read.

### F1 / F1b — decision vocabulary is not conditioned on coverage — **FALSIFIED**

Two independent worlds (N5 2x2, N6 unary 3-category), both with a target stratum
having **no eligible source support**:

| | N5 | N6 |
|---|---|---|
| `decision` | `SYNTHETIC_CANDIDATE` | `SYNTHETIC_CANDIDATE` |
| `candidate.distribution` | `None` | `None` |
| `uncovered_target_mass` | `1/5` | `1/5` |
| covered subprobability sum | `4/5` | `4/5` |

The decision token asserts a synthetic candidate exists; the payload asserts the
complete target joint does **not**. A consumer keying on `decision` will treat a
no-positivity, 4/5-covered result as a successful candidate. Reproduced on two
independent topologies, so it is a systematic property of the vocabulary.

### F2 / A1 / A3 — admission is a boolean seam — **FALSIFIED**

| Probe | Observed |
|---|---|
| `test_origin=False`, `admit = lambda *a: True` | **accepted**; 4 invocations (`SOURCE_INDEXED_BASELINE` x2, `TARGET_JOINT_STANDARDIZATION` x2); identity/scope/operation/permission checks: **none** |
| `test_origin=False`, `admit = None` | correctly **refused** (`real source baseline lacks external owner admission`) |
| `test_origin=True`, any `admit` | **0 invocations** — the gate is bypassed entirely |

The evidence graph advertises
`authority_ceiling = EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE`. That "admission" is only
as strong as the caller's unverified boolean. The gate is fail-closed against
*absence* but fail-open against a *lying* callback, and is conditional on the
caller's own self-declared `test_origin` flag.

### F3 — equiweights are not calibration — **FALSIFIED**

`alpha` values `1/2`/`1/2` under equiweight and `3/4`/`1/4` under `3:1`. Scaling
every weight by 10 (`3:1 -> 30:10`) leaves the estimate **bit-identical**. A quantity
invariant to the absolute scale of its inputs cannot encode a calibration. No design
weights, calibration target, variance or reference distribution enters `alpha`.

### F4 — sensitivity halfwidth `3/50` is not a CI — **FALSIFIED**

With `mapping_bias_radius = transport_bias_radius = target_share_bias_radius = 1/50`,
the observed halfwidth is exactly `3/50` — the sum of three *assumed bias* radii.
`coverage_probability_available = False`. Native limitations text: "Sensitivity
envelopes are not confidence intervals; fixed target shares and disjoint
sources/strata for sampling variance; covariance and conditional uncertainty
unavailable."

### F5 — no cross-survey person invented — **correctly refused**

`complementary_binary_bounds(1/2, 1/2)` → lower `0`, upper `1/2`,
`independence_scenario = 1/4`, `scenario_is_measured = False`,
`dependence = UNIDENTIFIED`. Matches independent Fréchet derivation exactly.
`candidate.dependence` preserves `NO_CROSS_SURVEY_RESPONDENT_LINKS`.
**The falsifier fires only against a consumer that would quote `1/4` as an observed
joint.** The native is correct.

### F6 — conditional variance unidentified — **correctly refused**

`conditional()` returns `uncertainty = CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED`,
`observed_denominator = None`, and no variance field anywhere in the payload.
Self-conditioning returns `DESCRIPTIVE_SELF_CONDITIONING` /
`OUTCOME_LEAKAGE_TAUTOLOGY`. Out-of-support category returns `UNAVAILABLE` /
`CATEGORY_OUTSIDE_MAPPED_SUPPORT`. All correct.

---

## 4. New findings beyond the pre-registration

**G1 — `minimum_raw_support` is a stratum-level total, not a minority guard.**
The threshold compares the *summed* raw count of a stratum. In world N8, source S1
carries a genuine minority cell of 3 respondents inside a stratum of 100. Raising
`minimum_raw_support` above 3 leaves the estimate **unchanged** and S1 stays
eligible. Only when the threshold exceeds the stratum total (100) is S1 dropped —
and then S2 (also 100) is dropped too. Constructing a local variant with S2 total 200
and threshold 150 drops S1 alone and `alpha` renormalizes to `1` on S2, erasing S1's
minority pattern entirely. The threshold therefore gates whole-stratum admission and
cannot be represented as protecting minority representation.

**G2 — transformed evidence nodes carry no authority ceiling.**
Evidence-graph nodes `mapped:S1`, `mapped:S2` have **no** `authority_ceiling` key,
while `native:*` nodes carry `EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE` and
`target_joint` carries `DESCRIPTIVE_SOCIOLOGICAL_MODEL_ONLY`. A derived product has a
weaker authority record than its parent.

**G3 — inherited-fixture transport is not reproducible from the repo alone.**
Machine-absolute symlink; see §1.

---

## 5. Refusals verified to fire

| Class | Condition | Observed |
|---|---|---|
| Sample | duplicate `product_ref` | `DUPLICATE_SAMPLE`, `decision = SOURCE_INDEXED_BACKOFF` |
| Clock | target year 1900 outside source scope | `TIME_NOT_APPLICABLE`, backoff |
| Risk | `table_status = SUPPRESSED` | `SynthesisError` — suppressed cells cannot become zeros |
| Risk | incomplete joint domain (3 of 4 cells) | `SynthesisError` — omitted category cannot be manufactured as zero |
| Risk | `eligible_n` not conserved | `SynthesisError` |
| Risk | UNWEIGHTED `mass != n` | `SynthesisError` |
| Risk | weighted/raw zero-support mismatch | `SynthesisError` |
| Geo | target geography differs | `TARGET_SCOPE_MISMATCH`, backoff |
| Mapping | `mapping_confidence = LOW` | `MAPPING_UNQUALIFIED`, backoff |
| Mapping | wrong mapping preimage | `MAPPING_REVIEW_PREIMAGE_MISMATCH`, backoff |
| Overlap | no overlap review | `OVERLAP_UNRESOLVED`, backoff |
| Policy | zero weight assigned | `SynthesisError` |
| Policy | `dependence_kind != MEASURED_SAME_SURVEY_JOINT` | `SynthesisError` |
| Policy | target shares not summing to one | `SynthesisError` |

---

## 6. Raw JUnit

| File | SHA-256 |
|---|---|
| `05_JUNIT/inherited_s03fo_suite_24.xml` | see `07_EVIDENCE/all_courts_execution.json` |
| `05_JUNIT/f6c_author_court_57.xml` | see `07_EVIDENCE/all_courts_execution.json` |
| `05_JUNIT/f6j_new_adversarial_tests.xml` | see `07_EVIDENCE/all_courts_execution.json` |

Full stdout/stderr in `06_LOGS/`. Reproduce with
`python3 -B 03_SCRIPTS/run_all_courts.py`.
