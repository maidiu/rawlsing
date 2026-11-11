# SAVED_ACCESS_CONTRACT_R1 — exact API, representation, impediments, grant

Source: `16f97fe23e395d6807a13a4fa5ea0c2b96bccd69` via `git show` from `pyat-w03-w04-mcr-completion-r1`; production `f329b8c04` is identical for all cited files. The reviewer checkout is unchanged at `475035790098d11751012308b7fd62576987502d`.

## 1. Existing APIs and owners

| Owner/API | Exact location | Role in saved access |
|---|---|---|
| `ParquetC11Carrier._relation_objects` | `pre553_parquet_carrier.py:221-235` | Maps a `C11LogicalRelease` to relation tables; iterates `release.public_objects` (materializes compact events). |
| `ParquetC11Carrier._write_tables` | `:237-258` | Writes full relation Parquet/zstd tables, sorted rows, logical digests, member hashes, identity row. |
| `ParquetC11Carrier.persist` | `:260-295` | Atomic full-release publication; calls `_write_tables`. |
| `ParquetC11Carrier._read_rows` | `:297-300` | Reads a whole relation table into a Python list. |
| `ParquetC11Carrier.reopen` | `:301-376` | Reads all `RELATION_SPECS` + `release_identity`, checks manifest/member/relation digests, reconstructs every object via `_object_from_row`, calls `_make_validated_release`, checks identity/closure. |
| `verify_semantic_release_root` | `:160-196` | Derives release root from persisted identity/replay/coverage; must stay at open. |
| `C11LogicalRelease` | `pre553_c11_repository.py:26-67` | Accepts `public_objects` as a full tuple or `_CompactPublicObjects`; binds compact view to release/replay refs. |
| `_make_validated_release` | `:142-143` | Sole seal for a validated release; accepts compact `public_objects`. |
| `C11Repository._commit_validated` | `:115-139` | Uses `exact_entries()` for compact releases; stores `_EventLocator`s without materializing every event. |
| `C11Repository.resolve_object_exact` | `:107-113` | Materializes exactly the selected `_EventLocator`; no fuzzy fallback. |
| `_EventRead` | `_pre553_c11_execution_view.py:48-81` | Compact selector: ref, typed state, native/canonical/component refs, authority refs, raw/canonical value, multiplicity/order/rank, occurrence id. |
| `_CompressedBodies` | `:85-112` | Bounded zstd event-body chunks with row starts/counts; on-demand exact body retrieval. |
| `_EventLane`, `_EventLocator`, `_RespondentEvents`, `_CompactPublicObjects` | `:114-206` | In-memory compact lane, lazy exact locator, respondent sequence, compact public-object view. |
| `_read_bodies` / `_write_bodies` | `:228-330,367-389` | Existing body-cache reader/writer with per-body SHA, schema/envelope checks; body-only accelerator. |
| `_compact_public_objects` | `:451-556` | Existing derivation of selectors, groups, non-events and bodies from full I02 objects; exact representation map. |
| `ColdCompactBuilder` | `_pre553_w03_cold_compact.py:38-147` | Streaming builder from an already-validated event stream; retains selectors/compressed bodies, drops full events; `finish` sorts entries/by-respondent/event states. |
| `attach_governed_cache` | `:215-256` | Attaches the disposable governed body cache to a compact release; safe miss; not a canonical store. |
| `_build_release_index` | `_pre553_query_predicate.py:63-128` | For compact releases uses `public.by_respondent`; no full event materialization. |
| `_select_respondent_events` | `:18-61` | Compact path yields `_EventRead`; native path yields `RespondentEvent`; same selector contract. |
| `_semantic_value`, `_ReleaseIndex` | `_pre553_query_common.py:159-172,249-255` | Consume `_EventRead` without full event bodies. |
| `CarrierNeutralResearchExecutor.execute_i03/execute_i05` | `pre553_carrier_execution.py:403-479` | Exact repository-driven native I03/I05; accepts `C11Repository` with compact release. |
| `BatchExecutionRunner` | `pre553_batch_runner.py:385-430,536-624` | Exact `C11Repository`; executor bindings run I03/I05; no separate event path. |
| `execute_empirical_query` | `pre553_empirical_query.py:685+` | Exact repository/index query; uses compact selectors through `_ReleaseIndex`. |
| FieldForge owner | `field_forge_conditional_support.py:194-273,467-580` | Consumes exact `EmpiricalFact`/query/permissions; no direct C11 event read. |
| Full construction | `pre553_source_backed_c11_facade.py:896-1100,1265-1300` | `build_cold_source_backed_c11_release` (streaming compact) and `build_source_backed_c11_repository`; full I02 validation stays here. |
| Identity/coverage | `pre553_c11_integrity.py:305-330,510-560` | `ReplayManifest` and `make_m01_m18_coverage`; metadata-level identity. |
| Canonical encoding | `pre553_empirical_objects.py:215-220,516-535` | `canonical_json` is deterministic sorted JSON; `RespondentEvent` fields/identity. |

