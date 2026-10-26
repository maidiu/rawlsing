# SOROK V3 COURTS RX01 — INDEPENDENT HOSTILE REVIEW OF X01

**Reviewer branch:** `agent/v3court-review-rx01-baseline-source-r1`
**Sealed startup:** `b9ff1cf05721ea8609cb631489b4a07448ec287b`
**Review target:** X01 `2e1853dd535bb2b4e9d0bd8a8e31ab561aa75c2a`
**Role:** independent I2/I3 historical-code reviewer; not X01, Sorok HQ, production editor, native scientific issuer or own reviewer.
**Surface:** S2 local Mac, read-only historical V3 source at `<V3_SOURCE_ROOT>`; no provider/model call, no raw respondent data, no production edit.
**Terminal:** `RX01_REVIEW__ENGINEERING_ACCEPT_SCOPED_WITH_PRECISE_REVISIONS__X01_150P1F_REPRODUCED__M36_CONFLICTING_AGREED__SCIENCE_RULE_UNISSUED__AUTHORITY_NO_NATIVE_GRANT__CURRENT_C9C12_HOLD`.

---

## 0. Verdicts

**ENGINEERING: `ACCEPT_SCOPED_WITH_PRECISE_REVISIONS`.**
X01's exact source files, file-level identities, historical test command, full-suite count, probe results and core code facts are independently reproduced. Several **precision corrections** are required (MDV failure cause; one-parent “identical observable”/“erased” wording; “one coarse split” wording; the `rules={}` empty-rule probe; a few line locators). They do not overturn the engineering findings.

**SCIENCE: `HOLD / RULE_UNISSUED`.**
X01's source-grounded critique is accepted: the historical code cannot represent the required love-plus-material-insufficiency relation, mixed impression, repair, scoped expectation or later semantic recruitment. That is a source-level and conceptual finding, **not** an empirical law, native rule or validated developmental mechanism. The concrete care/expectation/impression/child-model/coupling rule remains unissued.

**AUTHORITY: `NO_NATIVE_GRANT / READ_ONLY_HISTORICAL_SOURCE`.**
No native actor/source/rule/CAN/ADP/Pyat/C8/C9/C11/C12/human permission is used or inferred. No production, canonical atlas, X01 return or other worker was edited. Historical V3 is evidence, not a current person. Current C9/C12 integration remains `HOLD/UNTRACED`.

---

## 1. Preflight and source custody

- Remote reviewer branch was at the exact sealed startup `b9ff1cf05721ea8609cb631489b4a07448ec287b` before this work; a dedicated isolated worktree was created from that SHA.
- No existing RX01 worktree/session was found; no other worker branch/worktree was modified.
- Authorized source exists at `<V3_SOURCE_ROOT>` and was read directly, read-only.
- X01 target tree at `2e1853dd535bb2b4e9d0bd8a8e31ab561aa75c2a` was read: `00_RETURN.md`, all six dossiers, `SOURCE_IDENTITIES.json`, `TEST_MANIFEST.json`, `REMOTE_READBACK.json`, all probe scripts/outputs and test logs.
- No model/provider call, raw survey/respondent data, LLM person run or production implementation occurred.

### 1.1 Source identity independently checked

| Check | Result |
|---|---|
| S50 31-file manifest | **31/31 exact** |
| X01 `additional_required_files` | **10/10 exact** |
| X01 `supporting_files` | **9/9 exact** |
| Local staging zip | `3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289` |
| TD-R05 archive identity | `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086` |
| Archive-wide identity | **NOT CLAIMED / NOT MATCHED**; X01 correctly caveats this. File-level identities are the evidence. |

Key exact hashes (all match X01 and the local source):

