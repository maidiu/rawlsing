# CAN-014 — V3 Pure Derived-State Schedule Authority

**Authority ID:** `V3_PURE_DERIVED_STATE_SCHEDULE`  
**Authority version:** `1.0.0`  
**Canonicalization ID:** `CAN-014` / `CDP-CAN-014`  
**Owner:** `V3`  
**Status:** `CANONICALIZED`  
**Authority class:** `AUTHORITY_NEEDS_CANONICALIZATION`  
**Whole-machine architecture:** `CLOSED`  
**Production code modified:** `NO`  
**Historical archive authority:** continuity / authority-recovery evidence only; recovered V5/DDM has zero authority over current V550+.

## 1. Binding disposition

This authority binds the recovered V3 **pure derived-state schedule** as one versioned machine contract. It preserves the recovered stored-versus-derived separation, the ordered derived-publication checkpoints, full recomputability, and fail-fast schedule-consistency law while removing legacy ambiguity about which declaration is authoritative.

It does **not** define causal event scheduling, slow cadence, hybrid trigger precedence, causal mutation rules, V2 rendering/session scheduling, derived formulas not otherwise governed, or any new causal meaning.

The constitutional split is:

```text
stored / checkpointed V3 causal truth
        ↓ exact frozen state identity
pure deterministic derived evaluation
        ↓
versioned DerivedActorView / derived-field stamps
        ↓ read-only input where separately governed causal rules permit
causal mutation only through those separately governed rules/events
```

`DerivedActorView` is recomputable materialization. It is not a `DevelopmentalEvent`, not a checkpoint, not objective causal history, and not a render/session artifact.

## 2. Governing evidence and authority rank

### 2.1 Current binding authority inspected

- `state/CURRENT_STATE.md`;
- `integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`;
- `integration/IMPLEMENTATION_RELEASE_SYNTHESIS_RULING.md`;
- `integration/V3_COMPLETION_IMPLEMENTATION_RULING.md`;
- RA-R00 `RESULT.md` and `RESULT.json`;
- TD-R05 `RESULT.md`.

These establish that:

1. the whole-machine architecture is closed;
2. V3 causal scheduler (`MUST-021`), V3 pure derived schedule (`CAN-014`), and V2 render/session scheduling are separate authorities;
3. `CAN-014` is V3-owned, release-blocking, and consumed by V3-P3 and V3-P4;
4. recovered derived scheduling is an adaptation/preservation target, not legacy sovereignty;
5. derived views are not events and may not become hidden causal mutation.

### 2.2 Required historical archive directly verified

Archive supplied for this court:

```text
Rawlsing_code_bundle_staging.zip
SHA256 = 953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086
SHA verdict = EXACT_MATCH
```

Directly inspected recovered evidence:

| Recovered path | SHA256 | Authority-recovery finding |
|---|---|---|
| `v3/v3_yearly_step_order.yaml` | `90496a2cc852ca00ef99c8bd4fcb2b41c9aa43c4aaa9108d3ac8cce0ebe22ffc` | top-level 14-entry derived schedule; seven ordered publication checkpoints; annual cadence is legacy execution metadata only |
| `v3/engine/step_runner.py` | `5a737c1704eaa6dc2c67f6c2db3118a6daa8a213b44d559bc37eadbc9c09d95a` | full derived recomputation before the legacy run loop |
| `v3/engine/yearly_step.py` | `da3147c3da7ff2724a61dd26d595055668899c83beb541400f58633568b92acb` | per-checkpoint full candidate recomputation, selective publication, and top-level-vs-local declaration equality assertion |
| `v3/core/invariants.py` | `81298f3fc51b46cda8d72d0db914b672b17b9a35e13004fe59a9b0e29dada5e3` | derived indices are not stored backbone fields; fail-fast invariant posture |
| `v3/core/derived.py` | `e479fc3eba21734752c372742fb2ee247cbdde6a73ac42545dc30b5039301360` | recovered derived outputs and complete-candidate evaluation; also exposes legacy side effects that this authority rejects |
| `v3/core/config_loader.py` | `5f953d9661f61081187898c3ad06b4567bc4fa99d3d7cd856d30cdd961f78577` | legacy empty/fallback behavior is implementation evidence, not canonical authority |
| `v3/tests/test_architecture_invariants.py` | `bb2baec1c57de169a2e1e05533b9721b4b05191403ff4993d61df17ac29d05fa` | stored-versus-derived and explicit-order invariants are test-protected historically |

Direct mechanical inspection of the recovered YAML found `14` schedule entries, no top-level/step-local consistency mismatches, and each logical output assigned exactly once across the seven recovered checkpoints.

