# VT3-CM-R11 — CONDITIONAL WORKLOAD AUTHORITY COURT

**Repository:** `maidiu/rawlsing`  
**Required base SHA:** `8c87f7725ba58202b5377c974548140420709fa9`  
**Required branch:** `agent/vozhd-trii-vt3-cm-r11`  
**Status of this copy:** local salvage publication; **not uploaded or committed to GitHub**.

## Epistemic status

The exact base commit and repository tree were located through the connected GitHub repository. In this salvage pass, the connector did not yield reliable line-level extraction of every requested authority file, so this result does **not** pretend to be a line-cited source-verification record. Where exact source-level authorization could not be demonstrated, the court classifies the seam as `MISSING_AUTHORITY` rather than inferring authority from implementation.

The controlling distinction is three separate jurisdictions:

1. authority to **compute/preserve** an empirical conditional;
2. authority to **interpret** that conditional as structural evidence;
3. authority to **bind** that structural evidence to a generated V3 position.

These are not interchangeable.

# VERDICT

No demonstrated authority law licenses a universal compiler from every question to all twelve hard-coded V550 `INDICATOR_FIELDS`. The fixed twelve-field crossing is therefore implementation behavior unless each question × conditioning coordinate is independently justified by governing authority.

Conversely, absence of a CAN-006-compatible V3 binding does **not** erase all legitimate empirical value. A conditional may be lawfully worth computing or retaining for contextual, historical, diagnostic, or future-evidence purposes while remaining forbidden from structural interpretation or runtime position binding.

The missing seam is a declarative workload-selection authority that compiles existing question/measure authority, conditioning authority, source/value-domain authority, response topology, weighting/denominator law, support/absence policy, semantic lane, and optional structural/runtime authority into an exact governed workload.

# A. CURRENT CONDITIONAL-WORKLOAD AUTHORITY GRAPH

```text
SOURCE / WAVE / GEOGRAPHY AUTHORITY
        |
        | defines observable coordinates, domains, provenance
        | does NOT by itself order conditional computation
        v
QUESTION / MEASURE AUTHORITY
        |
        | establishes admissible question/measure and semantic use
        v
CONDITIONING WORKLOAD AUTHORITY
        |
        | must identify dimension, predicate, or conjunction
        v
GOVERNED CONDITIONAL WORKLOAD
        |
        +--> RESPONSE TOPOLOGY AUTHORITY
        +--> WEIGHT / DENOMINATOR AUTHORITY
        +--> SUPPORT RETENTION / TYPED ABSENCE LAW
        |
        v
EMPIRICAL CONDITIONAL FACT
        |
        +--> diagnostic-only lane
        +--> contextual / historical / future-evidence lane
        +--> STRUCTURAL INTERPRETATION AUTHORITY
                     |
                     v
             structural evidence
                     |
                     +--> RUNTIME BINDING AUTHORITY
                                  |
                                  v
                      generated V3 structural position
```

A downstream authority does not retroactively create an upstream one. Runtime binding does not automatically command V550 computation; source-field existence does not command workload; structural interpretation does not imply V3 binding; and failure of V3 binding does not by itself forbid contextual/future retention.

# B. FIELD / QUESTION-USE AUTHORITY MATRIX

