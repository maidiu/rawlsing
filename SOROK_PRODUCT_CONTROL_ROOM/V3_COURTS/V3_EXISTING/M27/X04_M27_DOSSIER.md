# X04 M27 — Pass 1 LLM proposal

**Court grade:** `HISTORICAL_SOURCE_AUDITED` + `HISTORICAL_RUN`; current integration `UNTRACED`.
**Coverage:** `PARTIAL_WRONG_MEANING`. Proposal-only boundary is real; selected proposals become code-applied premerged psychological deltas.
**Authority:** no native rule; model callback is caller-supplied.

## 1. Direct source map

| Symbol | File:lines | Input → output | Actual role |
|---|---|---|---|
| `run_llm_band_year` | `v3/engine/run_llm_band.py:146-431` | state/derived/config + `llm_callback` → mutated state/derived | Pass 1, selection, merged deltas, Pass 2 render |
| `state_summary_from_backbone` | `v3/engine/llm_contract.py:518-789` | state/derived/identity → summary | Prompt input; includes baseline/child model/strivings/registers |
| `build_pass1_prompt` | `v3/engine/prompts.py:107-131` | summary + suggested targets/backdrop → prompt | Proposal-only instruction |
| `pass1_response_instruction` | `prompts.py:171-178` | none → text | CandidatePacket caps/schema |
| `parse_candidate_packet` / `_with_fallback` | `llm_contract.py:87-211` | LLM raw → packet | Parse/truncate; fabricates fallback if empty (M34) |
| `select_candidates` | `v3/engine/scoring.py:197-298` | packet + summary + rng → events/magnets | M28 |
| `delta_from_event` / `merge_deltas` / `apply_deltas_to_state` | `v3/engine/effects/delta_templates.py:17-364` | selected events → merged deltas → state | M28/application |

## 2. Actual flow

1. `run_llm_band_year` builds `state_summary`; adds suggested targets from active strivings; may add country/decade backdrop from `fetch_country_history` (external history fetch; not source-grounded actor data).
2. One Pass-1 `llm_callback` call returns a CandidatePacket (caps: 6 events, 4 magnets, 3 branches).
3. `parse_candidate_packet_with_fallback` parses/truncates; if both lists empty, a fabricated `fallback_ev_*` practice event is added.
4. `select_candidates` scores/selects up to 2 major, 2 minor, 1 surprise + 2 magnets.
5. All selected event/magnet deltas are computed, **merged**, and applied to the state in one `apply_deltas_to_state` call; then `compute_all_derived`.
6. Pass 2 renders a scene from the selected events and applied deltas; `render_year` may call the LLM again and retry on validation failures.
7. `run_llm_band_year` returns updated derived; the state has changed.

**Reviewer probe:** fake Pass 1/Pass 2 callbacks produced calls `llm_band_pass1_age_8`, `llm_band_pass2_age_8`, `llm_band_pass2_age_8_retry`; the selected event `ev_x04` was **not** appended to `state.events_this_year`; `practice_stack` changed; `backbone_hash` changed after the band; `yearly_integrity.llm_band.status="applied"`.

## 3. Why this is not the user-settled second half

The target second half of call N proposes **3–5 contingent concrete events**; Rawlsing then realizes them sequentially. Old Pass 1:
- proposes up to 6 **annual candidates**, not a 3–5 conditional batch;
- selected proposals are converted to **pre-merged code deltas** before any sequential realization;
- no event occurrence/time/source/access/admission is recorded in the canonical event ledger;
- no independent coactor action;
- no per-event state used by the next event;
- one Pass-1 call and one Pass-2 call (plus retry), not a batch call with no intermediate ordinary calls;
- the band is applied after `run_one_year` and after year/age increment, so it is not a "second half" at the batch boundary.

The code has a genuine proposal boundary and schema; it is not the developmental recursion.

## 4. Reuse / adaptation / creation

**Retain:** proposal-only model boundary, candidate schema, caps, prompt separation, provenance snapshots, `yearly_integrity` band ledger.
**Adapt:** replace free annual proposal with compact 3–5 conditional event specifications; keep factual contingency, actor access and independent coactor action distinct; do not merge effects before sequential realization; remove fabricated fallback.
**Create:** `BatchProposal` (second half), canonical event admission, per-event realization, retrospective first half (N+1), explicit clocks and access.

**First consumer today:** `run_llm_band_year` → state deltas + Pass 2 render; server year record. Required future consumer: C9/C12 same-person event sequence.

**Tests:** `test_llm_contract.py` 18 passed (parse/fallback/render packet), `test_v5_render_surface_psyche.py` 3 passed; no test of sequential batch or independent coactor. **NOT_RUN:** provider/LLM person run, batch engine, current C9/C12.

**Negative/fault:** changing event-1 has no event-2 reception effect because there is no event sequence; a label-only change in the annual packet can change deltas and render because the LLM label is the semantic class. These are discriminating failures for the target.

**Owner:** C6/C8/C9/C12 + ADP016/017/SCI05; no native grant by this review.
