# 05 — CURRENT CORPUS AND CODEBOOK GROUNDING

## Fixed empirical universe for FIELD FORGE

FIELD FORGE works from the Rawlsing sources already in scope. The current CLOSED_35 survey universe spans nine families:

- GSS
- WVS
- EVS
- Arab Barometer
- Afrobarometer
- Asian Barometer
- Latinobarómetro
- South Asia
- LiTS

Do not infer that all families observe the same forms of position, capital, identity, attitude, or trajectory. Variation in instrument design is a fact to model, not a nuisance to erase.

## Known examples from actual instrument grounding

These examples are reminders of feasibility, not universal schemas. Re-open the exact current codebook/questionnaire before using them.

### Arab Barometer — Lebanon / Wave VII example

The source has unusually useful materials for the Lebanon hostile case discussed in FIELD FORGE, including forms of:

- governorate / geographic position;
- neighborhood affluence or related local material context;
- respondent education;
- household income and relation to median/reference income;
- detailed Muslim denomination/sect distinctions, including Sunni/Shia/Ja'fari or related source-native categories where present in the exact form;
- large batteries on politics, religion, economics, identity, migration, media, and institutions.

This makes it plausible to test configuration-dependent disposition redistribution such as geography × sect × education × resources without pretending each component has a universal effect.

### Latinobarómetro 2023 example

Source documentation contains useful forms of:

- subjective class placement;
- food insecurity / income adequacy;
- religion/devoutness;
- ethnicity/race;
- respondent education;
- parental education;
- household-head education/occupation;
- social-media/media variables;
- ideology and institutional-trust batteries.

This is useful for distinguishing objective-ish position indicators, origin/trajectory proxies, subjective self-placement, and disposition/boundary material rather than collapsing them into one SES index.

## General observability conclusion

The existing adult-survey substrate is comparatively strong for:

- economic/resource position;
- education/credentials;
- employment/occupation in many contexts;
- geography/urbanity;
- religion/sect/ethnicity/caste/race in source-specific ways;
- institutional and political attitudes;
- religious/moral attitudes;
- national/geopolitical identity;
- trust, democracy/authority, redistribution/economic morality;
- gender/family attitudes;
- migration/media/organization in some contexts;
- subjective class/status in some contexts;
- parental/origin proxies in some contexts.

It is weaker and inconsistent for fine-grained cultural consumption, peer-field prestige, detailed social-network capital, embodied cultural competencies, childhood local status systems, and many forms of elite-specific capital.

Those weaknesses are `OBSERVABILITY_LIMIT`s. Do not infer the missing dimensions and do not request new sources in FIELD FORGE.

## Mandatory codebook-grounding exercise for a new agent

Before independent FIELD FORGE design, inspect at least four contrasting source contexts using the exact source-native questionnaire/codebook plus Rawlsing's current normalized/governed manifests:

1. Arab Barometer Lebanon or another exact AB context capable of the sect/geography/resource example;
2. Latinobarómetro context with subjective class/origin/resource information;
3. at least one of GSS / WVS / EVS;
4. LiTS or another current family/context with useful origin/trajectory/education/occupation structure.

If exact file paths have moved, search the repository/Library and record the current path/identity rather than substituting internet memory.

For each context produce a compact observability sheet:

```text
CONTEXT_ID
SOURCE_FAMILY
WAVE / YEAR
COUNTRY / SCOPE

POSITION CANDIDATES
- exact variable id
- exact wording/labels
- respondent universe
- routing/applicability
- missing/refusal/dk categories
- objective / subjective / origin / identity / resource candidate role

DISPOSITION CANDIDATES
- exact variable id
- semantic authority link
- direction/role where governed
- source-native group/J candidate or exact J authority if current

TRAJECTORY / ORIGIN PROXIES
- parental education/occupation
- migration
- cohort
- subjective mobility/status
- other exact source-native evidence

OBSERVABILITY LIMITS
- desired dimension not present
- present but not comparable
- present only as weak proxy
```

## Source-native authority remains upstream

A FIELD FORGE `POSITION_ROLE_AUTHORITY` cannot silently redefine source meaning.

Example:

If a source asks for highest completed degree, FIELD FORGE may adjudicate that exact variable as an active credential-position indicator for a local geometry. It may not rewrite the source into a richer measure of embodied cultural capital.

If a survey asks subjective class, it can be useful as self-placement or symbolic-position evidence. It does not become objective class by convenience.

If a source records sect, that variable may define a relational identity position within the exact context. It does not automatically become religion-as-attitude, institutional embeddedness, or causal “sect pressure.”

## Routing/missingness grounding

Never collapse:

```text
NOT ASKED
ROUTED NONAPPLICABLE
REFUSED
DON'T KNOW
MISSING
ADMINISTRATIVE/NONRESPONDENT
UNRESOLVED ROUTING
```

Geometry must have an explicit law for whether each modality is active, passive/supplementary, excluded from a specific analysis with provenance, or causes the operation to fail closed.

A routed nonapplicable response must not accidentally become a social-distance coordinate.

## Cross-survey caution

Construct local spaces first.

A Lebanese position space and a GSS position space may both reveal relational dimensions interpretable as capital volume/composition, but their raw axes/coordinates are not automatically equivalent.

```text
LOCAL AXIS SIMILARITY != MEASUREMENT PORTABILITY
SHARED LABEL != CROSS-INSTRUMENT EQUIVALENCE
```

Compare derived structural signatures only under a separately governed comparability/portability law. Until then, cross-context comparison should be cautious, qualitative/structural where licensed, and explicit about noncomparability.