### 2.3 Current V3 source/tests terrain

At exact base `655da47b9e03ab310ed4b7fa65ceec9b9d04d3bc`, the repository contains the accepted V3 rulings/recalibration and V3-facing upstream boundary tests, but no current production `v3/` runtime source tree implementing the terminal V3 engine. No absent current implementation is inferred or manufactured. Historical V3 code therefore supplies continuity evidence only; this file is the machine authority for this bounded schedule meaning.

## 3. Jurisdiction

### 3.1 This authority owns

- stable identity/version of the V3 pure derived-state schedule;
- the recovered seven-checkpoint derived-publication order;
- the exact logical outputs assigned to each checkpoint;
- initial/full recomputation semantics;
- frozen input-state identity requirements;
- per-output freshness/provenance requirements for incrementally materialized views;
- schedule declaration consistency checks;
- cycle/duplicate/unknown handling for the derived schedule contract;
- cache/recomputation/replay/hash obligations;
- legacy compatibility validation for recovered schedule declarations;
- fail-fast behavior when the derived contract is ambiguous or inconsistent.

### 3.2 This authority does not own

- when a causal event, phase boundary, context-change trigger, or slow tick fires;
- precedence among causal triggers;
- the duration of a slow cadence;
- annual timestep as ontology;
- event sampling or event caps;
- any causal state-transition formula;
- any derived formula not already governed elsewhere;
- actor initialization, position generation, encounter/exposure, memory, attractor transition, external-event admission, or randomness policy;
- V2 render/session timing or transcript persistence;
- structural V550+ semantics.

`ADP-021` / `MUST-021` later owns hybrid causal trigger precedence and slow cadence. It may consume this authority but may not silently redefine the schedule.

## 4. Canonical machine identity

```text
authority_id      = V3_PURE_DERIVED_STATE_SCHEDULE
authority_version = 1.0.0
canonicalization  = CAN-014
owner             = V3
schedule_kind     = PURE_DERIVED_STATE_PUBLICATION_SCHEDULE
```

There is no implicit `latest`. A consumer MUST request/record the exact authority ID and version. Unknown versions fail closed.

## 5. Inputs and admissible source classes

A derived evaluation receives only a frozen, content-addressed V3 stored-state snapshot plus exact evaluator/config identities already governed outside this schedule.

Required input identity:

```text
StoredStateRef {
  state_schema_id
  state_schema_version
  state_version_id
  state_content_sha256
}
```

`state_version_id` is an opaque identity assigned by the V3 causal/checkpoint authority. CAN-014 does not define how causal versions advance.

Admissible semantic input class:

- fields lawfully present in that frozen stored causal-state snapshot.

Admissible nonsemantic control inputs:

- exact `V3_PURE_DERIVED_STATE_SCHEDULE@1.0.0` identity;
- exact derived-evaluator set ID/version/content hash;
- exact governed config/rule identities required by that evaluator set.

Forbidden direct inputs:

- mutable wall clock;
- filesystem enumeration/order;
- mutable `latest` pointers;
- V2 render/session/transcript material;
- unadmitted proposals or LLM text;
- stale derived cache as if it were stored truth;
- direct raw-stage/V550+ filesystem lookup;
- direct structural-prior substitution for actor state where the recovered schedule expected stored state;
- unnamed randomness. Pure derived evaluation uses no RNG.

Missing/unknown required inputs are not coerced to `0`, `50`, empty collections, false, or any other semantic default by this authority.

## 6. Canonical ordered derived schedule

The canonical schedule has seven ordered **derived-publication phases**. The `legacy_anchor` column records the recovered causal-step anchor for compatibility. These anchors do not schedule themselves and do not define slow cadence.

| Order | Phase ID | Legacy anchor | Logical outputs published |
|---:|---|---|---|
| 1 | `D01` | `reproduction_constraints_update` | `hostage_index` |
| 2 | `D02` | `capacity_update` | `agency_capacity_AC` |
| 3 | `D03` | `health_drift_update` | `health_level` |
| 4 | `D04` | `buffers_update` | `insulation_score` |
| 5 | `D05` | `domains_update` | `structural_lucidity_SL` |
| 6 | `D06` | `cracks_and_alienation_update` | `mis_aim_risk`, `metabolic_style` |
| 7 | `D07` | `topology_and_boundary_update` | `autonomy_gap`, `safety_gap`, `gap_pressure_index`, `alignment_vector`, `stability_threshold`, `peak_regime`, `che_jesus_eligible` |

`metabolic_style` is one logical scheduled output with the recovered materialized view fields:

