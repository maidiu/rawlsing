# D05 — Populated Empirical Substrate Reality Court

## VERDICT

`BLOCKED_MISSING_POPULATED_DATA_ACCESS`

## AUDIT APPARATUS

`CLOSED_EXECUTABLE_NOT_RUN_AGAINST_POPULATED_DATA`

Those are deliberately separate findings.

D05 still cannot lawfully adjudicate the actual populated empirical substrate in this worker environment because no live populated PostgreSQL database and no exact transactionally consistent production-equivalent populated snapshot are available. Therefore D05 makes **no** claims about actual respondent counts, overlap rates, position completeness, weight coverage, routing prevalence, question topology prevalence, join success, facet-row preservation, cache losslessness, or source equivalence.

But the first return was itself inadequate. A fail-closed court cannot answer a missing-data blocker with an underspecified wish list. The audit machinery required to resolve the blocker is now closed and executable.

## SUPERSESSION OF THE FIRST RETURN

The first D05 result is superseded in three material respects:

1. It recorded incorrect SHA256 values for `Rawlsing_WVS_public_schema.sql` and `Rawlsing_WVS_authority_reconcile_schema.sql`.
2. It referred to an `AUDIT.sql` and `EXPECTED_OUTPUT_SCHEMAS.json` execution kit that had not actually been created.
3. It did not provide a worker-executable, fixed-semantics audit sufficient to complete the court without making new semantic decisions.

The corrected evidence identities from `evidence/conversation_inputs/SHA256SUMS.txt` are:

- `Rawlsing_WVS_public_schema.sql` — `2c3f4a9ebec1e6c0cf62e8827ab982e52243c5c8899c961cd0e30b489573ec76`
- `Rawlsing_WVS_authority_reconcile_schema.sql` — `57e8c58c9444be9c34df54765e1801a9819f7a15fd02ddaa9a8e194e57596877`
- `rawlsing_v5_ddm_production_continuation_pack_v2_ATTITUDE_CLOUD_LOCKED.zip` — `e9c66a9638371966d620ef73c30f03c5dcca255cd874acbdf66e3738654b5861`
- `rawlsing_v5_home_stretch_build_pack_v18_FINAL_LOCKED_NO_GHOSTS.zip` — `a654014fb56032544fc4044ee230cf69823e076cb5f3e4fc3df91eb3148f12bd`
- `rawlsing_chatlog_DDM_chatgpt_1.txt` — `b0ff181b0d1f6a591b005b829aafeb27b0740249332b49e08bd381800ab1745a`

At execution time the audit hashes the checked-in static evidence itself and records both SHA256 and Git blob identity. A mismatch against a locked external-evidence identity is a fatal `D05_E_STATIC_PROVENANCE_MISMATCH`, not a warning.

## CANONICAL EXECUTION — ZERO SEMANTIC CHOICES

A worker with database access runs exactly:

```bash
DATABASE_URL='postgresql://USER:PASSWORD@HOST:PORT/DBNAME' \
  bash data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/courts/D05/run_d05_empirical_audit.sh
```

No source, wave, country, question, position field, overlap subset, authority lane, response relation, or cache scope is supplied by the worker.

The execution stack is:

- `D05_AUDIT_CONTRACT.json` — normative relation/column contract, output schemas, invariants, failure codes, source-equivalence bar;
- `run_d05_empirical_audit.sh` — canonical no-choice entrypoint;
- `run_d05_empirical_audit.py` — core populated relational audit;
- `audit_d05_output_semantic_guard.py` — prevents non-exposed fields from being mislabeled as preserved;
- `audit_d05_authority_scope_cache.py` — production-R1, canonical-registry, governed-scope, and materialized-cache audit;
- `EXECUTION_KIT.md` — operator contract and exact grains.

Both database runners independently establish PostgreSQL `REPEATABLE READ, READ ONLY` transactions and verify `transaction_read_only = on`. They contain no database repair or mutation path. Their only outputs are files under this D05 directory.

## EXACT PHYSICAL RELATION CONTRACT

Fatal core relations and columns are:

### `public.survey_microdata_respondents`

- `id`
- `source`
- `wave`
- `country_code`
- `survey_year`

### `public.survey_microdata_responses`

- `respondent_id`
- `var_code`
- `value_raw`
- `value_text`

