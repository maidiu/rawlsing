# PYAT R3 S00-S02 — Selected-world to sociological seam

**TERMINAL:** `PYAT_R3_S00_S02_SELECTED_WORLD_SEAM__RETAINED_SOURCE_CONDITIONED__NONISSUING`
**RESULT:** `PASS__S00_CONTRACT_FROZEN__S01_ADAPTER_BUILT__S02_WITNESS_REPLAYABLE__60_TESTS_PASS__CONSUMER_RECEIPTS_VERIFIED`

**Branch:** `agent/rabochii-pyat-r3-s00-s02-selected-world-seam-r1`
**Canonical base:** `7f29aec36d24f16da52d84f17c00f08db3a55434`
**R3 plan:** `88d3c40def26d34ff202258171c256dfa9d17dbb`

## What was built

### S00: Frozen sociological target contract

`WORKER_RETURNS/PYAT-R3-S00-S02-SELECTED-WORLD-SEAM-R1/s00_target_contract.json`

- Geography: Sub-Saharan Africa, 11-country Afrobarometer R5 subset
- Population: Adult citizens 18+, country-stratified
- Two contrasted scenarios: High democracy support / high institutional trust vs Low/Low
- Three required channels: democracy_support (MEASURED), institutional_trust (MEASURED), democratic_attitudes (TRANSFORMED)
- Evidence boundaries: measured, transformed, inferred, prior, synthetic (separately labeled)
- Legitimate missingness: coexposure counts are not national prevalence
- Expected change/stability cases defined
- Status: `FROZEN_FOR_S03_S04_COORDINATION`

### S01: Selected-world to progressive-serving adapter

`rawlsing_next/r3_s02_seam_witness.py`

- `SociologicalWorldBundle` — machine-readable bundle binding world scope, channels, evidence graph, dependence and replay metadata
- `build_sociological_bundle()` — assembles bundle from P04 progressive chain, preserving owner-native semantics
- `ContractOnlySeamConsumer` — contract-only consumer that dereferences bundle, requests progressive conditional possibilities, verifies permissible use, records actual values read, computes scenario distributions
- Smallest lawful adapter: passes actual selected producer values into progressive possibility serving

### S02: Replayable sociological witness

`rawlsing_next/tests/test_r3_s02_seam_witness.py` (18 tests)

- Per-value read receipts with semantic effects
- Deterministic replay verification (same content_hash across runs)
- Same-marginals/different-joints semantic difference
- Cumulative conditioning narrows denominator (32→16→8)
- Minority survival at every depth
- Irrelevant inputs do not change result
- Zero support produces typed refusal
- Scope mismatch produces refusal
- No V3, no actor, no biography, no parent/coparent

## Test results

| Suite | Tests | Result |
|---|---|---|
| Seam witness (S00-S02) | 18 | ALL PASS |
| P04 selected-world contract | 24 | ALL PASS |
| P04 progressive candidate | 18 | ALL PASS |
| **Combined** | **60** | **ALL PASS** |

## Evidence boundary

**Strongest output status: `RETAINED_SOURCE_CONDITIONED`**

- **Source-free elements**: P04 synthetic fixture, interface acceptance tests
- **Retained-source elements**: N01/N02 GT2 Q86A/Q86B coexposure counts, Afrobarometer R5 metadata
- **Not source-executed**: fresh survey runs, national prevalence estimation, institutional capacity measurement
- **Not conflated**: synthetic fixtures, modeled material conditions and priors separately labeled

## Consumer receipts

The `ContractOnlySeamConsumer` produces:
- `ValueReadReceipt` per channel read (channel_id, value_hash, semantic_effect, query_ref)
- `ConsumerReceipt` with values_read, scenario_results, refused_fields, output_hash
- Semantic effects verified: changed conditioning changes conditional result, irrelevant inputs stable

## Restrictions honored

- No new raw survey execution
- No protected CURRENT without authorization
- No invented scientific grants or model-use credentials
- No V3 actor, developmental psychology, parents, biography or V2 rendering
- P04 proven functionality ported, not cherry-picked
- No canonical control, immutable handoff or V3 changes
