# CAN-014 — V3 Pure Derived-State Schedule Authority

**Authority ID:** `V3_PURE_DERIVED_STATE_SCHEDULE`  
**Authority version:** `1.1.0`  
**Registry contract ID:** `V3_DERIVED_OUTPUT_REGISTRY`  
**Registry contract version:** `1.0.0`  
**Canonicalization ID:** `CAN-014` / `CDP-CAN-014`  
**Owner:** `V3`  
**Status:** `CANONICALIZED__LEGACY_OUTPUT_NONPROMOTION_HARDENED`  
**Authority class:** `AUTHORITY_NEEDS_CANONICALIZATION`  
**Whole-machine architecture:** `CLOSED`  
**Production code modified:** `NO`  
**New causal semantics introduced:** `NO`

## 1. Binding disposition

CAN-014 canonicalizes the **mechanics by which independently governed pure derived outputs are registered, dependency-ordered, recomputed, published, freshness-stamped, replayed, compatibility-checked and failed closed**.

CAN-014 does **not** create the semantic existence, meaning, formula, causal status, or terminal necessity of any individual derived output merely because that output appeared in recovered V3 code.

The terminal contract is:

```text
V3_PURE_DERIVED_STATE_SCHEDULE@1.1.0
+
V3_DERIVED_OUTPUT_REGISTRY@1.0.0
+
exact independently governed semantic/evaluator authority refs
+
exact evaluator-set/dependency identities
        ↓
pure deterministic recomputation/publication
        ↓
V3 DerivedActorView materialization
```

At this authority-foundation point, no independently accepted semantic/evaluator authority has been identified that lawfully promotes any of the fourteen recovered legacy derived fields into the terminal registry. Therefore:

```text
CURRENT_CANONICAL_REGISTERED_OUTPUT_COUNT = 0
CURRENT_CANONICAL_REGISTRY_STATUS = VALID_EMPTY_DERIVED_OUTPUT_REGISTRY
```

An empty registered-output set is a lawful complete state of the schedule machinery. No synthetic placeholder output, minimum output count, or recovered field is required.

## 2. Preserved constitutional law

The following prior findings remain binding without reduction:

```text
stored causal state != derived view != causal event history
```

- derived state is recomputable materialization;
- pure derived evaluation uses no RNG;
- pure derived evaluation reads an exact frozen stored-state identity;
- no wall clock, filesystem order, module/import order, mutable `latest`, unnamed randomness or incidental iteration order may become authority;
- derived evaluation cannot mutate `ActorCausalState`, append causal events, advance causal cursors, or manufacture generated history;
- a derived cache is nonauthoritative optimization only;
- schedule/evaluator/state/provenance identities are explicit and versioned;
- duplicate registration, dependency cycles, schedule disagreement, provenance mismatch and nondeterministic replay fail closed/fail fast;
- annual timestep is recovered implementation evidence, not ontology;
- hybrid causal scheduling / trigger precedence / slow cadence remains `ADP-021/MUST-021` jurisdiction;
- V2 render/session scheduling remains separate.

A derived result may influence causal truth only when a **separately governed causal rule** explicitly consumes that result and owns/records the resulting causal transition or event. CAN-014 never grants that causal authority itself.

## 3. Governing evidence and authority rank

### 3.1 Binding current authority inspected

- `state/CURRENT_STATE.md`;
- `integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`;
- `integration/IMPLEMENTATION_RELEASE_SYNTHESIS_RULING.md`;
- `integration/V3_COMPLETION_IMPLEMENTATION_RULING.md`;
- RA-R00 `RESULT.md` / `RESULT.json`;
- TD-R05 `RESULT.md`.

These establish that CAN-014 is `AUTHORITY_NEEDS_CANONICALIZATION`, that V3 pure-derived scheduling is separate from the causal scheduler and V2 scheduling, and that the recovered V3 archive is continuity/authority-recovery evidence rather than terminal semantic sovereignty.

### 3.2 Required historical archive — directly reverified

```text
archive: Rawlsing_code_bundle_staging.zip
expected SHA256: 953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086
computed SHA256: 953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086
verdict: EXACT_MATCH
```

Directly inspected continuity evidence remains:

| Recovered path | SHA256 | Recovery finding |
|---|---|---|
| `v3/v3_yearly_step_order.yaml` | `90496a2cc852ca00ef99c8bd4fcb2b41c9aa43c4aaa9108d3ac8cce0ebe22ffc` | seven legacy derived checkpoints / fourteen legacy logical outputs; annual cadence is legacy execution metadata |
| `v3/engine/step_runner.py` | `5a737c1704eaa6dc2c67f6c2db3118a6daa8a213b44d559bc37eadbc9c09d95a` | full derived recomputation before recovered run loop |
| `v3/engine/yearly_step.py` | `da3147c3da7ff2724a61dd26d595055668899c83beb541400f58633568b92acb` | complete candidate recomputation, selective publication, duplicate-surface consistency assertion |
| `v3/core/invariants.py` | `81298f3fc51b46cda8d72d0db914b672b17b9a35e13004fe59a9b0e29dada5e3` | stored-versus-derived separation and fail-fast posture |
| `v3/core/derived.py` | `e479fc3eba21734752c372742fb2ee247cbdde6a73ac42545dc30b5039301360` | recovered formulas/outputs plus noncanonical causal-state side effects |
| `v3/core/config_loader.py` | `5f953d9661f61081187898c3ad06b4567bc4fa99d3d7cd856d30cdd961f78577` | fallback/empty legacy behavior is implementation evidence, not terminal authority |
| `v3/tests/test_architecture_invariants.py` | `bb2baec1c57de169a2e1e05533b9721b4b05191403ff4993d61df17ac29d05fa` | historical schedule/order and stored-vs-derived invariants |

Mechanical recovery inspection found fourteen historical schedule entries, seven historical checkpoints and no top-level/local mismatch in that archive. This proves the historical profile; it does **not** promote its fields into terminal semantic vocabulary.

### 3.3 Current V3 terrain

At the original launch base `655da47b9e03ab310ed4b7fa65ceec9b9d04d3bc`, accepted V3 rulings/recalibration and V3-facing boundary tests are present, but no terminal production `v3/` runtime implementation supplies an already-accepted terminal derived-output ontology. No absent semantic authority is inferred.

## 4. Jurisdiction

### 4.1 CAN-014 owns

- `V3_PURE_DERIVED_STATE_SCHEDULE` schema, identity and versioning;
- `V3_DERIVED_OUTPUT_REGISTRY` registration contract schema and validation law;
- pure recomputation/publication mechanics for registered outputs;
- deterministic dependency/order representation;
- frozen stored-state input identity requirements;
- evaluator-set identity/version/hash requirements;
- per-output freshness/provenance/replay stamps;
- coherent full-recompute versus mixed-freshness incremental-view semantics;
- duplicate/cycle/unknown/mismatch failure behavior;
- derived-cache nonauthority;
- recovered-schedule compatibility profile and migration checks.

### 4.2 CAN-014 does not own

- semantic existence or necessity of an individual derived field;
- the formula, thresholds, taxonomy or interpretation of an individual derived field;
- the semantic/evaluator authority that licenses a field to be registered;
- causal event scheduling, trigger precedence or slow cadence;
- any causal mutation rule;
- annual timestep ontology;
- V2 render/session schedule;
- actor initialization, positions, encounters/exposures, memory, attractor transitions, external admission, or RNG policy;
- V550+ structural semantics.

Relevant separate authorities include CAN-009, CAN-010, CAN-011, CAN-012 and other V3 MUST/CAN authorities as applicable. Their existence in the release program does not mean their semantic decisions are already accepted.

## 5. Canonical machine identities

```text
schedule_authority_id      = V3_PURE_DERIVED_STATE_SCHEDULE
schedule_authority_version = 1.1.0
registry_contract_id       = V3_DERIVED_OUTPUT_REGISTRY
registry_contract_version  = 1.0.0
owner                      = V3
schedule_kind              = PURE_DERIVED_STATE_SCHEDULE
```

There is no implicit `latest`. Every schedule snapshot, registry snapshot and evaluator selection is content-addressed and version-explicit. Unknown versions fail closed.

## 6. V3_DERIVED_OUTPUT_REGISTRY contract

A canonical output exists for CAN-014 scheduling **only** through a validated registry entry backed by independently governed semantic/evaluator authority.

Minimum registration record:

```text
DerivedOutputRegistration {
  logical_output_id

  semantic_authority_ref {
    authority_id
    authority_version
    authority_content_sha256
  }

  evaluator_ref {
    evaluator_id
    evaluator_version
    evaluator_content_sha256
  }

  evaluator_set_ref {
    evaluator_set_id
    evaluator_set_version
    evaluator_set_sha256
  }

  admissible_stored_state_inputs[] {
    input_id
    schema_id
    schema_version
  }

  dependency_refs[] {
    logical_output_id
    required_registration_sha256
  }

  publication {
    publication_phase_id
    phase_order_key
    within_phase_order_key
    freshness_policy
  }

  purity_declaration = PURE_READ_ONLY_DERIVATION
  registration_sha256
}
```

