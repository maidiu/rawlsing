# Codex implementation instructions

## Mission

Implement the V550 shared respondent substrate and V550J co-execution contract described in this section. Do not perform a real respondent-data run during this task.

The deliverable is executable code, tests, manifests, and a cumulative checkpoint proving that V550 can query a unioned respondent surface once, persist it, run ordinary V550 from the base subset, and run V550J locally from the persisted substrate with database access forbidden.

## Starting state

Begin from the cumulative checkpoint commit recorded in `CURRENT_STATE.json`.

Preserve unchanged:

- R184 database dump and authority files;
- Section 85 bounded adapter authority and adjudications;
- the original uploaded nine-source archive;
- all existing semantic identity hashes unless a concrete failed invariant demonstrates a necessary change.

Create a new working branch and a separate test output root. Do not modify or use the restored R184 database as a respondent-data store.

## Phase 0 — reproduce the parent checkpoint

Before editing:

1. verify package hashes;
2. clone/verify the Git bundle;
3. require a clean worktree;
4. run Section 85 self-contained reproduction;
5. run Section 85 bounded adapter tests;
6. run existing V550J regression tests.

Record exact returns.

## Phase 1 — create the neutral shared-substrate module

Create:

```text
.../ddm_v550_shared_respondent_substrate.py
```

Move no behavior destructively. Implement neutral shared functions and re-export them from `build_v550j_prepared_substrate.py` where existing imports require compatibility.

Required functions, names may vary only with a documented reason:

```python
canonicalize_shared_respondent_substrate(...)
logical_shared_substrate_hash(...)
shared_substrate_paths(...)
write_shared_respondent_substrate_atomic(...)
load_shared_respondent_substrate(...)
validate_shared_respondent_substrate(...)
shared_substrate_cache_signature_matches(...)
```

Reuse `_harmonize_question_frame` output. Do not harmonize again inside the writer.

## Phase 2 — implement exact base/joint/union selection

In the V550 shard runner:

1. preserve the existing base question list;
2. load the applicable governed Section 85 registry;
3. resolve exact applicable items by source, wave, country, configuration ID, and question implementation identity;
4. create the joint-required set;
5. create a deterministic union extraction set;
6. write a pre-extraction selection audit;
7. fail closed on unresolved or duplicate applicable items.

The selection audit must prove all set equations from the shared-substrate contract.

Do not let the union replace the base list in V550's ordinary per-question loop.

## Phase 3 — query and harmonize once

Route only the union extraction set into `_prefetch_question_rows_by_country`.

Require `--v550-prepared-substrate-mode country` or `chunked` for the new governed mode. The returned cache must be harmonized once and then used by both branches.

Add query-count instrumentation around the actual respondent relation calls.

## Phase 4 — atomically persist the union cache

Immediately after preparation and before the ordinary question loop:

1. convert each country frame to the shared schema;
2. annotate row selection roles;
3. write the atomic Parquet/schema/manifest/validation/COMPLETE group;
4. reload and validate it;
5. compare in-memory and reloaded logical hashes;
6. preserve only aggregate diagnostics in logs.

The ordinary V550 loop continues using the in-memory frame. Do not reread Parquet merely to continue the same process.

## Phase 5 — make V550J checkpoint-native and database-forbidden

Extend `compile_v550j_joint_response_patterns.py` and prepared-substrate loading so an explicit shared Parquet and manifest can be supplied.

Implement `--forbid-database-access` as a hard gate, not a convention.

When explicit shared substrate is supplied:

- validate source/wave/country and all authority hashes;
- validate the registry's required items against the substrate;
- never open PostgreSQL for respondent rows;
- never rebuild the response map from PostgreSQL;
- fail if the supplied response-option map is absent or stale;
- use `prepared_required`.

## Phase 6 — co-execute through a subprocess

When `--v550j-execution-mode compile_after_v550`:

1. ordinary V550 base processing completes;
2. V550 writes its scoped response-option map;
3. V550 invokes the V550J compiler as a subprocess;
4. V550 passes the shared paths, governed registry, exact response map, and no-DB flag;
5. V550 captures stdout/stderr and return metadata;
6. shard promotion depends on V550J success.

Do not run V551J or V552J in this implementation tranche except on a tiny synthetic fixture after V550J passes. The objective is to establish the reusable physical boundary first.

## Phase 7 — fix resume and recovery

Move cache/checkpoint resolution ahead of respondent prefetch.

Prove:

- fresh run: one query per country;
- exact resume: zero respondent queries;
- V550J rerun from shared substrate: zero respondent queries;
- bridge/cloud recovery from complete shared substrate: zero respondent queries;
- stale cache: fail or rebuild according to mode, never silently reuse.

## Phase 8 — synthetic structural integration

Build a small deterministic synthetic response relation in a temporary PostgreSQL database or a mocked SQL reader. It must include:

- all nine Section 85 configurations;
- complete and incomplete respondents;
- substantive, neutral, DK, refusal, IAP, and missing responses;
- response variants;
- at least one joint-only question outside a base 20-variable selection;
- multiple countries only where required to test partitioning;
- no personal or real respondent data.

Required end-to-end structural tests:

```text
synthetic relation
→ V550 single union query
→ shared respondent substrate
→ ordinary V550 base outputs
→ V550J prepared_required/no-DB compile
→ minimal V551J
→ minimal V552J
```

Keep association mode off.

## Phase 9 — regression and mutation gates

Run every test in `validation/TEST_AND_MUTATION_MATRIX.csv`.

Do not weaken existing tests to accommodate the new path. Add compatibility tests proving legacy mode remains unchanged when the new options are off.

## Phase 10 — checkpoint

Only after all gates pass:

1. commit intentionally;
2. create a Git bundle;
3. package code, instructions, manifests, test returns, and synthetic fixtures;
4. do not package any respondent-level real-data substrate;
5. include the unchanged R184 dump and Section 85 authority;
6. write exact next instructions for a later GSS real-data canary;
7. verify the cumulative ZIP from a fresh extraction and Git-bundle clone.

## Stop boundary

Stop after structural implementation and synthetic end-to-end acceptance.

Do not:

- run GSS 2010 real respondents;
- run nine real source canaries;
- run one country per wave;
- generate the full 35-wave canonical universe.

Those are later empirical gates after the whole downstream structure is closed or the user explicitly authorizes them.
