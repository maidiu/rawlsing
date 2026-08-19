# D12D — COMPARABILITY AUTHORITY REQUIREMENTS

**Status:** `NON_DISPOSITIVE_D12_FEEDER__AUTHORITY_GAP_SPECIFICATION_ONLY`  
**Repository:** `maidiu/rawlsing`  
**Exact base:** `6899e58e7ed509327fca3e0294b76bef378d0caf`  
**Branch:** `agent/vozhd-trii-d12d-actor-empirical-comparability`

This document specifies what a lawful actor-fact → empirical-conditioner authority would have to prove. It does **not** create that authority, choose its implementation, select storage, define a production registry, or close D12.

## 1. The seam being specified

The target transformation is:

```text
EXACT GENERATED ACTOR DEMOGRAPHIC / BIOGRAPHICAL FACT
    + exact actor-fact authority and effective time
    + exact survey-coordinate authority
    + field-specific comparability rule
    + exact normalization / temporal / source scope
    ↓
EMPIRICAL POSSIBILITY-FIELD CONDITIONER
    = a governed D08 empirical predicate over historical respondents
```

The output is **only an empirical selection predicate**. It is not:

- a generated structural position;
- a claim that the actor is a member of a survey population subgroup in an ontological sense;
- an actor belief or belief probability;
- an actor response propensity;
- a finished possibility field;
- a persona/profile;
- a V552 structural fact;
- a V554 affordance;
- an encounter/exposure;
- a memory or epistemic state.

The binding four-way ontology is:

```text
EMPIRICAL RESPONDENT COORDINATE
!= GENERATED ACTOR DEMOGRAPHIC / BIOGRAPHICAL FACT
!= GENERATED NINE-STRATUM STRUCTURAL POSITION
!= EMPIRICAL POSSIBILITY-FIELD CONDITIONER
```

A lawful mapping from ontology 2 to ontology 4 may mention ontology 1 because ontology 4 is a predicate over ontology 1. It must not route through ontology 3.

## 2. Current pieces that already exist

D12D finds several current authorities that can be reused **as endpoints or constraints**, but none is a general actor→survey comparability law.

### 2.1 Survey-side empirical predicate grammar

D08 already provides the lawful empirical fact grammar. A conditioner may be an exact typed predicate over an `EMPIRICAL_POSITION_COORDINATE`, with explicit scope, risk set, response topology, missingness, measure and provenance. The predicate identity must survive into any E1/E2 empirical fact produced from it.

This means D12D does **not** need a new statistical meaning for `P(Y | C)`. It needs an authority that lawfully constructs `C` from an independently generated actor fact.

### 2.2 Survey-side coordinate vocabulary

Current V550 recognizes empirical position-coordinate fields including:

- `sex`, `sex_gender`, `gender`;
- `age`, `age_group`;
- `education`, `education_level`;
- `income`, `income_level`;
- `religion`, `religion_label`;
- `urban_rural`;
- `region`;
- `ethnicity`;
- `language`;
- `employment`;
- `marital`;
- `household_size`.

The fixed V550 diagnostic inventory uses a narrower normalized set:

`sex, age_group, education_level, income_level, religion_label, urban_rural, region, ethnicity, language, employment, marital, household_size`.

Those declarations prove a present empirical-coordinate vocabulary and executable conditioning surface. They do **not** prove that identically named values have one cross-source meaning, that all fields are populated, or that an actor-side value is comparable.

### 2.3 Current actor-side generated facts

Current V3 authority is uneven by fact family.

- `ADP-007` owns actor initialization and the admission contract for initial generated facts, but its v1 domain initial-fact registry is valid-empty. It does not supply universal demographic fact semantics for age, sex/gender, income, education, employment, language, religion, ethnicity, residence or occupation.
- `ADP-009` owns exact generated structural-position facts and prospective position mobility. Those facts are ontology 3 and are **not** generic D12D comparators.
- `ADP-010` owns actor-specific objective opportunity/encounter/exposure records. These can establish exact biographical exposure facts when their subject semantics are relevant, but exposure does not imply travel, residence, memory, belief or response.
- `ADP-015` owns exact generated relationship, household-membership and genealogy facts. Those can support actor-side household/relationship biography, but do not automatically equal survey marital status, household size or household composition categories.
- `ADP-016` owns generated memory and expressly separates memory from objective event history.
- `ADP-017` owns actor knowledge/belief/accessibility and expressly separates belief from objective fact and self-report/demographic constructs.