The following are mandatory audit targets but non-core absence is itself measured and emitted rather than silently substituted:

- `public.survey_weight_fact`
- `public.respondent_position_fact`
- `public.question_structural_mapping`
- `public.survey_authority_compendium`
- `public.v_ddm_response_long_facet_ready`
- `public.v_ddm_response_long_facet_ready_authority`
- `public.ddm_demographic_field_register`

The exact required/expected columns for every relation are fixed in `D05_AUDIT_CONTRACT.json` and duplicated as executable constants in the runner.

For authority-reconciliation surfaces, the apparatus discovers `canonical_question_registry` by relation name across schemas. Exactly one installed schema is allowed. Zero installed schemas emits `D05_W_CANONICAL_REGISTRY_NOT_INSTALLED`; more than one is fatal `D05_E_AUTHORITY_SCHEMA_AMBIGUOUS`. A worker is not permitted to choose between competing schemas. `question_variable_alias` is read only from that same resolved schema.

## 1. RESPONDENT IDENTITY

The apparatus measures and enforces:

- total respondent rows;
- global uniqueness and non-nullness of `survey_microdata_respondents.id`;
- response-parent orphan count;
- response-bearing respondent count;
- source/wave/country respondent counts;
- raw respondent/variable multiplicity;
- canonical respondent/question multiplicity after the current mapping rule.

Fatal invariants include:

- respondent surrogate IDs must be globally unique;
- every response row must have a respondent parent;
- no identity result may be reconstructed from schema declarations when populated evidence is absent.

## 2. SOURCE / WAVE / COUNTRY / YEAR COVERAGE

`SOURCE_WAVE_READINESS.csv` reports actual populated:

- source;
- raw wave;
- canonical wave exposed by the facet relation;
- country;
- survey year;
- respondents;
- response rows;
- responding respondents;
- distinct variable codes;
- historical facet-ready rows/respondents;
- authority facet-ready rows/respondents;
- raw-minus-derived row counts.

`GOVERNED_SCOPE_COMPARISON.csv` separately compares the populated source/wave substrate to the **current production `CLOSED_35` law**. D05 does not hard-code a second wave alias ontology: it imports `canonical_source_family()`, `canonical_wave()`, and `active_closed_35_waves()` from `ddm_v550_question_relation_authority.py`.

## 3. RESPONSE INCIDENCE, MULTIPLICITY, AND COTRAVEL

`RESPONSE_MULTIPLICITY_AUDIT.csv` measures, per source/wave/country:

- response rows;
- distinct respondent/var pairs;
- duplicate respondent/var pairs;
- excess duplicate rows;
- respondent/canonical-question pairs;
- duplicate canonical-question pairs and excess rows;
- min/P50/P90/P99/max distinct questions per respondent;
- min/P50/P90/P99/max response rows per respondent.

`QUESTION_OVERLAP_SUMMARY.csv` audits **every unordered pair of actually populated variable codes** within each source/wave/country. It is not sampled and has no top-N semantic cut. For each pair it reports:

- respondents answering X;
- respondents answering Y;
- same-respondent overlap;
- union;
- overlap percentages against both marginals;
- Jaccard coverage;
- overlap where both respondent/question cells are individually unique;
- overlap compromised by duplicate response multiplicity;
- whether cotravel is physically possible at all.

Invariant: `0 <= overlap <= min(n_x, n_y)` for every pair.

This is the physical denominator for any later claim about `P(Y | X response)` or attitude cotravel.

## 4. POSITION COMPLETENESS

For every physically available current position field the audit measures:

- respondent rows;
- nonmissing rows;
- missing rows;
- coverage percentage;
- distinct nonmissing values;
- source family;
- wave.

The required governed surface includes at minimum:

- sex;
- age;
- age group;
- education level;
- income level;
- religion label;
- urban/rural;
- region;
- ethnicity;
- language;
- employment;
- marital status;
- household size;
- class level.

`age_group` is explicitly identified as a derived facet-ready coordinate rather than falsely attributed to `respondent_position_fact`.

If `ddm_demographic_field_register` physically exposes the expected register fields, all additional source-native demographic candidates are emitted as register candidates. Their presence in the register is **not** treated as proof that they survive in the respondent fact.

A null/blank position value is measured only as substrate missingness. It is never interpreted as real-world absence.

## 5. WEIGHTS

