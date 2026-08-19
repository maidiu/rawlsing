# D15 — FINAL TARGET ARCHITECTURE

**Court:** Vozhd Trii D15 — Final Parent Architecture Synthesis  
**Repository:** `maidiu/rawlsing`  
**Exact base:** `bfda722ba89595cfeebed27bbfcbbe3f9d65195f`  
**Branch:** `agent/vozhd-trii-d15-parent-architecture-synthesis`  
**Production code modified:** `NO`

## 1. Selected architecture

D15 selects:

`C11 EMPIRICAL EVIDENCE REPOSITORY`
`+ EXACT EMPIRICAL QUERY ENGINE`
`+ AUTHORITY-BOUNDED AUTONOMOUS DISCOVERY SERVICE`
`+ EXACT ACTOR EMPIRICAL COMPARABILITY SERVICE`
`+ POSITIONED-SUBJECT EMPIRICAL POSSIBILITY SERVICE`
`+ SEPARATE STRUCTURAL EMPIRICAL ADMISSION SERVICE`
`+ REVALIDATED V553→V558 STRUCTURAL DAG`
`+ NEW DIRECT POSITIONED-SUBJECT POSSIBILITY → V3 DEVELOPMENTAL METABOLISM LANE`

This is the minimum architecture that preserves all D12 terminal capabilities while instantiating the D13 information family and using D14's freedom to remove nonterminal eager materialization.

The architecture is intentionally asymmetric:

- **C11 is durable deep empirical authority.**
- **EmpiricalFact is a canonical semantic query result but normally physically derivable.**
- **DiscoveryResultReceipt is durable when a discovered historical result/branch must be identified and replayed.**
- **PositionedSubjectEmpiricalPossibilityField is a canonical population-empirical semantic object, not actor state.**
- **StructuralEmpiricalAdmission is a canonical governed promotion receipt, not a generic survey→structure rule.**
- **V553–V558 remain structural/world-side.**
- **V3 remains the owner of life realization and now receives one additional non-structural upstream constraint lane.**

No existing V550/V550J table shape is selected as the canonical deep carrier.

## 2. Constitutional object separation

The following inequalities are architectural type boundaries, not documentation conventions:

```text
POPULATION EMPIRICAL FACT
!= POSITIONED-SUBJECT EMPIRICAL POSSIBILITY FIELD
!= V3 DEVELOPED / REALIZED DISPOSITION
!= ACTOR BELIEF / RESPONSE
```

```text
EMPIRICAL RESPONDENT COORDINATE
!= GENERATED ACTOR DEMOGRAPHIC / BIOGRAPHICAL FACT
!= GENERATED NINE-STRATUM STRUCTURAL POSITION
!= EMPIRICAL POSSIBILITY-FIELD CONDITIONER
```

```text
DISCOVERY AUTHORITY
!= DISCOVERY RESULT
!= MATERIALIZATION AUTHORITY
!= CACHE POLICY
```

```text
SOURCE SEMANTIC EQUIVALENCE
!= RESPONDENT IDENTITY LINKAGE
!= SAMPLE POOLING AUTHORITY
!= GENERATED ACTOR COMPARABILITY
```

The implementation campaign must enforce these through distinct object types/owners and negative-authority tests.

## 3. Physical C11 representation strategy

D15 selects the physical **representation strategy**, while deliberately leaving storage engine, codec, compression and production index implementation as benchmark-time choices because D14 did not establish live sizing.

### 3.1 Canonical physical core

The concrete C11 implementation SHALL be an **append-only, source-universe-scoped normalized incidence repository** with these physically authoritative families:

1. `EmpiricalUniverse` manifests;
2. scoped respondent identity;
3. `RespondentEvent` incidence;
4. `EmpiricalCoordinateFact` incidence;
5. `RoutingEligibilityFact` incidence or exact deterministic routing rule references;
6. `WeightMeasureFact` incidence;
7. immutable/content-addressed `AuthoritySnapshot` manifests;
8. source-universe relation/overlap/linkage authority;
9. content-addressed semantic-integrity/replay manifests.

