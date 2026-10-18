# PYAT R35 T35 — two historical TEST_ONLY institutional-rule epochs to actual read-only E04 consumers; N8E absent/HOLD

**Worker terminal:** `TWO_EPOCH_TEST_ONLY_NATIVE_WORLD_CONSUMER_POSITIVE__N8E_ABSENT_HOLD`
**Role/ceiling:** bounded source-free native temporal-world executable worker. Not HQ, not EE12 source/method issuer, not Field Forge issuer, not Sorok actor.
**Sealed startup:** `5064d76b3c58a8225693055a8ec6bb07e216d9b1`
**Branch:** `agent/rabochii-pyat-r35-t35-historical-temporal-world-consumer-r1`
**Return:** only `WORKER_RETURNS/PYAT-R35-T35-TEMPORAL-WORLD-POSITIVE-R1/`
**Duplicate check:** direct remote branch was exactly the commission tip before work; no return directory and no running worker existed. No active worker was duplicated.

## 1. What was actually executed

The two epochs run the real sourcefree owner chain, not a new feasibility calculation:

```text
synthetic E04 source (base tag e04-base-r1)
→ pre553 empirical query / N10E / C1 / F8 progressive possibility
→ E04 GenericSelectedWorldService
→ M4 V557 publication + V558 repository exact resolution
→ M5 RSC currentness + validation
→ N9C two-field values reader (GSS/NCA TEST_ONLY fixture values)
→ original NONPARENT_OPTIONS consumer + original finite scenario-proposal consumer
```

Both epochs share the same empirical source and the same two consumers. Only the synthetic institutional rules differ. The rules are published through the E04 catalog's own `_publish` method; no owner source byte was edited. The epoch-2 `training_fee=6` / `exit_cost=8` revision is a **new TEST_ONLY rule extension** created at the owner's publish boundary, not a rule that pre-existed in E04.

Pinned byte identities: 26 frozen closure pins all match; 53 imported modules are recorded with Git blob SHA-1 and SHA-256. Sealed M4/M5/empirical/query modules are from `5064d76`; the E04 product package is the exact R10 blob set, the E05R adapter the exact R13 blob, and the N9C reader/fixture the exact HQ297 blobs. All pinned preimages match in `02_PINNED_NATIVE_TEMPORAL_IMPORTS_AND_JUNIT/import_preimages.json`.

## 2. Two epochs — actual consumer-visible result

| | E1 early 2026 | E2 late 2027 |
|---|---|---|
| clock | `AS_OF` valid `2026-06-01`, as-of `2026-04-15` | `TEST_CURRENT` valid=as-of=test-now `2027-09-01`; `operative_CURRENT=False` |
| selected rule | rev 1: effective `2026-01-01`, published `2026-03-01` | fee/exit rev 2: effective `2027-01-01`, published `2027-06-01` |
| `training_access` (formal eligibility) | **true** | **true** |
| `training_fee` (material tokens) | 2 | 6 |
| `exit_cost` (material tokens) | 2 | 8 |
| `civil_open` / `civil_sanction` | true / false | true / false |
| `NONPARENT_OPTIONS` training | `ELIGIBLE` | `BLOCKED_BY_MODELED_RULE` |
| `NONPARENT_OPTIONS` exit | `WITHIN_MODELED_BUDGET` | `RESOURCE_CONSTRAINED` |
| `NONPARENT_OPTIONS` civil | `ELIGIBLE` | `ELIGIBLE` (null) |
| scenario proposals (institutional/civil) | `FEASIBLE` / `FEASIBLE` | `FEASIBLE` / `FEASIBLE` (null) |
| empirical steps | 18/32 → 10/16 → 6/8 | identical |
| source-balance counts | 4, 4, 4 | identical |
| receipt state | `SELECTED_WORLD_VALUES_SERVED` | `SELECTED_WORLD_VALUES_SERVED` |
| receipt SHA-256 identity (semantic hash) | `4b592251…0459ae2` | `d29f2aab…c595951` |

