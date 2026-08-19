# D12G — SOURCE DISAGREEMENT SEMANTICS

**Status:** `NON_DISPOSITIVE_D12_FEEDER_EVIDENCE`  
**Purpose:** preserve disagreement among distinct empirical respondent universes without converting it into a false pooled fact, an actor trait, or an unexplained scalar average.

## 1. Governing proposition

When two lawfully comparable empirical universes disagree, the first semantic fact is the disagreement itself.

```text
FACT_A(source=A, universe=UA)
!=
FACT_B(source=B, universe=UB)
```

and, when both are admitted for a service:

```text
{FACT_A, FACT_B}
```

is not automatically equivalent to:

```text
AVERAGE(FACT_A, FACT_B)
```

A combination is a new derived operation requiring its own authority, estimand, design semantics, overlap treatment, uncertainty law, and provenance.

## 2. What must remain visible

Any multi-universe semantic use must preserve enough identity to recover:

- source/study/release;
- respondent-universe identity;
- instrument/question version;
- source-native and canonical wave;
- field dates/time;
- country/geography;
- target population/sample frame;
- response topology/scale contract;
- risk set/routing/applicability;
- raw versus weighted measure basis;
- sampling/weight design;
- support/uncertainty/typed absence;
- harmonization/comparability authority;
- parent/derived/constituent provenance;
- service-specific admission/use authority.

The downstream fact may preserve these by exact reference rather than physical duplication. D12G chooses no representation. But the distinctions may not become unrecoverable.

## 3. Disagreement classes

### 3.1 Temporal change

Use only when the source/instrument comparison is temporally governed, item semantics/topology are comparable, target-population/sample-design differences are controlled or explicitly retained, and field-time identity is known.

Ruling: `DISAGREEMENT_IS_INFORMATION`.

Do not call a difference “change over time” merely because one wave is newer.

Current V553 provides a bounded positive example: same survey family + same country + at least two waves + shared certified semantic/directionality/position structure can enter a governed temporal-comparability surface. It preserves wave-specific authority and differences rather than joining respondents across waves.

### 3.2 Geographic heterogeneity

Use only when the compared facts have a governed geographic relation and comparable item/risk-set semantics.

Examples include Beirut versus Lebanon-national, Lebanon versus Arab-regional, and Lebanon versus global.

Ruling: `SOURCE_INDEXED_FIELD_REQUIRED` and, when the difference is interpretable, `DISAGREEMENT_IS_INFORMATION`.

Do not turn geographic heterogeneity into generated actor identity or belief.

### 3.3 Instrument non-equivalence

If wording, question version, routing, response topology, scale contract, translation, or response-option semantics are not exactly harmonized, disagreement may reflect the instruments.

Ruling: `UNPROVEN` as a substantive population contrast.

The correct output is an explicitly source/instrument-indexed non-equivalence or unresolved comparison, not a fabricated substantive difference.

### 3.4 Target-population heterogeneity

If sources target different populations, the estimates answer different empirical questions even when displayed labels match.

Ruling: `DISTINCT_UNIVERSES`; `COMPARE_SEPARATELY`.

Any standardization or combined estimand requires explicit authority.

### 3.5 Weight/design heterogeneity

Raw and weighted empirical facts are distinct measure bases. Different survey weights may estimate different target quantities or correct different designs.

Ruling: `POOLING_REQUIRES_HARMONIZATION_AUTHORITY`.

Do not average percentages or sum weighted counts across designs without a governed target estimand and transformation.

### 3.6 Support-limited disagreement

A configuration observed in A and unobserved in B is not automatically a contradiction.

Possible states include:
- B truly has zero observed incidence in a comparable risk set;
- B is underpowered;
- B did not ask the relevant item;
- B routed the relevant population away;
- B used a non-equivalent topology;
- B's source population genuinely differs.

These must remain typed.

A supported minority in A must never be converted into impossibility merely because B lacks it.

### 3.7 Unresolved contradiction

When multiple admitted sources disagree and current authority cannot attribute the difference to time, geography, instrument, design, or population:

`DISAGREEMENT_IS_INFORMATION`

with an unresolved-source-contradiction state.

Do not create a false resolution.

## 4. Service-specific disagreement law

The same cross-universe disagreement can have different lawful significance in the three target DDM services.

### A. Autonomous forward social discovery

Forward discovery may treat disagreement as a discovery target:

- Which forks/configurations recur across universes?
- Which appear only in one geography/time/instrument?
- Which conditional structures reverse?
- Which minority configurations are source-local?
- Which comparisons fail because semantics/topology/risk sets are non-equivalent?

The unit is a comparison among **source-indexed empirical facts**.

Forbidden:
- joining unrelated respondents across sources;
- synthesizing an unobserved cross-survey respondent vector;
- calling a cross-source comparison a same-person cotravel relation.

Cross-universe discovery therefore preserves:

```text
response-response incidence within UA
vs
response-response incidence within UB
vs
comparison(incidence_UA, incidence_UB)
```