## 2. Representation contract

**Full carrier:** one Parquet/zstd table per relation (`empirical_universes`, `respondent_identities`, `question_variable_bindings`, `respondent_events`, `routing_eligibility`, `empirical_coordinates`, `weight_measure`, `authority_snapshots`, `source_universe_relations`, `replay_bindings`, `replay_manifest`, `release_identity`). Rows are sorted by `(object_family, object_id)`; each relation has a canonical JSON logical digest; the manifest has member SHA-256s and relation digests; identity/replay rows bind source/release/semantic/replay/M01-M18. This is the current canonical full artifact.

**Compact lane:** `_EventRead` selectors + zstd body chunks + non-event objects + `entries` (integers for event rows, objects for non-events) + `by_respondent` groups + `event_states`. The selector/body/group/order construction is exactly `ColdCompactBuilder`/`_compact_public_objects`; `entries` and `by_respondent` are sorted by exact event key/ref key, matching eager `public_objects` order. `_CompactPublicObjects.exact_entries()` yields `_EventLocator`s; repository and query index use those refs; only selected events materialize.

**Existing saved body accelerator:** `c11-events-*.parquet` is body-only (binary canonical bodies, zstd), policy/root/envelope-bound and disposable. It has no selectors/groups; `_read_bodies` requires in-memory selectors. It is not a canonical compact saved release.

**Missing saved representation:** no canonical compact selector/body/group sidecar in the release directory; no `reopen_compact`; `persist` of a compact release materializes all events; `reopen` reconstructs all relations/objects.

## 3. Exact supported seam

Yes, the repository/executor/query/batch owners already support the compact representation. The supported seam is:

`ParquetC11Carrier.persist_compact(release) -> compact sidecar + manifest-bound metadata`
→ `ParquetC11Carrier.reopen_compact(source_sha, release_id, semantic_hash) -> C11LogicalRelease` with `_CompactPublicObjects`
→ `C11Repository((release,))` (stores `_EventLocator`s)
→ `CarrierNeutralResearchExecutor.execute_i03/execute_i05` or `BatchExecutionRunner`
→ `_build_release_index`/`_select_respondent_events`/`_semantic_value` selectors; only selected events materialize
→ exact `EmpiricalFact` identity for the existing FieldForge owner if a direct FieldForge consumer is exercised.

No repository, executor, query, batch, or FieldForge ABI change is required. No DuckDB: PyArrow Parquet/zstd and the existing `_BodyCacheWriter`/`_compress_body_chunk` are sufficient. The R4 DuckDB compaction is a separate SR06 event reader and is not the C11 release-identity representation; it would add an adapter, not the smallest seam.

## 4. Exact impediments

1. `ParquetC11Carrier.persist`/`_relation_objects` iterates `release.public_objects`; for `_CompactPublicObjects` this materializes every event before writing (`pre553_parquet_carrier.py:221-258`). Compact saving is therefore not bounded.
2. `ParquetC11Carrier.reopen` reads every relation via `_read_rows` (whole-table list) and reconstructs every object via `_object_from_row` before `_make_validated_release` (`:297-376`). There is no compact branch and no streaming row reader.
3. The compact selectors/groups are not persisted. The accelerator body cache stores only bodies; `_read_bodies` needs selectors from an in-memory release. A fresh process cannot reconstruct the compact lane from the cache alone.
4. The event relation logical digest is global: `_write_tables` sorts full event rows and `_logical_digest(rows)` hashes the complete canonical JSON array (`:117-120,237-258`). A compact sidecar cannot recompute that exact full-row digest without the full event rows. This is the only place where the existing digest can force a complete event-row pass; it does not force full object reconstruction.
5. `_CompactPublicObjects`/`_EventRead`/`_EventLane` are private and have no constructor from persisted rows; `_EventRead` does not carry universe/respondent group keys (the builder groups them separately). A sidecar loader must persist group keys or a group table and add a private constructor.
6. The manifest schema has no storage mode/compact members. `reopen` has a fixed relation list; a compact-only manifest with no `respondent_events.parquet` would fail the eager path. The compact path must be explicit and typed.
7. The full event file member hash is file-level; the full relation digest is row-level. A compact-only artifact needs an admission-time event-set commitment (the full event relation digest) and exact selector/body/group digests; otherwise completeness/ordering of omitted events is unproved.
8. FieldForge is not directly called by the carrier/executor; it consumes an exact `EmpiricalFact`. A compact C11 release that preserves the exact I03 fact identity preserves the FieldForge input. No C11-event-level FieldForge change is needed.

## 5. Ordering, logical digest, global semantic validation

