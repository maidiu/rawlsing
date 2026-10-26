# SOROK V3 COURTS X01 — ORIGINAL V3 EXPECTATION / CHILD-MODEL SOURCE FORENSICS

**Terminal:** `X01_ORIGINAL_V3_SOURCE_VERIFIED__M01_INFRASTRUCTURE_ONLY__M15_PARTIAL_WRONG_MEANING__M17_PARTIAL_WRONG_MEANING_SINGLE_VALENCE__M22_PARTIAL_WRONG_MEANING__M36_CONFLICTING_UNKNOWN_TO_HOPEFUL__NO_NATIVE_GRANT__NO_SELF_ADOPTION`

**Court return:** `X01_DOCUMENTARY_SOURCE_AND_SOURCEFREE_PROBE_RETURN__ENGINEERING_PASS_WITH_REDS__SCIENCE_HOLD_RULE_UNISSUED__AUTHORITY_NO_NATIVE_GRANT`

## 1. Scope, source and authority

- Assigned branch: `agent/v3court-x01-expectations-child-model-r1`.
- Exact sealed startup: `2647a4cf25d8bb33a00471e1af9c5e58c2825efb`.
- No duplicate X01 worktree existed at preflight; the worktree is isolated at `<X01_WORKTREE>`.
- Source root: `<USER_HOME>/Desktop/Rawlsing/Rawlsing_code_bundle_staging`; V3 is the `v3/` subtree. The user confirmed this location. The parent is the whole old Rawlsing; V3 imports/callers in `v2/` and `server/` were read only where the assigned mechanisms actually flow through them.
- Source access was read-only. No source edit, production edit, canonical atlas edit, native rule, actor/source permission, Pyat/C8/C9/C11/C12 grant or provider/model call was made.
- **Source-identity grade:** the 31-file S50 identity manifest is exact **31/31**. Additional required files were hashed and matched to independent authority records where available:
  - `v3/io/parent_baseline_from_behavior.py` `4e5be6448a5b76c413492ec2a83b62d9e9a2247ce131a094727d974a17cf750b` — matches `ADP_007_V3_ACTOR_INITIALIZATION/AUTHORITY.json`.
  - `v3/engine/effects/delta_templates.py` `7d99ddf26fd45b52e5e3c10074066ba5e06d17cdaf1fabad06298af3770815f0` — matches `CAN_012_V3_RUPTURE_METABOLIZATION/AUTHORITY`.
  - `v3/io/identity_to_backbone.py` `cb29c9595ac495c3b69b693d4c58a278e9ef1f63a7a8917d8e407920fbd3bdda` — matches ADP_007/CAN_011/CAN_009 authority records.
  - `v3/engine/prompts.py` `4702de20590579c3c4543dfa5139aa4a3ce6df47ed1aee2c92c800d5a3038d57` — matches CAN_017 authority.
  - `v3/engine/expectation_events.py` `307ae929a43935170a2f792b4a702a02ac54819a4fa897aa3fef4a099a96cb49` — matches the top-level `Rawlsing_code_bundle_staging/v3/...` staging-zip entry; no separate frozen authority hash was located.
  - `v3/need_axis_rules.yaml` `e18cb396…`, `v3/proxy_striving_map.yaml` `a9f4e9bd…`, `v3/expectation_event_templates.yaml` `4fead214…`, `v3/engine/effects/rupture_templates.yaml` `8c182165…`, `v3/v3config.yaml` `5efc71e3…` — hashed local inputs.
- **Important provenance caveat:** the local `Rawlsing_code_bundle_staging.zip` hashes to `3f2c5ed9…`, **not** the TD-R05 archive `953c9149…`. The local zip is a re-zipped staging container, so its archive-level hash is **not** used as proof. The 31 S50 file hashes and the independent authority-file hashes are the source evidence. The file-level work is source-verified; the archive-level identity is not claimed.

## 2. What was read and executed

