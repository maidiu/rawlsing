# SYN02-B — lawful construction tranche, code-change and dependency plan

**Status:** `DESIGN_ONLY__NO_PRODUCTION_IMPLEMENTATION__NO_NATIVE_GRANT`.
**Scope:** a prioritized construction plan for the 40-mechanism adaptation. It separates immediately lawful engineering hygiene from source/semantically/natively gated work. No code is changed here; the plan is a handoff for a future implementation owner and SYN02-S integrator.

## 1. Architecture thesis

The existing V3 machine is a real but mixed reservoir. It contains genuinely reusable **carriers, traces, ordering, transaction and hysteresis techniques**, but also fabricated defaults, demographic/type presets, one-valence event labels, narrator-to-psyche feedback, premerged LLM deltas, missing event ledgers, hidden derived writes and a readiness guard that confuses a fixture/stored persona with a native person.

The design target is a **layered, sparse, source-qualified actor**:

```text
World/C0/C8/ADP019 source layer
  └─ CanonicalEventV1 / EpisodeV1 / SourceEnvelope
       └─ Actor intake/access (ADP017)
            └─ CAN008 immediate Rule A response / transient impression
                 └─ CAN011 durable mediator/tension/practice or NO_CHANGE
                      └─ next realized event reads the actor's semantic state
                           └─ ADP016/017 retrospective actor-accessible memory
                                └─ V2 / A0–A5 read-only expression
```

The actor layer is `ActorSnapshotV1` plus append-only `CanonicalEventV1` ledger and typed records. `DerivedViewValue` is pure. `SurfaceRecord` is one-way. There is no second psyche, no global all-to-all graph and no automatic narrator write-back.

## 2. Rejected alternatives

| Alternative | Why rejected |
|---|---|
| **A. Patch the old `BackboneState` in place** | It preserves fabricated 50/hopeful defaults, demographic seeds, placeholders, derived writes, event premerge and the second-psyche ambiguity. A new field cannot repair the wrong writer/causal unit. |
| **B. Clean-sheet rewrite** | It discards reviewed carriers, explicit ordering, transaction/trace, hysteresis and source/test knowledge. The commission’s parent instruction is reuse/adapt, not rebuild from zero. |
| **C. All-to-all or Hebbian relation graph** | No scientific rule supports automatic coactivation wiring; it would manufacture learned relations and a synapse metaphor. Dynamic inter-wiring remains a SYN02-C research question, not a default graph. |
| **D. Promote legacy numeric values as scientific state** | Old 0–100 scales, age/religion/class seeds, modes and weights are historical policy, not empirical law. Importing them by rename is laundering. |
| **E. Separate V2 narrating psyche** | It violates one-person jurisdiction. V2 expression must read the actor, not become a second causal author or memory authority. |
| **F. Event ledger without durable middle state** | It cannot represent support-dependent retained practice, tensions, relations or delayed change. The inverse—durable state without canonical events—also fails. |
| **G. Global topology/framework enum as the whole organization** | RX02/RX03 show fixed regime switches, not learned relations. Hysteresis is a technique; the scalar enum is not the terminal ontology. |
| **H. Complete person from a single E1→E2 fixture** | The user explicitly requires whole-person architecture first. E1→E2 is a falsifier inside the architecture, not its definition. |

**Chosen:** layered sparse actor + canonical event/interval ledger + pure derived views + one-way surface + explicit migration/compatibility. Dynamic functional connections are an optional, owner-gated `FunctionalConnectionRecord` candidate; they are not adopted by this court.

## 3. Tranche plan

Effort ranges are indicative engineering estimates, not commitments, and exclude scientific issuance, source permission, native qualification and human evaluation.

### B0 — Custody, source identity and design baseline (largest lawful immediate tranche part 1)

