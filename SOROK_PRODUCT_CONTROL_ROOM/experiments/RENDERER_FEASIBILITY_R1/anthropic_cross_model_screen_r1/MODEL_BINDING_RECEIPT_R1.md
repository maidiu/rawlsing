# RFA-06C — current Anthropic model binding and cost/latency receipt protocol

Official sources checked on 2026-10-12:
- [Anthropic Models overview](https://platform.claude.com/docs/en/models/overview)
- [Claude Sonnet 5.5 overview](https://platform.claude.com/docs/en/models/sonnet-5-5/overview)
- [Claude Haiku 5.5 overview](https://platform.claude.com/docs/en/models/haiku-5-5/overview)
- [Claude Haiku 5.5 migration guide](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide)
- [RFA-06A inherited binding receipt](../anthropic_court_r1/ANTHROPIC_BINDING_RECEIPT_R1.md).

The official overview lists exact Claude API IDs `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`. Sonnet and Haiku support adaptive thinking with an effort control; `high` is available, even though Haiku defaults to medium. Haiku guidance says omit `temperature`, `top_p`, and `top_k`. New-model calls use **exactly the frozen inherited R2 request, except for its `model` field**.

| Parameter | Opus inherited | Sonnet new | Haiku new |
| --- | --- | --- | --- |
| Provider | Anthropic | Anthropic | Anthropic |
| API model | `claude-opus-5-5` | `claude-sonnet-5-5` | `claude-haiku-5-5` |
| `output_config.effort` | high | high | high |
| `max_tokens` | 16384 | 16384 | 16384 |
| `output_config.format` | Original R2 per-case JSON-schema const | Same | Same |
| System message | absent | absent | absent |
| Generation seed | absent | absent | absent |
| Temperature/top-p/top-k | absent | absent | absent |
| Transport wrapper | R2 fixture identity | byte-equivalent R2 fixture identity | byte-equivalent R2 fixture identity |

API version `2023-06-01`, `anthropic==1.13.0`, `jsonschema==4.25.1`, timeout 180 seconds and retry contract remain inherited. Before new primary calls, each tier has its own non-primary RF001_N smoke and exact returned-model check. If live API binding is not accepted, do not substitute an available model.

## Public list-price context, not observed invoices

The official model overview reports Opus 5.5 standard rates **$4 input / $20 output per million tokens** and Sonnet 5.5 **$2 / $10**. Haiku 5.5 pricing starts at **$0.10 / $0.50** per million tokens and varies by pricing conditions. Caching, routing, billing plan and token accounting can change realized cost. These figures are documentation context only; this commission has **zero observed generations or billed amounts**.

## Per-call observed receipt after owner execution

Every local raw request record captures requested model, returned model, message ID, stop reason, full provider `usage` object (including thinking, cache-related fields when provided), input/output token counters, latency, attempt outcome, original schema and corrected structural review. These remain private. The post-seal comparison summary reports observed token totals, means, thinking tokens where returned, latencies and success/failure counts by model/condition. Do not substitute published list prices for an actual invoice or leak price/usage into the evaluator's blinded scoring bundle.

The 20/20/20 screen is exploratory; a cheaper tier does not win solely by spending fewer tokens, and no renderer success establishes future Rawlsing upstream-generation capability.