- `v3/core/state.py` `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`
- `v3/engine/expectation_baseline.py` `632e1e608bfc674a241e57bafa24e91834a2b8bdc3e4ed326dae6fca4e695d43`
- `v3/io/parent_baseline_from_behavior.py` `4e5be6448a5b76c413492ec2a83b62d9e9a2247ce131a094727d974a17cf750b`
- `v3/engine/expectation_events.py` `307ae929a43935170a2f792b4a702a02ac54819a4fa897aa3fef4a099a96cb49`
- `v3/engine/effects/delta_templates.py` `7d99ddf26fd45b52e5e3c10074066ba5e06d17cdaf1fabad06298af3770815f0`
- `v3/io/identity_to_backbone.py` `cb29c9595ac495c3b69b693d4c58a278e9ef1f63a7a8917d8e407920fbd3bdda`
- `v3/engine/prompts.py` `4702de20590579c3c4543dfa5139aa4a3ce6df47ed1aee2c92c800d5a3038d57`
- `v3/need_axis_rules.yaml` `e18cb396cc5dfba28cad1681ca86fb855496a2261b7942d408eedcccbf67bf95`
- `v3/proxy_striving_map.yaml` `a9f4e9bdf5a9942e9de9c82b839c1e6f5e4aadef56ee83bdbe53ca6beb150f2c`
- `v3/expectation_event_templates.yaml` `4fead2145e6b5695d016e6d22f7dc52349ac43c970c21875b49f728e9d5e0fee`
- `v3/engine/effects/rupture_templates.yaml` `8c1821659a5335b511555b3c41b0a3b67fee9a05793e91afd1bfe29deafa7c94`
- `v3/v3config.yaml` `5efc71e3f1b6f6a188df8b650a16bb16db099db8448655816e10989129221ba9`
- `v3/engine/llm_contract.py` `f024debf7b8a637e91c546689a0bed31baff55d98f1378b06cb82ebb4c0fe9cf`
- `v3/engine/scoring.py` `36833287c72ffa40d0ece1ebc66fb0d685a92fc71aab1d211be9b21bfd0a82cb`
- `v3/engine/striving_objects.py` `78c79a9312b05aa51220d09bb63c91cafd6bb204f2c398ac1876b1ef3144c1c3`
- `v3/io/json_codec.py` `c4bc07dd73c249c35d788f5b459f4b0c1b23702a7d55157a4eb3fdbc74b1cf14`
- `v3/io/persona_sheet.py` `4a0009533443baef2786fc498c7f8db3ead7d133d8ee7e97e6d7128d4322a00e`
- `v2/run_full_simulation_with_llm_log.py` `b7d727e2732c5520e663e047c9815eead3b24d41be8b63edc55279bb01f66064`
- `server/generation/simulation.py` `5d68ffe3bc6902dc60b90625443a03127cf0d04b4eed4327270a3a0226bc78d1`
- `v2/spec.py` `f7ca16a7addf4dd1bd155a985586f926f1a4c31f127b829bcb8056c851d58296`

Independent authority-record spot checks: `ADP_007_V3_ACTOR_INITIALIZATION/AUTHORITY.json` records `parent_baseline_from_behavior.py` hash `4e5be644…` and explicitly marks `parent_child_baseline_defaults: REMOVE_FROM_ADP007`, `universal_midpoint_defaults: REMOVE_REJECT`; `CAN_012_V3_RUPTURE_METABOLIZATION/AUTHORITY.json` records `delta_templates.py` hash `7d99ddf…`. These support the architectural direction, not a new rule.

---

## 2. Independent execution and probes

### 2.1 Test execution

| Evidence | Reviewer result |
|---|---|
| Focused historical tests (`test_connector_and_field_injection.py`, `test_wave4.py`, `test_llm_contract.py`, `test_v5_baseline_load.py`) | **51 passed** |
| Full `v3/tests` with read-only YAML bridge | **150 passed, 1 failed** in 167.31s |
| The one failure | `test_persona_sheet_integrity::…` `'MDV' != 'Maldives'` at `v3/tests/test_persona_sheet_integrity.py:49` |
| Simple-bridge numeric-key failure | Independently reproduced on `test_metabolization_effects::TestMetabolizationEffects::test_get_template_for_age` (template lookup `None`) |
| X01 probe scripts rerun | All three outputs **byte-identical** to X01 committed outputs |
| Independent reviewer probe | Reproduced missing-parent, both-present love/low-material, one-present, cold/high-material, environment, axis rules, child-model, shard, alienation, provenance, duplicate and country cases |

The YAML bridge supplies `yaml.safe_load` through system Ruby/Psych because PyYAML is absent; it converts numeric YAML keys back to integers. It is a read-only compatibility layer, not a source edit. It is adequate for the 150/1 suite at this grain; it is not a claim of universal PyYAML equivalence.

### 2.2 MDV failure — precise correction

X01 says the failure is an “environment/data canonicalization dependency” outside M15/M17/M22/M36. **Scope AGREE; cause REVISE_PRECISE.**

- `factbook-out/country_cdf1.json` **exists and contains “Maldives”**.
- `pycountry` is **not installed**.
- `_factbook_index` builds `by_iso3` only when `pycountry` is available (`v2/country_reference.py:89-95`).
- `normalize_country_ref("MDV")` therefore returns `canonical_name="MDV"`, `resolved_via="original"`, `fallback_used=True`; `normalize_country_ref("Maldives")` resolves to `Maldives`.
- So the failure is **missing optional pycountry plus an ISO3→factbook fallback gap**, not missing country data. It remains outside M15/M17/M22/M36 and does not change the mechanism findings.

