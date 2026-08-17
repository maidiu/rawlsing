# Rawlsing Runtime-Prior Repository & Context Resolution — Cross-Cutting Architecture Exploration

**Status:** advisory terminal-consumer architecture exploration  
**Date:** 2026-08-17  
**Purpose:** make concrete how the additive V550–V558 semantic DAG becomes a runtime-consumable historical structural field for V3, especially for target persons born primarily in the 1980s/1990s and for their earlier-born parents.

## 1. Executive verdict

Rawlsing is already pointed toward the correct architecture, but one cross-cutting contract needs to become explicit before remaining maximal stage-architecture passes are treated as terminally grounded.

The offline V550–V556 chain should compile survey-derived and other governed evidence into a **normalized, authoritative structural-prior repository** whose semantic object families remain owned by their producing stages. V557 should preserve those runtime-authorized semantics while adding source/generated/rendered governance. V558 should act as the **runtime-prior linker / publication boundary**: it creates a hash-bound, stage-agnostic runtime repository with queryable indexes and a stable consumer contract. A read-only **Context Resolver** over that V558 repository materializes the structural field applicable to a generated actor at a particular time, place, and set of already-generated structural positions. V3 consumes only that stable context interface; it does not know or care which prior originated in V552, V553, V554, V555, or V556.

The central shape is:

```text
GOVERNED SURVEY / SOURCE EVIDENCE
        ↓
V550–V552/J  evidence, semantics, structural facts, permission
        ↓
V553         temporal relations and temporal limits
        ↓
V554         bounded mediation-input eligibility / requirements / limits
        ↓
V555         structural mediation paths and conditions
        ↓
V556         typed structural pressure-flow multigraph + attractor prerequisites
        ↓
V557         lossless runtime-authorized preservation + generation/rendering governance
        ↓
V558         runtime-prior linker / canonical publication
        ↓
STRUCTURAL PRIOR REPOSITORY
        ↓
Context Resolver(query_time, location, generated_position_state)
        ↓
ResolvedStructuralContext
        ↓
V3 developmental runtime
```

The previous Wave-0 R0-04 result already anticipated the key endpoint: V558 should expose both an immutable hash-bound runtime-prior bundle/manifest and queryable slices keyed by temporal scope, geography/scope, stratum/relation, and supported actor-seed scope. The missing piece is the concrete **resolution law** that turns those indexed priors into the context for “this actor, here, now.”

## 2. Operating population envelope

The intended normal product regime is not arbitrary historical person generation.

Primary target:
- target persons born predominantly in the **1980s and 1990s**;
- later cohorts naturally supported as coverage expands;
- earlier target births allowed at explicitly reduced historical fidelity.

Important genealogical consequence:
- a target actor born in 1990 may have parents born in 1955–1970;
- therefore pre-survey-birth resolution is required even for ordinary target-person generation;
- those parents may begin with a proxy childhood structural context and then move into much better observed structural contexts during adolescence/adulthood as survey coverage begins.

Rawlsing should therefore support older birth dates without claiming equal fidelity.

## 3. The completed offline product is a repository, not one giant stage payload

Under the governed DAG model, semantic completeness lives across authoritative object families.

V552 remains authoritative for structural pressure facts. V553 remains authoritative for temporal relations/limits. V554 owns its bounded eligibility/requirement meaning. V555 owns structural mediation-path possibility. V556 owns pressure-flow topology and attractor prerequisites. Later stages do not need to serialize every earlier meaning into their own object.

The runtime-facing build must therefore perform **linking**, not another semantic inference pass.

### 3.1 Logical V558 StructuralPriorRepository

The V558 runtime publication should expose a stage-agnostic repository whose logical collections include at minimum:

- structural pressure priors;
- structural-position / stratum references required for causal applicability;
- temporal observations/relations/limits;
- bounded structural affordances / eligibility / requirements;
- structural mediation paths and route conditions;
- pressure-flow nodes, edges, interactions and attractor prerequisites;
- Absolute-Horizon-relevant structural prior references where lawful upstream authority exists;
- typed negative authority / known absence / unresolved / denied / noncomparable states;
- item-level epistemic class, causal-use permission, uncertainty/completeness and provenance;
- geographic and temporal scope indexes;
- canonical artifact/producer lineage and content hashes.