These are three different empirical operations.

### B. Reverse positioned-subject empirical possibility field

Parent corrective 15 makes the reverse possibility service a target-machine obligation. D12G does not decide the generated-actor-to-empirical-conditioner crosswalk; it decides what happens once candidate universes are considered.

If multiple universes are separately admitted as applicable to the generated actor, disagreement among them is part of the empirical possibility field rather than a reason to fabricate one answer.

Semantic requirements:

1. each source component retains its universe identity;
2. each component records why it is applicable to this reverse query;
3. local/national/regional/global scope is explicit;
4. temporal distance/applicability is explicit;
5. question/scale harmonization is explicit;
6. support and typed absence remain visible;
7. broader backfill is explicitly marked as backfill, never relabeled local;
8. source overlap/dependence is tracked;
9. no component becomes actor belief/response probability without a separately governed downstream rule.

If local and regional components disagree: `DISAGREEMENT_IS_INFORMATION`.

If local evidence is sparse and broader evidence is introduced: `BACKFILL_REQUIRES_EXPLICIT_AUTHORITY`.

If no authority says how to combine them numerically, preserving several components plus uncertainty is lawful; forcing one scalar is not.

### C. Structural/stratal field production

Structural service authority is independent from reverse-field applicability.

A structural producer may admit a broader regional universe, a temporally harmonized same-family series, a different source instrument, or a subset of the sources admitted to reverse inference, but only under its own exact empirical-to-structural producer authority.

Disagreement among structural evidence sources can remain competing source-specific evidence, temporal structural difference, geographic structural heterogeneity, noncomparability, or unresolved contradiction.

It does not have to use the same source priority as reverse inference.

## 5. Locality and backfill

### Locality closeness

“Closest geography” is not sufficient authority.

A Beirut-local survey can be less semantically applicable than a national survey for a particular question if target population differs, the local sample frame is specialized, the instrument differs, field date is mismatched, or routing excludes the relevant group.

Conversely, a global survey does not become applicable merely because it is large.

Locality is one identity/applicability dimension, not a universal ranking function.

### Country identity

Country equality is not sufficient either.

Two Lebanon samples can differ in field period, target population, instrument, sample frame, weights, routing, source family, and questionnaire version.

Therefore:

```text
same_country
!= same_universe
!= same_reverse_applicability
!= same_structural_use_authority
```

### Broader-universe backfill

A broader universe may backfill a sparse local universe only if a versioned authority states:
- which service is backfilled;
- the target query/condition;
- why the broader population is relevant;
- semantic/topology equivalence requirements;
- geographic relation;
- temporal relation;
- support/uncertainty conditions;
- overlap/double-count treatment;
- source-specific provenance;
- how the broader component remains distinguishable from direct local evidence.

D12G does not specify a formula or weight.

## 6. Disagreement and negative authority

The following inferences remain forbidden:

```text
local survey differs from global
-> local actors believe X

Arab-regional survey differs from WVS
-> Arab worldview X

source A has a minority configuration
-> generated actor belongs to that configuration

larger source disagrees with smaller source
-> larger source is true

newer source disagrees with older source
-> newer source automatically dominates

country-local source disagrees with regional source
-> one source must be discarded
```

Population empirical possibility can constrain a target reverse field only through separately governed comparability/applicability. Structural evidence can constrain actor-independent structure only through structural producer authority. V3 still owns generated history and actor state.

## 7. Double-counting changes disagreement semantics

Two agreeing sources are not independent corroboration if they duplicate the same observations.

Two disagreeing sources may not be independent if one is a transformation/subsample of the other.

Therefore disagreement/confirmation requires provenance sufficient to classify source relationships:

- independent sample;
- overlapping sample;
- panel/repeated persons;
- subset/constituent;
- pooled aggregate;
- derived harmonized representation;
- exact duplicate import;
- unknown relation.

If relation is unknown: `DOUBLE_COUNTING_RISK` and dependence remains `UNPROVEN`.

## 8. What a future combination authority must not erase

Without choosing a statistical model, D12G holds that any lawful multi-universe combination must preserve or expose:

- the target estimand;
- universe membership of every contributing fact;
- source-specific support/uncertainty;
- source dependence/overlap;
- instrument/topology transform status;
- temporal/geographic applicability;
- weight/design basis;
- disagreement residual rather than only a pooled mean;
- provenance back to each source fact;
- typed exclusions/noncomparability;
- service-specific use permission.

A pooled number without these identities cannot replace the source-indexed facts.

## 9. Finite semantic holding

The lawful default is `SOURCE_INDEXED_FIELD_REQUIRED`.

When admissible universes disagree: `DISAGREEMENT_IS_INFORMATION`.

When a broader universe fills a local evidentiary gap: `BACKFILL_REQUIRES_EXPLICIT_AUTHORITY`.

When composition could repeat the same observations: `DOUBLE_COUNTING_RISK`.

These are semantic constraints, not an architecture or statistical-model choice.
