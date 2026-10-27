# X04 M29 — Pass 2 render-only role

**Court grade:** `HISTORICAL_SOURCE_AUDITED` + `HISTORICAL_RUN`; current integration `UNTRACED`.
**Coverage:** `MEANINGFUL_COVERAGE` for render nonmutation and output separation; `PARTIAL_WRONG_MEANING` for retrospective meaning/causal self-account.
**Authority:** no native rule; render is historical surface.

## 1. Direct source map

| Symbol | File:lines | Input → output | Actual role |
|---|---|---|---|
| `render_year` | `v3/render/phenomenology.py:55-160` | state/derived/render packet/callback → `state.rendered_output` | Pass 2 render; only rendered_output write |
| `build_render_packet` | `v3/engine/llm_contract.py:791-869` | selected events/magnets, deltas, identity, persona context, surface → packet | Pass 2 input; sanitizes surface |
| `build_pass2_prompt` | `v3/engine/prompts.py:132-159` | packet → prompt | Narrative render instruction |
| `parse_render_output` | `llm_contract.py:371-500` | raw → structured render | Sanitizes; fallback scene if empty |
| `validate_render_output` | `v3/engine/validators.py:109-127` | parsed/history → pass/fail | Particularity/jaggedness/no-repeat checks |
| `pass2_corrective_instruction` | `prompts.py:161-168` | failures → retry instruction | Retry on validation failure |
| `backbone_hash` | `v3/core/invariants.py:338-343` | state → hash excluding rendered_output | Render nonmutation test |

## 2. Actual behavior

- `render_year` constructs base year/age/derived; without `render_packet+llm_callback` it only sets `state.rendered_output` (no narrative snapshot).
- With packet/callback, it calls the LLM, parses/validates; on validation failure it calls the LLM **again** with a corrective prompt; it merges narrative/dialogue/consistency/particularity/jaggedness/micro-causality into `rendered_output`.
- It does **not** mutate backbone fields; `backbone_hash` excludes only `rendered_output`.
- Empty/missing scene becomes `"[This year had no recorded scene.]"` and `_integrity=degraded`; if validation still fails, it uses first parse. This is a render fallback, not actor no-change.
- `run_llm_band_year` is **not** render-only: it applies all merged deltas and creates rupture/shards before calling `render_year`. The invariant test calls `render_year` alone, not `run_llm_band_year`.
- `render_year` can make **two ordinary LLM calls** (initial + corrective retry); this is not a retrospective first-half call and is not part of the user-settled no-intermediate-call batch.
- `build_render_packet` receives `surface_psyche`; `_sanitize_render_packet_surface_psyche` allowlists surface fields; analyst/history are excluded. Good separation at this grain.
- `previous_scene` is included if not `"[This year had no recorded scene]"`; structural annotations without that marker can be treated as previous scene (M37).

**Reviewer probe:** direct `render_year` with fake callback produced two calls (`pass2`, `pass2_retry`) but `backbone_hash` unchanged and scene set. `run_llm_band_year` changed backbone before render.

## 3. N09/N11 differential

N09 needs **actor-owned, fallible retrospective memory and later meaning**, with objective history distinct. Old M29:
- has render-only nonmutation, surface allowlist, particularity/jaggedness validation and retry;
- has no actor access, memory store, fallibility, forgetting, reconstruction, or later same-person read;
- `rendered_output` is a narrative surface, not actor memory;
- retrospective meaning is generated in the same annual pass, not first half of N+1 after a sequential batch;
- a renderer could not lawfully write backbone; current code honors that at the function grain.

**Coverage:** `MEANINGFUL_COVERAGE` for render isolation/contract; `MISSING` for fallible retrospective memory/meaning.

## 4. Tests / first consumer

Tests: `test_architecture_invariants.py::test_llm_no_backbone_mutation` (4 total in file), `test_v5_render_surface_psyche.py` 3, `test_v5_persona_sheet_surface_psyche.py` 2, `test_v5_v2_chat_prompt_no_raw_v5_leaks.py` 1; reviewer probe. No test of retrospective memory, actor access or batch.

First consumer: V2 persona/backstory and chat prompt; `persona_sheet` surface; no current C9/C12 semantic consumer.

## 5. Disposition / owner

**Retain:** render-only isolation, surface allowlists, structured packet, validation/retry only as render quality control, not state mutation.
**Adapt:** separate retrospective first-half call from event realization; pass an actor-accessible trajectory/memory record; do not treat renderer output as actor memory or causal state.
**Create:** `RetrospectiveRecord` with actor access/fallibility, `MemoryMeaningAdmission` through ADP016/017/SCI05 if it becomes causal; later C9/C12 consumer.

**Owner:** ADP016/017/SCI05 + C9/C12; no native grant.

**Negative/fault:** If a renderer changes backbone or a retrospective narrative is later read as objective event, that is a RED. If the same scene is produced from a hash-only state change without semantic difference, the consumer is not semantic.