**The scientific positive:** a changed material constraint changes the actual read-only consumer's practical opportunity while formal training eligibility remains true. The fixed consumer budget is 5 modeled tokens; the fee rises from 2 to 6 and the exit cost from 2 to 8. The `NONPARENT_OPTIONS` client therefore moves from `ELIGIBLE`/`WITHIN_MODELED_BUDGET` to `BLOCKED_BY_MODELED_RULE`/`RESOURCE_CONSTRAINED`.

**The legitimate nulls are explicit, not failures:**
- the civil route is unchanged (`ELIGIBLE` → `ELIGIBLE`) because `civil_open` and `civil_sanction` are unchanged;
- the finite proposal evaluator is unchanged (`FEASIBLE` → `FEASIBLE`) because that original client reads only `training_access`, not fee or exit cost. This is a genuine consumer-grain limitation, not a claim that affordability is irrelevant;
- the empirical possibility steps and source-balance counts are identical because the rule-only change does not touch source, release, risk set or rows.

## 3. Formal eligibility isolated from material affordability

A same-clock control at E2 (`2027-09-01`, fee and exit fixed at 2) flips only `training_access` to false:

| control `training_access=true`, fee=2 | formal rule `training_access=false`, fee=2 |
|---|---|
| training `ELIGIBLE` | training `BLOCKED_BY_MODELED_RULE` |
| institutional proposal `FEASIBLE` | institutional proposal `INFEASIBLE` |
| civil `ELIGIBLE` | civil `ELIGIBLE` |
| empirical steps identical | empirical steps identical |

Thus the epoch-1/epoch-2 change is not a formal-eligibility change; the separate control changes formal eligibility with material constraints held fixed. The two effects are distinct.

## 4. Effective / publication / requested as-of

The clock cross-product executes the same rule store under different requested knowledge times:

| valid_at | published_as_of | fee | exit | training | interpretation |
|---|---|---|---|---|---|
| 2027-09-01 | 2027-05-31 | 2 | 2 | `ELIGIBLE` | rev 2 is effective but not yet published; known-at selection keeps rev 1 |
| 2027-09-01 | 2027-06-01 | 6 | 8 | `BLOCKED_BY_MODELED_RULE` | publication boundary admits rev 2 |
| 2026-06-01 | 2027-09-01 | 2 | 2 | `ELIGIBLE` | later as-of does not retroactively apply a rule not effective at valid_at |
| 2027-01-01 | 2027-06-01 | 6 | 8 | `BLOCKED_BY_MODELED_RULE` | exact effective boundary |
| 2026-12-31 | 2027-09-01 | 2 | 2 | `ELIGIBLE` | one day before effective boundary |

This is the frozen retroactive-publication/effective-time separation: the rule takes effect `2027-01-01` but is published `2027-06-01`, so the requested as-of time controls what a consumer could have known. An additional `AS_OF` control at `2027-09-01` selects the same late institutional rule as `TEST_CURRENT`, with `operative_CURRENT=False`, so the late epoch is not an artifact of an operative-present clock.

## 5. Historical immutability, replay and revocation

- **Historical immutability:** re-serving E1 after E2 on the same adapter returns the byte-identical E1 receipt (`4b592251…`); a retrospective `AS_OF` query at E1's valid time still resolves the early rule. Old receipts are retained in `historical_receipt()` with `archival_only=true`, `fresh_use_authorized=false`.
- **Cold replay:** two fresh child processes (PIDs `31393`, `31397`) executed the complete product independently; both exited 0 and produced byte-identical 1,099,273-byte JSON with SHA-256 `c4697da7e08a6920d2208e46274a0bab122ecdd334249f6268875625ea2f857b`. The product contains no wall clock, PID or absolute host path.
- **Selective structural revocation:** revoking `civil_sanction` yields `TYPED_PARTIAL_SELECTED_WORLD`; the civil route becomes `UNAVAILABLE_AUTHORITY_OR_CLOCK`, while training remains `ELIGIBLE` and exit remains `WITHIN_MODELED_BUDGET`. The old receipt is invalidated for fresh use and retained as history.
- **Selective non-contamination:** revoking `training_fee` leaves a civil-only receipt unaffected and still `SELECTED_WORLD_VALUES_SERVED`, while a full fresh receipt has training `UNAVAILABLE_AUTHORITY_OR_CLOCK`.
- **Native field revocation:** revoking `GSS_RURAL_LIGHTING` leaves the native readset `PARTIAL_TEST_ONLY_NOT_POSITIVE` with only `NCA_NATIONAL_MOBILE_DATA` and a typed `SOURCE_REVOKED` refusal; the world receipt is `TYPED_PARTIAL_SELECTED_WORLD`.

