# EE-P2R6X — stopped-ledger reconciliation audit

Status: `PREPARED_FOR_GOVERNED_SYNTHETIC_QUALIFICATION`

Authority:
- live sealed HQ checkpoint observed before implementation: `20260919T0330-0400`
- immutable handoff: `9540aba11d40fc749ffa59827e871c1ba00e7ec6`
- controlling decisions: `HQD-2026-09-19-081`, `HQD-2026-09-19-082`
- commissioned R6X tip: `d7f22f8c2eaff326f547925f403a6f494b3f04c9`
- held P2X head: `ae8b1db9d8c3288e002950ac01123c70f3138320`
- exact stopped ledger SHA-256: `7de7c91d539dd267e31098fd47285b3f4a7873e1c9ec7b542c45cac3908b8671`

## Exact ledger rewind

Only these blocker roots are reopened:
- `LITS_I/A/S02_C11_REACHABILITY`
- `LITS_I/B/S03_PARITY_ORACLE_GATE`
- `WVS7/A/S01_CANDIDATE_PREPARATION_BUILD`
- `WVS7/B/S01_CANDIDATE_PREPARATION_BUILD`

For each blocker, the reconciler requires the exact governed exception identity, requires every later same-cell candidate-stop entry to carry the mechanical propagation schema and point back to that exact blocker, then removes the blocker plus only those linked propagations.

The orphan `COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION` entry is removable only if it is exactly `RUNNING`, nonterminal, receipt-less, and still bound by the governed P2X return/final-verifier blocker.

The resulting first unfinished stage is again:
`LITS_I/A/S02_C11_REACHABILITY`.

## Preserved state

The reconciler does not mutate:
- source identities;
- continuation-map identity;
- any unrelated terminal ledger entry;
- LiTS-A S00/S01 preservation;
- LiTS-B S00/S01/S02 preservation;
- LiTS-C terminal states;
- WVS-C preserved portability failure/frozen-law states;
- Git-tracked P2X failure/cell evidence;
- durable transformed carriers or external preserved physical carriers.

## Local filesystem ownership

The driver isolates mutable state at:
`<work-root>/cells/<source>/<candidate>/`.

For each of the four affected cells, and for `COURT/ALL`, the only durable file deleted is:
`durable/ee_p2x_backend_state.json`

and the only directory class removed wholesale is that cell's isolated:
`scratch/`

No candidate root is deleted. No other durable file is deleted.

This follows the backend's exact state path and preserves transformed carrier material such as WVS-A's durable R5 root if present.

## Fail-closed idempotence

A mutating invocation requires the exact stopped ledger SHA above. Once reconciliation changes the ledger, another mutating invocation refuses. `--audit-only` may verify either the exact stopped state without mutation or an already-reconciled state bound by the reconciliation receipt.

## Source boundary

The reconciler accepts no LiTS/WVS source-path arguments, contains no decoder/import path for empirical carriers, and records:
- `source_carrier_access_performed: false`
- `empirical_measurement_performed: false`