**Read (line-level):** `v3/core/state.py`, `v3/core/year_record.py`, `v3/core/generation_integrity.py`, `v3/engine/expectation_baseline.py`, `v3/io/parent_baseline_from_behavior.py`, `v3/engine/expectation_events.py`, `v3/engine/effects/delta_templates.py`, `v3/io/identity_to_backbone.py`, `v3/engine/prompts.py`, `v3/engine/llm_contract.py`, `v3/engine/scoring.py`, `v3/engine/striving_objects.py`, `v3/engine/run_llm_band.py`, `v3/engine/yearly_step.py`, `v3/v3_yearly_step_order.yaml`, `v3/io/json_codec.py`, `v3/io/persona_sheet.py`, `v2/run_full_simulation_with_llm_log.py`, `server/generation/simulation.py`, the V3 tests named below, `need_axis_rules.yaml`, `proxy_striving_map.yaml`, `expectation_event_templates.yaml`, `v3/v3config.yaml`.

**Executed (sourcefree read-only):**

| Evidence | Result |
|---|---|
| `v3/tests/test_connector_and_field_injection.py` | **11 passed** |
| `v3/tests/test_wave4.py` | **14 passed** |
| `v3/tests/test_llm_contract.py` | **18 passed** |
| `v3/tests/test_v5_baseline_load.py` | **8 passed** |
| Full `v3/tests` with a faithful YAML bridge | **150 passed, 1 failed** |
| The one full-suite failure | `test_persona_sheet_integrity::...` expects country `"MDV"` to canonicalize to `"Maldives"`; got `"MDV"`. This is a data/environment canonicalization dependency outside M15/M17/M22/M36. |
| Simpler YAML bridge | 149 passed, 2 failed; the extra failure is `test_metabolization_effects::test_get_template_for_age`, caused by Ruby-JSON stringifying numeric YAML keys (bridge artifact), not original V3 semantics. The faithful bridge converts numeric keys and removes that failure. |
| `probe_v3_x01.py` | Direct function/state probe for missing parent, loving low-material, cold high-material, environment, shards, baseline mutation, alienation delta, axis rules. Output in `TEST_SOURCE_AND_LOGS/probe_v3_x01_output.json`. |
| `probe_v3_x01_one_parent.py` | One-present-parent dilution probe. Output `probe_v3_x01_one_parent.json`. |
| `probe_v3_x01_backbone.py` | `backbone_state_from_identity` integration/provenance probe. Output `probe_v3_x01_backbone.json`. |

No real LLM call, no survey/raw data, no V2 conversation run, no current S44/S49/C9/C12 consumption test, no native person. The tests establish historical source behavior at the tested grain, not current product integration.

## 2a. TD-R05 reconciliation

TD-R05’s original-source rows (at `25830fe7…`/blob `dfcc7e4f…`) are confirmed as documentary dispositions, not as current integration proof:

| M | TD-R05 disposition | X01 source finding |
|---|---|---|
| M01 | ADAPT_TO_TERMINAL_ARCHITECTURE | Confirm state container; X01 adds `INFRASTRUCTURE_ONLY` for baseline/child-model/shards and identifies missing parentage/provenance. |
| M15 | ADAPT_TO_TERMINAL_ARCHITECTURE | Confirm typed axes/baseline; X01 finds dead per-axis YAML rules, 50/hopeful, one-parent dilution, static baseline and no love/availability schema. |
| M17 | ADAPT_TO_TERMINAL_ARCHITECTURE | Confirm shard creation; X01 finds one-valence LLM-label classification, no mixed record, duplicate legacy creation and lost alienation delta. |
| M22 | ADAPT_TO_TERMINAL_ARCHITECTURE | Confirm child-model carrier; X01 finds hardcoded category→text, unused `age`, safe-home default and positive-rule suppression. |
| M36 | REMOVE_AS_OBSOLETE_OR_REDUNDANT | Confirm; the 50→hopeful/safe-home conversion is `CONFLICTING` with required unknown handling. |

The TD-R05 counts (3 REUSE / 31 ADAPT / 3 REPLACE / 3 REMOVE) are historical architecture dispositions, not execution or current-person proof. X01’s refinements are source-level and do not modify the TD-R05 record.

## 3. M01 — persistent BackboneState

**As built:** `BackboneState` (`state.py:500–614`) persists `expectation_baseline`, `striving_objects`, `gift_shards`, `disruption_shards`, `child_model`, `initial_state_provenance`, `yearly_integrity` and pressure-flow fields. `json_codec.state_to_json/state_from_json` round-trips them. `year_record.hash_jsonable` hashes records. `GenerationIntegrityAccumulator` records failures/fallbacks.

