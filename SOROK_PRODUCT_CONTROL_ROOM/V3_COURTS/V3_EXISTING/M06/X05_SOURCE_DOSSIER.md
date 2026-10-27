# M06 — multidimensional alienation: X05 direct-source dossier

**Court:** X05 historical source / material-actor-world bridge. **Evidence grade:** `HISTORICAL_SOURCE_AUDITED` plus executed sourcefree probe; `CURRENT_INTEGRATION: UNTRACED`; `THEORY: PROPOSED_NOT_ISSUED`; `AUTHORITY: NO_NATIVE_GRANT`.  
**Direct source:** `v3/core/state.py` `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`; `v3/systems/alienation.py` `2209d8171a14f18c252e847e2d0beb113d574e1378c49d2fb7e7f43513106207`; `v3/engine/alienation.py` `ad9f6ee25b2464e5055f65f1dd18e2b20fd9133255f41b45a0e9dc884741243e`; `v3/engine/effects/delta_templates.py` `7d99ddf26fd45b52e5e3c10074066ba5e06d17cdaf1fabad06298af3770815f0`.

## 1. Exact as-built map

| Element | Source | Inputs / state reads | Operation | State writes / outputs | Callers / consumers |
|---|---|---|---|---|---|
| `AlienationVector` | `v3/core/state.py:95-110` | four dimensions: `distant_others, near_others, self, moral_totality`; default 50 each | `aggregate()` = mean of four; clamp | stored `state.alienation_vector`; scalar `state.alienation` | JSON codec; `compute_mis_aim_risk`; persona sheet |
| `systems.update_alienation` (active yearly path) | `v3/systems/alienation.py:20-39` | `state.events_this_year[].alienation_delta`; annual cap 15 | sums delta, caps, computes `new_agg = vector.aggregate() + delta`, then assigns **`v.structural = v.affective = v.institutional = new_agg`** and `state.alienation = new_agg` | creates non-schema dynamic attributes `structural/affective/institutional`; real four dimensions unchanged | `_run_cracks_and_alienation` in `yearly_step.py:154-157` |
| `delta_templates.apply_deltas_to_state` (LLM/event path) | `v3/engine/effects/delta_templates.py:254-319` | merged `alienation_delta` | same wrong assignment: `v.structural = v.affective = v.institutional = new_agg`; `state.alienation = new_agg` | same phantom attributes; real vector unchanged | `run_llm_band` after candidate selection (`run_llm_band.py:264-271`) |
| `engine.derive_alienation` (correct but unwired) | `v3/engine/alienation.py:1-75` | domain `A/S/V`, domain `buffer_type`, `registers.inner_load`, `peak_routing.coherence`, `practice_stack.spiritual` | derives `distant_others`, `near_others`, `self`, `moral_totality`; keeps scalar in sync | real four dimensions | **no production caller** found; only `v3/tests/test_v5_alienation.py` |
| Consumed indirectly | `v3/core/derived.py:103-110` | `state.alienation` scalar | `mis_aim_risk = .40*alienation + .30*hostage + .30*organizing_deficit` | derived index | `stability_threshold`, `alignment_vector`, persona sheet warmth/connection |

**The active path is broken.** `AlienationVector` has no `structural`, `affective` or `institutional` fields. Python dataclasses without `slots` allow those attributes to be created dynamically, so the assignment does not raise. But `aggregate()` still averages the unchanged four real fields. `state.alienation` is set to `new_agg` only until the next `state.clamp_all()`, which recomputes it from `alienation_vector.aggregate()` (`state.py:568-570`; JSON load also does this at `json_codec.py:554`). In `run_one_year`, `clamp_after_each_step` defaults true, so the event delta is lost before the next step. The scalar is a transient.

**Sourcefree probe (X05):** starting with vector all 50 and `state.alienation=0`:
- event `alienation_delta=3.0`; after `systems.update_alienation`: scalar `53.0`, vector aggregate `50.0`, phantom attrs `53.0`;
- after `clamp_all()`: scalar `50.0`, vector unchanged.
This reproduces RX01's independent finding.

**Test artefact.** `v3/tests/test_step_logic.py:97-112` asserts `state.alienation == 30.0` immediately after `update_alienation` and does **not** call `clamp_all()`; it passes despite the vector being unchanged. `v3/tests/test_v5_alienation.py` tests the **unwired** `engine.derive_alienation`, not the active yearly path. A green test therefore does not establish the active mechanism.

**Initial scalar/vector mismatch.** `BackboneState.alienation` defaults to `0.0` while `AlienationVector` defaults to 50 on all four fields (`state.py:516-517`). The normal connector ends with `clamp_all()` (`identity_to_backbone.py:685`), which syncs the scalar to 50; but any construction that skips clamp has a 0 scalar and a 50 vector.

