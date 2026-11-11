# SAVED_ACCESS_CONTRACT_R1 — decision

**Verdict:** `IMPLEMENT_WITH_EXISTING_CONTRACT`

**Decision:** The existing governed C11 repository and executor already support the existing W03 compact/selective event representation and lazy exact event access. The **missing work is confined to the carrier's persisted compact form and compact reopen path, plus the private persisted-row constructor in the existing compact lane**, not the repository, query executor, I03/I05/Batch consumers, or a new engine. A bounded carrier-side compact sidecar plus `reopen_compact` can use the existing representation from saved artifacts without reconstructing all relations/objects or changing C11 release identity, semantics, authority, or native query results.

No consequential semantic contract change or user decision is required for this seam. The storage artifact is a content-addressed compact projection bound to the existing full release manifest/release identity; the full I02 validation remains at construction/admission. The only fallback if the integrity owner rejects admission-time compact-sidecar binding is to re-stream the full event relation for the exact logical digest; that is a bounded strict mode, not a different contract.

## Exact source and review position

- Current implementation read via `git show` from `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-completion-r1` at `16f97fe23e395d6807a13a4fa5ea0c2b96bccd69` (`Record bounded setup memory and repair retained selector mismatch`).
- Production source `f329b8c041af1f70291535a27cfde13af1b59642` is equivalent for every file cited below (`git diff 16f97fe..f329b8c04 -- <cited files>` is empty).
- Reviewer worktree remains `pyat-w03-w04-mcr-engineering-review-r1` at `475035790098d11751012308b7fd62576987502d`; no checkout/reset/rebase or production change.
- Own `AGENTS.md` read: `/Users/matthewsmith/Desktop/Rawlsing/AGENTS.md` (real worker returns: verify durable receipt/artifacts, decide demonstrated scope, preserve independence, no invented authority).

## Why this is the existing-contract answer

The existing compact representation is not a proposal; it is already implemented and accepted by the current governed consumers:

- `_CompactPublicObjects`, `_EventRead`, `_EventLane`, `_CompressedBodies`, `_RespondentEvents`, `_EventLocator` in `rawlsing_next/_pre553_c11_execution_view.py:48-206`.
- Streaming `ColdCompactBuilder` in `rawlsing_next/_pre553_w03_cold_compact.py:38-147`.
- `C11LogicalRelease` explicitly accepts compact `public_objects` and exact locators (`rawlsing_next/pre553_c11_repository.py:26-67`); `C11Repository` handles `exact_entries()` and stores `_EventLocator`s (`:115-139`); `resolve_object_exact` materializes only the selected event (`:107-113`).
- `_build_release_index` uses `public.by_respondent` for compact releases and `_select_respondent_events` yields `_EventRead` selectors (`rawlsing_next/_pre553_query_predicate.py:18-128`); `_semantic_value` consumes `_EventRead` without full event bodies (`rawlsing_next/_pre553_query_common.py:249-255`).
- `CarrierNeutralResearchExecutor.execute_i03/execute_i05` is repository-driven and unchanged (`rawlsing_next/pre553_carrier_execution.py:403-479`); `BatchExecutionRunner` accepts the same `C11Repository` (`rawlsing_next/pre553_batch_runner.py:385-430,536-624`).
- The direct FieldForge receiving owner `produce_exact_conditional_support_profile` consumes an exact `EmpiricalFact`/query/permissions (`rawlsing_next/field_forge_conditional_support.py:467-580`), not C11 events; the compact release must preserve the I03 fact identity, not add a new C11-to-FieldForge dependency.

What is missing is confined to `rawlsing_next/pre553_parquet_carrier.py`: `persist` iterates `release.public_objects` (`:221-258`), so persisting a compact release materializes every event; `reopen` reads every relation (`:297-376`) and reconstructs every object via `_object_from_row` before `_make_validated_release`. The compact lane and body cache exist, but there is no canonical saved compact sidecar and no `reopen_compact`.

