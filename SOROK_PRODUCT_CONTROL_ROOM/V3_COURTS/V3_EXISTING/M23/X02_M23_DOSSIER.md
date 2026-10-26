# X02 M23 — autonomy/safety drives and conditions

**Historical code grade:** `HISTORICAL_SOURCE_AUDITED`; `HISTORICAL_RUN` only indirectly via yearly/derived tests; no behavioral unit test.
**Current integration:** `UNTRACED` outside historical V3.
**Coverage:** `PARTIAL_WRONG_MEANING` for N01/N03/N04.
**Authority:** none; universal constants and SES lookups are legacy policy.

## Direct source map

- State fields: `v3/core/state.py:554-561` — `autonomy_drive`, `safety_drive`, `autonomy_condition`, `safety_condition`, 0–100.
- Seed: `v3/io/identity_to_backbone.py:339-368` — drives fixed at **65/68** (“universal constant”); conditions from SES lookup + minority modifier (−12 minoritized; +8 dominant).
- Derived gaps: `v3/core/derived.py:202-214` — `max(0, drive−condition)`, gap pressure .5/.5.
- Micro-drift: `v3/systems/autonomy_safety.py:27-110` — random uniform drift/repair seeded by year/config; drift bias from gap/stability; repair bias from insulation/support/alignment; clamps ±2; appends micro trace; no caregiver/relationship action.
- Pressure-flow relation: not directly read. `derive_insulation_profile`/`vitality` do not read these. `stability_threshold` and `alignment_vector` (derived) feed micro-drift, not pressure flow.
- Tests: no dedicated autonomy/safety behavior test found; only architecture order/JSON roundtrip and field-injection isolation.

## Actual behavior

Autonomy/safety are four scalar fields. Drives are fixed near-universal constants; conditions are structural SES/minority lookups. Each year, if the larger gap exceeds 5, a random uniform drift (negative) plus repair (positive) is applied; sign can be mixed. The trace records conditioning inputs (`gap_pressure`, `stability_threshold`, `insulation_score`, `alignment_vector`, `social_support`). This is a stochastic micro-adjustment around a default, not an account of actual caregiver support, safety relations or practical latitude.

The random seed is `config.seed or state.year`; a fixed year/config gives deterministic draws, but there is no actor- or relationship-specific access evidence. The default state (50/50/50/50) is non-terminal.

## Differential

N01/N03/N04 require **context-bound seek/avoid/explore/appease activity and felt safety via actual caregiver and conditions**, with retention only through causal history. Old code:
- represents drive/condition gaps;
- has a repair/drift trace;
- but uses universal drive constants and demographic condition lookup;
- has no caregiver/relationship/action input;
- no support/repair semantics beyond aggregate insulation/support;
- no scope or access;
- no direct relation to pressure-flow channel recruitment.

**Coverage:** `PARTIAL_WRONG_MEANING` — a scalar gap/repair model exists; actual relational safety/autonomy is not represented.

## Dispositions

- **Retain:** drive/condition/gap distinction; trace of micro-adjustments; repair bias idea.
- **Adapt:** condition from actual material/social/relationship facts; drive from issued needs/motives or clear experimental policy, not universal constants; add support/access/repair and temporal scope; remove random drift as default psychology.
- **Replace:** fixed 65/68 drives; SES/minority condition lookup; random uniform micro-drift as a causal law.
- **Create:** relational safety/autonomy conditions and repair/appeasement operations (CAN008/CAN011 owners). No new constants proposed.

## Falsifiers / limits

- If fixed drives are claimed as human universals, source labels them “universal_constant” without evidence; Neo-V3 rejects that as law.
- If micro-drift is claimed to reflect caregiver repair, source is random uniform plus aggregate bias; no caregiver/action input.
- If autonomy/safety is claimed to drive pressure-flow routing, source does not read those fields in the pressure-flow family; it feeds derived stability/alignment and micro-drift.

**Owner:** V3 implementation/M23; CAN008/CAN011 science owners.
