# PYAT R2 T8F -- Temporal Integrity Repair Return

**Commission:** PYAT-USERDIRECT-20261014-R2-T8F-TEMPORAL-INTEGRITY-R1
**Branch:** `agent/userdirect-pyat-20261014-r2-t8f-temporal-integrity-r1`
**Sealed startup:** `7bf38e045fb09253f0b8e15917a28c32c7fcfce0`
**T8R predecessor:** `6f4706b703124993dacab86cbfa3d41428ca3a25`
**T8C original:** `059d7ce1b35a08fa4fe735ffccc1a5dddbfe5899`

## Three T8R Integrity REDs -- Closed

| RED | Defect | Repair | Status |
|---|---|---|---|
| 1 | Tampered delta accepted under stale product digest | `consume()` recomputes canonical product hash and rejects `PRODUCT_DIGEST_MISMATCH` | CLOSED |
| 2 | Tampered native category accepted under stale digest | `consume()` verifies `satisfied_share` arithmetic against categories | CLOSED |
| 3 | Malformed as-of raises bare ValueError | `compare()`/`consume()` catch `ValueError` and raise typed `Refusal("INVALID_ASOF_DATE")` | CLOSED |

## Content-Addressed Wave-Fact Registry

`WaveFactRegistry` with immutable `WaveFactRef`:
- Defensive-copy registration with content hash
- `retrieve()` validates stored hash against ref hash
- `revalidate()` re-checks full `WaveFact.validate()` chain
- Tampered ref rejected with `FACT_HASH_MISMATCH`

## Test results: 29/29 PASS

- 3 integrity repairs (tampered delta, tampered category, invalid asof)
- 19 original T8C test equivalents (Ghana category 0, independent waves, missing/refusal distinctions, 2017 gap, arithmetic, EE12, temporal inversion, population, historical time, mixed asof, zero support, question match)
- 3 registry tests (register/retrieve, tampered ref, revalidate)
- 4 propagation tests (numerical change, unrelated stable, wave-one-only, version downgrade)

## Preserved distinctions

- Ghana native category 0: substantive distinct response
- Independently sampled waves: `INDEPENDENT_CROSS_SECTION_TEST_ONLY`
- Missing/refusal: R5 Q43 refused=998, R9 Q31 refused=8
- 2017 gap: `UNKNOWN_UNOBSERVED_GAP`
- No invented Ghana trends, no same-person joins

## HQ214 Comparator Reuse

T8R could not execute HQ214 owner import (network failure). The comparator pattern is reusable on two source-issued measures but does not calculate native distributions or issue EE12. Test double proves local method only.

## Source/EE12 Holds

- No original Afrobarometer data read
- No EE12 issuance
- No N8S objective institutions
- No V3 actor
- Test-only fixture authorization

## Terminal

`PYAT_R2_T8F_TEMPORAL_INTEGRITY_REPAIR__THREE_REDS_CLOSED__29_TESTS_PASS__AWAITING_INDEPENDENT_REVIEW`