## Bounded next implementation grant

**Add a canonical compact event sidecar and compact reopen to the existing carrier only.** Reuse the existing compact representation, `ColdCompactBuilder`/`_CompactPublicObjects`, `_make_validated_release`, `C11Repository`, `CarrierNeutralResearchExecutor`, `_ReleaseIndex`/`_select_respondent_events`, and `BatchExecutionRunner`. No new engine, no DuckDB dependency, no repository/executor/query/FieldForge ABI change.

Exact files:

- `rawlsing_next/pre553_parquet_carrier.py` — add `persist_compact`/`reopen_compact` (or `persist(..., compact=True)` plus `reopen(..., compact=True)`), a `CompactEventSidecar` manifest, selector/body/group member writers, and exact sidecar verification. Keep full `persist`/`reopen` behavior unchanged for legacy/full releases.
- `rawlsing_next/_pre553_c11_execution_view.py` — add the private persisted-selector/body constructor needed to rebuild `_CompactPublicObjects` from sidecar rows without materializing all `RespondentEvent`s; reuse `_EventRead`, `_CompressedBodies`, `_EventLane`, `_RespondentEvents`, `_CompactPublicObjects`.
- `rawlsing_next/_pre553_w03_cold_compact.py` — add a persisted-row builder/`ColdCompactBuilder` entry that accepts selector/body/group rows and compressed chunks, reusing `_compress_body_chunk`/`_BodyCacheWriter` semantics. Do not duplicate the builder.
- Tests: extend `rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py` (compact persist/reopen, fresh process, I03/I05 exact material, no full event-row decode) and `rawlsing_next/tests/test_pre553_w03_w04_completion.py` (sidecar/accelerator separation, corruption/missing/member/digest fail-closed, canonical sidecar survives accelerator deletion). Add a focused batch/FieldForge-fact identity witness only if the existing Route B fixture directly exercises that receiver; otherwise state the direct-call boundary.
- No changes to `rawlsing_next/pre553_c11_repository.py`, `pre553_carrier_execution.py`, `pre553_empirical_query.py`, `pre553_batch_runner.py`, `field_forge_conditional_support.py`, or the native ABI.

Exact invariants and acceptance checks are in `01_API_REPRESENTATION_CONTRACT_AND_GRANT.md`: exact release/source/semantic/replay/coverage identity, manifest/member hashes, selector/body/group hashes, full event relation digest binding, sorted selector/event order, `_make_validated_release` seal, exact `resolve_object_exact` selected-event materialization, no `respondent_events.parquet` row decode in compact open, I03/I05/Batch canonical-JSON equality to the eager baseline, typed corruption/missing errors, and no fuzzy/trusted-cache fallback. Heavy benchmarks and the full 12-ID/final MCR acceptance remain outside this grant.

## Evidence versus inference

- **Source evidence:** the exact APIs, line references, and tests cited in `01`/`02`; the existing compact lane and repository/executor behavior; the full carrier's current materialization path; the existing Route B/C11/I03/I05 tests (`test_pre553_c11_cold_reopen_i03.py:63-130`, `test_pre553_w03_w04_cold.py:90-195`, `test_pre553_w03_w04_completion.py:328-345`).
- **Inference:** expected memory/fresh-process speed benefit and the compact sidecar's bounded-memory saving; no heavy benchmark or 100k run was performed. The grant's acceptance checks are structural and exact-output based, not a performance claim.
- **Not claimed:** whole MCR/12-ID/final code/economic acceptance; original35/source/native/science/actor authority; universal35 support; production merge; a new query/authority engine.

**Next action:** authorize the bounded carrier-side compact-sidecar/reopen grant above; keep the full I02 validation at admission and the existing full carrier mode as legacy/recovery. Final full-code/economic receiving still resumes at the same immutable HQ-frozen candidate with all 12 obligations and external MCR proof.
