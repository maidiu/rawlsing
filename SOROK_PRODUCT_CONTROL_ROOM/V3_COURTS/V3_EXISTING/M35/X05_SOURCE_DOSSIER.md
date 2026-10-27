# M35 — placeholder crack/framework invariant repair: X05 direct-source dossier

**Court:** X05 historical source / material-actor-world bridge. **Evidence grade:** `HISTORICAL_SOURCE_AUDITED` plus sourcefree probe; `CURRENT_INTEGRATION: UNTRACED`; `THEORY: PROPOSED_NOT_ISSUED`; `AUTHORITY: NO_NATIVE_GRANT`.  
**Direct source:** `v3/core/invariants.py` `81298f3fc51b46cda8d72d0db914b672b17b9a35e13004fe59a9b0e29dada5e3`; `v3/engine/yearly_step.py` `da3147c3da7ff2724a61dd26d595055668899c83beb541400f58633568b92acb`; `v3/engine/llm_contract.py` `f024debf7b8a637e91c546689a0bed31baff55d98f1378b06cb82ebb4c0fe9cf`; `server/generation/simulation.py` `5d68ffe3bc6902dc60b90625443a03127cf0d04b4eed4327270a3a0226bc78d1`.

## 1. Exact as-built map

| Element | Source | Inputs / reads | Operation | Writes | Consumers |
|---|---|---|---|---|---|
| `ensure_min_cracks` | `v3/core/invariants.py:253-275` | `state.cracks`, `invariants.min_cracks` (default 2) | while count below min, append `Crack(type="placeholder", intensity=5.0, latent_pressure=5.0, active=True, origin_year=state.year)`; record `yearly_integrity.placeholder_counts.cracks` and `placeholder_repair.status="degraded"` | `state.cracks`, `state.yearly_integrity` | invariants; yearly runner; JSON/persona |
| `ensure_min_frameworks` | `v3/core/invariants.py:277-300` | active frameworks weight >0; min default 2 | append `Framework(id=f"placeholder_{len(state.frameworks)}", weight=5.0)`; record placeholder count/degraded | `state.frameworks`, `yearly_integrity` | invariants; framework update; LLM summary filtering |
| Call sites | `v3/engine/yearly_step.py:25-30,37-44` | `v3config.invariants.repair_min_counts=true` | before the yearly steps, ensure min; after `frameworks_update`, enforce caps then ensure min again | state | every year |
| LLM filter | `v3/engine/llm_contract.py:598-615` | frameworks/cracks | excludes IDs starting `placeholder` and crack type `placeholder` from Pass-1 summary | summary | LLM event proposal |
| Server diagnostics | `server/generation/simulation.py:623-657` | cracks/frameworks after year | counts placeholders; if any, marks year `integrity_level=degraded`, fallback reason includes placeholder counts | yearly integrity; generation diagnostics | readiness |
| Invariants | `v3/core/invariants.py:188-215,303-333` | cracks/frameworks | min-count assertions; placeholders can satisfy them | pass/fail | tests/court |

**What is already quarantined.** The current bundle does not send placeholder cracks/frameworks to the LLM (`llm_contract.py:598-615`) and marks placeholder repair degraded. It also includes placeholder counts in yearly integrity. Those are real improvements and should not be misdescribed as lived experience. TD-R05's correction is right: the exact bundle marks the repair degraded rather than laundering it into a real scene.

**What is still harmful.** The placeholders are still **substantive dataclass objects in causal state**:
- a `Crack(type="placeholder", intensity=5.0, latent_pressure=5.0, active=True)` is a crack object with a type string and active flag;
- a `Framework(id="placeholder_N", weight=5.0)` is an active framework object;
- `compute_metabolic_style` sums `intensity + latent_pressure` over all cracks, including placeholders (`derived.py:180-181`);
- the `assert_min_cracks`/`assert_min_frameworks` invariants are satisfied by manufactured objects;
- the placeholders are serialized and can be inspected by downstream code.

The `llm_contract` filter prevents the Pass-1 LLM from seeing them, and the server marks the year degraded. But the state still contains synthetic content with no event parent, no relation, no actor, and no source. The correct disposition is to keep diagnostics, not causal objects.

## 2. What this actually models, and what it does not

It models an **invariant repair scaffold**: if the state lacks the minimum number of cracks/frameworks, insert a placeholder so the invariant can pass. It does not model:

- an actual unresolved tension or prediction error (crack);
- a learned metabolic operator (framework);
- an event parent or source;
- an actor-accessible experience;
- a distinction between “not yet formed” and “placeholder”.

This is exactly the “manufactured internal content to satisfy invariants” the M35 card criticises. The current code adds a degradation marker, but that marker does not make the object non-causal; it only records that the causal object is fake.

## 3. Coverage and disposition

| Target | Coverage | Reason |
|---|---|---|
| N12 actual C12 person | `CONFLICTING` | ready/invariant state can be satisfied by non-causal placeholders |
| N05/N09 (adjacent) | `INFRASTRUCTURE_ONLY` | no real crack/framework or memory |
| M35 card “remove synthetic evidence” | correct | diagnostics may remain; causal objects must go |

**Disposition: REMOVE the placeholder causal objects. Keep diagnostic counts/degradation only.** If an invariant genuinely needs a minimum, it must be a **formation rule** that either produces a source-qualified object or returns valid-empty/missing-authority, not a synthetic object. A placeholder may be recorded as a diagnostic `PlaceholderEvent`, never as a `Crack`/`Framework`.

## 4. Harmful defaults / defects to remove

1. **Synthetic `Crack`/`Framework` objects** satisfy invariants with no event/source.
2. **Placeholder cracks contribute to crack load** in derived metabolic style.
3. **Placeholder frameworks are active for min-count purposes**; `enforce_framework_caps` keeps weight 5 (not <5).
4. **Placeholder repair can rerun every year** if no real objects form; yearly integrity repeatedly degraded.
5. **`llm_contract` filtering is a downstream band-aid**; the fake objects remain in state/JSON.
6. **No distinction between missing formation rule and valid no-change**; the invariant forces content.

## 5. Proposed typed seam (nonissuing)

```text
PlaceholderDiagnostic {
  year; kind (crack/framework); count; reason (missing_formation_rule);
  source_state_hash; no_causal_object_created; severity;
}
FormationResult {
  status = FORMED | VALID_EMPTY | HELD_MISSING_RULE | CONFLICTING;
  object_refs[]; source_event_refs[]; rule_version;
}
```
`FormationResult` is the only way to create a crack/framework. `VALID_EMPTY`/`HELD_MISSING_RULE` are lawful; the system must not manufacture an object to satisfy a count. `PlaceholderDiagnostic` may be retained in `yearly_integrity`, never in `state.cracks`/`state.frameworks`.

**Owner:** CAN011/CAN010 and the current C9/C12 implementer for crack/framework formation; C12 architecture for diagnostics. **Not issued by X05.**

## 6. Counterexamples and hostile alternative

**Counterexample (placeholder becomes load).** A state with one real low crack and one placeholder crack has `compute_metabolic_style` crack_load including both. The placeholder can shift `contradiction_load` and thus the metabolic style. It is not only a diagnostic.

**Counterexample (invariant satisfied by fabrication).** Remove all real cracks and frameworks; `ensure_min_cracks/frameworks` inserts placeholders, and `assert_min_*` passes. A court that reports “invariants pass” has not shown that any real tension/operator exists.

**Hostile alternative.** The placeholders may be a harmless debug scaffold because the LLM filter hides them and the year is marked degraded. That is true for the LLM/readiness surface, but not for any code that reads `state.cracks`/`state.frameworks` directly. A hostile test checks `compute_metabolic_style`/framework operators with and without placeholders; if they differ, the scaffold is causal.

**Falsifier.** Replace placeholder objects with a diagnostic-only record and assert that yearly behavior (excluding explicit placeholder counts) is unchanged; if it changes, the placeholders were causal. If a missing formation rule returns `VALID_EMPTY` and downstream consumers treat that as missing rather than zero/no-change, the invariant is correctly relaxed.

## 7. Tests and limits

- Sourcefree X05 probe: starting with one real crack/framework, `ensure_min_cracks/frameworks` added one placeholder each, marked `placeholder_counts` and `placeholder_repair.status="degraded"`.
- Tests read: `test_invariants.py` (default state repair); `test_architecture_invariants.py` (state invariants); `test_step_logic.py` (framework/crack updates).
- **NOT_RUN:** full old suite; current C9/C12; native person.
- **No native rule or source permission is issued.**

**Required future reviewer:** independent V3 source/consumer reviewer for M35; CAN011/CAN010 owner for any crack/framework formation; current C9/C12 implementer. X05 does not self-adopt.
