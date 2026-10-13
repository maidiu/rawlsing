# PYAT HQ286 S00E -- Native Value-Provenance Integration Return

**Commission:** PYAT-R3-HQ286-S00E-NATIVE-VALUE-INTEGRATION-R1
**Branch:** `agent/rabochii-pyat-r3-hq286-s00e-native-value-provenance-integration-r1`
**Sealed startup:** `789ed8dd6cd92112ff469556e81923731c45b4d2`
**S00C parent:** `54f145538ed0880f8257368f838baa5b0e12e2d3`
**S00CR review:** `7f0d655ff98056bfe161e4947ef0f17add521db2`
**S00D wrapper (read-only evidence):** `4c8168b7e68e034796221bcbf36281324042e94c`

## What was repaired

The ACTUAL `ContractOnlySeamConsumer` in `rawlsing_next/r3_s02_seam_witness.py`:

1. **Fraction closure** (`_validate_fraction_closure`): Declared `raw_probability_exact_fraction` must equal recomputed `Fraction(numerator, denominator)` for every channel and step cell. Refuses mismatched fractions before any value-used receipt.

2. **Step geometry closure** (`_validate_step_geometry`): Step cell numerators must match channel `raw_numerator_support`. Condition denominators must equal sum of channel numerators. Refuses contradictory step/channel data.

3. **Case-insensitive semantic rejection**: `democracy_support`, `institutional_trust`, `democratic_attitudes` tokens checked case-insensitively in scenario IDs. Prevents case-variant bypass of false historical S00 semantics.

4. **P04 preserved**: 32->16->8 denominators, 18/32->10/16->6/8 target support, exact 9/16->5/8->3/4 fractions. Native binary Q86B/Q86A opposite joints (3/4 vs 1/4) preserved.

## S00CR 16-test read-only overlay

`test_hq286_s00e_s00cr_overlay.py` implements the EXACT frozen oracle expectations R01-R18 from `01_PRETEST_FROZEN_HOSTILES.json` without changing assertions. All 18 tests pass.

## Test evidence

| Suite | Command | Exit | Pass | Fail |
|---|---|---|---|---|
| S00C full-fixture | `python3 -m pytest rawlsing_next/tests/test_r3_s02_seam_witness.py -v` | 0 | 27 | 0 |
| S00CR overlay | `python3 -m pytest rawlsing_next/tests/test_hq286_s00e_s00cr_overlay.py -v` | 0 | 18 | 0 |
| **Total** | | | **45** | **0** |

## GT2 scientific hold

Real GT2 numerical source use remains on `SOURCE_VALUE_UNAVAILABLE__ISSUED_GT2_AGGREGATE_AND_USE_AUTHORITY_HOLD`.

## Q86A/Q86B semantics

Binary citizenship-inclusion opinions (0=No, 1=Yes, 9=Dont know, 997=Not asked, 998=Refused, -1=Missing). NOT democracy/trust Likert.

## Remaining holds

- Independent reviewer verification: separate commission
- Real GT2 mode: requires source-owned EmpiricalFact and use permission
- Historical S00 contract replacement: requires competent source-contract owner
- Protected CURRENT, V3, G0b: not granted

## Terminal

`PYAT_HQ286_S00E_NATIVE_VALUE_PROVENANCE_INTEGRATION_IMPLEMENTED_LOCAL_TESTS_PASS__AWAITING_INDEPENDENT_REVIEW__NO_SELF_ADOPTION`
