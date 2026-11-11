# PRE553 SUBSTRATE RECONSTRUCTION — SR02 R3 ADJUDICATION

Status: `ACCEPTED__LEGACY_RUNTIME_CONE_NONAUTHORITATIVE__PROVENANCE_CLOSED`

Frozen parent machine: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
SR02 execution HEAD: `4713aad8fb5f6dc9b5359c5a2eff11e3dfb1d524`
SR02 receipt size: `417137` bytes
SR02 receipt SHA-256: `c3e507f8661cd2f5e4cbfa5657499bd0426d6b29ea856259a29b6397df9c938a`
Completion token: `PRE553_SR02_CURRENT_DB_PROVENANCE_RECEIPT_COMPLETE`

## 1. Court holding

The current legacy Postgres runtime cone is populated and historically useful, but it is **not lawful source authority for the rebuilt machine**. The receipt and historical writer archaeology prove that runtime-critical carriers have multiple provenance layers, destructive source reductions, post-load mutations, source-identity transformations, and later authority/weight materializations.

No additional live-DB reconnaissance is required before substrate reconstruction. Future empirical truth must be rebuilt from exact source bytes plus governed authority; the legacy DB remains historical/parity evidence with explicitly bounded trust scopes.

## 2. Schema/runtime closure

R3 passed both embedded schema preflights before scanning data.

The frozen V550 runtime cone is confirmed live:

- `survey_microdata_respondents`;
- `survey_microdata_responses` transitively through the response-long view;
- `respondent_position_fact`;
- all 36 physical `respondentsDemo*` constituents of that view;
- `survey_weight_fact`;
- `respondent_source_wave_identity`;
- `question_structural_mapping`;
- `v_ddm_response_long_facet_ready`;
- optional `v_ddm_response_long_facet_ready_authority` + `survey_authority_compendium` override surface.

Peripheral tables such as `driver_aggregates` and old `respondents/responses` are not default V550 empirical ingress and remain static archaeology only.

## 3. Proven post-load response mutation — Mode A

R3 found `84698` `survey_microdata_responses` rows with **blank `dataset_id` and blank `source_file`**, written between `2026-07-20 03:18:58-04` and `2026-07-20 04:48:53-04`. Their respondent-ID envelope runs from `3877541` through `3994580`, inside the historical Afrobarometer R9 → Arab Barometer VIII ranges.

Historical writer archaeology identifies `backfill/backfill/run_mode_a_backfills.py` as the matching writer class:

- campaign root `authority_db_reconciliation/ar_20260719T213835Z`;
- direct `INSERT INTO survey_microdata_responses (respondent_id,var_code,value_raw,value_text)`;
- no `dataset_id` or `source_file` fields supplied;
- source targets include Afrobarometer R9 and Arab Barometer VIII;
- therefore inserted rows receive the later blank-provenance shape observed in R3.

The same writer contains the already-identified respondent-association defect: it filters a source variable to non-null rows and then enumerates that compressed frame against the full ordered DB respondent-ID list. When source missingness occurs before an observed value, later source values can shift onto earlier respondents.

Disposition:

`MODE_A_POSTLOAD_ROWS = RETAIN_AS_HISTORICAL_EVIDENCE__RESPONDENT_ASSOCIATION_NOT_TRUSTED`

No attempt will be made to repair these rows in place. Certified C11 reconstruction supersedes them.

## 4. Proven post-load Asian Barometer W6 mutation — Mode B

R3 separately records a later Asian Barometer W6 dataset route:

- dataset id `Asian Barometer W6`;
- blank `source_file`;
- `3224` respondents written around `2026-07-20 17:00-04`;
- `16120` response rows in the same route.

Historical `backfill/backfill/run_mode_b_backfills.py` explicitly creates absent W6 Japan/Malaysia/Singapore respondent routes and inserts response rows under dataset id `Asian Barometer W6` without source-file provenance. This matches the R3 shape.

W6 is `RECOGNIZED_EXCLUDED`, not CLOSED_35, under the accepted source-wave identity table. It remains historical evidence and is outside the governed 35-source reconstruction universe unless separately re-admitted.

Disposition:

`ASIAN_W6_MODE_B = RETAIN_AS_HISTORICAL_EVIDENCE__OUTSIDE_CLOSED_35`

## 5. LiTS I legacy respondent loss and country corruption

Cross-adjudication with SR03 proves the exact frozen `LiTS_I.dta` contains `29002` source rows. R3 shows only `28002` LiTS 2006 respondents in both `survey_microdata_respondents` and `respondentsDemoLiTS2006`.

