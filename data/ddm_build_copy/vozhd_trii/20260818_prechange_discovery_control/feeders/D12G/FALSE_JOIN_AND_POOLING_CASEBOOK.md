# D12G — FALSE JOIN AND POOLING CASEBOOK

**Status:** `NON_DISPOSITIVE_D12_FEEDER_EVIDENCE`  
**Repository:** `maidiu/rawlsing`  
**Exact base:** `6899e58e7ed509327fca3e0294b76bef378d0caf`  
**Branch:** `agent/vozhd-trii-d12g-cross-survey-multi-universe`  
**Production code modified:** `NO`  
**Architecture/model selected:** `NO`  
**Populated-data claims:** `NONE`

All overlap, support, sample-size, and disagreement examples below are typed hypothetical cases unless an exact static authority is cited. They do not claim anything about the populated Rawlsing database.

## 1. Court rule

The default is:

```text
RESPONDENT UNIVERSE A
!=
RESPONDENT UNIVERSE B
```

unless positive authority proves that the observations are partitions, continuations, or alternate representations of one lawful empirical sample universe.

Three different operations must never be conflated:

```text
semantic comparability
!= respondent identity linkage
!= sample pooling
```

A question can be semantically comparable across two universes while respondent joining remains forbidden. A person-linkage key can be lawfully available across two temporal universes while pooling their observations as one cross-section remains forbidden. Two files can belong to one sample universe while numerical composition remains unsafe because one is a derived duplicate of the other.

## 2. Exact respondent-join proof bar

`EXACT_RESPONDENT_JOIN_AUTHORIZED` requires positive evidence for all applicable items:

1. source/study identities and releases;
2. respondent identity namespaces;
3. a stable person-linkage key or exact namespace equivalence;
4. whether linkage is one-to-one, one-to-many, household-level, or another governed grain;
5. temporal/event identity for each observation;
6. country/geography and sample-frame consistency;
7. question applicability/routing at each observation;
8. duplicate/repeated/multiselect semantics;
9. immutable linkage provenance and authority version.

String equality of `respondent_id` proves none of these.

When namespaces are known independent, cross-source respondent cotravel is `RESPONDENT_JOIN_FORBIDDEN`.

When linkage might exist but no exact authority has been established, the correct state is `RESPONDENT_JOIN_UNPROVEN`.

A lawful respondent join does **not** itself authorize pooling two sample distributions, treating repeated observations as independent respondents, importing one survey's weights into another, or treating non-equivalent instruments as the same empirical event.

## 3. Pooling proof bar

`POOLING_AUTHORIZED` is reserved for a narrow case: exact authority proves that rows are nonduplicative components of one intended sample/estimand and that the relevant instrument, target population, routing, response topology, sampling design, weighting basis, scope, and provenance are composition-compatible.

Otherwise:

- semantically harmonizable distinct universes -> `POOLING_REQUIRES_HARMONIZATION_AUTHORITY`;
- incompatible or unresolved topology/population/design, fabricated joins, or known alternate representations of the same observations -> `POOLING_FORBIDDEN`;
- distinct universes can remain `COMPARE_SEPARATELY`.

A future hierarchical or multi-source combination rule would have to preserve at minimum source/universe identity, target estimand and population, instrument/question equivalence, response topology/scale transform, field-time applicability, sampling design and weight basis, overlap/dependence/constituent relationships, source-specific support/uncertainty, disagreement/heterogeneity, and provenance sufficient to prevent counting the same observation twice. D12G specifies these semantic obligations but selects no statistical model.

---

## CASE A — same question semantics, same country, different waves

Two waves from the same survey family ask what appears to be the same governed question in the same country.

Different field periods are distinct empirical observation universes:

`DISTINCT_UNIVERSES`.

Current `ddm_survey_identity` may canonicalize wave aliases, but alias equality is a naming normalization, not proof that two wave samples contain the same people or share one sample frame.

Current V553 wave harmonization provides a bounded positive comparator: it allows a multi-wave comparison only inside one survey family and one country, requires at least two waves plus shared certified semantic/directionality/position structure, and preserves wave-specific differences. It does not concatenate respondents or manufacture longitudinal person identity.

Respondent join: `RESPONDENT_JOIN_UNPROVEN` by default.

If exact panel/person-linkage authority later proves the same persons across waves, person-level linkage can become `EXACT_RESPONDENT_JOIN_AUTHORIZED` while the observation universes remain temporally distinct.

Pooling: `POOLING_REQUIRES_HARMONIZATION_AUTHORITY`.

Comparison: `COMPARE_SEPARATELY`, with temporal identity retained.

---