- Freeze exact source cut and 59-file hash manifest; keep the historical staging tree read-only.
- Record 40/40 author/reviewer provenance and `CURRENT_INTEGRATION_UNTRACED`.
- Define candidate schema names (`neo_v3.actor@1`, `neo_v3.event@1`, `neo_v3.legacy_migration@1`) and the migration report.
- No actor behavior, no science, no production.

**Outputs:** source manifest, schema proposal, migration report/receipt types, decision log.
**Effort:** 3–5 days. **Risk:** low.

### B1 — Pure schema, derived registry and migration foundation (largest lawful immediate tranche part 2)

- `ActorSnapshotV1`, `CanonicalEventV1`, `EpisodeV1`, `ImpressionV1`, `TransitionReceiptV1`.
- `DerivedViewSpec`/`DerivedViewValue`; no derived writes.
- `LegacyV3Reader` read-only; `MigrationDecision`; `LegacyArtifact`; `MigrationReport`; atomic/idempotent migration.
- Fresh valid-empty actor; explicit `UNKNOWN`/`ABSENT`.
- `ReadinessVector` with separate engine/rule/source/actor/memory/consumer gates.
- First consumer: `ActorHistoryReader` / a read-only migration report; no C9/C12 behavior.

**Effort:** 10–16 days. **Risk:** medium (schema/migration); high for legacy classification.
**Authority:** engineering/schema owner; no science/source grant.

### B2 — Canonical event ledger, transaction and surface boundary (largest lawful immediate tranche part 3)

- `CanonicalEventLedger`, `EventAdmission`, `NoEventRecord`, `HeldMissingRule`.
- `TransactionScope` with whole-actor commit/rollback or explicit committed-prefix policy.
- `SurfaceRecord` one-way; remove annotation/marker from memory/previous-scene selection.
- `DerivedViewRegistry`; no `registers`/`metabolic_style` writes.
- **First consumer:** event ledger read by a future `CAN008` adapter; V2 surface read-only.

**Effort:** 8–14 days. **Risk:** high (ordering/transaction).
**Authority:** C6/C8/C9 architecture; no concrete Rule A/T.

### B3 — Event/interval and proposal transport

- Replace `run_one_year`-as-causal-unit with `advance_interval` + `run_event_sequence`.
- `propose_batch` (3–5 conditional specifications), `realize_world_event`, `admit_event`, `select_event` with hard admissibility and named RNG/ADP020.
- Per-event CAN008/011 or typed `NO_CHANGE`; no premerge; event 2 reads state after event 1 and interval activity.
- `retrospect` is a separate first-half N+1 surface; no extra ordinary LLM calls.
- **First consumer:** next event's actor-state read; future C9/C12.

**Effort:** 12–18 days for the sourcefree shell; **HOLD** for concrete realization/rule. **Risk:** high.
**Authority:** C6/C8/C9/C12 + ADP019/ADP020/ADP021; no native.

### B4 — World, material, relations and independent coactors

- `SourceEnvelope` → `MaterialFact`, `InstitutionRef`, `ParticipationRef`, `ActorEntityRef`, `RelationRecord`.
- Actual care/work/availability intervals; co-care; absence/no-contact; source-owned other actor.
- Remove unconditional mother/father labels, `who` loss and label-to-practice.
- **First consumer:** event realization / actor material/support read.

**Effort:** 15–25 days plus source/owner work. **Risk:** very high. **Authority:** C0/C8/ADP019/SDTF/world owner. **HOLD** until source owner.

### B5 — Actor middle-state formation and maintained practice

- `NeedRecord`, `ExpectationRecord`, `MotiveTargetRecord`, `TensionRecord`, `MediatorRecord`, `PracticeRecord`, `SupportRecord`, `SensitivityRecord`, `ResidueRecord`.
- Acquisition/use/scope/contradiction/support/loss and explicit `NO_CHANGE`; remove age/random/demographic presets.
- Optional `FunctionalConnectionRecord` only if SYN02-C/science authorizes; no automatic Hebbian coactivation.
- **First consumer:** later event read by CAN008/C9.