Historical `reload_survey_microdata_cache.py` explains the discrepancy and a deeper corruption:

- for LiTS it chooses the numeric `country` column before `countryname`;
- the LiTS I raw file uses codes `1..29` with source-native meanings such as `2=Belarus`, `3=Bosnia`, `9=Moldova`, etc.;
- the historical `LITS_COUNTRY_NUMERIC` mapping is a different coding scheme (for example `2 -> AM`, `3 -> AZ`) and has **no entry for `9`**;
- unresolved numeric country values are rejected by `normalize_country_code`;
- LiTS I has exactly `1000` rows with raw `country=9` (Moldova), explaining the exact `29002 -> 28002` respondent deficit;
- many retained LiTS I rows were also assigned the wrong country code because the wrong numeric map was applied.

Therefore legacy LiTS 2006 country-conditioned empirical output is not trustworthy.

Disposition:

`LITS_2006_LEGACY_ROUTE = REBUILD_FROM_SOURCE__COUNTRY_MAPPING_INVALID__1000_SOURCE_RESPONDENTS_DROPPED`

No in-place repair is authorized.

## 6. Weight/materialization epochs

`survey_weight_fact` was materially loaded on `2026-08-18 00:58:30-04`, long after the May source ingestion. The table represents later operational primary-weight selection, not source-native estimand authority.

Likewise `respondent_source_wave_identity` and `question_structural_mapping` were loaded/materialized on August 18 from separate governance layers.

Disposition:

- DB `survey_weight_fact`: `COMPATIBILITY_ONLY__REBUILD_FROM_SOURCE_PLUS_WEIGHT_AUTHORITY`;
- DB `respondent_source_wave_identity`: `COMPATIBILITY_MATERIALIZATION__UNDERLYING_GIT_AUTHORITY_CONTROLS`;
- DB `question_structural_mapping`: `COMPATIBILITY_MATERIALIZATION__UNDERLYING_GIT_AUTHORITY_CONTROLS`.

## 7. Country identity repair

R3 records completed country-identity repair run `country_identity_repair_20260729T033706Z` with frozen crosswalk/source/repair/runner hashes and `164945` base/demo snapshot rows plus `512` response invariant rows.

These artifacts are useful historical provenance, but they do not supersede source-native row/country identity in C11.

Disposition:

`COUNTRY_IDENTITY_REPAIR = RETAIN_AS_HISTORICAL_EVIDENCE`

## 8. Runtime surface dispositions

| surface | disposition |
|---|---|
| `survey_microdata_respondents` | `REBUILD_FROM_SOURCE`; old table historical/parity evidence only |
| `survey_microdata_responses` | `REBUILD_FROM_SOURCE`; post-load Mode-A rows explicitly untrusted |
| `respondentsDemo*` | `REGENERATE_FROM_C11` if compatibility consumers remain |
| `respondent_position_fact` | `REGENERATE_FROM_C11` |
| `survey_weight_fact` | `REBUILD_FROM_SOURCE_PLUS_AUTHORITY`; DB materialization compatibility only |
| `respondent_source_wave_identity` | `COMPATIBILITY_MATERIALIZATION`; governing registry/artifact authority remains external |
| `question_structural_mapping` | `COMPATIBILITY_MATERIALIZATION`; frozen mapping authority remains external |
| `v_ddm_response_long_facet_ready` | `REGENERATE_FROM_C11` only if legacy compatibility still needs it |
| authority response-long override | `COMPATIBILITY_ONLY` |
| reload/build/repair progress tables | `RETAIN_AS_HISTORICAL_EVIDENCE` |
| W6 Mode-B route | `RETAIN_AS_HISTORICAL_EVIDENCE__OUTSIDE_CLOSED_35` |
| peripheral old aggregates/carriers | `NO_ACTION_REQUIRED_FOR_C11__STATIC_ARCHAEOLOGY` |

## 9. Closure law

Exact attribution of every historical row mutation is **not required** for the rebuilt empirical substrate once a runtime surface has a terminal nonauthoritative disposition and exact source reconstruction is mandatory. No unidentified writer may regain trust by default.

Any remaining per-source old-vs-new discrepancies are not free-floating SR02 investigations. They belong to the explicitly scheduled 35-source source-equivalence/certification wave at G-SR09.

G-SR02 is closed.

Token:

`PRE553_SR02_R3_ACCEPTED__LEGACY_RUNTIME_CONE_NONAUTHORITATIVE__PROVENANCE_CLOSED`
