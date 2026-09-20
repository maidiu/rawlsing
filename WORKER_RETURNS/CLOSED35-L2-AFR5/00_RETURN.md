# CLOSED35-L2-AFR5 — Afrobarometer Round 5 Documentary Authority Closure

Branch: agent/rabochii-closed35-l2-afrobarometer-r5-authority-r1

Base: agent/vozhd-premain-fiabc-s35-fanin-r1@770d95c1a604ea1f47ac2971b923673c14c42984

Canonical source: Afro Barometer Round 5.sav

Canonical SHA-256: c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651

## Disposition

PARTIAL.

Producer-authoritative research closes the Round-5 weighting/design-use burden to explicit estimand scopes and recovers strong country-routing facts for Q10B and Q47C. It does not supply the final missing documentary link needed to assign numeric code 997 on Q10B or Q47C, nor does it bind the exact raw COUNTRY carrier to the final codebook's COUNTRY_ALPHA coordinate. The exact administrative routing-carrier names inherited from Authority71 also remain unbound by producer documentation.

No raw carrier was opened. No source execution or measured P2X was run.

## Strongest recovered producer authority

1. Final merged R5 codebook (July 2015)
   - COUNTRY_ALPHA is the documented country coordinate.
   - Q10B lists 0-3, 9, 998, -1 and omits 997.
   - Q47C lists 0-10, 98, 99, -1 and omits 997.
   - Neighboring questions explicitly print 997=Not asked where Afrobarometer intended that documentation.
   - WITHINWT and COMBINWT are the exact weighting variables documented in the final merged release.

2. July-2015 revision note
   - Tanzania Q10B was dropped because the Swahili translation asked about fear of theft rather than physical attack.
   - This closes the Tanzania routing circumstance but does not explicitly bind merged numeric 997 to that circumstance.

3. South Africa R5 codebook (May 2012)
   - Explicitly states Q47C-Not asked.
   - This closes South Africa routing for Q47C but does not explicitly bind merged numeric 997 to that circumstance.

4. Afrobarometer weight/sampling authority
   - WITHINWT is a within-country individual-selection-probability weight.
   - R5 weighting is at EA level, with stratification/sampling-frame structure and rural SSU stages where applicable.
   - COMBINWT equalizes country sample sizes on top of within-country adjustment.
   - Producer guidance: WITHINWT for national descriptive statistics; COMBINWT for multi-country/cross-national descriptive reporting.
   - R5 reporting protocol explicitly disables weights for relationship/coefficient analyses such as contingency, correlation and regression.

## Exact unknown set

AFR5-U01 — Q10B=997 exact documentary semantic binding.
- Producer final merged codebook omits 997 for Q10B.
- Producer revision note proves Tanzania Q10B was dropped.
- No producer document recovered explicitly states that Q10B value 997 means that dropped/not-asked state.
- Disposition: DOCUMENTARY_AUTHORITY_UNKNOWN.

AFR5-U02 — Q47C=997 exact documentary semantic binding.
- Producer final merged codebook omits 997 for Q47C.
- Producer South Africa R5 codebook explicitly says Q47C was not asked.
- No producer document recovered explicitly states that Q47C value 997 encodes South Africa's not-asked state.
- Disposition: DOCUMENTARY_AUTHORITY_UNKNOWN.

AFR5-U03 — exact raw COUNTRY carrier binding.
- Final merged producer codebook documents COUNTRY_ALPHA.
- Inherited exact source evidence identifies a distinct raw carrier COUNTRY.
- No producer exact-release document recovered binds COUNTRY to COUNTRY_ALPHA or another official R5 coordinate.
- Disposition: DOCUMENTARY_AUTHORITY_UNKNOWN.

AFR5-U04 — exact administrative routing carrier semantics.
- WEST.AFR, EAST.AFR, SOUTHERN, NORTH.AF, R1.ONLY..R4.ONLY are inherited raw carriers.
- Producer documents recover question-level routing but no exact-name binding for these fields.
- Disposition: DOCUMENTARY_AUTHORITY_UNKNOWN / OPAQUE_RAW_ROUTING_METADATA.

AFR5-U05 — ACROSSWT/AFCOMBWT as exact July-2015 canonical-source carriers.
- Producer manuals discuss these method variables historically/protocol-wise.
- Final merged R5 codebook does not contain them.
- Disposition: DOCUMENTARY_AUTHORITY_UNKNOWN as exact source-carrier identities; they are not admitted into realization by this worker.

## Physical/documentary separation

Authority71's inherited physical fact that numeric 997 declarations coexist with SPSS system-missing incidence does not supply semantics. Numeric 997 and system missing must remain distinct. No missingness incidence may be used to infer routing.

## Admission consequence

The source is not ready for source-specific semantic realization at every named L2 surface.

The weight/design layer may be realized only at the documented scopes recorded in 02_FIELD_AUTHORITY_MAP.csv and 03_ROUTING_WEIGHT_AND_COORDINATE_AUTHORITY.md. Q10B/Q47C 997, COUNTRY carrier binding, and exact administrative carrier semantics remain fail-closed.

## Terminal

CLOSED35_L2_AFROBAROMETER_R5_DOCUMENTARY_AUTHORITY_PARTIAL__EXACT_UNKNOWN_SET_RETURNED
