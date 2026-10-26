# X02 — pressure-flow, conductance, grooves and interpressure source atlas

**Status:** `X02_SOURCE_AUDITED__HISTORICAL_RUN_82_TESTS__CURRENT_INTEGRATION_NOT_VERIFIED__NO_NATIVE_GRANT`.

**Source:** authorized local historical bundle `<V3_SOURCE_ROOT>`, read directly at the file/body level. Exact hashes and line counts are in `source_identity.json` and `SOURCE_INDEX.json`. **Archive-wide caveat:** the local staging zip SHA-256 is `3f2c5ed9…`; it is not the TD-R05 original archive identity `953c9149…`. The inspected files match the local source directory, the same entries inside the local zip, and the S50 31-file identity manifest. No archive-wide identity is claimed.

**Historical execution:** 82 focused historical V3 tests passed in one reviewer run (`logs/pytest_x02_original_v3.log`). This is historical source execution, **not** current Sorok integration and **not** a native scientific rule.

---

## 1. Actual call graph

```text
run_and_print / historical yearly runner
  -> run_one_year(state, derived, config, step_order)            v3/engine/yearly_step.py:12
       -> 19 configured steps in order (event_sampling, reproduction,
          capacity, health, buffers, frameworks, domains, cracks/alienation,
          metabolization/plasticity, stability_inertia, striving,
          practices/infrastructure, topology/boundary, attention,
          signal, style, render)                                  v3/v3_yearly_step_order.yaml
       -> state.year += 1; state.age += 1                         v3/engine/yearly_step.py:56-57
       -> run_pressure_flow_cycle(state)                          v3/engine/yearly_step.py:68-70
            -> assign_sublimation_channels(state)                 v3/psyche/flow.py:767-768
                 -> _seed_wound_scores(state)                     v3/psyche/channels.py:103-150
                 -> _seed_domain_scores(state, domain)            v3/psyche/channels.py:153-187
                 -> _pick_channel(scores)                         v3/psyche/channels.py:190-191
            -> compute_baseline_load(state)                        v3/psyche/flow.py:769-770
                 -> _stratum_latent_pressure + weights             v3/psyche/gating.py:10-58,108-146
            -> apply_expression_gating(state)                      v3/psyche/flow.py:771-772
                 -> _derive_hostage_index(state)                   v3/psyche/gating.py:61-71
            -> _prior_memory(state)                               v3/psyche/flow.py:233-235
            -> _domain_charge_ledger(state, memory)               v3/psyche/flow.py:406-465
                 -> _derive_current_charge                     v3/psyche/flow.py:268-284
                 -> _dominant_channel                          v3/psyche/flow.py:359-363
                 -> _channel_conductance                       v3/psyche/flow.py:366-403
                 -> derive_attribution_and_vessel_hint          v3/psyche/vessels.py
                 -> derive_insulation_profile                   v3/psyche/insulation.py:72-147
            -> derive_vitality_profile(state, ledger, memory)      v3/psyche/vitality.py:85-191
            -> _merge_vitality_profile(ledger, profile)            v3/psyche/flow.py:468-498
            -> _simulate_domain_routes_transactionally             v3/psyche/flow.py:547-567
                 -> _apply_single_domain_route(working, item)      v3/psyche/flow.py:500-544
            -> _history_after_append(state, snapshot)              v3/psyche/flow.py:651-659
            -> _update_memory(history, prior_memory)               v3/psyche/flow.py:678-750
            -> _compact_surface_profile(ledger, memory, vitality)  v3/psyche/flow.py:576-617
            -> _analyst_account(ledger, trace_delta, per_domain)   v3/psyche/flow.py:620-648
            -> _commit_route_state(state, routed_state)            v3/psyche/flow.py:570-573
            -> write pressure_flow_history/memory/surface/analyst  v3/psyche/flow.py:806-809
            -> write yearly_integrity["pressure_flow"]             v3/psyche/flow.py:810-822
       -> optional run_llm_band_year(state, derived, ...)          v3/engine/run_llm_band.py:146
            -> Pass 1 -> select -> apply deltas -> re-derive
            -> build_render_packet(..., surface_psyche=state.surface_psyche_profile)
            -> Pass 2 render; no pressure-flow rerun                  v3/engine/run_llm_band.py:264-380
```