### 2.3 Exact independent probe values

- **Missing parent `{}`:** inferred baseline all `hopeful`; derived all `hopeful`; regime `warmth 50, coercion 50, openness 50, anxiety 50, shame 50, modeling 60`; child model `[“Adults are mostly fair”,“Friends don't betray you in public”,“Home is safe”]`, taboos `[“sex”,“police”,“money shame”]`, possibility `medium`.
- **Both present, warmth 85 / authority 45 / material 20:** inferred parent baseline `status=competence=hopeless`, others `hopeful`; derived `status=competence=forbidden`, other axes `entitled`; child model only `[“Status is for others.”,“You're not allowed to be good at this.”]`, no safe-home/fair-adult rules; possibility `medium`.
- **One present, 85/45/20, other absent:** arithmetic means `warmth=67.5, authority=47.5, material=35.0`; derived all `hopeful`; child model safe-home defaults; possibility `medium`. This matches missing parent on **baseline and child-model rules**, but **not on transmission_regime** (67.5/47.5/52.5/32.5/50/69.5 vs 50/50/50/50/50/60), and not on the parent input.
- **One present, 85/45/10, other absent:** material mean 30 → `status=forbidden`; child model `[“Status is for others.”]`; not identical to missing. The dilution is threshold-sensitive.
- **One present cold high material 30/80/80:** means `warmth=40, authority=65, material=65`; derived all `hopeful`; child model safe-home defaults but possibility `narrow`; not identical to missing on possibility.
- **Both present cold high material 30/80/80:** `attachment=hopeful` at exactly 30 (code uses `<30`), `belonging/safety/autonomy=forbidden`; child model three negative rules; possibility `narrow`.
- **Both present 85/45/80:** all axes `entitled`; child model safe-home defaults.
- **`what_counts_as_possible` orthogonality:** child model with `attachment=forbidden, safety=hopeless`, regime openness 70/coercion 30 returns `what_counts_as_possible="wide"` while containing “Adults can leave…” and “Institutions can hurt you.” Possibility is computed only from openness/coercion, not from the rules.
- **Child-model age:** age 0 and age 80 produce identical output; `age` is unused.
- **Shards:** same label “Parent works late but calls to say she loves me”:
  - `fulfillment` → one GiftShard (`positive`, `medium`, `low`), no DisruptionShard;
  - `violation` → one DisruptionShard (`negative`, `high`, `high`, `malheur_risk=true` at identity_load 65), no GiftShard;
  - `mixed` → no shard;
  - baseline unchanged in all cases;
  - shard keys contain `striving_object_id`, year, age, need_axis, label, valence, prediction_error, opacity/malheur, but **no event id/hash, source/access, causal parent or rule/version**.
- **Duplicate path:** `apply_deltas_to_state` with a fulfillment event creates one shard; a second direct call to `apply_gift_disruption_shards_from_events` creates a second (`gs_2024_8_0`, `gs_2024_8_1`). This reproduces the two-call legacy V2 path; the actual V2 conversation runner was not executed end-to-end (no LLM).
- **Alienation:** violation delta 3.0 → scalar before 0.0, after 50.0 (reset by vector aggregate); vector remains 50.0 across all real fields; dynamic attributes `structural/affective/institutional=53.0`; **delta lost**.
- **Provenance:** `initial_state_provenance.fields` has no `expectation_baseline`, `child_model`, `gift_shards` or `disruption_shards` entries.
- **Parent container merge:** if `parent_behavior.father` is present and `parents.mother` is also present, the mother is ignored (line 41 only falls back when both `father_b` and `mother_b` are empty). This is an additional one-parent/data-shape defect.
- **Axis rules:** `axis_rules` exists in YAML but is not consumed. Corrected test: truthy `{'axis_rules': …}` → all `hopeful` under high warmth; `{'global_modifiers': [], 'meta': {}}` → all `hopeful`; actual full rules → all `entitled` under high warmth. The axis-only and no-global outputs match; the global-only output matches actual. This confirms the conclusion but corrects X01's `rules={}` probe method (`rules={}` is falsy and reloads the actual rules at `expectation_baseline.py:125`).

---

## 3. Claim matrix

**Status vocabulary:** `AGREE` = exact at the stated grain; `REVISE_PRECISE` = finding stands but evidence/wording/scope needs the named correction; `HOLD` = not verifiable/issued at required grain.