```text
metabolic_style_current
metabolic_style_trend
```

No other output is silently added to this schedule.

### 6.1 Schedule-order law

When the legacy-compatible incremental derived schedule is used, phases execute in exact `D01 → D02 → D03 → D04 → D05 → D06 → D07` order. No consumer may infer a different order from source-file position, dictionary iteration, module import order, or incidental runtime order.

This is derived-publication ordering only. It is not a decision that the corresponding causal mutation anchors happen annually, at all, or with any specific precedence among external events/context changes/developmental boundaries. Those causal scheduling decisions remain outside CAN-014.

## 7. Recompute and publication semantics

### 7.1 Initial/full recompute

Before a derived consumer reads the view for a newly materialized stored-state snapshot, V3 MUST be able to perform an atomic `FULL_RECOMPUTE` from that exact frozen snapshot.

A full recompute:

1. reads the frozen stored-state snapshot only;
2. evaluates the complete versioned derived evaluator set deterministically;
3. performs no causal-state writes;
4. publishes all canonical derived outputs with one exact `StoredStateRef`;
5. records the schedule/evaluator identities and a canonical output hash.

### 7.2 Incremental phase publication

The recovered runner recomputed a complete candidate derived set at each scheduled checkpoint, then copied only the fields assigned to that checkpoint. That semantic is canonicalized.

For each invoked `Dxx` phase:

1. freeze the exact post-mutation stored-state snapshot supplied by the separately governed causal runtime;
2. compute a complete candidate derived set from that snapshot using the exact evaluator-set identity;
3. publish only the logical outputs assigned to that phase;
4. stamp every published output with the exact source-state identity, phase ID, authority version, and evaluator identity;
5. leave other derived fields unchanged until their own governed publication phase or a full recompute.

The derived view may therefore contain fields refreshed from different causal-state versions during an incremental sequence. That mixed freshness MUST be explicit in per-output stamps; it may never masquerade as one coherent single-snapshot full view.

A consumer requiring a coherent all-fields view from one state version MUST demand `FULL_RECOMPUTE` and verify a single shared `StoredStateRef` across all fields.

### 7.3 Derived evaluation is pure

Derived evaluation may create/replace derived-view materialization only. It MUST NOT write any field in `ActorCausalState`, append a `DevelopmentalEvent`, advance a causal cursor, alter a checkpoint, or generate an externally observable causal fact.

Recovered `compute_all_derived()` writes `state.metabolic_style` and `state.registers` as side effects. Those writes are explicitly **NONCANONICAL LEGACY IMPURITY** under terminal V3. CAN-014 preserves `metabolic_style` as a derived-view output; it does not authorize backbone mutation. `registers` are not in the recovered 14-entry schedule and are not silently promoted by this authority. Any causal/stateful register semantics require separate authority.

## 8. Stored-versus-derived law

The following is binding:

```text
stored causal state != derived view != causal event history
```

- Canonical derived outputs are recomputable from their exact frozen input state and evaluator identities.
- Derived outputs are not authoritative stored causal fields merely because an implementation caches them.
- A cache is optional optimization only and cannot alter semantics.
- A derived value may influence later causal mutation only when a separately governed causal rule explicitly reads it and records the resulting causal transition/event under that rule's authority.
- Recomputing, invalidating, replacing, or deleting a derived cache does not itself alter causal truth.
- Replay of causal truth cannot depend on whether a derived cache happened to be persisted.

## 9. Derived-view identity and freshness

Each materialized logical output MUST carry or be losslessly attributable to:

```text
DerivedFieldStamp {
  logical_output_id
  phase_id
  source_state_ref
  authority_id
  authority_version
  evaluator_set_id
  evaluator_set_version
  evaluator_set_sha256
}
```

A materialized view MUST additionally expose:

```text
DerivedViewIdentity {
  view_kind = "V3_DERIVED_ACTOR_VIEW"
  authority_id
  authority_version
  field_stamps
  canonical_view_sha256
  coherence = "SINGLE_STATE_FULL" | "MIXED_STATE_INCREMENTAL"
}
```

`canonical_view_sha256` is computed over canonical serialization of the derived values plus their ordered provenance stamps. It is not a causal-event hash.

## 10. Consistency and failure law

### 10.1 One canonical declaration

`V3_PURE_DERIVED_STATE_SCHEDULE@1.0.0` is the schedule authority. Legacy or implementation-local declarations are generated/check-only compatibility surfaces.

No precedence rule resolves disagreement between duplicate declarations. Disagreement is an integrity error.

### 10.2 Fail-fast conditions

The schedule MUST reject before derived values are admitted for consumer use if any of the following occurs:

- duplicate logical output ID;
- one logical output assigned to more than one phase;
- missing canonical logical output;
- undeclared extra scheduled output;
- unknown phase ID;
- phase order mismatch;
- legacy top-level schedule vs step-local declaration mismatch;
- duplicate local declaration even if set equality would otherwise hide it;
- evaluator-set ID/version/hash missing or mismatched;
- required input-state identity/hash missing or mismatched;
- mutable/implicit `latest` schedule or evaluator selection;
- derived dependency cycle in the selected evaluator set;
- side effect on causal state during derived evaluation;
- use of RNG/wall clock/filesystem order in derived evaluation;
- stale cache key presented as current;
- same exact input/evaluator/authority identity producing a different canonical output hash on replay.

Canonical failure class:

```text
DERIVED_SCHEDULE_INTEGRITY_FAILURE
```

No fallback schedule, filesystem order, source-code order, empty schedule, first-N-step fallback, stale cache, or guessed default may be substituted.

### 10.3 Missing and deferred states

Control/status states are distinct from semantic derived values:

- `DERIVED_READY` — requested output is fresh and provenance-valid;
- `DERIVED_DEFERRED_NOT_REQUESTED` — its canonical phase has not been requested since the relevant causal state change; not usable where freshness is required;
- `DERIVED_STALE` — a prior materialization exists but its stamp does not satisfy the consumer's required state identity;
- `DERIVED_BLOCKED_MISSING_INPUT` — required stored input/identity is absent or unknown;
- `DERIVED_BLOCKED_MISSING_EVALUATOR` — exact evaluator authority/implementation identity is absent;
- `DERIVED_SCHEDULE_INTEGRITY_FAILURE` — schedule/provenance/purity/replay contract is violated.

A boolean `false`, numeric zero, empty structured value, or other formula-produced value is not a negative-authority state. Conversely, missing authority/input may not be converted into an ordinary semantic value.

## 11. Dependency and cycle law

This authority fixes publication-phase order, not new formula semantics.

Every evaluator set used with this schedule MUST publish an explicit dependency graph for the canonical derived outputs. The graph MUST be finite and acyclic before evaluation begins. Dependencies may reference:

- frozen stored-state fields; and
- derived values computed within the same complete candidate evaluation.

They may not read a stale materialized derived field as an undeclared dependency.

A dependency cycle is `DERIVED_SCHEDULE_INTEGRITY_FAILURE`. No iterative fixed-point solver, arbitrary cycle break, or prior-cache substitution is authorized by CAN-014.

## 12. Compatibility adapter law

A recovered `v3_yearly_step_order.yaml` adapter is lawful only as a compatibility reader for the CAN-014 projection.

For the verified historical file, the adapter MUST project exactly:

```text
D01 reproduction_constraints_update -> [hostage_index]
D02 capacity_update                 -> [agency_capacity_AC]
D03 health_drift_update             -> [health_level]
D04 buffers_update                  -> [insulation_score]
D05 domains_update                  -> [structural_lucidity_SL]
D06 cracks_and_alienation_update    -> [mis_aim_risk, metabolic_style]
D07 topology_and_boundary_update    -> [autonomy_gap, safety_gap, gap_pressure_index,
                                        alignment_vector, stability_threshold,
                                        peak_regime, che_jesus_eligible]
```

The adapter MUST ignore as CAN-014 authority:

- `execution.timestep: year`;
- `max_events_per_year`;
- event sampling semantics;
- the full causal `steps` spine except as needed to validate the relative derived anchors and local check annotations;
- `extension_policy` as causal-scheduler authority.

Legacy `derived_compute` annotations may be generated from the canonical schedule or validated against it. They may not become a second mutable source of truth.

Legacy fallback behavior such as “missing schedule → `{}`” or “missing core steps → first N steps” is forbidden for canonical consumption.

## 13. Exact consumers and release relationship

Direct CAN-014 consumers named by RA-R00:

- `V3-P3` — state migration/checkpoints/stored-versus-derived;
- `V3-P4` — hybrid scheduler/context/requery integration.

Additional lawful consumers are audit/replay/acceptance tooling that validates those packets. V2 render/session code is not a CAN-014 scheduling consumer.

For `V3-P4`, CAN-014 supplies only the derived side of the contract. `ADP-021/MUST-021` separately supplies hybrid causal trigger precedence and slow cadence.

## 14. Replay and hash obligations

For a given exact tuple:

```text
(authority_id, authority_version,
 evaluator_set_id, evaluator_set_version, evaluator_set_sha256,
 StoredStateRef,
 requested_phase_or_FULL_RECOMPUTE)
```

