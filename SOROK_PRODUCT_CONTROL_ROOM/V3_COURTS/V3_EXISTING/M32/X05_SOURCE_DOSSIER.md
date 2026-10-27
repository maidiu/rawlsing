# M32 — old V5 runtime-input / field-injection bridge: X05 direct-source dossier

**Court:** X05 historical source / material-actor-world bridge. **Evidence grade:** `HISTORICAL_SOURCE_AUDITED` plus sourcefree probe; `CURRENT_INTEGRATION: UNTRACED`; `THEORY: PROPOSED_NOT_ISSUED`; `AUTHORITY: NO_NATIVE_GRANT`.  
**Direct source:** `v3/io/v5_bridge.py` `31700b4031a62b0b5ff8257691e460ce47c983f86daaec72f1011bd6f2823baa`; `v3/io/v5_field_bridge.py` `444ed1e074439d006d341808386ca31e0616ac99ce11f5b99f9d101791ff9eea`; `v3/io/field_injection.py` `d3750fdb61eb73471612cad5c7d7c530da9519c93469a17f4f70a9b2505df0aa`; `v3/systems/field.py` `5f8fdc46153ce10c1a76618c596b7f7d486e8887e084e00fa128b90c94e8c411`.

## 1. Exact as-built map

| Element | Source | Inputs / reads | Operation | Writes / outputs | Consumers |
|---|---|---|---|---|---|
| `normalize_v5_runtime_input_bundle` | `v3/io/v5_bridge.py:40-75` | `bundle` mapping, status/refs/notes | normalise status (`not_attached/attached/degraded/blocked/green`), refs, notes, payload; copy source/provenance | inert dict | attach |
| `attach_v5_runtime_input_bundle` | `v3/io/v5_bridge.py:78-91` | state, bundle | attaches metadata only | `state.v5_runtime_input_bundle`, `v5_runtime_input_refs`, `v5_bridge_status` | state/JSON; no numeric mutation |
| `v5_bridge_snapshot` | `v3/io/v5_bridge.py:94-100` | state | read-only status/refs/bundle | snapshot dict | diagnostics |
| `build_v5_field_bridge_injection` | `v3/io/v5_field_bridge.py:35-73` | v5 bridge mapping; green statuses `ok/green/attached`; field keys | extracts numeric field values; **empties numerics if status not green**; emits `_integrity` and `_provenance` | injection dict | field update |
| `build_field_injection_from_harmonization` | `v3/io/field_injection.py:182-215` | world_slice, driver_vec, civic_soul, imperial_block, driver_model, v5 bridge | merges sources; later sources override earlier; v5 numerics appended | `field_injection` dict | field update |
| `merge_field_injection` | `v3/io/field_injection.py:116-179` | world_slice/driver_vec dicts | merge; conflict provenance; status `ok/degraded/failed` | injection with `_integrity` | field update |
| `get_field_injection` / `_for_year` | `v3/io/field_injection.py:218-280` | country/year/age/gender | world_slice + driver_vec via v2 data_access; integrity on failure | injection dict | server per-year |
| `update_field` | `v3/systems/field.py:14-123` | `config.field_injection`, `config.v5_field_bridge`, event `field_deltas` | merge v5 into injection; **apply every numeric injection value**; then apply event deltas; record provenance | `state.field.raw`, `field.provenance`, `yearly_integrity.field_injection` | field consumers |
| Test | `v3/tests/test_v5_blocked_bundle_does_not_change_field_values.py` | blocked bundle | asserts no state change except bridge metadata | test | architecture check |

**Inert-carrier law is real.** `attach_v5_runtime_input_bundle` does not mutate any numeric/psyche field; the test exercises that. `build_v5_field_bridge_injection` correctly strips numeric values for a blocked bridge. This is the valuable seam TD-R05 and M32 identify.

**Failure/defect.** `update_field` does **not** fail closed on the injection's integrity. It applies every numeric key in `config["field_injection"]` regardless of `_integrity.status` (`field.py:54-78`). If a blocked v5 bridge is merged with an existing injection that already has numeric values, the merge keeps those existing numerics and overwrites the integrity to `blocked`; the numerics are still applied. A non-green, non-empty injection from another source can also apply numbers while `yearly_integrity` records `failed/degraded`. The green gate is in the v5 bridge constructor, not in the field consumer.

Also:
- the old V5 payload uses stage-specific `economy/repression/...` field keys; there is no actor, world entity, clock or source-authority binding;
- conflict handling in `merge_field_injection` records provenance but still chooses `driver_vec`; no owner decision;
- `get_field_injection` failure returns integrity but no numerics; a caller may still pass an empty/degraded injection; field update records degraded but does not block other numeric sources.