**Propagation caveat:** in the historical runner, the LLM band runs **after** `run_one_year`, i.e. after the post-year pressure-flow cycle. Its applied deltas do not re-enter the pressure-flow ledger until a later cycle. `build_render_packet` receives the previous `surface_psyche_profile`. This is not the user-settled sequential event loop.

---

## 2. Actual functions, inputs, outputs and mutation

| Function | Exact source | Reads | Writes | Conditions / limits |
|---|---|---|---|---|
| `run_pressure_flow_cycle` | `flow.py:753-843` | Whole state, `pressure_flow_memory`, flags | `affect_channel`, `baseline_load`, `expression_rate`, `expressed_aim` (pre-route); route objects; `pressure_flow_history`, `pressure_flow_memory`, `surface_psyche_profile`, `analyst_pressure_account`, `yearly_integrity`, diagnostics | Four optional flags; default all true; on exception records diagnostic and raises `PressureFlowError` |
| `assign_sublimation_channels` | `channels.py:194-201` | `wound_vector`, `practice_stack.spiritual`, domain A/S/V, `buffer_type` | `domain.affect_channel` | One channel per domain; recomputed every cycle |
| `_seed_wound_scores` | `channels.py:103-150` | 7 wound scalars, `practice_stack.spiritual` | Local score dict only | Linear bands; several hard thresholds at 60/50/70/30 |
| `_seed_domain_scores` | `channels.py:153-187` | domain A/S/V, `buffer_type` | Local score dict only | Fixed domain-channel mapping |
| `_pick_channel` | `channels.py:190-191` | score dict | none | `max`; tie broken by fixed `SUBLIMATION_CHANNELS` order (earlier wins) |
| `compute_baseline_load` | `gating.py:122-149` | `strata_stack`, domain A/S/V, `buffer_type` | `domain.baseline_load`, `expression_rate` (preserved), `activation_threshold` (preserved) | Structural weights sum to 1 per domain; clamps 0–100; no event/access/meaning |
| `apply_expression_gating` | `gating.py:152-188` | `reproduction_constraints`, psych `vitality`, `registers.inner_load`, `baseline_load`, `expression_rate`, `activation_threshold` | `domain.expression_rate`, `domain.expressed_aim` | Hostage >70 ×0.3, >50 ×0.6; energy <30 ×0.5, <50 ×0.75; `expressed` only above threshold |
| `_derive_hostage_index` | `gating.py:61-71` | reproduction constraints | none | **Separate weights** from `derived.compute_hostage_index` |
| `_derive_current_charge` | `flow.py:268-284` | domain `baseline_load`, `registers.inner_load`, mean wound | none | `clamp` 0–100; no event input |
| `_prior_groove` | `flow.py:262-265` | `memory.grooves[domain][channel]` | none | Clamp 0–100 |
| `_channel_conductance` | `flow.py:366-403` | prior groove, psych vitality/agency/aperture, social support, network density/repression, spiritual/aesthetic state, relational-field status | none | Clamp 0.65–1.45; channel-specific terms |
| `_domain_charge_ledger` | `flow.py:406-465` | current charge, expressed aim, domain channel, conductance, vessel/insulation/memory | none (returns dict) | `overt = min(expressed_aim,current)`; `internal = current-overt`; `trace = internal × conductance` |
| `derive_vitality_profile` | `vitality.py:85-191` | vitality, age, insulation, ledger, memory | none (returns dict) | Age penalty `(age-30)*0.25`; fatigue/conductance/recovery/horizon readouts |
| `derive_insulation_profile` | `insulation.py:72-147` | buffer type, channel, insulation score, practices, collective, capacity, memory | none (returns labels) | Fixed buffer/channel→mode table; support thresholds |
| `_simulate_domain_routes_transactionally` | `flow.py:547-567` | state + ledger | none on live state; deep-copied working state | Applies route per domain, records numeric deltas |
| `_apply_single_domain_route` | `flow.py:500-544` | ledger item `trace_intensity`, `primary_channel` | capacity, psych capacity, practice, peak routing, style, wound, intensity/capture | Scalar additions/subtractions; categorical style change for conspiracy |
| `_commit_route_state` | `flow.py:570-573` | working state | seven route objects on live state | Deep copies committed objects; `clamp_all` |
| `_history_after_append` | `flow.py:651-659` | state history + snapshot | none | Cap 120 snapshots |
| `_update_memory` | `flow.py:678-750` | full history, previous memory | none (returns memory) | Recent window 5; groove decay 0.985, increment 0.035×trace; ±10 relation bands |
| `_compact_surface_profile` | `flow.py:576-617` | ledger, memory, vitality | none | Sanitized surface; no analyst/history |
| `_analyst_account` | `flow.py:620-648` | ledger, deltas | none | Analyst-only; voice export false |

