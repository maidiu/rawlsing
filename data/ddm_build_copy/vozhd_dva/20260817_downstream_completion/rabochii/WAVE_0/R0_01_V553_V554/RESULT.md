# R0-01 Result — V553/V554 Boundary and POSTG5-004

**Worker:** R0-01  
**Status:** COMPLETE_WITH_FINDINGS  
**Branch:** `agent/vozhd-dva-r0-01-v553-v554`  
**Base SHA:** `958983139b8f75dc5cda65d5bf71b376d17820df`  
**Implementation head audited:** `b24a758133985f894548c3d50db9bb1536cc9b4b`  
**Draft PR:** #39 → `agent/vozhd-dva-wave0-integration`

## 1. Repair performed

`POSTG5-004` remains repaired on the V553 consumer side. Canonical V552J publishes the current structural join/input/handoff surface; V553 no longer requires or recreates `packets/v552j_structural_handoff_packet.json`. No V550–V552J file and no V554 production-semantic file was modified.

The Vozhd Dva review of PR #39 identified one defect in the first repair: the new adapter treated path existence as sufficient evidence of a canonical surface and converted Parquet read failures into empty frames. That could collapse corruption or partial publication into apparent emptiness.

The review correction makes the V552J→V553 trust boundary fail closed. `ddm_v553_canonical_harmonization.py` now requires and verifies the full V552J publication needed at this boundary:

- `manifest.json` with the frozen pipeline-boundary contract, V552J schema/compiler versions, PASS run integrity, coherent producer identity, and the exact canonical artifact-name set;
- `packets/v552j_structural_join_index.parquet` as declared canonical output;
- `audits/v552j_join_audit.parquet` as declared canonical output;
- `packets/v552j_v553_input_index.parquet` as the declared V553 compatibility input;
- `packets/v552j_to_v553_handoff_index.parquet` as the declared V553 compatibility handoff;
- `manifest/v552j_readiness_report.json`;
- `manifest/v552j_v553_handoff_manifest.json`.

For each required Parquet artifact the adapter checks declaration count, exact path and artifact kind, schema/compiler version, producer-declared SHA-256, producer-declared row count, full readability, required columns, row-level schema/compiler identity, and run/source/wave/country scope. It also requires the structural-join, V553-input, and V553-handoff row counts to agree, requires the two V553 compatibility indexes to be identical, and checks the handoff-manifest input path and probe/temporal row counts against the verified index.

The boundary now classifies transport state explicitly:

- `VALID_PRESENT` — complete verified publication with V553 rows;
- `VALID_EMPTY` — complete verified publication with zero join/input/handoff rows;
- `MISSING` — required root/document/artifact absent;
- `UNREADABLE_OR_CORRUPT` — required document/artifact exists but cannot be parsed/read;
- `SCHEMA_INVALID` — declaration, version, required-column, identity-shape, or handoff-manifest schema is invalid;
- `INTEGRITY_INVALID` — hash, row-count, state, scope, or cross-artifact consistency fails.

Only `VALID_PRESENT` and `VALID_EMPTY` set `surface_valid=true`. Invalid statuses set both `surface_valid=false` and `surface_present=false`, and the supported V553 harmonization build raises `V553CanonicalSurfaceError` before producing a V553 report. Path existence therefore cannot authorize the surface.

`VALID_EMPTY` remains distinct from failure: it is transport-valid but is marked `valid_empty_v552j_surface` rather than being promoted to a complete semantic wave.

The supported compile entrypoints remain routed through this canonical adapter. The historical packet loader remains only in the retained shadow implementation and is still covered by `POSTG5-005` rather than being reopened here.

## 2. Tests and executable evidence

The focused regression file is `data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py`.

Its positive fixture now reproduces the current V552J publication contract rather than merely dropping two Parquet files into place. It builds the producer manifest with hashed declarations, canonical join/audit artifacts, both V553 compatibility indexes, readiness, and V553 handoff manifest, while explicitly asserting that the obsolete structural-handoff packet does not exist.

Adversarial coverage proves:

1. a complete verified publication is accepted and preserves relation/target/driver/channel/horizon identity;
2. a complete zero-row publication is classified `VALID_EMPTY`, not missing;
3. deleting one required canonical handoff index yields `MISSING` and the V553 build raises;
4. corrupting the canonical V553 input index yields `UNREADABLE_OR_CORRUPT` and the V553 build raises;
5. a simulated permission/read failure on the canonical handoff index yields `UNREADABLE_OR_CORRUPT` and the V553 build raises;
6. removing a required index column while updating the file hash/row count still yields `SCHEMA_INVALID` and the V553 build raises;
7. leaving both index paths present while corrupting `manifest.json` cannot produce a valid/present surface;
8. both supported V553 compile entrypoints still import the canonical adapter.

Execution evidence available in this worker environment:

- `python -m py_compile /mnt/data/r0_01_fix/ddm_v553_canonical_harmonization.py /mnt/data/r0_01_fix/test_postg5_v552j_v553_consumer_contract.py`: **PASS**.
- `PYTHONPATH=/mnt/data/r0_01_fix/mini pytest -q data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py`: **PASS — 8 passed in 0.08s**. The mini package used the exact updated adapter/test source and contract-compatible stubs for the unavailable repository checkout; the adversarial boundary behavior itself executed.
- repository-root pytest on the connected GitHub checkout: **NOT RUN** because this environment exposes the repository through the GitHub connector rather than a network-authenticated working tree, and PR #39 has no GitHub Actions run/status. This limitation is stated rather than converted into a pass.

## 3. V552J → V553 contract actually observed

