# REC-07X — EXACT 588-ROW R10F O03 SUCCESSOR AUTHORING COURT

Status: `ISSUED__EXACT_588_ROW_DOCKET__NO_SELF_EXPANSION__HQ_ADOPTION_REQUIRED`

Repository: `maidiu/rawlsing`

Execution environment: Browser / connected GitHub. Container/Python may be used for deterministic CSV joins and validation. No local Mac archaeology and no survey-binary execution are required.

## 0. Mission

Author exactly one append-only same-grain R10F O03 response-topology successor record for each of the **588 additional source-proved REC-05X candidate rows**, and nothing else.

This is not an evidence-discovery court. The evidence court is already complete.

## 1. Preflight

Before substantive work:

1. verify assigned worker branch and exact starting HEAD supplied in the handoff;
2. read `HQ/HQ_REC05X_REC07_INTAKE_AND_ADOPTION.md`;
3. fetch REC-05X immutable worker HEAD `29cf12dd91cf644c234239e5782cb7544f8c5898`;
4. fetch at that exact HEAD:
   - `returns/REC-05X/SUCCESSOR_CANDIDATE_LEDGER.csv`;
   - `returns/REC-05X/README.md`;
   - `returns/REC-05X/SOURCE_LIMITED_LEDGER.csv`;
5. verify `SUCCESSOR_CANDIDATE_LEDGER.csv` blob SHA is exactly:
   `8865ef9080230733a4cfac3c13cea4e5f56b1330`;
6. verify the frozen R10F authority identity from REC-05X:
   `R10F_S2_CENTRAL_INTEGRATED_AUTHORITY.csv`
   SHA-256 `f593caa27f3eb9a7e49ff819626dc5294c6e7031748e74914aefc18f27b011d5`;
7. do not proceed if any identity check fails.

If an exact immutable input is unreachable, return `BLOCKED__EXACT_INPUT_NOT_REACHABLE` and do not substitute a nearby file.

## 2. Exact denominator construction

The REC-05X candidate ledger must contain exactly 613 data rows.

Partition it by `rec07_exact_o03_overlap`:

- `TRUE` = exactly 25 rows;
- `FALSE` = exactly 588 rows.

REC-07X denominator is exactly:

`all rows where rec07_exact_o03_overlap == FALSE`

Required denominator assertions:

- rows = 588;
- duplicate candidate rows = 0;
- all `CANDIDATE_ONLY__NOT_INSTALLED` = 1;
- all `S1_SPECIAL_STATES_PRESERVED` = 1;
- no `TRUE` overlap row enters the denominator.

Write `returns/REC-07X/DENOMINATOR_REPLAY_RECEIPT.json` before authoring successors.

If any assertion fails, STOP with:

`REC07X_BLOCKED__DENOMINATOR_REPLAY_MISMATCH`

## 3. Join law

For each of the 588 candidate rows:

1. use `r10f_data_row` only as a locator inside the SHA-pinned frozen R10F CSV;
2. resolve the exact frozen R10F row;
3. recover its exact governed `question_implementation_id` and current O03 assertion;
4. verify the candidate's `source_variable_code` matches the frozen row;
5. expand `source_proved_topology_code` using the exact REC-05X README codebook;
6. expand `defect_code` using the exact REC-05X README defect codebook;
7. preserve all source-special states outside substantive topology.

`r10f_data_row` is not semantic precedence and numeric response code order is not semantics.

Do not identify rows by variable code alone. Same-looking variable labels across waves/families must remain distinct governed implementation identities.

Write one row per candidate to:

`PREDECESSOR_JOIN_LEDGER.csv`

Required columns:

- `r10f_data_row`
- `question_implementation_id`
- `source_family`
- `wave`
- `source_variable_code`
- `frozen_predecessor_topology_assertion`
- `source_proved_topology_code`
- `source_proved_topology_expanded`
- `defect_code`
- `defect_class_expanded`
- `source_evidence_locator`
- `special_state_preservation`
- `join_status`

Every `join_status` must equal:

`EXACT_PREDECESSOR_AND_SOURCE_PROPOSITION_JOINED`

