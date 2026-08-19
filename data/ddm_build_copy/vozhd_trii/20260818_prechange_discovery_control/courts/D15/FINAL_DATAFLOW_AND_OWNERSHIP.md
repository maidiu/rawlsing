# D15 — FINAL DATAFLOW AND OWNERSHIP

## 1. Governing ownership rule

Each semantic transformation has exactly one owner. Later stages may direct-DAG reuse earlier producer-owned objects; they do not acquire authority merely by transporting them.

```text
SOURCE EVIDENCE
  ↓ SourceIngest / EmpiricalEvidenceRepository
C11 EMPIRICAL INCIDENCE + AUTHORITY
  ├──────────────────────────────────────────────────────────────┐
  │                                                              │
  │ exact query                                                  │ exact query
  ↓                                                              ↓
EmpiricalQueryEngine                                      EmpiricalQueryEngine
  │                                                              │
  ├─→ DiscoveryService                                          ├─→ ActorComparabilityService
  │    DiscoveryAuthority                                       │    ActorComparatorReceipt
  │    ↓ data selects                                            │          ↓
  │    DiscoveryResultReceipt                                   │    PossibilityFieldService
  │                                                              │          ↓
  └─→ StructuralEmpiricalAdmissionService                       │    PositionedSubjectEmpiricalPossibilityField
       ↓                                                         │          ↓ direct DAG
       StructuralEmpiricalAdmission                              │    V3EmpiricalPossibilityInput
       ↓                                                         │          ↓
       V553 temporal structural prior                            │    V3 developmental metabolism
       ↓                                                         │
       V554 structural affordance                                │
       ↓                                                         │
       V555 structural mediation possibility                     │
       ↓                                                         │
       V556 pressure-flow topology                               │
       ↓                                                         │
       V557 lossless publication                                 │
       ↓                                                         │
       V558 StructuralPriorRepository / ContextResolver          │
       ↓ ResolvedStructuralContext ──────────────────────────────┘
                         ↓
                         V3 actor-specific history
                         ↓
                         GeneratedPersonRecord
                         ↓
                         V2 phenomenology/expression
                         ↓
                         LLM rendering
```

## 2. Lane ownership

### SourceIngest / EmpiricalEvidenceRepository

**Owns:** faithful normalized preservation of source-native empirical information and M01–M18 physical authority closure.

**May create:** EmpiricalUniverse, RespondentEvent, EmpiricalCoordinateFact, RoutingEligibilityFact, WeightMeasureFact, source semantic/lineage/replay manifests.

**Does not own:** statistical discovery significance, structural meaning, actor comparability, actor state.

### EmpiricalQueryEngine

**Owns:** exact evaluation of a governed empirical predicate/target/risk-set/measure/topology against C11.

**Creates:** EmpiricalQuerySpec identity; EmpiricalFact or typed query failure.

**Does not own:** whether a fact should be searched for, whether it is structurally meaningful, whether an actor property is comparable, whether it becomes actor state.

### DiscoveryService

**Owns:** authority-bounded candidate construction, search execution, exact validation, coverage/replay receipt.

**Creates:** DiscoveryAuthority and DiscoveryResultReceipt/branch receipt.

**Does not own:** structural promotion or actor identity.

### ActorComparabilityService

**Owns:** exact generated objective fact -> empirical conditioner comparability.

**Creates:** ActorComparatorReceipt or typed no-match/ambiguity/noncomparability.

**Does not own:** structural position or actor belief.

### PossibilityFieldService

**Owns:** source-indexed exact conditional/joint population possibility field for a lawfully comparable generated subject.

**Creates:** PositionedSubjectEmpiricalPossibilityField.

**Does not own:** actor state, source pooling, structural interpretation.

### StructuralEmpiricalAdmissionService

**Owns:** explicit empirical fact -> structural interpretation/use admission.

**Creates:** StructuralEmpiricalAdmission with target structural relation, temporal/use scope, transformation authority and negative limits.

**Does not own:** generated structural position, mediation realization or actor psyche.

### V553

