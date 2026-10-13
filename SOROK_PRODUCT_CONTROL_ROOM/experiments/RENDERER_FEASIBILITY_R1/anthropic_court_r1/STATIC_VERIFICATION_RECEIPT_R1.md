# RFA-06A — browser/GitHub static verification receipt

Verification performed against exact sealed GitHub commit `a406e1d289faac31fd51cca8b36a4bb47af93852`, using read-only GitHub file/tree retrieval and independent deterministic JavaScript checks. **This is a static source verification, not a claim that local Python --preflight or the provider API has executed.**

## Inherited inputs and manifest

- `20_INPUT_PACKETS_PRESENT = PASS`: RF001–RF010 in both WP and N, source Git blob IDs stored in `EXPERIMENT_CONFIG_R1.json`.
- `10_WP_N_PAIRS_PRESENT = PASS`: all ten pairs inspected.
- `PAIR_SHARED_PARITY = PASS`: the two `model_payload.shared` trees serialize identically for each RF.
- `NARROW_UNCHANGED = PASS`: N's actor projection equals the corresponding original RFA-05 `actor_safe_projection`.
- `EXACT_USER_EVENT = PASS`: every pair retains the source case's exact utterance.
- `INPUT_SIZE_PARITY = PASS`: compact UTF-8 payload byte counts for all twenty cases agree with RFA-05B's manifest.
- `MODEL_VISIBLE_OUTPUT_SCHEMA = PASS`: packet schema equals the original output schema minus its explicitly local-only `x-local-admission-contract`.
- `EVALUATOR_ORACLE_NOT_TRANSMITTED = PASS` (static denylist): neither prompt arm contains known excluded evaluator-only fields / phrases. The runner transmits the allowlisted `model_payload` only.
- `USER_PHENOMENAL_STATE_NOT_TRANSMITTED = PASS` (static denylist), without modifying inherited fixtures.
- `60_PRIMARY_RUN_IDENTITIES = PASS`: independently recomputed xorshift32 Fisher–Yates schedule from recorded `0x5A0A2026`; exact 60 identities matched.
- `3_REPLICATES_PER_PAIR = PASS`: 10 × 2 conditions each exactly three replicate ordinals.
- `CONDITION_MAPPING_SEPARATED = PASS`: blinded manifest contains `RUN-XXXX` only, in exact agreement with private randomized mapping.
- `MODEL_OUTPUTS_PRESENT = 0` at handoff: only empty-result directory sentinels were committed. No Anthropic generation was requested.

## Execution status and limits

- `MODEL_CALLS_EXECUTED_BY_COMMISSION = 0`.
- `API_KEY_REQUESTED_BY_COMMISSION = NO`; no credentials embedded in committed static harness.
- `OFFLINE_PYTHON_VALIDATOR_EXECUTED_BY_COMMISSION = NO`: the complete offline validator is provided for execution in the repository owner's clone. It checks Git blobs, packet/schema parity, prompt isolation, manifest/custody and prior-run collisions.
- `REAL_PROVIDER_SCHEMA_ACCEPTANCE = UNTESTED`: official documentation was inspected; no schema/output can be empirically certified before an intentional owner call.
- `RENDERER_FEASIBILITY = NOT_TESTED`; no quality scores, model responses, canonical admissions or Nadia interpretation created.

The owner should first run `python3 validate_renderer_court.py --expect-empty` after installing pinned dependencies, then intentionally run `--preflight` and `--freeze` as documented. No empirical outcome is implied by this receipt.