If even one row cannot be joined exactly, do not invent its successor. Mark that row blocked, report the exact count, and keep all independent exact rows separate.

## 4. Successor authoring law

For every exactly joined denominator row, author one record in:

`SUCCESSOR_RECORDS_O03.csv`

Required fields:

- `record_id`
- `predecessor_id`
- `predecessor_surface`
- `predecessor_evidence_identity`
- `old_assertion`
- `new_assertion`
- `fields_changed`
- `fields_preserved`
- `special_negative_state_handling`
- `successor_relation`
- `reason_code`
- `replay_impact`
- `status`

Required values/law:

- `predecessor_surface = R10F_O03`;
- `fields_changed = response_topology` only;
- `successor_relation = APPEND_ONLY_SAME_GRAIN_SUCCESSOR`;
- `status = CANDIDATE_SUCCESSOR__PENDING_HQ_ADOPTION`;
- `new_assertion` must be the expanded source-proved topology from REC-05X, preserving its non-interval/non-scalar qualification where present;
- all special DK/refusal/IAP/not-asked/nonresponse/routing states remain outside substantive topology unless REC-05X explicitly proved otherwise;
- preserve exact implementation identity, source family, wave, variable, question/stem/child identity, labels, source locator and unrelated semantic/routing fields.

## 5. Absolute prohibitions

REC-07X must not:

- author any of the 25 `rec07_exact_o03_overlap == TRUE` rows;
- author any of the three EVS-2008 SIOPS source-limited rows;
- author any of the 2,268 REC-05X pass rows;
- modify R10G, QRA, O07, O08, O09, SWID, routing, source, runtime or compiler authority;
- infer polarity/directionality from ordered topology;
- infer interval distance from ordered categories;
- infer semantics from numeric response code order;
- turn rank-position language into ranking unless source proves respondent-supplied rank positions;
- turn a single top-selection into a ranked response;
- turn a binary state into a tradeoff;
- convert a tradeoff into a scalar merely because it has two sides;
- create new evidence or broaden the denominator.

## 6. Exact cardinality expectations

Normal successful terminal state requires:

- denominator rows = 588;
- exact predecessor joins = 588;
- successor records = 588;
- duplicate predecessor IDs = 0;
- overlap with REC-07 adopted 25-row O03 set = 0;
- overlap with source-limited SIOPS 3-row set = 0;
- overlap with REC-05X pass set = 0.

If any row is blocked by an exact predecessor-join failure, the court may return partial authoring, but it must not hide the shortfall. The expected successful count remains 588.

## 7. Required outputs

Write only under:

`.../AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/returns/REC-07X/`

Required files:

1. `README.md`
2. `DENOMINATOR_REPLAY_RECEIPT.json`
3. `PREDECESSOR_JOIN_LEDGER.csv`
4. `SUCCESSOR_RECORDS_O03.csv`
5. `EXCLUSION_AND_DEDUPLICATION_RECEIPT.json`
6. `REPLAY_AND_REGENERATION_IMPACT.md`
7. `HQ_ADOPTION_CANDIDATE.md`
8. `CHANGED_FILES.txt`

No writes outside this return root.

## 8. Final validation

Before sealing:

1. compare exact start HEAD to final worker HEAD;
2. assert behind = 0 and exact start is merge base;
3. assert every changed path is under `returns/REC-07X/`;
4. assert denominator count;
5. assert predecessor-join count;
6. assert successor count;
7. assert exclusions 25 / 3 / 2,268 were respected;
8. assert no canonical/runtime/source mutation;
9. assert all successor statuses are pending HQ adoption.

## 9. Terminal returns

Successful:

`REC07X_COMPLETE__588_EXACT_O03_SUCCESSORS_AUTHORED__HQ_ADOPTION_REQUIRED`

Partial only because exact predecessor joins failed:

`REC07X_PARTIAL__EXACT_JOIN_BLOCKERS_PRESERVED__NO_GUESSED_SUCCESSORS`

Input/denominator failure:

`REC07X_BLOCKED__EXACT_INPUT_OR_DENOMINATOR_MISMATCH`

Stop token:

`REC07X_O03_ADDITIONAL_SUCCESSOR_REPAIR_RETURNED`
