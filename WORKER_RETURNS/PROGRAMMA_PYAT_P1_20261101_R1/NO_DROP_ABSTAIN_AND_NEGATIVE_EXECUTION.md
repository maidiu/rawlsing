# No-drop, abstain and negative execution

**Sourcefree only.** Every fault below is synthetic input metadata. No survey
byte, respondent row, native P07 or original source right was read.

## 1. Positive no-drop baseline

| Property | Value |
|---|---:|
| Waves | 35 |
| Items | 70 |
| Compiled operations | 840 |
| Batch units | 840 |
| Holds | 0 |
| Abstentions | 0 |
| Wave E_pre roots | 35 |
| Duplicate operation refs | 0 |
| `no_drop_ok` | True |

Each wave contributes 24 operation records: 3 distribution for item A; and for
item B, 3 distribution + 6 conditional + 6 joint + 3 heterogeneity + 3 recursive.
No operation is generated from an observation value; operations are prospective
and outcome-independent.

## 2. Fault matrix

| Fault | Exact result | Batch units | Receipt |
|---|---|---:|---|
| 34 waves | `INDEPENDENT_ORIGINAL35_ROSTER_REQUIRED` | 0 | `test_thirty_four_waves_are_refused` |
| Duplicate atlas/wave identity | `INDEPENDENT_ORIGINAL35_ROSTER_REQUIRED` | 0 | `test_duplicate_wave_is_refused` |
| Duplicate item ref | `DUPLICATE_ITEM_REF` | 0 | `test_duplicate_item_ref_is_refused` |
| Missing source grant, one wave | 24 HOLD `SOURCE_GRANT_ABSENT`, 816 compiled | 816 | `test_missing_source_grant_is_typed_hold_and_still_no_drop` |
| Wrong source SHA, one wave | 24 ABSTAIN `SOURCE_SHA_MISMATCH`, 816 compiled | 816 | `test_wrong_source_sha_abstains_only_that_wave_and_restores` |
| Stale source grant | 24 HOLD `SOURCE_GRANT_NOT_CURRENT` | 816 | `test_stale_source_grant_is_typed_hold` |
| Missing item registry | 24 HOLD `ITEM_REGISTRY_REF_ABSENT` | 816 | `test_missing_item_registry_is_typed_hold` |
| Missing route, item A | 3 HOLD `ROUTE_REF_ABSENT` | 837 | `test_missing_route_is_typed_hold_and_restores` |
| Missing weight, item A | 3 HOLD `WEIGHT_REF_ABSENT` | 837 | `test_missing_weight_is_typed_hold` |
| Respondent eligibility mismatch, item B | 21 ABSTAIN `RESPONDENT_ELIGIBILITY_MISMATCH` | 819 | `test_respondent_eligibility_mismatch_is_typed_abstain` |
| Missing conditional binding | 1 HOLD `CONDITIONER_BINDING_ABSENT`, 6 conditional slots unenumerated | 834 | `test_conditional_binding_absence_is_typed_hold_not_silent_drop` |
| False native/proxy measurement under direct method | 3 HOLD `MEASURE_NOT_IN_SOURCE_GRANT` | 837 | `test_false_native_measurement_is_typed_hold` |
| Proxy method without owner/authority | 840 HOLD `SCIENTIFIC_METHOD_OWNER_ABSENT` | 0 | `test_proxy_method_requires_owner_and_authority` |
| All 35 waves source-held | 840 HOLD, no BatchManifest | 0 | `test_all_held_has_no_batch_manifest_and_no_drop` |

All fault plans keep `no_drop_ok=True` when the wave roster is valid and every
admitted item/operation class is represented by a compiled, HOLD or ABSTAIN
record. A missing conditional binding cannot invent 6 conditioner-value
combinations; one typed HOLD accounts for the unenumerated class and the batch
count is 834, not 839.

## 3. Named positive/restore assertions

`test_wrong_source_sha_abstains_only_that_wave_and_restores`:

- baseline: 840 compiled units;
- mutated wave 0 source SHA: exactly 24 ABSTAIN records and 816 compiled units;
- restore: 840 compiled units and a different `plan_ref` from the mutation;
- the other 34 waves remain compiled.

`test_missing_route_is_typed_hold_and_restores`:

- baseline: 840 units;
- mutated item A route: 3 HOLD records, 837 units;
- restore: 840 units and a different `plan_ref`.

These are receiving assertions on the exact operation status and batch count,
not generic exception checks.

## 4. Batch boundary

Only `STATUS_COMPILED` operations receive a `batch_job_ref`. HOLD and ABSTAIN
records have `batch_job_ref=None` and never enter `BatchManifest`. The positive
and all-held tests assert this boundary.

## 5. What is not proven

- no real C11/I03/I05 execution;
- no measured distribution/conditional/joint;
- no original-source route/weight/respondent eligibility;
- no actual all35 occupancy;
- no N9/N10W/N11/N12 product.

The negative court is a sourcefree construction/refusal court, not a scientific
result or an all35 populated claim.
