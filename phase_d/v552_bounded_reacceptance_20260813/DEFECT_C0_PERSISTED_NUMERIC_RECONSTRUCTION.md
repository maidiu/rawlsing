# V552 Defect C0: Persisted Numeric Reconstruction

## Finding

The unchanged V552 implementation computed derived pressure fields from full-precision in-memory values, then wrote CSV artifacts with pandas' six-decimal default. Re-reading those artifacts produced sub-micro-unit differences in signed-intensity summaries and pressure magnitude, causing the unchanged validator to reject otherwise coherent scopes.

## Repair

- CSV frames now preserve IEEE-754 values with `%.17g`.
- Persisted numeric validation uses a bounded `1e-6` source-coordinate tolerance.
- Classification and authority decisions retain the existing `1e-12` contract epsilon.

This is a serialization/reconstruction repair only. It does not alter source rows, response semantics, weights, pressure formulas, eligibility, or authority.

## Evidence

After the repair, the four affected scopes Afrobarometer R1/BF, Arab Barometer I/LY, Latinobarometro 1995/BR, and South Asia W1/IN pass the unchanged V552 output contract. EVS, GSS, LiTS, and WVS remain passing.
