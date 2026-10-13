# RFA-06B — static browser/GitHub validation receipt

Commission date: 2026-10-12. Sealed predecessor: `4a6bf4dafbe113ae61ab6fc2423acec6619dc0f9`. This receipt describes **read-only code inspection and independent JavaScript checks** against the remote repository, **not** a completed Python preflight, Anthropic API test, provider output, or character-quality assessment.

## Exact source proof

- `R1_FIXTURE_ID_INFORMATION_PATH_DEFECT = CONFIRMED`: R1 sends only `model_payload`, packet `packet_id` remains outside, source/provider-visible output schema allows RF001–RF010, and R1 later compares candidate ID to the withheld manifest case ID.
- `OTHER_HIDDEN_OUTPUT_REQUIREMENT_DEFECTS = NONE FOUND`: all eight top-level output fields and nested required/local checks audited in `OUTPUT_REQUIREMENT_AUDIT_R2.md`. The only hidden exact predetermined output was fixture identity.
- `RFA05B_SEMANTIC_PAYLOADS_CHANGED = NO`: new changes are confined to R2 directory; inherited `render_inputs_r1/` and `lab_fixture/` remain the sealed parents. Common code verifies their exact original Git blob bytes at execution.
- `R2_MODEL_VISIBLE_IDENTITY = STATIC PASS`: new envelope has `required_fixture_id`, fixed transport-only instruction and unchanged source `model_payload`. This field has no arm, replicate or score.
- `R2_PROVIDER_CONST = STATIC PASS`: `request_specific_provider_schema` deep-copies the original grammar and binds `properties.fixture_id` to the exact case `const`. The original source enum is not modified.
- `R2_LOCAL_EXPECTED_IDENTITY = STATIC PASS`: the same manifest `case_id` drives both `request_for` and `deterministic_candidate`; `identity_alignment` enforces their equality before execution.
- `R2_SMOKE_HOLD_BEFORE_PRIMARY = STATIC PASS`: the primary execution path calls `require_r2_smoke_pass`, requiring persisted schema-valid `R2SMOKE-0001` with exact RF001 ID.
- `R1_R2_EVIDENCE_ISOLATION = STATIC PASS`: separate `anthropic_court_r2/` directory, freeze, raw/blinded/receipt subdirectories and only `R2RUN-XXXX`/`R2SMOKE-0001` attempt filename patterns.

## Independent schedule verification

The manifest has **60 R2 primary IDs**, exactly `R2RUN-0001`–`R2RUN-0060`. Independent xorshift32/Fisher–Yates reproduction from `0x5A0B2026` matched every entry. There are exactly three replicate ordinals for each of 10 × 2 pairs. All **60 positions** differ from the R1 order. The blinded manifest contains only opaque run IDs, in correct order, without condition or replicate mapping.

## No executed provider trial

`ANTHROPIC_MESSAGES_CALLS_BY_COMMISSION = 0`.
`API_KEY_RECEIVED_BY_COMMISSION = NO`.
`RAW_MODEL_RESULTS_COMMITTED = 0`.
`R2_RENDERER_SCORES = NOT_ASSESSED`.

The local Python offline gate, installation-version check and real provider acceptance of per-request schema `const` remain **owner execution steps**. The runner refuses primary execution without a successful separately persisted smoke result. No R2 experimental success is claimed by this static receipt.

## Recommended owner checks

```sh
python3 validate_renderer_court_r2.py --expect-empty
python3 run_anthropic_renderer_court_r2.py --preflight
python3 run_anthropic_renderer_court_r2.py --freeze
python3 run_anthropic_renderer_court_r2.py --smoke
```

Proceed to R2 primary sampling only if smoke confirms its exact fixture const and there are no local holds. Do not resume R1.