**Actual behavior:** the container and JSON persistence are real. But the stored psychological fields have **no canonical event parentage, rule identity, scope, uncertainty, actor-access or derivation history**:
- `initial_state_provenance.fields` records identity/capacity/reproduction/practice fields, not `expectation_baseline` or `child_model`; the backbone probe returned `null` for both provenance entries.
- `GiftShard`/`DisruptionShard` have no selected-event id/hash, source/access actor or causal parents; ids are list-position strings (`gs_{year}_{age}_{len}`, `ds_...`).
- No V3 event ledger owns the baseline/child-model/shards; `yearly_integrity` records stage diagnostics/event sampling, not these states.

**Coverage:** `INFRASTRUCTURE_ONLY` for the assigned psychological fields. **Retain** the typed checkpoint/JSON roundtrip and stored/derived direction; **adapt** into event-parented, time-indexed, scoped records; **create** the missing causal provenance/access/uncertainty. Owner: V3 actor developmental causality engine (CAN011/ADP016 jurisdiction), not X01.

**Adjacent contamination (outside the five mechanisms):** `identity_to_backbone` also seeds capacity, reproduction constraints, impunity, autonomy/safety conditions, practice stack, wound vector, frameworks, cracks, family/body domains and parent magnets from class, urbanicity, minority status, age, religiosity and universal constants (e.g. autonomy drive 65/safety drive 68; parent magnets mother 60/father 55). These seeds are not part of M15/M36, but they mean the initial state is not a clean care-history carrier. Any reuse must strip or re-own them under competent rules; otherwise a “baseline” result is contaminated by demographic/structural defaults.

## 4. M15 — need axes / expectation baseline

