# SR08 P1 RESOURCE-TRIPWIRE ADJUDICATION AND SR06 SCALE REOPEN

Status: `ACCEPTED_SCALE_FAILURE__G_SR06_REOPENED_FOR_RELATIONAL_EXECUTION_REPRESENTATION`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Accepted SR08-P1 branch: `agent/vozhd-trii-sr08-p1-lits1-c11-scale`

Accepted SR08-P1 return commit: `1f46ec7cb3752f41059706a33fbec11862191ab3`

Required return token observed: `PRE553_SR08_P1_LITS1_C11_SCALE_PREFLIGHT_RETURNED`

## 1. Publication and execution holding

HQ accepts the SR08-P1 return as valid fail-closed scale evidence.

The return is exactly one commit ahead of its frozen starting HEAD `7633f84473dcd63e3acb00247ac094bbc6ef4fde`, behind by zero, and changes exactly four files under the authorized `SR08_P1_LITS1_C11_SCALE_PREFLIGHT/` directory.

The exact LiTS I source remained:

- SHA-256 `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- 29,002 rows;
- 1,198 variables;
- 34,744,396 physical cells;
- Latin-1 reader use remained `COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`.

No runtime file or source byte was modified.

## 2. Accepted measurements

S1, 16 rows / 19,168 events, completed:

- supervised peak RSS: 1,131,312 KiB;
- Parquet: 3,814,750 bytes;
- I02 validation, persistence, full reopen and direct DuckDB all completed.

S2, 64 rows / 76,672 events, completed:

- supervised peak RSS: 1,604,384 KiB;
- Parquet: 13,823,355 bytes;
- I02 validation, persistence, full reopen and direct DuckDB all completed.

Fresh S2 repeat completed at peak 2,061,024 KiB and reproduced exactly:

- source/frontier identity;
- semantic release hash;
- relation logical digests;
- public object inventory digest;
- internal object inventory digest.

S3, 256 rows / 306,688 events, did not complete:

- external 4 GiB RSS tripwire fired;
- measured peak RSS: 4,238,408 KiB;
- termination occurred during full reopen;
- S4 was correctly not run.

The worker disposition `P1_BLOCKED__RESOURCE_TRIPWIRE` is accepted.

## 3. Dispositive diagnosis

This is NOT evidence of:

- a LiTS source-format contradiction;
- a DTA decoder failure;
- a Parquet product-selection failure;
- source-semantic impossibility;
- a new CLOSED_35 physical hazard class.

S1/S2 prove the current logical semantics can be validated, persisted and queried correctly at bounded size.

The failure is the accepted I02/SR06 execution representation at source scale.

Current runtime requires large logical sections to exist as tuples of Python `CanonicalSemanticObject` / `C11InternalRecord` instances, repeatedly walks and sorts exact refs, materializes replay closure, reconstructs the full logical release from Parquet, and can stage another in-memory object dictionary in `C11Repository`.

That representation is not viable for a source with tens of millions of respondent events.

The P1 projection is non-dispositive arithmetic but strongly confirms the measured direction: full LiTS I would require machine-impossible memory under the current materialized-object path. The S3 tripwire alone is sufficient to block continuation.

## 4. Contradiction scope

This finding REOPENS G-SR06 only for scalable execution representation.

It does NOT reopen:

- the public C11 semantic object families;
- M01-M18 meaning;
- exact source/respondent/event identity law;
- typed physical-versus-semantic separation;
- authority semantics;
- exact-ref semantics;
- I03/I05 truth conditions;
- structural admission semantics;
- V553-V558 / V3 / V2 semantics;
- selected physical carrier `PARQUET_DUCKDB_DIRECT`.

The correction must preserve those semantics while removing the requirement that the entire event/object universe coexist as Python objects.

## 5. Required scalable representation holding

The preferred correction is relation-first / stream-first C11 admission and access:

`physical batches -> validated canonical relation batches -> immutable Parquet -> lightweight exact release handle -> direct DuckDB / exact on-demand object reconstruction`

Full-source certification must not require:

- `tuple[RespondentEvent, ...]` over the complete event universe;
- full Python public/internal object inventories;
- full replay-closure tuples in memory;
- `ParquetC11Carrier.reopen()` reconstructing every object before ordinary analytical use;
- `C11Repository` duplicating the complete release into an object dictionary.

## 6. Semantic identity preservation law

This is an execution-representation correction, not a semantic rewrite.

For a bounded candidate representable by the preexisting object path, the new relation-first path must reproduce EXACTLY the same:

- per-object `object_id` / `content_hash` values;
- public and internal exact-ref inventories;
- candidate semantic projection hash;
- ReplayManifest exact identity;
- semantic release hash;
- M01-M18 coverage;
- source artifact ref;
- release ref.

The implementation may compute these identities by deterministic streaming rather than by materializing sorted Python lists, but the semantic bytes/hash result must be identical.

Any unavoidable change to those semantic identities is a new contradiction requiring HQ adjudication, not an implementation convenience.

## 7. Replay closure at scale

Replay closure remains mandatory.

The scalable path may persist closure refs as a canonical relation and verify/hash them by streaming or relational operations instead of storing all refs in one Python tuple.

The exact logical content of the closure must remain equivalent to existing I02 law.

A lightweight persisted replay-manifest identity/header plus canonical closure relation is acceptable only if small-fixture parity proves the resulting semantic ReplayManifest identity is exactly the one existing I02 would produce.

## 8. Repository/access model at scale

A scalable sealed release may be represented by a lightweight exact release handle containing identity, relation/member digests, coverage and replay identity, with canonical objects reconstructed on demand from verified Parquet when an exact object is requested.

Direct empirical query/discovery paths must operate against canonical Parquet relations rather than forcing full object reconstruction.

The old in-memory `C11LogicalRelease` / `C11Repository` may remain as bounded/test compatibility surfaces, but they may not be the required production representation for full survey releases.

## 9. SR07 status

The already-authorized WVS7 P1 scale preflight may finish as independent cross-format corroborative evidence if already launched.

Its result cannot authorize full SR07 certification while G-SR06 is reopened.

No new full proving-source certification may begin until the scalable C11 correction is accepted and the proving-source P1 courts are rerun or otherwise lawfully reclosed against it.

## 10. Gate state

`G-SR06 = REOPENED__RELATIONAL_SCALE_CORRECTION_REQUIRED`

`G-SR08 = BLOCKED__ACCEPTED_P1_RESOURCE_TRIPWIRE__ON_G_SR06_SCALE_CORRECTION`

`G-SR07 = P1_MAY_COMPLETE_CORROBORATIVE__FULL_CERTIFICATION_BLOCKED_ON_G_SR06_SCALE_CORRECTION`

`G-SR09 = BLOCKED`

## 11. Next execution

HQ must issue a bounded Codex implementation order for a scalable relation-backed I02/C11 execution path.

After that implementation is accepted, real-source scale proof resumes before full certification.