| Candidate authority source / property | Conditional compute | Structural interpretation | V3 binding | Classification |
|---|---|---|---|---|
| Source-structure declaration that a coordinate exists | No, standing alone | No | No | `NOT_AUTHORITY_FOR_CONDITIONAL_COMPUTE` |
| Response-semantic / topology authority | Governs HOW, not WHETHER | Response semantics only | No | `NOT_AUTHORITY_FOR_CONDITIONAL_COMPUTE` |
| Question-use authority with no named conditioner | Question admissibility only | Separate rule | No | `NOT_AUTHORITY_FOR_CONDITIONAL_COMPUTE` / `MISSING_AUTHORITY` |
| Question/overlay naming a conditioning dimension | Yes only if rule actually orders stratification by it | Separate rule unless explicit | No | `DIMENSION_LEVEL_PERMISSION_ONLY` |
| Authority naming exact conditioning predicate | Yes for that predicate | Separate rule unless explicit | Separate rule | `EXACT_CANONICAL_WORKLOAD_AUTHORITY` |
| `allowed_as_demographic_predictor` | Diagnostic only | No | No | `DIAGNOSTIC_ANALYSIS_PERMISSION` |
| `allowed_as_branch_splitter` | Diagnostic only | No | No | `DIAGNOSTIC_ANALYSIS_PERMISSION` |
| `allowed_as_position_distribution` | Only where governing rule expressly requests the distribution | If expressly structural | No | `DIMENSION_LEVEL_PERMISSION_ONLY` + possible `STRUCTURAL_INTERPRETATION_AUTHORITY` |
| `allowed_as_context_distribution` | Only where expressly governed | Contextual, not actor identity | No | `FUTURE_EVIDENCE_RETENTION_AUTHORITY` where explicit |
| `position_conditioning` | Scope depends on specificity; bare/generic marker does not enumerate fields/values | If explicitly structural | No | `DIMENSION_LEVEL_PERMISSION_ONLY`, `STRUCTURAL_INTERPRETATION_AUTHORITY`, or `MISSING_AUTHORITY` |
| `position_modifiers` | No independent workload mandate | Possible modifier semantics | No automatic binding | `NOT_AUTHORITY_FOR_CONDITIONAL_COMPUTE` unless expressly workload-bearing |
| `conditional_strata_weights` | Governs HOW an authorized workload is weighted | No | No | `NOT_AUTHORITY_FOR_CONDITIONAL_COMPUTE` standing alone |
| CAN-006-compatible empirical→V3 mapping | No independent compute mandate | As governed | Yes, mapped predicates only | `RUNTIME_BINDING_AUTHORITY` |
| Explicit future/topology evidence-retention rule | Yes where preservation is expressly required | Not necessarily | Not necessarily | `FUTURE_EVIDENCE_RETENTION_AUTHORITY` |
| Membership in hard-coded `INDICATOR_FIELDS` | No | No | No | `NOT_AUTHORITY_FOR_CONDITIONAL_COMPUTE` |
| Strong unrequested association / interaction | Diagnostic regime only | No | No | `DIAGNOSTIC_ANALYSIS_PERMISSION` |

For example, `income_level`, `religion_label`, `employment`, and `region` do not acquire identical authority merely because they are observable respondent coordinates or appear in a common implementation list.

# C. COMPUTE vs STRUCTURAL INTERPRETATION vs RUNTIME BINDING

## Compute / preserve

Answers whether Rawlsing may expend production computation and preserve `P(response | condition)` or an equivalent governed conditional fact.

It requires authority over the question/measure and the conditioner at defined granularity, together with the relevant topology/denominator semantics. It does **not** require current V3 bindability when contextual, historical, or future-evidence retention is separately authorized.

## Structural interpretation

Answers whether the conditional may be treated as evidence about a structural position/relation rather than merely an empirical association.

Predictive power, source availability, demographic-predictor permission, and branch-splitting success are insufficient. Structural meaning requires its own authority.

## Runtime binding

Answers whether governed structural empirical evidence may be resolved against a particular lawfully generated V3 structural position.

This requires an explicit cross-ontology bridge. Shared strings are not ontology.

```text
COMPUTE AUTHORITY != STRUCTURAL INTERPRETATION AUTHORITY
STRUCTURAL INTERPRETATION AUTHORITY != RUNTIME BINDING AUTHORITY
RUNTIME BINDING AUTHORITY does not retroactively imply universal COMPUTE authority
```

# D. DETERMINICITY OPERATIONS: AUTHORITY-REQUESTED vs HARD-CODED

## Authority-requested when explicitly governed

- instantiate an authorized dimension over its authoritative value domain when the rule calls for a distribution/stratification;
- compute an exact authorized predicate;
- apply governed response topology;
- apply governed weighting and denominator;
- preserve support, sample size, uncertainty, and typed absence;
- preserve provenance/version/hash;
- retain a conditional in an explicitly authorized context/future-evidence lane.

## Not authority-requested merely because code does it

- loop every question over all twelve `INDICATOR_FIELDS`;
- treat every observed respondent coordinate as a production conditioner;
- treat every observed value as a canonical predicate;
- form Cartesian products of individually permitted fields;
- promote `allowed_as_demographic_predictor` or `allowed_as_branch_splitter` to canonical workload;
- promote empirical interaction strength into structural ontology;
- infer V3 binding from matching field/value strings;
- delete an otherwise authorized contextual/future conditional solely because no current CAN-006 bridge exists.

