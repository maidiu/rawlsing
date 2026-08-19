# D13 — MINIMUM INFORMATION SUBSTRATE SPECIFICATION

**Court:** Vozhd Trii D13  
**Status:** `PHYSICAL_INFORMATION_SPECIFICATION__NO_ARCHITECTURE`  
**Selected information family:** `MINIMUM_NORMALIZED_RESPONDENT_EVENT_COORDINATE_INCIDENCE_PLUS_AUTHORITY_PROVENANCE`

This document specifies physical **information content**, not a database schema, API, stage boundary, cache strategy, migration, or production architecture.

## 1. Selection theorem

The smallest information-equivalent family justified by the accepted evidence is:

```text
complete governed respondent-event incidence
+ complete empirically conditionable respondent-coordinate incidence
+ exact respondent-universe/source identity
+ routing/applicability/risk-set semantics
+ response topology/event multiplicity/order semantics
+ raw/governed weight and measure authority
+ source-native-to-canonical semantic/normalization authority
+ cross-universe derivation/linkage/overlap authority
+ actor-fact comparator authority and replay receipts
+ discovery/branch replay authority
+ empirical-predicate / structural-admission / replay provenance
```

The information may be physically partitioned, normalized, content-addressed, or represented by another injective encoding. D13 selects no table layout.

The defining condition is **injectivity with respect to every D12 R01-R14 distinction and every D13B P01-P20 proof dimension**.

## 2. Why respondent-*event* incidence is the minimum deep grain

A scalar `respondent_id × question` row is not a generally sufficient grain.

D12 requires exact replay of:

- multiselect sets;
- repeated responses/events;
- ranked/ordered responses;
- routed and not-asked states;
- same-respondent k-way response geometry;
- future respondent-bound conditionals and conjunctions.

Therefore the retained representation must distinguish lawful response events/components whenever the source topology permits more than one event per respondent/question. If a source/question is authoritatively scalar-singular, the event dimension may collapse to one canonical event for that question. The collapse is lawful only because topology authority proves singularity, not because current data happen to show one row.

## 3. Physically necessary information atoms

### M01 — Respondent-universe identity

Every empirical incidence must be bound to an exact universe identity sufficient to distinguish at least:

- source family / raw source identity;
- study/product/release identity;
- questionnaire/instrument release;
- country/geography and sampling geography;
- raw wave;
- canonical wave where governed;
- field/reference time;
- target population and sample frame where known;
- sampling/design regime identity;
- respondent namespace;
- source artifact/import lineage;
- harmonization authority identity.

A canonical source/wave alias cannot replace raw identity.

### M02 — Respondent identity within universe namespace

Retain an exact respondent key scoped by M01.

If physical respondent identifiers are normalized or replaced, retain an explicit bijective identity map proving equivalence. Count equality is not sufficient.

Cross-universe string equality is not person linkage.

### M03 — Question / variable native and canonical identity

For every response/routing/coordinate event retain or dereference:

- source-native question/variable identifier;
- instrument/question version;
- canonical question identity where authorized;
- component/subitem identity where applicable;
- semantic authority/version/content hash.

Canonical equality may not erase native instrument identity.

### M04 — Response-event identity and value

For every governed response event retain enough information to distinguish:

- scoped respondent;
- question/component;
- event group where a source answer comprises several components;
- event ID or deterministic event index;
- raw/source-native response code/value;
- normalized/canonical response value where governed;
- source-to-canonical value transform authority.

### M05 — Response topology and multiplicity

Retain or dereference exact topology authority and event-specific topology fields sufficient to distinguish:

- scalar singular response;
- unordered multiselect set;
- ordered sequence;
- repeated event/measurement;
- ranked response;
- routed response structure;
- componentized response.

When order is semantic, retain explicit rank/index. When order is non-semantic, physical ordering may be normalized.

### M06 — Typed response / absence state

Retain enough respondent-question-event state to distinguish at minimum:

- substantive response;
- missing/blank where semantically defined;
- DK;
- refusal;
- IAP/inapplicable;
- not asked;
- other source-specific special states;
- invalid/unresolved source code;
- zero-support outcome versus absent respondent eligibility.

Absence of a stored substantive response is not itself a typed state.

### M07 — Routing / applicability / risk-set incidence

For every question/risk-set family that may be lawfully queried, retain or reconstruct exact respondent eligibility/applicability from:

- respondent-question routing/applicability state or an information-equivalent deterministic rule;
- exact rule/authority version;
- source/question topology;
- any parent-answer predicates required by routing.

This information must permit exact member-set replay for new authorized risk-set predicates. Equal denominators with different members are different facts.

### M08 — Empirical-coordinate incidence

For every coordinate inside the future-authorizable empirical frontier retain, at respondent grain or information-equivalent grain:

- scoped respondent identity;
- source-native coordinate identity;
- governed canonical coordinate identity where one exists;
- raw/native coordinate value;
- canonical/normalized value where governed;
- unit/category/taxonomy identity;
- effective/reference time when temporally varying;
- typed unknown/missing state;
- normalization/crosswalk authority/version/hash;
- source-specific semantic authority.

The retained coordinate universe cannot be limited solely to today's fixed V550 `INDICATOR_FIELDS` if D12's future-authorized frontier includes additional lawful source coordinates.

Empirical coordinates remain distinct from generated nine-stratum structural position.

### M09 — Weight / measure facts and design authority

Where weighted empirical measures are governed, retain:

- scoped respondent;
- weight basis ID;
- exact weight value;
- weight status/validity;
- weight variable/source identity;
- sampling/design/estimand authority needed to interpret the weight;
- any governed recalibration/normalization rule and version.

Missing/invalid weights must yield a typed unavailable weighted result unless separate authority defines another treatment. `1.0` is not a lawful generic fill value.

Raw measure remains separately reconstructible.

### M10 — Source-native semantic and transformation authority

The physical information family must retain or immutably dereference the exact authority snapshots needed to interpret M01-M09, including as applicable:

- source questionnaire/instrument semantics;
- response scale/value mapping;
- routing logic;
- topology law;
- native-to-canonical question mapping;
- coordinate/value crosswalks;
- wave/source/country normalization;
- missing/special-state semantics;
- measure/weight interpretation.

A raw byte archive without M10 is not an exact empirical replay substrate.

### M11 — Cross-universe relation and double-counting provenance

Retain explicit authority/provenance for any relationship among empirical universes, including:

- independent/distinct by default;
- exact respondent/person linkage;
- namespace mapping;
- panel/repeated-observation linkage;
- constituent/pooled relation;
- original/derived/harmonized relation;
- sample overlap/nonoverlap evidence;
- pooling authority;
- backfill authority;
- harmonization authority;
- deduplication/one-count rule.

The absence of such authority means universes remain distinct.

### M12 — Empirical predicate grammar and replay identity

Retain the versioned predicate grammar/operator semantics used to build D08-compatible empirical predicates.

For a materialized fact, structural admission, comparator receipt, or recorded discovery result retain:

- typed predicate AST or an exact content-addressed reference;
- canonical predicate hash;
- coordinate/question/value identities used by the AST;
- risk-set identity;
- target identity;
- scope identity;
- measure basis.

Not every future predicate must be materialized; it must be constructible and evaluable over M01-M11.

### M13 — Actor-fact -> empirical-conditioner comparator authority

The empirical retention family must retain or immutably dereference the field/source/time-specific comparator rules required by D12D, including when used:

- actor fact type/owner authority;
- empirical coordinate target;
- exact equality rule;
- versioned normalization/crosswalk;
- range/band semantics;
- geographic hierarchy;
- source-specific semantic equivalence;
- temporal alignment;
- no-match and ambiguity semantics;
- comparator rule ID/version/hash.

For replay of a past reverse query retain a comparator receipt containing the actor fact ref/hash and effective time, rule identity, resolved empirical predicate, cardinality/ambiguity result, and source scope. Full actor-state storage is outside D13 jurisdiction.

Generated structural position is not a substitute for M13.

### M14 — Branch / cohort and autonomous-discovery replay provenance

Permanent branch-row materialization is not required if exact branch membership is deterministically replayable.

For any discovered branch/result whose exact historical identity must be replayed, retain or immutably dereference enough to reproduce:

- discovery/search family identity;
- authority-bounded candidate universe;
- predicate/composition grammar;
- source/universe/risk-set/topology/measure scope;
- algorithm implementation/version/content identity;
- coverage/pruning contract;
- deterministic parameters/tie rules;
- RNG seed/state only where lawful randomness is part of the algorithm;
- parent branch chain;
- winning branch predicate AST/hash;
- rejected/pruned trace when required by the claimed coverage law.

Either exact member-set persistence or deterministic membership replay over M01-M13 is information-equivalent. Branch label/support alone is not.

### M15 — Structural-admission provenance

For every empirical fact used by structural/stratal production, retain or dereference:

- exact empirical query/fact identity;
- input predicate/risk-set/target/scope/measure identity;
- source empirical provenance;
- structural transformation/admission authority ID/version/hash;
- target structural producer/use identity;
- negative/limit authority;
- transformation version and replay identity.

The respondent incidence itself need not cross into later structural runtime if the admitted empirical fact remains exactly replayable from this D13 family.

### M16 — Support and uncertainty-method basis

Exact query replay must produce:

- raw numerator/support;
- raw denominator/support;
- governed weighted numerator/denominator where authorized;
- zero-support versus observed-zero distinctions;
- low-support state;
- uncertainty method/design authority where a numeric estimator is governed;
- otherwise the same typed unquantified uncertainty state.

Support summaries need not be permanently stored when exactly derivable from M01-M15.

### M17 — Authority snapshot / provenance closure

Every authority referenced above must remain immutable or content-addressably dereferenceable by:

- authority ID;
- version;
- content hash or equivalent immutable identity;
- effective scope/time where relevant;
- supersession/migration relation if later versions exist.

Permission cannot be silently reinterpreted as workload authority during replay.

### M18 — Deterministic replay and semantic integrity identity

Retain replay identity sufficient to bind:

- D12 frontier version;
- relevant authority snapshot;
- producer/query/search implementation version where required;
- exact physical source/substrate content identity;
- canonical semantic projection/hash covering every proof-relevant field;
- deterministic tie/order rules;
- replay protocol version.

Serialized-file SHA is useful provenance but not semantic equivalence by itself. A logical hash is authoritative only over a projection that includes every D12-relevant field.

## 4. What is not physically necessary as permanent canonical information

When M01-M18 survive, the following are **convenient materializations / derived replayable views**, not independently necessary retention authority:

- `answer_distribution` / `country_answer_distribution`;
- unary E1 conditionals;
- bounded E2 joint contingencies;
- branch node tables where M14 replay is complete;
- branch-conditioned distributions/cotravel;
- population prevalence tables;
- current V550J joint-pattern aggregate tables;
- E3 cloud/network views;
- E4 association metrics;
- historical V547/V548/V549/V549b summary shapes.

This does not make their underlying capabilities optional. It means their information is exactly regenerable from the selected deeper family.

## 5. What cannot be discarded

Deletion is unlawful if it leaves no exact surviving representation of any of:

- a response event/component/rank/repeat distinction;
- an empirically conditionable coordinate/value/time distinction inside the future frontier;
- routing/applicability membership;
- source/native instrument identity;
- universe/sample/derivation relation;
- weight value or weight/design authority;
- branch/discovery replay identity needed to reproduce a recorded result;
- comparator authority/receipt required for reverse-field replay;
- structural-admission provenance;
- any authority snapshot necessary to interpret the retained incidence.

## 6. Source snapshots are not intrinsically mandatory

D13 does **not** find that permanent preservation of every original source byte is information-theoretically necessary if M01-M18 have already captured every source-native empirical distinction and every interpretation/provenance authority required by the D12 frontier.

However, current evidence does not prove that any existing normalized substrate has achieved that source equivalence. Therefore deleting source snapshots on the basis of this specification alone would be an implementation/migration decision outside D13 and would require a later positive equivalence proof.

## 7. Current shared substrate fails this specification

The current V550/V550J shared substrate cannot serve as the selected carrier because its static contract lacks first-class:

- response-event identity;
- multiselect component identity;
- rank/order identity;
- governed predicate identity;
- branch/cohort identity;
- explicit denominator/risk-set/sample-space identity;
- future-coordinate completeness;
- complete weight provenance;
- semantic hash coverage for physical extra columns.

It also default-fills some semantic fields before validation and does not prove JOINT_ONLY semantic parity.

These are static information deficits, not merely unexecuted populated tests.

## 8. Exact replay proof contract

Any concrete implementation claiming to instantiate this specification must satisfy D13B P01-P20:

1. respondent incidence;
2. response-event multiplicity;
3. response topology;
4. risk-set identity;
5. routing/applicability;
6. typed missingness;
7. raw support;
8. weighted support;
9. weight basis;
10. scope;
11. predicate identity;
12. condition AST hash;
13. target identity;
14. branch-membership provenance;
15. k-way joint topology;
16. authority identity;
17. logical content hash;
18. deterministic replay;
19. duplicate semantics;
20. order independence.

A current populated implementation is not certified by D13 because the no-DB/source-equivalence blockers remain.

## 9. Minimality conclusion

The selected family is smaller than `source snapshots + normalized incidence + all materialized facts` because it does not require redundant source bytes or aggregate caches once source-native event semantics and interpretation authority are captured injectively.

It is larger than the current shared respondent substrate because D12 requires event topology, future coordinates, risk sets, universe provenance and authority closure that the current 67-column logical contract does not guarantee.

It is deeper than selected E1/E2 facts because the future-selectable frontier requires reconditioning on dimensions not necessarily materialized today.

Therefore:

`MINIMUM_D13_INFORMATION_FAMILY = COMPLETE_NORMALIZED_RESPONDENT_EVENT_AND_COORDINATE_INCIDENCE + M01-M18 AUTHORITY/PROVENANCE CLOSURE`

No broader system architecture is selected.