### Read/write separation

**Read but not written by the cycle:** `domains.A/S/V/Aim`, `strata_stack`, `collection_infrastructure`, `frameworks`, `buffers`, `cracks`, `striving_objects`, `active_magnets`, `registers.inner_load` (read only), `reproduction_constraints` (read only).

**Written before route simulation (live, not rolled back on later failure):** `domain.affect_channel`, `domain.baseline_load`, `domain.expression_rate`, `domain.expressed_aim`.

**Written on the working copy, then committed transactionally:** `capacity`, `psychological_capacity`, `practice_stack`, `peak_routing`, `intensity_and_capture`, `style_traits`, `wound_vector`.

**Written after successful route work:** `pressure_flow_history`, `pressure_flow_memory`, `surface_psyche_profile`, `analyst_pressure_account`, `yearly_integrity`.

**Not written at all by this cycle:** `domains.A/S/V/Aim`, `frameworks`, `buffers`, `cracks`, `strata_stack`, `active_magnets`, `striving_objects`. Their changes come from other annual steps.

---

## 3. Actual equations and constants

### 3.1 Structural latent load (`compute_baseline_load`)

For each stratum and domain:

```text
stratum_pressure =
    coercion_strength × V_weight
  + contradiction_load × A_weight
  + visibility_of_complicity × 0.25
  + salience × 0.10
  + (100 − provision_strength) × 0.20
```

where `V_weight` is `target 1.0`, `proximate 0.8`, `identified 0.65`, else `0.35`; `A_weight` is `structural 1.0`, `partial 0.8`, `distorted 0.55`, else `0.35` (`gating.py:74-91`).

Domain load:

```text
baseline_load = Σ_level weight[domain, level] × stratum_pressure
              + buffer_type penalty (guilt/colonial_justification +6; not_my_concern/liberal_utopian_blur +3)
              clamped 0..100, rounded 1 decimal
```

Domain weights are hard-coded in `gating.py:10-58`; each row sums to 1.0 (tested by `test_baseline_load_weights_sum_to_one_and_cover_all_levels`). `baseline_load` is structural position + current A/V, not an event impression.

### 3.2 Expression gating (`apply_expression_gating`)

```text
hostage = 0.35·housing_insecurity + 0.25·(100−legal_status)
        + 0.60·dependents + 0.30·debt
        + 0.30·job_insecurity + 0.35·caregiving_load   [clamp 0..100]
energy  = 0.5·vitality + 0.5·(100−inner_load)
rate    = prior expression_rate
          × (0.3 if hostage>70 else 0.6 if hostage>50 else 1)
          × (0.5 if energy<30 else 0.75 if energy<50 else 1)
expressed_aim = load×rate/100 if that exceeds activation_threshold else 0
```

`expression_rate` is **stored and reused**; there is no reset/recovery in the pressure-flow module. Under constant high hostage, the reviewer probe observed `100 → 30 → 9 → 2.7` across three cycles (`probe_flow.json`). This is a ratchet, not a documented memory law.

**Duplicate hostage index:** `derived.compute_hostage_index` (`derived.py:45-58`) uses weights dependents .25, housing .20, legal insecurity .15, debt .15, job .15, caregiving .10. `gating._derive_hostage_index` uses .60/.35/.25/.30/.30/.35. For a moderate state the reviewer probe measured **17.0 vs 35.2**. The pressure-flow gate does **not** use `derived.hostage_index`. This is a source-level semantic conflict.

### 3.3 Current charge (`_derive_current_charge`)

```text
inner_load_factor = 0.90 + inner_load/500      # 0.90..1.10 for inner_load 0..100
wound_factor      = 0.92 + mean_wound/625      # 0.92..1.08 for mean_wound 0..100
current_charge    = clamp(baseline_load × inner_load_factor × wound_factor, 0..100)
```