pure derived evaluation MUST be deterministic.

Replay must reproduce:

- the same published logical values;
- the same per-output provenance stamps;
- the same canonical derived-view hash.

Cache presence/absence is not part of semantic identity. A cache entry is usable only on an exact key match. Otherwise recompute or fail according to missing-authority/input law; never serve stale data as current.

## 15. Forbidden inferences / semantic contamination

CAN-014 does not authorize any inference that:

- because legacy code ran yearly, terminal V3 runs yearly;
- because a derived phase follows a legacy causal step, that causal step is terminally required or has fixed precedence;
- because a derived value exists, a causal event occurred;
- because a derived boolean is true/false, an event should be admitted or rejected absent a separately governed rule;
- because a cache is present, it is current;
- because recovered code mutates `state.metabolic_style`/`state.registers`, derived evaluation may mutate terminal causal state;
- because V2 needs a value for rendering, V2 may schedule or recompute causal V3 state;
- because an evaluator input is missing, a legacy numeric/default value is acceptable;
- because local declarations agree by set, duplicates/order differences are harmless.

## 16. Hostile fixture court

The consumer acceptance harness MUST include at least these fixtures:

| Fixture | Hostile condition | Required result |
|---|---|---|
| `CAN014-H01` | top-level and local declarations disagree | `DERIVED_SCHEDULE_INTEGRITY_FAILURE` |
| `CAN014-H02` | same output declared twice in one phase | fail fast; duplicate may not disappear through set normalization |
| `CAN014-H03` | one output assigned to two phases | fail fast |
| `CAN014-H04` | phase order permuted | fail fast |
| `CAN014-H05` | unknown/implicit `latest` schedule version | fail closed |
| `CAN014-H06` | missing evaluator identity/hash | `DERIVED_BLOCKED_MISSING_EVALUATOR` |
| `CAN014-H07` | state content hash mismatches supplied state identity | `DERIVED_SCHEDULE_INTEGRITY_FAILURE` |
| `CAN014-H08` | derived evaluator writes causal-state field | fail fast; causal state unchanged |
| `CAN014-H09` | recovered `compute_all_derived`-style write to `state.metabolic_style` or `state.registers` | rejected as noncanonical impurity |
| `CAN014-H10` | stale cache used after state version changes | `DERIVED_STALE`; no causal consumption requiring freshness |
| `CAN014-H11` | same exact replay tuple yields different view hash | integrity failure / nondeterminism |
| `CAN014-H12` | evaluator dependency cycle | fail fast; no fixed-point guessing |
| `CAN014-H13` | filesystem/module/dict incidental order changes | canonical phase/output order unchanged |
| `CAN014-H14` | annual timestep supplied as proof of terminal cadence | rejected as out-of-jurisdiction |
| `CAN014-H15` | hybrid causal-trigger precedence embedded in schedule | rejected; belongs to `MUST-021` |
| `CAN014-H16` | V2 render/session schedule presented as derived schedule | rejected |
| `CAN014-H17` | missing input coerced to numeric/boolean default | blocked; no default substitution |
| `CAN014-H18` | mixed-state incremental view presented as single-state coherent | integrity failure |
| `CAN014-H19` | full recompute produces all outputs from one state but field stamp differs | integrity failure |
| `CAN014-H20` | legacy YAML matches 14 schedule entries but adds undeclared 15th output | fail fast |

## 17. Sufficiency

`CAN-014` is fully canonicalized for its bounded jurisdiction. It is sufficient as the **derived-schedule authority dependency** for V3-P3 and V3-P4.

It does **not** by itself release either packet because RA-R00 records additional independent blockers for both consumers, especially the remaining V3 state-rule canonicalizations for V3-P3 and `MUST-021` plus other runtime dependencies for V3-P4.

```text
CONSUMER_RELEASE_SUFFICIENCY = PARTIAL
```

No deficiency in CAN-014's own semantic scope remains; `PARTIAL` reflects independent consumer dependencies, not an invitation to expand this authority.

## 18. Final court statement

This canonicalization preserves the strongest recovered V3 discipline—derived values are recomputable, scheduled explicitly, and consistency failures stop the machine—while closing the two dangerous legacy ambiguities: duplicate schedule surfaces have no precedence escape hatch, and derived evaluation has no license to mutate causal truth.

Annual cadence remains historical implementation evidence. Hybrid causal scheduling remains `ADP-021/MUST-021`. V2 scheduling remains separate. No new causal semantics are introduced.

`CAN_014_V3_DERIVED_SCHEDULE_CANONICALIZATION = PASS`
