# M36 — hopeful/medium parent defaults: direct source map

**Source grade:** HISTORICAL_SOURCE_AUDITED / HISTORICAL_RUN; CURRENT_INTEGRATION: PATH_LOCATED.
**Verdict:** the unknown→50→hopeful/safe-home conversion is real and occurs at several independent layers. It is not a neutral unknown; it is a semantic assertion.

## Exact default layers

1. **Per-field parent behavior default 50**
   `v3/io/parent_baseline_from_behavior.py:18–22` `_float(val, default=50.0)`; 45–50 reads father/mother warmth/authority/material with default 50; 51–53 averages them.
2. **Missing parent identity path**
   `infer_parent_baseline_and_regime({})` (parent_baseline_from_behavior.py:25–86): both father/mother empty → all six values 50 → warmth/authority/material 50 → all need axes start `"hopeful"` (56–58); no threshold fires at 50; regime warmth/coercion/openness/anxiety/shame 50, modeling 60.
3. **Derivation default**
   `v3/engine/expectation_baseline.py:131–135`: `parent_cat = (parent_baseline or {}).get(ax) or "hopeful"`; missing category → score 0 → `"hopeful"` (139–142).
4. **Yearly setdefault**
   `v3/engine/striving_objects.py:256–257`: every missing axis is set to `"hopeful"` at each yearly striving update.
5. **Child-model default**
   `v3/io/identity_to_backbone.py:81–90`: no forbidden/hopeless axis → default rules `"Adults are mostly fair"`, `"Friends don't betray you in public"`, `"Home is safe"`; default taboos `"sex","police","money shame"`.
6. **LLM summary fallback**
   `v3/engine/llm_contract.py:722–731`: if `state.child_model` is empty, the same safe-home rules/taboos are inserted into the Pass 1 summary.
7. **V2 sampler / server defaults**
   `server/generation/simulation.py:369` `default_behavior = {"parental_warmth":50,"parental_authority":50,"parental_material_support":50}` when no driver vector; `v2/spec.py:3517–3528` with `driver_vec is None` samples normal(50, variance) for the three behavior fields, i.e. a random near-50 rather than an actual parent history. The old V2 runner then writes those values to parent identity and calls `infer_parent_baseline_and_regime` (`v2/run_full_simulation_with_llm_log.py:772–785`); the server does the same at `server/generation/simulation.py:405–418`.

## Exact missing-parent probe

`probe_v3_x01.py` / `probe_v3_x01_output.json`:

- `infer_parent_baseline_and_regime({})` → all axes `hopeful`; regime `{warmth:50, coercion:50, openness:50, anxiety:50, shame:50, modeling_consistency:60}`.
- `derive_child_expectation_baseline(...)` → all ten axes `hopeful`.
- `child_model_from_parent_baseline_and_regime(None,None)` → safe-home rules, default taboos, `what_counts_as_possible="medium"`.
- `backbone_state_from_identity({}, year=1990, age=0)` → `state.expectation_baseline` all hopeful; `state.child_model` safe-home; `initial_state_provenance` has no baseline/child-model entry.

## The one-parent dilution (critical)

`infer_parent_baseline_and_regime` always averages a present parent with a missing parent's 50; the YAML's declared `seed_weights` (0.55/0.35/0.10 or 0.75/0.25) are not used. Probe with one present parent at `warmth=85, authority=45, material=20` and the other missing:
- averaged `warmth=67.5`, `authority=47.5`, `material=35.0`;
- no warmth/authority/material threshold fires (warmth is below 70 for the global modifier; material is exactly 35, not `<35`);
- all ten axes `hopeful`; child model safe-home defaults.
This is **identical to both parents missing for this threshold-boundary input**, even though one parent is palpably warm and the household is materially insufficient. Lower material could cross the status/competence threshold, so the defect is threshold-sensitive; the 50 default is still not a neutral missing marker: it dilutes the actual evidence and the code has no love/availability schema in any case.

## Hidden constants (legacy policy, not issued science)

- 0–100 clamp; default 50; warmth thresholds `<40`, `<30`, `<25`; authority thresholds `>60`, `>70`, `>65`; material thresholds `<35`, `<25`, `<30`; shame 50/60; modeling `0.5*warmth + 0.3*(100-authority) + 20`.
- Global modifier thresholds `warmth>=70`, `modeling>=60`, `anxiety>=80`, `shame>=80`, `openness>=70`.
- Need-axis score clamp `[-2,2]`; category map.
- Child-model `what_counts_as_possible` thresholds `openness>=60`, `coercion<50`, `openness<40`, `coercion>=60`.
- Shard malheur threshold `identity_load>=60`; shard prediction/opacity defaults.
These are constants in source; no source-issued scientific authority accompanies them.

## Tests

No original test asserts missing parent → 50/hopeful or one-parent dilution. `test_connector_and_field_injection.py` only checks that baseline/child-model objects exist; `test_llm_contract.py` checks summary presence; full suite 150 passed/1 environment-data failure. The missing→hopeful behavior is established here by direct probe, not by the original tests.

## Grade

**CONFLICTING** with the Neo-V3 requirement. The old behavior is a real implemented semantic; the required behavior is explicit unknown/missing, not 50/hopeful/safe-home. Disposition: remove the default conversion; if a product rule needs an explicit prior, it must be separately issued with provenance, not hidden in `_float`/`setdefault`.