Therefore a comparator must cite the exact actor fact's **semantic owner**, not merely an actor-record field name.

## 3. Required comparability-rule contract

Any future authority satisfying this feeder must govern the semantic equivalent of the following fields. This is an authority-requirement schema, **not a production schema selection**.

### 3.1 Rule identity

Required:

```text
comparator_rule_id
comparator_rule_version
comparator_rule_hash
status / effective scope
```

The rule must be immutable/versioned for replay. Mutable “latest” semantics are not sufficient.

### 3.2 Actor-fact binding

Required:

```text
actor_fact_kind
actor_fact_ref / actor_fact_hash
actor_fact_owner_authority_id / version
actor_fact_value_semantics
actor_fact_unit_or_taxonomy_ref
actor_fact_effective_from / effective_until or reference_time
actor_fact_provenance_refs[]
```

The comparator must verify that the actor fact is a generated objective/biographical fact of the intended kind. It may not accept:

- structural position merely because it has a similar label;
- actor belief where an objective/self-identification fact is required;
- memory where objective history is required;
- V2 prose or transcript-derived descriptors;
- an ungoverned prompt field;
- inferred/default demographics.

### 3.3 Empirical-coordinate binding

Required:

```text
survey_source_scope
survey_wave_scope / canonical_wave_scope
survey_country_scope
empirical_coordinate_id / native variable identity
empirical_coordinate_semantic_role
empirical_coordinate_authority_ref / version / hash
empirical_value_taxonomy_or_unit_ref
routing / applicability semantics where relevant
missingness semantics
```

A normalized field alias such as `income_level` does not by itself establish that source-native values share the same construct. Source-native and harmonized authority must be distinguishable.

### 3.4 Comparator type

Each rule must explicitly select one or more of the authorized **comparison mechanisms** below. There is no global default.

#### A — `EXACT_VALUE_EQUALITY`

Allowed only where:

- actor and survey value domains are the same governed domain;
- units and reference time are the same;
- value identity is exact, not label-similar;
- no hidden source-specific semantics change the construct.

Example candidate: exact completed age in years only after the survey age field's reference-date rule is known.

#### B — `VERSIONED_NORMALIZATION_CROSSWALK`

Required where actor and empirical values use different governed taxonomies or units but an explicit mapping preserves the intended construct.

Examples:

- education classifications;
- age-band boundaries;
- occupational classifications;
- denomination/sect taxonomies;
- language IDs;
- income-band harmonization.

The crosswalk must have an ID, version, hash, direction, coverage state, ambiguous mappings and negative/unmapped states.

#### C — `RANGE_BAND_MATCH`

Required where a scalar actor fact maps to an empirical interval/band.

The rule must encode:

- lower and upper boundaries;
- inclusive/exclusive endpoints;
- open-ended bands;
- unit;
- exceptional/source-specific categories;
- temporal version.

No band may be inferred from its display label alone.

#### D — `HIERARCHICAL_GEOGRAPHIC_MATCH`

Required where actor locality/residence is compared with a survey geography at a coarser or differently encoded level.

The rule must use exact governed place identities and historical containment/boundary authority. It must not use geographic proximity, string similarity or “nearest region.”

It must explicitly distinguish:

- identical place identity;
- historical containment;
- administrative successor/predecessor relation;
- survey sampling geography;
- country/territory sovereignty coding;
- noncomparable/ambiguous boundaries.

#### E — `SOURCE_SPECIFIC_SEMANTIC_EQUIVALENCE`

Required whenever the survey construct has source-specific wording, reference population, coding or category semantics.

This should be the default burden for:

- religion/sect self-identification;
- ethnicity;
- employment;
- marital/civil status;
- language dimension;
- urban/rural classification;
- household definition;
- migration/travel items;
- source-native biographical fields.

Source-specific does not mean fuzzy. It means exact authority is scoped narrowly.