| ID | X01 claim | Status | Reviewer evidence / correction |
|---|---|---|---|
| C01 | 31/31 S50 identities exact; additional/supporting hashes exact; archive-wide not claimed | **AGREE** | Independent hashes; local zip `3f2c5ed9…` ≠ TD-R05 `953c9149…`; file-level exact. |
| C02 | Full V3 suite 150 PASS / 1 FAIL; focused 51 PASS | **AGREE** | Independently 150/1 (167.31s) and 51/0; exact MDV failure reproduced. |
| C03 | Missing parent `{}` → all `hopeful` + safe-home child model | **AGREE** | Source `parent_baseline_from_behavior.py:18-22,45-58`, `expectation_baseline.py:131-135`, `identity_to_backbone.py:81-90`; probe exact. |
| C04 | One present 85/45/20 parent is averaged with 50 → 67.5/47.5/35; all-hopeful + safe-home | **AGREE** | Probe exact; `infer_parent_baseline...:45-53`; **wording correction**: regime differs (67.5/47.5/52.5/32.5/50/69.5), so not every observable field is identical. |
| C05 | One-parent dilution is threshold-sensitive, not universal erasure | **AGREE** | Material 10 → status forbidden; one cold 30/80/80 → all-hopeful derived but possibility narrow. X01 says “threshold-sensitive” but also “single-parent case is erased”; clarify scope. |
| C06 | Need-axis YAML `axis_rules`/flags/conditional modifiers/base_by_meaning_frame/meta.thresholds/seed_weights not consumed; only four global modifiers used | **AGREE** | `expectation_baseline.py:68-104` only `global_modifiers`; grep finds no other consumer; probe axis-only vs no-global equal. **But** X01's `rules={}` “empty” comparison is not a true empty rule set; see §4.3. |
| C07 | Environment keys have no current effect | **AGREE** | No current global modifier consumes `economic_precarity`, `external_threat`, etc.; code merges env into regime, so an issued modifier could consume them. |
| C08 | Child model safe-home defaults; hardcoded rules/taboos; `age` unused; positive rules suppressed by any forbidden/hopeless axis | **AGREE** | `identity_to_backbone.py:60-109`; probe exact; add `what_counts_as_possible` orthogonal finding. |
| C09 | Same event can become either one GiftShard or one DisruptionShard, never both | **AGREE** | `expectation_events.py:103-164`; probe exact; no mixed branch. |
| C10 | Shards lack event id/hash, access/source, causal parents, rule/version; ids positional | **AGREE** | `state.py:338-364`; probe keys; ids `gs_/ds_{year}_{age}_{len}`. |
| C11 | Alienation delta is silently lost | **AGREE** | `delta_templates.py:314-319` writes non-existent `structural/affective/institutional`; `clamp_all` resets scalar; probe exact. Applies to any `alienation_delta`, including epistemic rupture. |
| C12 | Legacy V2 runner double-creates shards; newer `run_llm_band` does not | **AGREE** | Static call sites `v2/run_full...:699-700,934-935` and `run_llm_band.py:266-270`; two-call probe yields 2 shards; actual V2 conversation runner not executed. |
| C13 | Baseline/child-model/shards have no initial provenance | **AGREE** | `initial_state_provenance` fields list; probe returns null for all three. |
| C14 | First consumers are historical `striving_update` / Pass 1 / persona / scoring / JSON, not current C9/C12 | **AGREE** | Source grep; no current C9/C12 integration located; current integration **HOLD**. |
| C15 | Failure is “environment/data canonicalization” outside M15/M17/M22/M36 | **REVISE_PRECISE** | Scope AGREE; cause is missing `pycountry` + ISO3 fallback gap, not missing factbook data; factbook contains Maldives. |
| C16 | “The old machine can produce one coarse cross-axis split only in a narrow both-present threshold-crossed case.” | **REVISE_PRECISE** | Multiple threshold-derived cross-axis patterns exist (both cold high material → autonomy/belonging/safety forbidden; both love/low material → status/competence forbidden; both love/material 80 → all entitled; one cold → all-hopeful/narrow possibility). The love+insufficiency input produces one split; “only one split possible” is too broad. |
| C17 | Missing parent is a “positive-normalizing input” | **REVISE_PRECISE** | 50 is a midpoint-normalizing input; direction depends on present values (lowers 85 warmth, raises 20 material). The semantic output is optimistic/safe-home; “positive-normalizing” should be read as optimistic normalization, not a positive value. |
| C18 | “The single-parent case is erased” | **REVISE_PRECISE** | The tested 85/45/20 one-present case matches missing on baseline/child-model rules; regime differs; cold one-parent differs in possibility; material 10 crosses status. Say “the tested loving-low-material one-parent case loses the intended love/insufficiency contrast,” not all single-parent cases. |
| C19 | Some source line locators (e.g. `BackboneState` 500–614, `GiftShard` 338–350) | **REVISE_PRECISE** | Class definitions are `BackboneState` at `state.py:501` (decorator 500), `GiftShard` at 339 (decorator 338); no semantic impact. |
| C20 | M01 `INFRASTRUCTURE_ONLY`, M15/M17/M22 `PARTIAL_WRONG_MEANING`, M36 `CONFLICTING` | **AGREE** | Source facts support; M36 current ADP007 authority explicitly rejects midpoint/default child assumptions. This is coverage, not native science. |
| C21 | Old V3 does not satisfy the love + material-insufficiency theoretical target | **AGREE** | No relation/availability/confidence/mixed schema; threshold artifacts only. Not an empirical law or native rule; scientific owner unissued. |
| C22 | No native/self-adoption | **AGREE** | X01 read-only; no source/production/atlas edits; no current C9/C12 claim. |

