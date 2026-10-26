# X01 — consolidated mechanism source map

Per-card line-level maps: `V3_EXISTING/M01/01_DIRECT_SOURCE_MAP.md`, `M15/...`, `M17/...`, `M22/...`, `M36/...`. This file is the cross-mechanism index.

## Source identity

- 31/31 S50 selected files exact. Additional required files matched to independent authority records or the staging-zip top-level entry; see `SOURCE_IDENTITIES.json`.
- Local staging zip `3f2c5ed9…` ≠ TD-R05 archive `953c9149…`; archive-level exactness is not claimed.
- Source grade: `HISTORICAL_SOURCE_AUDITED` / `HISTORICAL_RUN`; `CURRENT_INTEGRATION: NOT_VERIFIED`.

## Function index

| M | Symbol | File:lines | Input → output | Actual role |
|---|---|---|---|---|
| M01 | `BackboneState` | `v3/core/state.py:500–614` | dataclass fields → persisted state | Stores baseline (544), strivings (545), gift/disruption shards (546–547), child model (549), initial provenance (531), yearly integrity (532). |
| M01 | `state_to_json/state_from_json` | `v3/io/json_codec.py:405–558` | state ↔ JSON | Persists/read fields; missing keys fall back silently. |
| M01 | `hash_jsonable` | `v3/core/year_record.py:12–14` | JSON → SHA-256 | Record hash, not causal event id. |
| M01 | `GenerationIntegrityAccumulator` | `v3/core/generation_integrity.py:8–78` | stage/status/fallback → diagnostics | Records failures; normal baseline/child-model derivation not recorded. |
| M15 | `infer_parent_baseline_and_regime` | `v3/io/parent_baseline_from_behavior.py:25–86` | parent identity → `(baseline, regime)` | 50 defaults; 50/50 parent average; crude warmth/authority/material thresholds; `# Heuristics`. |
| M15 | `derive_child_expectation_baseline` | `v3/engine/expectation_baseline.py:107–143` | parent categories + regime/environment + rules → categories | Parent category→score, four global modifiers, score→category; missing→hopeful; per-axis YAML rules unused. |
| M15 | `update_striving_step` | `v3/engine/striving_objects.py:242–272` | state/age/config → strivings | `setdefault(ax,"hopeful")`; spawn proxies; no baseline revision. |
| M15 | `spawn_striving_objects_for_age` | `v3/engine/striving_objects.py:127–213` | baseline + age + map → strivings | Baseline selects proxy entries/multipliers; missing→hopeful. |
| M17 | `GiftShard/DisruptionShard` | `v3/core/state.py:338–364` | dataclass records | Flat one-valence records; no event/access parents. |
| M17 | `apply_gift_disruption_shards_from_events` | `v3/engine/expectation_events.py:103–164` | state + selected events → appended shards | LLM `expectation_type`; one gift or one disruption; malheur at identity_load≥60; no mixed/baseline. |
| M17 | `delta_from_event` | `v3/engine/effects/delta_templates.py:17–158` | event + config → deltas | Expectation fulfillment/violation → coherence/social support/alienation; no baseline. |
| M17 | `apply_deltas_to_state` | `v3/engine/effects/delta_templates.py:254–364` | state + merged deltas + events → mutated state | Applies deltas and shards; alienation mutation bug at 314–319. |
| M22 | `child_model_from_parent_baseline_and_regime` | `v3/io/identity_to_backbone.py:60–109` | baseline + regime + age → child model dict | Hardcoded category→rule/taboo; safe-home default if no forbidden/hopeless; `age` unused. |
| M22 | `PASS1_SYSTEM` | `v3/engine/prompts.py:11–33` | system prompt text | Interprets child model (28) and baseline (29); instructs LLM. |
| M22 | `state_summary_from_backbone` | `v3/engine/llm_contract.py:710–739` | state → Pass 1 summary | Exposes child model/baseline; safe-home fallback if child model empty. |
| M22 | `score_event_candidate` | `v3/engine/scoring.py:148–160` | event + summary → score | Uses child-model assumed rules for epistemic-rupture fit. |
| M36 | 50-default path | `parent_baseline_from_behavior.py:18–53`; `expectation_baseline.py:131–135`; `striving_objects.py:256–257`; `identity_to_backbone.py:81–90`; `llm_contract.py:722–731`; `server/generation/simulation.py:369`; `v2/spec.py:3517–3528` | missing → 50 → hopeful/safe-home | Multi-layer semantic default; one-parent dilution; random near-50 in V2 no-WVS path. |

## State read/write audit

| State | Written by | Read by | Provenance |
|---|---|---|---|
| `expectation_baseline` | `identity_to_backbone` 514–555; `striving_update` setdefault 256–257 | `striving_update` 158/166/192; `llm_contract` 735–739; `persona_sheet` 922 | No baseline-specific initial provenance; no event parentage; no revision. |
| `child_model` | `identity_to_backbone` 558–562 | `llm_contract` 710–717; `scoring` 148–160; prompt 28 | No child-model-specific initial provenance; static. |
| `gift_shards`/`disruption_shards` | `apply_deltas_to_state` 359–362 → `expectation_events` 126–163; legacy V2 double call 699–700/934–935 | `persona_sheet` 452–467/938–948; JSON | No event id/access/parents; list-position ids; duplicates possible. |
| `striving_objects` | `striving_update` 258–272 | Pass 1 summary 735–739; persona sheet 922 | Proxy map; baseline multipliers; no shard feedback. |

## First real consumers

- Baseline: `striving_update` → Pass 1 summary → V2 persona sheet.
- Child model: Pass 1 summary + rupture scoring.
- Shards: V2 persona sheet/backstory + JSON only; no V3 causal consumer.
- Required new consumer: C9/C12 same-person event; not present here.

## Actual test/probe evidence

- Focused tests 51 passed; full V3 150 passed/1 environment-data failure.
- Probes: missing parent all-hopeful/safe-home; both-present high-warmth/low-material coarse split; one-present 85/45/20 collapses to all-hopeful/safe-home; environment ignored; one-valence shards; baseline unchanged; alienation delta lost.
- See `TEST_SOURCE_AND_LOGS/` and `TEST_MANIFEST.json`.