This can be implemented with canonical Parquet/index tables, DuckDB, or another storage mechanism later. The architecture should specify information and query behavior, not prematurely choose a database engine.

### 3.2 V3 must be stage-blind

V3 should never perform calls conceptually equivalent to:

```python
load_v552(...)
load_v553(...)
load_v555(...)
```

V3 should consume only a stable runtime interface such as:

```text
StructuralPriorRepository
ResolvedStructuralContext
```

The V558 linker may denormalize selected fields for runtime efficiency, but every copied value retains a stable reference to its authoritative semantic object and hash-bound provenance.

## 4. Two distinct runtime artifacts

There should not be one static “birth prior” that permanently defines the actor's world.

### 4.1 StructuralPriorRepository

Immutable per build/version. It contains the full queryable historical structural model available to runtime.

### 4.2 ResolvedStructuralContext

A deterministic, reproducible resolved view for a particular runtime state:

```text
query_time
+ geographic location / geographic path
+ already-generated actor structural positions
+ household/family/relationship positions where generated
+ other applicability facts that V3 has lawfully generated
→ applicable structural prior slice
```

V3 may receive successive contexts over a life as time, residence and generated positions change.

## 5. Context Resolver input contract

Minimum query input:

```text
ContextQuery {
    repository_bundle_id,
    query_time,
    location,
    generated_position_bindings,
    actor_generation_phase,
    optional household/family bindings,
    deterministic resolution policy version
}
```

### 5.1 Location

The resolver should map a runtime location to a canonical geographic path such as:

```text
Planetary
→ applicable Imperial Block / macro-region if governed
→ Nation State
→ Sub-national Region if governed
→ locality/neighborhood scope if governed
```

A national prior applies to an actor in Tyre **as a Nation-State-stratum prior**. It does not become a Tyre-local estimate.

Missing lower-level coverage remains missing lower-level coverage.

### 5.2 Generated position bindings

Many important structural positions cannot be derived from location alone:

- sect / ethno / class position;
- party / movement affiliation or relation;
- household position;
- family position;
- occupation and institutional positions;
- actor-specific Self-stratum state.

The resolver must therefore support progressive binding.

Before V3 has generated a position, conditioned priors requiring it remain `UNBOUND_REQUIRES_RUNTIME_POSITION` or equivalent. They do not become active causal priors by geographic guesswork.

After V3 generates the position, it re-resolves the context and those priors may become applicable.

## 6. Two-phase initialization solves the apparent circularity

To generate an actor, Rawlsing may need distributions/constraints that help generate positions; but some priors require those positions in order to apply.

Use two phases.

### Phase A — environmental / position-generation context

Query only by time, geography, generation role and already-known non-actor facts.

Returns:
- unconditioned or broadly conditioned structural priors;
- lawful position-generation constraints/distributions;
- higher-strata context;
- unresolved conditional prior families.

V3/genealogy uses those to generate the actor's concrete runtime positions.

### Phase B — position-bound actor context

Re-query with generated positions.

Returns:
- position-specific structural pressures;
- mediation possibilities;
- applicable pressure-flow subgraph;
- Horizon-relevant context where lawful;
- typed limits/unknowns.

This is how the runtime avoids turning survey categories into predetermined biography while still using the population evidence to constrain generation.

## 7. Temporal resolution law

This is the most important missing specification.

The semantic compiler and the runtime resolver have different jurisdictions.

**V553 says what was actually observed/comparable and what temporal relation is lawfully derived.** It must never pretend a survey value observed in 1985 was observed in 1960.

**The runtime resolver may choose an observed object as a generation proxy for an unobserved time**, provided the proxy status is explicit and the original temporal authority remains unchanged.

### 7.1 Per-prior-key resolution order

For each required semantic key at runtime query time `T`:

#### Mode 1 — `DIRECT_TEMPORAL_SUPPORT`

Use an object whose governed validity/observation support includes `T`.