The exact semantic/evaluator authority may use a different physical schema, but the registry must losslessly expose the above information.

### 6.1 Registration admission law

A candidate output registration is admitted only when all are true:

1. `logical_output_id` is explicit and unique;
2. a separately governed semantic/evaluator authority ID + exact version + content hash is supplied and accepted;
3. exact evaluator and evaluator-set identities are supplied;
4. admissible stored-state inputs are explicit;
5. dependencies are explicit and resolve to other admitted registrations or declared stored-state inputs;
6. publication phase/order is explicit if incremental publication is enabled;
7. purity is declared and mechanically enforceable;
8. provenance/replay obligations can be satisfied.

**Recovered schedule presence is never an admission criterion.**

A recovered legacy name without accepted semantic/evaluator authority remains migration evidence only and does not enter the terminal registry.

### 6.2 Current registry state

At this W0 authority-foundation point:

```text
registry_status = VALID_EMPTY_DERIVED_OUTPUT_REGISTRY
registered_output_count = 0
registered_outputs = []
```

No minimum count exists. `0` is lawful and complete for CAN-014 scheduling mechanics.

The later acceptance of an appropriate semantic/evaluator authority may produce a new content-addressed registry snapshot with one or more registrations. That later registry update is not a change to CAN-014 mechanics and cannot be inferred before the authority is accepted.

## 7. Canonical schedule contract

The terminal schedule is a versioned projection over the **currently admitted output registry**, not a frozen list of recovered legacy field names.

A canonical schedule snapshot contains:

```text
DerivedScheduleSnapshot {
  schedule_authority_id
  schedule_authority_version
  registry_contract_id
  registry_contract_version
  registry_snapshot_sha256
  registered_output_count

  publication_phases[] {
    publication_phase_id
    phase_order_key
    registered_output_ids[]
  }

  dependency_graph_sha256
  canonical_schedule_sha256
}
```

### 7.1 Empty schedule

When the registry is valid-empty:

```text
registered_output_count = 0
publication_phases = []
dependency_graph = empty DAG
status = VALID_EMPTY_DERIVED_OUTPUT_REGISTRY
```

This is not a missing schedule and not a failure. It means no terminal derived output currently has independent authority to be scheduled.

### 7.2 Deterministic order

For nonempty registries, terminal execution/publication order is derived only from:

1. explicit dependency edges among admitted registrations;
2. explicit phase/order keys carried by admitted registrations/schedule snapshot;
3. a deterministic canonical tie rule over stable identifiers **only where the registry authority explicitly permits peers to be unordered semantically**.

No filesystem order, source-code order, dictionary order, module import order, recovered phase location, or incidental enumeration may determine semantics.

A dependency edge always outranks a conflicting phase/order declaration. A conflict that cannot satisfy both contracts is `DERIVED_SCHEDULE_INTEGRITY_FAILURE`; CAN-014 does not guess which declaration wins.

### 7.3 Dependency law

The admitted dependency graph must be finite and acyclic. Dependencies may reference:

- exact stored-state input declarations; and
- other admitted derived-output registrations.

An evaluator may not silently read stale materialized derived values as undeclared dependencies.

A cycle fails fast. CAN-014 authorizes no iterative fixed-point solver, arbitrary cycle break or prior-cache substitution.

## 8. Pure recomputation and publication

### 8.1 Frozen stored-state identity

Every evaluation reads an exact frozen state reference:

```text
StoredStateRef {
  state_schema_id
  state_schema_version
  state_version_id
  state_content_sha256
}
```

CAN-014 does not define how causal state versions advance.

### 8.2 FULL_RECOMPUTE

A coherent full recompute:

1. freezes one exact `StoredStateRef`;
2. loads one exact registry snapshot and canonical schedule snapshot;
3. evaluates all currently registered outputs in canonical dependency/order sequence;
4. performs no causal writes;
5. publishes all registered outputs with the same `StoredStateRef`;
6. records exact semantic authority/evaluator/evaluator-set/registration/schedule identities;
7. hashes the canonical materialized view.

For a valid-empty registry, `FULL_RECOMPUTE` lawfully returns an empty derived view with `SINGLE_STATE_FULL` coherence and complete schedule/state provenance. It does not fabricate placeholder outputs.

