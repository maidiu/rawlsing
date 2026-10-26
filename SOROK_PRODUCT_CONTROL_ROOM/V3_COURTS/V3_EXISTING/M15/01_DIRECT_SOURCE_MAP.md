# M15 — need axes / expectation baseline: direct source map

**Source grade:** HISTORICAL_SOURCE_AUDITED / HISTORICAL_RUN; CURRENT_INTEGRATION: PATH_LOCATED, not native/current.
**Primary files:**
- `v3/core/state.py` `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2` — `NEED_AXES` (305–309), `BASELINE_STATES` (309), `BackboneState.expectation_baseline` (544).
- `v3/engine/expectation_baseline.py` `632e1e608bfc674a241e57bafa24e91834a2b8bdc3e4ed326dae6fca4e695d43` — all formula code.
- `v3/io/parent_baseline_from_behavior.py` `4e5be6448a5b76c413492ec2a83b62d9e9a2247ce131a094727d974a17cf750b` — parent behavior → baseline/regime.
- `v3/io/identity_to_backbone.py` `cb29c9595ac495c3b69b693d4c58a278e9ef1f63a7a8917d8e407920fbd3bdda` — initialization consumer (514–555).
- `v3/need_axis_rules.yaml` `e18cb396cc5dfba28cad1681ca86fb855496a2261b7942d408eedcccbf67bf95` — declared rule data (per-axis rules are not fully consumed; see below).
- `v3/engine/striving_objects.py` `78c79a9312b05aa51220d09bb63c91cafd6bb204f2c398ac1876b1ef3144c1c3` — yearly consumer/setdefault (256–257) and spawn (127–213).

## Exact functions, inputs, outputs

### `infer_parent_baseline_and_regime(parent_identity)` — `parent_baseline_from_behavior.py:25–86`
Input: object/dict with `parent_behavior.father/mother` or `parents.father/mother`, each optionally `parental_warmth`, `parental_authority`, `parental_material_support` in 0–100.
Default per field: `_float(..., 50)` (18–22); missing parent behavior is 50. Father/mother values are averaged: `warmth=(warmth_f+warmth_m)/2`, `authority=...`, `material=...` (45–53).
Output: `(baseline: dict[NeedAxis,str], regime: dict[str,float])`.
Algorithm:
1. all axes = `"hopeful"` (56–58);
2. `warmth < 40` → attachment `"forbidden"` if `<30` else `"hopeful"`; belonging `"hopeless"` if `<25`, `"forbidden"` if `<40`, else `"hopeful"` (59–61);
3. `authority > 60` → autonomy `"forbidden"` if `>70`; safety `"forbidden"` if `>65` (62–64);
4. `material < 35` → status `"hopeless"` if `<25` else `"forbidden"`; competence `"hopeless"` if `<30` else `"hopeful"` (65–67);
5. regime: `coercion=authority`, `openness=100-authority`, `anxiety=100-warmth`, `shame=50` (60 if warmth<40 and authority>55), `modeling_consistency=warmth*0.5 + (100-authority)*0.3 + 20` (69–85).
Comment in source calls these heuristics (line 55). No `availability`, `reliability`, `harshness`, `spiritual_support`, work schedule, or actual care-rhythm fields are read.

### `derive_child_expectation_baseline(parent_baseline=None, transmission_regime=None, environment=None, rules=None)` — `expectation_baseline.py:107–143`
Inputs: parent categories per axis; regime values; environment values; optional rule dict.
Algorithm:
- `regime = dict(transmission_regime or {})`; `env` keys merged only by `setdefault` (120–124);
- `rules = rules or load_need_axis_rules()` (125);
- `parent_to_score` from meta or `PARENT_CATEGORY_TO_SCORE` (29–34, 127);
- per axis: `parent_cat = parent_baseline.get(ax) or "hopeful"`; score = parent_to_score[parent_cat] default 0; clamp to `[score_min,score_max]` (default `[-2,2]`) (131–135);
- `_apply_global_modifiers(scores, rules, regime)` (137);
- map score: 2/1→entitled, 0→hopeful, -1→forbidden, -2→hopeless (22–28, 139–142).