`WEIGHT_COVERAGE.csv` measures by source/wave:

- respondents;
- respondents with any weight row;
- respondents with a primary weight;
- respondents missing a primary weight;
- respondents with multiple primary weights;
- total/primary weight rows;
- null primary values;
- zero primary values;
- negative primary values;
- non-finite primary values;
- actual weight names;
- actual weight types;
- actual source variables.

The information-loss audit separately records whether PSU/stratum/cluster/FPC/replicate-design metadata are represented on the audited weight surface. A scalar primary weight is never called population truth and is never treated as sufficient authority for design-based inference.

Multiple primary weights are a named information-selection risk because current historical facet-ready construction chooses one primary row.

## 6. RESPONSE TOPOLOGY AND TYPED MISSINGNESS

D05 does **not** infer binary/ordinal/nominal/scale/matrix/multi-select topology from observed cardinality.

`RESPONSE_TOPOLOGY_AUDIT.csv` reports physically exposed question type, response topology, handling rule, and source-structure classification alongside observed response counts/cardinality and duplicate respondent/var multiplicity. If topology authority is not exposed, the audit records that fact.

Likewise, DK, refusal, IAP/not-asked, missing, and substantive-response status are measured only from explicit typed fields such as:

- `is_missing`
- `is_dk`
- `is_refusal`
- `is_iap`
- `is_valid_substantive_response`

Blank or null `value_raw`/`value_text` is never silently promoted to a semantic missingness category. If typed fields are absent the audit emits `D05_W_TYPED_MISSINGNESS_NOT_EXPOSED`.

## 7. RAW INFORMATION LOSS AND FACET-READY TRUTH

For each physically available facet-ready response relation, `FACET_READY_PARITY_AUDIT.csv` performs a full outer comparison against the raw response substrate at:

`(source, wave, country_code, respondent_id, UPPER(var_code))`

It measures:

- raw rows;
- facet rows;
- raw/facet keys;
- raw rows missing from facet;
- facet rows without raw parents;
- respondent/var multiplicity mismatches;
- `value_raw` multiset mismatches when the target relation exposes `value_raw`;
- `value_text` multiset mismatches when the target relation exposes `value_text`.

The semantic guard makes a crucial distinction: **a field absent from the target relation is `NOT_EXPOSED`, not “preserved with zero mismatches.”**

`INFORMATION_LOSS_AUDIT.csv` also records implementation-visible transformations already present in current construction, including:

- historical facet-ready `canonical_wave` fallback behavior;
- age-group derivation from age;
- exact-wave-first / newest-loaded QSM row selection;
- primary-weight selection;
- routing/design metadata exposure or absence;
- materialized shared-cache selectivity.

These are transformation facts. Whether they caused populated information loss is decided only from the populated run.

## 8. CANONICAL QUESTION IDENTITY

Question identity is audited through three distinct surfaces rather than collapsed:

### Current database QSM

`IDENTITY_JOIN_AUDIT.csv` partitions every raw response row into:

- exactly joined;
- fallback joined;
- ambiguous;
- unmapped;
- plus blocked/excluded mapping-status counts.

The partition is an invariant; the buckets must sum exactly to raw response rows.

### Current production R1 authority

`R1_AUTHORITY_JOIN_AUDIT.csv` calls the production `resolve_question_relation_authority()` for **every populated raw source/wave/country/var identity**. It records:

- canonicalized wave;
- response-row support;
- resolution status;
- match count;
- authority question ID;
- authority status;
- relation-use status;
- mapping status;
- authority rule ID;
- exact active authority artifact SHA256.

D05 therefore does not reproduce R1 identity rules with home-grown strings.

### Installed canonical registry / aliases

Where the reconciliation schema is physically installed, `CANONICAL_REGISTRY_JOIN_AUDIT.csv` separately measures exact canonical-registry matches and alias matches and classifies each populated raw identity as exact, alias, ambiguous, or unmapped.

Names are not treated as ontology equivalence.

## 9. FACET-READY QUERY RECONSTRUCTIBILITY

For each audited facet relation the apparatus determines whether respondent linkage and required position predicates remain physically sufficient to form:

- `P(Y | position)`;
- `P(Y | position conjunction)`;
- `P(Y | X response)`;
- `P(Y | X response AND position)`.

