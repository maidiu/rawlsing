# EE-R3G — A/B/C candidate adapter readiness

You are **EE-R3G — A/B/C CANDIDATE ADAPTER READINESS**.

Repository: `maidiu/rawlsing`
Library: `NO`.

Exact grain: `MAP_AND_QUALIFY_THE_EXISTING_A_B_C_PHYSICAL_CANDIDATE_IMPLEMENTATIONS_AGAINST_THE_QUALIFIED_HARNESS_INTERFACE_FOR_THE_NINE_SELECTION_CRITICAL_OPERATIONS_ONLY`.

Read current canonical HQ authority from `HQ_HANDOFF/LATEST.json`, then this commission.

Binding inputs:
- EE-R2A selection-critical operation set `6b9b39ddc089033bb5779806a9d08e56be320107`;
- independently qualified EE-W4 harness via EE-R2E `7f7f716ae9cd26bbb1fe5adc7a5ff1024955e285`;
- accepted Route A / Route B / Route C / common-harness lineage and exact current implementations where present;
- common contract and equal-work laws under `PREV3_EMPIRICAL_ENGINE_COMMON_CONTRACT_R1`.

For A, B, and C separately, map existing executable components to OP001–OP006 and OP020–OP022. Determine for each operation whether the candidate is:
- `ADAPTER_READY` — existing implementation can satisfy the harness request/response/telemetry contract without semantic changes;
- `BOUNDED_ADAPTER_NEEDED` — semantic work exists but a physical transport/adapter layer must be written;
- `PHYSICAL_IMPLEMENTATION_GAP` — the candidate does not yet implement the required operation;
- `WAITING_ON_COMMON_PREMISE` — candidate-independent semantic/oracle input is not yet frozen.

Where bounded adapter code can be written without changing candidate semantics, implement and test it. Do not implement missing semantic work, alter the common workload, rank candidates, or run the final comparison.

Require identical harness-facing request meaning and telemetry fields across candidates. A candidate-specific optimization is allowed only behind the same semantic contract; no candidate-specific workload omission or weakened oracle.

Return exact readiness matrix, adapter artifacts/tests if any, and the smallest physical implementation gaps remaining before final bakeoff. No MAIN or semantic PRE-MAIN mutation.