## 6. Source versus selected-world mismatch

All four hostile paths are refused by the owner code, not papered over:

| substitution | actual refusal |
|---|---|
| snapshot from a different source world accepted by another world | `ValueError: UNREGISTERED_SELECTED_SNAPSHOT` |
| acceptance from world A served with world B | `SelectedWorldInconsistency: ACCEPTANCE_BINDING_MISMATCH` |
| epoch-1 acceptance with epoch-2 snapshot | `SelectedWorldInconsistency: ACCEPTED_SNAPSHOT_SUBSTITUTION` |
| rehashed caller snapshot with forged source root | `ValueError: UNREGISTERED_SELECTED_SNAPSHOT` |

A 2×2 source/rule court separates the two causes:

- **rule-only change** (base E1 → base E2): empirical steps identical, structural routes changed;
- **source-only change** (base E1 → changed-source E1): structural routes identical, empirical steps change (18/32→19/32, 10/16→11/16, 6/8→7/8; source-balance 4→6);
- **both:** both change.

No source/selected-world mismatch was silently repaired, and no source change was used to fake a rule change.

## 7. N8E / EE12 — separate, absent and HOLD

The N8E Ghana input is **not** part of the world root, the M4 catalog, either consumer, or the selected-world receipt. It is an envelope-level `ABSENT_HOLD` with null numeric fields:

```json
{"state":"ABSENT_HOLD","claim_id":"N8E_GHA_R5Q43_R9Q31_DSAT_R1",
 "actual_result_state":"HELD_UPSTREAM_EVIDENCE_AND_ISSUANCE",
 "numeric_delta":null,"measured_no_change":null,
 "world_input":false,"m4_root_input":false,"consumer_input":false,
 "n9_installation_state":"NOT_INSTALLED_HOLD"}
```

The separate source-free comparator court (`runtime/n8e_sourcefree_comparator.py`) accepts only explicitly `HYPOTHETICAL_` receipts. It reproduces N03/EE12 admissibility expectations:

- five substantive categories `{0,1,2,3,4}` including `0` are preserved;
- R5 `998` refusal and R9 `8` refusal remain typed and are never merged into `0`;
- the estimator is the design-weighted ratio, never unweighted raw counts;
- missing EE12 → `HOLD_EE12_ISSUER`; missing science → `HOLD_SCIENCE`; missing design variance → `UNQUANTIFIED_DESIGN_UNCERTAINTY`; dependent waves without covariance → `HOLD_COVARIANCE`; zero denominator → `ZERO_SUPPORT` (delta null); interval including zero → `INCONCLUSIVE_WITH_INTERVAL` (never `NO_CHANGE`); no-change only under a predeclared margin; noncomparability only with a positive necessary-condition conflict; missing `0` → `CATEGORY_TOPOLOGY_MISMATCH`; special-code laundering refused; IID/headline variance refused; source-version change → `STALE_SOURCE_INVALIDATED`.

The only numeric delta in this return is the explicitly hypothetical arithmetic check (`p_A=0.5`, `p_B=0.7`, `Δ=0.2`, SE `0.07810249675906655`, interval `[0.04691910635222957, 0.35308089364777046]`). It uses fabricated wave labels, is labelled `HYPOTHETICAL_MEASURED_INCREASE`, and is not an N8E product, not Ghana, and carries no issued EE12 authority.

The full N03/Ghana pending-owner record is `04_GHANA_EE12_EXACT_PENDING_OWNER_RECORD.md`.

## 8. Historical V553 candidate-method evaluation