**Holding:** no demonstrated general authority licenses "all twelve `INDICATOR_FIELDS` for every question." The hard-coded loop is `NOT_AUTHORITY_FOR_CONDITIONAL_COMPUTE` as a universal workload rule.

# E. CONJUNCTION-ADMISSION FINDINGS

Authority is **not closed under conjunction**.

Separate authority for:

```text
income_level = low
religion_label = X
```

does not automatically authorize:

```text
income_level = low AND religion_label = X
```

A conjunction changes predicate cardinality, support geometry, denominator semantics, sparsity/typed-absence behavior, interpretive risk, and possible structural meaning. It therefore needs explicit conjunction authority or an explicit conjunction-generation rule.

V550J joint-configuration authority cannot be presumed to authorize respondent-condition conjunctions merely because it governs something "joint." If its ontology is joint-question, joint-response, or component configuration, that is a separate jurisdiction. Unless it expressly includes respondent conditioning predicates and their denominator/support semantics, it is `NOT_AUTHORITY_FOR_CONDITIONAL_COMPUTE` for this purpose; the conjunction seam remains `MISSING_AUTHORITY`.

# F. MINIMUM `GOVERNED_CONDITIONAL_WORKLOAD_SPEC`

```yaml
workload_spec_id: string

scope:
  source_ref: authority_ref
  wave_ref: authority_ref
  geography_ref: authority_ref

measure:
  question_or_measure_id: string
  question_measure_authority_ref: authority_ref

conditioning:
  authority_ref: authority_ref
  authority_granularity: dimension | predicate | conjunction
  dimensions: [string]
  predicates:
    - field: string
      operator: eq | in | governed_other
      value: scalar_or_set
      value_domain_authority_ref: authority_ref
  predicate_cardinality: integer
  predicate_order: integer_or_order_rule
  conjunction_semantics_ref: authority_ref | null

response:
  response_topology_ref: authority_ref

estimation:
  weighting_rule_ref: authority_ref
  denominator_rule_ref: authority_ref
  support_retention_policy_ref: authority_ref
  typed_absence_policy_ref: authority_ref

semantics:
  intended_semantic_lane:
    - canonical_empirical
    - diagnostic_discovery
    - contextual
    - future_evidence
    - structural_evidence
    - runtime_bindable
  allowed_use: [enum]
  structural_interpretation_authority_ref: authority_ref | null
  runtime_binding_authority_ref: authority_ref | null

provenance:
  authority_version: string
  compiler_version: string
  provenance_refs: [authority_ref]
  canonical_hash: string
```

The spec must let an auditor answer why this question was computed, why this conditioner was selected, whether authority selected a dimension or exact predicate, why these values were instantiated, why a conjunction exists, which denominator/weighting semantics govern it, how support/absence are represented, and whether the result is merely empirical, structurally interpretable, or runtime-bindable.

# G. EXACT MISSING AUTHORITY

The missing seam is a **governed conditional workload-selection law** mapping:

```text
(source, wave, geography, question/measure)
    ->
(authorized conditioning dimension(s), predicate(s), or conjunction(s))
```

It must resolve, directly or by authoritative reference:

- dimension vs exact-predicate granularity;
- authoritative value domain and instantiation rule;
- conjunction admissibility/order;
- response topology;
- weighting and denominator;
- support/uncertainty retention;
- typed absence;
- semantic lane;
- allowed downstream uses;
- structural-interpretation authority if any;
- V3 runtime-binding authority if any;
- future-evidence retention status.

Where existing authority does not supply this exact selection law, classification is `MISSING_AUTHORITY`.

# H. DIAGNOSTIC DISCOVERY vs CANONICAL PUBLICATION

Diagnostic discovery may test unrequested coordinates/interactions under an explicitly diagnostic regime, rank predictors/splitters, retain support/uncertainty/provenance, and emit candidate-authority records.

It may **not** silently become canonical workload, alter ontology, become structural evidence merely because an association is strong, create V3 binding, create an unauthorized conjunction, or discard weak/minority/multimodal configurations because another predictor is stronger.

