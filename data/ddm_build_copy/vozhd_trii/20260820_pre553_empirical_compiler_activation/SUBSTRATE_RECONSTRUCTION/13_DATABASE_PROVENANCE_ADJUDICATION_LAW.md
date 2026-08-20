# PRE553 SUBSTRATE RECONSTRUCTION — DATABASE PROVENANCE ADJUDICATION LAW

Status: `FROZEN_BROWSER_AUTHORITY__AWAITING_SR02_PG_RECEIPT`

## 1. Governing rule

Legacy Postgres is evidence, not source authority. Every database surface relevant to the empirical machine must terminate in a named provenance/disposition ruling. Presence, population, timestamps, foreign keys, or downstream use do not by themselves establish source equivalence.

## 2. Surface classes observed in the supplied SQL schemas

### A. Historical respondent/response carriers

- `survey_microdata_respondents`
- `survey_microdata_responses`
- older `respondents`
- older `responses`

These surfaces may contain useful positive-value and source/wave evidence but require writer genealogy and source parity before any authoritative use.

Known structural limitations already visible in schema include:

- `survey_microdata_responses` stores one `(respondent_id,var_code)` response carrier and generic numeric/text values;
- it has no first-class source-native typed-absence/routing/topology fields;
- source path/dataset fields are not immutable byte identities.

### B. Named demographic/position convenience tables

- the 35 `respondentsDemo*` tables;
- `respondent_position_fact` union/derived view.

These are derived compatibility/conditioning surfaces, not raw source authority. Their fields may have undergone normalization, mapping, defaulting or post-load rebuild. They must be reproducible from certified source/C11 plus governed transformation authority before future authoritative use.

### C. Weight/design surfaces

- `survey_weight_fact`;
- weight columns copied into named `respondentsDemo*` tables.

Raw source weight/design variables must be recovered independently from source bytes. Existing named `is_primary` decisions are evidence of historical operational choice, not automatically source-native weight/estimand authority.

### D. Source/wave identity and repair surfaces

- `respondent_source_wave_identity`;
- `country_identity_repair_*`;
- reload/rebuild progress tables.

These are provenance/governance evidence and may be retained as historical authority artifacts if their exact generating authority is proven. They may not overwrite source snapshot/row identity.

### E. Question/canonical/mapping authority surfaces

Public schema examples:

- `questions`;
- `variables`;
- `question_structural_mapping`;
- `survey_authority_compendium`;
- `survey_authority_compendium_gap_log`.

Authority-reconcile schema examples:

- `canonical_question_registry`;
- `question_structural_mapping_provenance`;
- `question_structural_mapping_raw`;
- `question_variable_alias`;
- `survey_wave_alias`;
- canonical mapping view.

These are not raw empirical responses. They are candidate semantic/mapping/provenance authority surfaces. Each must be evaluated for exact authority source, version/hash, scope and whether it remains lawful under accepted PRE553 object/admission/source-plurality law.

### F. Derived analytical/compatibility products

- `driver_aggregates`;
- `respondent_position_fact`;
- `v_ddm_response_long_facet_ready`;
- `v_ddm_response_long_facet_ready_authority`;
- cubes/aggregates built by historical ETL scripts.

These are never source-equivalence or C11 authority. They may become compatibility or regression evidence and should normally be regenerated from certified C11 if still required.

The facet-ready views demonstrate why this distinction matters: they join generic responses to selected primary weight, normalized position facts, source/wave identity and structural mapping/authority in one convenience surface. That is operationally useful but semantically downstream of several separately governed transformations.

## 3. Writer-genealogy questions per surface

For every relevant table/view/materialization determine:

1. What script(s)/SQL could create, truncate, delete, insert, update, rebuild or replace it?
2. Which writer actually ran, if execution-history evidence exists?
3. What source bytes or upstream tables did that writer read?
4. Did it filter missing/user-missing rows?
5. Did it sort/filter/reindex before respondent association?
6. Did it normalize or overwrite source codes/labels?
7. Did it choose a default/primary weight?
8. Did it copy normalized demographics into convenience columns?
9. Did it infer source/wave/country identity?
10. Did it perform canonical/structural mapping?
11. Did later repair/backfill/rebuild code mutate the same rows?
12. Can its output be deterministically regenerated from retained source bytes + named authority?

## 4. Required terminal dispositions

Every surface ends as exactly one of:

- `REBUILD_FROM_SOURCE` — authoritative future content must be reconstructed directly from source-native bytes/authority;
- `REGENERATE_FROM_C11` — useful derived product, but future version must derive from certified C11;
- `COMPATIBILITY_ONLY` — retained only to compare old/new behavior or serve a temporary legacy consumer;
- `RETAIN_AS_EXTERNAL_AUTHORITY` — genuinely independent authority artifact whose provenance remains valid;
- `RETAIN_AS_HISTORICAL_EVIDENCE` — useful for archaeology/audit, not future semantic/runtime truth;
- `NO_ACTION_REQUIRED` — proven irrelevant to the empirical rebuild;
- `RETIRE_AFTER_SEPARATE_RETIREMENT_AUTHORITY` — obsolete only after exact consumers/equivalence are closed;
- `BLOCKED_<EXACT_REASON>`.

No unclassified surface may remain at G-SR10 closure.

## 5. Legacy parity law

Legacy DB values may be used as parity or forensic evidence only with a named trust scope, for example:

- positive raw-value parity for a source/variable range proven aligned;
- row-count comparison;
- historical mapping comparison;
- regression compatibility.

A trust scope may never silently expand. In particular:

- absence of a legacy response row is not evidence that the source respondent had no typed state;
- legacy respondent association is not trusted where a writer path can shift alignment until disproven by source-row parity;
- named weight status is not source-native estimand authority;
- structural/facet-ready convenience views are not empirical source truth.

## 6. SR02-PG adjudication output

When the live read-only receipt returns, HQ must join it to `LEGACY_WRITER_INVENTORY.csv` and `DATABASE_SURFACE_INVENTORY.csv` and emit a complete surface ledger with:

- surface name;
- surface class;
- known writers;
- observed current population/epoch evidence;
- source-equivalence trust scope;
- corruption/loss risk classes;
- required rebuild/regeneration action;
- terminal disposition or exact blocker.

G-SR02 closes only when no discovered relevant writer/surface remains outside that ledger.