**Ordering.** The full carrier sorts rows by `(object_family, object_id)`; this is canonical storage order, not semantic order. `ColdCompactBuilder.finish` sorts `entries` by event key/ref key and `by_respondent` rows by event key; eager `_ReleaseIndex` sorts rows by ref key. Existing tests at `test_pre553_w03_w04_cold.py:163-195` compare selector sequence/yield and full I03/I05 material for routed/ordered/repeated cases. Preserve the exact sort; no semantic materialization is required.

**Logical digest.** `_logical_digest(rows)` is `SHA256(canonical_json(rows))`; `canonical_json` is deterministic sorted JSON (`canonicalize` sorts mapping keys; `json.dumps(sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)`). Because `_write_tables` writes the rows in the exact sorted order and Parquet preserves row order, a stream-equivalent digest is byte-identical using `[` + comma-joined `canonical_json(row)` in the same order + `]`. This is source-proven by composition, not executed here; the grant includes a tiny witness. It avoids materializing all rows, but the full event relation digest can only be recomputed from the full event rows; it cannot be recomputed from compact selectors alone.

**Global semantic validation.** `m01_m18_coverage`/replay/source/authority/closure validation is metadata/ref-level, not full-event-body-level. `C11LogicalRelease.__post_init__` checks compact release/replay binding; `_make_validated_release` seals; `C11Repository._commit_validated` uses exact locator refs. The full I02 semantic validation (event occurrence/topology/authority/source/replay) stays at construction/admission. Compact open can preserve the identity/ref/closure checks without full object reconstruction.

## 6. Checks at admission, persist, compact open, and after validation

| Stage | Must keep |
|---|---|
| Full construction/admission | Existing I02 validation: `build_cold_source_backed_c11_release`/`build_validated...`, `make_m01_m18_coverage`, `validate_public_carrier_object`, authority/source/replay closure, event occurrence/topology, `source_release_manifest_hash`, `semantic_release_hash`. |
| Persist | Full manifest hash/schema; every member SHA-256; relation digests; release/source/semantic/replay identity; exact selector/body/group hashes; admission-time full event relation digest (for compact-only) or full event table member hash (if retained). |
| Compact open | Full manifest hash/schema; member hashes including full event table if retained; compact sidecar member hashes; release/source/semantic/replay selectors; identity/replay rows; M01-M18 coverage; compact sidecar’s `full_event_relation_digest`/selector-body-group digests; event ref/content-hash/typed-state/order/authority; closure refs via locators/non-events/internal; `_make_validated_release`; exact path; no fuzzy selector. No `respondent_events.parquet` row decode. |
| Once validated | Repository’s exact object index may hold `_EventLocator`s; `resolve_object_exact` materializes selected events; `_ReleaseIndex` uses compact `by_respondent`; `execute_i03/i05` and `BatchExecutionRunner` trust the sealed release; per-call query/authority/source checks remain. No full event object reconstruction or revalidation per query. |

The full event relation digest is retained once validated at persist/admission and bound in the compact manifest. If the integrity owner requires independent recomputation at every compact open, use the streaming full-event-row digest pass; that is a strict mode, not a semantic change. No trusted-cache assumption: the compact sidecar is a content-addressed canonical member with exact hashes, not the disposable `c11-events-*` accelerator.

## 7. Smallest bounded next implementation grant

**Files:**

- `rawlsing_next/pre553_parquet_carrier.py` — add `persist_compact`, `reopen_compact`, compact sidecar manifest/member writers, and exact sidecar verification. Keep full `persist`/`reopen` unchanged for full/legacy releases; a compact-only manifest gets a typed `storage_mode` and `reopen` refuses it, directing to `reopen_compact`.
- `rawlsing_next/_pre553_c11_execution_view.py` — add a private persisted-selector/body/group constructor for `_CompactPublicObjects`; reuse `_EventRead`, `_CompressedBodies`, `_EventLane`, `_RespondentEvents`.
- `rawlsing_next/_pre553_w03_cold_compact.py` — add a persisted-row entry to `ColdCompactBuilder`/a sibling builder that accepts selector rows, compressed body chunks and group keys; reuse `_compress_body_chunk`/`_BodyCacheWriter`/`_read_bodies` semantics. Do not duplicate the builder.
- Tests: `rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py`, `rawlsing_next/tests/test_pre553_w03_w04_completion.py`, and a focused `rawlsing_next/tests/test_pre553_parquet_carrier_compact.py` if the existing files are too broad.
- No changes to `pre553_c11_repository.py`, `pre553_carrier_execution.py`, `pre553_empirical_query.py`, `pre553_batch_runner.py`, `field_forge_conditional_support.py`, or the native ABI.

**Compact sidecar layout (proposed, minimal):**

