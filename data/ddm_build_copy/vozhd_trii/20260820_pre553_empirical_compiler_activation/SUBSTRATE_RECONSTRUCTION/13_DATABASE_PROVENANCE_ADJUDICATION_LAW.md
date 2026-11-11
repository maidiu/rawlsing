# PRE553 SUBSTRATE RECONSTRUCTION — DATABASE PROVENANCE ADJUDICATION LAW

Status: `FROZEN_BROWSER_AUTHORITY__RUNTIME_DEPENDENCY_CONE_TRACED__AWAITING_SR02_R3`

Frozen pre-reconstruction machine: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

Binding companion authority: `14_PRE_RECONSTRUCTION_DB_DEPENDENCY_MAP.md`.

## 1. Governing rule

Legacy Postgres is evidence, not source authority. Database existence does not imply runtime relevance, and runtime relevance does not imply source equivalence.

SR02 therefore distinguishes:

- `DIRECT_RUNTIME_V550`;
- `TRANSITIVE_RUNTIME_V550`;
- `DIRECT_AND_TRANSITIVE_RUNTIME_V550`;
- `CONDITIONAL_RUNTIME_OVERRIDE`;
- `PROVENANCE_ONLY`;
- `PERIPHERAL_LEGACY__STATIC_GENEALOGY_ONLY`.

Only a traced runtime dependency can block the rebuilt empirical machine merely because its current contents are defective. Provenance-only surfaces can block genealogy closure if they leave a material writer history unresolved. Peripheral legacy surfaces remain archaeological/compatibility evidence unless a separately proven consumer promotes them.

## 2. Frozen default V550 runtime dependency cone

### Direct runtime reads

- `survey_microdata_respondents`;
- `respondent_position_fact`;
- `survey_weight_fact`;
- `question_structural_mapping`;
- `v_ddm_response_long_facet_ready`.

### Transitive runtime inputs

- `survey_microdata_responses` through the response-long view;
- `respondent_source_wave_identity` through the response-long view;
- all 36 physical `respondentsDemo*` tables through `respondent_position_fact`;
- `survey_weight_fact` through the response-long view as well as direct readiness;
- `question_structural_mapping` through the response-long view as well as direct mapping/readiness.

The exact supplied current schema has **36** named `respondentsDemo*` tables. All 36 participate in `respondent_position_fact`. The accepted reconstruction source universe remains 35: Asian Barometer W6 is physically present in the historical database/view but excluded from the governed CLOSED_35 source universe.

### Conditional runtime overrides

Frozen code permits:

- `DDM_RESPONSE_LONG_RELATION` (default `v_ddm_response_long_facet_ready`);
- `DDM_QSM_RELATION` (default `public.question_structural_mapping`).

The current supplied schema includes `v_ddm_response_long_facet_ready_authority`, backed additionally by `survey_authority_compendium`. Those are conditional, not default, dependencies. Historical execution claiming an override must prove the configured relation from its own run provenance.

## 3. Runtime-critical carrier trust law

### A. `survey_microdata_respondents` / `survey_microdata_responses`

These are historical empirical carriers, not source authority.

Known limitations include:

- `survey_microdata_responses` has one `(respondent_id,var_code)` carrier;
- no first-class typed absence/routing/topology incidence;
- source path/dataset fields are not immutable byte identities;
- WVS source forensics already prove SPSS user-missing response events were omitted from the legacy carrier.

Positive-value or identity parity may be trusted only under an explicit source-scoped parity receipt.

### B. `respondentsDemo*` / `respondent_position_fact`

These are normalized/derived position carriers. They are runtime-critical historically because V550 conditions on `respondent_position_fact`; they are **not** raw-source authority.

Every position field must eventually be reproducible from certified source incidence plus governed transformation authority. Writer genealogy must determine whether post-load rebuilds, aliases, defaults or respondent-association defects touched these tables.

### C. `survey_weight_fact`

Historical `is_primary` choices are operational evidence, not automatically native sampling/estimand authority. Raw source weights/design variables must be recovered independently and future selection must be governed.

### D. `respondent_source_wave_identity`

This is identity/governance infrastructure used transitively by the current response-long view. It may lawfully map raw DB labels to governed source/wave identity but may not replace source-snapshot + source-row replay identity.

### E. `question_structural_mapping`

This is structural/mapping authority, not raw empirical response data. Its current population/version must be traced separately from empirical source parity.

### F. `v_ddm_response_long_facet_ready`

This is a convenience join and the historical V550 response ingress. It fuses multiple separately governed layers. It is never C11/source equivalence authority in its own right.

## 4. Provenance-only surfaces