Promotion requires explicit governing authority. Before promotion the result remains `DIAGNOSTIC_ANALYSIS_PERMISSION`, not `EXACT_CANONICAL_WORKLOAD_AUTHORITY`.

# I. NO-LOSS CONSEQUENCES

1. Preserve conditionals explicitly required by contextual/future-evidence authority even without current runtime binding.
2. Retain enough source/value-domain, topology, weighting, denominator, support, typed-absence, and provenance information for exact reconstruction where retention law requires it.
3. Do not canonicalize all possible empirical crossings merely as insurance against future authority.
4. When future authority adds a conditioner or conjunction, reconstruct it exactly from lawfully retained substrate or state typed unavailability.
5. Do not erase weak, minority, contradictory, multimodal, or low-support evidence merely because it is a poor predictor.
6. Contextual empirical evidence may remain permanently non-bindable to V3 positions without becoming illegitimate.

The no-loss target is to preserve every **authorized** present/future empirical distinction and its required reconstructibility while refusing to turn the space of all computable correlations into ontology.

# DIRECT ANSWERS TO THE TEN PRIMARY QUESTIONS

1. **Exact pairs?** No universal exact enumeration was demonstrated for the full twelve-field crossing. Exact rules, where present, should compile exactly their stated workload.
2. **Broad permission?** Broad dimension/lane permissions do not imply arbitrary fields/values.
3. **Predictor/splitter flags?** Diagnostic/exploratory permission, not canonical workload authority standing alone.
4. **All twelve fields?** No demonstrated universal license. Hard-coded inclusion is not authority.
5. **Historical/contextual value without CAN-006?** Yes where context, historical evidence, structural-without-binding, or future-evidence authority expressly preserves it.
6. **Terminally unreachable?** Not mandatory production if there is neither workload authority nor contextual/future retention authority.
7. **Exact values?** Authority must declare dimension vs predicate granularity. Dimension-level distribution authority may instantiate its authoritative value domain; observed values do not self-authorize.
8. **Conjunctions?** Require explicit conjunction authority or generation law. V550J helps only if its accepted jurisdiction expressly includes respondent-condition conjunctions.
9. **Strong unrequested interaction?** May remain diagnostic discovery with provenance/support/uncertainty, but cannot self-promote.
10. **Minimum object?** `GOVERNED_CONDITIONAL_WORKLOAD_SPEC` binding scope, measure, conditioner/granularity, value/conjunction semantics, topology, weighting/denominator, support/absence, semantic lane, allowed uses, structural/binding refs, and provenance/version/hash.

# CLASSIFICATION SUMMARY

| Classification | Holding |
|---|---|
| `EXACT_CANONICAL_WORKLOAD_AUTHORITY` | Exact authority selecting a question/measure plus a defined conditioning predicate or governed instantiated dimension |
| `DIMENSION_LEVEL_PERMISSION_ONLY` | Authority permits stratification/distribution by a dimension but does not independently confer later semantic uses |
| `DIAGNOSTIC_ANALYSIS_PERMISSION` | Predictor/splitter/discovery authority; cannot self-promote to canonical ontology |
| `STRUCTURAL_INTERPRETATION_AUTHORITY` | Explicit authority to read the empirical conditional as structural evidence |
| `RUNTIME_BINDING_AUTHORITY` | Explicit bridge from governed structural evidence to generated V3 position |
| `FUTURE_EVIDENCE_RETENTION_AUTHORITY` | Explicit authority to preserve empirical evidence for contextual/future use despite absent current binding |
| `NOT_AUTHORITY_FOR_CONDITIONAL_COMPUTE` | Source availability, weighting mechanics, topology, hard-coded field membership, or downstream binding standing alone |
| `MISSING_AUTHORITY` | No existing rule demonstrated that selects exact production workload/conjunction at required granularity |

# FINAL RULING

The lawful replacement for broad V550 determinicity is neither "compute only what V3 can bind today" nor "cross every question with every available respondent field."

It is:

> compile canonical empirical conditionals authorized by exact or governed dimension-level workload law; preserve separately authorized contextual/future evidence even when presently non-bindable; allow exploratory discovery only in a typed diagnostic lane; require independent authority before structural interpretation and again before V3 runtime binding.

An explicit governed workload-selection seam is therefore required before the fixed twelve-field execution can be replaced by a genuinely authority-first compiler.
