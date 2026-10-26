# M17 — Gift/Disruption shards and expectation events: direct source map

**Source grade:** HISTORICAL_SOURCE_AUDITED / HISTORICAL_RUN; CURRENT_INTEGRATION: PATH_LOCATED, no V3 causal consumer.
**Primary files:**
- `v3/core/state.py` `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2` — `GiftShard` (338–350), `DisruptionShard` (353–364), `BackboneState.gift_shards/disruption_shards` (546–547).
- `v3/engine/expectation_events.py` `307ae929a43935170a2f792b4a702a02ac54819a4fa897aa3fef4a099a96cb49` — templates, suggested targets, shard creation.
- `v3/engine/effects/delta_templates.py` `7d99ddf26fd45b52e5e3c10074066ba5e06d17cdaf1fabad06298af3770815f0` — event deltas and shard application.
- `v3/expectation_event_templates.yaml` `4fead2145e6b5695d016e6d22f7dc52349ac43c970c21875b49f728e9d5e0fee` — templates.
- `v2/run_full_simulation_with_llm_log.py` (legacy V2 runner; not in S50 31-file manifest) — double-application call sites 699–700 and 934–935.
- `v3/io/persona_sheet.py` (not in S50 31-file manifest) — first visible consumer of shards, 452–467 and 938–948.

## Exact creation path

`apply_gift_disruption_shards_from_events(state, selected_events)` — `expectation_events.py:103–164`:

1. Build set of active `striving_objects` ids (111).
2. For each selected event: read `expectation_type`; only `"fulfillment"` or `"violation"` accepted (113–115). **Mixed is not accepted.**
3. Read `striving_object_id`; require it to be nonempty and in active ids (116–118).
4. Find the striving for `need_axis`; label = event label (120–125).
5. Fulfillment → append `GiftShard(id=gs_{year}_{age}_{len}, valence="positive", prediction_error="medium", opacity="low", ...)` (126–140).
6. Violation → read `identity_load` (default 50); `malheur_risk = identity_load >= 60`; append `DisruptionShard(valence="negative", prediction_error="high" if malheur_risk else "medium", opacity="high" if malheur_risk else "medium", malheur_risk=...)` (141–163).

There is no read of `state.expectation_baseline`, `need_axis` category, parent behavior, material condition, care/availability, event source/actor, or prior shard. The shard's label is the event's free-text label. The valence/type is supplied by the event/LLM; the code does not adjudicate whether the event actually fulfills or violates the actor's expectation. The `expectation_event_templates.yaml` `baseline_high_impact` and template `valence` fields are not consulted by this function.

## Downstream delta path

`delta_from_event(event, config)` — `delta_templates.py:17–158`:
- `kind=expectation_event` and `expectation_type=fulfillment`: `coherence_delta += 2*mult`, `capacity.social_support += 2*mult` (101–105).
- `expectation_type=violation`: `coherence_delta -= 2*mult`, `alienation_delta += 2*mult` (106–108).
- `mult = 1.0` minor, `1.5` major, `2.0` shock (37). Caps from config (27–33).
- `apply_deltas_to_state` applies deltas and then calls `apply_gift_disruption_shards_from_events` (355–362).

### Source defect: alienation update is lost

`apply_deltas_to_state` (314–322) computes `new_agg` and then executes:
```
v = state.alienation_vector
v.structural = v.affective = v.institutional = new_agg
state.alienation = new_agg
```
But `AlienationVector` fields are `distant_others`, `near_others`, `self`, `moral_totality` (`state.py:95–104`). The assignments create three **dynamic attributes** and leave the real vector unchanged. `state.clamp_all()` then recomputes `state.alienation = state.alienation_vector.aggregate()`, resetting the scalar. The probe with `alienation_delta=3.0` produced: before scalar 0.0, after scalar 50.0, vector unchanged 50.0; dynamic attrs `structural/affective/institutional=53.0`. The expectation-violation alienation consequence therefore does not persist. This is an engineering RED in the same consumer path.

### Source defect: duplicate shard creation in the legacy V2 runner

`apply_deltas_to_state` already calls `apply_gift_disruption_shards_from_events` (`delta_templates.py:359–362`). The legacy runner then calls it again immediately: `v2/run_full_simulation_with_llm_log.py:699–700` and `934–935`. A fulfillment/violation event can therefore create two shards (ids differ by list length). The newer `v3/engine/run_llm_band.py:266–270` calls only `apply_deltas_to_state`, so the duplicate is specific to that V2 integration path. No dedup or idempotency key exists.

## First consumers

- `v3/io/persona_sheet.py:452–467` renders each shard as a backstory line: gift = "received a gift: {label}—touched their {need}"; disruption = "a disruption: {label}" or "a disruption that cut to the bone" when `malheur_risk`. `persona_sheet.py:938–948` puts the last 10 gifts/disruptions in the V2 sheet.
- `v3/io/json_codec.py:525–530` persists the lists.
- The Pass 1 state summary (`llm_contract.py`) does **not** include gift/disruption shards; `scoring.py` does not read them; `v3/psyche/flow.py` and `v3/core/derived.py` do not read them.
- Therefore the first real consumer is the V2 persona/backstory surface, not a V3 causal state consumer.

## Actual probe

`probe_v3_x01.py` with one active attachment striving (`identity_load=65`) and the same label "Parent works late but calls to say she loves me":
- `expectation_type=fulfillment` → one `GiftShard` (valence positive, prediction_error medium, opacity low), zero disruption shards, baseline unchanged.
- `expectation_type=violation` → one `DisruptionShard` (valence negative, prediction_error high, opacity high, malheur_risk true), zero gift shards, baseline unchanged.
- There is no mixed result. The same event cannot produce both a gift and a disruption; the LLM's `expectation_type` decides which record exists.

## Tests

- `v3/tests/test_wave4.py:136–167` asserts one gift for a fulfillment event and one malheur-risk disruption for a high-identity-load violation. It does not test mixed events, baseline influence, duplicate creation, provenance, or later state revision.
- `test_wave4` 14 passed; full `v3/tests` 150 passed/1 environment-data failure.

## Grade

**PARTIAL_WRONG_MEANING.** Persistent one-valence shards are implemented; the event is pre-classified as reward/wound by an LLM-supplied label, the actor's baseline is not consulted, mixed care+insufficiency is not representable, and the shards have no V3 causal consumer. The alienation-delta loss and duplicate-creation path are concrete engineering REDs.