| V552J information/state | Producer surface | V553 repaired consumption | Preservation |
|---|---|---|---|
| publication integrity | main manifest declarations, hashes, row counts, versions | fail-closed surface verification | preserved and enforced |
| typed empty vs failure | typed state + verified zero-row artifacts | `VALID_EMPTY` distinct from missing/corrupt/schema-invalid | preserved |
| scope identity | manifest + indexes | run/source/wave/country checked before use | preserved/enforced |
| structural identity | relation/target/driver/channel/horizon fields | per-wave structural inventories; later sparse temporal-key logic | preserved at entry |
| structural provenance | V552 structural fact IDs, temporal-key-source IDs, lanes/grain, V552J packet/input IDs | V553 temporal-key basis and sparse provenance | preserved in sparse path |
| permission | read/probe/temporal-field/runtime permission fields | key authority/candidate/probe status and handoff authority context | preserved materially |
| comparability | comparability requirement/status and blockers | comparable-key authorization and noncomparability handling | preserved materially |
| temporal obligation | must-temporalize / anchor-required | temporal key/anchor authorization logic | preserved materially |
| negative/blocked state | blocker reason, unresolved/probe-only/audit states | probe/fallback keys and blocker classes | preserved as typed non-readiness |
| readiness/handoff state | readiness + V553 handoff manifests | state-coherent boundary context | preserved and cross-checked |

The significant architectural fact remains unchanged: `ddm_v553_temporal_pressure.py` already contains a richer canonical-aware sparse-key path carrying exact structural dimensions, V552/V552J lineage, permission classes, comparability, probe-vs-field authorization, and typed known-unknown states. `POSTG5-004` was a V553 entry-contract defect; it did not justify recreating a V552J legacy packet.

## 4. V553 → V554 preservation/loss trace

| Information/state | V553 production | Current V554 consumption/transformation | Finding |
|---|---|---|---|
| year/wave coordinate | wave anchors, sparse observations, country-year pressure rows | regional seed rows consume year/wave context | substantially preserved |
| pressure point/band/status | country-year pressure field/component breakdown | bounded seed strength/readiness | transformed, aggregate |
| exact relation/target/driver/channel/horizon identity | sparse temporal-key/observation surfaces | current regional-seed path does not carry the exact sparse key set | **loss** |
| comparable temporal key / grain / semantic signature | V553 comparable-key and temporal-key indexes | not represented in current regional seed contract | **loss** |
| V552/V552J lineage | sparse V553 basis/provenance | not propagated into regional seed rows | **loss** |
| permission/comparability state | authority ledger, blocker classes, absence/noncomparability registers | compressed into thinner seed readiness | **conflation risk** |
| negative authority / known unknown / absence | explicit V553 typed registers | no equally typed V554 seed representation | **loss/conflation risk** |
| uncertainty/confidence | anchor confidence, penalties, authority state | some survives aggregate pressure path | partially preserved |
| persistence/drift/rupture | temporal comparison machinery; event slots often reserved/not supplied | no strong typed lineage into V554 | **semantic gap** |
| structural identity in aggregate path | synthetic `shared_*::<semantic_signature>` identifiers | can reach V554 instead of exact upstream IDs | **placeholder hazard** |

The Vozhd review explicitly accepted these semantic audit findings for later synthesis. No V554 production semantics were changed in this fix.

## 5. Producer-consumer obligations retained for later vertical slices

V553→V554 must preserve, or losslessly transform with reversible lineage:

- stable temporal/comparable key plus key grain;
- source/country/wave/year and historical anchor identity;
- exact authorized relation/target/driver/channel/horizon IDs;
- semantic signature;
- pressure/component state with direction/magnitude only where authorized;
- confidence/uncertainty and interpolation status;
- comparability/noncomparability;
- absence, blocked, probe-only, unresolved, audit-only, and negative-authority states as distinct values;
- V552 structural-fact / temporal-key-source lineage and V552J packet/input lineage;
- persistence/drift/rupture/event state once authority exists, without inventing missing event semantics.

## 6. Remaining cross-hooks for Vozhd Dva

### R0-01-XH001 — retained shadow orchestration (`POSTG5-005`)

A retained thin/orchestration specification still names the obsolete `v552j_structural_handoff_packet` dependency. The supported V553 compilers are repaired and fail closed, but the shadow path remains a future regression risk.

**Needed:** remove, hard-disable, or contract-test the stale orchestration path during vertical/horizontal consolidation.

### R0-01-XH002 — authoritative sparse V553 surface must reach V554

Current V554/later paths do not carry the full sparse V553 structural key, typed noncomparability/absence state, and upstream lineage.

**Needed:** adjudicate the minimum governed V553→V554 typed handoff before broad semantic deepening.

### R0-01-XH003 — rupture/persistence semantics

V553 reserves rupture/event structure but event authority is often not supplied. Later stages need persistence/drift/rupture without manufacturing rupture from temporal distance or pressure deltas.

**Needed:** define the authorized event/rupture source and preservation contract in a later vertical slice.

No new cross-hook was created by the fail-closed review correction.

## Terminal summary

- `POSTG5-004`: repaired on the V553 consumer side; V552J remains untouched.
- Vozhd review fail-closed concern: **resolved** at implementation head `b24a758133985f894548c3d50db9bb1536cc9b4b`.
- Missing, unreadable/corrupt, schema-invalid, integrity-invalid, valid-empty, and valid-present surfaces are now distinct.
- Path existence cannot imply a valid canonical consumer surface.
- The full required V552J publication/manifest set is verified before V553 accepts the boundary.
- Focused adversarial executable harness: **8/8 passed**.
- V554 production semantics remain untouched; the previously accepted semantic cross-hooks remain for Vozhd synthesis.
- Draft PR #39 remains open and unmerged.