A response event is the minimum generic response grain. A scalar respondent×question projection is allowed only when the exact source topology authority says the question is scalar-singular.

### 3.2 Physical partition law

Canonical incidence is partitioned first by exact `EmpiricalUniverse` identity, never by a harmonized alias that could merge distinct samples. Within a universe implementation may partition by wave/time/question family or another exact, lossless key.

Cross-universe respondent joins do not exist in the generic query path. They require a positive `SOURCE_UNIVERSE_RELATION_AUTHORITY` relation.

### 3.3 Semantic integrity

Every canonical partition/manfiest must bind a canonical semantic projection containing all applicable M01–M18 information. File hash alone or a hash over a convenience subset is not enough.

Authority objects are immutable/content-addressed. Historical facts and receipts dereference the exact authority snapshot that governed their production.

### 3.4 Source safety lane

Original source/native snapshots remain retained beside C11 until a per-source positive `SOURCE_TO_C11_EQUIVALENCE_CERTIFIED` receipt exists after D13B P01–P20, D12 T01–T18 and M01–M18 validation.

D15 does **not** authorize source deletion. It defines only the prerequisite proof after which a separate governance action may consider retirement.

## 4. Canonical semantic layer above C11

`CANONICAL_OBJECT_MODEL.csv` is dispositive. The minimum families are:

- `EmpiricalUniverse`
- `RespondentEvent`
- `EmpiricalCoordinateFact`
- `RoutingEligibilityFact`
- `WeightMeasureFact`
- `AuthoritySnapshot`
- `EmpiricalQuerySpec`
- `EmpiricalFact`
- `DiscoveryAuthority`
- `DiscoveryResultReceipt`
- `ActorComparatorReceipt`
- `PositionedSubjectEmpiricalPossibilityField`
- `StructuralEmpiricalAdmission`
- `ReplayReceipt`
- existing `ResolvedStructuralContext`
- new V3 boundary `V3EmpiricalPossibilityInput`

The model avoids separate canonical object families for unary distributions, pair clouds, recursive trees, branch signatures, position matrices, E3 networks or E4 metrics. Those are exact derived views, optional caches, diagnostics or superseded implementations.

## 5. Lane 1 — source / empirical ingest

```text
source-native evidence
+ questionnaire/instrument semantics
+ routing/topology authority
+ weight/design authority
+ normalization/crosswalk authority
        ↓
C11 source-universe-scoped incidence
        ↓
source→C11 equivalence receipt (only after proof)
```

The producer owns empirical preservation, not downstream structural or actor interpretation.

Typed ingest failures include unresolved native code, unknown topology, unavailable routing rule, invalid weight, missing authority and source-equivalence not certified.

## 6. Lane 2 — exact empirical query engine

`EmpiricalQueryEngine` owns exact evaluation of governed `EmpiricalQuerySpec` objects over C11.

It supports:

- distributions and prevalence;
- empirical-coordinate conditionals;
- arbitrary authorized conjunctions;
- response×coordinate conditionals/conjunctions;
- same-respondent pair joints;
- requested bounded k-way joints;
- branch/cohort-conditioned facts;
- branch-conditioned cotravel;
- temporal components;
- source-indexed comparison components;
- exact support/risk-set/measure/topology/typed absence.

The engine does **not** decide structural meaning, actor comparability, source applicability to a service, discovery coverage or actor development.

A fixed E1/E2 cache may answer only a bit-identical semantic query key. Otherwise execution falls back to C11.

## 7. Lane 3 — autonomous forward social discovery

D15 selects a two-mode service:

### `EXACT_BOUNDED`

For an authority-declared finite/finitely constructible candidate frontier, enumerate/evaluate every lawful candidate (or a mathematically proven coverage-equivalent computation) and exact-validate it through the query engine.

Only this mode may make generic **complete-for-declared-frontier** claims.