### 8.3 Incremental publication

If separately governed runtime behavior requests incremental derived publication, only registered outputs assigned to the requested canonical phase may publish.

Each published field is evaluated from the exact frozen state supplied for that publication and receives its own provenance/freshness stamp. Fields refreshed from different stored-state versions yield:

```text
coherence = MIXED_STATE_INCREMENTAL
```

Such a view may never masquerade as one coherent snapshot. A consumer requiring all derived outputs from one causal state must demand `FULL_RECOMPUTE` and verify one shared `StoredStateRef`.

CAN-014 does not decide **when** an incremental publication phase is triggered. That causal/timing question remains outside this authority.

## 9. Derived-field provenance

Each materialized registered output must carry or be losslessly attributable to:

```text
DerivedFieldStamp {
  logical_output_id
  registration_sha256
  semantic_authority_id
  semantic_authority_version
  semantic_authority_content_sha256
  evaluator_id
  evaluator_version
  evaluator_content_sha256
  evaluator_set_id
  evaluator_set_version
  evaluator_set_sha256
  publication_phase_id
  source_state_ref
  schedule_authority_id
  schedule_authority_version
  registry_snapshot_sha256
}
```

A materialized view exposes:

```text
DerivedViewIdentity {
  view_kind = V3_DERIVED_ACTOR_VIEW
  schedule_authority_id
  schedule_authority_version
  registry_snapshot_sha256
  canonical_schedule_sha256
  field_stamps[]
  canonical_view_sha256
  coherence = SINGLE_STATE_FULL | MIXED_STATE_INCREMENTAL
}
```

The derived-view hash is not a causal-event hash.

## 10. Purity and causal nonmutation

Pure derived evaluation may create, replace or invalidate derived-view materialization only. It must not:

- write `ActorCausalState`;
- append `DevelopmentalEventLedger` entries;
- advance causal cursors;
- alter checkpoints;
- create relationship/genealogy/position facts;
- create or change causal memory;
- admit external events;
- mutate structural priors;
- use RNG.

Recovered `compute_all_derived()` side effects writing locations such as `state.metabolic_style` and `state.registers` remain **NONCANONICAL LEGACY IMPURITY**. CAN-014 does not repair that impurity by declaring those fields causal. A derived materialization remains outside `ActorCausalState` unless some separate accepted authority explicitly owns a causal state field and its mutation rule.

Because `metabolic_style` lacks an independently accepted evaluator authority in this court, its presence in recovered derived code also does not register it as a terminal derived output.

## 11. Stored-versus-derived and cache law

- registered derived outputs are recomputable from their exact frozen inputs and exact authority/evaluator identities;
- derived outputs are not stored causal fields merely because an implementation caches them;
- cache persistence/absence is semantically irrelevant;
- cache keys must include exact state, registry, schedule, registration, semantic-authority and evaluator identities sufficient for exact replay;
- a stale/mismatched cache entry is rejected, never served as current;
- deleting/recomputing derived cache cannot itself alter causal truth;
- causal replay cannot depend on cache presence.

## 12. Status / missing / failure law

Control states are distinct from ordinary semantic values:

- `VALID_EMPTY_DERIVED_OUTPUT_REGISTRY` — registry is valid and contains zero admitted outputs;
- `DERIVED_READY` — requested registered output is fresh and provenance-valid;
- `DERIVED_DEFERRED_NOT_REQUESTED` — registered output has not been refreshed for the relevant request/state and freshness is required;
- `DERIVED_STALE` — materialization exists but provenance does not satisfy required state/registry/schedule identity;
- `DERIVED_BLOCKED_MISSING_INPUT` — an admitted evaluator's required stored input is absent/unknown;
- `DERIVED_BLOCKED_MISSING_EVALUATOR` — an admitted registration refers to an unavailable/mismatched evaluator implementation;
- `DERIVED_BLOCKED_MISSING_SEMANTIC_AUTHORITY` — candidate output lacks accepted independent semantic/evaluator authority and therefore is not admitted;
- `DERIVED_SCHEDULE_INTEGRITY_FAILURE` — registry/schedule/dependency/purity/provenance/replay contract is violated.

A legitimate evaluator result of numeric zero, boolean false, an empty structured result or another semantic value is not a missing-authority state. Missing authority/input may never be converted into an ordinary value by default.

## 13. Fail-fast integrity law

