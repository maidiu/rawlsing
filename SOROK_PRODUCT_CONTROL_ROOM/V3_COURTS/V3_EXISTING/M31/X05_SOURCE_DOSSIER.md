# M31 — life-course Enneagram emergence / end matcher: X05 direct-source dossier

**Court:** X05 historical source / material-actor-world bridge. **Evidence grade:** `HISTORICAL_SOURCE_AUDITED` plus sourcefree probe; `CURRENT_INTEGRATION: UNTRACED`; `THEORY: PROPOSED_NOT_ISSUED`; `AUTHORITY: NO_NATIVE_GRANT`.  
**Direct source:** `v2/enneagram_wisdom.py` `95c018092eae44f319bead262c7d815c477df85ede4f7574e2b08aeff17ce34d`; `v2/parent_type_inference.py` `b05632d01c48f52a5bed36b07b094ac770cada81f51951d78b7bea61e4e66cf3`; `v2/spec.py` `f7ca16a7addf4dd1bd155a985586f926f1a4c31f127b829bcb8056c851d58296`; `v2/ENNEAGRAM_EMERGENCE_SYSTEM.md` `95f8876926dda96a33c36925aedacee65645c74863cff68241e6b67457f819ab`; `v2/PROBABILISTIC_ENNEAGRAM_SYSTEM.md` `3a63f8caa258b5d00c4baa5bbe064eacf4b3a0fed3a83560dd2469d1b5654106`; `server/generation/simulation.py` `5d68ffe3bc6902dc60b90625443a03127cf0d04b4eed4327270a3a0226bc78d1`.

## 1. Exact as-built map

| Element | Source | Inputs / reads | Operation | Writes / outputs | Consumers |
|---|---|---|---|---|---|
| `PatternRange` / `EnneagramTypeWisdom` | `v2/enneagram_wisdom.py:21-40` | type wisdom patterns | ranges and probability density | static data | matcher |
| `match_life_course_to_type` | `v2/enneagram_wisdom.py:615-700` | life-course states 0–7, 7–14, 22+; context | matches early/child/adult patterns, strategies, indices; weights early 1.5×, child 1.2×, adult 1.0×; **adds `np.random.normal(0,5.0)`** and clamps | score 0–100 per type | probability computation |
| `_compute_enneagram_probabilities` | `v2/spec.py:3263-3315` | states; context; parent types | nine `match_life_course_to_type` calls; normalise; add parent-type effects; 0.02 floor; renormalise | type probabilities/scores | candidate/crystallise |
| `infer_enneagram_candidates` | `v2/spec.py:3319-3326` | states ages 0–6 | calls probabilities | `EnneagramCandidates` | pre-7 trajectory |
| `crystallize_enneagram` | `v2/spec.py:3328-3335` | states 0–7 | calls `infer_enneagram_from_life`, sets crystallization age 7 | `EnneagramProfile` | main loop at age 7 |
| `infer_enneagram_from_life` | `v2/spec.py:3338-3390` | states | probabilities; **`random.choices(types, weights=probabilities)`**; wing from adjacent scores; health level | `EnneagramProfile` | age 7 / end fallback |
| main loop | `v2/spec.py:2238-2270` | yearly states | age ≤6 candidates; age 7 crystallise; age >7 keep fixed type, update health only | `current_state.enneagram` | later loop |
| parent type inference | `v2/parent_type_inference.py:33-127` | warmth, authority, material support, gender, driver vector | fixed logit table for types 1–9; softmax | type probabilities | parent type |
| parent-type child effects | `v2/parent_type_inference.py:143-217` | father/mother type, trust | fixed identification/reaction/complementary adjustments | additive child type adjustments | `_compute_enneagram_probabilities` |
| parent type in server | `server/generation/simulation.py:350-435` | WVS-sampled parent behaviour | calls `infer_parent_type_most_likely` for father/mother; builds parent narrative/relations | parent types/narratives | parent narrative; v2 relational nodes |

**Correction to the M31 card's shorthand.** The implementation is not only an “end matcher”. It has:
1. a **crystallisation at age 7** from states 0–7 (`spec.py:2248-2251`), with the type fixed thereafter;
2. a fallback end matcher if no type exists (`spec.py:2375-2378`);
3. **random selection** of the primary type from the probability weights (`random.choices`, `spec.py:3360-3370`);
4. **random score variance** in each type match (`np.random.normal(0,5.0)`, `enneagram_wisdom.py:699`);
5. **fixed parent-type effects** and gender-coded heuristics;
6. **type-specific health-level constants** (`compute_health_level`, `spec.py:3187-3260`), including `type_resilience` and `buffer_multiplier`.

The design text says “no type at birth”; the implementation does not assign at birth, but it fixes a type at age 7 from the early trajectory. That is still an early typological closure, not a later optional description.

## 2. What this actually models, and what it does not

It models a **probabilistic pattern classifier** over life-course needs/strategies/indices, plus a parent-type inference layer. It does not model:

- a historically generated life-course attractor with explicit event/route evidence (the TD-R05 successor);
- an underdetermined, multi-label or non-label outcome;
- the difference between a descriptive label and a causal disposition;
- a parent's actual conduct; it infers parent type from behaviour/driver values and then imposes fixed child-type effects;
- actor-accessible self-interpretation;
- a prohibition on feedback from the label into later state (the label is attached to `PersonaState` and used in compensation/health).