These flags require row/linkage parity and the relevant physical columns. They are not assertions that any conditional is substantively authorized or sufficiently supported for inference.

## 10. SHARED RESPONDENT SUBSTRATE

The apparatus auto-discovers every materialized:

`data/ddm_repository_copy/v550/**/v550_shared_respondent_substrate.parquet`

If none are present, it emits `D05_W_SHARED_CACHE_NOT_MATERIALIZED`; cache losslessness remains unproved rather than guessed.

For every discovered cache it audits every physically selected `(source, wave, canonical_wave, country_code, var_code)` against the production response relation selected by current authority-first V550 relation law. It measures:

- cache rows vs selected DB rows;
- cache respondents vs selected DB respondents;
- explicit selection columns;
- required position predicate fields;
- typed missingness fields;
- topology fields;
- whether the cache is predicate-preserving over the selection it actually claims to contain.

This distinguishes two questions that the first return blurred:

1. Is the cache selective relative to the database?
2. Is it lossless over its explicit selection?

Selection is not itself corruption, and parity over a selected cache is not source equivalence.

## 11. SOURCE-EQUIVALENT AUTHORITY QUESTION

Because populated data are unavailable here, D05 does not choose one of the five substantive classifications yet.

Current blocked state:

`UNDETERMINED_DUE_TO_BLOCKED_POPULATED_DATA_ACCESS`

When the apparatus is actually run, the allowed substantive classifications remain:

- `PROVED_SOURCE_EQUIVALENT`
- `POTENTIALLY_SOURCE_EQUIVALENT_UNPROVED`
- `DERIVED_CACHE_WITH_KNOWN_LOSS`
- `DERIVED_CACHE_WITH_UNKNOWN_LOSS`
- `NOT_SOURCE_EQUIVALENT`

The proof bar is intentionally hostile: **database-internal parity alone cannot yield `PROVED_SOURCE_EQUIVALENT`.** Source-native evidence must additionally establish the fate of routing/not-asked semantics, original labels/codes where not retained, weighting design, geographic detail, demographic coordinates, source identifiers, multiple-response semantics, and ingest provenance.

## MACHINE-READABLE OUTPUT CONTRACT

The canonical run produces, where the relevant physical surface exists:

- `RELATION_PREFLIGHT.csv`
- `SOURCE_WAVE_READINESS.csv`
- `POSITION_FIELD_COMPLETENESS.csv`
- `QUESTION_OVERLAP_SUMMARY.csv`
- `WEIGHT_COVERAGE.csv`
- `IDENTITY_JOIN_AUDIT.csv`
- `R1_AUTHORITY_JOIN_AUDIT.csv`
- `CANONICAL_REGISTRY_JOIN_AUDIT.csv`
- `GOVERNED_SCOPE_COMPARISON.csv`
- `RESPONSE_MULTIPLICITY_AUDIT.csv`
- `TYPED_MISSINGNESS_PREVALENCE.csv`
- `RESPONSE_TOPOLOGY_AUDIT.csv`
- `FACET_READY_PARITY_AUDIT.csv`
- `CACHE_SELECTED_PARITY.csv`
- `INFORMATION_LOSS_AUDIT.csv`
- `STATIC_EVIDENCE_PROVENANCE.csv`
- `INVARIANT_RESULTS.csv`
- `FAILURES.csv`
- `EXTENDED_FAILURES.csv`
- `AUDIT_RUN.json`
- `EXTENDED_AUDIT_SUMMARY.json`

Every exact CSV header, failure code, invariant, relation/column requirement, and source-equivalence value is fixed in `D05_AUDIT_CONTRACT.json`. A completing worker is not authorized to alter those semantics merely to make the audit pass.

## BLOCKER RESOLUTION CONDITION

D05's empirical verdict can close only when the canonical entrypoint is run against:

1. the populated production PostgreSQL database, or an exact transactionally consistent production-equivalent snapshot; and
2. where source-equivalence rather than DB-internal equivalence is being claimed, the exact source-native/ingest evidence identified by hash/provenance.

Until then, the court remains:

`BLOCKED_MISSING_POPULATED_DATA_ACCESS`

But unlike the first return, the missing database is now the **only legitimate remaining execution blocker**. The worker who receives database access has an executable audit contract rather than a request to invent one.

No ingestion, production database, V550 production code, downstream architecture, or retention policy has been changed by D05.
