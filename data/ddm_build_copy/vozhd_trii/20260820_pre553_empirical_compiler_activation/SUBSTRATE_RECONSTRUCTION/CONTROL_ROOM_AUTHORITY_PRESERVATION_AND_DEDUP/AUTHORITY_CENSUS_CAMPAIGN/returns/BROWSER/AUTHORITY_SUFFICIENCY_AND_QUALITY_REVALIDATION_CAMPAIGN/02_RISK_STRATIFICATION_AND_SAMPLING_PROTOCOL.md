# Authority Revalidation — Risk Stratification & Sampling Protocol

Status: `BINDING__DETERMINISTIC__EXPANSION_TRIGGERED`

## Purpose

The campaign must not spend high-powered semantic review uniformly across 18,276 implementations. It must concentrate review where an error would be likely, consequential or structurally contagious, while still retaining a representative baseline capable of detecting unanticipated failure modes.

## Unit of review

The audit unit is the smallest governed assertion whose quality is being tested: implementation-level semantic/use judgment, semantic-unit equivalence, driver/facet assignment, directionality relation, routing/applicability rule, structural relation, respondent-position judgment, etc.

Do not sample physical rows when multiple rows represent the same governed assertion.

## Risk dimensions

Each candidate audit unit receives explicit flags or scores on the following dimensions.

### R1 — provenance confidence

Highest risk examples:

- semantic judgment produced by legacy agent lineage with no later source-backed revalidation;
- generated/helper output that subsequently influenced accepted work;
- unknown or ambiguous manual/agent provenance;
- accepted artifact whose producing rationale is absent.

Lowest risk examples:

- exact source-native mechanical identity;
- explicit human adjudication with source citation and accepted receipt;
- later hostile-validated source-backed successor.

### R2 — scope/sufficiency uncertainty

High risk where:

- the expectation universe says `SEARCH_IN_PROGRESS`, partial scope, succession unproved or current quality pending;
- a bounded authority is being treated as if it might cover a broader consumer requirement;
- downstream consumers require authority outside the observed target.

### R3 — downstream consequence

High risk where an assertion feeds:

- many relation candidates;
- driver/facet aggregation;
- generated-person runtime;
- respondent filtering/risk set;
- directionality/polarity;
- position/strata activation;
- compiler admission/exclusion;
- cross-wave or cross-family equivalence.

### R4 — semantic complexity

Increase risk for:

- mixed modality / hypothetical vs realized behavior;
- actor/target ambiguity;
- nested conditionals;
- tradeoffs and bipolar scales;
- multi-target batteries;
- status vs attitude ambiguity;
- source-language/translation issues;
- variable labels that underdescribe questionnaire context;
- stems whose meaning depends on parent/battery text.

### R5 — conflict/cardinality signal

Increase risk for:

- one-to-many carrier bindings;
- conflicting historical/current assertions;
- case-sensitive collision groups;
- blocked identity joins;
- d62 duplicate-shadow lineage;
- helper/parent residues;
- multiple source aliases or physical-variable expansions.

### R6 — explicit unresolved/block state

Treat explicit unresolved states as high review priority for **sufficiency classification**, but not automatically as defects. The review question is whether unresolved is the correct source-evidence ceiling or whether stronger existing evidence was missed.

### R7 — source-family risk

Elevate families/waves where prior courts already found scope, structural or source problems, including explicit partial family authority, source-native pending states, itinerary drift or legacy helper aliases.

### R8 — novelty / under-sampled class

Reserve representative coverage for classes not already captured by known risk signals. A campaign that audits only known weird cases cannot estimate baseline legacy quality.

## Risk tiers

Workers may implement a numeric score, but must map each audit unit to a stable tier:

- `T4_CRITICAL` — direct conflict, high-consequence legacy authority, or explicit known defect class;
- `T3_HIGH` — multiple risk dimensions or one severe semantic/provenance weakness;
- `T2_MEDIUM` — ordinary legacy semantic work with incomplete independent revalidation;
- `T1_LOW` — strong provenance/source backing with limited downstream consequence;
- `T0_MECHANICAL` — deterministic source identity/mechanical facts; audit mainly for implementation correctness rather than semantic judgment.

