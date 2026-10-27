# X04 M28 — score/select/apply boundary

**Court grade:** `HISTORICAL_SOURCE_AUDITED` + `HISTORICAL_RUN`; current integration `UNTRACED`.
**Coverage:** `PARTIAL_WRONG_MEANING`; the boundary exists, but selection lacks hard admissibility/NO_CHANGE and applies merged arbitrary deltas.
**Authority:** historical policy only.

## 1. Direct source map

| Symbol | File:lines | Input → output | Actual role |
|---|---|---|---|
| `score_event_candidate` | `v3/engine/scoring.py:32-178` | event + summary → score 0..1 | Fixed weights, age/channel/salience/hostage/capacity/wound/boundary/rupture fit |
| `select_candidates` | `scoring.py:197-298` | packet + summary + rng → selected events/magnets | Top 2 major/2 minor/1 surprise + 2 magnets; no hard threshold |
| `run_llm_band_year` | `v3/engine/run_llm_band.py:240-270` | selected events/magnets → merged deltas/state | Fallback first candidate if selection empty; merge/apply |
| `delta_from_event` | `v3/engine/effects/delta_templates.py:17-158` | event kind/intensity/hooks → deltas | Fixed semantic-class→numbers mapping |
| `merge_deltas` | `delta_templates.py:222-251` | multiple deltas → one dict | Sums capacity/alienation/coherence; merges lists |
| `apply_deltas_to_state` | `delta_templates.py:254-364` | merged deltas + events → state | Applies all at once; shard/rupture side effects |

## 2. Actual behavior

- Weights: age .20, channel .15, salience .15, wound .15, capacity .15, hostage .10, novelty -.05, coercion -.05; striving attach bonus .05. `score` clamps 0..1.
- There is **no hard admissibility threshold**. Every event with any score can be selected up to the caps; only intensity pools and shock cap constrain selection.
- `select_candidates` fills major slots with up to 2 attached/unattached, up to 2 minor, then a surprise event with `rng.random() < .10`; magnets top 2.
- If selection returns empty while candidates exist, `run_llm_band_year` takes the **first candidate** (`fallback_first_candidate`) so Pass 2 always has something; if no candidates, fallback packet has already fabricated a practice event (M34).
- `rng = rng or random.Random()` in `select_candidates`; `run_llm_band_year` `rng = rng or random.Random()`; server passes `random.Random()` (system seed) at `server/generation/simulation.py:547`; `run_and_print.py:137` passes `random.Random()`. Surprise selection is not a named deterministic stream.
- Scored events are converted to **deltas**, merged, and applied in one call. Event 1 and event 2 are never separately realized; there is no state-after-event-1 for event 2 to read.
- `delta_from_event` maps event `kind`, `intensity`, offers/costs and wound hooks to fixed numbers (e.g. relationship +3 social support, practice +2 organizing/craft, puncture -4 health/+3 alienation). This is code-authored psychological result, not an actor-specific causal rule.
- `score_event_candidate` wound fit rises with wound sensitivity; boundary fit, rupture assumption fit; no source/actor access. It can favor thematic/wound-matching drama.

**Reviewer probe:** one `practice` candidate selected; `apply_deltas_to_state` changed `practice_stack`; `state.events_this_year` unchanged; no per-event state; selected event only in `yearly_integrity.llm_band.selected_event_ids`.

## 3. N07/N11 differential

N07/N11 need **lawful admissibility** (event can happen under actual world/coactor/access conditions), **ordinary no-event/no-durable-change**, and **independent participant action**. Old M28 has a finite scoring/selection capability and caps, but:
- no hard admissibility; score is a soft ranking, not a legal event gate;
- no typed NO_CHANGE (empty candidates trigger fabrication; zero selection triggers first candidate);
- no independent actor/coactor source;
- random surprise uses unseeded global RNG in current callers;
- all selected events merge into one delta application.

**Coverage:** `PARTIAL_WRONG_MEANING`; retain finite scoring/caps/provenance; adapt admissibility/no-event/named RNG; replace premerged delta application.

## 4. First consumer / tests

First consumer: `run_llm_band_year` state mutation + Pass 2 render; server year record. Tests: `test_llm_contract.py` 18, `test_wave4.py` 14, `test_v5_render_surface_psyche.py` 3; no dedicated test for hard admissibility, no-event, unseeded RNG or per-event sequential selection. **NOT_RUN:** provider model, independent coactor, current C9/C12.

## 5. Disposition / owner

**Retain:** finite candidate schema, scoring/caps, mutation provenance inside the band, explicit `selected_event_ids`.
**Adapt:** hard admissibility gate, named RNG/ADP020, explicit no-event/no-durable-change, source/access conditions, per-event selection state.
**Create:** `EventAdmission`/`NO_CHANGE` records, independent coactor proposal/realization, sequential event effects, C9/C12 consumer.

**Owner:** C8/C9/ADP019/ADP020 + current C12; no native grant.

**Negative/fault:** same two events in reversed order produce identical merged deltas because `merge_deltas` sums; a label-only change in event kind/intensity changes the delta. Both falsify the claim that this is sequential event-conditioned development.