**Effort:** 20–30 days plus CAN/ADP rule issuance. **Risk:** very high. **Authority:** CAN010/CAN011/ADP; **HOLD** for concrete rules.

### B6 — Rupture/metabolization and memory/retrospection

- `RuptureRecord`, `MetabolizationProcessRecord`, `ImpressionRecord` mixed components.
- Exact CAN012 admission/parents/support/status/IRR/NO_CHANGE; no age/global RNG/prose support/direct wound.
- ADP016/017 actor-accessible memory packet; SCI05 retrospective internal-act admission; no extra ordinary LLM.
- **First consumer:** later same-person C9 semantic read / memory read.

**Effort:** 20–30 days plus owner rules. **Risk:** very high. **Authority:** CAN012/ADP016/017/SCI05/C9/C12. **HOLD**.

### B7 — Current person integration, migration and evaluation

- Assemble current C9/C12 with old V3 projections only at explicit compatibility seams.
- Migration of existing records with source labels/archive.
- First same-person E1→CAN008→CAN011/NO_CHANGE→E2 semantic read; independent B; V2/A0–A5.
- Positive/no-change/severed-edge/batch tests; current C9/C12 actual source imports.

**Effort:** 20–35 days plus native/source/authority time. **Risk:** very high. **Authority:** C9/C12/CAN/Pyat/A0–A5. **HOLD**.

## 4. Immediate safe hygiene vs semantically controlled work

### 4.1 Immediate safe hygiene (new implementation branch only)

These are new-engine changes that remove known old defects without claiming a new psychological law. They may be implemented only after the schema/owner accepts the target shape.

1. Remove fabricated fallback events; add `NoEventRecord`/held.
2. Remove placeholder cracks/frameworks; valid-empty.
3. Remove `50→hopeful`/safe-home defaults; unknown.
4. Remove age-band rupture and random striving spawn/retirement from the new path.
5. Fix phantom alienation and duplicate hostage authorities.
6. Make derived views pure; stop `registers`/`metabolic_style` writes.
7. Make render one-way; exclude annotation/markers from memory.
8. Make Pass-2 failure transactional or return a committed-prefix receipt.
9. Make readiness multi-gate; stored/degraded persona is not clean person.
10. Preserve full source/archive evidence; no deletion.

**Effort:** 8–15 days. **Risk:** medium. **First consumer:** migration/event shell. **Authority:** engineering/source owner; no science.

### 4.2 Semantically controlled work

- Actual material/care constraints vs received care.
- Expectation formation/repair/coexistence.
- Multiple interpressures/recruitment.
- Acquired frameworks/practices/motives.
- Rupture/metabolization transition.
- Memory/meaning/ideology.
- Dynamic functional connections.

Each requires a concrete competent owner, input preconditions, output, no-effect/NO_CHANGE, rival alternative and first C9 consumer. These cannot be filled by old formulas, defaults or model prose.

### 4.3 Native/product work

C9/C12 same-person semantic consumer, independent B, Pyat C11/A0–A5 and production adoption are separate authority holders. No current source/actor/native permission is inferred from this design.

## 5. New code surface (candidate names, not implemented)