---

## 4. Detailed verification and precise corrections

### 4.1 Missing-parent 50/hopeful/safe-home (C03) — AGREE

`parent_baseline_from_behavior.py:18-22` supplies `_float(..., default=50)`; `:45-50` reads both parent fields with default 50; `:51-53` averages. Missing parent `{}` therefore becomes 50/50/50; `:56-58` starts all axes `hopeful`; no threshold fires; `:78-85` gives regime 50/50/50/50/50/60. `identity_to_backbone.py:514-555` derives baseline; `derive_child_expectation_baseline` line 133 defaults missing category to `hopeful`; `striving_objects.py:256-257` setdefaults every year; `identity_to_backbone.py:81-90` inserts safe-home rules.

This is an exact source behavior. It is a multi-layer optimistic default, not an unknown marker.

### 4.2 One-parent dilution (C04/C05) — AGREE with precise scope

For one present parent at 85/45/20 and the other absent, arithmetic means are **67.5/47.5/35.0**; warmth is below the global ≥70 rule, material exactly 35 is not `<35`, authority 47.5 is below >60. Derived baseline is all `hopeful`; child model is safe-home.

**Corrections:**

- X01's “identical observable result” is too broad: the **transmission regime differs** (67.5/47.5/52.5/32.5/50/69.5 vs 50/50/50/50/50/60). Baseline and child-model rules/taboos/possibility are identical for this input; the regime is not.
- “Single-parent case is erased” should be scoped to the tested loving-low-material input. One present cold parent 30/80/80 yields all-hopeful derived but `what_counts_as_possible="narrow"` (not medium); one present 85/45/10 yields `status=forbidden`. The dilution is real but threshold-sensitive.
- The source also silently ignores the other parent if the two parents are split across `parent_behavior` and `parents` containers (line 41 only falls back to `parents` when both `parent_behavior` parents are empty). This is an additional one-parent/data-shape defect.

### 4.3 YAML per-axis rules (C06) — AGREE, probe method REVISE_PRECISE

Only `rules["global_modifiers"]` is consumed by `_apply_global_modifiers` (`expectation_baseline.py:68-104`). No code consumes `axis_rules`, `flags`, `conditional_modifiers`, `base_by_meaning_frame`, `meta.thresholds` or `meta.seed_weights`. `infer_parent_baseline_and_regime` uses a simple 50/50 average, not `seed_weights`.

**Precise correction:** X01's `axis_rules_application` probe compares actual rules to `rules={}`. But `derive_child_expectation_baseline` does `rules = rules or load_need_axis_rules()` (`:125`), so `{}` is falsy and reloads the actual YAML. The `empty_rules` result is therefore not an empty-rule control.

Reviewer corrected test (truthy dicts):

- `{"axis_rules": actual_axis_rules}` under warmth 80/modeling 80 → all `hopeful`;
- `{"global_modifiers": [], "meta": {}}` → all `hopeful`;
- actual full rules → all `entitled`;
- `{"global_modifiers": actual_global_modifiers, "meta": actual_meta}` → all `entitled`.

So the **conclusion** “per-axis rules are not applied; global modifiers are” is correct; the **evidence method** needs the truthy empty/axis-only control.

### 4.4 Child-model safe-home defaults (C08) — AGREE

`child_model_from_parent_baseline_and_regime` (`identity_to_backbone.py:60-109`) maps any `forbidden`/`hopeless` axis to one hardcoded rule and up to two taboos; if no such axis, it inserts the three safe-home/fair-adult rules. `age` is accepted but never read. When a forbidden/hopeless axis exists, positive defaults are suppressed; in the both-present love/low-material case it returns only status/competence prohibitions, no love/availability rule.

