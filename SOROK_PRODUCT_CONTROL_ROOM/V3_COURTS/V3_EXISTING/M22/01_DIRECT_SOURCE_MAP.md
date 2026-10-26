# M22 — child model / assumed rules / taboos / possible-world boundary: direct source map

**Source grade:** HISTORICAL_SOURCE_AUDITED / HISTORICAL_RUN; CURRENT_INTEGRATION: PATH_LOCATED, prompt/scoring only.
**Primary files:**
- `v3/core/state.py` `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2` — `child_model` (549).
- `v3/io/identity_to_backbone.py` `cb29c9595ac495c3b69b693d4c58a278e9ef1f63a7a8917d8e407920fbd3bdda` — `child_model_from_parent_baseline_and_regime` (60–109), initialization call (556–572).
- `v3/engine/prompts.py` `4702de20590579c3c4543dfa5139aa4a3ce6df47ed1aee2c92c800d5a3038d57` — `PASS1_SYSTEM` child-model instruction (28).
- `v3/engine/llm_contract.py` (not in S50 31-file manifest) — summary exposure/default (710–732).
- `v3/engine/scoring.py` (not in S50 31-file manifest) — rupture assumption fit (148–160).

## Exact function

`child_model_from_parent_baseline_and_regime(parent_baseline, transmission_regime, age=0)` — `identity_to_backbone.py:60–109`.

Input: parent baseline dict; regime dict; `age` parameter. **`age` is not read anywhere in the function.**
Output: `{"assumed_rules": [...], "taboos": [...], "what_counts_as_possible": "narrow|medium|wide"}`.

Algorithm:
1. For each axis in `_NEED_AXIS_TO_RULES_AND_TABOOS` (45–57): `cat = parent.get(axis) or "hopeful"` (75); if `forbidden` or `hopeless`, add the first rule and up to two taboos for that axis (76–79).
2. If no rules were added, set default rules: `"Adults are mostly fair"`, `"Friends don't betray you in public"`, `"Home is safe"` (81–86). This condition is **any forbidden/hopeless axis suppresses all three defaults**, even when the positive relational axes are `entitled`.
3. Deduplicate rules (max 15) and taboos (max 10); if no taboos, default `["sex","police","money shame"]` (87–90).
4. `what_counts_as_possible` from `openness`/`coercion`: `openness>=60 and coercion<50` → wide; `openness<40 or coercion>=60` → narrow; else medium; missing values → medium (92–103).

The rule/taboo text is hardcoded in `_NEED_AXIS_TO_RULES_AND_TABOOS`; no actual caregiver behavior, household history, culture, language, or event record is read. There is no scope, confidence, evidence count, support, contradiction, procedural/bodily component, or later revision. The `age` argument is dead.

## Initialization and default path

`identity_to_backbone.backbone_state_from_identity` calls the function with the identity's `parent_expectation_baseline` and `transmission_regime` (556–562). If parent baseline is missing, `child_model_from_parent_baseline_and_regime(None, None)` produces:
- rules `["Adults are mostly fair","Friends don't betray you in public","Home is safe"]`;
- taboos `["sex","police","money shame"]`;
- `what_counts_as_possible="medium"`.

This is the exact safe-home default for unknown parents. `llm_contract.state_summary_from_backbone` has a second fallback with the same safe rules when `state.child_model` is empty (`llm_contract.py:722–731`).

## First consumers

1. `v3/engine/llm_contract.py:710–717` puts `assumed_rules`, `taboos`, `what_counts_as_possible` into the Pass 1 state summary.
2. `v3/engine/prompts.py:28` tells the LLM these are “the assumptions-rules-taboos this person carried from childhood,” that they are “the default architecture,” and that violating them is an epistemic-rupture candidate.
3. `v3/engine/scoring.py:148–160` uses `assumed_rules` to score whether an `epistemic_rupture` event actually matches a declared assumption: match → 1.0; no match → 0.35; no rules → 0.7.
4. `v3/io/json_codec.py` persists the dict.
No V3 flow/derived/event-admission consumer was located.

## Probe values

- `child_model_from_parent_baseline_and_regime(None, None, age=0)` → safe-home defaults, medium possibility.
- `parent_baseline={"attachment":"forbidden","safety":"hopeless"}`, regime `{"openness":70,"coercion":30}` → rules `["Adults can leave; attachment is not guaranteed.","Institutions can hurt you."]`, taboos `["abandonment","being left","police","authority"]`, `what_counts_as_possible="wide"`.
- Both parents high warmth/low material (`warmth=85, authority=45, material=20`) → baseline `attachment` etc. entitled and `status/competence` forbidden; child model rules `["Status is for others.","You're not allowed to be good at this."]`, taboos status/success/showing off/being better; **the safe-home and fair-adult rules are absent**, and there is no positive rule about parental love/availability.
- One present loving low-material parent, other missing → all-hopeful baseline and **safe-home defaults**, identical to missing parent. The loving parent's material insufficiency is erased, and the safe-home default is asserted.

## Tests

- `v3/tests/test_connector_and_field_injection.py:75–91` asserts only types and nonempty rules/taboos for forbidden/hopeless axes; it does not assert text, defaults, age, route from actual history, or the love+insufficiency case.
- `test_connector...` 11 passed; full suite 150 passed/1 environment-data failure.

## Grade

**PARTIAL_WRONG_MEANING.** A typed child-model carrier exists and reaches the Pass 1 prompt and rupture scoring. It is static, category-to-text, age-blind, culturally hardcoded, lacks provenance/scope/confidence, suppresses positive defaults when any axis is forbidden, and treats missing parent data as a safe home. It is not a procedural/bodily anticipation or an actual childhood history.
