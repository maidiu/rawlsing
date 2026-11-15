# Rawlsing V550–V552J Repair — G4 Final Closure Wave

Gate G4 is PASS. Canonical V550/V550J/V551/V551J/V552/V552J producer surfaces and the shared `rawlsing_pipeline_boundary_v1` contract are merged. The remaining worker work is consumer closure and final regression; no new semantic redesign is authorized.

All three workers must read `index.json`, `PROCEDURE.md`, `WORKER_PLAN.json`, `GATE_STATUS.json`, all assigned issue records, relevant `closed.json` and `deferred.json`, and the current merged producer contracts before editing. All PRs target `agent/v550-v552j-repair-integration`.

## W01-final — Section85 exact producer binding

You are **W01-final**. Work only on branch `agent/v550-v552j-w01-section85-final`.

Assigned mandatory issues still awaiting closure:
- `ORCH-003`
- `ORCH-010`

`ORCH-002` is already terminally resolved and must remain preserved.

Write domain: `section85/**` only.

Replace the post-G2 generic/pending adapters with exact bindings to the now-merged V551J and V552J producer contracts. Section85 must verify the supported shared boundary contract, producer schema/compiler version, `run_integrity_status`, `evidence_status`, `downstream_permission_status`, exact producer run/source/wave/country-or-shard identity, required manifest-declared canonical Parquet artifacts, and producer-declared serialized SHA-256 before relying on a producer surface. Do not resurrect legacy readiness booleans, cardinality/nonempty gates, or `bool(nonempty_json)` success logic.

For V551J, valid `PASS/VALID_EMPTY/NOT_APPLICABLE` and `PASS/PRESENT/DENY` review-only states must remain distinguishable from producer failure. For V552J, a nonempty manifest is not itself readiness; `OBSERVED_ZERO`, `NOT_APPLICABLE`/valid empty, and `APPLICABLE_UNRESOLVED` must remain distinct. Evidence-dependent Section85 operations may proceed only when the typed producer state explicitly allows them.

Preserve all W01-A repository-relative path and source-authority work. Do not edit stage builders, W05 lineage/orchestration files, or issue-register governance.

Run focused Section85 tests for exact V551J/V552J version/hash/scope binding, valid empty, review-only, unresolved, observed zero, legacy boolean rejection, malformed status, and nonempty-blocked manifest rejection. Return `ORCH-003` and `ORCH-010` with terminal issue results and the exact WORKER_PLAN machine-readable report.

Commit and open a draft PR against `agent/v550-v552j-repair-integration`.

## W05-final — end-to-end lineage/orchestration closure

You are **W05-final**. Work only on branch `agent/v550-v552j-w05-infra-final`.

Mandatory issues still awaiting terminal closure:
- `LIN-001`
- `LIN-002`
- `LIN-004`
- `LIN-007`
- `LIN-008`
- `LIN-010`
- `ORCH-001`
- `ORCH-007`
- `ORCH-008`

`LIN-003`, `LIN-005`, `LIN-006`, `LIN-009`, `LIN-011`, `ORCH-005`, and `ORCH-006` are already terminally resolved and must remain preserved.

Use the same W05 lineage/orchestration/publication write domain defined by WORKER_PLAN. Do not edit V550/V550J/V551/V551J/V552/V552J semantic builders or Section85.

All stage-side hooks now exist. Replace the intentional `PARTIAL_AWAITING_CROSS_HOOK` stops with exact end-to-end verification of the merged producers. The resolver/smoke path must bind one coherent inherited run identity and exact source/wave/country-or-shard scope across V550, V550J, V551, V551J, V552, and V552J; verify supported contract/schema/compiler versions and producer-declared serialized artifact hashes before semantic use; distinguish run integrity from evidence state and downstream permission; accept lawful valid-empty/no-applicable states without nonempty requirements; reject malformed/failed/mixed-version/mixed-run/mixed-scope producers; require canonical Parquet; and consume only manifest-declared current artifacts.

Remove obsolete/dead V552 contract requirements such as `v552_input_provenance_manifest.json` where the effective merged producer no longer declares them. Remove atom-count/nonempty smoke failure semantics. The all-wave smoke must no longer intentionally stop before V552/V551J/V552J merely because hooks were absent at G2. Preserve CLOSED_35_WAVES, Asian Barometer W6 exclusion, same-run V550/V550J selection, association-mode applicability scoping, fail-closed malformed status, and stale-safe publication.

Terminally verify the shared closures for `LIN-007`, `LIN-008`, `ORCH-007`, and `ORCH-008` across the actual merged stage hooks rather than merely checking W05 helper code in isolation.

Run focused lineage + smoke tests and, where available, governed multi-wave smoke fixtures. Required regression classes include valid-empty versus corrupt, missing/unknown producer version, producer hash tamper, cross-run/cross-scope mixing, zero-promotable V551, zero-joint-evidence V551J, unresolved V552, V552J typed absence, stale reused-run artifact removal, CSV-only rejection, and no ghost V552 dependency. Return every listed issue with a terminal result or an evidence-backed blocker; do not invent downstream semantics.

Commit and open a draft PR against `agent/v550-v552j-repair-integration`.

## W06-C — final regression / canaries

You are **W06-C**. Work only on branch `agent/v550-v552j-w06-final-regression`.

This phase owns no new semantic issue IDs. It is the final independent regression lane required by G5. Write only W06-namespaced test/fixture/regression artifacts unless an existing W06 QA runner requires a narrowly scoped test-only adaptation. Do not modify stage semantics, W05 orchestration, Section85, or issue-register governance.

Deliver and execute, where the repository/runtime permits:

1. **EVS 1999 / Iceland canary** through the repaired V550→V552J contract path, using governed current producer contracts and typed-state assertions. Preserve the canary's source/wave/country identity exactly; no wrong-source or fuzzy scope rescue.
2. **CLOSED_35_WAVES regression** across the governed wave set, using existing governed upstream shards where possible. Asian Barometer W6 must remain excluded. Verify typed run integrity/evidence/downstream-permission propagation rather than requiring nonzero evidence at every stage.
3. **Downstream absence/zero leakage regression** for deferred `WATCH-001`, `WATCH-002`, and `WATCH-006`: confirm V553/V554/thin downstream consumers do not turn missing/absent/unresolved upstream evidence into authoritative numeric zero or scalar readiness. Do not redesign V553–V558; if an active regression is proven, report the exact file/path/value flow and blocker rather than silently broadening scope.
4. Cross-stage negative controls: tampered producer bytes, unsupported producer version, cross-run/source/wave/country-or-shard mismatch, stale reused-run artifact, valid empty, applicable-unresolved, and true observed zero.

The final report must state exactly which commands actually ran, which fixtures/data were available, and which assertions passed. Never claim an unexecuted 35-wave or canary run. If full runtime data are unavailable, commit executable regression coverage plus the strongest available bounded run, and report the limitation precisely.

Return a machine-readable report using the WORKER_PLAN fields, with `primary_issue_ids` empty, explicit results for the EVS canary, 35-wave regression, WATCH-001/002/006 containment, downstream typed-absence regression, and `no_unowned_files_changed`.

Commit and open a draft PR against `agent/v550-v552j-repair-integration`.