This is the highest-fidelity mode.

#### Mode 2 — `LATEST_PRIOR_OBSERVATION_PROXY`

If no direct support contains `T`, select the latest lawfully usable observation **before** `T`.

Record:
- `anchor_time`;
- `query_time`;
- `staleness_lag`;
- `resolution_mode = LATEST_PRIOR_OBSERVATION_PROXY`;
- any V553 temporal limits or later known relation context.

This is a runtime approximation policy, not a claim that the earlier value persisted unchanged.

No interpolation is performed.

#### Mode 3 — `EARLIEST_POST_QUERY_PROXY`

If no usable observation exists at or before `T`, select the earliest lawfully usable observation **after** `T`.

This is the critical pre-coverage mode for an actor/parent born before the survey era.

Record:
- `anchor_time`;
- `query_time`;
- `forward_anchor_lag`;
- `resolution_mode = EARLIEST_POST_QUERY_PROXY`;
- explicit `historical_observation_at_query_time = false`;
- a reduced-fidelity / proxy status.

For birth initialization this may also be described as `EARLIEST_POST_BIRTH_ANCHOR`.

The future observation remains evidence about its actual observation period. The resolver merely uses it as the closest available governed structural proxy for generation.

#### Mode 4 — `NO_LAWFUL_TEMPORAL_ANCHOR`

If no applicable observation exists in the repository, return typed missing authority. Do not invent a zero, neighboring-country value or synthetic temporal estimate.

### 7.2 No numerical interpolation by default

Between survey observations, the resolver does not linearly interpolate structural pressure values unless some later explicitly governed rule authorizes that semantic operation.

V3 may therefore see stepwise context changes at new observation/relationship boundaries rather than a fake smooth annual series.

### 7.3 V553 relations still matter

Even when a proxy anchor is selected, V553 temporal objects remain attached:

- known drift/delta between observations;
- gaps;
- noncomparability;
- rupture candidates where governed;
- missing temporal authority.

The resolver's selection policy does not overwrite V553's epistemic state.

### 7.4 Avoid future leakage after coverage begins

After an actor's historical timeline reaches the first observed period, default resolution should prefer information observed at or before the simulated time rather than selecting a later wave merely because it is numerically closer.

The only intentional look-forward rule is the pre-coverage fallback where no prior observation exists.

## 8. Birth and life-course behavior

For an actor born at `B`:

1. Resolve the birth context per prior key.
2. For keys with earlier/direct observations, use those under their proper modes.
3. For keys with no pre-birth observation, attach the earliest post-birth observation as a marked proxy.
4. Record the per-key observation/proxy lag in the context coverage report.
5. As simulation time crosses governed observation/change boundaries, re-resolve affected keys.
6. As the actor's location or generated positions change, re-resolve affected spatial/position-conditioned keys.

V3 should not need to poll the entire repository every simulated year.

The resolver can expose a `next_context_change_time` or `ContextChangeSchedule` derived from:
- applicable observation boundaries;
- V553 temporal relation endpoints;
- runtime migration/residence changes;
- generated class/household/family/party/institution position changes;
- other applicability events.

## 9. Genealogical recursion

The same resolver contract applies recursively to parents, partners and children.

Example:

```text
Target child born 1990
    ↓
Parent 1 generated, birth 1961
    ↓
1961 early-life context uses earliest post-birth proxies where needed
    ↓
parent development enters 1980s survey era → fidelity improves
    ↓
Parent 2 generated similarly
    ↓
encounter / relationship / household formed from generated histories
    ↓
child born 1990
    ↓
child receives historically situated structural context
    + generated household/family environment caused by the parents' actual runtime histories
```

The survey repository never says “the child's father believed X.”

It says which structural fields and mediation possibilities were available. V3 creates the parents' actual histories. Those histories become generated causal facts for the child's environment.

## 10. Spatial resolution law

There should be **hierarchical applicability**, not geographic value substitution.

Given a query location:

- Planetary priors apply at Planetary stratum where authority exists.
- Imperial-block/macro-region priors apply at that stratum where authority exists.
- Nation-state priors apply to the actor as member/resident of that national structural context.
- Subnational priors apply only when that scope is governed and geographically applicable.
- locality/neighborhood priors apply only where corresponding authority exists.

Never implement:

```text
missing Tyre value → copy Lebanon national value and relabel it Tyre
```

Instead:

```text
Nation State: PRESENT
Sub-national Region: PARTIAL / MISSING
Neighborhood: MISSING
```

This preserves the nine-strata logic instead of turning “backoff” into false local precision.

## 11. Runtime context output contract

A useful logical output is:

```text
ResolvedStructuralContext {
    context_id,
    repository_bundle_id,
    actor_or_generation_subject_id,
    query_time,
    geographic_path,
    generated_position_bindings,

    selected_priors: [...],
    structural_pressures: [...],
    temporal_relations: [...],
    mediation_paths: [...],
    pressure_flow_subgraph: {...},
    attractor_prerequisites: [...],
    horizon_context: [...],
    negative_authority: [...],

    selection_ledger: [...],
    coverage_profile: {...},
    next_context_change_time,
    resolver_policy_version
}
```

Each selected prior carries or references:
- authoritative `prior_id` / semantic object ID;
- producer-layer provenance hidden behind the V558 consumer abstraction;
- epistemic class;
- causal-use permission;
- temporal support;
- geographic/structural scope;
- resolution mode;
- proxy/staleness lag where applicable;
- typed uncertainty/absence/noncomparability.

## 12. Selection ledger is mandatory

Every context should be explainable after the fact.

For each selected or rejected candidate prior:

```text
SelectionRecord {
    semantic_key,
    candidate_prior_id,
    decision,
    resolution_mode,
    anchor_time,
    query_time,
    temporal_lag,
    geographic_scope,
    position_bindings_used,
    authority_state,
    causal_use_permission,
    rejection_or_limit_reason
}
```

This permits deterministic replay and prevents a runtime bug from silently choosing a convenient but unauthorized survey row.

## 13. Fidelity / coverage model

Do not hardcode a universal claim that “1980 is the high-fidelity cutoff.” Coverage differs by source, country, stratum and semantic family.

Instead compute a **context coverage profile** from objective resolution facts.

Suggested fields:

- birth-anchor lag distribution;
- fraction/count of priors under `DIRECT_TEMPORAL_SUPPORT`;
- fraction/count under `LATEST_PRIOR_OBSERVATION_PROXY`;
- fraction/count under `EARLIEST_POST_QUERY_PROXY`;
- maximum and median proxy lag;
- number of applicable strata with governed coverage;
- structural relation / mediation / pressure-flow family coverage;
- typed missing/noncomparable/unresolved counts;
- observation density over formative/developmental periods.

User-facing release language can then be derived after a corpus coverage audit, for example:

> Rawlsing can generate earlier cohorts using the earliest available post-birth structural evidence, but historical fidelity improves materially for cohorts whose formative years overlap the survey archive.

A more precise year/cohort statement should be calculated from the actual coverage index rather than encoded as architecture folklore.

## 14. What this means for the remaining stage architecture passes

This cross-cutting consumer architecture should become explicit terminal demand for the Noviy Vozhd Dva passes.

### V553 must ensure

- ordered, stable temporal observation identity per structural semantic key;
- exact temporal scope/reference identity;
- zero/missing/noncomparability distinctions;
- temporal relation and limit objects usable by the resolver;
- no ungoverned interpolation;
- enough structural/stratum/source-target references to resolve applicability later without rematching descriptive text.

The resolver particularly needs to be able to enumerate “all lawful observations for semantic key K, ordered through time.”

### V554 must ensure

- bounded mediation-input eligibility and requirements remain linked to exact structural/temporal objects;
- applicability/position requirements are machine-resolvable;
- unresolved runtime-position requirements remain explicit;
- no actor fact is created merely to make an affordance selectable.

### V555 must ensure

- typed structural mediation paths and conditions;
- source/receiving structural-position refs;
- geographic/temporal applicability;
- runtime-position prerequisites;
- buffer/amplify/block/deflect/reroute semantics only where governed;
- no generated parent/household history.