**Exact as-built:**
- Ten need axes and four categories exist (`state.py:305–309`).
- `infer_parent_baseline_and_regime` (`parent_baseline_from_behavior.py:25–86`) reads per-parent `parental_warmth`, `parental_authority`, `parental_material_support`; defaults every missing field to **50** (`_float` 18–22); averages father/mother 50/50 (51–53; the YAML's declared `seed_weights` are not used); sets all axes `hopeful` (56–58); applies crude thresholds (59–67) and builds a regime (69–85).
- `derive_child_expectation_baseline` (`expectation_baseline.py:107–143`) maps parent categories to scores `[-2..2]`, applies **only** the YAML `global_modifiers` (`_apply_global_modifiers` 68–104), and maps back to categories. Missing parent category defaults to `"hopeful"` (133). `axis_rules`, `flags`, `conditional_modifiers`, `base_by_meaning_frame`, `meta.thresholds` and `seed_weights` are **not consumed** by this function. Environment keys (`economic_precarity`, `external_threat`, `institutional_reliability`, `status_competition`, `collective_solidarity`) have **no effect**: the probe returned identical results with and without high precarity, and identical results for actual rules vs empty rules.
- `striving_update` (`striving_objects.py:256–257`) sets every missing axis to `"hopeful"` **every year**; no function updates existing categories from experience.

**Actual probe values:**
- **Missing parent `{}`** → inferred baseline all `hopeful`; regime warmth 50/coercion 50/openness 50/anxiety 50/shame 50/modeling 60; derived all `hopeful`.
- **Both parents high warmth/low material (85/45/20)** → inferred `status=competence=hopeless`, other axes `hopeful`; after the global warm+consistent +1 modifier, most relational axes become `entitled`, `status/competence=forbidden`. This is the only path that produces a coarse cross-axis split; it does not read material/environment into the derivation beyond the initial status/competence thresholds.
- **One present loving low-material parent (85/45/20), other missing** → averages `warmth=67.5, authority=47.5, material=35.0`; **all axes `hopeful`; default safe-home child model** — identical observable result to both parents missing. This is threshold-sensitive: a lower material value could cross the status/competence threshold, so the failure is not “every one-parent case is erased”; the 50 default dilutes the actual warm parent, and there is no love/availability schema even when a threshold is crossed.
- **Cold high material (30/80/80)** → attachment `hopeful` at exactly 30, belonging/safety/autonomy `forbidden`, status/competence `hopeful`; child model narrow.

**First real consumers:** `striving_update` (proxy `StrivingObject` spawning/multipliers), `llm_contract.state_summary_from_backbone` (Pass 1 prompt), `persona_sheet` (V2 surface). No V3 pressure-flow/derived/event-admission consumer was located.

**Coverage:** `PARTIAL_WRONG_MEANING`. Retain the typed axis/category carrier; adapt the derivation to actual care history/material conditions with scope/evidence/uncertainty; remove 50/hopeful, one-parent dilution, dead per-axis rules, global all-axis warm bump and static setdefault. The required love+insufficiency semantics are missing. No issued scientific rule exists for the thresholds or the mapping.

## 5. M17 — GiftShard/DisruptionShard and expectation events

**Exact as-built:** `expectation_events.apply_gift_disruption_shards_from_events` (`expectation_events.py:103–164`) creates a `GiftShard` for `expectation_type=fulfillment` or a `DisruptionShard` for `violation` when the event has an active `striving_object_id`. The event/LLM supplies the type and free-text label. Fulfillment always gets positive/medium/low; violation gets negative/`high` prediction error and `high` opacity when `identity_load>=60` (`malheur_risk`), else medium/medium. There is no mixed type, no baseline read, no material/care/availability read, no event id/parentage, and no later V3 state consumer.

**Actual probe:** the same label “Parent works late but calls to say she loves me” with `expectation_type=fulfillment` creates one GiftShard; with `violation` creates one DisruptionShard (malheur risk at identity_load 65). It cannot create both. The baseline remains unchanged in both cases.

**Downstream:** `delta_from_event` adds coherence/social-support for fulfillment and coherence/alienation for violation (`delta_templates.py:101–108`). The alienation delta is then lost: `apply_deltas_to_state` assigns `v.structural = v.affective = v.institutional = new_agg` (314–319), but `AlienationVector` has fields `distant_others/near_others/self/moral_totality`; the real vector is unchanged and `clamp_all` resets the scalar. Probe: `alienation_delta=3.0` → after scalar 50, vector 50, dynamic attrs 53. The legacy V2 runner also calls the shard function a second time after `apply_deltas_to_state` already did (`v2/run_full_simulation_with_llm_log.py:699–700,934–935`), producing duplicate shards. The newer `run_llm_band.py` does not double-call.

**First real consumer:** `persona_sheet` recent gifts/disruptions/backstory (`persona_sheet.py:452–467,938–948`) and JSON persistence. The Pass 1 state summary, `scoring`, `derived.py` and `psyche/flow.py` do not read shards. This is a V2 narrative surface, not a V3 causal consumer.

**Coverage:** `PARTIAL_WRONG_MEANING`. Retain a typed event-effect record; adapt to actor-relative, mixed, event-parented records with source/access/provenance; create mixed impression, baseline/striving linkage, later semantic consumer and explicit NO_CHANGE. Remove one-valence pre-classification, LLM-label authority, 60 threshold-as-science, duplicate creation and the alienation-vector defect.

## 6. M22 — child model / assumed rules / taboos / possible-world boundary

**Exact as-built:** `child_model_from_parent_baseline_and_regime` (`identity_to_backbone.py:60–109`) maps each `forbidden`/`hopeless` axis to one hardcoded rule and up to two taboos; if no such axis exists it inserts `"Adults are mostly fair"`, `"Friends don't betray you in public"`, `"Home is safe"`; default taboos `"sex","police","money shame"`; `what_counts_as_possible` from openness/coercion thresholds. `age` is accepted but unused. The model is static; no later update/revision/provenance.

**Actual probe:**
- Missing parent → safe-home defaults, medium possibility.
- Forbidden attachment + hopeless safety → “Adults can leave…”, “Institutions can hurt you…”, abandonment/police taboos, wide possibility.
- Both parents high warmth/low material → only status/competence prohibitions; **the safe-home/fair-adult rules are absent**; no positive parental-love/availability rule.
- One present loving low-material parent (85/45/20) + missing other → all-hopeful baseline and **safe-home defaults**, identical to missing parent in this probe; threshold-sensitive, but no love/availability schema.

**First consumers:** `llm_contract.state_summary_from_backbone` (`llm_contract.py:710–717`) → Pass 1 prompt (`prompts.py:28`); `scoring.score_event_candidate` rupture-assumption fit (`scoring.py:148–160`). `persona_sheet` does not include child_model. This is a prompt/scoring scaffold, not a V3 causal state.

**Coverage:** `PARTIAL_WRONG_MEANING`. Retain a child-model carrier; adapt to actual care/household history and procedural/bodily/unspoken versus verbal layers; create scope/confidence/provenance, age-sensitive development, contradiction and later ideological mediation. Remove hardcoded cultural taboos/default safe home, category→text determinism and any assumption that forbidden axes erase positive relational rules.

## 7. M36 — missing-parent → 50/hopeful/safe-home

**Exact pathway:** (1) `_float` default 50; (2) `infer_parent_baseline_and_regime` missing parent = 50 and all axes `hopeful`; (3) `derive_child_expectation_baseline` missing category = `hopeful`; (4) `update_striving_step` setdefault `hopeful`; (5) `child_model` default safe-home rules; (6) `llm_contract` duplicate safe-home fallback; (7) `server/generation/simulation.py:369` exact 50 default; (8) `v2/spec.py` no-WVS normal(50, variance). The archive-level V2 sampler can produce random near-50 values, but the server path has exact 50 and the V3 inference path has exact 50.

**One-parent dilution:** the present parent’s 85 warmth is averaged with the absent parent’s 50 to 67.5, below the 70 global-warm threshold; 20 material is averaged to 35, not below the `<35` threshold. All axes become `hopeful` and the safe-home child model appears. The missing parent is therefore not neutral; it is a positive-normalizing input.

**Coverage:** `CONFLICTING` for the old behavior; required operation `MISSING`. Remove the unknown→50→hopeful/safe-home conversion. Unknown must remain unknown/typed missing; any explicit prior must be separately issued with provenance.

## 8. The user’s case: palpably loving parent, work/material insufficiency

**Answer:** the old machine can produce **one coarse cross-axis split only in a narrow both-present, threshold-crossed case**, and it does not represent the relational phenomenon itself:
- Both parents present, high warmth/low material → derived baseline `attachment/autonomy/belonging/safety/meaning/justice/beauty/play/eros=entitled`, `status/competence=forbidden`; child model says only “Status is for others”/“You’re not allowed to be good at this” and omits safe-home/fair-adult/love rules.
- One present loving low-material parent (85/45/20) → **all-hopeful** baseline and **safe-home** child model, identical to missing parent in this probe; the actual love and insufficiency are both erased in this threshold case, and no configuration represents the love/availability relation itself.
- Event level → one `expectation_type` yields either GiftShard or DisruptionShard; the same “works late but calls to say she loves me” event cannot be both. The code forces one interpretation; the label is LLM-supplied.
- There is no confidence/uncertainty, no evidence count, no scope, no reliability, no routine, no repair, no contradiction set, and no separate love-versus-world availability schema. The four categories are ordinal labels, not confidence.
- The global warm modifier can raise most axes from `hopeful` to `entitled` and the material thresholds can lower `status/competence` from `hopeless` to `forbidden`; the global modifier itself shifts `hopeless`→`forbidden` and `hopeful`→`entitled` without new material evidence. This is a coarse threshold product, not a representation of “my parent loves me but the world does not provide.”

**Therefore:** the old V3 **does not** satisfy the theoretical target. It has a partial, fragile cross-axis effect in one configuration; it fails the single-parent/missing-parent configuration and the mixed-event configuration. This is a `PARTIAL_WRONG_MEANING`/`CONFLICTING` result, not a scientific positive.

## 9. Challenge / complication / threat, stable repair, NO_CHANGE, falsifier

**Challenge** (supported difficulty congruent with expectation; e.g., demanding practice with available help) has no distinct type. It can appear as `opportunity`/`practice` or a fulfillment expectation event; `delta_from_event` maps it to skill/practice/coherence gains, not a challenge-specific operator. **Complication** (conflicting care/insufficiency, love plus material limit) is forced into one fulfillment/violation shard. **Threat** (danger to a valued need/object) can appear as a violation shard with `malheur_risk` if identity_load≥60, or as a trauma-kind event with `stability_delta`; there is no objective-versus-subjective threat separation and no challenge/complication/threat taxonomy. **Stable history/repair**: repeated relationship/care events can reduce `wound_vector.abandonment/fear` through `delta_from_event` (143–154) within caps, but the expectation baseline, child model and shards are not revised; there is no routine-thickening or repair rule. **NO_CHANGE**: an event with no `expectation_type`/active striving is skipped; no explicit typed NO_CHANGE record exists, and `striving_update` still setdefaults missing axes. **Falsifier**: hold actor/world/later event fixed; compare (A) reliable loving care + material insufficiency, (B) insufficiency without warmth, (C) warmth without insufficiency, (D) no received event, (E) verbal-only exposure, (F) source hash changed without semantic change. A correct representation must preserve love confidence in A while marking worldly insufficiency, must not collapse A to B or to missing parent, must not turn C into insufficiency, must leave D/F unchanged, and must preserve mixed positive/negative components in A. The old code fails A vs missing-parent equality and A vs one-valence shard. This is a conceptual falsifier, not an implementation instruction.

## 10. Engineering, science and authority courts

**ENGINEERING — PASS at documentary/sourcefree grain, with REDs.** Exact source identities, line-level call/value maps, actual historical tests, direct probes, cold JSON/state behavior. REDs: dead per-axis YAML rules; 50/hopeful/one-parent dilution; static baseline; one-valence shards; duplicate shard creation in the legacy runner; alienation-vector delta loss; missing baseline/child-model provenance; tests that assert presence rather than the core semantics. No current C9/C12 integration.

**SCIENCE — HOLD / `RULE_UNISSUED`.** The old thresholds, 50 defaults, proxy-striving multipliers, valence labels and child-model text are legacy policy, not issued developmental law. The required love/availability/material-insufficiency ontology, mixed impression, baseline thickening/repair, and later semantic recruitment are not established. Owner: original V3/Neo-V3 CAN008/CAN011/ADP016/017 competent authorities, not X01.

**AUTHORITY — NO_NATIVE_GRANT.** Original V3 source was read-only historical evidence. No native actor, source, rule, C8/C9/C11/C12, Pyat N11/N12 or production right was used or inferred. The first consumers are historical prompts/persona/scoring, not a current native person. Any new operation requires the competent owner and source/permission path.

## 11. Recommended actions (nonissuing)

1. **Do not reuse M36** unknown→50→hopeful/safe-home. Preserve typed missing/unknown and require actual caregiver history or an explicitly issued prior.
2. **Retain M15/M17/M22 as carriers, not laws.** Keep the ten axis names and a typed event-effect/child-model record only as compatibility carriers; replace the derivation and semantics.
3. **Scientific decision first:** issue one concrete rule for caregiver warmth, availability, material insufficiency, reliability, routine, repair, mixed impression, and later recruitment. Distinguish love confidence from world sufficiency; do not force one valence.
4. **Engineering next:** event-parented, time-indexed, scoped expectation/child-model records with evidence, confidence, contradiction, actor access and rule version; a mixed impression record with positive/negative components; a later semantic consumer; explicit NO_CHANGE. Reuse BackboneState/JSON and Pass 1/persona seams only at their demonstrated grain.
5. **Fix separate defects:** alienation-vector mutation; duplicate shard creation in the legacy V2 runner; missing provenance; tests that would catch missing→hopeful, one-parent dilution and mixed events.
6. **First real consumer:** the next lawful C9/C12 person event that reads the semantic value, not a prompt summary, hash, label or narrative line. No production implementation by X01.

## 12. Tests not run / limits

- No current S44/S49/C9/C12/S50 actual-person integration; no C12 person; no native actor/source/rule; no paid model; no survey/raw data.
- No V2 conversation/LLM run and no sourcefree end-to-end person-world test; the V3 tests are historical fixture/state tests.
- The full V3 suite is 150 passed/1 environment-data failure; the one failure is country canonicalization, not an assigned-mechanism result. The simpler YAML bridge’s metabolization failure is a bridge numeric-key artifact, not source behavior.
- No claim that old V3 is empirically valid, that proxy strivings are human motives, or that the child model is a real childhood. No claim that the historical tests prove current product integration.
- The archive-level zip hash is not the TD-R05 archive hash; file-level identities are the evidence. This is a documented limitation, not a claim of original-archive exactness.

## 13. Remote and return artifacts

- Sealed startup: `2647a4cf25d8bb33a00471e1af9c5e58c2825efb`.
- Branch: `agent/v3court-x01-expectations-child-model-r1`.
- Final artifact commit and remote readback are recorded in `REMOTE_READBACK.json` and in the worker handoff response; the branch tip after the readback commit is the final remote SHA. The return tree is `V3_COURTS/WORKER_RETURNS/X01/` plus the assigned `V3_EXISTING/M01/M15/M17/M22/M36/01_DIRECT_SOURCE_MAP.md` files.

**STOP:** documentary/sourcefree return only; no self-adoption, no native issuance, no production implementation, no reviewer dispatch.