Probe: baseline 80, inner_load 60, wound_mean 50 → **81.6** (expected 81.6). No event/access/relationship/meaning input.

### 3.4 Charge ledger and “conservation”

```text
overt_aim_charge        = min(clamp(expressed_aim), current_charge)
internally_routed_charge = max(0, current_charge − overt_aim_charge)
trace_intensity          = internally_routed_charge × channel_conductance
```

The only invariant is per-domain `overt + internal = current`. There is **no global conserved quantity**, no transfer between domains, no source/sink, and `trace_intensity` can exceed `internally_routed_charge` (probe: 71.6 × 1.062 = 76.039). The source itself says trace is “effect strength, not additional charge” (`flow.py:451-452`). Therefore “charge conservation” is computational bookkeeping, not established psychological theory.

### 3.5 Channel conductance (`_channel_conductance`)

```text
conductance = 1.0
            + min(0.35, prior_groove/250)
            + vitality/channel chronic bonuses
            + channel-specific support/network/repression/aperture/agency/spiritual terms
            + relational_field_bonus
clamped 0.65..1.45
```

Examples of hard-coded terms (`flow.py:383-401`): vitality ≤35 gives +0.18 for withdrawal/somatic and −0.16 for quiet/hyper; vitality ≥70 gives +0.08 for quiet/hyper/aesthetic; quiet organizing adds `min(0.18,(social_support+network)/800)` and subtracts `min(0.12,repression/700)`; piety +0.08 if spiritual ≥50; aesthetic +0.06 if aperture ≥60; micro-authoritarianism +0.08 if agency <40. Relational field adds a small bonus only if `strata_salience["relational_field"]["status"] == "ok"`; it is a projection/status, not a specific relationship.

### 3.6 Route effects (`_apply_single_domain_route`)

| Channel | Exact writes (all `+= routed × coefficient` unless noted) |
|---|---|
| `humor_irony` | `style_traits.absurdist_humor += 0.10r` |
| `hyper_competence` | `practice_stack.study += 0.05r`; `practice_stack.craft += 0.05r`; `intensity_and_capture.craft_talent += 0.02r` |
| `caretaking_warmth` | `practice_stack.care += 0.08r`; `practice_stack.spiritual += 0.01r` |
| `piety_ritual` | `practice_stack.spiritual += 0.08r`; `peak_routing.coherence += 0.02r` |
| `aesthetic_intensification` | `style_traits.aesthetic_sensitivity += 0.07r`; `practice_stack.craft += 0.03r` |
| `withdrawal_numbness` | `psychological_capacity.aperture -= 0.03r`; `practice_stack.risk_training -= 0.05r` |
| `micro_authoritarianism` | `style_traits.conscientiousness += 0.04r`; `peak_routing.coherence += 0.01r` |
| `conspiracy_symbolic` | `psychological_capacity.reality_anchor -= 0.03r`; **categorical** `peak_routing.theory_of_change_style = "witness_exposure"` |
| `quiet_organizing` | `practice_stack.organizing += 0.08r`; `peak_routing.coherence += 0.02r` |
| `somatic_irritability` | `capacity.health -= 0.02r`; `wound_vector.anger += 0.05r` |
| fallback | `practice_stack.craft += 0.02r` |

`r = trace_intensity`. All numeric targets are clamped after each domain route. `_simulate_domain_routes_transactionally` applies the five domain routes to one deep-copied state in `DOMAIN_NAMES` order; per-domain deltas are numeric snapshots. The categorical conspiracy effect is **not** in `_snapshot_numeric_state`/`trace_delta`; reviewer probe: theory changes `institution_building → witness_exposure`, `aggregate_contains_theory=false`.

### 3.7 Memory (`_update_memory`)

For each domain:
- lifetime/recent charge averages; lifetime/recent route totals by channel;
- `dominant_channel_by_domain` = channel with max cumulative trace; `recent_dominant...` over last 5 cycles;
- `historical_relation` = current charge vs prior-recent average: `≥ +10` rising, `≤ −10` falling, else continuous; no prior → first cycle;
- `grooves`: all prior grooves decay `×0.985`; current channel groove gains `trace_intensity × 0.035`; clamp 0–100.

Probe: prior groove 10, trace 50 → `10×0.985 + 50×0.035 = 11.6`. History cap 120; recent window 5. `pressure_flow_history` snapshots contain event **counts by type**, not event identity, actor access, or meaning (`flow.py:203-226`). Memory is aggregate trace statistics, not autobiographical or relationship memory.