## CASE B — same question semantics, different countries

Country is part of empirical scope and target-population identity.

`DISTINCT_UNIVERSES`  
`RESPONDENT_JOIN_FORBIDDEN`  
`COMPARE_SEPARATELY`

Even exact question-semantic equivalence does not create one respondent population. Current V553 reinforces this boundary by rejecting a harmonization report that contains more than one country.

A broader cross-country comparison or synthesis may be lawful only under a separate authority that names the target estimand and preserves country/source identities.

---

## CASE C — same conceptual construct, non-identical wording

Concept similarity is not question equivalence.

`UNPROVEN`

Final R1/QSM source-specific structural semantics and source-native questionnaire authority can establish governed meaning for each implementation. A cross-instrument equivalence requires its own exact harmonization rule. It cannot be inferred from keywords, translated similarity, or an LLM judgment.

Until then: `POOLING_FORBIDDEN`.

Within-universe discovery remains lawful for each instrument under its own authority. Cross-universe comparison may report related constructs observed in distinct instruments, but numerical equivalence remains unproven.

---

## CASE D — same labels, different response scales

Displayed labels do not establish topology or coordinate equivalence.

The current response-scale registry proves why: response semantics are contract-hashed and source-provenanced, with response family, endpoint/coordinate geometry, scale direction, projection rule, and source authority hashes.

If exact response contracts differ: `POOLING_FORBIDDEN` unless a versioned cross-scale transform authority explicitly maps them, in which case composition remains `POOLING_REQUIRES_HARMONIZATION_AUTHORITY`.

---

## CASE E — Lebanon-local survey and Arab-regional survey

Geographic relevance is not sample-universe identity.

`DISTINCT_UNIVERSES`  
`RESPONDENT_JOIN_FORBIDDEN`  
`COMPARE_SEPARATELY`

If the regional product literally contains the same Lebanon observations stored separately, that is a provenance/constituent relation and creates `DOUBLE_COUNTING_RISK`.

If actual overlap is not statically proven, its populated incidence remains `UNPROVEN` under D05.

For reverse positioned-subject possibility use, regional evidence may not silently replace sparse local evidence: `BACKFILL_REQUIRES_EXPLICIT_AUTHORITY`.

---

## CASE F — Lebanon-local and global/WVS evidence disagree

Two separately admissible source universes point in different empirical directions.

Do not average away the disagreement.

`SOURCE_INDEXED_FIELD_REQUIRED`  
`DISAGREEMENT_IS_INFORMATION`

Possible lawful interpretations depend on what is actually proven: geographic heterogeneity if geographic comparability is authorized; temporal change if temporal comparability is authorized; instrument non-equivalence if item/scale equivalence fails; unresolved contradiction if multiple explanations remain possible.

The disagreement cannot be renamed actor ambivalence, Lebanese culture, or a latent worldview without separate authority.

---

## CASE G — asymmetric variable coverage across surveys

Survey A observes:

`income + religion + Q1`

Survey B observes:

`education + Q1 + Q2`

No synthetic respondent can be created by horizontally stitching the universes.

`RESPONDENT_JOIN_FORBIDDEN`

Lawful operations include discovering `income/religion ↔ Q1` within A, discovering `Q1 ↔ Q2` and `education ↔ Q1/Q2` within B, and comparing source-specific Q1 facts if Q1 equivalence is separately authorized.

Forbidden without a separately governed statistical inference model: constructing empirical `income × education × religion × Q1 × Q2` incidence, calling that unobserved joint a same-respondent population fact, or using shared Q1 as a pseudo-link key.

`POOLING_FORBIDDEN`  
`COMPARE_SEPARATELY`

---

## CASE H — no respondent overlap between sources

When source metadata positively establishes two independent samples with no respondent overlap:

`DISTINCT_UNIVERSES`  
`RESPONDENT_JOIN_FORBIDDEN`

This does not prevent source-level comparison. If question semantics/topology and target populations are harmonizable, the facts may be compared or later combined by an explicitly authorized multi-sample model.

No response-response cotravel may be computed across the two sources because no respondent variable ranges over both.

---

## CASE I — apparent respondent-ID collision across namespaces

Source A contains `respondent_id=123`. Source B contains `respondent_id=123`. The namespaces are distinct.

The equality is lexical, not personal identity.

`RESPONDENT_JOIN_FORBIDDEN`

Joining them would fabricate a same-person cotravel edge and may also create `DOUBLE_COUNTING_RISK`.

If namespace relation is unknown rather than known distinct: `RESPONDENT_JOIN_UNPROVEN`.

No normalization function may convert a namespace collision into identity authority.

---

