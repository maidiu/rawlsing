# FIELD FORGE R1 — LOCAL RELATIONAL POSITION SPACE CONTRACT

Status: **EXPLORATORY / NON-BINDING / PROSPECTIVE PRODUCER CONTRACT**

This document specifies the strongest feasible first-stage social-space producer Rawlsing can build from its existing governed survey corpus.

The objective is not to discover universal classes.

It is to recover **context-local relational position geometry** from variables already admitted by Position Role Authority.

---

# 1. PRIMARY LAW

```text
LOCAL SOCIAL GEOMETRY
!=
GLOBAL CLASS ONTOLOGY
```

A position-space build answers:

> Where are respondents located relative to one another in the structured distribution of the position/resource coordinates that this exact survey context actually observes?

It does not answer by itself:

- what the true classes are;
- what the true fields are;
- which axis is economic/cultural capital;
- which group is hegemonic;
- which position causes which disposition.

---

# 2. CONTEXT GRAIN

The default geometry should be local to an exact governed context, potentially:

```text
source family × wave × country × lawful respondent universe
```

A broader multi-country or multi-wave geometry requires separate measurement/comparability authority.

Do not force all CLOSED_35 observations into one universal coordinate system.

Hard law:

```text
LOCAL AXIS COORDINATE
IS NOT PORTABLE BY LABEL.
```

---

# 3. WHY MCA / GEOMETRIC DATA ANALYSIS IS THE PRIMARY CANDIDATE

The current survey substrate contains many categorical/ordinal position variables.

Multiple Correspondence Analysis (MCA) / geometric data analysis is attractive because it:

- treats categories/modality relations geometrically;
- does not require one arbitrary universal metric over unlike position variables;
- allows active variables to construct the geometry while supplementary variables are projected afterward;
- aligns with Bourdieusian social-space practice;
- reveals opposition, proximity, volume/composition structure, and modality contributions without forcing discrete classes first.

MCA is a **descriptive geometry instrument**.

It is not semantic authority.

---

# 4. ACTIVE VS SUPPLEMENTARY VARIABLES

## Active

Only variables with explicit Position Role Authority may actively construct the position space.

Typical candidate roles:

```text
ECONOMIC_RESOURCE_POSITION
MATERIAL_DEPRIVATION_POSITION
OCCUPATIONAL_POSITION
EMPLOYMENT_RELATION_POSITION
EDUCATIONAL_CREDENTIAL_POSITION
ORIGIN_BACKGROUND_POSITION
RELATIONAL_IDENTITY_POSITION where justified
GEOGRAPHIC_POSITION where justified
MIGRATION_MOBILITY_POSITION where justified
```

## Supplementary

Project afterward where useful:

- subjective class/status;
- ideology;
- attitudes/dispositions;
- attitude complexes;
- institutional trust;
- moral/symbolic boundary complexes;
- demographic descriptors intentionally excluded from the active geometry;
- source-defined groups used to inspect but not define the geometry.

Hard anti-circularity law:

```text
IF ATTITUDE VARIABLES DEFINE THE POSITION SPACE,
THE SAME ANALYSIS MAY NOT THEN CLAIM
THE POSITION SPACE EXPLAINS THOSE ATTITUDES
WITHOUT EXPLICIT CIRCULARITY ADMISSION.
```

---

# 5. MODALITY ENGINEERING

The geometry must preserve source-native meaning as far as possible.

Do not casually convert every ordinal variable into a continuous score.

Potential operations must be governed:

- exact categorical modalities;
- source-native ordered categories;
- rare-category handling;
- routing/not-applicable separation;
- explicit missing categories where analytically appropriate;
- collapsing categories only under positive semantic authority.

Hard law:

```text
SPARSE MODALITY
!= PERMISSION TO MERGE SEMANTICALLY DISTINCT CATEGORIES.
```

Continuous variables require a separately governed treatment.

Until FIELD FORGE establishes a lawful partition/continuous geometry protocol:

```text
UNGOVERNED QUANTILE BINNING
!= POSITION AUTHORITY.
```

---

# 6. WEIGHTING / SAMPLE DESIGN

The position space must bind to existing survey weight/design law.

A geometry based on raw respondent frequency when design weights are required is not automatically admissible.

Exact implementation choice (weighted MCA variant, preprocessing, replicate strategy) should be validated per source family.

The producer must preserve:

```text
weight/design refs
respondent denominator
routing universe
active-variable coverage
modality counts
missingness patterns
```

---

# 7. OUTPUT — DESCRIPTIVE GEOMETRY, NOT CLASSES

Proposed core object:

```text
LOCAL_POSITION_SPACE {
    position_space_id
    context_id
    respondent_universe_ref
    input_manifest_ref
    weight_design_ref

    method
    dimensions[]
    inertia_profile
    modality_coordinates
    modality_contributions
    respondent_coordinates_or_sufficient_projection_representation
    supplementary_projection_results

    missingness_diagnostics
    stability_diagnostics
    bootstrap_or_resampling_diagnostics where appropriate

    provenance
    replay_contract
}
```

No semantic dimension names are required at production time.

Initially dimensions may remain:

```text
DIM_01
DIM_02
DIM_03
...
```

---

# 8. MANUAL AXIS / REGION INTERPRETATION COURT

After geometry exists, a manual agentic court may inspect:

- strongest contributing modalities;
- coordinate oppositions;
- supplementary projections;
- source context;
- Position Role Authority;
- stability across resamples/subsets;
- neighboring dimensions.

Possible dispositions:

```text
INTERPRETABLE_AS_CAPITAL_VOLUME_CANDIDATE
INTERPRETABLE_AS_CAPITAL_COMPOSITION_CANDIDATE
INTERPRETABLE_AS_RURAL_URBAN_POSITION_CANDIDATE
INTERPRETABLE_AS_IDENTITY_POWER_POSITION_CANDIDATE
MIXED_DIMENSION_NO_SINGLE_SEMANTIC_LABEL
UNSTABLE_DIMENSION
UNRESOLVED
```

Hard law:

```text
LARGE INERTIA
!= SOCIOLOGICAL IMPORTANCE

HIGH CONTRIBUTION
!= STRUCTURAL CAUSATION.
```

---

# 9. REGIONS / FRACTIONS ARE DERIVED, NOT PRIMARY

Discrete regions may be useful for pressure-footprint calculation or persona generation.

But do not begin with latent-class ontology.

Candidate regions can be generated by:

- geometry neighborhoods;
- hierarchical clustering on principal components;
- source-semantic cut surfaces;
- predefined profile queries;
- manual structural-region adjudication.

Any discrete region must remain a **derived operational view** unless separately admitted as a sociological class/fraction/field position.

Proposed object:

```text
POSITION_REGION {
    parent_position_space_ref
    exact membership_or_boundary_rule
    derivation_method
    semantic_status
    support
    stability
}
```

---

# 10. TESTS FOR PARTIAL AUTONOMY / FIELD-LIKE STRUCTURE

The position-space producer may compute evidence useful for later field candidacy but must not mint a field.

Possible evidence:

- local subgeometry stable after controlling for wider position axes;
- resource/disposition valuation differs inside vs outside a bounded region;
- internally structured oppositions recur;
- attitude/disposition complexes map differently inside the region;
- conversion of a resource differs by region/context.

These become candidate evidence for a later `FIELD_CANDIDACY` court.

---

# 11. CROSS-CONTEXT COMPARISON

The default cross-context comparison object is **structural signature**, not coordinate equivalence.

Compare things like:

```text
which admitted variables dominate local geometry
number/stability of major dimensions
capital-volume-like vs capital-composition-like patterns
relative location of subjective-class categories
position-disposition homology patterns
pressure-footprint topology
```

Do not compare raw MCA coordinates across contexts unless a separate common-space/comparability law establishes that operation.

---

# 12. PERSONA-GENERATION USE

Given a generated adult profile with known position attributes:

1. locate or probabilistically place the profile in the relevant local position space;
2. preserve uncertainty where the profile does not uniquely determine location;
3. query pressure-footprint/disposition distributions associated with nearby lawful regions/configurations;
4. use those distributions as PRE-V3 possibility evidence;
5. never equate the geometric location with the person's realized worldview.

Conceptually:

```text
PROFILE
-> PROBABILISTIC LOCAL POSITION
-> EMPIRICAL DISPOSITION LANDSCAPE
-> V3 GENERATION INPUT
```

---

# 13. HOSTILE CASES

The implementation should fail/reject or remain typed unresolved when asked to:

- treat harmonized labels as globally equivalent coordinates;
- collapse rare but semantically distinct modalities for convenience;
- use attitude variables actively and then claim them as explained outcomes;
- interpret axis 1 as class by default;
- convert subjective class directly into objective class;
- use raw unweighted sample geometry where weighting is mandatory;
- compare coordinates across sources without portability authority;
- call a cluster a field/class automatically;
- use administrative/routing categories as structural coordinates without authority.

---

# 14. CURRENT RECOMMENDATION

FIELD FORGE should prototype **local MCA-like position spaces** only after a bounded Position Role Authority court has created an exact input manifest.

The first prototype should be deliberately descriptive and over-instrumented with diagnostics.

The goal is not a pretty two-dimensional chart.

The goal is to learn whether the existing Rawlsing corpus contains enough relational position structure to support the later structural ontology honestly.
