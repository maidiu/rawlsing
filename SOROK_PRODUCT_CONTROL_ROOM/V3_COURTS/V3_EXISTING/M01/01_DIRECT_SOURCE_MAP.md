# M01 — persistent BackboneState: direct source map

**Source root:** `<USER_HOME>/Desktop/Rawlsing/Rawlsing_code_bundle_staging`
**Source grade:** HISTORICAL_SOURCE_AUDITED / HISTORICAL_RUN (local read-only probe); CURRENT_INTEGRATION: NOT_VERIFIED.
**Files:** `v3/core/state.py` SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`; `v3/core/year_record.py` `4bbd7518a6ec8bc8dd22758a2f9e876882253dfd59021a998a6d541b23e5cfc2`; `v3/core/generation_integrity.py` `5265aac2fda4d6e6ac62927353518045f215d7d1916930e19e980b6d77eff214`; `v3/io/json_codec.py` (not in S50 31-file manifest; `state_to_json`/`state_from_json` read directly).

## Exact symbols

| Symbol | Lines | Input / output | Notes |
|---|---|---|---|
| `BackboneState` | `state.py:500–614` | dataclass; persisted yearly | Contains `expectation_baseline` (544), `striving_objects` (545), `gift_shards` (546), `disruption_shards` (547), `child_model` (549), `initial_state_provenance` (531), `yearly_integrity` (532), pressure-flow fields (536–539). |
| `BackboneState.__post_init__` | 563–566 | creates default domains | No baseline/child-model initialization. |
| `BackboneState.clamp_all` | 568–614 | mutates numeric fields | Clamps numeric state; does not add provenance or event parentage; gift/disruption shards have no clamp. |
| `hash_jsonable` | `year_record.py:12–14` | dict/JSON → SHA-256 | Stable JSON hash for a record; not a causal event identity. |
| `state_and_derived_from_snapshot` / `normalize_year_record_snapshot` | `year_record.py:17–64` | legacy tuple or YearRecord → normalized dict | Normalizes state/derived shape; no baseline/child-model-specific audit. |
| `GenerationIntegrityAccumulator` | `generation_integrity.py:8–78` | stage/status/source inputs/fallback → diagnostic dict | Records failures; normal successful baseline/child-model derivation is not recorded. |
| `state_to_json` / `state_from_json` | `json_codec.py:405–558` | `BackboneState` ↔ JSON | Persists `expectation_baseline`, `gift_shards`, `disruption_shards`, `child_model` (525–530); missing keys fall back silently. |

## What is actually persisted

The probe called `backbone_state_from_identity({}, year=1990, age=0)` and serialized/read the state through the source helpers. The state contains the ten-axis baseline and child model, but `initial_state_provenance.fields` has **no** `expectation_baseline` or `child_model` entry. `initial_state_provenance` records identity input plus selected capacity/reproduction/practice fields; it does not record the derivation rule version, parent behavior inputs, or environment inputs for M15/M22/M36.

`GiftShard`/`DisruptionShard` carry `year`, `age`, `need_axis`, `striving_object_id`, `label`, `valence`, `prediction_error`, `opacity`, `malheur_risk`; they do **not** carry the selected event id/hash, source/access actor, causal parents, or a derivation rule. Their ids are `gs_{year}_{age}_{len(gift_shards)}` / `ds_{year}_{age}_{len(disruption_shards)}` (`expectation_events.py:127,150`), i.e. list-position identities, not content hashes or event refs.

## Adjacent seeded fields (not M15/M36)

`identity_to_backbone.py` also seeds capacity (class/urbanicity/minority lookups, `246–260`), reproduction constraints (class lookups, `286–313`), impunity (SES/minority, `315–337`), autonomy/safety (SES/minority plus universal 65/68, `339–369`), practice stack (SES/age, `386–405`), parent magnets (`mother` 60, `father` 55, `407–434`), wound vector (`592–605`), frameworks/cracks (`607–625`), and family/body domains (`657–674`). These are outside M15/M36 but contaminate any claim that the initial state is an actual care-history carrier. They must be separately owned/stripped before reuse.

## Callers / consumers

- `v3/io/identity_to_backbone.py:225` creates `BackboneState`; 514–572 writes baseline/child model.
- `v3/engine/yearly_step.py:12–99` mutates the state and writes `yearly_integrity`; `striving_update` is dispatched at 146.
- `v3/io/json_codec.py` round-trips the state.
- `v3/io/persona_sheet.py:922,938–948` exposes baseline and recent shards to the V2 surface.
- `v3/engine/llm_contract.py:710–739` exposes child model/baseline in the Pass 1 summary.
- No canonical event ledger parentage for baseline/child model/shards was located.

## Tests actually run

Focused sourcefree tests: `v3/tests/test_connector_and_field_injection.py` (11 passed), `v3/tests/test_wave4.py` (14 passed), `v3/tests/test_llm_contract.py` (18 passed), `v3/tests/test_v5_baseline_load.py` (8 passed). Full `v3/tests`: 150 passed, 1 environment/data failure (country canonicalization `MDV` vs `Maldives`); the test suite does not assert baseline/child-model provenance or shard parentage.

## Grade and limit

**INFRASTRUCTURE_ONLY** for the M15/M17/M22/M36 fields. Persistence and JSON roundtrip exist; causal history, rule identity, scope, uncertainty, actor-access and event parentage for these fields do not. This is a historical state container, not a current C9/C12 causal person.
