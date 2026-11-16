# FIABC-W3-I02 — Implementation / Diff Inventory

Base: `56697a27e94eb9603dfa412a15ab8f1feb819b0c`

## Production delta

### `rawlsing_next/pre553_effective_n.py`

New current F018 effective-N successor.

Public callable surface:

- `compute_effective_n(...)`
- `replay_effective_n(...)`

Receipt:

- `EffectiveNProduct`

Contract constants:

- `EFFECTIVE_N_CONTRACT_ID = PRE553_F018_EFFECTIVE_N@1.0.0`
- `EFFECTIVE_N_FORMULA_ID = SUM_W_SQUARED_OVER_SUM_W2_EXACT@1.0.0`

No existing I03/I05/C11 production file was modified.

### Ownership boundary

The module consumes, rather than replaces:

- `EmpiricalQuerySpec` for exact measure kind, weight basis, risk/query/source grain;
- `EmpiricalFact` for exact I03 denominator truth and provenance;
- `WeightMeasureFact` for exact respondent weight identity/value/scope;
- `AuthorityRegistry` for exact immutable authority resolution.

It does not create:

- a second routing owner;
- a second risk-set owner;
- a second denominator owner;
- a weight selector;
- an estimand selector;
- an `EmpiricalFact`;
- structural or discovery authority.

## Focused test delta

### `rawlsing_next/tests/test_pre553_effective_n.py`

Added ten focused tests covering the positive exact formula/replay path and the commissioned hostile classes:

- absent weight authority;
- invalid weights;
- zero/degenerate sums;
- mismatched scope;
- default-weight inference attempts.

Additional controls verify RAW/nonweighted non-applicability, design/estimand separation, I03 weighted-denominator coupling, and presentation-order invariance.

## Existing files intentionally untouched

The following present owners were inspected but not modified:

- `rawlsing_next/pre553_empirical_objects.py`
- `rawlsing_next/pre553_empirical_authority.py`
- `rawlsing_next/_pre553_query_common.py`
- `rawlsing_next/_pre553_query_eval.py`
- `rawlsing_next/pre553_empirical_query.py`
- `rawlsing_next/pre553_discovery_exact.py`

This is intentional. I03 already owns exact denominator truth and authorized weighted aggregation. Extending I03's semantic object to own effective-N would have mixed a derived F018 measurement with the empirical-truth surface.

## Historical evidence intentionally not imported

`data/ddm_build_copy/numeric_formulas.py` contains historical `effective_n_v1` evidence. The current successor independently implements exact rational `sum_w^2 / sum_w2`; no historical V550/V550J implementation is imported, called, or promoted to current ownership.

