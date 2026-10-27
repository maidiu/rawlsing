# M26 — stored-versus-derived separation: X05 direct-source dossier

**Court:** X05 historical source / material-actor-world bridge. **Evidence grade:** `HISTORICAL_SOURCE_AUDITED` plus sourcefree probe; `CURRENT_INTEGRATION: UNTRACED`; `THEORY: PROPOSED_NOT_ISSUED`; `AUTHORITY: NO_NATIVE_GRANT`.  
**Direct source:** `v3/core/state.py` `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`; `v3/core/derived.py` `e479fc3eba21734752c372742fb2ee247cbdde6a73ac42545dc30b5039301360`; `v3/core/invariants.py` `81298f3fc51b46cda8d72d0db914b672b17b9a35e13004fe59a9b0e29dada5e3`; `v3/io/json_codec.py` `c4bc07dd73c249c35d788f5b459f4b0c1b23702a7d55157a4eb3fdbc74b1cf14`.

## 1. Exact as-built map

| Element | Source | Inputs / state reads | Operation | Writes / outputs | Consumers |
|---|---|---|---|---|---|
| `DerivedIndices` | `v3/core/derived.py:14-31` | computed from stored state | dataclass of indices: hostage, AC, insulation, SL, mis_aim, peak, metabolic style, health, gaps, alignment, stability | returned to caller; not stored as a named field | `run_one_year` local variable; `year_record` derived dict |
| `compute_all_derived` | `v3/core/derived.py:322-359` | stored state (capacity, reproduction, domains, cracks, etc.) | computes derived values; **also writes** `state.metabolic_style` and `state.registers`; recomputes `state.alienation` only later via clamp | `state.metabolic_style`, `state.registers`; returns `DerivedIndices` | yearly runner; server |
| `assert_no_derived_fields_in_backbone` | `v3/core/invariants.py:15-23,346-354` | `BackboneState.__dataclass_fields__` | checks overlap with six names only: `hostage_index, agency_capacity_AC, insulation_score, structural_lucidity_SL, mis_aim_risk, peak_regime` | raises on those names | `test_architecture_invariants.py:123-126` |
| `compute_all_derived` docstring | `v3/core/derived.py:1-2` | — | says “Do not mutate state” | — | — |
| `state_to_dict` / `state_from_dict` | `v3/io/json_codec.py:400-554` | all dataclass fields | serializes `registers`, `metabolic_style`, `alienation`, `alienation_vector`; on load recomputes scalar from vector | full state dict | year records; store; persona sheet |
| `_compute_derived_after_step` | `v3/engine/yearly_step.py:173-200` | `derived_indices_schedule` vs step-local `derived_compute` | asserts the two declarations agree, then computes/copies scheduled fields | `DerivedIndices` | yearly runner |
| `backbone_hash` | `v3/core/invariants.py:338-343` | state dict minus `rendered_output` | stable hash for render non-mutation test | hash | render test |

**What is genuinely separated.** The six named indices are not stored as fields. `DerivedIndices` is a separate object. The derived schedule is explicit and fail-fast checked (`yearly_step.py:181-186`). `backbone_hash` excludes `rendered_output` for the render test.

**What is not separated.** `compute_all_derived` writes `state.metabolic_style` and `state.registers` (`derived.py:331-334`), both derived from stored state. `state.alienation` is a scalar cache of `alienation_vector.aggregate()`, and `state.alienation_vector` is stored. `state_to_dict` serializes all of these. The invariant only checks six names, so it does not catch `registers`, `metabolic_style`, or the scalar/vector duplication. The `compute_all_derived` docstring (“Do not mutate state”) is false for those two writes.

**Sourcefree probe (X05):** after `compute_all_derived`, serialized state contains `registers=True`, `metabolic_style=True`, `alienation=True`; none of the six protected names appears as a stored key. This is a partial, name-based separation, not a general derived-view invariant.

## 2. What this actually models, and what it does not