### 3.8 Vitality, insulation, vessel and surface

- `derive_vitality_profile`: age phase (cutoffs 13/20/35/50/65), age penalty `max(0,(age−30)×0.25)`, fatigue `100−vitality + age penalty + 0.04·current + 0.03·internal − 0.08·insulation`; conductance multiplier, recovery cost and future horizon are **readouts** and are not consumed by `_channel_conductance` or routing.
- `derive_insulation_profile`: fixed buffer/channel → mode table; practice/collective thresholds; confidence labels. It is not an inhibitory gate in the pressure-flow route.
- `derive_attribution_and_vessel_hint`: fixed channel hint and confidence from charge/ practice/memory; surface only.
- `_compact_surface_profile` exports mediated labels; `_analyst_account` exports analyst domains with `voice_export_allowed=false`.

### 3.9 `_pick_channel`

`max(SUBLIMATION_CHANNELS, key=(score, −priority))` returns exactly one channel. Ties go to the earlier channel in the fixed tuple. Domain stores one `str`; no score vector, no secondary channel, no simultaneous channel set. Reviewer probe: tie `{humor_irony:10, hyper_competence:10, quiet_organizing:10}` → `humor_irony`. The score dict is not persisted.

---

## 4. Transaction and failure behavior

The route is applied to a `deepcopy` and committed only at the end (`flow.py:547-573,803-805`). This is real and tested:

- `test_transactional_failure_after_route_projection_does_not_mutate_live_state` patches `_update_memory` to raise after projection and verifies `style_traits.absurdist_humor` and history remain unchanged.
- **Gap:** that test calls `run_pressure_flow_cycle(..., assign_channels=False, compute_pressure=False, apply_gating=False)`. It does **not** cover the default pre-route mutations. Reviewer probe with defaults and forced `_update_memory` failure shows `affect_channel` and `baseline_load` change on the live state before the exception; `pressure_flow_history` remains empty. The transactional claim is therefore **partial**: route objects are atomic, but channel/pressure/gating writes are not.
- **Audit gap:** the conspiracy categorical `theory_of_change_style` change is committed but absent from numeric `trace_delta`/`per_domain_trace_delta`.

---

## 5. What the code actually does with history

| History form | Read by | Actual effect | Not present |
|---|---|---|---|
| `pressure_flow_history` | `_update_memory`, surface historical relation | Charge averages, dominant/recent channel labels, ±10 relation label | Event identity, access, relationship, meaning, recall |
| `pressure_flow_memory.grooves` | `_prior_groove` → `_channel_conductance` | Numeric conductance increase | Channel selection, relation scope, conditional access |
| dominant/recent channel | surface/vessel/insulation confidence | Descriptive labels/confidence | Recruitment/selection |
| vitality profile | memory/surface | Descriptive readouts | Route/gating |
| wound/practice changes from route | next `assign_sublimation_channels` / charge | Indirect value-mediated feedback | Learned relation/edge |

**Critical negative result:** setting 100-point grooves does not change `_pick_channel`; reviewer probe selects the same five channels with and without grooves. The groove biases how strongly the already-selected channel etches trace, not which channel is recruited.

---

## 6. Cross-component effects: value modification versus changed causal relation

Real cross-component writes exist:

- `somatic_irritability` route increases `wound_vector.anger`, which next cycle raises `wound_mean`/`inner_load` and therefore current charge; it also lowers `capacity.health`.
- `withdrawal_numbness` lowers `psychological_capacity.aperture`, changing aesthetic conductance next cycle.
- `caretaking_warmth` raises `practice_stack.spiritual` and `care`, potentially changing later channel scores/insulation labels.
- `quiet_organizing` raises `practice_stack.organizing`, changing alignment/mis-aim/insulation labels.
- `conspiracy_symbolic` changes `reality_anchor` and categorically sets `peak_routing.theory_of_change_style`, which is read by liberatory-orientation/eligible gates and signal effects.
- `frameworks` (separate step) switch acute/chronic operator by tenure/half-life and active/dormant by weight threshold; `topology` (separate step) switches loop topology by fixed hysteresis.