**Owns:** temporal structural binding/harmonization/comparability of already-governed structural inputs.

**New target intake:** StructuralEmpiricalAdmission + exact empirical fact/replay references.

**Does not own:** generic survey interpretation or reverse subject possibility.

### V554

**Owns:** bounded structural affordance/applicability relative to generated structural position/context.

**Does not own:** opportunity/encounter/exposure occurrence or survey comparator mapping.

### V555

**Owns:** structural mediation-route candidates/conditions.

**Does not own:** realized actor mediation/history.

### V556

**Owns:** world-side pressure interaction, pressure-flow topology and attractor prerequisites.

**Does not own:** actor routing, final attractor/personality, belief or action.

### V557

**Owns:** lossless mixed-producer structural publication preserving producer identity.

**Does not own:** reinterpretation or generic transport of non-structural possibility fields.

### V558

**Owns:** immutable StructuralPriorRepository + deterministic read-only ContextResolver -> ResolvedStructuralContext.

**Does not own:** actor state or reverse empirical possibility field.

### V3

**Owns:** generated structural position and all actor-specific developmental causality: opportunity, encounter, exposure, relationship, mediation realization, memory, knowledge/belief, action/response, orientation-to-strata, path dependence and attractor formation.

**Inputs:** ResolvedStructuralContext and new V3EmpiricalPossibilityInput remain distinct.

**Does not own:** source empirical truth or structural evidence production.

### V2

Unchanged by D15. Owns phenomenological/expression/session membrane over lawfully accessible actor state. Rendered language remains noncausal until explicit V3/world admission.

## 3. Direct-DAG rules

1. C11 remains directly reachable by EmpiricalQueryEngine; no intermediate V550 artifact is required.
2. StructuralEmpiricalAdmission references its exact EmpiricalFact/C11 replay identity rather than copying all respondent incidence downstream.
3. V553–V558 retain direct upstream producer references where their existing architecture already requires them.
4. PositionedSubjectEmpiricalPossibilityField bypasses V553–V558 and enters V3 through its own typed boundary.
5. V3 objective actor facts are referenced by ActorComparabilityService; comparator resolution does not route through generated structural position.
6. V557/V558 remain structural repositories and are not expanded into generic all-prior containers.

## 4. Epistemic classes

```text
C11 source/empirical evidence
!= EmpiricalFact
!= StructuralEmpiricalAdmission / structural prior
!= PositionedSubjectEmpiricalPossibilityField
!= V3 generated runtime fact/state
!= actor-accessible memory/knowledge/belief
!= V2 rendered expression
```

Every boundary object carries an epistemic class and producer identity. Downstream consumers may use only permissions attached to that class/authority.

## 5. Negative authority routing

Typed failures terminate at the owner that can lawfully know the failure:

- source semantics unresolved -> SourceIngest;
- query unauthorized/risk set unavailable -> EmpiricalQueryEngine;
- candidate outside discovery frontier -> DiscoveryService;
- actor fact missing/no comparator/ambiguity -> ActorComparabilityService;
- source not applicable/zero support/target unavailable -> PossibilityFieldService;
- structural promotion missing/denied -> StructuralEmpiricalAdmissionService;
- actor did not encounter/know/remember -> V3;
- actor cannot lawfully express/claim -> V2.

No later stage fills an earlier typed absence by inference unless an explicit authority owns that transformation.

## 6. Downstream revalidation checksum

- **V553:** semantic jurisdiction retained; new admitted-evidence producer/input required.
- **V554:** semantic jurisdiction retained; corrected V553 supply; no reverse-field input.
- **V555:** semantic jurisdiction retained; no reverse-field input.
- **V556:** semantic jurisdiction retained; no reverse-field input.
- **V557:** publication semantics retained; adapter-only changes if producer object versions change.
- **V558:** resolver semantics retained; structural repository remains structural-only.
- **V3:** developmental jurisdiction retained; new direct empirical-possibility input and metabolism authority required.

The exact classification is in `V553_PLUS_REVALIDATION_MATRIX.csv`.