The code models an **engineering discipline**: don't store the six headline derived indices; recompute them; check schedule equivalence; protect render from mutation. It does not model:

- a dependency registry for every derived view;
- a versioned cache with recompute rules;
- a general rule that no derived quantity can be stored as causal truth;
- a distinction between a recomputable cache and a stored actor fact;
- an ownership/version for `registers`, `metabolic_style`, scalar `alienation`.

This is broadly compatible with Neo-V3 because it provides a real constitutional pattern. It needs an owner and a stronger rule, not a new psychology.

## 3. Coverage and disposition

| Target | Coverage | Reason |
|---|---|---|
| N11 sequential recursion (adjacent) | `INFRASTRUCTURE_ONLY` | no event/state split; schedule check only |
| N12 actual C12 person | `INFRASTRUCTURE_ONLY` | no current C9/C12 consumer; storage invariant only |
| N09 memory (adjacent) | `INFRASTRUCTURE_ONLY` | no memory |

**Disposition: REUSE the engineering invariant, with extension.** Do not accept “derived fields not stored” as proven globally. Add a derived-view registry with:
- owner, formula, dependencies, version, computed_at;
- explicit cache policy and recompute-on-load;
- no derived scalar may be read as causal truth without its evidence refs;
- one authoritative `alienation` representation (vector or scalar, not both);
- no hidden writes inside a “compute” function.

## 4. Harmful defaults / defects to remove

1. **Name-only invariant**: only six names checked; `registers`/`metabolic_style`/scalar alienation escape.
2. **Compute mutates state** despite docstring.
3. **Dual alienation representation**; scalar can be stale/0 while vector is 50.
4. **No derived-view version/dependency metadata** for stored caches.
5. **`state_to_dict` serializes caches as if they were stored facts**; reload may use stale cache instead of recomputing.
6. **`DerivedIndices` dict omits `registers`/`metabolic_style`** from the named derived object while state stores them; two parallel derived surfaces.

## 5. Proposed typed seam (nonissuing)

```text
DerivedViewSpec {
  view_id; owner; formula_ref; dependencies[]; version;
  cache_policy; recompute_on_load; permitted_consumers[];
}
DerivedViewValue {
  view_id; actor_id; value; source_state_hash; computed_at; rule_version;
}
```
The six named indices and any other derived value are instances of `DerivedViewSpec`. A stored cache is allowed only with `cache_policy` and `source_state_hash`; on load it is recomputed or marked stale. No C9/C12 consumer may read a cache without the spec.

**Owner:** C12/architecture (engineering); no scientific rule. **Not issued by X05.**

## 6. Counterexamples and hostile alternative

**Counterexample (stored derived).** Change `state.registers` directly and reload the serialized state; the stale value persists. A true derived-only architecture would recompute and discard it. The current code would not.

**Counterexample (dual alienation).** A state with `alienation=0` and `alienation_vector` all 50 serializes both; `state_from_dict` sets scalar to vector aggregate, but an in-memory constructed state can carry 0. `compute_all_derived` does not fix the scalar. Two copies, one truth.

**Hostile alternative.** Perhaps the stored registers/metabolic_style are intentional caches, not causal state. If so, the code must mark them as caches, version them, and recompute on load; otherwise they are indistinguishable from stored facts.

**Falsifier.** Add a field named `registers` to `DERIVED_INDEX_NAMES` or a general registry; if the invariant test still passes with a stale stored value, the separation is not enforced. Recompute a cache from a changed source state and compare; if the consumer reads the stale cache, it is a stored truth.

## 7. Tests and limits

- Sourcefree X05 probe: serialized `registers`/`metabolic_style`/scalar alienation present; six protected names absent.
- Historical test: `test_architecture_invariants.py:123-126` (name check only).
- **NOT_RUN:** full old suite; current C9/C12; native person.
- **No native rule or source permission is issued.**

**Required future reviewer:** independent V3 architecture/source reviewer for M26/N12; C12 storage owner; current C9/C12 implementer. X05 does not self-adopt.
