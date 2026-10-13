# PYAT HQ285 S00D -- Producer Binding and Semantic Quarantine Return

**Commission:** PYAT-R3-HQ285-S00D-PRODUCER-BINDING-QUARANTINE-R1
**Branch:** `agent/rabochii-pyat-r3-hq285-s00d-value-binding-quarantine-r1`
**Sealed startup:** `7a0e42477c5528ae19a0150a05f633df058d203c`
**S00C source parent:** `54f145538ed0880f8257368f838baa5b0e12e2d3`
**S00CR review:** `7f0d655ff98056bfe161e4947ef0f17add521db2`

## S00CR defects addressed

| Defect | S00CR finding | S00D fix |
|---|---|---|
| D1 | Numeric channel substitutions retaining stale producer identity | Content-derived producer identity: `_producer_identity()` hashes actual channel/condition/step values; any change alters identity |
| D2 | Contradictory declared step cells and exact probability fractions | `validate_fraction_closure()` and `validate_step_geometry()`: recomputed fraction must match declared, step cells must match channel data |
| D3 | Case-variant and alias bypass of false historical S00 semantics | `is_false_s00_semantic()`: case-insensitive check for democracy/trust/attitudes tokens; `quarantine_historical_s00_contract()` |
| D4 | Receipt provenance not independently witnessed | `RECEIPT_PROVENANCE_CLASS = "LOCAL_INTROSPECTIVE_LOGGING__NOT_EXTERNALLY_AUTHENTICATED"` |

## P04 progressive conditioning preserved

- Denominators: 32 -> 16 -> 8 respondents
- Fractions: 9/16 -> 5/8 -> 3/4 exact conditional probabilities
- Verified in `test_r01_p04_owner_risk`, `test_r02_overlap_no_duplication`, `test_s00d_witness_preserves_p04`

## Q86A/Q86B semantics

Binary citizenship-inclusion opinions (0=No, 1=Yes, 9=Dont know, 997=Not asked, 998=Refused, -1=Missing). NOT democracy/trust Likert measures. Historical S00 contract quarantined as `INVALID_SOURCE_SEMANTICS__HISTORICAL_REFERENCE_ONLY`.

## S00CR 16-test court (R01-R18)

All 16 independent hostile oracles pass as read-only overlay without changing assertions:
- R01-R04: P04 geometry, read-to-arithmetic, unconsumed read
- R05-R07: numeric mutation, irrelevant invariance, opposite joints
- R08-R10: scope mismatch, risk mismatch, zero support
- R11-R13: replay hash, fake issuer, old S00 semantic prohibition
- R14: case-variant rejection (S00D fix)
- R15-R17: fraction closure, step geometry, producer binding (S00D fixes)
- R18: no original rights

## Test evidence

`python3 -m pytest rawlsing_next/tests/test_s00d_s00cr_court.py -v` -- exit 0, 24/24 pass

## GT2 scientific hold

Retained GT2 numerical source consumption remains on `SOURCE_VALUE_UNAVAILABLE__ISSUED_GT2_AGGREGATE_AND_USE_AUTHORITY_HOLD` until actual source-owned aggregate, risk and use permission exist.

## Remaining holds

- Historical S00 contract replacement: requires competent source-contract owner
- Real GT2 mode: requires exact source-owned EmpiricalFact and use permission
- Independent reviewer verification: separate commission
- External custody for production claims

## Terminal

`PYAT_HQ285_S00D_PRODUCER_BINDING_QUARANTINE_IMPLEMENTED_LOCAL_TESTS_PASS__AWAITING_INDEPENDENT_REVIEW__NO_SELF_ADOPTION`