The canonical contract fails before consumer use on any of the following:

- same `logical_output_id` registered twice;
- conflicting ownership/semantic-authority refs for one output ID;
- registration without exact accepted semantic/evaluator authority;
- missing/mismatched evaluator/evaluator-set/version/hash;
- undeclared dependency;
- dependency cycle;
- unknown publication phase/order key;
- schedule snapshot disagrees with the admitted registry snapshot;
- duplicate schedule entry for one registered output;
- registered output omitted from a schedule snapshot that claims complete publication coverage;
- schedule includes an output absent from the admitted registry;
- state identity/hash mismatch;
- implicit/mutable `latest` selection;
- evaluator writes causal state or uses RNG/wall clock/filesystem/incidental order;
- stale cache presented as current;
- same exact replay tuple produces a different canonical result/hash.

No fallback output, empty placeholder, first-N schedule, recovered field resurrection, stale cache, or guessed default is authorized.

## 14. Recovered seven-phase/fourteen-output profile

The recovered schedule is preserved **only** as:

```text
profile_id = LEGACY_V3_RECOVERED_DERIVED_SCHEDULE_20260818
profile_kind = LEGACY_COMPATIBILITY_PROFILE
semantic_authority = NONE
terminal_registration_power = NONE
```

Historical profile:

| Legacy order | Legacy phase | Legacy causal anchor | Historical outputs |
|---:|---|---|---|
| 1 | `D01` | `reproduction_constraints_update` | `hostage_index` |
| 2 | `D02` | `capacity_update` | `agency_capacity_AC` |
| 3 | `D03` | `health_drift_update` | `health_level` |
| 4 | `D04` | `buffers_update` | `insulation_score` |
| 5 | `D05` | `domains_update` | `structural_lucidity_SL` |
| 6 | `D06` | `cracks_and_alienation_update` | `mis_aim_risk`, `metabolic_style` |
| 7 | `D07` | `topology_and_boundary_update` | `autonomy_gap`, `safety_gap`, `gap_pressure_index`, `alignment_vector`, `stability_threshold`, `peak_regime`, `che_jesus_eligible` |

This profile records directly inspected historical behavior. It is **nonauthoritative for terminal semantic existence**.

It cannot:

- create a terminal output registration;
- satisfy the independent semantic/evaluator-authority requirement;
- require a missing evaluator to be invented;
- make `che_jesus_eligible`, `peak_regime`, `metabolic_style`, or any other recovered name terminal V3 vocabulary;
- force an obsolete field into terminal V3;
- block terminal completion merely because an obsolete historical output is intentionally unregistered;
- define terminal publication phases for outputs not independently registered;
- define terminal causal cadence or scheduler precedence.

A migration adapter may test whether legacy code matches this recovered profile. A mismatch against the **legacy profile itself** can be reported as legacy compatibility drift. A mismatch between this profile and the **terminal registered-output set** is expected/lawful when fields were intentionally not promoted and must not cause semantic resurrection.

### 14.1 Explicit `che_jesus_eligible` disposition

`che_jesus_eligible` is recorded only as a recovered D07 historical output. CAN-014 grants it no terminal semantic/evaluator authority, no canonical registration, no formula authority and no causal meaning.

The same nonpromotion rule applies to every other recovered output unless and until a separate accepted authority explicitly registers it through the canonical registry contract.

## 15. Compatibility adapter law

A compatibility adapter may:

- parse recovered `v3_yearly_step_order.yaml`;
- verify the recovered D01–D07 / fourteen-output profile against the directly inspected migration fixture;
- validate recovered top-level versus step-local declarations for internal consistency;
- report legacy impurity/fallback behavior;
- map a separately accepted terminal registration to legacy machinery where the mapping is lossless and explicit.

A compatibility adapter may not:

- auto-register a recovered field;
- infer semantic authority from historical schedule presence;
- require terminal registry equality with the historical fourteen-output set;
- fail terminal completion solely because terminal registered outputs intentionally differ from the legacy profile;
- import `execution.timestep: year`, `max_events_per_year`, event sampling, extension policy or causal step order as CAN-014 terminal authority;
- treat missing legacy output as terminal semantic deficiency.

## 16. Replay law

For an exact tuple:

```text
(schedule_authority_id, schedule_authority_version,
 registry_snapshot_sha256,
 canonical_schedule_sha256,
 registration_sha256(s),
 semantic/evaluator/evaluator-set identity+version+hash(s),
 StoredStateRef,
 requested publication phase or FULL_RECOMPUTE)
```

