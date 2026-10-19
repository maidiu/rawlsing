# E41 hand-back — P41 (N10W progressive serving) and A41 (N11 acceptance assembly)

## To P41 — consume the computed N10E product

Contract: `N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER_EXT@1.1.0`
(`empirical_slice_provider_contract.md`). P41 can ingest:

* `artifacts/computed_slice_evidence.json` — 18 producer-derived slices, each with
  `route`, `producer_fact_state`, `generated_evidence_ref`,
  `composed_result_identity_hash`, `coverage_state`, `consumer_result_state`.
* `artifacts/slice_consumer_receipt.json` — 18 real consumer receipts with
  consumer result states + identity hashes (positioned consumer + original E04
  `NONPARENT_OPTIONS`).
* Direct route reuses the accepted provider function object; discovery/recursive
  routes carry the exact `discovery_receipt_refs` / `recursive_handoff_refs` /
  `recursive_lineage_refs` needed for progressive conditioning and lineage.

P41 must treat these as SOURCEFREE/TEST_ONLY grain: no source right, no selected
world, no issued N10W. The extension never mints N9/N10W semantics.

## To A41 — source/function evidence for N11 cells

For every F2/F3/F4 acceptance row, cite per-op:
`artifacts/f1f4_coverage_ledger.json` (expected/actual cells + denominators +
grades + `held_original_scope`) and `artifacts/computed_slice_evidence.json`
(evidence/composed identity hashes). The typed-state rows (AT14–16) cite
`OWNER_TYPED_STATE` receipts carrying the accepted owners' own producer states.

F1 substrate rows: `sourcebacked.stream_query` (physical→C11→I03 deterministic
parity) and the learned M01→M1→M2→B5→I4 composition op.

Honest grade for all of it: SOURCEFREE_FIXTURE / ADOPTED_FREEZE /
SOURCEFREE_TEST_ONLY; **original-source occupancy = 0; original35 U/E_pre remains
UNISSUED_HELD** (exact blocker and counts in `held_original_scope`). A41 must not
promote these rows to source-backed occupancy, and this return cannot close N11.

## Explicitly NOT handed over

Original-source reads, U/E_pre, model-use rights, selected-world/N9 issuance,
N10W issuance, Field Forge relations, Sorok actor semantics, N11 pass, N12 wake.
