# PRE553 SUBSTRATE RECONSTRUCTION — PRE-RECONSTRUCTION DDM DATABASE DEPENDENCY MAP

Status: `FROZEN_STATIC_TRACE__FROZEN_PARENT_9188DC9`

Frozen pre-reconstruction machine head: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

This map answers one question only:

> Which current PostgreSQL surfaces can actually affect the pre-reconstruction V550→V552J build, and which surfaces are merely archaeological/provenance evidence?

It is derived from the frozen V550 runtime source under `data/ddm_build_copy/` plus the exact user-supplied current database schema dump `Rawlsing_WVS_public_schema(2).sql`. It supersedes any treatment of every extant Postgres table as an equal runtime dependency.

## 1. Runtime ingress boundary

The database is a live empirical ingress dependency primarily at V550. Downstream V551+ compilers consume V550-produced frames/artifacts and governed authority artifacts; they are not authorized to treat arbitrary legacy database tables as independent empirical truth.

### DIRECT_RUNTIME_V550

These relations are queried directly by frozen V550/runtime readiness code:

| relation | runtime use |
|---|---|
| `survey_microdata_respondents` | source/wave/country scope discovery and respondent counts |
| `respondent_position_fact` | demographic/position coverage and conditioning fields |
| `survey_weight_fact` | weight coverage and primary-weight values exposed through the response-long layer |
| `question_structural_mapping` | question/structural mapping slices and mapping coverage |
| `v_ddm_response_long_facet_ready` | primary respondent-response long-form query surface for question rows and response coverage |

Frozen-code evidence paths:

- `data/ddm_build_copy/build_determinicity_repository_v550.py`
- `data/ddm_build_copy/ddm_v550_readiness.py`
- `data/ddm_build_copy/ddm_v550_shared_cache.py`

## 2. Transitive runtime substrate

These relations are not all independently queried by the top-level builder, but they materially determine the direct runtime surfaces above.

### TRANSITIVE_RUNTIME_V550

| relation | transitive path |
|---|---|
| `survey_microdata_responses` | read by `v_ddm_response_long_facet_ready` |
| `respondent_source_wave_identity` | read by `v_ddm_response_long_facet_ready` to attach canonical display source/wave + governed source/wave UID identity |
| all 36 `respondentsDemo*` tables | unioned by `respondent_position_fact` |
| `survey_weight_fact` | read by `v_ddm_response_long_facet_ready` primary-weight selection as well as direct readiness |
| `question_structural_mapping` | read by `v_ddm_response_long_facet_ready` as well as direct V550 mapping logic |

The exact supplied schema contains **36** named `respondentsDemo*` tables. All 36 are constituents of `respondent_position_fact`. This physical database fact must not be confused with the governed **35-source** reconstruction universe: `respondentsDemoAsianBarW6` is physically present in the historical view but Asian Barometer W6 is excluded from the accepted CLOSED_35 source universe.

## 3. Conditional runtime override surfaces

Frozen V550 supports explicit relation overrides:

- `DDM_RESPONSE_LONG_RELATION`, default `v_ddm_response_long_facet_ready`;
- `DDM_QSM_RELATION`, default `public.question_structural_mapping`.

The supplied current schema also contains `v_ddm_response_long_facet_ready_authority`, which extends the base response-long view with `survey_authority_compendium` fields. That authority view and `survey_authority_compendium` are therefore classified as `CONDITIONAL_RUNTIME_OVERRIDE`, not default empirical ingress.

No alternate relation becomes authoritative merely because the schema contains it. Any historical run claiming an override must identify the exact configured relation in its own execution provenance.

## 4. Provenance-only surfaces

These surfaces do not supply ordinary V550 empirical rows, but they can prove which writers/rebuilders/repairs acted on runtime-critical carriers and when.

### PROVENANCE_ONLY

- `survey_microdata_reload_progress`
- `ddm_inline_respondent_build_progress`
- `ddm_named_respondent_demographics_progress`
- `ddm_template_rebuild_progress`
- `evs_loader_chunk_progress`
- `country_identity_repair_runs`
- `country_identity_repair_base_snapshot`
- `country_identity_repair_demo_snapshot`
- `country_identity_repair_response_invariants`

They may affect genealogy adjudication. They may not be used as source-native empirical authority.

## 5. Peripheral legacy surfaces

The following extant relations are not part of the frozen default V550 empirical ingress path and therefore must not consume SR02 live-probe budget as if they were runtime dependencies:

### PERIPHERAL_LEGACY__STATIC_GENEALOGY_ONLY

- `driver_aggregates`
- old `respondents`
- old `responses`
- legacy `variables`
- legacy `questions`
- historical cubes/aggregates not referenced by the frozen V550 ingress

They remain in `DATABASE_SURFACE_INVENTORY.csv` / writer archaeology. They can be retained as regression/history evidence, but a defect in one of these surfaces cannot by itself block the C11 rebuild unless a separately traced live consumer is proven.

## 6. Runtime-critical dependency closure

For substrate reconstruction, current-DB provenance must close this dependency cone:

```text
survey_microdata_respondents ------------------------------┐
                                                           │
survey_microdata_responses --------------------------┐     │
                                                     │     │
respondent_source_wave_identity ---------------------┤     │
                                                     │     │
respondentsDemo* (36 physical tables)                │     │
        ↓                                            │     │
respondent_position_fact ----------------------------┤     │
                                                     │     │
survey_weight_fact ----------------------------------┤     │
                                                     │     │
question_structural_mapping -------------------------┤     │
                                                     ↓     │
                                  v_ddm_response_long_facet_ready
                                                     │     │
                                                     └──┬──┘
                                                        ↓
                                                       V550
                                                        ↓
                                            V550-produced artifacts
                                                        ↓
                                                   V551→V552J
```

`respondent_position_fact`, `survey_weight_fact`, and `question_structural_mapping` are shown both as direct V550 inputs and as dependencies of the long view because both paths are real.

## 7. SR02 consequence

SR02 live execution is henceforth ordered by this dependency map:

1. verify live schema contract for every runtime-critical and provenance-only relation **before scanning data**;
2. capture current population/write-epoch/fingerprint evidence for the runtime-critical dependency cone;
3. capture progress/repair tables only as provenance evidence;
4. do not scan peripheral legacy analytical tables merely because they exist;
5. join the resulting receipt to static writer genealogy;
6. assign every runtime-critical surface an exact trust scope and terminal rebuild/regeneration disposition.

No SR02 rerun may be launched from an un-audited SQL payload.
