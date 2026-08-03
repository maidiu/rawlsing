# Source-code audit supporting the implementation plan

This plan is based on the packaged code at parent commit `96831be6459abcf428670905adcc22021ee49c81`.

## V550 already performs the required bulk respondent extraction

File:

```text
35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE/
  runtime_reproducibility_code/data/ddm_build_copy/
    build_determinicity_repository_v550.py
```

Function `_prefetch_question_rows_by_country`:

- accepts the complete question-row selection;
- builds source, wave, country, and alias predicates;
- queries `DDM_RESPONSE_LONG_RELATION`, default `v_ddm_response_long_facet_ready`;
- selects all matching rows for one country;
- orders by `var_code, respondent_id`;
- returns one DataFrame per country.

This is the expensive database operation that must not be repeated by V550J.

## V550 already supports one-time whole-country harmonization

Same file, function `_prepare_v550_question_row_cache`:

- mode `country` harmonizes one complete country frame in one call;
- mode `chunked` harmonizes bounded chunks;
- mode `off` leaves the legacy per-question path.

The new governed shared-substrate mode must require `country` or `chunked` and persist the resulting frame. It must not create a second harmonization pass.

## The shard runner currently discards respondent identity after execution

File:

```text
.../build_determinicity_wave_shard_v550.py
```

The runner:

1. builds `wave_question_rows`;
2. filters response authority;
3. prefetches `question_row_cache`;
4. prepares it;
5. slices per question with `_question_rows_from_cache`;
6. writes derived per-question checkpoints and aggregate final tables.

The listed output tables include distributions, summaries, matrices, cloud tables, audits, and bridge artifacts. No raw respondent substrate is included.

`--write-csv` and `--write-parquet` govern those derived outputs. They do not preserve the bulk country response frame.

## Existing checkpoint paths are derived-table paths

File:

```text
.../ddm_v550_storage.py
```

`V550ShardPaths` defines:

- `checkpoints/questions`;
- `checkpoints/tables`;
- core/distribution/determinicity/cloud/audit/bridge output directories.

It does not define a respondent-substrate checkpoint. Section 86 adds one additively.

## Existing V550J prepared-substrate schema is the compatibility target

File:

```text
02_CORE_REFERENCE/code/build_v550j_prepared_substrate.py
```

It already defines:

- `PREPARED_SUBSTRATE_REQUIRED_COLUMNS`;
- normalized respondent, variable, response, source, wave, and country fields;
- semantic response role, directionality, target resolution, source structure, and question-use fields;
- validation of required columns and normalized identities;
- prepared Parquet and manifest paths;
- cache signature checks.

The shared V550/V550J schema must reuse this contract through a neutral module or compatibility re-export. Creating a divergent row schema would recreate the same integration problem one layer lower.

## V550J currently permits rebuilding or fallback

File:

```text
02_CORE_REFERENCE/code/compile_v550j_joint_response_patterns.py
```

Current `--v550j-substrate-mode` choices include:

```text
prepared_required
prepared_or_build
prepared_or_forensic_fallback
forensic_reharmonize
```

The co-execution path must use `prepared_required` plus a new hard `--forbid-database-access` gate and explicit substrate paths.

## Shard-launch arguments must be propagated

File:

```text
.../run_v550_shards_from_plan.py
```

The launcher constructs the shard-runner command and currently forwards thresholds, readiness, CSV/Parquet, resume, and overwrite options. New shared-substrate and co-execution options must be added here or they will disappear at orchestration time.

## The all-wave smoke runner already uses prepared mode but must remain unexecuted

File:

```text
.../run_20var_allwaves_v550_552j_smoke.py
```

It currently invokes V550 with `--v550-prepared-substrate-mode country`. This is compatible with the new shared checkpoint, but the runner must preserve the frozen base selection separately from added joint-required extraction items.

Section 86 authorizes updating this runner's contract only. It does not authorize launching the 35-wave run.

## Section 85 authority remains the joint-configuration source

Directory:

```text
85_V550J_BOUNDED_NINE_FAMILY_AUTHORITY_ADAPTER_AND_CANARY/
```

Its governed registries and adjudications identify which items form bounded joint configurations. They do not contain respondent rows. Section 86 uses them to construct the joint-required extraction surface without changing their authority.
