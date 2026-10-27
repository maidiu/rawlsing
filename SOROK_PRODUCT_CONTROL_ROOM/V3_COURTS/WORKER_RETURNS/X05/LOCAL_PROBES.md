# X05 local sourcefree probes

**Date:** 2026-10-26. **Source:** `/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging` (read-only). **Method:** `python3 -B` with `PYTHONDONTWRITEBYTECODE=1`; no source edit, no LLM/provider call, no raw respondent data, no production code. These are **sourcefree arithmetic/state probes**, not native-person runs.

## P1 — selected source identities and archive distinction

```text
manifest archive_sha256: 953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086
selected_sources: 31; matched: 31; mismatched: 0
local staging zip sha256: 3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289
```

Result: whole-ZIP identity **does not match** TD-R05; selected file identities **do match**. File-level hashes are in `SOURCE_IDENTITIES.json`. This is consistent with RX01/RX02.

## P2 — alienation active path loses delta; phantom fields

```python
s=BackboneState(year=2000, age=10)
d=compute_all_derived(s)
# initial scalar 0.0, vector aggregate 50.0
s.events_this_year=[{'alienation_delta': 3.0}]
update_alienation(s,d,{})          # systems.update_alienation
# scalar 53.0, vector aggregate 50.0, phantom structural/affective 53.0
s.clamp_all()                      # run_one_year clamps after each step
# scalar 50.0, vector aggregate 50.0
```

Result: the active yearly `systems/alienation.py` path does **not** change the real four dimensions; the scalar is reset by clamp. `AlienationVector` has no `structural/affective/institutional` fields. The historical test asserts before clamp and therefore passes. The correct `engine/alienation.py` derivation is **not imported** by `yearly_step.py`.

## P3 — duplicate hostage formulas

State: dependents 40, housing 50, legal_status 20, debt 30, job 60, caregiving 70.

```text
compute_hostage_index (derived.py, weights sum 1.0) = 52.5
_derive_hostage_index (gating.py, weights sum 2.15) = 100.0
```

Result: same state, two different “hostage” values; the private gate saturates. No owner/declaration in source.

## P4 — capacity and reproduction caps

```text
event capacity_deltas money=-100, time=-100 from 50
after update_capacity: money=30, time=30          # per-field cap 20
event reproduction_deltas debt=+100, job_insecurity=-100
after update_reproduction_constraints: debt=20, job_insecurity=0
```

Result: per-field annual caps, as source states. This is arithmetic, not actual work/care feasibility.

## P5 — `compute_all_derived` writes stored-derived fields

```text
serialized state keys: registers=True, metabolic_style=True, alienation=True
protected derived names: none stored
```

Result: M26 separation is partial. `compute_all_derived` mutates `state.registers`/`state.metabolic_style`; the invariant checks only six names.

## P6 — placeholders satisfy invariants and mark degraded

Start with one real crack and one real framework; call `ensure_min_cracks`/`ensure_min_frameworks`.

```text
cracks: [('real',5.0), ('placeholder',5.0)]
frameworks: [('real',5.0), ('placeholder_1',5.0)]
yearly_integrity: {
  'placeholder_counts': {'cracks': 1, 'frameworks': 1},
  'placeholder_repair': {'status': 'degraded',
                         'reasons': ['placeholder_cracks_required','placeholder_frameworks_required'],
                         'added': 2}
}
```

Result: current bundle records degradation and filters placeholders from the LLM summary, but still inserts causal objects. See M35.

## P7 — v5 inert carrier and green gate

```text
attach_v5_runtime_input_bundle(status='green', refs=['r1'], payload={'economy':42})
snapshot status=green, refs=['r1'], bundle payload economy=42
green bridge injection: economy=42.0, fear=10.0, _integrity=ok
blocked bridge injection: no numeric fields, _integrity=blocked
```

Result: the carrier and bridge constructor are real and green-gated. **However**, `systems/field.update_field` applies any numeric `config["field_injection"]` regardless of `_integrity`; a blocked v5 bridge merged with existing numerics can leave those numerics applied. See M32.

## P8 — magnets drop `who`; lexical practice side effect

```text
selected candidate {'id':'m1','label':'music mentor','magnet_type':'mentor','who':'Ms X','intensity':70}
stored Magnet(id='m1', magnet_type='mentor', label='music mentor', intensity=70.0, tenure_years=0)
# `who` absent
after one decay with susceptibility 10: intensity 67.74
```

```text
active magnets: music studio (scene), teacher (mentor), community movement (scene)
before health_drift: practice_stack study=0, craft=0, organizing=0
after health_drift: study=1, craft=1, organizing=1
```

Result: `Magnet` has no actor/entity reference; `who` is dropped by `_candidate_to_magnet`; magnet label keywords directly add practice points. See M20.

## P9 — parent-type heuristic

```text
infer_parent_type_most_likely(85,45,20,'male') = 2
infer_parent_type_most_likely(30,80,80,'female') = 8
get_parent_type_effects_for_child(1,9) = {1:0.27, 7:0.025, 9:0.15}
```

Result: fixed gender/parent-type logit table and fixed child-type effects. `material_support` is accepted but not used in the logit scores. See M31.

## Limits

- These probes do not execute the full historical test suite, current S39–S52, current C9/C12, Pyat, or any native person.
- No probe result is a scientific law, a native source grant, or a production acceptance.
- The probes were run locally read-only; no source file was modified.