None of these creates a new **edge**, changes a rule condition, or learns a relation. They are scalar/categorical state writes in fixed formulas. The source has **no** operator that changes the function mapping of another component based on history. Therefore:

- **Component-value modification:** real and pervasive.
- **Changed causal relation / rewiring:** not implemented in this family. Claims of “the bike wheel rewires relations” are not supported by this source; only value-mediated feedback and fixed categorical switches exist.

---

## 7. Tests actually executed and coverage

**Command:** `PYTHONPATH=<yaml-shim> PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider <17 test files>`
**Result:** **82 passed**, 0 failed, 0 errors (`logs/pytest_x02_original_v3.log`).

| Group | Tests |
|---|---|
| `test_v5_pressure_flow.py` | 23 |
| `test_v5_pressureflow_golden_run.py` | 1 |
| `test_v5_pressureflow_mediates_relation_state_without_surface_leak.py` | 1 |
| `test_v5_surface_psyche_profile.py` | 5 |
| `test_v5_sublimation_channels.py` | 3 |
| `test_v5_baseline_load.py` | 8 |
| `test_phase3_activation_gate.py` | 5 |
| `test_v5_vitality_fatigue.py` | 3 |
| `test_v5_insulation_registry.py` | 4 |
| `test_v5_vessel_hints.py` | 4 |
| `test_step_logic.py` | 12 |
| `test_v5_render_surface_psyche.py` | 3 |
| `test_v5_persona_sheet_surface_psyche.py` | 2 |
| `test_v5_v2_chat_prompt_no_raw_v5_leaks.py` | 1 |
| `test_v5_structural_diagnostics.py` | 1 |
| `test_architecture_invariants.py` + `test_invariants.py` | 6 |

**What the tests establish:** formula/decomposition, per-channel trace paths, groove→conductance, transaction on the route-only path, source failure diagnostics, surface/analyst separation, roundtrip, historical relation labels, vitality/fatigue readouts, insulation/vessel labels, step order. **What they do not establish:** event-specific impression, multi-stream recruitment, relation scope/access, durable CAN011 state, current Sorok integration, or native science. `_pick_channel` tie/secondary behavior and the duplicate hostage index have no direct test; the expression-rate ratchet and pre-route transaction gap are not covered.

**NOT_RUN:** the exact full TD-R05 80-test suite as a single run; server/model/provider integration; live persona conversation; current Sorok S44/S49/S52 consumer; original respondent/survey data; native actor/person tests.

---

## 8. Coverage grades

| Scope | Grade | Meaning |
|---|---|---|
| Stored/derived separation, route transaction, per-domain trace/audit, surface/analyst split | `MEANINGFUL_COVERAGE` | Real code, executed tests; reusable with owner mapping |
| Structural `baseline_load` + A/V weights | `PARTIAL_WRONG_MEANING` | Real computation, but structural position is not an event-specific psychological impression |
| Charge/conductance/groove/history | `PARTIAL_WRONG_MEANING` | Real bookkeeping; “conservation” and “memory” are overinterpretations; history is mostly numeric |
| Single-channel sublimation routing | `PARTIAL_WRONG_MEANING` | Real route paths; winner-take-all and fixed taxonomy discard simultaneous/contradictory recruitment |
| Buffers/insulation as regulation | `INFRASTRUCTURE_ONLY` | Dataclass/update/cost and labels; buffer strength not in pressure-flow route; no standard seeding |
| Vitality/fatigue/horizon | `INFRASTRUCTURE_ONLY` / `PARTIAL` | Raw vitality affects conductance/gating; fatigue/recovery/horizon/conductance multiplier are readouts only |
| Autonomy/safety conditions | `PARTIAL_WRONG_MEANING` | Drives/conditions/gaps exist; universal constants and SES seed; no actual caregiver/safety relation |
| Stability inertia | `PARTIAL_WRONG_MEANING` | Real spike/drain; year/process-based; no relation scope; not in pressure-flow core |
| Event-conditioned interpressure, relational scope, durable rewiring | `MISSING` | No source operator in this family |

---

## 9. Scientific questions — direct answers

1. **Is charge conservation psychological theory or bookkeeping?**
   **Bookkeeping.** The only invariant is per-domain `expressed + internal = current`, with no global conservation, no transfer law, and a non-conserved `trace_intensity`. The word “charge” is a metaphor; no empirical conservation is established.

