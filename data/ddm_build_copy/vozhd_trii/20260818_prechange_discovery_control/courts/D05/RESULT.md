# D05 — Populated Empirical Substrate Reality Court

## VERDICT

`BLOCKED_MISSING_POPULATED_DATA_ACCESS`

D05 cannot lawfully adjudicate the populated empirical substrate from the available environment. The repository exposes control law, schema/authority definitions, and ingestion/normalization code, but it does not expose a live populated PostgreSQL database or an exact materialized production-equivalent empirical snapshot. No populated substitute was found in the conversation/library surfaces available to this worker.

Per the court's fail-closed rule, no population counts, completeness claims, overlap claims, weight-coverage claims, response-topology claims, canonical-join rates, facet-row preservation claims, cache-loss claims, or source-equivalence classification are inferred from schemas or Python artifact names.

## Evidence actually available

At exact base SHA `bf9a0434eb2096d5c4725cf483ec757fd319b6af`, D05 inspected the pre-change control surface, `apply_postgres_facet_ready_substrate.py`, and the authority-reconciliation evidence under `evidence/conversation_inputs/`.

The control record identifies `Rawlsing_WVS_public_schema.sql` as a conversation attachment with expected raw-byte SHA256:

`a6963225c627110aec94617abbca1a85b2ac70338d477735d43e9b4ebf72cc56`

That file is not present in the repository copy available to this worker. The checked-in `Rawlsing_WVS_authority_reconcile_schema.sql` has expected SHA256:

`014ffe6994ac4a04b1d7e56457298c5c2cef3b106de5af5a3d009cabca084b0b`

The checked-in loader establishes relevant relational contracts, but these are implementation evidence only. In particular, current facet-ready construction joins `survey_microdata_responses` to question definition, structural mapping, wave registry, respondent position fact, and primary-weight state while retaining `source_family`, `country_code`, `source_wave_raw`, `source_wave_canonical`, `respondent_id`, response fields, position fields, and primary-weight fields. The authority view then left-joins `question_structural_mapping` and `survey_authority_compendium`. Whether those joins are populated, complete, unique, row-preserving, or multiplying is exactly what D05 must measure and therefore remains unadjudicated.

## What is not proved

All eleven requested physical questions remain empirically open: respondent identity; source/wave/country coverage; response incidence and pair overlap; position completeness; weight coverage/pathology; response topology; source-native information loss; canonical question identity; facet-ready respondent-link preservation; V550 shared-cache losslessness; and source-equivalent authority.

The source-equivalent classification is therefore:

`UNDETERMINED_DUE_TO_BLOCKED_DATA_ACCESS`

This is deliberately outside the five substantive source-equivalence outcomes because selecting any of those outcomes without populated evidence would decide the question the court is blocked from testing.

## Exact required populated inputs

A completing worker must have read access to the populated production database, or a transactionally consistent production-equivalent PostgreSQL snapshot, containing at minimum:

- `survey_microdata_respondents`
- `survey_microdata_responses`
- `survey_weight_fact`
- `respondent_position_fact`
- `question_structural_mapping`
- `survey_authority_compendium`
- `v_ddm_response_long_facet_ready`
- `v_ddm_response_long_facet_ready_authority`
- `ddm_demographic_field_register`
- `survey_question_definition`
- `survey_response_option_map`
- `survey_wave_registry`
- the actual primary-weight state relation consumed by `v_ddm_response_long_facet_ready`
- any actual relation substituted in production for one of the foregoing

To answer raw-loss and cache-loss questions rather than merely database-internal preservation questions, the same run also requires:

1. the exact source-native/ingest artifacts from which the populated database snapshot was produced, with hashes/manifests sufficient to identify their bytes;
2. `Rawlsing_WVS_public_schema.sql` with SHA256 `a6963225c627110aec94617abbca1a85b2ac70338d477735d43e9b4ebf72cc56`;
3. the exact materialized V550 shared-respondent cache/input artifact used for that same database build/run, plus its manifest/hash and the V550 loader configuration that selected it.

## Exact execution kit

Run the read-only SQL in `AUDIT.sql` against the populated database. It performs catalog/surface checks followed by the respondent, response, position, weight, canonical-identity, and facet-row-preservation measurements without mutating the database.

The required machine-readable output schemas are fixed in `EXPECTED_OUTPUT_SCHEMAS.json`. A completing worker must write the following under this D05 directory:

- `SOURCE_WAVE_READINESS.csv`
- `POSITION_FIELD_COMPLETENESS.csv`
- `QUESTION_OVERLAP_SUMMARY.csv`
- `WEIGHT_COVERAGE.csv`
- `IDENTITY_JOIN_AUDIT.csv`
- `RESPONSE_MULTIPLICITY_AUDIT.csv`

Any query that cannot be executed against the actual populated schema must itself be reported as a blocker; its intended metric must not be reconstructed from table DDL.

## Governing cautions for the completing run

- A non-null scalar weight does not establish design-based inference authority.
- Missing position values measure database absence, not real-world absence.
- A schema column does not establish populated coverage.
- A row in an authority table does not establish a unique authority join; multiplicity must be measured.
- Question-pair cotravel is possible only over same-respondent overlap actually present in the physical substrate.
- A cache is source-equivalent only if its transformations can be proved to preserve every empirically governed predicate/topology needed for replay; name similarity is irrelevant.
- No ingestion, database repair, or retention redesign is authorized by this court.