**Additional finding:** `what_counts_as_possible` is computed only from regime openness/coercion (`:92-103`). A child model can contain “Adults can leave…”/“Institutions can hurt you” and still be `wide` when openness is 70/coercion 30. The possibility field is not integrated with the assumed-rule content. X01's probe contains this value but the return does not discuss the inconsistency.

### 4.5 Mono-valent shards and missing parentage (C09/C10) — AGREE

`apply_gift_disruption_shards_from_events` (`expectation_events.py:103-164`) accepts only `fulfillment`/`violation`; creates one `GiftShard` or one `DisruptionShard`; requires an active `striving_object_id`; uses the caller/LLM-supplied label; `identity_load>=60` drives malheur; no baseline read. The same event cannot produce both components. Shards have no selected event id/hash, source/access actor, causal parent, rule/version or scope. IDs are positional (`gs_{year}_{age}_{len}`, `ds_...`).

This is exact at source and probe grain. It is a **carrier** limitation, not a native rule.

### 4.6 Alienation delta loss (C11) — AGREE

`delta_templates.py:314-319` computes `new_agg`, then writes `v.structural = v.affective = v.institutional = new_agg`. `AlienationVector` has `distant_others, near_others, self, moral_totality` (`state.py:95-104`); those assignments create dynamic attributes. `state.clamp_all()` recomputes `state.alienation` from the unchanged vector. Probe: delta 3.0; scalar before 0.0, after 50.0; vector unchanged; dynamic attrs 53.0. The consequence is lost. The bug applies to expectation violation and epistemic rupture (`delta_templates.py:97-108`).

### 4.7 Duplicate legacy shard creation (C12) — AGREE

`apply_deltas_to_state` already calls `apply_gift_disruption_shards_from_events` (`delta_templates.py:359-362`). The legacy V2 runner then calls it again at `v2/run_full_simulation_with_llm_log.py:699-700` and `:934-935`. Reviewer two-call probe: 1 shard after `apply_deltas_to_state`, 2 after the second call (`gs_2024_8_0`, `gs_2024_8_1`). The newer `run_llm_band.py:266-270` has only the `apply_deltas_to_state` call. The actual V2 conversation runner was **NOT_RUN**; the duplicate path is established by source + functional two-call reproduction.

### 4.8 Provenance (C13) — AGREE

`backbone_state_from_identity` records `initial_provenance.fields` for selected capacity/reproduction/practice/wound/country fields; it does **not** add `expectation_baseline`, `child_model`, `gift_shards` or `disruption_shards`. Probe returns `None` for baseline/child-model/shards provenance. No rule version, parent behavior input hash, scope, confidence or access.

### 4.9 Full suite, YAML bridge and MDV (C02/C15) — AGREE scope, REVISE cause

Reviewer command (from source root):

```sh
RAWLSING_STAGING_ROOT=<V3_SOURCE_ROOT> PYTHONDONTWRITEBYTECODE=1 \
python3 -B <X01 run_v3_tests.py> v3/tests
```

Result: **150 passed, 1 failed in 167.31s**; failure exactly `test_persona_sheet_integrity.py:49`, `'MDV' != 'Maldives'`. Focused 51/0. The simple YAML bridge’s extra `test_get_template_for_age` failure is independently reproduced; the improved bridge removes it via numeric key restoration.

**Cause correction:** `factbook-out/country_cdf1.json` contains Maldives; `pycountry` is absent; `_factbook_index` does not build an ISO3 index without pycountry; `normalize_country_ref("MDV")` returns `MDV`/`original`; `"Maldives"` resolves. This is an optional-dependency/fallback gap, not missing country data. It is outside the assigned mechanisms and does not invalidate the 150/1 report.

### 4.10 “One coarse cross-axis split” and “positive-normalizing” (C16/C17) — REVISE_PRECISE

The reviewer probe shows at least these threshold patterns:

- both 85/45/20: relational axes `entitled`, `status/competence=forbidden`;
- both cold 30/80/80: `attachment=hopeful` at exact 30, `belonging/safety/autonomy=forbidden`;
- both 85/45/80: all `entitled`;
- one 85/45/20: all `hopeful` + safe-home;
- one cold 30/80/80: all `hopeful` + safe-home but possibility `narrow`;
- one 85/45/10: `status=forbidden`.

So the code can produce **multiple** threshold-derived cross-axis patterns; the love+insufficiency family produces one. X01's “one coarse cross-axis split only” should be read as “one split for that input family,” not “only one split possible.”

The 50 default is a **midpoint normalization**; it can lower warmth and raise material in the 85/45/20 case. Its output semantics are optimistic (hopeful/safe-home), but “positive-normalizing” should not imply a uniformly positive numeric shift in every field. The core point—50 is not a neutral unknown—stands.

