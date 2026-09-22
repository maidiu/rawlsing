# FIABC FINAL AUTHORITY / COMPLETENESS REPAIR — R1

Branch:
`agent/rabochii-premain-fiabc-final-authority-repair-r1`

Commission commit preserved:
`757147b06291a79ead1a3df67cebc361848e8f28`

Exact commissioned base:
`4c05a5289d0dd2fb6d475e90a039cce1360b38e3`

Repair implementation commit:
`2c4695e899c505a49ab71efc5fd25f8caf4be178`

## Disposition

**PASS — B01, B02, and B04 are closed within the commissioned authority boundary.**

No B03/B05/B06/B07 producer ownership was touched.

## B01 — closed

`rawlsing_next/fiabc_terminal_completeness.py` now freezes exactly the same 35 metric names as `fiabc_telemetry_semantics.METRIC_DEFINITIONS`.

Added exactly:

- `source_reread_count`
- `source_release_invalidation_wall_ns`
- `source_release_invalidation_bytes_rewritten`
- `semantic_authority_invalidation_wall_ns`
- `semantic_authority_invalidation_bytes_rewritten`
- `fresh_process_replay_cpu_ns`

Lifecycle bindings are exact:

- S10: source-release recomputation units + wall + rewritten bytes
- S11: semantic-authority recomputation units + wall + rewritten bytes
- S15: fresh replay wall + CPU

Candidate-A `delete_rebuild_wall_ns` remains typed `NOT_APPLICABLE_BY_FROZEN_COURT`.

The module now fails import on set drift and also contains the commissioned hostile assertion:

`assert set(FROZEN_DISPOSITIVE_METRICS) == set(METRIC_DEFINITIONS)`

No telemetry metric definition changed. `rawlsing_next/fiabc_telemetry_semantics.py` remains blob `3d57f35e20816f096bb37a56e557267d618abb9c`.

## B02 — closed

The active WVS parity-oracle constitution now uses only the adopted successor identities:

- DiscoveryAuthority: `3aee36014e4c3b39dd36bfef46006d8e9058a93aa5eb53bd81aef627883c8873`
- Lock2: `5e2a53f0e5f3b6ddd8db53b724b352ca41fe1a49408483fbf83dfdaa96283139`
- Lock2 replay: `9b5ac1726a03798d07e965396192d1bfefbee6d2188bad5a3acfb467ef063d4a`

The predecessor identities remain named only as immutable historical constants inside `pre553_independent_parity_oracle.py`; they no longer drive `_validate_constitution()`.

The active T5 `_court_constitution()` now binds directly to its already-declared `WVS7_SUCCESSOR_*` constants rather than imported predecessor-era names.

Unchanged semantic surfaces include WVS source SHA, risk set, measure basis, 46-candidate ordered hash stream/family shape, candidate grammar, runtime package, and accepted R1M oracle truth artifact.

The accepted R1M oracle remains byte-identical at blob:
`9eecf801afa2c9f3d9140b4e5fb79fb14fc1fe20`.

## B04 — closed

`ee_p2x_darwin_stage_backend._cell()` no longer reads `09_LOCAL_COURT_FROZEN_EXPECTATIONS.json["lock2"]` when serializing current failure receipts.

Current failure authority is now sourced from the already-adopted successor runtime package:
`rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json`

and fail-closed checked against the current backend successor constants.

Every current failure receipt now carries successor:

- `lock2_hash = 5e2a53...`
- `lock2_replay_hash = 9b5ac1...`

WVS7 failure receipts additionally carry:

- `discovery_authority = 3aee360...`

LiTS failure receipts retain lawful historical Lock1/HQ/owner/seam metadata, but no longer inherit the predecessor WVS Lock2 from the historical expectation file.

Manifest-derived six-cell ordering remains unchanged; WVS7/C remains sequence index 5 (sixth cell).

## Tests

Source-free tests were **authored/updated but not executed**, as required by the browser/GitHub-only commission.

Focused expected test surfaces are documented in `03_TESTS_AND_EXPECTED_ASSERTIONS.md`.

## Prohibitions observed

- user Mac/local runtime: NOT USED
- LiTS/WVS raw source bytes: NOT OPENED
- Candidate A/B/C: NOT RUN
- measured P2X: NOT RUN
- GitHub Actions: NOT TRIGGERED
- metric definitions: NOT CHANGED
- candidate meanings/workloads/source identities: NOT CHANGED
- B03/B05/B06/B07 producer ownership: NOT TOUCHED

## Terminal

`FIABC_FINAL_AUTHORITY_REPAIR_R1_PASS__B01_B02_B04_CLOSED__35_OF_35_COMPLETENESS__WVS_SUCCESSOR_AUTHORITY_ACTIVE__FAILURE_SERIALIZATION_SUCCESSOR_BOUND__TESTS_AUTHORED_NOT_EXECUTED`
