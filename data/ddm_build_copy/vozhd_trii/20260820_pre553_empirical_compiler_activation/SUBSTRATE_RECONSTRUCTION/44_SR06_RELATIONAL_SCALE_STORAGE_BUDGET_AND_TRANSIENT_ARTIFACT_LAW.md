# SR06 RELATIONAL SCALE CORRECTION — STORAGE BUDGET AND TRANSIENT ARTIFACT LAW

Status: `BINDING_SUPPLEMENT__SR06_SCALE_ACCEPTANCE_REQUIRES_MEMORY_AND_DISK_FIT`

Parent authorities:

- `42_SR08_P1_RESOURCE_TRIPWIRE_ADJUDICATION_AND_SR06_SCALE_REOPEN.md`
- `43_SR06_RELATIONAL_SCALE_CORRECTION_IMPLEMENTATION_AUTHORITY.md`

## 1. Holding

A relation-first SR06 correction does not pass merely because it avoids the Python-object RAM wall.

The corrected canonical C11 persistence must also be operationally thin enough for the full CLOSED_35 campaign on a normal local workstation.

The prior P1 `18.7 GiB` WVS7 and `5.63 GiB` LiTS I figures are projections from the rejected materialized compatibility path. They are pathology evidence, not accepted storage targets.

No G-SR06 reclosure is authorized if the corrected representation merely moves the scale failure from RAM to disk.

## 2. Persistent-versus-transient accounting

Every scale receipt must distinguish exactly:

1. `CANONICAL_STEADY_STATE_BYTES`
   - immutable authoritative Parquet relations;
   - exact release/manifest metadata required to reopen and audit;
   - no scratch, no staging duplicate, no cache.

2. `ATOMIC_STAGING_PEAK_BYTES`
   - temporary bytes required while publishing a release atomically.

3. `SCRATCH_EXECUTION_PEAK_BYTES`
   - Arrow/spill/sort/temp material used during admission/audit.

4. `NONAUTHORITATIVE_CACHE_BYTES`
   - if any; must be separately identified and deletable.

5. `POST_SUCCESS_RETAINED_BYTES`
   - bytes remaining after lawful cleanup of staging/scratch/cache.

A temporary peak may exceed steady state. It may not be reported as canonical storage, and it must not silently remain after successful publication.

## 3. No duplicate steady-state truth

After successful atomic publication, steady state may contain only one authoritative empirical C11 copy:

`canonical immutable Parquet + tiny exact manifests/handles`

Forbidden steady-state duplication includes:

- persistent `.duckdb` copies;
- PostgreSQL mirrors as C11 truth;
- SQLite mirrors;
- old full Python-object serializations;
- duplicate object/release blobs;
- retained staging trees;
- retained full Arrow/materialization checkpoints that duplicate canonical empirical content.

Raw source snapshots remain separate source evidence and are not counted as a duplicate canonical C11 copy.

Legacy PostgreSQL retirement remains governed by G-SR10; this authority does not delete legacy evidence early.

## 4. Required million-event storage receipt

The Authority-43 synthetic 1,000,000-RespondentEvent court must additionally report:

- canonical steady-state bytes total;
- bytes by canonical relation/member;
- fixed per-release metadata bytes;
- event-bearing relation bytes;
- `canonical_bytes_per_respondent_event`;
- atomic staging peak bytes;
- scratch execution peak bytes;
- post-success retained bytes;
- ZSTD settings and row-group/encoding configuration;
- proof that source-variable/dictionary/topology metadata is normalized rather than repeated per event where exact refs/keys suffice.

The receipt must identify any per-event field whose value is invariant at respondent/question/source-variable scope and justify why it cannot be normalized.

## 5. Required source/corpus projections

Using measured corrected relation sizes, report `PROJECTION_ONLY` steady-state canonical storage for:

- WVS7: `59,595,860` physical cells;
- LiTS I: `34,744,396` physical cells;
- CLOSED_35: `486,174,936` physical cells.

Projections must separate fixed metadata overhead from event/cell-scaled relations and must not use the rejected P1 wide-object bytes/event as the corrected basis.

## 6. Operational storage bands

These are operational acceptance bands, not semantic identity rules.

### Preferred targets

- WVS7 corrected canonical steady state: `<= 2 GiB`;
- LiTS I corrected canonical steady state: `<= 1.5 GiB`;
- CLOSED_35 corrected canonical steady-state projection: `<= 20 GiB`.

### Hard stop / HQ re-adjudication thresholds

The implementation may NOT receive automatic G-SR06 acceptance if any corrected projection is:

- WVS7: `>= 4 GiB`;
- LiTS I: `>= 3 GiB`;
- CLOSED_35: `>= 32 GiB`.

Crossing a hard-stop threshold yields:

`SR06_SCALE_CORRECTION_BLOCKED__PERSISTENT_STORAGE_SCALE`

unless HQ explicitly revises the operational budget after inspecting the measured relation breakdown.

A result between preferred target and hard-stop threshold requires explicit HQ adjudication; it is not an automatic pass.

## 7. Thinness is part of correctness at this gate

The selected `PARQUET_DUCKDB_DIRECT` carrier won SR04 partly because it was the lightest candidate inside the accepted speed tie. The corrected C11 layout must preserve that architectural purpose.

Storage reduction may use:

- normalized variable/source metadata;
- dictionary encoding;
- binary rather than redundant textual physical keys where semantic reconstruction remains exact;
- derivable object identifiers rather than duplicated persisted representations where exact on-demand reconstruction proves identity;
- deterministic partitioning/row groups;
- ZSTD;
- relation-level typed defaults/absences where existing semantics permit exact recovery.

Storage reduction may NOT use:

- dropping raw physical states;
- dropping source declarations;
- losing label dictionaries/topology;
- lossy numeric coercion;
- semantic recoding without authority;
- weakening object/ref/replay identity;
- aggregate-only substitution for respondent incidence.

## 8. Cleanup law

After a successful bounded or full execution:

- staging directories must be removed after atomic publication is verified;
- scratch Arrow/spill/sort products must be removed;
- temporary preflight Parquet carriers need not be retained once their small committed receipts are accepted;
- nonauthoritative caches must be safely regenerable and deletable;
- only canonical accepted release material plus required exact audit metadata remains as C11 steady state.

No raw source snapshot or legacy database evidence is deleted under this authority.

## 9. G-SR06 acceptance amendment

Authority 43's `PARITY_AND_SCALE_PASS` now means ALL of:

1. exact old/new semantic identity parity on bounded fixtures;
2. 1,000,000-event court completes below the RAM threshold;
3. no whole-event or replay-closure Python materialization;
4. streaming full audit passes;
5. direct DuckDB and exact on-demand resolution pass;
6. canonical steady-state storage is measured and projected under this law;
7. no hard-stop persistent-storage threshold is crossed;
8. transient artifacts are proven disposable and absent from post-success steady state.

RAM pass alone is insufficient.

## 10. Required return addition

The SR06 relational-scale worker return must include a `STORAGE_BUDGET` section containing all measurements and projections required above.

If the worker began before this supplement was published, it must read this file from the exact control branch and incorporate it without rebasing or changing its frozen starting HEAD.

Token remains:

`PRE553_SR06_RELATIONAL_SCALE_CORRECTION_RETURNED`