### 4.11 Line locators (C19) — minor REVISE_PRECISE

`BackboneState` is defined at `state.py:501` (decorator at 500); X01 writes 500–614. `GiftShard` is defined at `state.py:339` (decorator at 338); X01 writes 338–350. No semantic impact; source review should cite the class line.

---

## 5. Positive, NO_CHANGE/alternative and severed-edge

These are sourcefree historical-grain demonstrations, not native psychology.

**Positive (meaningful source result):** both present 85/45/20 produces a real derived split: relational axes `entitled`, `status/competence=forbidden`; child model emits status/competence prohibitions. This is a narrow threshold product, not a representation of love+insufficiency.

**NO_CHANGE/alternative:** one present 85/45/20 yields all-hopeful baseline and safe-home child model (baseline/child-model rules equal to missing; regime differs). A `mixed` expectation_type creates no shard; an event with no expectation type / no active striving creates no shard; baseline is unchanged by expectation events. These are **skips/defaults**, not typed NO_CHANGE records.

**Severed-edge negative:** remove parent behavior `{}` → all-hopeful/safe-home; lower material to 10 → `status=forbidden` with one-parent averaging; remove `striving_object_id` → no shard; second direct shard call → duplicate shard. These show the causal dependencies are real, but they are legacy defaults/one-valence paths, not lawful developmental operations.

---

## 6. Engineering court

**Verdict: `ACCEPT_SCOPED_WITH_PRECISE_REVISIONS`.**

Accepted at sourcefree/historical grain:

- exact 31/31 S50 file identities and additional/supporting hashes;
- 150/1 full suite and 51/0 focused tests reproduced;
- parent 50/hopeful/safe-home pathway;
- one-parent average dilution at the tested values;
- unused per-axis YAML rules/global-only consumption;
- child-model safe-home/category-to-text/age-unused;
- one-valence shards and missing event parentage;
- alienation-vector delta loss;
- duplicate legacy V2 shard path;
- missing baseline/child-model/shards provenance;
- historical first consumers and no current C9/C12.

Required precise revisions:

1. MDV failure cause: optional pycountry/fallback gap, not missing data.
2. `axis_rules_application` `rules={}` control is not empty; use truthy controls.
3. “Identical observable result” for one-parent: baseline/child-model equal, regime differs.
4. “Single-parent case erased” is threshold-sensitive; cold one-parent and material-10 differ.
5. “One coarse cross-axis split only” is too broad; multiple threshold patterns exist.
6. “Positive-normalizing” should be “optimistic midpoint normalization.”
7. Class line locators off by decorator line.
8. Additional findings: `what_counts_as_possible` can be `wide` with forbidden attachment/safety; mixed parent containers ignore the other parent.

No engineering RED invalidates the core source facts. The precise revisions are corrections, not a rejection.

---

## 7. Science court

**Verdict: `HOLD / RULE_UNISSUED`.**

X01's source-grounded critique is scientifically sober:

- The ten axes/four categories are a coarse carrier, not a validated developmental ontology.
- The parent thresholds (warmth `<40/<30/<25`, authority `>60/>70/>65`, material `<35/<25/<30`), `50` midpoint, global warm `+1`, `identity_load>=60` malheur threshold and hardcoded child-model text are legacy implementation policy, not issued scientific law.
- The code cannot represent love and material insufficiency as coexisting components; it forces one valence at the event level and a thresholded category at the baseline level.
- It has no scoped expectation, evidence/confidence, care availability/reliability/routine, repair, contradiction, mixed impression or later semantic recruitment.
- A missing parent is not unknown; it is an optimistic midpoint/safe-home input.

This is a negative source finding, not a positive scientific rule. The competent owner still must issue the concrete care/expectation/impression/child-model/coupling rule(s); X01 and this reviewer cannot. No empirical effect size, trait, learning law, human A5 or native person is established.

**Science HOLDs:**

- concrete care/availability/material/reliability/routine/repair semantics;
- mixed/uncertain impression and challenge/complication/threat taxonomy;
- durable CAN011 target transition and later CAN008 recruitment;
- current person/world source/permission and C9/C12 consumer.

---

## 8. Authority court

**Verdict: `NO_NATIVE_GRANT / READ_ONLY_HISTORICAL_SOURCE`.**

