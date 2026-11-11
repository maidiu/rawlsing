# FIELD FORGE R1 — HOMOLOGY IDENTIFICATION, CIRCULARITY, AND MEASUREMENT-ARTIFACT GOVERNANCE R1

Status: **EXPLORATORY / NON-BINDING / METHOD-GOVERNANCE REFINEMENT**

Jurisdiction: this note refines how FIELD FORGE may claim position↔disposition homology after the codebook-grounded observability stress test in `27`. It does not create structural ontology, current survey authority, or V3 runtime law.

Central hostile question:

> When Rawlsing sees correspondence between position space and disposition space, how do we know that correspondence belongs to the observed social world rather than to shared inputs, questionnaire design, weighting/calibration, response mode, or an algorithm explicitly optimized to create correspondence?

---

# 1. WHY THIS PASS IS NECESSARY

The dual-space design was introduced to prevent a hidden circularity:

```text
build social space from attitudes
→ discover that social space predicts attitudes
```

But the same circularity can re-enter in subtler forms.

Examples:

- one exact measurement receives lawful roles on both sides;
- a derived position composite shares source measurements with a disposition complex;
- a weight is calibrated using variables active in the position geometry;
- interview mode/language/privacy shifts response distributions;
- a cross-space method rotates/reweights the two spaces to maximize their apparent relation;
- an external group-power source is joined through an ungoverned identity equivalence;
- questionnaire form/order/randomization generates apparent branches that are then narrated sociologically.

Therefore FIELD FORGE needs not only geometry governance but **homology-identification governance**.

---

# 2. ACTUAL CURRENT MATERIAL THAT MOTIVATED THIS PASS

This pass used existing Rawlsing/Library evidence already owned by the project.

Examples include:

- WVS Wave 1 active/inactive membership of labour unions and political parties;
- Afrobarometer membership/attendance in religious groups, development associations, business groups and trade unions;
- WVS Wave 7 metadata for mode of collection, interview language, interview privacy, duration and interviewer-assessed respondent interest;
- GSS 2024 multimode / mode-experiment topology and weight restrictions;
- WVS `W_WEIGHT`, documented as adjusting age, sex, education and region marginals toward target-population distributions;
- existing EPR adapter/provenance work showing that country/entity routing itself has historically required explicit governance;
- `09_POSITION_ROLE_AUTHORITY_CONTRACT_R1.md`, which already permits multi-role variables and warns against position/disposition circularity but does not yet define full cross-space lineage conservation.

No new source acquisition is proposed.

---

# 3. CROSS-SPACE ACTIVE-INPUT EXCLUSIVITY

A variable may lawfully have multiple semantic/analytic roles.

That does **not** mean it may actively construct both sides of the same homology claim.

New hard law:

```text
FOR A GIVEN POSITION ↔ DISPOSITION HOMOLOGY ANALYSIS,
NO ACTIVE MEASUREMENT ANCESTRY MAY OCCUR
ON BOTH SIDES OF THE DIVIDE.
```

The word `ANCESTRY` matters.

This is not enough:

```text
position variable name = religious_embeddedness_index
disposition variable name = religious_attendance
names differ
→ no overlap
```

If the position index contains the exact attendance measurement, the homology is contaminated.

---

# 4. CROSS_SPACE_INPUT_OVERLAP_AUDIT

Every homology build should deterministically emit:

```text
CROSS_SPACE_INPUT_OVERLAP_AUDIT {
    homology_build_id

    position_active_measurement_ancestry[]
    disposition_active_measurement_ancestry[]

    exact_direct_overlap[]
    derived_ancestry_overlap[]
    context_only_shared_refs[]

    overlap_disposition
    resolution_actions[]
    provenance
}
```

Suggested states:

```text
CLEAN_ACTIVE_ANCESTRY_SEPARATION
CONTEXT_ONLY_SHARED
DIRECT_ACTIVE_OVERLAP
DERIVED_ANCESTRY_OVERLAP
RESOLVED_BY_POSITION_PRIMARY_BUILD
RESOLVED_BY_DISPOSITION_PRIMARY_BUILD
RESOLVED_BY_SUPPLEMENTARY_PROJECTION
BLOCK_HOMOLOGY_CIRCULARITY
UNRESOLVED
```

Respondent identity, source/wave/country scope, weight references, and routing/risk-set identity may of course be shared as context/record linkage. They do not become active coordinates merely because they are shared.

