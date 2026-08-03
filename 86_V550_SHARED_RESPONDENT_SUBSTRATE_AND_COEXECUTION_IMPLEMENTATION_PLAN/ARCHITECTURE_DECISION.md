# Architecture decision: one respondent extraction, two governed branches

## Decision

V550 owns the physical interaction with the live respondent database. V550J becomes a co-executed branch of the V550 shard envelope and consumes an immutable respondent-level checkpoint produced from the same in-memory cache that V550 already uses.

V550J remains logically separate because it asserts a different kind of fact:

- V550: one governed respondent answer to one question implementation;
- V550J: several governed answers from the same respondent instantiate one governed joint configuration.

Separate semantics do not justify duplicate database I/O.

## Existing implementation facts

The current V550 shard runner already performs a bulk country-level query in:

```text
35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE/
  runtime_reproducibility_code/data/ddm_build_copy/
    build_determinicity_repository_v550.py
```

Function:

```python
_prefetch_question_rows_by_country(...)
```

It queries the relation named by `DDM_RESPONSE_LONG_RELATION`, defaulting to:

```text
v_ddm_response_long_facet_ready
```

The query retrieves all selected question aliases for one source/wave/country and orders by `var_code, respondent_id`. The resulting country frames are held in `question_row_cache`.

The shard runner then calls:

```python
_prepare_v550_question_row_cache(...)
```

which can harmonize the entire country frame once in `country` or `chunked` mode.

The normal V550 outputs and per-question checkpoints are aggregates and derived tables. They do not preserve respondent identity. The existing checkpoint recovery path may therefore reopen PostgreSQL to rebuild respondent-level state.

The V550J code already contains most of the correct respondent-substrate schema in:

```text
02_CORE_REFERENCE/code/build_v550j_prepared_substrate.py
```

including `PREPARED_SUBSTRATE_REQUIRED_COLUMNS`, normalization, manifest validation, and prepared-substrate caching.

The missing connection is that V550 discards the harmonized union frame while V550J can independently rebuild it from the database.

## Target dataflow

For each V550 shard and each country in that shard:

1. Resolve three disjointly described question sets:
   - **base set**: questions ordinary V550 is instructed to process;
   - **joint-required set**: questions required by the applicable governed Section 85 V550J registry;
   - **union extraction set**: exact union of the two sets.
2. Query the respondent relation once for the union extraction set.
3. Harmonize the returned country frame once.
4. Atomically persist the harmonized union as the shared respondent substrate.
5. Ordinary V550 processes only the base set from the in-memory shared frame.
6. V550J consumes the persisted shared frame using `prepared_required` plus explicit database prohibition.
7. V551/V552 and V551J/V552J remain separate downstream branches.

## Why the base and union sets must remain distinct

Some joint configurations require questions outside the frozen 20-variable base fixture. Those additional questions are allowed into the extraction only to complete the bounded joint configuration. They must not silently expand ordinary V550 outputs, alter the frozen base fixture, or create a production-completeness claim.

Therefore:

```text
base processing surface != union extraction surface
```

The manifest must record both surfaces and their overlap.

## Identity and compatibility

The implementation must not alter existing V550 question-output identities or V550J joint-pattern identities merely because new provenance fields or checkpoint hashes are recorded.

The shared-substrate hash is a new execution/provenance identity. It is not to be inserted into existing semantic object IDs unless an existing contract explicitly requires it.

## Database ownership

Production rule:

```text
V550 shard runner: database access permitted
V550J compiler: database access forbidden when invoked from V550 shared-substrate mode
```

A V550J fallback database path may remain for legacy/forensic use, but it must be opt-in, visibly non-governed for promotion, and impossible to enter silently from the co-execution path.

## Privacy and handoff boundary

Respondent-level substrate files are local execution artifacts. They must:

- be Parquet only by default;
- never be mirrored to CSV;
- never be committed to Git;
- never be bundled in cumulative handoff ZIPs;
- be permission-restricted where the host supports it;
- be represented in checkpoints only by manifests, schemas, hashes, counts, and verification returns.