## 2. What this actually models, and what it does not

The bundle contains two incompatible ideas:

1. **A tenable derivational operator** (`engine/alienation.py`): estrangement from objective/actor-domain mismatches, buffer relational costs, inner load, coherence, spiritual practice. It is a candidate computational affordance, not a native rule.
2. **A broken event scalar updater** (`systems/alienation.py`, `delta_templates.py`): an `alienation_delta` that silently disappears, with phantom fields named after an older schema.

Neither models:
- estrangement from a **specific** relation, institution, activity, object or opportunity;
- actor-accessible estrangement versus analyst classification;
- a contradiction between a valued object and an actual social relation;
- a real other actor's power or care;
- the difference between “not knowing” and “not caring”.

The old vector dimensions (`distant_others/near_others/self/moral_totality`) are broad orientations. They are not target-specific alienation and do not carry a relation or event parent.

## 3. Coverage and disposition

| Target | Coverage | Reason |
|---|---|---|
| N01 needs/motives/objects | `MISSING` | no need/object operation; alienation is not a motive |
| N07 independent others/power/love | `PARTIAL_WRONG_MEANING` | relational estrangement is named, but no actual other actor or relation; active path loses deltas |
| N09 fallible memory/meaning | `INFRASTRUCTURE_ONLY` | scalar could be a derived view; no memory/access |
| N12 actual C12 person | `UNKNOWN` | no current C9/C12 consumer |

**Disposition: CONFLICTING → ADAPT/REPLACE.** Delete the phantom-field delta path. Preserve the four-dimensional schema **only** as a derived evidence view. Reuse the unwired `engine.derive_alienation` as a candidate operator after owner review. Create target-specific estrangement records parented by actual events/relations; no predeclared universal estrangement from demographic location.

## 4. Harmful defaults / defects to remove

1. **Phantom fields and silent delta loss** (`systems/alienation.py:36-39`; `delta_templates.py:314-319`).
2. **Scalar/vector split** (`state.alienation=0` vs vector=50); one authoritative representation or explicit cache.
3. **Active test passes before clamp**; test must assert after the same clamp boundary as `run_one_year`.
4. **Unwired correct operator**; deciding not to reuse it must be explicit, not by import accident.
5. **Broad estrangement presumed from social location**; no target-specific relation or event parent.
6. **`mis_aim_risk` reads a scalar** that may be stale or reset.

## 5. Proposed typed seam (nonissuing)

```text
EstrangementEvidence {
  actor_id; target_ref (person/institution/activity/object/self);
  relation_ref/event_ref; objective_relation; actor_access;
  discrepancy_kind; buffer_costs[]; inner_load_ref;
  value/meaning_ref; uncertainty; rule_version;
}
DerivedAlienationView {
  actor_id; dimensions[]; dependencies[]; source_event_refs[];
  computed_at; rule_version;
}
```
The evidence record must be parented by an admitted event/relation. The derived view recomputes from evidence and is never a causal store. The first legitimate C9/C12 consumer must read the **semantic estrangement** of the target relation, not a scalar hash or a phantom attribute.

**Owner:** CAN010/CAN011 for the actor relation/meaning; ADP015/ADP019 for relation/other actor; C9/C12 for read. **Not issued by X05.**

## 6. Counterexamples and hostile alternative

**Counterexample (test passes, mechanism lost).** The historical test asserts the scalar immediately after the update; a real year then clamps and loses it. This is a concrete positive: same code, different boundary, opposite conclusion.

**Counterexample (target specificity).** A person is estranged from a specific employer but not from “near others” generally. The old vector cannot represent this; a target-specific record can.

**Hostile alternative.** The unwired `engine.derive_alienation` may be the intended old mechanism, and the active path may be a wiring mistake. A hostile test calls the active yearly path and the unwired derivation on the same state, then checks which one changes the real vector and which one feeds `mis_aim_risk`. If only the unwired one works, the active path is not the mechanism.

**Falsifier.** If removing `systems.update_alienation` from the yearly spine leaves all downstream values identical (because deltas were lost anyway), the active path is causally inert. If adding target-specific evidence changes a later C9 semantic read while a scalar `alienation_delta` does not, the target record is the required seam.

## 7. Tests and limits

- Sourcefree X05 probe executed: delta loss confirmed; phantom attributes confirmed.
- Historical tests read: `test_step_logic.py:97-112`; `test_v5_alienation.py` (unwired operator).
- **NOT_RUN:** full old suite; current C9/C12; native person.
- **No native rule or source permission is issued.**

**Required future reviewer:** independent V3 source reviewer for M06; CAN010/CAN011 owner for target-specific estrangement/meaning; ADP015/019 for relation/other actor; current C9/C12 implementer. X05 does not self-adopt.