## CASE J — different weighting regimes

Weights are meaningful only relative to their governed design/estimand.

`POOLING_REQUIRES_HARMONIZATION_AUTHORITY`

D08 separates raw and weighted measures. D13B requires missing/invalid weighted evidence to remain typed unavailable rather than defaulted. D13C shows why the current substrate's ability to default weight to `1.0` cannot be used as source-equivalence proof.

A lawful cross-universe combination would need an explicit rule for target estimand, design/calibration basis, source-specific weight meaning, overlap/dependence, and uncertainty propagation. D12G assigns no weights.

---

## CASE K — different target populations

Two surveys ask equivalent questions but target different populations—for example different age thresholds, residency rules, citizen-only versus resident samples, household-head versus adult-person sampling, or national versus urban-only populations.

`DISTINCT_UNIVERSES`  
`POOLING_FORBIDDEN`  
`COMPARE_SEPARATELY`

A comparison must retain the target-population definitions. A later model may standardize or condition them only under explicit authority.

Question equivalence cannot erase denominator/population non-equivalence.

---

## CASE L — minority configuration supported in A and absent in B

Absence in B cannot erase possibility in A.

`DISAGREEMENT_IS_INFORMATION`  
`SOURCE_INDEXED_FIELD_REQUIRED`

Before interpreting the contrast, prove item semantic equivalence, response topology equivalence, risk-set equivalence, sufficient/typed support, and scope/time comparability.

If those do not hold, absence in B may be instrument/routing/support noncomparability rather than a substantive difference.

Even when difference is real, it remains population evidence, not actor membership or a rare persona.

---

## CASE M — temporally closer source is much smaller

Neither recency nor sample size creates an automatic priority.

`COMPARE_SEPARATELY`  
`SOURCE_INDEXED_FIELD_REQUIRED`

For reverse possibility inference: `BACKFILL_REQUIRES_EXPLICIT_AUTHORITY`.

A future rule must state how temporal applicability, support, uncertainty, instrument equivalence, target-population fit, and provenance enter. D12G does not invent a recency weight, sample-size weight, Bayesian prior, or fallback threshold.

---

## CASE N — broad regional evidence, sparse local evidence

Sparse local support is not permission to relabel regional evidence as local.

`BACKFILL_REQUIRES_EXPLICIT_AUTHORITY`

A lawful backfill must remain typed as broader-universe evidence and preserve geographic level, source identity, time, target population, question/scale equivalence, support/uncertainty, overlap/constituent risk, and any disagreement with local evidence.

If the regional survey includes the same local sample: `DOUBLE_COUNTING_RISK`.

---

## CASE O — structural service uses one source, reverse field uses another

This is not inherently contradictory.

The three DDM services have different semantic jurisdictions and may have different source-admissibility rules.

`SOURCE_INDEXED_FIELD_REQUIRED`

No source hierarchy may be copied automatically from one service into another.

Structural-field use asks: “What evidence may lawfully support a structural/stratal fact?”

Reverse-field use asks: “What empirical respondent universe is applicable as a possibility reference for this generated positioned subject?”

Forward discovery asks: “What empirical distinctions may be autonomously searched or compared?”

These are separate authority questions.

---

## 4. Additional hostile cases

### P — nonoverlapping shards of one exact study/wave/sample

If an immutable partition manifest proves that two files are nonoverlapping shards of one intended sample universe and all design/instrument/weight identities match:

`SAME_UNIVERSE`  
`POOLING_AUTHORIZED`

This is the narrow lawful row-concatenation case.

If nonoverlap is unproved: `DOUBLE_COUNTING_RISK`, and pooling falls back to `UNPROVEN`.

### Q — exact panel linkage across distinct waves

A panel authority can prove person identity across temporal observation universes.

Then: `EXACT_RESPONDENT_JOIN_AUTHORIZED`.

But `DISTINCT_UNIVERSES` still applies to the time-indexed observation universes, and `POOLING_FORBIDDEN` applies to treating repeated observations as one undifferentiated cross-section.

The join is lawful for a specifically authorized longitudinal query, not as a generic cloud-merger.

### R — original source plus its harmonized derivative

The derivative and original can refer to the same observations. They are alternate representations, not independent empirical support.

`SAME_UNIVERSE`  
`EXACT_RESPONDENT_JOIN_AUTHORIZED` where lineage preserves row identity  
`POOLING_FORBIDDEN`  
`DOUBLE_COUNTING_RISK`

A one-count-only provenance rule is required.

### S — pooled wave plus constituent waves

If a pooled product is derived from constituent waves, using both pooled and constituent observations as independent mass double-counts evidence.

