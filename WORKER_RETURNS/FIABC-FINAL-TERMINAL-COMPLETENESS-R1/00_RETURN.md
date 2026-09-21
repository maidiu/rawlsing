# FIABC FINAL TERMINAL COMPLETENESS GATE — R1 RETURN

## Terminal

`FIABC_FINAL_TERMINAL_COMPLETENESS_GATE_R1__PASS__S16_AND_S17_FAIL_CLOSED_ON_MATERIALLY_MISSING_REQUIRED_REACHABLE_DISPOSITIVE_MEASUREMENTS__SELECTION_NEUTRAL`

Exact sealed HQ parent: `445c2fd534db61de0d0d348a6d77a11faa419cc3`

Commission-preserving branch entry head: `737b1d64ed78e16ad9a8f7baf1e8defbbbab9000`

Implementation head before return-packet commits: `d7d91f9d6548240ffc215d2b56a59f43b6dbae3f`

The exact final branch head is the commit containing this return file and is reported by the worker terminal response.

## Code / test blobs

- `rawlsing_next/fiabc_live_terminal_control.py` — `09e8b633346c76a8025f36060d0718896255eed4`
- `rawlsing_next/fiabc_terminal_completeness.py` — `8b855eb5f866ff442a69bdac523a81eb44abdfbc`
- `tests/test_fiabc_terminal_completeness.py` — `fc0e4b8056f5ac7cc3941d24d033af026f318327`
- `WORKER_RETURNS/FIABC-FINAL-TERMINAL-COMPLETENESS-R1/01_HOSTILE_TEST_LEDGER.json` — `4461d193a6310cecd1266d5b316aca896f6e417a`
- `WORKER_RETURNS/FIABC-FINAL-TERMINAL-COMPLETENESS-R1/02_COMPLETENESS_CONTRACT.json` — `e680609ac1fb57a329b24f2503d6cae35b43181b`

## Exact completeness law

A completed qualifying source×candidate cell may reach S16 PASS only when the canonical T4 receipt proves the frozen dispositive measurement vector complete under the current execution manifest.

1. Every required and reachable frozen dispositive metric must exist in the canonical metric set and have state `MEASURED` with a non-negative numeric value.
2. `MEASUREMENT_NOT_CAPTURED` is never sufficient for a required/reachable dispositive metric.
3. The T4 metric-definition hash and full definition manifest must exactly equal the canonical frozen definitions.
4. CPU, RSS, and whole-cell wall accounting must be sealed from process envelopes, with exactly one MAIN process envelope for a completed cell.
5. The canonical I/O stream must be sealed before bytes-read/written/rewritten can satisfy final completeness. Endpoint sizes or partial event coverage are not enough.
6. Scratch high-water accounting must be sealed before peak scratch bytes/file count can satisfy final completeness. Endpoint directory size is not a peak.
7. Required lifecycle stages must have the exact expected lifecycle action receipt. Ready stale/corrupt/interruption/replay stages therefore cannot disappear merely because semantic parity passed.
8. Frozen N/A is accepted only as `NOT_APPLICABLE_BY_FROZEN_COURT` under the exact current cell law. Candidate B's no-cache stale/corrupt stages and WVS/C's zero-accelerator stale/corrupt stages remain lawful skips and create no fake cache obligation.
9. Authorized-stop state is accepted only downstream of an executable authorized stop and is forbidden in a cell simultaneously claiming completed qualification.
10. Preserved work with forbidden numeric repetition is accepted only when its stage receipt proves the exact `PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY` disposition, `numeric_credit_allowed=false`, and `missing_numeric_is_zero=false`. It cannot be silently promoted to current numeric credit.
11. No N/A, authorized stop, preserved absence, or uncaptured value may be converted to numeric zero.
12. The completeness receipt is selection-neutral: it contains no rank, score, winner, preferred candidate, or cross-candidate comparison.

## S16 / S17 binding

At S16, `seal_live_cell_terminal()` now loads the exact current execution manifest, re-opens the canonical T4 telemetry receipt by the already-bound path/SHA, derives the cell's metric/lifecycle obligations, and blocks before writing a PASS terminal if completeness fails. The resulting completeness receipt is embedded into the cell terminal.

At S17, `verify_live_final_terminal()` independently re-runs the same completeness proof for every one of the six cells from the canonical telemetry receipt and current manifest, then requires identity equality with the S16 completeness receipt before the existing I08 final-terminal verifier may PASS.

This means a future S17 cannot certify a qualifying completed court merely because a T4 receipt exists and hashes correctly.

## Worker A telemetry integration seam

Worker A does not need to change this gate. Its instrumentation must make the existing canonical T4 receipt truthful enough to satisfy it:

- required/reachable slots become genuinely `MEASURED`;
- lawful non-applicable slots become exact typed N/A rather than zero;
- preserved no-numeric work remains typed absent and is backed by the exact preserved-stage adjudication;
- event-level I/O and scratch coverage set their completeness seals only when complete;
- process and lifecycle receipts remain bound to the exact cell/stage/action identities.

No measurement is invented by the gate.

## Hostile-test ledger

The synthetic hostile suite covers all commission minimums plus invalid-N/A and preserved-work cases. See `01_HOSTILE_TEST_LEDGER.json`.

This worker did **not** run GitHub Actions, Candidate A/B/C, raw LiTS/WVS source processing, or measured P2X. The tests are deterministic synthetic-receipt tests authored for the repository but were not executed in this browser/GitHub-only lane.

## Scope / prohibitions preserved

No edits were made to:

- `rawlsing_next/ee_p2x_darwin_stage_backend.py`
- `rawlsing_next/fiabc_live_accounting_binding.py`
- `rawlsing_next/ee_p2x_darwin_court_driver.py`

No ranking or selection was performed. No frozen metric definition was changed. No new score was added. No source bytes were opened.
