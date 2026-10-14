# 03 — executed outputs and consumer receipts (HQ295 W10)

All commands below were executed on the local runtime (Python 3.11.3, macOS darwin x86_64) at sealed startup `1616b299f97ae3b4e2b8003659f59439fcc0c77a`. Full machine-readable artifacts: `outputs/experiment_result.json`, `outputs/consumer_receipt_A.json`, `outputs/consumer_receipt_B.json`, `outputs/hostile_oracle_results.json`, `outputs/run_log.txt`.

## 1. Commands and actual output

### 1.1 Probe unit harness (isolated candidate)

```
$ python3 -m pytest WORKER_RETURNS/PYAT-R3-HQ295-W10-WORLD-CONSUMER-PROBE-R1/probe/test_world_consumer_probe.py -q
.................                                                        [100%]
17 passed in 1.64s
```

### 1.2 Reused-owner regression suites (read-only evidence that the reused seams are green at this tree)

```
$ python3 -m pytest rawlsing_next/tests/test_pre553_empirical_possibility_provider.py \
    rawlsing_next/tests/test_pre553_analytical_composition.py \
    rawlsing_next/tests/test_m4_v557_v558_publication_repository.py \
    rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py \
    rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py \
    rawlsing_next/tests/test_wsc_gt0_end_to_end_integrated.py \
    rawlsing_next/tests/test_wsc_gt0_prev3_bridge.py -q
........................................................................ [ 64%]
.......................................                                  [100%]
111 passed in 16.59s
```

### 1.3 Probe CLI (producer-to-consumer execution)

```
$ python3 WORKER_RETURNS/PYAT-R3-HQ295-W10-WORLD-CONSUMER-PROBE-R1/probe/run_probe.py
experiment_id: E05_VERTICAL_CONTEXT_ROUTE_POSSIBILITY_CONTRAST_R1
grade: TEST_ONLY_INTERFACE_COURT__NOT_OPERATIVE_N9_WORLD__NOT_INTEGRATED_N10W_OWNER__NO_ACTOR__NO_MODEL_USE_ISSUER
positive_oracles_pass: True
hostile_oracles_pass: True
typed_refusals_pass: True
replay_invalidation_pass: True
sourcefree_interface_court_pass: True
integrated_n9_n10w_pass: False
receipt_a_replay_hash: e4a85143af8b1f06fb299c2ae621ad4eef76b312f9cb2ec066f5e859d67c7330
receipt_b_replay_hash: c99b52a15b9ade09d73f76594d579a23aa595c2bf64237acc6dbf9b04701d364
n10e_lane_hash: f1c033e6a00ec37d8817a0ce7cdbe185e29d12265dab90adf0640153f5163186
metrics: {"actor_or_stereotype_leak_count": 0, "constraint_grade_change_count": 3, "counterfactual_selectivity": {"household_only_contamination": [], "institution_only_contamination": [], "unchanged_controls_invariant": true}, "minority_path_retention_exact": [5, 5], "persona_quality_effect": "TEST_HYPOTHESIS_NOT_MEASURED", "semantic_currentness_integrity": 0, "source_backed_successor_quality": "NOT_MEASURED__NO_SOURCE_OR_MODEL_USE_ISSUER", "typed_route_change_count_eligibility": 1, "unmeasured_probability_fraction_exact": [5, 5]}
(exit 0)
```

### 1.4 Missing objective-context boundary (owner-specific blocker, exact output)

```
$ python3 -c "import rawlsing_next.prev3_objective_position_v557_v558_publication"
ModuleNotFoundError: No module named 'rawlsing_next.prev3_objective_position_materializer'
```

## 2. Consumer receipt (executed)

Receipt schema `W10_N10W_PROGRESSIVE_WORLD_CONSUMER_RECEIPT@1`, consumer id `urn:rawlsing:hq295-w10:consumer:E05_VERTICAL_WORLD_N10E_N10W_PROBE@1`, adapter contract `W10_N10W_PROGRESSIVE_PARENT_COPARENT_ADAPTER@1.0.0`. Full bodies in `outputs/consumer_receipt_A.json` / `outputs/consumer_receipt_B.json`.

### 2.1 Bound identities (variant A)

