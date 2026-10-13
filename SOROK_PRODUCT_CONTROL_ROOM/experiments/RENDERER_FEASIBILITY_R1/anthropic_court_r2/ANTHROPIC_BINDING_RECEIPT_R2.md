# RFA-06B — R2 provider binding receipt

RFA-06B inherits the verified RFA-06A Anthropic binding without changing model, effort, sampling or original output schema. See `../anthropic_court_r1/ANTHROPIC_BINDING_RECEIPT_R1.md` at sealed commit `4a6bf4dafbe113ae61ab6fc2423acec6619dc0f9` for the official documentation basis.

| Parameter | Frozen R2 value |
| --- | --- |
| Provider/model | Anthropic `claude-opus-5-5` (pinned model ID) |
| API | Messages `POST /v1/messages`, API version `2023-06-01` |
| SDK | `anthropic==1.13.0`, checked at execution |
| Effort | `high` in `output_config.effort` |
| Structured JSON | `output_config.format.type=json_schema` |
| max_tokens | `16384` |
| Sampling parameters | No seed, temperature, top-p or top-k |
| System | No system message |
| Calls | 60 primary; separate optional non-primary smoke |
| Operational retry | Only no-candidate connection/timeout, 429 or 5xx |
| Provider-seed status | Unsupported; schedule seed is not a provider seed |

## Exact R2-only identity binding

The model's one user message is deterministic compact JSON whose *shape* is:

```json
{
  "required_fixture_id": "RF004",
  "transport_instruction": "Set output.fixture_id exactly equal to required_fixture_id.",
  "model_payload": {}
}
```

The empty object above is **only a schematic placeholder**. Actual `model_payload` is the complete decoded, unchanged original RFA-05B `model_payload`, with no edits to Nadia's context, world facts, utterance, renderer instructions, or output semantics. The first two keys are transport bookkeeping and identical in role across both arms. No condition/replicate/scoring field is sent.

The global source schema remains exactly `../lab_fixture/OBJECTIVE_OCCURRENCE_OUTPUT_SCHEMA_R1.json`: `fixture_id` has an enum of RF001–RF010. R2 deep-copies the existing supported grammar projection **per request** and replaces only its `fixture_id` field with `{"const":"<current RF case>"}`. The authoritative original Draft 2020-12 schema remains unchanged and separately validated locally, including constraints unsupported by provider-side JSON grammar.

R2 uses a distinct experiment ID, fixed new schedule seed `0x5A0B2026`, `R2RUN-0001` through `R2RUN-0060`, `R2SMOKE-0001`, distinct raw/blind result directories, and a new `EXPERIMENT_FREEZE_R2.json`. R1's original files and owner-held diagnostics remain unchanged.

No live provider call is performed by this commission. Local smoke must establish API acceptance of the per-request const and exact ID return before the owner can start R2 primary calls.
