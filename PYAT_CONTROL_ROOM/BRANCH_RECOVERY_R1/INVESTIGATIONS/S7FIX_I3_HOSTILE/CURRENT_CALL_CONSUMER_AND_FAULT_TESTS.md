# Current call consumers and fault tests

## Exact current cut

- Startup: `d0342290b257f85c3e8931f9962e0aecabc84ed3`.
- Current PRE-MAIN recheck: `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- `rawlsing_next` tree: `1d88d3fbb1d18dadfda946d9cd7f309d84afa479`.
- `pre553_source_relations.py` current blob: `5b67e3f98a5faf95a6c82700af2346fef6e306a5`.
- `pre553_physical_decoder.py` current blob: `8732e34d0ea3f4cfffd7d33ee00f258dbc2d65dd`.
- `pre553_temporal_comparability.py`: **ABSENT**.

## Import and call map

### `pre553_source_relations.py`

AST import audit over non-test `rawlsing_next`:

- **No production import found.**
- Test import: `rawlsing_next/tests/test_pre553_source_relations.py:13`.
- String map only: `rawlsing_next/fiabc_succession_producer.py:59` names the path in `F008`; this is not an import or call.
- `pre553_temporal_comparability.py` is absent, although S7-FIX member first-consumer evidence names it.

Current API symbols present in the outer class only:

- `SourceRelationResolver.__init__`
- `SourceRelationResolver.require`
- `SourceRelationResolver._validate_positive`
- `SourceRelationResolver.decide`
- `SourceRelationResolver.resolve_exact`
- `SourceUniverseRelation@1.0.0`, `RelationDecision`, `SourceRelationAuthorizationError`, `SourceRelationIntegrityError`

There is **no current nested `_make_sealed_source_relation_owner.SourceRelationResolver`**. The nested owner is historical only. The corrected mapping's nested member `current_implementation_candidate` still names the outer class; that is the current ownership conflation.

### `pre553_physical_decoder.py`

Static production import sites (AST, non-test):

- `rawlsing_next/pre553_source_native_preimage_adapter.py:30`
- `rawlsing_next/wave1_r5_q86_c11_projection.py:17`
- `rawlsing_next/fiabc_lits_common_representation.py:20`
- `rawlsing_next/pre553_physical_c11_bridge.py:10`
- `rawlsing_next/fiabc_lm2_r1e_common_c11.py:24`
- `rawlsing_next/fiabc_final_oracle_freeze_producers.py:53`, `:1247`
- `rawlsing_next/ee_p2x_darwin_stage_backend.py:713`
- `rawlsing_next/pre553_source_backed_c11_facade.py:35`
- `rawlsing_next/pre553_route_b_production.py:53`
- `rawlsing_next/fiabc_lits_i_representation_authority.py:20`
- `rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py:23`

Actual execution path for the historical join:

```text
materialize_native_preimages
  -> PhysicalSourceIncidence.iter_cells()
  -> iter_batches()
  -> nested emit(...)
  -> PhysicalCell tuple
  -> build_validated_source_backed_c11_release / Route B / C11