- `compact_events.parquet` — one row per event, sorted by exact event key/ref key: `event_ref_json`, `typed_state`, `native_question_ref_json`, optional `canonical_question_ref_json`, optional `component_ref_json`, `authority_identities_json`, `raw_response_value_json`, optional `canonical_response_value_json`, `multiplicity_order_rank_json`, `response_event_id_json`, `empirical_universe_ref_json`, `scoped_respondent_ref_json`, `canonical_event_body` binary. Parquet+zstd; body SHA equals the event ref content hash; columns aligned.
- `compact_manifest.json` or full-manifest optional fields — `storage_mode`, schema, release/source/semantic/replay refs/hashes, M01-M18 coverage, `full_event_relation_digest`, `selector_body_group_digest`, `event_count`, `event_states`, member SHA-256s, full event table member hash if retained. The full manifest hash must cover the compact fields/member hashes (extend the unsigned manifest material for compact mode; legacy full manifests unchanged).
- Compact-only `reopen_compact` must verify the full manifest hash/member hashes, compact member hashes, selector/body/group hashes, `full_event_relation_digest` binding, release/replay/coverage identity, exact event ref/content/typed-state/order/authority, closure, `_make_validated_release`, and exact path. It must not decode `respondent_events.parquet` rows or construct all `RespondentEvent`s.

**Invariants:**

1. Exact release identity: same source/release/semantic/replay refs, `release_id`, `source_release_manifest_hash`, `semantic_release_hash`, M01-M18 coverage, closure refs.
2. Exact event semantics: selector refs/content hashes/typed state/order/authority/raw/canonical/multiplicity/occurrence; body bytes hash; sorted entries/by-respondent; non-events/internal records exact.
3. No full relation/object reconstruction in compact open: no `_object_from_row` loop over `respondent_events`, no `_read_rows("respondent_events")`; only compact selectors/bodies and non-event/internal/identity tables; repository stores `_EventLocator`s; selected event materialization only.
4. Integrity: full manifest/member/relation checks; compact sidecar is a canonical content-addressed member; full event relation digest admitted at persist and bound; no disposable cache/trusted-cache assumption; no fuzzy selectors.
5. Bounded-batch saving: `persist_compact` streams selectors/body chunks/groups; does not call `_relation_objects` over compact `public_objects`; no all-event in-memory list. Full upstream construction remains the existing `build_*` path.
6. No new engine/query/authority registry; no DuckDB; no changes to I03/I05/Batch/FieldForge semantics.

**Meaningful acceptance checks (tiny, exact, no 100k):**

- Persist a compact release; compact-only fresh process `reopen_compact` returns the same `release_ref`, `replay_manifest.ref`, `source_release_manifest_hash`, `semantic_release_hash`, `m01_m18_coverage`; `C11Repository` accepts; `resolve_object_exact` materializes selected events equal to eager.
- `CarrierNeutralResearchExecutor.execute_i03/execute_i05` canonical-JSON material equals the eager/full-reopen baseline for the existing Route B fixture cases (routed-ordered-repeated, missing optional weight, valid empty); `BatchExecutionRunner` unit results match.
- Compact open reads no `respondent_events.parquet` rows (instrument `_read_rows`/`pyarrow.ParquetFile.iter_batches`; assert compact sidecar/non-event paths only); full event table member hash is checked by bytes only if retained.
- Corrupt/missing compact sidecar/member/selector/body/group/hash/identity/coverage -> typed `ParquetCarrierError`; no fallback to full objects or disposable cache.
- Tiny stream-equivalent digest witness: exact `_logical_digest(rows)` equals the streaming canonical-JSON-array digest for a synthetic event relation; if compact-only omits full rows, the `full_event_relation_digest` must be bound and checked.
- FieldForge: if a direct receiver fixture exists, the I03 `EmpiricalFact` and `produce_exact_conditional_support_profile` result/ref are exact; otherwise document that FieldForge is not directly called by the C11 carrier and preserve the fact-level boundary.

## 8. Distinctions and boundary

- **Bounded-batch saving vs full upstream construction:** the grant saves an already-validated compact release in batches; it does not perform or replace the upstream I02 semantic construction/validation. The existing `build_cold_source_backed_c11_release` remains the construction owner.
- **Selective disk-backed access vs in-memory lazy object reconstruction:** the compact sidecar is the disk-backed selector/body/group representation; `_CompactPublicObjects`/`_EventLane`/`_EventLocator` is the in-memory lazy representation. The grant connects the two; it does not create a new lazy-object engine or a new query engine.
- **No whole MCR/final/economic acceptance:** this decision enables the next carrier code grant only. The final 12-ID/same-candidate/external MCR proof, economic/100k receiving, source/native/science/actor authority, protected merge, and universal35 claims remain outside. The current repaired pilot in the other worktree is untouched and not polled.