---

# 5. MULTI-ROLE VARIABLES REQUIRE ALTERNATE BUILDS, NOT DOUBLE COUNTING

Suppose organizational membership is lawfully interpretable as both:

```text
ORGANIZATIONAL_EMBEDDEDNESS_POSITION
```

and:

```text
CIVIC / POLITICAL DISPOSITION OR PRACTICE
```

Then possible lawful analyses include:

```text
BUILD A — POSITION PRIMARY
membership active in position space
membership excluded/supplementary in disposition space
```

```text
BUILD B — DISPOSITION PRIMARY
membership active in disposition space
membership excluded/supplementary in position space
```

The comparison between A and B is informative.

Forbidden default:

```text
membership active on both sides
→ strong homology
→ sociological interpretation
```

Position Role Authority may authorize multiple uses.

The geometry build must choose a noncircular use for the exact claim being tested.

---

# 6. PRIMARY HOMOLOGY MUST BE POST-HOC TO INDEPENDENT SPACE CONSTRUCTION

The intellectual point of the dual-space design is that the two spaces are allowed to disagree.

Therefore primary homology evidence must preserve their independence.

Preferred sequence:

```text
FREEZE POSITION GEOMETRY SPECIFICATION
        ↓
BUILD POSITION SPACE

FREEZE DISPOSITION GEOMETRY SPECIFICATION
        ↓
BUILD DISPOSITION SPACE / ATLAS

ONLY THEN
LINK BY EXACT RESPONDENT ID / RISK SET
        ↓
MEASURE CORRESPONDENCE
```

Hard law:

```text
PRIMARY HOMOLOGY EVIDENCE
MUST NOT REQUIRE RE-OPTIMIZING THE TWO SPACES
TO MAKE THEM CORRESPOND.
```

---

# 7. JOINTLY OPTIMIZED CROSS-SPACE METHODS ARE SECONDARY

Methods that explicitly maximize cross-table association can be useful.

Examples conceptually include:

- canonical-correlation-style methods;
- partial least squares;
- co-inertia / co-structure methods;
- supervised joint embeddings;
- learned cross-space latent factors.

But their output answers:

> What common structure can be extracted if the method is allowed to optimize for common structure?

That is not identical to:

> How homologous are the independently constructed social-position and disposition spaces?

Therefore classify such outputs as:

```text
OPTIMIZED_CROSS_SPACE_ASSOCIATION_DIAGNOSTIC
```

not primary independent homology evidence.

They may nominate motifs or reveal missed structure, but later structural interpretation must know how the relation was produced.

---

# 8. PRIMARY HOMOLOGY EVIDENCE OPTIONS

Candidate post-hoc evidence over independently frozen spaces may include:

- disposition-space barycenters by position-space region/modalities;
- position-space barycenters by disposition complex/region;
- region×region weighted contingency;
- mutual information between independently frozen region assignments;
- conditional density shifts;
- neighborhood composition correspondence;
- distance/correspondence diagnostics that do not refit the source spaces;
- exact repertoire prevalence over position neighborhoods;
- pressure-footprint topology itself.

No single metric becomes ontology.

The object should preserve a profile.

---

# 9. RESPONDENT-LINK PERMUTATION AS A NULL TEST

The two spaces are linked by respondent identity.

That creates a powerful hostile test.

Within the exact lawful risk set, preserve each independently built geometry but permute the respondent correspondence under a governed null scheme.

Conceptually:

```text
REAL RESPONDENT LINK
→ observed homology profile

PERMUTED RESPONDENT LINKS
→ null homology distribution
```

If observed homology is not materially stronger/more structured than the lawful permutation null, do not promote it.

Permutation must respect relevant design/risk-set constraints where necessary. Do not shuffle across respondents who were not eligible for the same measurement surface.

This is descriptive identification, not causal proof.

---

# 10. HELD-OUT / CROSS-FITTED HOMOLOGY

Same-sample geometry and homology can overfit high-dimensional surfaces.

Where method permits, use:

```text
TRAINING RESPONDENTS
→ estimate/freeze geometry bases

HELD-OUT RESPONDENTS
→ supplementary projection into frozen spaces
→ measure position↔disposition correspondence
```

This is especially valuable when:

- many modalities exist;
- rare categories have leverage;
- candidate regions/clusters are learned;
- model-based disposition representations are used.

Possible evidence states:

```text
IN_SAMPLE_DESCRIPTIVE_HOMOLOGY
HELD_OUT_REPLICATED_HOMOLOGY
BOOTSTRAP_STABLE_HOMOLOGY
PERMUTATION_DISTINCT_HOMOLOGY
UNSTABLE_HOMOLOGY
UNDERPOWERED
```

Do not require held-out proof for every exploratory picture, but require stronger evidence before structural promotion.

---

# 11. MEASUREMENT REGIME IS A SEPARATE DIAGNOSTIC LAYER

The instruments themselves provide measurement-context variables.

Examples in current material include:

```text
interview mode
interview language
form / ballot / split
question order / randomized section where known
interview privacy
interview duration
interviewer-assessed respondent interest
```

These are not ordinary position/disposition coordinates by default.

Proposed class:

```text
MEASUREMENT_REGIME_DIAGNOSTIC_ONLY
```

unless separate semantic authority establishes another role.

---

# 12. MEASUREMENT_REGIME_SENSITIVITY_PROFILE

Before a geometry feature receives sociological interpretation, compute where feasible:

```text
MEASUREMENT_REGIME_SENSITIVITY_PROFILE {
    geometry_or_footprint_ref

    mode_refs[]
    language_refs[]
    form_split_refs[]
    privacy_or_interviewer_context_refs[]

    axis_or_region_associations
    disposition_shift_by_regime
    pressure_shift_by_regime

    randomized_design_evidence_if_any
    observational_only_regime_evidence

    sensitivity_state
    provenance
}
```

Candidate states:

```text
LOW_OBSERVED_REGIME_SENSITIVITY
MODERATE_REGIME_SENSITIVITY
HIGH_REGIME_SENSITIVITY
RANDOMIZED_MEASUREMENT_EFFECT_EVIDENCE
REGIME_CONFOUNDED_WITH_SAMPLE_COMPOSITION
UNOBSERVED
UNRESOLVED
```

Hard law:

```text
MEASUREMENT REGIME DIFFERENCE
!=
SOCIAL POSITION DIFFERENCE
```

and:

```text
SOCIAL GEOMETRY THAT TRACKS MODE / FORM / INTERVIEW CONTEXT
REQUIRES CAUTION BEFORE STRUCTURAL INTERPRETATION.
```

---

# 13. RANDOMIZED SOURCE DESIGN CAN BECOME A DIAGNOSTIC ASSET

Where the exact questionnaire/source authority proves random assignment of:

- section order;
- wording arm;
- mode experiment;
- form/split treatment;

FIELD FORGE can use that randomization to test measurement sensitivity.

This is stronger than treating randomized routing merely as an inconvenience.

But randomization authority must be exact.

Do not infer random assignment because a field is called `random` or because forms appear balanced.

---

# 14. WEIGHTED GEOMETRY LANGUAGE NEEDS A CORRECTION

`27` proposed the candidate label:

```text
TARGET_POPULATION_RELATIONAL_GEOMETRY
```

This may overstate what ordinary calibration weights establish.

For example, current WVS documentation says `W_WEIGHT` adjusts selected sample marginals such as age, sex, education and region toward the target population distribution.

That does not by itself prove that every multivariate relational structure in the weighted sample is an unbiased estimate of the full target-population social geometry.

Therefore prefer conservative states:

```text
UNWEIGHTED_SAMPLE_RELATIONAL_GEOMETRY
SOURCE_WEIGHT_ADJUSTED_RELATIONAL_GEOMETRY
EQUAL_CONTEXT_POOLING_GEOMETRY
```

Reserve a stronger state such as:

```text
DESIGN_AUTHORIZED_TARGET_POPULATION_RELATIONAL_ESTIMATE
```

for uses where source/design/estimand authority actually supports that claim.

Hard law:

```text
CALIBRATED MARGINS
!=
PROVED POPULATION RELATIONAL STRUCTURE.
```

This clause refines the terminology proposed in `27` and the current-state note.

---

# 15. WEIGHT-CONSTRUCTION OVERLAP IS PART OF GEOMETRY PROVENANCE

Some source weights are explicitly constructed from variables that may also be active in position geometry.

Example pattern:

```text
weight calibrated on age + sex + education + region
```

while:

```text
education + region + possibly age/sex
```

help construct the local position space.

That is not an error.

But it means weighted modality masses are partly a deliberate design/calibration product.

Required diagnostic:

```text
WEIGHT_GEOMETRY_DEPENDENCY_PROFILE {
    weight_ref
    documented_calibration_or_construction_variables[]
    active_geometry_measurement_overlap[]
    known_design_purpose
    unknown_construction_components[]
    provenance
}
```

Then compare where feasible:

```text
UNWEIGHTED SAMPLE GEOMETRY
vs
SOURCE-WEIGHT-ADJUSTED GEOMETRY
```

and report geometry displacement.

Do not narrate calibration-induced changes as purely discovered social structure.

---

# 16. EXTERNAL STRUCTURAL ALIGNMENT REQUIRES A REAL ENTITY/GROUP CROSSWALK

`13_HEGEMONY_SUBHEGEMONY_EVIDENCE_PROFILE_R1.md` correctly permits political-power alignment only where existing EPR/GeoEPR or other adopted structural authority can be lawfully joined.

A country adapter is not sufficient.

The required semantic proposition is often:

```text
THIS EXACT SURVEY IDENTITY CATEGORY
CORRESPONDS TO / IS CONTAINED IN / OVERLAPS
THIS EXACT EXTERNAL STRUCTURAL GROUP
AT THIS TIME AND SCOPE.
```

That is a separate authority problem.

Current FIELD FORGE search in this pass did not locate a governed current survey-category → EPR-group crosswalk. Therefore the political-power dimension must remain:

```text
UNOBSERVED / MISSING JOIN AUTHORITY
```

unless such authority is subsequently located or constructed.

Do not infer absence of all historical mapping work from this search result; the requirement is to locate **current governed authority** before use.

---

# 17. NEW MANUAL AUTHORITY CANDIDATE — EXTERNAL STRUCTURAL GROUP CROSSWALK

If no current owner is found, a likely finite manual authority class is:

```text
SURVEY_IDENTITY_TO_EXTERNAL_GROUP_AUTHORITY
```

Potential grain:

```text
source_family
wave / exact source scope
country
question_implementation_id
response_category / exact identity value

external_system
external_group_id
external_group_temporal_scope

relation_type
    EXACT_EQUIVALENCE
    SURVEY_CATEGORY_SUBSET_OF_EXTERNAL_GROUP
    EXTERNAL_GROUP_SUBSET_OF_SURVEY_CATEGORY
    PARTIAL_OVERLAP
    AGGREGATE_ONLY
    NON_EQUIVALENT
    UNRESOLVED

allowed_join_operations
forbidden_inferences
source/evidence refs
version/provenance
```

This is a strong candidate for bounded GPT-5.6 manual adjudication because names, translations and umbrella categories are not safe join logic.

Hard law:

```text
COUNTRY MATCH
+
SIMILAR ETHNIC / SECT / LANGUAGE LABEL
!=
GROUP EQUIVALENCE.
```

---

# 18. HEGEMONY PROFILE SHOULD FAIL SOFTLY, NOT IMPUTE POWER ALIGNMENT

A hegemony profile can remain useful with:

```text
population prevalence
cross-position reach
high-position alignment
geographic concentration
counter-complex structure
```

while:

```text
political_power_alignment = UNOBSERVED
```

Do not delay all hegemony evidence merely because EPR joining is unavailable.

But do not substitute high-income/high-education survey respondents for external political-power authority either.

This preserves the existing profile logic.

---

# 19. NEGATIVE-CONTROL GEOMETRY DIAGNOSTICS

Where exact source metadata provides administrative/randomization variables that should not constitute substantive social position, project them supplementary onto the learned geometries.

Examples:

```text
ballot/form
random split arm
mode-assignment arm where truly randomized
administrative implementation ID
```

If a supposedly substantive axis is dominated by such variables, investigate:

- routing/exposure artifact;
- source implementation artifact;
- weighting/design artifact;
- accidental missingness geometry.

Do not automatically delete the axis; first identify why the association exists.

---

# 20. RESPONSE-STYLE ARTIFACT REMAINS AN OPEN QUESTION

Even after DK/refusal/not-asked modalities are governed, substantive response scales may contain respondent-level method tendencies such as:

- extreme-category use;
- midpoint avoidance;
- generalized acquiescence;
- indiscriminate high/low trust response style.