```

`pre553_source_native_preimage_adapter.py:548` calls `incidence.iter_cells()`.
`pre553_source_backed_c11_facade.py:587` consumes `PhysicalSourceIncidence` and
builds the validated C11 release. `pre553_route_b_production.py` accepts
`PhysicalSourceIncidence` as a source transport.

This is a real current Python code path, but it is not the historical
`emit` behavior: current `emit` has AST `77d9be6c955342b971b1f0393833e7e0c557c913`
and uses `_jsonable`; the historical four-variant AST is
`4f7cd7ccb7a06b3d6a4f75f19c65dd16d6911445` and uses `_physical_value`.

### Current PR526 custody contract

`PhysicalSourceIncidence` carries `_SourceSnapshot` (`pre553_physical_decoder.py:210`):

- `_acquire_source_snapshot()` copies input through a read-only `O_RDONLY` source fd into a private temp file, `fchmod 0400`, opens it `O_RDONLY | O_NOFOLLOW`, verifies matching device/inode/size, unlinks the path, and verifies `_sha_fd` again.
- `_SourceSnapshot._ensure_read_only()` checks `O_RDONLY` with `fcntl` and regular-file type.
- `iter_batches()` calls `verify_source_identity()` before lazy reads, uses `/dev/fd/<fd>`, checks `snapshot.check_stable()` after each SAV chunk, and verifies the snapshot after full DTA reads.
- `source_custody` exposes contract, digest, snapshot size, unlinked state, reader binding and access mode.

This is current sourcefree behavior at the decoder test scope. It does not prove
behavioral equivalence to historical `emit`; it is a different implementation with
its own tests.

## Current test receipts

Commands run from the review worktree with
`PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0` and
`pytest -q -p no:cacheprovider`:

| Suite | Result | Scope |
|---|---|---|
| `test_pre553_source_relations.py` | **24 passed** | current outer source-relations API, test-only |
| `test_universal_source_byte_custody.py` | **26 passed** | current PR526 byte custody / snapshot / TOCTOU |
| `test_universal_source_projection.py` | **31 passed** | current native preimage/decoder positive path |
| `test_pre553_sr06_decoder_carrier.py` | **16 passed, 1 skipped** | current decoder carrier |

The source-relations tests include:

- `test_no_relation_and_shared_labels_or_ids_remain_distinct_by_default`
- `test_provenance_and_alias_can_never_be_positive_relation_authority`
- `test_conflicting_positive_and_denied_relation_receipts_fail_closed`
- `test_relation_authority_must_be_available_by_exact_historical_ref`
- `test_same_exact_relation_inputs_replay_identically_independent_of_registration_order`
- `test_i03_guard_rejects_alias_or_provenance_substitution_for_semantic_equivalence`

The decoder suite covers replacement after snapshot acquisition, replacement
between hash gate and acquisition, writable-fd denial, lazy snapshot-only reads,
private-path replacement, mmap/write attempts, closed-snapshot release and typed
POSIX refusal. These are current sourcefree tests; they do not execute original
survey corpora or the historical F7/P07 sealed-owner attacks.

## ABI / ownership / schema / lifecycle gaps

| Axis | Current status |
|---|---|
| Source-relations ABI | Outer class present; current AST differs from historical S4 blob; nested owner absent |
| Source-relations ownership | Test-only; no production import; stale first-consumer path |
| Source-relations schema | `SourceUniverseRelation@1.0.0`, `RelationDecision`; current tests exercise exact refs and denial |
| Source-relations lifecycle | Constructor pins `AuthorityRegistry`; exact historical authority must resolve; no current production caller |
| Decoder ABI | `PhysicalSourceIncidence.iter_batches` / `PhysicalCell`; current `emit` is a different AST from historical |
| Decoder ownership | Production static imports; current tests execute the native preimage/decoder path |
| Decoder schema | `PhysicalCell`, `PhysicalVariable`, `SOURCE_CUSTODY_CONTRACT`; current tests cover physical metadata and source identity |
| Decoder lifecycle / byte custody | `_SourceSnapshot` read-only private copy, `/dev/fd`, stable checks, unlink/close; 26 current tests |
| Historical nested owner | Not current; no ABI/consumer execution |
| F7/P07 and HQ240/HQ245–HQ248 | Preserved as historical source/review negatives; not rerun; no native C compiled |

## Fault/falsifier status

- **Current outer source relations:** 24 tests pass at test scope; this is not a
  production consumer proof.
- **Current decoder PR526:** 26 tests pass, plus 31 projection and 16/1 carrier
  tests; this is current sourcefree behavior, not historical `emit` equivalence.
- **Nested sealed owner:** current absent; historical F7/P07 defect negatives
  preserved under nested families, not rerun.
- **HQ240/HQ245–HQ248:** preserved historical evidence; not rerun; unsafe native C
  was not compiled.
- **No production whole-service consumer** was executed.

## Verdict for current ABI

`CURRENT_OUTER_SOURCE_RELATIONS_PRESENT__TEST_ONLY__CURRENT_NESTED_ABSENT__CURRENT_EMIT_DIFFERENT__PR526_CURRENT_TESTS_PASS__NO_PRODUCTION_CONSUMER__NOT_BEHAVIORAL_EQUIVALENCE`.