### V556 must ensure

- machine-routable typed multigraph;
- edge/interaction/prerequisite IDs;
- temporal and structural applicability;
- source/target strata;
- mediation linkage;
- actor-history requirements;
- explicit attractor-prerequisite topology without final actor type.

### V557 must ensure

- lossless preservation of every runtime-authorized semantic object needed by V3;
- addition of source/generated/rendered separation and runtime-use governance;
- no reduction to readiness/blocker prose.

### V558 must ensure

V558 is the likely owner of the **linker/publication boundary**:

1. resolve stage-owned semantic objects into stage-agnostic runtime prior collections;
2. bind them by hash/version/provenance;
3. build temporal/geographic/stratal/position query indexes;
4. expose the stable `StructuralPriorRepository` contract;
5. define or ship the read-only deterministic `ContextResolver` policy/API;
6. produce context snapshots/selection ledgers in a form V3 can consume/replay;
7. never add actor biography, psyche, dialogue, memory, or final attractor identity.

No V559 is currently justified. If later architecture proves offline linking and runtime resolution are operationally separate modules, they can still both belong to the V558→V3 boundary contract.

## 15. What V3 then owns

V3 receives a resolved structural context, not survey artifacts.

V3 owns:
- generated actor initial conditions;
- generated structural positions where not fixed externally;
- actual exposure/encounter history;
- absorption/resistance/reproduction/rerouting history;
- relationship and household events;
- orientation-to-strata formation;
- vitality/need/desire interaction with the structural field;
- wounds, expectations, strivings, shame/pride/debt/resentment where lawfully produced by history;
- actual pressure-flow traversal;
- reinforcement/destabilization and path dependence;
- Enneagram-like attractor emergence/evolution;
- explicit causal event/state history.

When V3 changes residence or structural position, it re-queries the context resolver rather than rewriting the structural repository.

## 16. Key architecture laws discovered in this exploration

### Law A — evidence time and runtime proxy time are different

A runtime proxy never changes the source observation date.

### Law B — forward proxy is a generation policy, not temporal semantic authority

Using a 1981 observation to initialize a person born in 1960 may be allowed by the runtime generation policy, but V553 must continue to report 1960 as unobserved.

### Law C — runtime addressability does not imply empirical coverage

The resolver should return a valid typed context response for supported generation queries even when parts of the context are missing/proxy-based.

### Law D — higher-stratum applicability is not geographic imputation

A national prior can apply to a person in a locality as a national-stratum influence without being relabeled as a local estimate.

### Law E — actor positions are progressively generated and progressively bind priors

Unknown sect/class/party/household/family positions must not be guessed merely to complete a context.

### Law F — V3 depends on structural-prior interfaces, not surveys or stage numbers

This is the abstraction that makes the eventual runtime maintainable and source-extensible.

### Law G — genealogy makes pre-coverage resolution part of the ordinary path

1980s/1990s target-person generation naturally requires earlier-born-parent contexts.

## 17. Architecture verdict

**CURRENT DIRECTION:** correct.

**MAJOR MISSING CROSS-CUTTING SPECIFICATION:** deterministic context resolution policy over V558 queryable priors, especially temporal proxy selection, progressive actor-position binding, context refresh triggers and fidelity reporting.

**RECOMMENDED PROJECT ACTION:** treat this exploration as terminal-consumer demand before further maximal V553–V558 architecture is frozen. It does not require reopening upstream evidence semantics. Instead, every remaining architecture pass should prove that its stage emits/preserves what the V558 linker and context resolver require.

**IMPLEMENTATION SEQUENCING:** no need to implement the resolver now. Finish terminal-demand-aware stage architecture with this contract visible, complete V553–V558 semantics, then build V558 linker/repository/resolver before implementing full V3 evolution.

**NO NEW STAGE REQUIRED:** current evidence supports V558 as the natural linker/runtime-prior publication boundary, with the Context Resolver as its runtime-facing read-only consumer surface unless a later architecture pass demonstrates a genuine jurisdictional split.
