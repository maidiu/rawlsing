# X04 M34 — fallback concretization

**Court grade:** `HISTORICAL_SOURCE_AUDITED` + `HISTORICAL_RUN`; current integration `UNTRACED`.
**Coverage:** `CONFLICTING` with legitimate NO_CHANGE; fabrication should be removed.
**Authority:** no native rule.

## 1. Direct source map

| Symbol | File:lines | Input → output | Actual role |
|---|---|---|---|
| `parse_candidate_packet_with_fallback` | `v3/engine/llm_contract.py:159-170` | raw LLM → packet | Parses then calls fallback |
| `make_fallback_event` | `llm_contract.py:173-187` | year/age → event dict | Fabricated `practice` event |
| `fallback_candidate_packet_if_empty` | `llm_contract.py:190-211` | packet → mutated packet | Adds fallback if both events/magnets empty; marks degraded |
| `run_llm_band_year` | `v3/engine/run_llm_band.py:204-262,240-252` | empty/parse/no-candidate → derived | Empty/parse/no-candidate return unchanged; empty packet fallback; if selection empty, first candidate fallback |
| `RUN_LLM_BAND` status | `run_llm_band.py:205-262` | status | `empty_response`, `parse_failed`, `no_candidates`, `fallback_first_candidate` |

## 2. Actual behavior

- Empty LLM string → status `empty_response`, no mutation, returns derived (no fallback; honest no-change-ish but no typed record).
- Parse failure → `parse_failed`, no mutation.
- A syntactically valid packet with **empty candidate lists** goes through `parse_candidate_packet_with_fallback` **before** the `no_candidates` check: it fabricates `fallback_ev_{year}_{age}` (`kind=practice`, minor, empty hooks/domains), marks `_integrity` degraded; then selection/application mutates practice deltas and renders.
- `no_candidates` is effectively unreachable for ordinary parsed packets because fallback runs first; it is not a lawful no-event path. A fallback packet containing only a magnet is also not a no-event path.
- If scoring/selection returns zero selected events/magnets while candidates exist, `run_llm_band_year:244-252` selects the first event or magnet (`fallback_first_candidate`) and applies it.
- The fallback event is not in `state.events_this_year`; only the band record lists it.
- Tests `test_llm_contract.py` 18 confirm fallback packet when both lists empty; no test for full-band fallback mutation/NO_CHANGE/legitimate empty.

**Reviewer probe:** empty packet → `fallback_ev_2024_8` practice; band with a simple candidate applied practice changes and three LLM calls (Pass1, Pass2, retry). The fallback path is real.

## 3. N11 differential

The user-settled cycle permits **legitimate no-event/no-durable-change** and conditional batch outcomes. M34 manufactures a practice event so "something happens"; it conflates:
- LLM empty packet vs lawful no-event;
- insufficient evidence/HELD vs fabricated event;
- non-memorable routine vs practice delta.

**Coverage:** `CONFLICTING`; remove fabrication, preserve typed no-event/no-change/held.

## 4. Tests / first consumer / disposition

First consumer: `run_llm_band_year` state mutation + render; no current C9/C12. Tests: `test_llm_contract.py` 18; no full-band fallback test. **NOT_RUN:** provider, actual person, batch.

**Retain:** typed integrity/degraded status, no-mutation paths for empty response/parse failure/no candidates.
**Adapt:** make empty candidate list a typed `NO_EVENT`/`HELD` result; never fabricate.
**Remove:** `make_fallback_event`/first-candidate fallback as psychological event source.
**Create:** explicit no-change/insufficient-evidence records and batch-level no-durable-change.

**Owner:** C8/C9/C12 product owner; no native grant.

**Negative/fault:** empty packet with no lawful event must not produce practice deltas; a fallback practice event is indistinguishable from an actual LLM proposal except provenance. This is a RED for any claim that the old band preserves legitimate no-change.
