# Anthropic binding receipt — RFA-06A (verified 2026-10-12)

## Authority

These are **current official provider-document facts**, verified before implementing this experimental harness. Repository fixture authority remains the sealed RFA-05B commit, not the provider documentation.

| Binding | Frozen choice / finding | Official documentation |
| --- | --- | --- |
| Provider/model | Anthropic Claude API, **`claude-opus-5-5`** | [Models overview](https://platform.claude.com/docs/en/models/overview), [Opus 5.5 model page](https://platform.claude.com/docs/en/models/opus-5-5/overview) |
| Model stability | **Pinned snapshot**: 4.6+ dateless IDs are fixed, not mutable legacy aliases; serving infrastructure can change independently | [Model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions) |
| Messages | `POST /v1/messages`, `client.messages.create`; SDK transport header `anthropic-version: 2023-06-01` pinned | [Create a Message](https://platform.claude.com/docs/en/api/messages/create), [API versions](https://platform.claude.com/docs/en/api/versioning) |
| JSON grammar | `output_config={"format":{"type":"json_schema","schema":...}}` in Messages GA, no beta header | [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) |
| Effort | `output_config.effort="high"`; Opus 5.5 supports `low`, `medium`, `high`, `xhigh`, `max`, default `medium` | [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) |
| Thinking | Opus 5.5 uses adaptive thinking, always on; do not set legacy `budget_tokens` or disabled thinking | [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking), [Opus 5.5 prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) |
| Explicit provider generation seed | **No documented seed field** in current Messages create request; unsupported by this pinned request binding, not presumed deterministic | [Messages create request parameters](https://platform.claude.com/docs/en/api/messages/create) |
| Sampling controls | Newer-than-Opus-4.6 models deprecate `temperature`, `top_p` and `top_k`; `top_k` rejected, `temperature`/ `top_p` only backward-compatible narrow values; **all three omitted** | [Messages create request parameters](https://platform.claude.com/docs/en/api/messages/create) |
| Python SDK | `anthropic==1.13.0`; exact installation pinned in requirements; runtime records package version and rejects mismatch | [Official Python SDK releases](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v1.13.0), [SDK repository](https://github.com/anthropics/anthropic-sdk-python) |
| Token counting | Non-generative `POST /v1/messages/count_tokens`, via `client.messages.count_tokens`; **never** used by ordinary preflight; explicit `--preflight --count-tokens` only | [Count tokens in a Message](https://platform.claude.com/docs/en/api/messages/count_tokens) |
| Usage | Preserve full provider `usage`: `input_tokens`, `output_tokens`, available cache input/write counters, `output_tokens_details.thinking_tokens` where exposed, service tier, etc. Total output includes thinking tokens. | [Messages create response](https://platform.claude.com/docs/en/api/messages/create), [Adaptive thinking usage](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost) |

## Non-negotiable JSON Schema boundary

The inherited `lab_fixture/OBJECTIVE_OCCURRENCE_OUTPUT_SCHEMA_R1.json` includes provider-unsupported enforcement keywords: integer `minimum`/`maximum`, array `maxItems`/`uniqueItems`, and string `minLength`. It also contains `x-local-admission-contract`, which is expressly local-only. Anthropic's [structured output limitations](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#json-schema-limitations) state that sending unsupported constraints directly returns HTTP 400. The official SDK's schema helpers similarly remove unsupported constraints while retaining validation against the original.

Therefore the harness deterministically projects ONLY supported structure into the API-side JSON grammar, keeping descriptions of locally enforced constraints. **The original schema remains unchanged and is validated as a whole locally using Draft 2020-12 `jsonschema`.** Schema-invalid candidates are typed retained experimental results, not repaired, scored, or retried. This is not a claim of provider-level enforcement for unsupported keywords. If the provider rejects the projection, preserve `PROVIDER_SCHEMA_FAILURE` and HOLD rather than substituting a model, changing the schema mid-court, or silently rerendering.

The `model_payload.shared.output_schema` embedded in every matched packet is the inherited *model-visible* schema and deliberately excludes the original local-only `x-local-admission-contract`. The harness verifies this exact partition against the original local schema (minus that local-only extension). The provider user message is the canonical UTF-8 JSON of **only** `model_payload`.

## Frozen call design

- **60** independent invocations = 10 RF cases × 2 conditions × 3 replicate ordinals. The schedule's `0x5A0A2026` xorshift/Fisher–Yates seed shuffles *run order only*; it is NOT a Claude seed.
- **One** user role message per call, containing deterministic minified UTF-8 `model_payload` JSON; **no system message**, no user-phenomenal information, no evaluator metadata and no scoring rubric.
- Constant `max_tokens=16384`: allows high-effort adaptive reasoning plus a compact schema-limited 30-second proposal without using a huge 128K budget; it is a ceiling, not a request for long narration. No tools, temperature, top-p or top-k.
- The API may add its own identical structured-output and thinking instructions to each request; these are provider infrastructure, not hidden arm-specific authoring.
- Explicit SDK retry disable `max_retries=0`; only recognized connection/timeout, 429, or HTTP 5xx with **no captured candidate** can prompt up to two logged operational retries. The local owner must decide whether operational timeouts could create duplicate billed requests; evidence keeps every attempt.
- Primary `RUN-0001`–`RUN-0060` are sealed before results. Distinct `SMOKE-0001` is a **non-primary** probe and never enters the primary manifest or scoring export.
- No Anthropic key was requested or used while authoring. **ANTHROPIC_MESSAGES_CALLS_BY_COMMISSION = 0**. Provider connectivity and grammar acceptance are not empirically demonstrated by this commission.

## Residual reproducibility limits

Provider infrastructure and stochastic sampling can evolve even with fixed model weights. No provider sampling seed is claimed, no exact bit-for-bit replay of outputs is promised, and per-run provider message IDs/usage must be captured in local evidence. Feasibility, character quality, and admissibility remain **NOT SCORED / NOT TESTED**.