pure derived evaluation is deterministic.

Replay must reproduce the same:

- admitted output set;
- execution/publication order;
- logical values;
- field stamps;
- coherence classification;
- canonical derived-view hash.

A changed registry snapshot, evaluator hash, semantic-authority version, dependency graph or input-state hash changes replay identity. Cache presence does not.

## 17. Hostile fixture court

The acceptance harness must include at least:

| Fixture | Hostile condition | Required result |
|---|---|---|
| `CAN014-H01` | recovered legacy field has no accepted semantic/evaluator authority | not registered; `DERIVED_BLOCKED_MISSING_SEMANTIC_AUTHORITY` if registration is attempted |
| `CAN014-H02` | `che_jesus_eligible` appears in recovered D07 | remains legacy compatibility evidence only; no terminal registration/meaning |
| `CAN014-H03` | independently accepted evaluator authority registers new derived output `new_governed_output` | admitted with exact authority/version/hash, evaluator-set refs, inputs, dependencies, purity and publication provenance |
| `CAN014-H04` | canonical registry contains zero entries | `VALID_EMPTY_DERIVED_OUTPUT_REGISTRY`; full recompute returns lawful empty derived view; no placeholder |
| `CAN014-H05` | terminal registry intentionally omits obsolete historical output | no resurrection; legacy-profile mismatch does not block terminal schedule completion |
| `CAN014-H06` | same canonical `logical_output_id` registered twice | `DERIVED_SCHEDULE_INTEGRITY_FAILURE` |
| `CAN014-H07` | registered dependency cycle | fail fast; no fixed-point guessing |
| `CAN014-H08` | evaluator mutates `ActorCausalState` or appends event | fail fast; causal state/history unchanged |
| `CAN014-H09` | stale derived cache presented as current after state/registry/evaluator change | reject as `DERIVED_STALE` |
| `CAN014-H10` | annual recovered cadence offered as terminal scheduler authority | reject as out of jurisdiction; `ADP-021/MUST-021` owns causal cadence/precedence |
| `CAN014-H11` | output listed in terminal schedule but absent from admitted registry | fail fast |
| `CAN014-H12` | registration has evaluator but no exact independent semantic-authority version/hash | not admitted |
| `CAN014-H13` | filesystem/module/dict order changes | canonical registered-output order remains unchanged |
| `CAN014-H14` | same replay tuple yields different result/hash | integrity failure / nondeterminism |
| `CAN014-H15` | recovered `compute_all_derived()` writes `state.metabolic_style` / `state.registers` | rejected as noncanonical legacy impurity; fields are not made causal |
| `CAN014-H16` | mixed-state incremental view labeled coherent full snapshot | fail fast |
| `CAN014-H17` | missing input coerced to zero/false/empty | blocked; no semantic default substitution |
| `CAN014-H18` | V2 render/session order presented as derived schedule | reject as wrong jurisdiction |

## 18. Consumers and release sufficiency

Direct CAN-014 consumers named by RA-R00 remain:

- `V3-P3` — state migration/checkpoints/stored-versus-derived;
- `V3-P4` — hybrid scheduler/context/requery integration.

CAN-014 is complete for its own scheduling/registration/purity/freshness/replay jurisdiction, including the lawful empty-registry case. It does **not** claim closure of any individual derived semantic/evaluator authority.

V3-P3/P4 remain independently gated by their other RA-R00 CAN/MUST/EXT dependencies. In particular, V3-P4 still requires `ADP-021/MUST-021` for hybrid causal scheduling and slow cadence.

```text
CONSUMER_RELEASE_SUFFICIENCY = PARTIAL
```

`PARTIAL` reflects independent consumer dependencies, not a missing CAN-014 schedule mechanic and not a license to promote legacy outputs.

## 19. Final binding statement

CAN-014 canonicalizes a **schedule and output-registration contract**, not a recovered ontology.

The recovered D01–D07 / fourteen-output schedule remains valuable source evidence and a migration fixture. It has zero power to create terminal semantic existence. At the present authority-foundation state, the canonical terminal derived-output registry is lawfully empty with `0` registered outputs.

No recovered field is promoted solely by schedule presence. No causal semantics are added. The legacy `compute_all_derived()` causal-state side effects remain noncanonical. Derived computation stays pure, deterministic, versioned, provenance-complete and fail-fast.

`CAN_014_V3_DERIVED_SCHEDULE_CANONICALIZATION = PASS`