The parent-type table is explicitly stereotyping: type 8 father → child type 4/8/2; type 5 mother → child type 5; type 1+9 pair → responsible child. These are fixed directional claims, not evidence-qualified actor history. The `material_support` argument to `infer_parent_type` is accepted but not used in the logit scores (only warmth/authority/driver values). The `infer_parent_type_most_likely` softmax always yields a most-likely type; there is no unknown/underdetermined outcome.

The server's current generation path uses parent type inference for parent narratives/relational nodes, not the child's v2 Enneagram crystalliser. The v2 crystalliser is historical engine code, not a proved current consumer. This distinction is essential: the presence of parent-type calls in `server/generation/simulation.py` does not prove a current C12 Enneagram integration.

## 3. Coverage and disposition

| Target | Coverage | Reason |
|---|---|---|
| N01 needs/motives/objects | `CONFLICTING` | a type label can feed compensation/health; it is not a need or object |
| N07 independent others/power/love | `CONFLICTING` | parent type is inferred from behaviour, then imposed on the child; no independent parent history |
| N12 actual C12 person | `UNKNOWN` | no current C9/C12 consumer; server does not run the child crystalliser |
| M31 card claim “no type at birth” | design true / implementation early closure | type crystallises at 7 and is fixed; random choice; parent effects |

**Disposition: REPLACE/REMOVE the causal type matcher.** If typology is retained at all, it must be an **optional, derived, non-causal descriptive label** over generated attractor evidence, with multiple/underdetermined outcomes allowed and no parent-type determinism. Remove the fixed parent-type child effects and the random score variance from any causal path. Do not use a type label to seed needs, capacity, health or later appraisal.

## 4. Harmful defaults / defects to remove

1. **Type crystallised at 7 and fixed thereafter**; no underdetermination.
2. **Random primary type** (`random.choices`) from probabilities; repeated runs can differ without new history.
3. **Random ±5 score noise** in each match; a green score is not a stable classification.
4. **Fixed gender/parent-type tables**; parent type → child type determinism.
5. **`material_support` ignored** in parent type logits, despite the signature.
6. **Type-specific health constants** (`type_resilience`, `buffer_multiplier`) feed health; the label becomes causal.
7. **Parent type inferred from WVS/default behaviour**, not actual parent conduct.
8. **Server parent type use** in narratives/relations, with no source/actor validation.

## 5. Proposed typed seam (nonissuing)

If retained at all:

```text
AttractorEvidence {
  actor_id; event/route/interaction refs; recurrence; reinforcement;
  destabilization; competing tendencies; uncertainty; rule_version;
}
OptionalTypologyLabel {
  actor_id; label(s)[]; evidence_refs[]; interpretation_rule;
  uncertainty; non_causal; no_state_feedback;
}
ParentConductEvidence {
  parent_id; event/action refs; warmth/coercion/care; source; clock;
}
```
The label is a derived interpretation over evidence, not an input to needs/health/capacity. Parent conduct is independently recorded; no parent-type table is a child cause. Multiple labels or “no label” are lawful.

**Owner:** a competent personality/developmental science issuer (not X05), CAN010/CAN011/ADP for any causal state, ADP016/017 for self-meaning, C9/C12 for consumer. **Not issued by X05.**

## 6. Counterexamples and hostile alternative

**Counterexample (same history, different type).** Two runs with the same life history but different random draws can select different primary types because of `random.choices` and the ±5 noise. If the label is descriptive, that is acceptable uncertainty; if it is causal, the state is randomized by a coin.

**Counterexample (parent type → child).** A warm, authoritative parent is classified type 8; the table boosts child type 8/4/2. The same parent conduct with a different gender can produce a different type. This is a fixed heuristic, not an actual parent-child history.

**Counterexample (type at 7).** A child with a stable early history crystallises at 7; later events cannot change the type. The design promise of life-course emergence is not met after age 7.

**Hostile alternative.** The type label may be a harmless description that never feeds a current consumer. The hostile test checks whether removing the type from `PersonaState` changes any current server/C9 output; if not, the historical type code is dead. If it changes only the historical v2 health/compensation, the label is causal in that old engine.

**Falsifier.** If two actors with identical current C9 inputs but different type labels produce different semantic outputs, the label is causally read. If a source-grounded attractor evidence record produces the same output while the label does not, the label is not needed.

## 7. Tests and limits

- Sourcefree X05 probe: `infer_parent_type_most_likely(85,45,20,'male') = 2`; `(30,80,80,'female') = 8`; `get_parent_type_effects_for_child(1,9)` = `{1:0.27, 7:0.025, 9:0.15}`. This confirms the fixed heuristic.
- Tests/entries read: `enneagram_wisdom.py`, `parent_type_inference.py`, `spec.py` main loop; `server/generation/simulation.py:350-435`.
- **NOT_RUN:** full v2 life-course; current C9/C12; native person; any empirical typology validation.
- **No native rule or source permission is issued.** X05 takes no position on the empirical validity of Enneagram typology; the finding is about source semantics and causality.

**Required future reviewer:** independent historical-source reviewer for M31; a competent personality/developmental science issuer; ADP/CAN owner for any causal use; current C9/C12 implementer. X05 does not self-adopt.