It must not require unary signal, so a declared arity-2 frontier can discover XOR/zero-unary interactions.

### `ADAPTIVE_EXPLORATORY`

For larger lawful frontiers, use priority/beam/screen/recursive proposals, but every emitted result is exact-validated. The receipt explicitly states the evaluated frontier and non-exhaustive coverage. Unevaluated candidates are not negative evidence.

Support pruning is lawful only when authority defines it as a feasibility boundary and the typed state remains visible. Cost alone cannot suppress a supported minority.

Recursive discovery is a traversal mode over exact cohort predicates, not a canonical tree object.

## 8. Lane 4 — actor empirical comparability

The comparator path is:

```text
objective generated actor demographic/biographical fact
        ↓
field/source/time-specific comparator authority
        ↓
exact empirical predicate OR typed failure
        ↓
ActorComparatorReceipt
```

Generated nine-stratum structural position is never the generic bridge.

Allowed comparator families are exact equality, versioned normalization/crosswalk, range/band match, historical geographic hierarchy, source-specific semantic equivalence and temporally conditional equivalence. All require explicit authority.

No fuzzy string, nearest geography, prevalence imputation, actor belief-as-affiliation or memory-as-objective-fact fallback is allowed.

## 9. Lane 5 — positioned-subject empirical possibility

```text
objective actor fact refs
        ↓ comparator receipts
exact empirical conditioner predicate(s)
        + source applicability authority
        + historical/source scope
        ↓
EmpiricalQueryEngine exact conditional/joint query
        ↓
support + uncertainty + source provenance
        ↓
PositionedSubjectEmpiricalPossibilityField[source universe]
        ↓
V3EmpiricalPossibilityInput
```

Multiple lawful source universes remain multiple source-indexed components by default. Disagreement is preserved. There is no generic averaging or backfill model.

Typed outcomes include actor property missing, no comparator, ambiguous comparator, source not applicable, temporal noncomparability, target unavailable, routed/not-asked, zero support, low support and uncertainty-unquantified.

No nearest-cohort fallback exists without separately created positive authority.

## 10. Lane 6 — structural empirical admission

The structural lane is deliberately separate:

```text
exact EmpiricalFact
        ↓
STRUCTURAL_EMPIRICAL_ADMISSION_AUTHORITY
        ↓
StructuralEmpiricalAdmission
        ↓
V553 temporal structural production
        ↓
V554 affordance
→ V555 mediation possibility
→ V556 pressure-flow topology
→ V557 publication
→ V558 StructuralPriorRepository/ContextResolver
```

An empirical fact may exist and be useful for discovery/reverse inference while structural admission is denied or absent.

Admission rules state exact structural target/relation/stratum/time, transformation meaning, negative authority and provenance. Generic association or prevalence does not become structural truth.

Current V551/V551J/V552/V552J paths become migration compatibility producers/adapters while their intended narrow structural semantics are re-expressed under this unified admission contract.

## 11. Lane 7 — V3 developmental metabolism

The corrected architecture does **not** move developmental semantics upstream.

V3 continues to own:

- generated structural position;
- opportunities;
- encounters;
- exposures;
- relationship/household/genealogy state;
- mediation realization;
- memory and accessibility;
- knowledge/belief;
- action/response;
- mobility;
- orientation-to-strata;
- pressure-flow realization;
- developmental attractors;
- path-dependent causal history.

V3 receives two noncollapsed upstream families:

```text
ResolvedStructuralContext
+
V3EmpiricalPossibilityInput
```

The possibility input constrains historically plausible proposal/configuration space under a new explicit V3 metabolism authority. It cannot set actor belief, response, identity, memory, knowledge or finished disposition directly.

Two actors can lawfully receive identical structural contexts and empirical possibility fields and develop differently because actual opportunities, encounters, relationships, choices, generated events and explicit randomness alter later causal history.

## 12. Downstream V553+ revalidation result

`V553_PLUS_REVALIDATION_MATRIX.csv` is dispositive.

### V553