#### F — `TEMPORALLY_CONDITIONAL_EQUIVALENCE`

Required whenever equivalence depends on time.

The rule must identify the temporal relation, for example:

- `CONTEMPORANEOUS_WITH_SURVEY_FIELDWORK`;
- `ACTOR_AGE_AT_SURVEY_REFERENCE_TIME`;
- `ACTOR_LIFE_STAGE_MATCH` under an independently governed life-stage definition;
- `RETROSPECTIVE_WINDOW_MATCH` for a survey question such as “in the last N years”;
- `HISTORICAL_BOUNDARY_VERSION` for region/place;
- `ATTAINED_BY_REFERENCE_TIME` for education;
- `CURRENT_STATUS_AT_REFERENCE_TIME` for employment/marital/household status.

A survey wave label is not automatically an exact fieldwork timestamp.

#### G — `NOT_LAWFULLY_COMPARABLE`

Required when the constructs are different or negative authority forbids the proposed mapping.

Examples:

- actor belief → survey religion affiliation;
- generated class position → survey income level;
- generated sect position → survey religion label;
- political allegiance → survey region;
- class consciousness → survey employment;
- actor memory → objective demographic field;
- current actor response → retroactive comparator selection absent separate anti-circular authority.

## 4. Normalization requirements by family

### 4.1 Age

A lawful exact-age comparator requires:

- actor-side age authority or a birth/reference-time fact from which age is lawfully derived;
- survey-side definition of age and reference date;
- identical unit, normally completed years if that is the survey construct;
- validity handling for inconsistent/unknown ages;
- exact temporal alignment.

An actor age of `35` may produce `survey_age = 35` **only after those requirements are certified**.

If the empirical coordinate is `age_group`, the mapping must instead be a versioned interval rule. `35 -> 30–39` is not lawful merely because that band seems conventional.

### 4.2 Sex / gender

The comparator must identify which construct each side represents. No authority may collapse:

- sex recorded at birth;
- current sex classification;
- gender identity;
- survey interviewer classification;
- self-identification;
- binary/nonbinary coding.

No missing value may be converted into a 50/50 draw or default category.

### 4.3 Income / household resource state

The rule must declare:

- individual vs household unit;
- gross/net/earned/disposable/resource-state construct;
- nominal currency and date;
- any CPI/PPP/price normalization;
- household equivalence scale if used;
- absolute amount vs source-relative band/quantile;
- reference period;
- survey category thresholds/version.

No path through generated class position is permitted.

### 4.4 Education

The rule must distinguish:

- completed attainment;
- current enrollment;
- credential;
- years of schooling;
- source-native categories.

Cross-source use needs a versioned education-classification crosswalk. Similar labels are insufficient.

### 4.5 Employment

The rule must distinguish:

- employed/unemployed/inactive;
- paid/unpaid work;
- self-employment;
- student/retired/caregiver classifications;
- multiple simultaneous jobs/statuses;
- reference period.

Employment is not relation to production, class consciousness or occupational structural position.

### 4.6 Language

The rule must bind the dimension:

- first/native language;
- home language;
- current use;
- fluency;
- interview language;
- self-identified language.

Multilingual actors may lawfully produce several candidate empirical mappings only if the comparison rule states whether the predicates are conjunctive, alternative, set-valued or separately queried.

### 4.7 Religion / sect self-identification

The actor input must be an exact generated affiliation/self-identification fact with its own semantic owner. An ADP-017 belief is not sufficient.

The rule must distinguish:

- current affiliation;
- denomination/sect;
- upbringing;
- practice;
- belief in a proposition;
- self-description;
- multiple affiliation;
- no affiliation;
- source-specific category collapse.

A generated structural sect position under ADP-009 also cannot substitute for this actor fact.

### 4.8 Ethnicity

The rule must identify whether each side is:

- self-identification;
- ancestry;
- externally assigned classification;
- citizenship/nationality;
- language proxy;
- source-specific census-like category.

Country-specific/historical category authority is normally required.

### 4.9 Region / locality / urbanicity

Residence comparison requires an independently generated residence/locality fact. ADP-009 structural position/location must not be used as a generic demographic bridge.

