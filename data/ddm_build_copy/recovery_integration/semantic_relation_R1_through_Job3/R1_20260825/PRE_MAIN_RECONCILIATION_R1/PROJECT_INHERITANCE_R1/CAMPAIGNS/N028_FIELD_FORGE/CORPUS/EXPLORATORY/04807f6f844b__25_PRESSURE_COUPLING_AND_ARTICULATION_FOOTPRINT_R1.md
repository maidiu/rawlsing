# FIELD FORGE R1 — PRESSURE COUPLING / ARTICULATION FOOTPRINT

Status: **EXPLORATORY / NON-BINDING / PROSPECTIVE PRE-V3 PRODUCT**

This document provides an empirical replacement for the vague phrase `inter-strata pressure`.

The central object is not a causal claim that social layer A acts on social layer B.

It is the respondent-backed fact that:

```text
THE DISPOSITIONAL FOOTPRINT ASSOCIATED WITH POSITION DIMENSION A
CHANGES DEPENDING ON POSITION DIMENSION / CONFIGURATION B.
```

FIELD FORGE calls this a:

```text
PRESSURE_COUPLING
or
ARTICULATION_FOOTPRINT
```

---

# 1. CORE EXAMPLE

Suppose the disposition distribution associated with education differs among southern Lebanese Shia respondents from the education-associated distribution among southern Lebanese Sunni respondents.

Then:

```text
EDUCATION FOOTPRINT
IS CONDITIONED BY
SECT × REGION
```

and equivalently:

```text
SECT FOOTPRINT
IS CONDITIONED BY
EDUCATION × REGION.
```

This is an empirical interaction/articulation fact.

It is not yet a causal statement about which position `acts on` the other.

---

# 2. WHY ADDITIVE MODELS ARE INSUFFICIENT

A simple additive model assumes approximately:

```text
D = effect(A) + effect(B) + effect(C)
```

But the social world may behave like:

```text
D = topology(A × B × C | context K)
```

where changing B changes the direction, destination, magnitude, or heterogeneity of A's disposition footprint.

Hard law:

```text
POSITION EFFECTS NEED NOT BE SEPARABLE.
```

---

# 3. DESCRIPTIVE STATES

A coupling producer may identify patterns such as:

```text
AMPLITUDE_MODIFICATION
    A points toward same disposition destination but more/less strongly under B

SIGN_OR_DESTINATION_REVERSAL
    A is associated with different disposition direction/region under B

BRANCH_CREATION
    joint A×B configuration creates a minority/alternative branch absent in marginal views

BRANCH_SUPPRESSION
    a branch common under A disappears under A×B

HETEROGENEITY_MODIFICATION
    B changes how internally diverse the A footprint is

NULL_COUPLING
    no materially supported nonadditive relation

UNDERPOWERED_COUPLING
NONCOMPARABLE
UNRESOLVED
```

These are descriptive topology states.

Do not automatically rename them:

- amplification mechanism;
- mediation;
- causal moderation;
- ideological articulation;
- class conditioning.

Manual structural interpretation comes later.

---

# 4. PROPOSED OBJECT

```text
PRESSURE_COUPLING_PROFILE {
    coupling_id
    context

    position_component_A_ref
    position_component_B_ref
    optional_component_C_refs[]

    target_disposition_complex_ref
    exact_risk_set_ref

    marginal_footprint_A_ref
    marginal_footprint_B_ref
    joint_configuration_footprint_ref

    nonadditivity_profile
    destination_change_profile
    branch_change_profile
    heterogeneity_change_profile

    support
    evidence_level
    uncertainty

    provenance
}
```

---

# 5. COUPLING IS N-ARY

Do not force all coupling into pairs.

Some social articulation may require:

```text
sect × geography × education
race × region × class position
religion × gender × urbanity
caste × education × generation
```

But combinatorial explosion and sparse support require strict evidence hierarchy.

Direct J3 / exact configuration evidence should be preferred.

Higher-order configurations unsupported by current authority fail closed or remain model-derived with explicit status.

---

# 6. CANDIDATE GENERATION

Compute can nominate couplings using:

- conditional mutual information;
- log-linear interaction;
- model interaction terms;
- fracture-map topology changes;
- pressure-footprint distributional differences;
- direct J2/J3 redistribution;
- local geometry region comparison.

Nomination should prioritize:

```text
large/stable topology changes
adequate respondent support
repeated appearance across multiple disposition complexes
clear minority-branch effects
```

No statistic alone creates semantic meaning.

---

# 7. ARTICULATION AS A LATER SEMANTIC INTERPRETATION

Stuart Hall's concept of articulation is useful when a relation is historically contingent rather than necessary.

A manual court may later decide that a recurrent pressure-coupling pattern is well represented as a contextual articulation.

But the empirical object should remain available even if that theoretical label is rejected.

Pipeline:

```text
PRESSURE COUPLING FACT
-> STRUCTURAL INTERPRETATION
-> optional ARTICULATION AUTHORITY
```

---

# 8. COUPLING NETWORK / TOPOLOGY

Once many lawful coupling profiles exist, Rawlsing can construct a context-local topology:

```text
position component A
    modifies footprint of B on disposition family X

position component C
    suppresses minority branch Y under A×B

position component D
    reverses the A relationship for disposition family Z
```

This becomes a much more precise successor to `inter-strata pressure`.

It is a network/hypergraph of **empirically observed conditional dependence of pressure footprints**.

---

# 9. PERSONA-GENERATION USE

For a generated profile, V3 should not apply independent demographic adjustments.

Instead it can consume the closest lawful configuration-specific footprint.

Conceptually:

```text
PROFILE
-> position configuration
-> retrieve relevant coupling profiles
-> choose disposition distribution conditioned on the full supported configuration
```

This directly reduces stereotypical additive generation.

---

# 10. HOSTILE CASES

Reject:

- interaction coefficient -> causal mechanism;
- pairwise coupling used to reconstruct unsupported higher-order configuration;
- sparse cell reversal treated as substantive;
- universalizing one context's coupling to another country;
- calling every nonadditive result `intersectionality`;
- dropping minority branches in favor of average interaction;
- assuming symmetric causal influence from a symmetric statistical interaction.

---

# 11. CURRENT RECOMMENDATION

Replace the old vague primitive:

```text
STRATUM A INTER-PRESSES STRATUM B
```

with the empirically stronger sequence:

```text
POSITION COMPONENTS / CONFIGURATIONS
-> PRESSURE FOOTPRINTS ON DISPOSITION SPACE
-> NONADDITIVE COUPLING / ARTICULATION FOOTPRINTS
-> OPTIONAL LATER STRUCTURAL INTERPRETATION
```

This is more feasible, more data-driven, and better aligned with Rawlsing's persona-generation objective.
