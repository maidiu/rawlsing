# FIABC FINAL AUTHORITY / COMPLETENESS REPAIR — R1
## Tests and expected assertions

**Execution status: NOT RUN.** This lane is browser/GitHub-only. The following tests were authored or updated and are expected to be run by the later local qualification lane.

### Focused source-free command

```bash
set -euo pipefail
python -m pytest -q \
  tests/test_fiabc_terminal_completeness.py \
  tests/test_fiabc_final_measurement_telemetry_closure.py \
  rawlsing_next/tests/test_pre553_independent_parity_oracle.py \
  rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py \
  rawlsing_next/tests/test_fiabc_final_progress_driver.py
```

### B01 assertions

`tests/test_fiabc_terminal_completeness.py` now asserts:

1. `len(METRIC_DEFINITIONS) == 35`
2. `len(FROZEN_DISPOSITIVE_METRICS) == 35`
3. `set(FROZEN_DISPOSITIVE_METRICS) == set(METRIC_DEFINITIONS)`
4. every lifecycle-grain metric maps to the exact governed stage:
   - S09 delete/rebuild;
   - S10 source-release units/wall/rewrite;
   - S11 semantic-authority units/wall/rewrite;
   - S15 fresh-replay wall/CPU.
5. existing Candidate-A delete/rebuild typed-N/A test remains unchanged.

The production module additionally contains an import-time fail-closed set check plus the exact commissioned assertion.

### B02 assertions

`rawlsing_next/tests/test_pre553_independent_parity_oracle.py` now asserts the three active constants equal successor Lock2/replay/DiscoveryAuthority and that a material object carrying all three predecessor identities is rejected by `freeze_wvs7_oracle_from_common_material()`.

`rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py` now asserts `_court_constitution("WVS7", ...)` returns only the successor values and contains none of the three predecessor values.

Existing oracle tests continue to protect:

- WVS source SHA;
- exact 46-candidate frontier;
- 10/1/10/25 family shape;
- risk set;
- measure basis;
- candidate-neutral provenance;
- frozen oracle immutability.

### B04 assertions

`rawlsing_next/tests/test_fiabc_final_progress_driver.py` now uses a deliberately predecessor-valued historical `09_LOCAL_COURT_FROZEN_EXPECTATIONS.json` fixture while separately supplying the current successor runtime package.

The WVS7/C failure test expects:

- source = WVS7
- candidate = C
- sequence_index = 5
- Lock2 = successor `5e2a53...`
- Lock2 replay = successor `9b5ac1...`
- DiscoveryAuthority = successor `3aee360...`
- predecessor Lock2/DiscoveryAuthority absent from emitted authority
- manifest cell count remains six.

A new LiTS failure test expects:

- sequence_index = 0 for LiTS-I/A;
- HQ handoff + Lock1 metadata preserved;
- candidate-owner + execution-seam metadata preserved;
- current successor Lock2/replay bound instead of the historical predecessor Lock2;
- no WVS DiscoveryAuthority field injected into the LiTS authority block.

### Telemetry/progress regression protection

The focused command includes the already-authored final telemetry closure suite and final progress-driver suite. No telemetry producer, progress reporter, six-cell topology, or Candidate-A typed-N/A semantics were modified by this repair.