Geographic matching requires exact historical hierarchy/boundary authority. `Beirut` may lawfully map to a survey region only through an exact place and survey-geography rule, never by string similarity or nearest centroid.

Urban/rural additionally requires the source's classification rule at the relevant time.

### 4.10 Marital status

ADP-015 relationship facts provide current actor-side objective relationship history, but no universal mapping from relationship entities to survey `marital` categories is established.

A lawful comparator must specify the source survey construct and the generated fact basis needed to derive it. Civil/legal marriage, cohabitation, partnership, separation, divorce, widowhood and never-married cannot be invented from generic relationship presence/absence.

### 4.11 Household size and composition

ADP-015 provides exact household entities and membership facts. A comparator may derive a household size only under an explicit rule defining:

- the generated household whose membership is counted;
- effective time;
- active membership;
- temporary absence;
- nonresident dependents;
- boarders/institutional members if relevant;
- the survey household-definition convention.

Household composition requires an additional role/set crosswalk and source-native coordinate authority.

### 4.12 Migration and travel

No inspected current authority supplies a universal generated migration/travel biography.

ADP-010 exposure records are exact actor history, but `EXPOSURE` means objective presentation/impingement through an encounter; it does not imply movement, travel, residence or migration. A travel-related OEE record may be a valid actor fact only if its subject and witness semantics establish the exact construct needed by the source survey item.

Migration/travel comparators therefore require source-specific rules and, where movement itself matters, an independent generated movement/residence-history owner.

Memory of travel under ADP-016 is not a substitute for objective travel history.

### 4.13 Occupation

No generic current generated occupation-biography fact owner was located. ADP-009 may govern an occupation as a structural-position target under a position rule, but D12D may not repurpose that ontology as a demographic comparator.

Any future actor occupation fact must then be crosswalked to the source survey occupational classification/version.

### 4.14 Time / year / period

Generated facts/events have effective causal times; survey facts have source/wave/year scope. A comparator must still choose the temporal relation.

Possible lawful modes include contemporaneous matching or an explicitly governed retrospective/life-stage relation. There is no global rule that “actor year = survey year” is always the correct historical comparator.

## 5. Multiple mappings and composition law

One actor property may lawfully map to zero, one or several empirical coordinates. Multiplicity must be typed.

Required mapping cardinality states:

```text
ZERO_LAWFUL_COMPARATORS
ONE_EXACT_COMPARATOR
MULTIPLE_ALTERNATIVE_COMPARATORS
MULTIPLE_CONJUNCTIVE_COMPARATORS
MULTIPLE_COMPARATORS_AMBIGUOUS
```

### Alternative comparators

If several source-native fields are alternative measurements of the same construct, the rule must say how the consumer chooses or queries them. It may not OR them merely to increase support.

### Conjunctive comparators

An actor property may generate several empirical predicates conjunctively only when the comparability authority explicitly states that the conjunction represents the actor fact.

Individual field permissions do not compose automatically. This inherits D07's rule that arbitrary conjunctions require separate authority.

### Set-valued actor facts

For multilingual, multi-affiliation, multi-household or similar actor facts, the rule must state whether survey comparison is:

- exact set equality;
- contains-any;
- contains-all;
- component-wise separate query;
- source-specific reduction;
- noncomparable.

No first-item, modal-item or string-similarity fallback is allowed.

## 6. Missingness, unknown and negative authority

Actor-side and respondent-side missingness are separate.

### Actor-side

If actor fact authority is missing or the actor value is unknown:

- do not impute from structure, prevalence, nearby actors or demographics;
- do not broaden to an “average” survey comparator;
- do not treat unknown as a wildcard unless a separately governed query explicitly requests an unconditioned population field;
- emit a typed no-comparator or deferred state.

### Respondent-side

A valid actor comparator does not authorize treating survey missing/DK/refusal/IAP/not-asked states as matching values.

The resulting D08 predicate must preserve the exact risk set and typed respondent missingness/applicability semantics.

### Negative authority

If a mapping is semantically forbidden, the output is a negative comparator decision, not `UNKNOWN` and not a fallback to another field.

## 7. Required typed failure/ambiguity outputs