Current FIELD FORGE does not yet have enough source-specific engineering to declare a universal response-style correction.

Therefore:

```text
RESPONSE_STYLE_DIAGNOSTIC
= OPEN ENGINEERING QUESTION
```

not a new latent trait or automatic correction.

Any future work must respect exact response-scale semantics and avoid subtracting genuine strong opinion as if it were measurement noise.

---

# 21. REVISED HOMOLOGY PRODUCER

```text
POSITION GEOMETRY FAMILY
        +
DISPOSITION GEOMETRY ATLAS / REPERTOIRE OBJECTS
        ↓
CROSS-SPACE INPUT OVERLAP AUDIT
        ↓
MEASUREMENT-REGIME SENSITIVITY CHECK
        ↓
WEIGHT-GEOMETRY DEPENDENCY PROFILE
        ↓
FREEZE INDEPENDENT SPACE SPECIFICATIONS
        ↓
EXACT RESPONDENT LINK UNDER COMMON RISK SET
        ↓
POST-HOC HOMOLOGY PROFILE
        +
PERMUTATION NULL
        +
HELD-OUT / BOOTSTRAP STABILITY WHERE FEASIBLE
        ↓
PRESSURE FOOTPRINT / COUPLING CANDIDACY
```

Jointly optimized cross-space methods may run alongside this path as secondary diagnostics, not replace it.

---

# 22. HOSTILE CASES

## H1 — direct double use

Union membership is active in position and disposition space.

Result: `BLOCK_HOMOLOGY_CIRCULARITY` unless alternate nonoverlapping builds are used.

## H2 — derived double use

Position composite contains church attendance; disposition repertoire also contains church attendance.

Different output names do not cure shared ancestry.

## H3 — supervised homology masquerading as discovery

Cross-space method explicitly learns axes maximizing covariance and then output is called `independent homology`.

Forbidden.

## H4 — mode axis mistaken for ideology

Disposition axis separates web respondents from interviewer-administered respondents in a multimode source.

Must emit measurement-regime sensitivity before structural interpretation.

## H5 — calibration geometry narrated as spontaneous structure

Weighted position geometry changes mainly because the weight calibrates active education/region marginals.

Must expose weight-construction overlap.

## H6 — EPR label join by lexical resemblance

Survey identity label resembles an EPR group name.

Forbidden political-power alignment without current crosswalk authority.

## H7 — equal-country weight used inside a single-country geometry as if substantively informative

If weight is constant within the exact local scope, it adds no within-scope relational information; record purpose rather than fetishizing presence of a weight column.

---

# 23. IMMEDIATE FIELD FORGE EXPERIMENT IMPLICATIONS

The first geometry prototypes should deliberately include tests for:

```text
A. active-ancestry overlap = zero
B. sample vs source-weight-adjusted geometry displacement
C. projection of mode/form/routing variables as supplementary diagnostics
D. respondent-link permutation null
E. train/held-out projection where feasible
F. independent homology vs optimized cross-space diagnostic comparison
```

A prototype that cannot report these things is not yet ready to support structural interpretation.

---

# 24. TERMINAL FINDING

The dual-space idea survives another hostile turn, but its epistemic standard is now stronger.

Rawlsing should not ask only:

> Are position and disposition geometrically associated?

It should ask:

> Does the association survive removal of shared measurement ancestry, respect exact respondent exposure, remain distinguishable from measurement regime and weight construction, exceed a lawful respondent-link null, and persist when the spaces are not jointly optimized to agree?

Only then does `HOMOLOGY` become a serious empirical object rather than an attractive visualization.

Strongest hard laws from this pass:

```text
NO ACTIVE MEASUREMENT ANCESTRY ON BOTH SIDES OF A HOMOLOGY CLAIM.

NO PRIMARY HOMOLOGY PROOF FROM A METHOD DESIGNED TO MAXIMIZE HOMOLOGY.

MEASUREMENT REGIME IS NOT SOCIAL POSITION BY DEFAULT.

CALIBRATED MARGINS ARE NOT PROVED POPULATION RELATIONAL STRUCTURE.

WEIGHT CONSTRUCTION IS PART OF GEOMETRY PROVENANCE.

EXTERNAL GROUP POWER REQUIRES EXPLICIT SURVEY→GROUP JOIN AUTHORITY.
```