These do not supply normal V550 empirical rows but may prove post-load mutation/rebuild history:

- `survey_microdata_reload_progress`;
- `ddm_inline_respondent_build_progress`;
- `ddm_named_respondent_demographics_progress`;
- `ddm_template_rebuild_progress`;
- `evs_loader_chunk_progress`;
- `country_identity_repair_runs`;
- `country_identity_repair_base_snapshot`;
- `country_identity_repair_demo_snapshot`;
- `country_identity_repair_response_invariants`.

They may establish that a runtime-critical surface was rebuilt or repaired. They may not authorize source values or semantics.

## 5. Peripheral legacy surfaces

The following remain in static writer/database archaeology but are not default frozen V550 empirical ingress:

- `driver_aggregates`;
- old `respondents` / `responses`;
- legacy `variables` / `questions`;
- historical cubes/aggregate products not referenced by the traced V550 ingress.

SR02 R3 does not spend live-scan budget on these surfaces. Their existence or defect alone cannot block C11 reconstruction without a separately traced consumer.

## 6. Schema-assumption prohibition

No SR02 execution payload may be launched until every relation/column referenced by that payload is reconciled against the exact supplied current schema artifact.

For R3, the exact external schema authority is:

`Rawlsing_WVS_public_schema(2).sql`

SHA-256:

`2c3f4a9ebec1e6c0cf62e8827ab982e52243c5c8899c961cd0e30b489573ec76`

Static R3 audit result:

- 155 explicit required relation/column pairs: `PASS`, zero missing;
- 36/36 `respondentsDemo*` tables: `PASS` for all fields used by `respondent_position_fact` plus provenance fields;
- V550-required `respondent_position_fact` columns: `PASS`;
- V550-required `v_ddm_response_long_facet_ready` columns: `PASS`.

Binding receipt: `SR02_SCHEMA_REFERENCE_AUDIT.csv`.

R3 additionally rechecks this contract against the **live** database before any large data scan. If live schema has drifted from the supplied contract, R3 stops immediately.

## 7. Writer-genealogy questions per runtime-critical surface

Determine:

1. Which script/SQL could create/truncate/delete/insert/update/rebuild/replace it?
2. Which writer actually ran, if execution evidence survives?
3. What source bytes/upstream relations did it read?
4. Did it suppress source/system/user-missing values?
5. Did it filter/sort/reindex before respondent association?
6. Did it normalize or overwrite source codes/labels?
7. Did it choose/default a weight?
8. Did it normalize demographics/coordinates?
9. Did it infer source/wave/country identity?
10. Did it perform canonical/structural mapping?
11. Did later repair/backfill/rebuild writers mutate the same surface?
12. Can future authoritative content be deterministically regenerated from exact source bytes + named authority?

## 8. Required terminal dispositions

Every relevant surface ends as exactly one of:

- `REBUILD_FROM_SOURCE`;
- `REGENERATE_FROM_C11`;
- `COMPATIBILITY_ONLY`;
- `RETAIN_AS_EXTERNAL_AUTHORITY`;
- `RETAIN_AS_HISTORICAL_EVIDENCE`;
- `NO_ACTION_REQUIRED`;
- `RETIRE_AFTER_SEPARATE_RETIREMENT_AUTHORITY`;
- `BLOCKED_<EXACT_REASON>`.

No runtime-critical or provenance-material surface may remain unclassified at G-SR10 closure.

## 9. Legacy parity law

Legacy DB values are parity/forensic evidence only under a named trust scope. A trust scope may never silently expand.

In particular:

- absence of a legacy response row is not evidence that no typed source state existed;
- respondent association is not trusted where a writer can shift source-row alignment until source parity disproves that risk;
- historical primary-weight status is not source-native estimand authority;
- facet-ready/position convenience views are not empirical source truth;
- peripheral legacy aggregates are not allowed to bootstrap C11 authority.

## 10. SR02-PG closure output

HQ joins the R3 live receipt to:

- `14_PRE_RECONSTRUCTION_DB_DEPENDENCY_MAP.md`;
- `SR02_SCHEMA_REFERENCE_AUDIT.csv`;
- `LEGACY_WRITER_INVENTORY.csv`;
- `DATABASE_SURFACE_INVENTORY.csv`.

The resulting adjudication ledger must state for every runtime-critical/provenance-material surface:

- dependency class;
- known writers;
- observed current population/epoch/view-fingerprint evidence;
- source-equivalence trust scope;
- corruption/loss risk classes;
- required rebuild/regeneration action;
- terminal disposition or exact blocker.

G-SR02 closes only when the actual pre-reconstruction runtime dependency cone and every material writer path into it are fully terminalized.