| Item | Exact ref / hash |
|---|---|
| Request fingerprint | `dd667b3835231da4b0bc113bafdeb24410bb15096c6a0c59e6a3d86f585cf38c` |
| V558 repository (modeled world A) | `V558REPOSITORY_BUNDLE` `V558REPO:420798d0ad3f37b623592db6d36a3454f1c892c59a79d9bd1534ea2507622423` |
| M4 resolution receipt | `V558_RESOLUTION_RECEIPT` `V558REC:1487d9287c3b8a81c34a673924d7a63354ce2fb2e06a6c455860b758f73ec8dd` (state `RESOLUTION_COMPLETE`) |
| M5 RSC (as-of 2008) | `SCR5578_RESOLVED_STRUCTURAL_CONTEXT@1.0.0` `RSC:c9f02d0dd6ae3a6c3ffc497e6fbbff58d5dd34d88ebf02dc7c6bbd92e7c7a236` |
| M5 currentness | `M5_STRUCTURAL_CURRENTNESS_RECEIPT`, state `CURRENT`, decision-effective-time `urn:test:w10:as-of:2008` |
| N10E provider receipt | hash `f1c033e6a00ec37d8817a0ce7cdbe185e29d12265dab90adf0640153f5163186` |
| N10E computed evidence | `C1_POSITIONED_SUBJECT_SLICE_EVIDENCE@1` `urn:rawlsing:c1:positioned-subject-slice-evidence:sha256:b2407eeb3d22cc0d71e5d13308b0149338761efc4ef40921ab363c3cd9c78307` |
| N10E composed identity | `01c381d3f3c386cfc22fd2f57b8e2c244771ddf1529d4f8ab8c7b1cf41bd50dd` |
| N10E consumer result hash | `47b51a3b6df4ec051b5b9fb04a92760c791f4ac761f20a157966cbe1b481a4be` |
| Receipt A replay hash | `e4a85143af8b1f06fb299c2ae621ad4eef76b312f9cb2ec066f5e859d67c7330` |
| Receipt B replay hash | `c99b52a15b9ade09d73f76594d579a23aa595c2bf64237acc6dbf9b04701d364` |

Computed N10E lane (base AT07 law): denominator 60; cells `no` raw 6 → `{'$exact_fraction': [1, 10]}`, `yes` raw 54 → `{'$exact_fraction': [9, 10]}`. `CHANGED_SOURCE_LAW` variant: denominator 70; `no` 16 → `[8, 35]`, `yes` 54 → `[27, 35]` (lane hash changes; route table invariant).

### 2.2 Progressive stages (A vs B), C2 final typed route support

| Route | A (buffered public access) | B (institutional barrier + care pressure) | Witnessed modeled rule |
|---|---|---|---|
| `formal_schooling` | `ELIGIBLE_IN_MODELED_CONTEXT` | `BLOCKED_BY_MODELED_ACCESS_RULE` | C1 `M1_INSTITUTIONAL_ACCESS_RULE` (seat/fee/admin); C2 `M2_NONCONTAMINATION_HOUSEHOLD_PREMISE_DOES_NOT_REWRITE_INSTITUTION_RULE` |
| `nonformal_peer_study` | `POSSIBLE` | `POSSIBLE_BUT_TIME_CONSTRAINED` | `M2_CARE_TIME_CONSTRAINT_RULE` |
| `paid_apprenticeship` | `CONDITIONAL_TIME_AND_OPPORTUNITY` | `CONDITIONAL_WITH_HIGHER_TIME_TRADEOFF` | `M2_LABOR_TIME_TRADEOFF_RULE` |
| `family_care_work` | `POSSIBLE_NOT_IMPOSED` | `PRESSURE_APPLICABLE_NOT_ACTUAL_EVENT` | `M2_HOUSEHOLD_CARE_PRESSURE_RULE` (pressure is never an actor event) |
| `mutual_aid_participation` | `POSSIBLE` | `POSSIBLE` | `M2_CIVIL_ROUTE_AVAILABILITY_RULE` (invariant alternative) |

Every entry: `epistemic_label=MODELED__NOT_OBSERVED__NOT_MEASURED`, `probability=null` with `NO_OPERATIVE_MODEL_USE_ISSUER__NO_MEASURED_ROUTE_PROBABILITY__NO_NUMERIC_IMPUTATION`, `non_response_state=UNKNOWN_NOT_MEASURED`, `type_belief_voice_state=UNKNOWN_NOT_ASSIGNED`, `minority_alternatives_preserved=true`, `route_probability_merging=FORBIDDEN_CROSS_GRAIN`.

Conditioner witnesses are unique per step (A: `W10CW:0f72e647…` C0, `W10CW:4da4152c…` C1, `W10CW:6e5533bb…` C2) and bind the exact premise values plus the subject selector (index `synthetic_eligibility_case_001`, age 14, year 2008).

### 2.3 Dyad firewall (AT34)

`requested_claim_grain=HOUSEHOLD_COPARENT_DYAD` → `dyad_claim_state=REFUSED_NO_HOUSEHOLD_SAMPLING_UNIT_AUTHORITY`, `dyad_sampling_unit_authority=ABSENT`, `household_unit_semantics=STRUCTURAL_PREMISE_ONLY__NO_GENERATED_PARENT__NO_DYAD_JOINT`, while `individual_possibility_state=PRODUCED_RETAINED` and the full three-stage route table is still produced.

