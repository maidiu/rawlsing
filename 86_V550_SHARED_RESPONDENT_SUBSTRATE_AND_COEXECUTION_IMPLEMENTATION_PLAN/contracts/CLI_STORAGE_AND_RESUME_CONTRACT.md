# CLI, storage, orchestration, and resume contract

## New V550 shard CLI

Add the following arguments to:

```text
.../build_determinicity_wave_shard_v550.py
```

### Shared-substrate mode

```text
--shared-respondent-substrate-mode
```

Choices:

```text
off
write_required
reuse_or_write
reuse_required
```

Semantics:

- `off`: legacy behavior; no shared respondent checkpoint; not valid for governed V550J co-execution.
- `write_required`: database extraction must occur and a new valid substrate must be written; an existing cache does not satisfy the request unless explicitly overwritten.
- `reuse_or_write`: use an exact valid cache when present; otherwise query once and write it.
- `reuse_required`: database access for respondent rows is forbidden; an exact valid cache must exist.

### Registry and authority

```text
--v550j-registry-path PATH
--v550j-joint-configuration-id ID       # repeatable; optional when registry scope resolves uniquely
--v550j-authority-return-path PATH       # optional explicit Section 85 return
```

A governed co-execution mode requires a governed registry. A draft registry is not executable.

### Co-execution mode

```text
--v550j-execution-mode
```

Choices:

```text
off
substrate_only
compile_after_v550
```

Semantics:

- `off`: no J branch requested.
- `substrate_only`: write/reuse and validate the shared substrate, but do not compile V550J; this is the default structural-development mode.
- `compile_after_v550`: after ordinary V550 base processing and substrate validation, invoke V550J locally from the checkpoint with database access prohibited.

### Output override

```text
--shared-respondent-substrate-root PATH
```

Default: the canonical shard checkpoint location.

### Database prohibition passed to V550J

Add to the V550J compiler:

```text
--prepared-substrate-path PATH
--prepared-substrate-manifest-path PATH
--forbid-database-access
```

When `--forbid-database-access` is set:

- `--db-url` is rejected;
- environment database URLs are ignored or rejected before connection creation;
- any code path that would query or rebuild from PostgreSQL raises `V550J_DATABASE_ACCESS_FORBIDDEN`;
- `prepared_required` is mandatory;
- response-option authority must be provided as an artifact path.

## Existing CLI compatibility

Do not repurpose `--write-csv`. It continues to control human-reviewable aggregate mirrors only.

Do not overload `--v550-prepared-substrate-mode`; it controls in-memory harmonization strategy (`off`, `country`, `chunked`). Shared-substrate persistence is a separate concern.

When shared-substrate mode is not `off`, require in-memory preparation mode `country` or `chunked`. Fail if it is `off`; do not silently harmonize a second time.

## Query and processing sequence

Refactor the shard runner to make the sequence explicit:

```python
base_question_rows = ...                         # frozen ordinary V550 surface
joint_requirement_rows = ...                    # governed registry requirements
extraction_question_rows = exact_union(...)
scoped_response_map = filter_for(extraction_question_rows)
question_row_cache = load_valid_cache_or_prefetch(extraction_question_rows)
question_row_cache = prepare_once(question_row_cache)
write_or_validate_shared_substrate(question_row_cache)
process_v550_question_loop(base_question_rows, question_row_cache)
optionally_compile_v550j_from_checkpoint()
```

Do not replace `base_question_rows` with the union in the ordinary V550 loop.

## Propagation through orchestrators

Update the following code paths so the new arguments are not lost:

```text
.../run_v550_shards_from_plan.py
.../plan_v550_wave_shards.py
.../run_20var_allwaves_v550_552j_smoke.py
```

Required plan columns or plan metadata:

```text
shared_respondent_substrate_mode
v550j_execution_mode
v550j_registry_path
v550j_joint_configuration_ids
shared_respondent_substrate_root
base_question_count
joint_required_question_count
union_question_count
```

The 35-wave runner must not be executed during this implementation tranche. It is updated only so the contract is not lost later.

## V550J invocation from the V550 envelope

Use a subprocess boundary rather than importing the complete V550J compiler into the V550 shard process. This preserves stage isolation and captures independent logs.

The command must include:

```text
--v550j-substrate-mode prepared_required
--prepared-substrate-path <parquet>
--prepared-substrate-manifest-path <manifest>
--forbid-database-access
--registry-path <governed registry>
--response-option-map <V550 scoped response map artifact>
--association-mode off                       # for bounded structural development
--no-write-csv
--write-parquet
```

The V550 shard manifest records the exact command, exit code, log path, V550J manifest path, and shared-substrate hash.

## Shard success semantics

Add explicit fields:

```text
v550_base_success
v550j_branch_requested
v550j_branch_mode
v550j_branch_success
shared_respondent_substrate_status
shared_respondent_substrate_manifest
shared_respondent_substrate_content_hash
shared_respondent_substrate_row_count
shared_respondent_substrate_respondent_count
```

If `compile_after_v550` is requested, shard `success` and `promotable` require both V550 base success and V550J branch success.

If `substrate_only` is requested, V550J output is not required, but a valid shared substrate is required.

Preserve successful ordinary V550 outputs when V550J fails, but mark the shard non-promotable and retain failure evidence.

## Resume order

Current resume behavior must be corrected so a checkpoint-only resume does not query PostgreSQL before checking checkpoints.

Required order:

1. Resolve base/joint/union selection and expected cache signature without querying respondent rows.
2. If an exact complete substrate exists, load and validate it.
3. If `reuse_required`, fail before opening a respondent-data connection when cache is absent or stale.
4. If `resume-from-checkpoints-only` and V550 question checkpoints are complete:
   - use the shared substrate if downstream respondent state is needed;
   - do not query PostgreSQL;
   - finalize from checkpoints.
5. Only `write_required` or `reuse_or_write` with no valid cache may enter `_prefetch_question_rows_by_country`.

## Recovery scripts

Update:

```text
.../rebuild_v550_bridge_from_checkpoints.py
.../rebuild_v550_wave_clouds.py
```

They must prefer the shared substrate and refuse a database reload when invoked with `reuse_required` or an equivalent strict flag.

Legacy runs without a shared substrate may retain an explicitly named forensic fallback, but the return must state:

```text
NON_PROMOTABLE_LEGACY_RESPONDENT_RELOAD
```

## No hidden second query

Instrument respondent-data query count.

The manifest and performance profile must include:

```text
respondent_data_query_count
respondent_data_query_count_by_country
respondent_rows_fetched
respondent_cache_source              # database | shared_checkpoint
```

Acceptance requires one respondent extraction query per country on a fresh run and zero on an exact checkpoint-only resume.
