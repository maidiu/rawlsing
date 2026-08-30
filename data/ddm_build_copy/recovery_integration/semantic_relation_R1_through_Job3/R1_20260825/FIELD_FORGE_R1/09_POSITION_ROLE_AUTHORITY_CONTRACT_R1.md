# FIELD FORGE R1 — POSITION ROLE AUTHORITY CONTRACT

Status: **EXPLORATORY / NON-BINDING / PROSPECTIVE AUTHORITY DESIGN**

This document defines the first new authority class FIELD FORGE presently believes Rawlsing may need before a lawful Empirical Social-Space Observatory can be built.

The problem is simple:

```text
A QUESTION / DEMOGRAPHIC VARIABLE EXISTS
!=
RAWLSING KNOWS WHAT STRUCTURAL ROLE IT MAY PLAY.
```

A variable can be semantically well understood as a survey item while still lacking authority to function as:

- an active coordinate of social position;
- a resource/capital proxy;
- a relational identity position;
- a trajectory/origin indicator;
- a supplementary self-placement;
- a disposition/attitude;
- a context control only;
- an ineligible administrative variable.

FIELD FORGE therefore proposes a manually adjudicated, context-specific authority layer:

```text
POSITION_ROLE_AUTHORITY
```

The machine may consume this authority. It may not infer these roles dynamically from labels, data type, correlation, embeddings, or generic sociology.

---

# 1. WHY MANUAL AUTHORITY IS REQUIRED

Examples of semantic mistakes ordinary code can make:

```text
education -> CULTURAL_CAPITAL
income -> CLASS
religion -> ATTITUDE
race -> DEMOGRAPHIC_CONTROL_ONLY
subjective class -> OBJECTIVE_POSITION
occupation -> ECONOMIC_CAPITAL
urban/rural -> GEOGRAPHY_ONLY
```

None of these mappings is universally lawful.

Education may function as:

- credentialed institutional position;
- a cultural-capital proxy of limited scope;
- an origin/trajectory signal;
- merely an achieved demographic descriptor;
- a source-incomparable category whose exact structural use is unresolved.

Religion/sect may function as:

- a relational communal position;
- institutional embeddedness proxy;
- an identity marker;
- a disposition if the item is about belief/practice rather than membership;
- a source-specific routing variable;
- several of these simultaneously, with different target uses.

Subjective class may be useful precisely because it is **not** objective position: it can be projected as self-placement relative to a separately constructed position space.

Therefore:

```text
VARIABLE SEMANTICS
!=
POSITION ROLE
```

and:

```text
POSITION ROLE
MUST BE TARGET-USE AND CONTEXT SPECIFIC.
```

---

# 2. EXACT AUTHORITY GRAIN

A Position Role Authority row must bind at minimum:

```text
source_family
source_wave / exact source scope
country / governed geography where relevant
question_implementation_id / exact variable identity
respondent/risk-set scope
position_role
active_vs_supplementary_status
allowed_operations
forbidden_inferences
semantic_basis_refs
source_authority_refs
routing/applicability_refs
comparability_limit_refs where applicable
authority_version
provenance
```

No global role may be inferred merely because the same harmonized label occurs in multiple sources.

Potential exact scope:

```text
VARIABLE X may be ACTIVE_EDUCATIONAL_CREDENTIAL
in source S / country C / wave W
for LOCAL_POSITION_SPACE construction,
while remaining NONPORTABLE to another source/wave
unless separate portability authority exists.
```

---

# 3. PROPOSED ROLE VOCABULARY

The vocabulary should remain small enough to govern but rich enough not to collapse distinctions.

## A. ACTIVE_POSITION_COORDINATE

The variable may participate directly in constructing local relational position geometry.

Subroles may include:

```text
ECONOMIC_RESOURCE_POSITION
MATERIAL_DEPRIVATION_POSITION
OCCUPATIONAL_POSITION
EMPLOYMENT_RELATION_POSITION
EDUCATIONAL_CREDENTIAL_POSITION
HOUSEHOLD_RESOURCE_POSITION
ORIGIN_BACKGROUND_POSITION
RELATIONAL_IDENTITY_POSITION
GEOGRAPHIC_POSITION
MIGRATION_MOBILITY_POSITION
ORGANIZATIONAL_EMBEDDEDNESS_POSITION
OTHER_CONTEXT_LOCAL_POSITION
```

A subrole is not automatically a Bourdieusian capital.

## B. RESOURCE_OR_CAPITAL_PROXY_CANDIDATE

The variable may be used as evidence for a resource that plausibly has exchange/valuation effects in a local social field.

This is deliberately stronger than ACTIVE_POSITION_COORDINATE.

Examples:

- income may be an economic-resource proxy;
- education may be credential/institutionalized cultural-capital evidence;
- organizational ties may be social-capital evidence where the item genuinely measures such ties.

Hard law:

```text
POSITION_COORDINATE
!= CAPITAL
```

## C. RELATIONAL_IDENTITY_POSITION

The variable places a respondent relative to a socially meaningful identity order whose effect is contextual rather than intrinsic.

Examples may include, where source semantics and local social relevance support them:

- sect;
- religion;
- ethnicity;
- race;
- caste;
- language group;
- nationality/minority status.

Hard law:

```text
IDENTITY POSITION
!= FIXED DISPOSITION
!= UNIVERSAL EFFECT.
```

## D. TRAJECTORY_ORIGIN_INDICATOR

The variable informs origin/current-position difference or life-course trajectory.

Examples:

- parental education;
- parental occupation;
- previous occupational state;
- migration origin/destination;
- childhood class/origin indicators where actually present.

Hard law:

```text
ORIGIN INDICATOR
!= OBSERVED FULL TRAJECTORY.
```

## E. SUPPLEMENTARY_POSITION_DESCRIPTOR

The variable may be projected onto an already constructed geometry but may not define the active geometry.

Prime examples:

- subjective social class;
- subjective status;
- self-described ideology when the geometry is intended to remain position-based;
- self-perceived economic rank.

This separation permits comparison between objective relational location and self-placement without circularity.

## F. ATTITUDE_OR_DISPOSITION_ONLY

The variable belongs in the attitude/disposition space and must not be used to define the position geometry for the same analysis unless an explicit circularity court permits it.

## G. CONTEXT_OR_SCOPE_ONLY

The variable defines context/risk set but is not itself treated as a structural coordinate.

Examples may include source form, ballot, administrative region codes used solely for sampling/routing, or temporal identifiers.

## H. ADMINISTRATIVE_OR_INELIGIBLE

The variable is not a lawful structural/position input.

## I. UNRESOLVED_POSITION_ROLE

The source semantics are known, but the structural role has not been established.

This is a valid state.

---

# 4. MULTI-ROLE AUTHORITY

A variable may lawfully have multiple target-use roles.

For example:

```text
religious denomination
    RELATIONAL_IDENTITY_POSITION
    + possibly ORGANIZATIONAL_EMBEDDEDNESS_EVIDENCE

education
    EDUCATIONAL_CREDENTIAL_POSITION
    + TRAJECTORY_ORIGIN comparison if parental education also exists
    + RESOURCE_OR_CAPITAL_PROXY_CANDIDATE under a separate target use
```

Do not force one variable to one ontology slot.

The authority must bind role to operation.

---

# 5. FORBIDDEN AUTOMATIC PROMOTIONS

The runtime must reject:

```text
COLUMN_NAME contains income -> ECONOMIC_CAPITAL
COLUMN_NAME contains educ -> CULTURAL_CAPITAL
religion category -> FIELD
ethnicity category -> HEGEMONY
subjective class -> OBJECTIVE_CLASS
occupation code -> CLASS_FRACTION
urban -> MODERNITY
rural -> TRADITION
high education -> LIBERAL
```

Correlation with attitudes does not create position role authority.

MCA contribution does not create position role authority.

Predictive importance does not create position role authority.

---

# 6. MANUAL AGENTIC ADJUDICATION PACKET

A GPT-5.6-level manual court should receive, for each candidate variable:

1. exact questionnaire wording;
2. response options;
3. source documentation/codebook context;
4. routing/applicability context;
5. source family/wave/country;
6. existing semantic authority;
7. observed respondent coverage and missingness diagnostics;
8. neighboring questions/module context where relevant;
9. proposed target use;
10. exact theory-derived role definitions from FIELD FORGE.

It should return:

```text
ADMITTED_ROLE
ADMITTED_WITH_LIMITS
SUPPLEMENTARY_ONLY
ATTITUDE_ONLY
CONTEXT_ONLY
INELIGIBLE
UNRESOLVED
```

plus exact rationale and authority references.

The court is not asked to decide whether the variable empirically matters. That is downstream compute.

It decides only what uses are semantically lawful.

---

# 7. POSITION-SPACE INPUT MANIFEST

Once authority is frozen, each local position-space build consumes a deterministic manifest:

```text
POSITION_SPACE_INPUT_MANIFEST {
    context_id
    respondent_universe_ref
    weight_design_ref

    active_position_variables[] {
        exact_variable_ref
        admitted_role_ref
        modality_scope
    }

    supplementary_position_variables[]
    forbidden_attitude_variables[]
    unresolved_variables[]

    missingness_policy_ref
    routing_refs
    provenance
}
```

The geometry engine may not widen this manifest.

---

# 8. WHY THIS MATTERS FOR RAWLSING PERSONA GENERATION

The purpose is not to produce a sociological taxonomy for its own sake.

A lawful position space allows Rawlsing to ask:

> Given this adult/parent profile, where does it sit relationally among respondents in the exact social context represented by the survey?

Then the machine can map that location to joint disposition probability without pretending that income, education, sect, race, or any other coordinate has one universal effect.

This directly serves:

```text
PROFILE
-> LOCAL RELATIONAL POSITION
-> DISPOSITION PRESSURE LANDSCAPE
-> PLAUSIBLE JOINT WORLDVIEW
```

while preserving:

```text
POPULATION POSITION
!= INDIVIDUAL DESTINY.
```

---

# 9. CURRENT STATUS

FIELD FORGE recommendation:

```text
POSITION_ROLE_AUTHORITY
= HIGH-PRIORITY NEW MANUAL AUTHORITY CANDIDATE
```

It should be constructed only after the exact CLOSED_35 observability matrix identifies the finite current candidate variable surface.

Do not automate semantic role assignment first and attempt to repair it later.