| Package/module | Functions/types | Depends on | First consumer |
|---|---|---|---|
| `neo_v3/actor/schema` | `ActorSnapshotV1`, `ActorClock`, `Provenance`, `UnknownFact`, `ValidEmpty` | B0 | ActorHistoryReader |
| `neo_v3/actor/events` | `CanonicalEventV1`, `EpisodeV1`, `ImpressionV1`, `TransitionReceiptV1` | B2 | event ledger/C9 |
| `neo_v3/actor/middle_state` | `NeedRecord`, `ExpectationRecord`, `MotiveTargetRecord`, `TensionRecord`, `MediatorRecord`, `PracticeRecord`, `SupportRecord`, `SensitivityRecord` | B5 | CAN008/C9 |
| `neo_v3/actor/rupture` | `RuptureRecord`, `MetabolizationProcessRecord`, `admit_rupture`, `transition_metabolization` | B6 | CAN012/C9 |
| `neo_v3/actor/relations` | `ActorEntityRef`, `RelationRecord`, `InstitutionRef`, `ParticipationRef` | B4 | event realization/C9 |
| `neo_v3/runtime/scheduler` | `advance_interval`, `run_event_sequence`, `EventAdmission`, `NoEventRecord` | B2/B3 | event realization |
| `neo_v3/runtime/derived` | `DerivedViewRegistry`, `compute_view` | B1 | all read-only views |
| `neo_v3/runtime/transaction` | `TransactionScope`, committed-prefix receipt, rollback | B2 | event/surface writes |
| `neo_v3/runtime/readiness` | `ReadinessVector`, `assess_person_readiness` | B1 | store/C9 |
| `neo_v3/llm/batch` | `BatchProposal`, `propose_batch`, `retrospect` | B3 | next event/retrospective |
| `neo_v3/surface` | `SurfaceRecord`, `render_surface`, `ActorVisibleSurface` | B2 | V2/ADP017 |
| `neo_v3/migration/v3` | `LegacyV3Reader`, `MigrationDecision`, `MigrationReport`, `LegacyArtifact` | B1 | migration audit |

No implementation is authorized by this table. Names are candidate interfaces for a future code owner.

## 6. Test and falsifier plan (design grade, NOT_RUN)

### 6.1 Positive

One actor receives a source-owned E1 care/activity event with an independently acting B and actor access. A concrete CAN008 Rule A produces an immediate response/impression; a separate CAN011 Rule T creates or changes one scoped mediator/practice/tension or returns valid NO_CHANGE. A later E2 with the same world/A access/B identity is evaluated by the same C9/CAN008 code, reading the semantic value and scope of the changed state. The comparison must hold world/B/material conditions fixed and vary only the earned actor record. `SPECIFICATION_ONLY`.

### 6.2 Lawful NO_CHANGE / external-support alternative

If the later event is not accessible/current, or no owner rule applies, return `HELD_MISSING_RULE` or a warranted `NO_CHANGE`, not a fabricated state. If an external co-carer changes the outcome while the actor's durable state is unchanged, label external support separately. If the same event occurs without the formation edge, the semantic result should be identical where all actually consulted values are identical. `SPECIFICATION_ONLY`.

### 6.3 Artificial-NO_CHANGE prevention

Missing rule/source/record must not be presented as psychological NO_CHANGE. Empty candidate packet, parse failure, clamp, placeholder, unavailable bridge, missing B and stored-persona bypass remain `HELD`/`UNKNOWN`/`INTEGRITY` outcomes. The new system must distinguish `NO_CHANGE_EVALUATED` from `NO_CHANGE_UNAVAILABLE` and `HELD_MISSING_RULE`.

### 6.4 Severed upstream edge

In the same actor/E2/world/B case, remove only the exact earned-state→E2 semantic read edge (or the exact formation parent). The semantic difference must disappear or produce a precise `MISSING_CONDITIONER`/integrity refusal. A hash-only change, a different prompt string or a model-authored “learned” line does not satisfy the test. `SPECIFICATION_ONLY`.

### 6.5 Sequential batch fault

Propose 3–5 conditional events. Realize event 1, compute per-event actor/interval state, then event 2. Reverse event 1/2 or alter event 1 while holding event 2 candidate fixed. Event 2 must read the altered state or lawfully NO_CHANGE; the old `merge_deltas` order-invariance and premerged application fail this design. No ordinary LLM call between events; first half N+1 may only retrospect actor-accessible features of the realized prefix. `SPECIFICATION_ONLY`.

### 6.6 Prose-only perturbation