**Jurisdiction survives. Upstream completeness does not.**

V553 remains the owner of temporal structural harmonization/comparability of already-governed structural evidence. The old V552/V552J intake was narrow but lawful. Target V553 gains a new direct/producer input: `StructuralEmpiricalAdmission` carrying exact `EmpiricalFact` and replay provenance.

V553 does not become a generic survey interpreter.

### V554 / V555 / V556

Their world-side structural affordance, mediation-possibility and pressure-flow jurisdictions remain independently lawful. They receive richer lawful upstream structural evidence through corrected V553, not a new survey lane.

### V557 / V558

Lossless structural publication and stage-blind structural resolution remain valid. Adapter/schema implementation may need version updates for V553 provenance, but reverse empirical possibility fields are **not** added to `StructuralPriorRepository`.

### V3

V3 causal jurisdiction remains correct, but its pre-correction input surface was incomplete for the corrected D12 target. A new direct-DAG `PositionedSubjectEmpiricalPossibilityField -> V3EmpiricalPossibilityInput` lane and V3 metabolism authority are required.

## 13. Materialization/cache architecture

D15 selects **C11-first exact replay with bounded semantic caches**.

Allowed cache classes:

- fixed exact E1;
- fixed exact E2/k-way contingency;
- branch member/predicate receipt;
- comparator receipt;
- source-indexed temporal/comparison component fact;
- positioned-subject field;
- E3/E4 diagnostic view.

Every cache key includes exact semantic query/result identity, C11 content identity and relevant authority/version identities. A cache miss falls back to exact replay. A cache can never become authoritative merely through frequent use.

E3/E4 are evictable diagnostics.

## 14. Deterministic replay

Historical replay binds:

- C11 semantic content identity;
- source-universe identity;
- exact authority snapshots;
- query/predicate/risk-set/measure/topology identity;
- comparator/admission/discovery authority;
- algorithm implementation/coverage contract where algorithm matters;
- deterministic tie/order rules;
- lawful RNG seed/state only where randomness is a semantic input.

A new authority version does not reinterpret an old receipt.

## 15. Negative authority / typed empty states

The architecture recognizes first-class states rather than synthesizing graceful guesses:

- `MISSING_AUTHORITY`
- `DENIED`
- `OUT_OF_SCOPE`
- `NONCOMPARABLE`
- `ACTOR_PROPERTY_MISSING`
- `NO_COMPARATOR`
- `AMBIGUOUS_COMPARATOR`
- `SOURCE_NOT_APPLICABLE`
- `TARGET_UNAVAILABLE`
- `NOT_ASKED`
- `INAPPLICABLE`
- `DK`
- `REFUSAL`
- `ZERO_SUPPORT`
- `OBSERVED_ZERO`
- `LOW_SUPPORT`
- `UNCERTAINTY_UNQUANTIFIED`
- `VALID_EMPTY`
- `COVERAGE_NOT_CLAIMED`
- `REPLAY_HASH_MISMATCH`
- `SOURCE_EQUIVALENCE_NOT_CERTIFIED`

## 16. Why this is smaller than preserving the current V550 suite

The current suite repeatedly materializes distributions, matrices, predictor summaries, secondary interactions, outlier summaries, recursive nodes, signatures, clouds, V550J aggregates and checkpoints.

The target retains one deep C11 empirical authority and computes exact semantic facts from it. Current branch/tree/cloud/signature shapes stop being parallel retained authorities. This removes duplicated materialization without deleting their lawful underlying empirical distinctions.

No production percentage saving is claimed.

## 17. Why this is richer than sparse predeclared conditionals

Sparse predeclared facts cannot answer a later authorized conjunction, k-way target, new branch/risk set, actor comparator, or autonomous candidate search. C11 preserves the respondent-bound future-selectable information frontier; `DiscoveryAuthority` defines a lawful search universe without naming the winner.

## 18. Why the historical persona shortcut does not return

