# B03 — WVS Successor Oracle Standardization Contract

Producer:

`python -m rawlsing_next.fiabc_final_oracle_freeze_producers standardize-wvs ...`

## Input law

The sole truth input is the accepted R1M wrapper/truth:

`WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/07_FRESH_WVS_ORACLE.json`

The producer requires the exact accepted wrapper identity, truth identity, successor DiscoveryAuthority, successor Lock2, successor Lock2 replay, WVS source identity, and zero-candidate freeze/provenance fields.

It opens no WVS SAV bytes.

## Exact row conversion

R1M stores one rich I05 receipt row per 46 frontier candidates. The live T5 oracle expects one observation-shaped row:

- `candidate_hash`
- `typed_state`
- `semantic_fields.candidate_identity`
- `semantic_fields.constituent_fact_manifest = [{ref, typed_state}, ...]`
- `semantic_fields.coverage_state`
- `semantic_fields.support_uncertainty_state`
- `semantic_fields.replay_ref`

The adapter derives these fields only from the accepted R1M row itself. It pairs each accepted `empirical_fact_refs` entry with the corresponding accepted `support_uncertainty_state.fact_states` entry, sorts exact refs deterministically, and requires the union to equal the accepted R1M `constituent_i03_fact_manifest`. No raw-value or semantic inference occurs.

## Standard court binding

The standard court uses:

- `frozen_authority_identity` = canonical accepted R1M successor court-constitution object;
- `frozen_workload_identity` = canonical accepted R1M frontier manifest;
- standard live WVS keys:
  - `lock2_hash`
  - `lock2_replay_hash`
  - `discovery_authority`
  - `empirical_universe`
  - `risk_set`
  - `measure_basis`

The remainder of the standard material is copied from the accepted R1M truth payload.

The producer then calls existing `freeze_wvs7_oracle_from_common_material()` and `verify_frozen_oracle()`.

## Fail-closed integration boundary

This worker does not own B02. The producer requires the live standard oracle module's WVS constitution constants to equal the accepted successor values before freezing. If predecessor constants remain installed, B03 fails closed rather than minting an oracle under stale live law.