## 3. Declared contrast and measured metrics

- **One** scientifically declared affordance/eligibility route change: `formal_schooling`, oracle `DIFFERENT_DUE_TO_ADMINISTRATIVE_AND_FEE_RULE`.
- Three constraint-grade changes (`nonformal_peer_study`, `paid_apprenticeship`, `family_care_work`) with route presence preserved in both variants (not eligibility removals).
- `minority_path_retention_exact: [5, 5]`; `unmeasured_probability_fraction_exact: [5, 5]` (all route probabilities null by law).
- `counterfactual_selectivity`: household-only variation leaves the institution rule untouched; institution-only variation leaves care routes untouched (`contamination: []` both directions).
- `actor_or_stereotype_leak_count: 0`; `semantic_currentness_integrity: 0`.
- `persona_quality_effect: TEST_HYPOTHESIS_NOT_MEASURED`; `source_backed_successor_quality: NOT_MEASURED__NO_SOURCE_OR_MODEL_USE_ISSUER`.

## 4. Hostile/oracle packet results (executed)

| Oracle | Expected | Observed | Pass |
|---|---|---|---|
| H01 promote modeled world to real country claim | `REJECT_REAL_WORLD_AUTHORITY_PROMOTION` | same | yes |
| H02 assign type/personality/belief from context | `REJECT_DIRECT_STATIC_TYPE_ASSIGNMENT` | same | yes |
| H03 cross-universe household/parent-child joint | `REJECT_UNLICENSED_DYAD_OR_RESPONSE_JOIN` | same | yes |
| H04 replace UNKNOWN with zero/exact probability | `REJECT_UNSUPPORTED_PRECISION` | same | yes |
| H05 historic anchors as observed structural change | `REJECT_UNISSUED_TEMPORAL_COMPARABILITY` | same | yes |
| H06 handwritten slice into N10E provider | `REJECT_HANDWRITTEN_PROVIDER_INPUT` | public API excludes slice input; `evidence=` kwarg → `TypeError: provide_empirical_possibility_slice() got an unexpected keyword argument 'evidence'` | yes |
| H07 mark fixture CURRENT / adopt issuer from prose | `REJECT_MISSING_CURRENTNESS_OR_ISSUER` | same | yes |
| H08 call V3 runtime / V2 renderer | `NO_ACTOR_RUN_OR_MODEL_INVOCATION` | same | yes |
| H09 erase surviving community support by class | `REJECT_MINOR_ROUTE_ERASURE` | same | yes |
| H10 nonlocal counterfactual contamination | `REJECT_NONLOCAL_COUNTERFACTUAL_CONTAMINATION` | `NO_NONLOCAL_CONTAMINATION_DETECTED` (both directions; contamination `[]`) | yes |
| wrong original unit | `WORLD_SUBJECT_UNIT_MISMATCH` | same | yes |
| wrong original year (2009) | `WORLD_AS_OF_YEAR_MISMATCH` | same | yes |
| revoked/never-granted scope uses | `WORLD_SCOPE_NOT_AUTHORIZED` | same | yes |
| M4 selected-service revoked-scope resolution | `RESOLUTION_DENIED_OR_NOT_APPLICABLE` | same (actual `resolve_v558` denial) | yes |

## 5. Replay / current-as-of / invalidation

- N10E cold replay: provider `replay_empirical_possibility_slice` + public `verify_positioned_subject_possibility_replay` reproduce lane hash `f1c033e6…`-bound identity; public consumer direct evaluation equals the provider's consumer result.
- Progressive receipt recompute: identical-context receipt replay hash reproduced (`e4a85143…`); world selection determinism reproduced on rebuild.
- Current-as-of: currentness receipt binds `urn:test:w10:as-of:2008`; the as-of ref is part of the RSC identity.
- Invalidation: `refresh_structural_currentness` creates a prospective successor (`M5CUR:74b40bf6…`) and the prior receipt hash is unchanged (history immutable); `materialize_resolved_structural_context` and `validate_resolved_structural_context` on the non-current successor both fail closed with frozen code `FAIL_CLOSED_ZERO_STRUCTURAL_PEER_EFFECT`; the consumer adapter refuses a non-current world with `WORLD_CURRENTNESS_NOT_CURRENT__NO_STALE_SELECTED_TRUTH`.

## 6. Non-results (explicit)

- No integrated N9/N10W production PASS; no operative N9 current token; no source or model-use issuer.
- No V3 actor execution; no V2 expressive rendering; model calls 0; original respondent SAV/DTA read 0.
- Persona-quality effect is a test hypothesis only.
- The J04 objective-position carrier remains unexercised (missing materializer boundary, §1.4).