2. **Which simultaneous pressures can remain effective, and where does a primary-channel selector discard possibilities?**
   Up to five domain-level loads can remain effective simultaneously, and `expressed_aim` can coexist with one internal route per domain. Within each domain, `_pick_channel` selects exactly one of ten channels and discards the others from routing; the other scalar wound/domain contributions remain as state but have no simultaneous route. There is no multi-channel vector. The selector discards all non-winning channels and tie-breaks by fixed order.

3. **Can one component alter the functioning of another, rather than just changing a scalar contribution?**
   It can alter another component's **inputs** or a fixed categorical switch: wound→charge, aperture→aesthetic conductance, spiritual→piety score, organizing→alignment/mis-aim, conspiracy→theory-of-change/eligibility, framework tenure→acute/chronic operator, topology hysteresis→loop label. It does **not** change a rule condition, relation, access, or edge dynamically. So: value-mediated and fixed-switch effects yes; genuine relation rewiring no.

4. **Does history change susceptibility, relation scope, conditional accessibility or simply a numerical weight?**
   In this family, history changes **numerical conductance/effect strength** and descriptive labels; it does not change relation scope or conditional accessibility. Grooves do not affect channel selection. Route-induced wound/practice changes can indirectly alter future scores, but only as scalar inputs. There is no scoped expectation/relationship memory.

5. **Can actual contradictory orientations persist and be differently recruited by circumstances?**
   Contradictory wound/domain values can persist, and the single channel can change when the global wound/domain state changes. But there is no context/event-specific recruitment, no simultaneous contradictory channel set, and no access/relationship scope. The required sense is not implemented.

6. **Which old functions can be retained, reworked, or replaced?**
   Retain: stored/derived separation, transactional working-copy/commit for route effects, per-domain trace/audit, surface/analyst separation, history cap, candidate hysteresis/operator mechanisms. Rework: charge inputs/meaning, gating, channel selection, memory, vitality/insulation, buffers. Replace: demographic wound seeding, fixed channel priority/taxonomy, fixed coefficients/decays, duplicate hostage definition, expression-rate ratchet, “conservation” claim. Create: event impression/uptake, multi-stream recruitment, relation scope/access, durable CAN011 transition, intervening-time, fallible memory/meaning, explicit NO_CHANGE.

---

## 10. Causal alternatives and limits

- **Alternative A — structural projection:** the pressure-flow values describe current structural position + chronic wound, not an event-appraisal. The evidence: `baseline_load` uses strata/A/V; event context is counts only; no event semantics enter charge.
- **Alternative B — hydraulic metaphor:** “pressure/charge/conductance/groove” are computational metaphors for repression/sublimation; the code does not measure a conserved psychological substance. The evidence: per-domain arithmetic, no global conservation, non-conserved trace.
- **Alternative C — statistical smoothing:** grooves are a simple exponential moving average/conductance bias, not memory/meaning. The evidence: 0.985 decay, 0.035 increment, no event/access.
- **Alternative D — cost accounting:** buffers are resource costs and insulation is a top-3 buffer/money index, not regulatory activity; buffer strength does not inhibit the route. The evidence: `update_buffers` costs capacity; `compute_insulation_score`; no buffer term in `_channel_conductance`.

The source cannot adjudicate which alternative is psychologically true. It can establish which operations exist.

---

## 11. Exact provenance / constants

Hard-coded or config-derived values include:
- stratum weights (gating.py:10-58), viscerality/awareness weights (74-91), buffer penalties +6/+3 (142-145);
- charge factors 0.90/500 and 0.92/625 (flow.py:282-283);
- conductance base 1.0, groove/250 cap .35, clamp .65–1.45, channel bonuses (flow.py:372-403);
- route coefficients (flow.py:506-537);
- history cap 120, recent window 5, relation ±10 (flow.py:39-40,669-675);
- groove decay .985, increment .035 (flow.py:726-731);
- age cutoffs 13/20/35/50/65, age penalty .25, fatigue/recovery coefficients (vitality.py:30-181);
- duplicate hostage weights (gating.py:65-70 vs derived.py:35-42);
- expression-rate multipliers .3/.6/.5/.75 (gating.py:172-181);
- autonomy drive constants 65/68 and SES condition lookup (identity_to_backbone.py:339-368);
- stability drain caps 12/3, holding .6, sealed .15 (stability_inertia.py:11-14).

