# FIELD FORGE R1 — HEGEMONY / SUBHEGEMONY EVIDENCE PROFILE

Status: **EXPLORATORY / NON-BINDING / PROSPECTIVE STRUCTURAL EVIDENCE CONTRACT**

Rawlsing needs a way to distinguish:

```text
what is common
what is prestigious
what is institutionally/politically aligned
what is locally dominant
what is broadly convertible
what is oppositional
```

without collapsing all of those into one scalar `hegemony` score.

This document proposes an evidence profile informed by Gramsci but constrained to Rawlsing's existing evidence.

---

# 1. HARD LAW

```text
MAJORITY != HEGEMONY
MINORITY != SUBALTERN
HIGH-INCOME SURVEY TAIL != RULING CLASS
LOCAL DOMINANCE != GLOBAL DOMINANCE
```

Hegemony is relational and multidimensional.

---

# 2. UNIT OF ANALYSIS

The candidate hegemonic object is usually not a single question response.

Prefer:

```text
DISPOSITION COMPLEX
REPERTOIRE
SYMBOLIC / MORAL BOUNDARY COMPLEX
IDENTITY-ATTITUDE ARTICULATION
```

at exact context grain.

---

# 3. OBSERVABLE DIMENSIONS AVAILABLE FROM EXISTING RAWLSING EVIDENCE

## A. POPULATION PREVALENCE

Weighted prevalence of the complex within exact population scope.

Necessary but insufficient.

## B. CROSS-POSITION REACH

How broadly the complex appears across the local relational position space.

A complex with 60% national prevalence concentrated almost entirely in one social region is different from a 60% complex distributed across nearly all regions.

Candidate evidence:

```text
coverage across position neighborhoods
prevalence by region
entropy/dispersion across position space
minority penetration into opposed regions
```

## C. HIGH-POSITION ALIGNMENT

Alignment with the high-resource/high-capital portions of the **observed survey position space**, where that geometry is well supported.

Use cautious label:

```text
HIGH_POSITION_ALIGNMENT
```

not `ELITE_ALIGNMENT` unless independent elite authority exists.

## D. POLITICAL-POWER ALIGNMENT

Where existing adopted EPR / GeoEPR or other Rawlsing structural authority supplies lawful group-power information, compute relation between disposition prevalence and politically empowered identity positions.

Hard law:

```text
GROUP POWER
!= INDIVIDUAL GROUP MEMBER ATTITUDE.
```

This dimension is an alignment between independently grounded structures.

## E. GEOGRAPHIC REACH / CONCENTRATION

Using already-adopted geographic authority:

- nationally diffuse;
- regionally concentrated;
- concentrated in politically/economically central areas;
- peripheral/local.

No geographic centrality metric may be invented without its own authority.

## F. TEMPORAL PERSISTENCE / EXPANSION

Only where exact cross-wave comparability exists:

- persistent reach;
- expanding reach;
- declining but durable reach;
- conjuncturally volatile.

Do not call these `dominant/residual/emergent` automatically.

## G. COUNTER-COMPLEX STRUCTURE

Identify stable alternative complexes with:

- substantial prevalence;
- concentrated social bases;
- distinct position geometry;
- different power alignment;
- temporal persistence where lawful.

This is evidence for counterhegemonic/subhegemonic interpretation, not automatic semantic promotion.

---

# 4. PROPOSED OBJECT

```text
HEGEMONIC_ALIGNMENT_EVIDENCE_PROFILE {
    profile_id
    context_id
    disposition_complex_ref

    population_prevalence
    cross_position_reach
    position_concentration_profile
    high_position_alignment

    political_power_alignment_if_observed
    geographic_reach_if_observed
    temporal_reach_if_comparable

    counter_complex_refs[]
    local_dominance_profiles[]

    unavailable_dimensions[]
    uncertainty
    evidence_refs
    provenance
}
```

No scalar total is required.

---

# 5. MANUAL HEGEMONY INTERPRETATION COURT

A high-intelligence court may interpret the evidence profile with contextual/theoretical authority.

Candidate dispositions:

```text
HEGEMONIC_CANDIDATE
SUBHEGEMONIC_CANDIDATE
COUNTERHEGEMONIC_CANDIDATE
WIDELY_PREVALENT_NOT_POWER_ALIGNED
POWER_ALIGNED_BUT_NARROW
LOCAL_DOMINANT_ONLY
PLURAL_CONTESTED_COMMON_SENSE
INSUFFICIENT_HEGEMONY_EVIDENCE
UNRESOLVED
```

Do not force a single winner.

A context may exhibit multiple partially overlapping hegemonic complexes across different social arenas.

---

# 6. COMMON SENSE AS EMPIRICAL OBJECT

Gramscian `common sense` should not be reduced to popularity.

A strong candidate common-sense complex should show some combination of:

- broad cross-position reach;
- internal contradiction / sedimented repertoires;
- low dependence on one narrow social fraction;
- persistence across otherwise divergent groups;
- default-like rather than self-conscious ideological positioning where survey semantics allow such inference.

The last property may be difficult to observe directly in surveys and should remain `UNOBSERVED` unless the question semantics genuinely distinguish reflective ideology from taken-for-granted judgment.

Potential object:

```text
COMMON_SENSE_REACH_PROFILE
```

not `DOXA` by default.

---

# 7. SUBHEGEMONY

Working evidence definition:

```text
SUBHEGEMONIC CANDIDATE
=
strong local reach / local symbolic dominance
within bounded position/identity region
+
limited or asymmetric reach/conversion
into broader high-power/high-position spaces.
```

This is especially important because a person can inhabit several arenas simultaneously.

A disposition/repertoire can be:

```text
dominant in local communal field
subordinate nationally
prestigious within subculture
stigmatized in elite professional field
```

The model must allow these relations to coexist.

---

# 8. CAPITAL CONVERSION LINK

Subhegemony becomes especially informative when linked to later `CAPITAL_CONVERSION_RELATION` objects.

If a repertoire/resource bundle has:

- strong value inside local region F;
- weak/negative value in region G;
- limited social reach outside F;

that is powerful evidence for bounded-field dominance.

Do not infer the field from one conversion relation alone.

---

# 9. PERSONA-GENERATION VALUE

Hegemony profiles tell V3 something different from pressure footprints.

Pressure footprint:

> Which disposition complexes become more or less probable around this position?

Hegemony profile:

> Which of those complexes are socially broad/default, locally dominant, power-aligned, or counterposed within the surrounding context?

This matters because an uncommon belief held inside a powerful institutional milieu is a different developmental environment from an equally uncommon belief confined to a marginal local milieu.

PRE-V3 can expose that difference without asserting what the actor personally believes.

---

# 10. HOSTILE CASES

Reject/flag:

- `>50% = hegemonic`;
- `minority = subaltern`;
- `richest observed quintile = ruling class`;
- attaching EPR group power directly to individual attitudes without survey evidence;
- treating one survey item's prestige connotation as institutional dominance;
- collapsing multiple dimensions into one score before proof;
- inferring national dominance from a regional sample;
- inferring temporal dominance without measurement comparability;
- treating local subcultural dominance as global cultural capital.

---

# 11. CURRENT RECOMMENDATION

Hegemony should be a **late interpretive profile over already-produced empirical evidence**, not an early feature or universal coefficient.

Pipeline:

```text
position space
+ disposition complexes
+ pressure footprints
+ existing political/geographic structural authority
-> HEGEMONY EVIDENCE PROFILE
-> manual interpretation/admission
```

This preserves Gramsci's distinction between prevalence and power while staying within Rawlsing's actual evidence.