The companion `TYPED_NO_MATCH_AND_AMBIGUITY_MATRIX.csv` defines the minimum state vocabulary. A conforming comparator authority must distinguish at least:

- actor fact not authorized;
- actor fact unknown/missing;
- empirical coordinate not authorized/unavailable;
- comparability rule missing;
- normalization/crosswalk missing or uncovered;
- temporal alignment unresolved;
- source scope unresolved;
- construct mismatch;
- category/value no match;
- geographic hierarchy/boundary ambiguity;
- multiple possible mappings with no composition authority;
- respondent coordinate noncomparable;
- negative authority / forbidden inference;
- lawful valid-empty comparator set.

None may silently degrade to exact equality, nearest string, nearest geography, most common category, midpoint, default band or unconditioned population.

## 8. Provenance that must survive into the empirical condition

A resulting empirical conditioner must retain enough provenance to reconstruct **why this exact survey predicate was derived from this exact actor fact**.

Minimum lineage:

```text
actor_id
actor_fact_ref / hash
actor_fact_owner authority/version
actor_fact effective/reference time
comparator rule ID/version/hash
normalization/crosswalk ID/version/hash where used
source-specific semantic-equivalence authority where used
temporal-alignment rule and resolved time relation
geographic hierarchy/boundary authority where used
survey source/wave/country
empirical coordinate native/canonical identity
empirical coordinate authority/version/hash
resolved empirical predicate AST/hash
mapping cardinality / ambiguity decision
negative/no-match receipts where relevant
```

When the predicate is passed into the D08 algebra, the D08 fact must then preserve its ordinary predicate, risk-set, target, measure, topology and replay provenance. The actor fact does **not** become part of the respondent's empirical ontology; it is provenance for why that predicate was queried.

## 9. Anti-circularity law

Reverse empirical comparability is a prior/conditioning operation over a generated actor's independently established demographic/biographical facts.

The following is forbidden by default:

```text
actor response or actor belief at time t
→ select historical respondents who gave that same response/belief
→ treat the resulting distribution as prior evidence for the actor at or before t
```

Any future response-conditioned reverse query would require a separate authority defining causal timing, purpose and leakage prevention. D12D does not authorize it.

## 10. Structural-position non-use

D12D expressly forbids the following shortcuts:

```text
CAN-006 binding key
→ survey field lookup

ADP-009 generated class position
→ survey income_level

ADP-009 generated sect position
→ survey religion_label

ADP-009 generated region position
→ survey region

ADP-009 generated occupation/relation position
→ survey employment/occupation
```

Those are ontology-3 inputs. The D12D target starts from ontology-2 facts.

A generated actor may simultaneously possess both an objective biography fact and an ADP-009 structural position, but the comparator must cite the former if the survey condition measures biography/demography.

## 11. Current-versus-target verdict of this requirements court

### Current authority already present

Current Rawlsing already has:

1. D08's typed empirical-condition predicate grammar;
2. V550's recognized empirical position-coordinate vocabulary and survey scope identity;
3. source/wave/country/question/value provenance surfaces;
4. exact V3 effective-time and generated-event/fact authority for several biographical families, notably OEE and household/genealogy;
5. explicit negative authority preventing structural/demographic statistics from becoming psyche.

### Target capability requires

The binding steering corrective declares that reverse positioned-subject empirical possibility inference is a target DDM capability. Therefore the machine requires a lawful way to derive empirical comparability predicates from actor facts **where semantic comparability actually exists**.

This requirement is field-specific. It does not imply every actor fact must be comparable.

### Authority still missing

D12D did not locate a current general authority that binds:

```text
exact generated actor demographic/biographical fact
→ exact survey coordinate predicate
```

with the normalization, time, source scope, ambiguity, missingness and provenance rules above.

In addition, current actor-side semantic owners are missing for many common demographic/biographical facts. The comparator seam cannot repair that upstream absence.

The feeder therefore records:

`TARGET_COMPARABILITY_LAW_REQUIRED`

with current authority **partial at the endpoints and absent at the general cross-ontology comparison seam**.

This is an authority-gap specification only. D12 remains open, D12E/D12F/D12G remain independent feeders, and architecture remains D15 jurisdiction.
