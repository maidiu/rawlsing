# REC-06 — Afrobarometer R5 Q60 driver battery court

Branch: `agent/vozhd-trii-rec06-afro-q60-driver-battery`  
Exact start: `e410799cc7afa95e758ebe774f141e053e2bb711`  
TIR: `TIR-018`  
Exact denominator: `Afrobarometer R5 Q60A-Q60G` only.

## Holding

Q60D is **not isolated**. Q60A-Q60G are one source-native perceived-corruption-prevalence battery with a common stem and a shared ordinal extent response surface. The only substantive row-to-row change is the actor/institution target.

The source predicate is:

`respondent perceived prevalence / extent of target involvement in corruption`

It is not respondent tolerance/permissibility, generalized trust, performance evaluation, or experienced bribery/exposure.

All seven recovered historical V525b-style driver assignments are therefore defective at driver grain:

- Q60A and Q60E: `politicalStability` — wrong construct.
- Q60B: `civicEngagement` — wrong construct.
- Q60C, Q60D, Q60F, Q60G: `corruptionTolerance` — categorical prevalence→tolerance mismatch.

Historical confidence is not used as evidence of error: four of the defective rows are marked high confidence. The error is established by source predicate/driver mismatch.

## Current same-grain succession

The sealed R10G cumulative package was verified at SHA-256:

`d524010ffbce1e095da98cfd22e25e83f3293998e10a3a3f2b0ed1717ff4f70f`

Exact implementation-identity and var-code search of `R10G_S08_FULL_3324_COORDINATE_AUTHORITY.csv` finds **zero** exact Q60A-Q60G semantic-unit members. Therefore none of the seven historical defects is already repaired by an exact same-grain R10G successor.

The current QSM/P2 structural surface is not counted as a successor: final Q60 rows are `GOVERNED_NON_DIRECTIONAL_DISPOSITION`, and R03/HQ law forbids treating relation/structural-owner grain as silent supersession of R10G semantic-unit coordinates.

## Existing R10G vocabulary candidate

REC-06 creates no authority. It records that R10G already contains an exact semantic vocabulary suitable for a later authorized same-grain successor court:

- driver: `stateCapacityIntegrity`
- facet: `public_integrity_and_corruption`
- component: `perceived_corruption_prevalence`
- axis: `axis__perceived_corruption_prevalence`
- role: `PERCEPTION_OR_BELIEF`

R10G explicitly defines `public_integrity_and_corruption` as perceived prevalence/extent of corruption among public institutions/officials and explicitly excludes tolerance of corruption. Analogous existing R10G rows for parliamentarians, government officials, tax officials, judges/magistrates, the President/Prime Minister office, police, and local-government representatives corroborate the vocabulary without creating Q60 succession.

## Seven-row disposition

All seven rows: `CURRENT_SUCCESSOR_CANDIDATE_REQUIRED`.

No `HISTORICAL_AND_CURRENT_UPHELD` rows.  
No `HISTORICAL_DEFECT__CURRENT_SUCCESSOR_REPAIRS` rows.  
No `SOURCE_LIMITED__UNRESOLVED` rows.

## Scope guard

This court does not revalidate V525b broadly, does not review unrelated Afrobarometer batteries, does not rewrite the driver ontology, and does not author/install any successor authority.