`DOUBLE_COUNTING_RISK`

A provenance relation must identify constituent membership, aggregation transform, weight recalibration, and whether pooled rows are copies, summaries, or independent additions.

No populated relation is asserted here.

### T — regional product contains a country sample also stored separately

If exact provenance proves the inclusion: `DOUBLE_COUNTING_RISK`.

If inclusion is merely suspected: `UNPROVEN`.

No source-size or “regional” label may decide the overlap.

---

## 5. Beirut reverse-field ladder

Given a generated actor in Beirut, the existence of four evidence levels does not create a default ladder:

1. Beirut/local;
2. Lebanon-national;
3. Arab-regional;
4. global.

Neither locality closeness nor country identity alone establishes admissibility.

Before a universe contributes to the actor's reverse empirical possibility field, two separate things must be governed.

### Actor-side comparability

A separate authority must establish which generated actor properties can be used as empirical conditioners. D12G does not borrow D12D/E/F conclusions and does not invent this mapping.

### Universe-side applicability

For each candidate source independently, authority must establish applicable geography/target population, temporal applicability, questionnaire/construct equivalence, response topology/scale mapping, empirical condition availability, support/risk-set validity, sampling/weight basis, provenance, and overlap state.

Only then can the source contribute as a source-indexed component.

Broader-universe use as substitute for missing/sparse local evidence is `BACKFILL_REQUIRES_EXPLICIT_AUTHORITY`.

Disagreement among admitted components is `DISAGREEMENT_IS_INFORMATION`.

No actual component weight is assigned here.

---

## 6. Forward discovery law

### Within one universe

Forward social-fork discovery may search respondent-bound conditionals, conjunctions, cotravel, minority configurations, and higher-order patterns when that workload/query is authorized and the required E0/E1/E2 information is available.

### Across universes

Cross-universe discovery may compare marginal distributions, conditionals whose predicates are separately harmonized, configuration facts at matching governed arity, discovery results/forks, temporal/geographic source differences, and absence/noncomparability states.

It may not compute a same-respondent joint by pairing people from different universes.

Thus:

```text
within-universe joint discovery
!=
cross-universe comparison of joint facts
```

A cross-source edge must be typed as a comparison/relation among source-indexed facts, not respondent cotravel.

---

## 7. Structural/stratal service law

Structural evidence can lawfully draw from a broader or different universe than reverse empirical possibility inference only when the structural producer's own authority admits that source and transformation.

Current evidence is instructive:

- Final R1 is source-implementation-specific semantic/structural authority;
- V552 is a bounded structural producer over admitted empirical evidence;
- V553 temporal harmonization is same-family/same-country and authority-gated;
- V554+ requires already-governed structural bases.

Therefore no generic rule exists that “more local survey always wins” or “global survey always supplies the prior.”

The structural service must preserve its own source, scope, time, comparability, and provenance even when another DDM service uses a different source.

---

## 8. Double-counting proof obligations

To prevent the same evidence from becoming two votes, multi-universe composition needs provenance capable of distinguishing:

- original study/release ID;
- immutable source artifact hash;
- import/extraction instance;
- sample frame and target population;
- field dates/wave;
- respondent namespace;
- exact respondent/member-set hash when lawfully available;
- parent/derived representation relation;
- constituent/subsample/pooled relation;
- harmonization transform and version;
- weight basis and any recalibration;
- question/instrument version;
- deduplication/one-count-only rule.

The following are always `DOUBLE_COUNTING_RISK` until resolved: same underlying study imported twice; original source plus a row-equivalent harmonized derivative; a regional product plus an included country sample; a pooled wave/product plus its constituent observations; or person-linked longitudinal records counted as independent cross-sectional respondents in a query that assumes independence.

Under the no-DB law, D12G does not claim which of these occurs in production.

---

## 9. Court statement

The lawful cross-universe primitive is **not a pooled mega-sample**. It is a set of source/universe-indexed empirical facts whose comparability, linkage, composition, and service-specific use are independently governed.

The controlling defaults are:

`DISTINCT_UNIVERSES`

`RESPONDENT_JOIN_FORBIDDEN` or `RESPONDENT_JOIN_UNPROVEN` unless positive linkage authority exists.

`COMPARE_SEPARATELY`

`SOURCE_INDEXED_FIELD_REQUIRED`

`DISAGREEMENT_IS_INFORMATION`

`BACKFILL_REQUIRES_EXPLICIT_AUTHORITY`

`DOUBLE_COUNTING_RISK` whenever provenance cannot rule out repeated coverage.

This is a semantic law only. It selects no storage system, statistical model, source hierarchy, or weighting formula.
