# FIELD FORGE R1 — GEOMETRY GOVERNANCE / MODALITY BALANCE / MISSINGNESS

Status: **EXPLORATORY / NON-BINDING / METHOD-GOVERNANCE NOTE**

Even after Position Role Authority is correct, a social-space method can distort the geometry through ordinary technical choices.

Therefore:

```text
SEMANTICALLY LAWFUL INPUTS
!=
AUTOMATICALLY LAWFUL GEOMETRY.
```

This document identifies the main method-level governance requirements for MCA/geometric-data-analysis prototypes.

---

# 1. VARIABLE-BLOCK DOMINANCE

A block with many variables/modalities can dominate the geometry simply by having more representation.

Example:

```text
8 economic-resource variables
2 education variables
1 sect variable
1 region variable
```

A naive MCA may make the economic block disproportionately define the space even if that weighting is an artifact of questionnaire design.

FIELD FORGE should therefore evaluate block-aware approaches such as:

- Multiple Factor Analysis / grouped-variable weighting;
- specific MCA variants;
- manually governed active-block weights;
- sensitivity across lawful block specifications.

Hard law:

```text
NUMBER OF QUESTIONS IN SOURCE
!=
SOCIOLOGICAL IMPORTANCE OF DIMENSION.
```

---

# 2. BLOCK MANIFEST

Position Role Authority should optionally group active variables into analytical blocks:

```text
ECONOMIC_RESOURCE_BLOCK
OCCUPATION_EMPLOYMENT_BLOCK
EDUCATION_CREDENTIAL_BLOCK
ORIGIN_TRAJECTORY_BLOCK
RELATIONAL_IDENTITY_BLOCK
GEOGRAPHY_BLOCK
MOBILITY_BLOCK
ORGANIZATIONAL_BLOCK
```

These are method blocks, not necessarily ontology primitives.

The geometry contract should record whether blocks are:

- equally weighted;
- source-frequency weighted;
- authority-weighted;
- unbalanced/raw.

Default recommendation for prototype:

**prefer balance/sensitivity over raw questionnaire-count weighting.**

---

# 3. RARE MODALITIES

Rare categories can sit at extreme geometric coordinates and disproportionately influence dimensions.

But rare categories may be sociologically important minorities.

Therefore:

```text
RARE
!= NOISE
```

and:

```text
RARE
!= AUTOMATICALLY ACTIVE.
```

Potential handling states:

```text
ACTIVE_RARE_MODALITY
SUPPLEMENTARY_RARE_MODALITY
SEMANTICALLY_COLLAPSED_UNDER_AUTHORITY
INSUFFICIENT_SUPPORT_FOR_ACTIVE_GEOMETRY
```

Any category collapse requires semantic authority, not frequency threshold alone.

---

# 4. ROUTED / NOT-APPLICABLE / MISSING STATES

Do not use one generic `missing` modality.

Distinguish:

```text
NOT_ASKED_BY_DESIGN
ROUTED_NONAPPLICABLE
REFUSED
DONT_KNOW
MISSING_SOURCE_DATA
UNRESOLVED_ROUTING
```

These states have different semantics.

Where possible, routed/nonapplicable states should not create a fake social-position axis.

Method-specific handling must preserve exact state provenance.

---

# 5. CONTINUOUS VARIABLES

Before a general continuous/ordinal protocol exists, compare lawful alternatives rather than silently binning.

Candidate methods:

- source-native categories as active;
- continuous variables supplementary to MCA;
- mixed-data factor methods;
- manually adjudicated meaningful partitions;
- sensitivity over multiple semantically lawful codings.

Never use quantiles merely because the software expects categories and then interpret quantile boundaries sociologically.

---

# 6. IDENTITY BLOCKS

Race/sect/caste/religion/ethnicity can dominate geometry when categories are strongly associated with many other variables.

That may reflect real social structure, or it may obscure the resource geometry FIELD FORGE is trying to examine.

Therefore test at least two lawful views where appropriate:

```text
RESOURCE_POSITION_SPACE
    identity projected supplementary

FULL_RELATIONAL_POSITION_SPACE
    identity active where Position Role Authority permits
```

The difference between the two is itself informative.

Do not assume one view is always superior.

---

# 7. STABILITY / SENSITIVITY

Every prototype position space should report sensitivity to:

- active-variable subset;
- block weighting;
- rare-modality treatment;
- missing/routing treatment;
- sample resampling;
- weight/design application;
- inclusion/exclusion of relational identity block.

A semantic interpretation should not be frozen if it disappears under small lawful method changes.

Potential state:

```text
GEOMETRY_ROBUST
GEOMETRY_PARTIALLY_ROBUST
GEOMETRY_METHOD_SENSITIVE
GEOMETRY_UNSTABLE
```

---

# 8. DIRECT VS MODEL-DERIVED POSITION

Observed respondents with complete lawful inputs have direct geometric placement.

Generated personas or respondents with missing coordinates may require probabilistic/model-derived placement.

Hard law:

```text
DIRECT_SURVEY_POSITION
!=
MODEL_DERIVED_POSITION POSTERIOR.
```

Store the distinction explicitly.

---

# 9. SEMANTIC INTERPRETATION MUST SEE METHOD DIAGNOSTICS

A GPT/manual axis interpretation court should not receive only a pretty plot.

It must receive:

- exact active variables/blocks;
- block weights;
- modality contributions;
- inertia;
- rare modality flags;
- routing/missingness handling;
- sensitivity/stability results;
- supplementary projections;
- source context.

This reduces the risk of narrating an artifact of preprocessing as social structure.

---

# 10. CURRENT RECOMMENDATION

The first FIELD FORGE prototype should compare a small family of lawful geometry specifications and ask:

> Which social-position structures remain stable across reasonable method choices?

Only robust recurring geometry should feed structural interpretation.