## 2. What this actually models, and what it does not

It models a **typed inert carrier** for an external runtime bundle (status, refs, payload, provenance) and a **green-gated field projection** of eight legacy field keys. It does not model:

- a current V558 repository/resolver context or structural world authority;
- actor/institution entity refs, clocks or rights;
- a temporal binding from a source fact to a person's year;
- a fail-closed merge at the field consumer;
- a distinction between a source fact and a stage-specific V5 projection.

The carrier is useful; the old V5 identity/projection is obsolete. The field consumer is not safe enough to call “green-gated numeric use” at the end-to-end level.

## 3. Coverage and disposition

| Target | Coverage | Reason |
|---|---|---|
| N12 actual C12 person | `INFRASTRUCTURE_ONLY` | carrier/gating/provenance only; no current C9/C12 consumer |
| N06/N07 | none / indirect | field aggregates are not actual actors or activity |
| M32 card “green-gated” | true at bridge constructor, false at field consumer | blocked bridge plus existing injection can still apply numbers |

**Disposition: ADAPT.** Keep the inert carrier, status/refs/provenance and green gate. Replace the stage-specific V5 payload with a current structural-world/source binding (entity refs, clock, rights, rule/version). Make `update_field` fail closed on `_integrity.status != ok/green` unless an explicit owner permits a degraded partial use. Do not force world facts through legacy stratum/psyche classifications.

## 4. Harmful defaults / defects to remove

1. **Field consumer ignores integrity status**; numerics can apply on `failed/degraded/blocked`.
2. **Blocked bridge + existing injection** keeps existing numerics; the blocked status is recorded but not enforced.
3. **Old V5 stage-specific payload** is not a current world authority.
4. **No entity/actor/clock/rights binding.**
5. **Conflict resolution by source order** (`driver_vec` overrides) without owner/rule.
6. **`field.raw` default 50** when a delta targets an absent key (`field.py:108`), another missing-as-midpoint default.
7. **No typed uncertainty** for missing source fields; only `_integrity`.

## 5. Proposed typed seam (nonissuing)

```text
SourceBoundWorldInput {
  source_id; source_authority; entity_refs[]; clock_start/end;
  payload; units; provenance; integrity_status; version;
  permitted_consumers[]; unknown_fields[];
}
FieldInjectionDecision {
  input_ref; status; numeric_values; conflict_report;
  accepted_by_rule; rejected_reason;
}
```
`FieldInjectionDecision` is the only object the field consumer may apply. It rejects all numeric values unless the input status is explicitly green/ok under an issued rule. The decision cites the exact source authority and clock; it does not collapse V5 strata into field scalars.

**Owner:** current structural-world/SDTF authority; C8/ADP019 for actor/world; C9/C12 for consumer; C12 architecture for the carrier. **Not issued by X05.**

## 6. Counterexamples and hostile alternative

**Counterexample (blocked bridge still leaks).** Start with a field injection containing `economy=42` from a `world_slice`, attach a blocked v5 bridge with `economy=99`, call `update_field`. The merge keeps 42 and labels integrity blocked; the field raw still becomes 42. The bridge did not introduce 99, but the consumer applied a non-green injection. A fail-closed consumer would reject all numerics or require per-source status.

**Counterexample (old V5 category).** A V5 `repression_baseline` scalar becomes `field.raw.repression_baseline`; it cannot name the institution, agent, target or period of repression. A current C9 encounter cannot resolve the source.

**Hostile alternative.** The observed field value may come from the world_slice/driver_vec path, not the V5 bridge. A hostile test uses only a blocked V5 bridge with no other injection; numerics are correctly empty. The defect is in the merge/consumer, not the carrier.

**Falsifier.** If removing all numeric injection values but leaving a green carrier changes no current consumer output, the bridge is not the world source. If a blocked carrier plus existing numerics still changes field raw, the consumer is not green-gated.

## 7. Tests and limits

- Sourcefree X05 probe: green carrier `economy=42/fear=10` → injection with `_integrity=ok`; blocked carrier → no numeric fields, `_integrity=blocked`; attach does not mutate state.
- Historical tests read: `test_v5_blocked_bundle_does_not_change_field_values.py`; `test_connector_and_field_injection.py` (integrity); `test_v5_runtime_bundle_json_roundtrip.py`.
- **NOT_RUN:** full old suite; current structural world; current C9/C12; native person.
- **No native rule or source permission is issued.**

**Required future reviewer:** independent V3 source/consumer reviewer for M32/N12; current world/SDTF authority; ADP019/C8; current C9/C12 implementer. X05 does not self-adopt.