Historical profile/covariance machinery contained a valuable observation: joint empirical configurations and position-conditioned cotravel matter. D15 preserves that information as exact population geometry and a positioned-subject **possibility field**.

The field never becomes actor identity or finished psyche. V3 remains necessary. Therefore the valid empirical insight survives while the shortcut is superseded.

## 19. Why independent marginals cannot flatten plurality

The exact query engine can reconstruct same-respondent pair and k-way support from C11. Reverse fields use exact requested joint geometry. Discovery can inspect conjunctions and branch-conditioned cotravel. Supported minorities remain supported even when weak.

No independent-marginal product is an authorized substitute for a requested joint field.

## 20. Why survey demographics do not become structural position

Survey coordinates remain `EmpiricalCoordinateFact`. Generated structural position remains CAN-006/ADP-009/V3 authority. Structural admission is a separate relation-specific authority. Actor comparability maps objective actor facts into empirical predicates without using generated structural position as bridge.

## 21. Why empirical possibility is not destiny

The field is source-indexed population evidence conditioned on exact comparable actor properties. It is upstream of V3 and lacks authority to create actor states. V3 history can push two otherwise equivalent subjects into different opportunities, relationships, exposures, meanings, actions and attractors.

## 22. Why source universes are not silently pooled

Universes are physical/canonical partition boundaries. Source applicability is service-specific. Joining, pooling, backfill and composition require explicit positive authority. Source-indexed disagreement is a legitimate result, not noise that the architecture is obliged to average.

## 23. Why autonomous discovery is governed without being designer-predeclared

Authority declares the candidate grammar, scope, complexity, risk set, measures, support/validation and coverage semantics. The algorithm evaluates lawful candidates and the data determine which candidate wins. Thus authority governs the *space*, not the answer.

## 24. Expensive work that remains intrinsically necessary

Depending on the authorized workload Rawlsing still must pay for:

- exact respondent-bound predicate/risk-set evaluation;
- same-respondent joins/binding;
- requested k-way joint support;
- topology/routing/typed absence;
- weight/design semantics;
- source-indexed replay;
- exact actor comparator resolution;
- exact discovery coverage promised by an authority;
- deterministic branch/result replay;
- structural admission provenance.

Architecture cannot optimize these away by erasing their semantic distinctions.

## 25. Expensive current work that may disappear or become optional after migration

After positive equivalence gates:

- repeated per-question independent scans can be shared/replaced by exact query plans;
- broad checkpoint/final materialization amplification can shrink;
- permanent secondary-summary and recursive-tree materialization can retire;
- attitude cloud can become diagnostic/on-demand;
- V550J fixed joints can become optional exact E2 caches;
- V551/V551J packet republishing can collapse into explicit EmpiricalFact + StructuralEmpiricalAdmission contracts;
- current shared substrate can retire after C11 equivalence, not before.

## 26. Claims still blocked until implementation benchmarking

D15 does not claim:

- production savings percentage;
- production wall time;
- production CPU/RSS/I/O;
- required hardware;
- physical bytes per C11 event/coordinate;
- cache hit rates;
- actual search frontier sizes/support pruning rates;
- actual reverse query arity/no-match rates;
- populated source equivalence;
- source-retention byte duplication.

These are implementation parameters/measurements, not discovery blockers.

## 27. Architecture theorem

The selected machine is smaller where current software duplicates **representations**, but not smaller where the historical world contains distinctions the finished person may need.

```text
SOURCE EVIDENCE
→ C11 EXACT EMPIRICAL WORLD
    ├─→ governed autonomous discovery
    ├─→ actor-comparable source-indexed empirical possibility
    │      └─→ V3 developmental metabolism
    └─→ separately governed structural admission
           └─→ V553→V558 structural world
                  └─→ V3 developmental metabolism
                           └─→ generated life
```

The two empirical downstream branches meet only in V3 history, where they remain distinct causal inputs.

**Selected result:** `ARCHITECTURE_SELECTED__IMPLEMENTATION_CAMPAIGN_READY`.