- X01's return is a historical source review; it did not issue a native rule, adopt a person, or modify production/canonical files.
- This reviewer used the original V3 source read-only and X01's immutable return; no production/atlas/other-worktree edit.
- Current ADP007 authority (`ADP_007_V3_ACTOR_INITIALIZATION/AUTHORITY.json`) explicitly records `parent_baseline_from_behavior.py` as `REMOVE_FROM_ADP007`, `universal_midpoint_defaults` as `REMOVE_REJECT`, and `default child assumptions` as forbidden; this supports the direction to remove 50/hopeful/safe-home from native initialization. It does **not** issue the replacement care/expectation rule.
- No native C8/C9/C11/C12/Pyat N11/N12, actor/source, human or production right is used or inferred.
- Current C9/C12 integration is **HOLD/UNTRACED**: X01 correctly says it has none; this review did not convert historical tests into current-person evidence.

---

## 9. First actual consumer / currentness

| State | Historical first consumer | Current C9/C12? |
|---|---|---|
| `expectation_baseline` | `striving_update` proxy spawn (`striving_objects.py:256-270`), Pass 1 summary (`llm_contract.py:735-739`), V2 persona sheet (`persona_sheet.py:922,956`) | **UNTRACED / HOLD** |
| `child_model` | Pass 1 summary (`llm_contract.py:710-717`), rupture scoring (`scoring.py:148-160`), prompt (`prompts.py:28`) | **UNTRACED / HOLD** |
| `gift_shards`/`disruption_shards` | V2 persona/backstory (`persona_sheet.py:452-467,938-948`) and JSON persistence | **NONE LOCATED** |
| Striving/Axes | historical proxy layer | **NOT NATIVE** |

The required later same-person C9/C12 consumer that reads a typed semantic value is **not present** in this source and was not executed.

---

## 10. HOLDs, REDs and exact next blockers

**HOLD_SOURCE_ARCHIVE_WIDE_IDENTITY:** local zip `3f2c5ed9…` ≠ TD-R05 original `953c9149…`; file-level 31/31 and additional hashes are exact. Owner: source custodian. Not a blocker to the mechanism findings.

**HOLD_CURRENT_C9C12_INTEGRATION:** no current C9/C12/same-person consumer; historical tests/probes only. Owner: current Sorok actor/world/HQ; separate commission.

**HOLD_SCIENTIFIC_RULE:** care/availability/material/reliability/routine/repair, mixed impression, child-model development, baseline thickening and later recruitment are unissued. Owner: original V3/Neo-V3 CAN008/CAN011/ADP016/017 competent authority.

**HOLD_NATIVE_AUTHORITY:** no native actor/source/rule/C8/C9/C11/C12/Pyat/human grant.

**No RED** in X01's assigned source facts at the reviewed grain. The MDV failure is an environment/fallback issue outside the assigned mechanisms. X01's own self-adoption is absent; no self-review issue.

**Precise next blockers/decisions:**

1. Source custodian: confirm or re-bind the archive-wide staging identity; the file-level evidence suffices for this review.
2. Scientific owner: issue the concrete care/expectation/impression/coupling rule before implementation; unknown/missing must remain typed, not 50/hopeful/safe-home.
3. Engineering owner: after rule issuance, event-parented scoped records, mixed components, evidence/confidence, repair/no-change, later C9/C12 semantic consumer; no prompt/persona substitute.
4. Verification owner: add negative tests for missing vs known-safe vs known-negative parent, one-parent dilution, mixed care+insufficiency, no-received event, support withdrawal, hash-only change, and the two-call duplicate path.

---

## 11. Exact commands, limits and final remote

**Commands actually executed by this reviewer:**

- worktree creation from `b9ff1cf05721ea8609cb631489b4a07448ec287b`;
- source manifest checks (31/31 selected, 10/10 additional, 9/9 supporting);
- focused historical tests: **51 passed**;
- full `v3/tests` with read-only YAML bridge: **150 passed, 1 failed**;
- simple-bridge `test_get_template_for_age`: **1 failed** (numeric-key bridge artifact);
- X01 three probe scripts rerun: **byte-identical** outputs;
- independent reviewer probe: formulas/defaults/dilution/YAML/child-model/shards/alienation/provenance/duplicate/country cases.

**NOT_RUN:** current S44/S49/C9/C12/S50 actual-person integration; native actor/source/rule; C12 person; V2 conversation/LLM run; paid provider; raw survey/respondent data; official Astra K tests; any production implementation.

**Changed path:** only `SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/REVIEW_COURTS/RETURNS/RX01/00_REVIEW.md` on this reviewer branch. No source/atlas/production/other-review edit.

**Substantive review commit:** [recorded after the first push].
**Final remote tip:** [readback commit; independently verified by `git ls-remote` after push].

**No self-adoption. No native grant. No production implementation. STOP.**