## Deterministic sampling

Within every relevant source-family/wave × authority-lineage × risk-tier stratum:

1. sort by stable governed ID;
2. derive deterministic selection rank from SHA-256 of `campaign_id | worker_id | governed_id`;
3. take the lowest hashes up to the sample quota;
4. record the exact selection rule and denominator.

No worker may hand-pick only illustrative examples.

## Minimum initial sample

Unless the worker task requires a full census:

- review all `T4_CRITICAL` units up to 500; if more than 500, take a deterministic 500 plus class-specific census where the task demands it;
- review at least 100 `T3_HIGH` units, distributed across relevant families/lineages;
- review at least 75 `T2_MEDIUM` units;
- review at least 25 `T1_LOW` units as a false-security check;
- include at least one unit from every active family and every material authority lineage in scope where denominator permits.

Workers with narrow bounded denominators may audit the full denominator instead.

## Required defect taxonomy

At minimum:

- `SOURCE_CONTRADICTION`
- `TARGET_OR_ACTOR_LOSS`
- `CONDITION_OR_ROUTING_LOSS`
- `MODALITY_OR_HORIZON_LOSS`
- `RESPONSE_TOPOLOGY_MISREAD`
- `DIRECTIONALITY_ERROR`
- `SEMANTIC_ROLE_CATEGORY_ERROR`
- `DRIVER_FACET_CATEGORY_ERROR`
- `UNSUPPORTED_EQUIVALENCE_OR_CONTINUITY`
- `MISSED_EQUIVALENCE_OR_CONTINUITY`
- `POSITION_VS_SUBSTANTIVE_CATEGORY_ERROR`
- `STRUCTURAL_PARENT_BATTERY_ERROR`
- `SOURCE_LIMITATION_MISTAKEN_FOR_CERTAINTY`
- `CERTAINTY_MISTAKEN_FOR_UNRESOLVED`
- `PROVENANCE_OR_SUCCESSION_ERROR`
- `NO_DEFECT`

## Expansion triggers

A worker must propose targeted expansion when any of these occur:

1. **systematic rate trigger:** weighted defect rate > 2% within a lineage or risk class after at least 50 audited units;
2. **severe semantic trigger:** ≥3 source-contradiction / unsupported-equivalence / directionality / routing defects in the same lineage/class;
3. **cluster trigger:** ≥5 defects sharing a recognizable semantic or source-family pattern;
4. **downstream consequence trigger:** any single defect affects a high-fanout accepted relation/family/driver or executable routing predicate;
5. **provenance trigger:** quality differs materially by producing lineage/agent/stage;
6. **hidden-coverage trigger:** an authority believed jurisdiction-complete lacks required rows for a proven consumer obligation;
7. **false-unresolved trigger:** existing source evidence resolves a nontrivial class currently marked unresolved;
8. **false-certainty trigger:** accepted authority exceeds the source-evidence ceiling for a nontrivial class.

Expansion must target the implicated stratum, not the full universe by default.

## Pass guidance

A lineage may be proposed for `HOSTILE_SAMPLE_PASS` when:

- representative and high-risk samples both meet the task's evidence standard;
- no systematic trigger fires;
- severe defects are absent or isolated and explicitly bounded;
- family/source distribution is broad enough to rule out obvious localized collapse;
- all disagreements are recorded rather than silently reconciled.

A sample pass does not prove metaphysical infallibility. It certifies the lineage to the campaign's declared risk-based review standard.

## Error-rate reporting

Workers must report:

- raw audited count;
- defect count by severity/class;
- denominator represented;
- risk-tier distribution;
- family/wave distribution;
- provenance-lineage distribution;
- estimated weighted defect rate where meaningful;
- Wilson or equivalent interval if an error-rate estimate is reported;
- triggered/non-triggered expansion rules.

Do not report a global percentage when the sample design does not justify one.