`_apply_global_modifiers` (68–104) reads only `rules["global_modifiers"]`; conditions support `*_gte`/`*_lt`; actions `all_axes` or `axes`. The YAML's **`axis_rules`, `flags`, `conditional_modifiers`, `base_by_meaning_frame`, `meta.thresholds`, and `seed_weights` are not read by this function**. The `environment` keys (`external_threat`, `economic_precarity`, `institutional_reliability`, `status_competition`, `collective_solidarity`) do not match any global modifier condition and therefore have no effect. `meta.seed_weights` (`two_caregivers: p1 0.55/p2 0.35/env 0.10`; `one_caregiver: p1 0.75/env 0.25`) are also **not consumed**: `infer_parent_baseline_and_regime` simply averages father/mother 50/50 and defaults a missing parent to 50. The probe confirms `with_high_precarity == without_env` and `actual_rules == empty_rules` for these keys.

Global modifiers actually used:
- `warmth>=70 and modeling_consistency>=60`: all axes +1 (clamped).
- `anxiety>=80`: attachment, safety −1.
- `shame>=80`: autonomy, eros_intimacy, beauty_play −1.
- `openness>=70`: competence, beauty_play, meaning +1.
No per-axis `warmth_gte`, `coercion_gte`, `economic_precarity_gte`, `external_threat_gte`, etc. are applied.

### `striving_update` — `striving_objects.py:242–272`
For every axis missing from `state.expectation_baseline`, `setdefault(ax, "hopeful")` (256–257). It does not update existing categories from events. `spawn_striving_objects_for_age` reads baseline to choose proxy entries and multipliers; missing axis or missing proxy entry is treated as `"hopeful"` (158,166,192). No function elsewhere assigns or revises `state.expectation_baseline` from experience (search results: only initialization and these `setdefault`s).

## Actual probe values

Sourcefree read-only probe (`TEST_SOURCE_AND_LOGS/probe_v3_x01.py`, output `probe_v3_x01_output.json`):

- **Missing parent identity `{}`**: inferred baseline all `hopeful`; regime `warmth=50, coercion=50, openness=50, anxiety=50, shame=50, modeling_consistency=60`; derived all `hopeful`.
- **Both parents present, warmth=85, authority=45, material=20**: inferred parent baseline `attachment/belonging/autonomy/safety/...=hopeful`, `status=competence=hopeless`; derived after global warm modifier `attachment/autonomy/belonging/safety/meaning/justice/beauty/play/eros=entitled`, `status/competence=forbidden`; environment high precarity has no additional effect. The global warm+consistent +1 modifier therefore shifts `hopeless`→`forbidden` and `hopeful`→`entitled` without new material evidence; this is a semantic category change driven by warmth, not by the material condition.
- **One present parent, warmth=85, authority=45, material=20, other missing**: averages become `warmth=67.5`, `authority=47.5`, `material=35.0`; all ten axes and derived baseline are `hopeful`; child model is the default safe-home model. This is the same observable outcome as fully missing parent behavior **for this threshold-boundary input**. Lower material can cross the status/competence threshold, so the general defect is the 50 dilution plus the absence of a love/availability schema, not a universal one-parent erasure.
- **Cold high material (warmth=30, authority=80, material=80)**: attachment/belonging/safety/autonomy `forbidden` (attachment specifically `hopeful` at warmth=30 because the code uses `<30`), status/competence `hopeful`; child model narrow; default safe-home rules absent.

## First real consumer and later consumption

1. `v3/io/identity_to_backbone.py:514–555` initializes `state.expectation_baseline` (only at creation).
2. `v3/engine/striving_objects.py:256–270` in the yearly `striving_update` step: spawns proxy `StrivingObject`s and applies baseline multipliers; missing axes become `hopeful`.
3. `v3/engine/llm_contract.py:735–739` puts the baseline into the Pass 1 state summary; `v3/engine/prompts.py:29` instructs the LLM how to interpret it.
4. `v3/io/persona_sheet.py:922,956` exposes it to the V2 persona sheet.
No V3 pressure-flow, derived index, or event-admission function reads it.

## Tests

- `v3/tests/test_connector_and_field_injection.py:66–73` asserts only that `expectation_baseline` is a non-None dict when parent/regime are supplied.
- `v3/tests/test_llm_contract.py:166,180–187` asserts the summary includes the key and can carry `attachment=forbidden`.
- No test asserts missing→hopeful, one-parent dilution, love+insufficiency, environment application, per-axis YAML rules, or baseline revision.
- Actual runs: connector 11 passed; llm_contract 18 passed; full `v3/tests` 150 passed/1 environment-data failure.

## Grade

**PARTIAL_WRONG_MEANING.** Typed axes/categories and a derivation function are real; the implemented meaning is a flat, parent-defaulted, static category vector. The Neo-V3 requirement (thick, scoped, historically weighted, contradictory care with love and insufficiency separable) is not met.