Change only the rendered surface with actor/event/world fixed. New architecture: no actor-state difference. Old V3: an active process can make prose affect `narration_support`/capacity. This is a direct falsifier for any retained narrator feedback. `SPECIFICATION_ONLY` for new code; historical source behavior was independently observed by RX03/RX05.

### 6.7 Malformed/unknown legacy state

Inject missing/unknown/default/synthetic fields. Migration must archive/quarantine, not convert to `0`/`50`/`hopeful`/clean. A required unknown blocks readiness. `SPECIFICATION_ONLY`.

## 7. Dependencies and effort

| Dependency | Blocks | Owner |
|---|---|---|
| Schema/actor architecture decision | B1–B7 | V3/C9/C12 architecture owner |
| Canonical event/clock contract | B2/B3 | C6/C8/C9 |
| Source-owned world/coactor/material facts | B3/B4/B6 | C0/C8/ADP019/SDTF/world |
| CAN010 need/expectation/motive rule | B5 | CAN010 + ADP |
| CAN011 middle-state transition | B5/B6 | CAN011 + ADP |
| CAN012 rupture/metabolization | B6 | CAN012 + ADP020/021 |
| ADP016/017 memory/access + SCI05 | B6 | ADP/SCI05/V2 |
| C9/C12 same-person semantic read | B6/B7 | C9/C12 |
| Pyat C11/A0–A5 | B7 | Pyat/native owners |

Indicative implementation-only effort: B0 3–5d; B1 10–16d; B2 8–14d; B3 12–18d; B4 15–25d; B5 20–30d; B6 20–30d; B7 20–35d. This is not a delivery promise; owner/science/source time is additional and cannot be compressed by code.

## 8. Largest lawful build tranche now

**B0 + B1 + B2 + the sourcefree shell of B3** is the largest lawful immediate tranche without a new scientific rule, new world/B source or native permission. It creates:

- a versioned sparse actor/migration schema;
- pure derived views;
- canonical event ledger and transaction/rollback;
- read-only legacy projection and archive;
- a batch-proposal/event shell with explicit `NO_CHANGE`/held/fallback prohibition;
- a one-way surface boundary and multi-gate readiness.

It does **not** claim actual care, expectations, acquired practices, middle-state formation, rupture transition, memory, ideology or a native person. B4–B7 remain owner-held.

## 9. Positive / NO_CHANGE / fault ownership handoff

| Handoff | Input → output | Test | Owner |
|---|---|---|---|
| Migration | legacy bytes → `ActorSnapshotV1` + report/archive | unknown/synthetic/atomic/idempotent | schema/migration owner |
| Event ledger | world event proposal → canonical event + admission/held | source/access/parent/clock | C8/ADP019 |
| Per-event actor | event + actor state → CAN008 response/CAN011 transition or NO_CHANGE | positive/no-change/severed | CAN008/CAN011/C9 |
| Interval | accepted prefix → activity/support/material carry-forward | activity/no-contact/partial | C6/SDTF |
| Retrospection | realized prefix → actor-accessible memory/meaning | feature filtering/denied SCI05 | ADP016/017/SCI05 |
| Surface | actor + event → surface only | prose-only no actor change | V2/ADP017 |
| Readiness | gates → vector/verdict | blocked/degraded/clean stored | C9/native |

## 10. Stop conditions

- No concrete Rule A/T: stop B5/B6 formation; continue schema/ledger/surface.
- No independent world/B/access: stop B4/B6 realization; continue sourcefree shell.
- No ADP016/017/SCI05 permission: stop retrospective causal use; surface only.
- No C9/C12 native consumer: stop B7 person proof; do not substitute a fixture.
- Missing required historical identity: source HOLD; do not invent line/function evidence.
- Conflicting owner/authority: HOLD that edge; continue unrelated lawful work.

**No implementation, no scientific issuance, no native grant, no self-adoption.**