The actual sealed V553 implementation (`data/ddm_build_copy/ddm_v553_temporal_pressure.py`, blob `5304b70f…`) was imported and executed against empty input. It returns **45 typed readiness errors** beginning `V553 thin temporal pressure layer missing packet path` and ending `…missing harmonization_score`; the harmonization report returns `STATUS: V553_WAVE_HARMONIZATION_SCAFFOLD_ONLY_SINGLE_WAVE`, `comparability_status=comparability_limited`, `comparison_authority_status=insufficient_multi_wave_authority`, `multiple_waves_present=false`, `blocking_conditions=[at_least_two_waves, one_explicit_survey_family_and_country, shared_semantic_directionality_and_position_signal_columns, wave_specific_certified_authority_rows]`.

V553 is a **structural** temporal-pressure/harmonization producer. It does not consume respondent survey rows, five-category satisfaction, design weights/PSU/strata or produce a survey-wave delta. Candidate verdict: `V553_STRUCTURAL_TEMPORAL_HARMONIZATION_CANDIDATE__NOT_N8E_SURVEY_COMPARATOR`; reuse is structural-only and creates no Ghana/N8E authority.

## 9. Tests, imports and evidence

- **183 JUnit test events, 0 failures, 0 errors, 0 skips:** 41 new frozen world/N8E cases; 30 original sealed M4/M5; 75 original sealed empirical chain; 37 original E04 author court. This is pytest JUnit XML, not Java; the repository has no Java test target. Test events are implementation/regression observations, not independent scientific acceptance decisions.
- **Native owner calls actually observed:** 5,178 `m4.resolve_v558`; 1,320 `m4.build_v557_publication_bundle`; 1,540 `m4.build_v558_repository_bundle`; 642 `m5.make_structural_currentness_receipt`; 214 `m5.materialize_resolved_structural_context`; 642 `m5.validate_resolved_structural_context`; 384 progressive empirical steps; 44 world selects. Counts are cumulative profiled call events across all serves, not a claim of unique semantic operations.
- **Exact preimages:** 26 pins, all matching; 53 imported modules with Git blob and SHA-256; no absolute host path in the product.
- **Cold replay:** two independent child processes, byte-identical, SHA-256 `c4697da7e08a6920d2208e46274a0bab122ecdd334249f6268875625ea2f857b`.
- **Sanitized passport:** `environment_passport.json`.

## 10. What is not claimed — controlling limits

1. The institutional rules are **synthetic TEST_ONLY**, not observed Ghana, US, historical or current institutions. The resource tokens are modeled, not money.
2. The empirical chain is the synthetic E04 source, not original survey data. No SAV/DTA, respondent row, original file, private row or external source was read.
3. The N9C GSS/NCA field values are **TEST_ONLY fixture numerics** consumed under the exact N9C reader. They are not issued N5/N6, EE13, real OC05, a source custody proof or an installed N9 field.
4. No **N8E product**, no **N9 installed historical context**, no **N10W** structural-route model or use, no **N8S** structural authority, no **EE12** issuance, no **Field Forge** semantic issuance, no **N11/N12/V3** permission and no **Sorok actor** is created.
5. The N8E hypothetical comparator is a specification court. The hypothetical delta is arithmetic-only and is not a measurement, trend, no-change finding or interval about Ghana or any population.
6. The scenario evaluator's unchanged feasibility under the fee/exit change is a client-grain null, not evidence that material affordability is institutionally irrelevant.
7. This is a worker return. No HQ adoption, independent review or production installation is claimed. The WP2/WP2I selected-world and E04 chain is reused as accepted sourcefree method capital; this return does not re-adopt it.

## 11. Exact remote SHA

The branch tip after push is reported in the final chat return and is verifiable by direct `git ls-remote origin refs/heads/agent/rabochii-pyat-r35-t35-historical-temporal-world-consumer-r1`. The published evidence manifest is `artifact_manifest.json`; this document is committed in the same evidence commit.

**No original35, U/E_pre, Field Forge, EE12, N9, N10W, N11/N12 or Sorok permission is issued by this work.**