**None of these has an issued scientific authority in this review. They are legacy implementation policy, not Neo-V3 law.** The only v3config values are caps; the core coefficients are hard-coded.

---

## 12. Current consumer / nonintegration

- Historical consumer: `v3/run_and_print.py` calls `run_one_year` (which calls `run_pressure_flow_cycle`) and optionally `run_llm_band_year`; `build_persona_sheet` exposes a sanitized `surface_psyche` (`persona_sheet.py:962-964`); `build_render_packet` passes surface to Pass 2 (`run_llm_band.py:367-380`); tests confirm analyst/history are kept out of voice surfaces.
- Current Sorok S44/S49/S52 consumer: **not traced**. The S52 work is a separate test-only closure; no current import of this V3 flow. The actual S50 root is `SOURCE_OWNER_HOLD` (from prior independent review). This atlas is historical source, not current-person integration.

**Do not call old V3 current integrated.** The source evidence is historical.

---

## 13. Minimum falsifiable downstream dependency

A lawful next sourcefree dependency test should be:

> Given the same actor and later probe, an admitted event with actual actor access and a specific expectation/relation/support change must change a typed recruited response or durable transition; the same event without access, or with support withdrawn, must produce explicit NO_CHANGE; a label/ID-only change with the same event semantics must not change the result; and a later event must read the changed state.

This is **not** implemented by pressure-flow. Its current code would fail the label-only test for routing (event semantics not read) but pass a narrow material/charge test; therefore it is not sufficient. The proposed downstream dependency must be built on a CAN008 concrete rule and a CAN011 target rule, not on the legacy channel selector.

---

## 14. Retain / adapt / replace / create summary

| Disposition | Items |
|---|---|
| **RETAIN** | `BackboneState` stored/derived separation; `_simulate_domain_routes_transactionally` + `_commit_route_state`; per-domain numeric trace/audit; `_compact_surface_profile`/`_analyst_account` separation; `pressure_flow_history` cap; `update_loop_topology` hysteresis as candidate; framework acute/chronic/dormant operator as candidate; `stability_inertia` as candidate |
| **ADAPT** | `_derive_current_charge` to accept exact event/impression/relation inputs, not only baseline/wound; `_channel_conductance` to use event/relationship/access rather than fixed coefficients; `compute_baseline_load` re-key to exact V555/V556 structural identities; `_update_memory` to scoped event/relation memory; `apply_expression_gating` to one canonical constraint index and no ratchet; vitality/insulation/buffers to causal only if owner-issued; `run_pressure_flow_cycle` to event/interval scope |
| **REPLACE** | `_pick_channel` winner-take-all with a multi-stream recruitment operator; fixed channel taxonomy/priority; demographic wound seeding; duplicate hostage index; expression-rate ratchet; fixed legacy coefficients/decays; “conserved charge” claim; `route_unexpressed_load` duplicate legacy path |
| **CREATE** | Event→impression/uptake rule (CAN008 R2 concrete); situated multi-stream recruitment and conflict/regulation; relationship/scope/access state; durable CAN011 transition adapter; intervening-time computation; fallible autobiographical memory/meaning; explicit valid `NO_CHANGE` and support-withdrawn/irrelevant controls |

**Authority:** retain/adapt/replace is a research disposition, not adoption. Concrete CAN008/CAN011 rules and any native/source permission remain with the competent owners. No new coefficient is proposed as scientific law.

---

## 15. Reviewer-visible source/evidence files

- `source_identity.json` — file hashes, line counts, S50 manifest, zip caveat.
- `logs/pytest_x02_original_v3.log` — 82 passed.
- `evidence/probe_flow.json` — formula, channel, groove, memory, hostage-duplicate, ratchet, transaction, buffer, event-semantic and categorical-audit probes.
- `evidence/probe_flow.py` — exact probe source.
- `SOURCE_INDEX.json` — index of evidence.
- `EXECUTION_LEDGER.json` — commands/exit/results.
- `NEO_V3_INTERPRESSURE_REQUIREMENTS.md` — typed target differential and falsifiers.
- Per-card dossiers: `V3_EXISTING/M03/X02_M03_DOSSIER.md` … `M24`.
- `00_RETURN.md` — courts, findings, actions, owners, HOLDs, remote SHA.
