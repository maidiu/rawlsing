# G-SR07-R3 — WVS7 DOCUMENTARY RECOVERY W6

Status: `COMPLETE__NON_DISPOSITIVE_W6_DOCUMENTARY_RECOVERY__POSITIVE_AUTHORITY_ONLY__HQ_JOIN_REQUIRED`

Repository: `maidiu/rawlsing`

Worker branch: `agent/vozhd-trii-gsr07r3-wvs7-doc-w6`

Verified exact starting HEAD: `d643edc4d4a0be155e92c374b8d1d4b560140fbb`

Pinned Authority 84 read from Trii control: `04a0109aa170c6041b199e5c6130a39a8e0f6029`

Accepted R2 inputs consumed only at their exact accepted refs:

- Lane A: `a06f2bced8677453cf77fec5e622cb334a9810a5`
- Lane B: `a07f449221256e0c52cffd3f85812d30c0f047fc`
- Lane C: `930d89b8930c21c9a8f1180093ee15ed10c495e4`

## Scope

This return covers only:

1. Turkey 2018
2. Ukraine 2020
3. United Kingdom - Great Britain 2022
4. United Kingdom - Northern Ireland 2022
5. Uruguay 2022
6. USA 2017
7. Uzbekistan 2022
8. Venezuela 2021
9. Vietnam 2020
10. Zimbabwe 2020

The run remained sibling-blind. No sibling documentary-return branch or output was consumed.

## Source-order discipline

Authority-83 source order was applied:

1. exact official WVSA country technical/methodology/sample-design/questionnaire material;
2. exact WVSA/source-owner material surfaced through authorized deposits/mirrors with explicit provenance;
3. exact retained Library material;
4. checked-in accepted documentary authority.

IHSN country deposits were used for exact producer-document identity because they identify The World Values Survey as producer and the World Values Survey Association as document author. UK Data Service Study 9311 exposes the WVSA methodology forms for Great Britain and Northern Ireland directly. The Ukrainian national WVS report supplies positive country-specific survey facts. Generic wave-level WVS sampling boilerplate was not promoted into country-specific target/frame/design authority.

## Positive country-universe recovery

### Ukraine 2020

Positive producer/national-team authority recovers:

- target: adult population age 18+, including citizens and residents who had lived in the settlement at least two months;
- coverage deviation: territories outside Ukrainian government control in Donetsk and Luhansk oblasts and the Autonomous Republic of Crimea excluded;
- actual regime: multistage stratified sampling with random selection at every stage;
- mode: face-to-face CAPI on tablets;
- fieldwork: 2020-07-21 through 2020-08-17; 1,289 interviews.

The report explicitly says stage detail is in a fuller report, so the exact sample frame is **not** inferred.

### United Kingdom - Great Britain 2022

The WVSA methodology form positively recovers:

- adult target age 18+ in Great Britain (England, Scotland, Wales);
- no excluded or under-represented groups; Scotland and Wales intentionally over-represented for analysis, followed by national weighting;
- frame: Royal Mail Postcode Address File, Small User version;
- first stage: postcode sectors, stratified random probability-proportional-to-size;
- second stage: 30 PAF addresses per selected postcode sector;
- within participating household: one adult 18+ randomly selected electronically;
- 273 postcode sectors total, including 56 Scotland and 45 Wales;
- stratifiers: country/region, population-density tertiles, percentage owner-occupied.

### United Kingdom - Northern Ireland 2022

The WVSA methodology form positively recovers:

- entire adult target age 18+;
- no groups excluded, over-represented, or under-represented;
- frame: Royal Mail Postcode Address File, Small User version;
- first stage: postcode sectors, stratified random PPS;
- second stage: 30 PAF addresses per selected postcode sector;
- within household: one adult 18+ randomly selected electronically;
- 45 postcode sectors;
- stratifiers: population-density tertiles and percentage owner-occupied.

### Other W6 countries

Exact WVSA-authored questionnaire/methodology/sample-design/technical-report identities were recovered for Turkey, Uruguay, USA, Venezuela, Vietnam, and Zimbabwe, but the required substantive technical bodies were not recovered through the authorized host at the claim grain needed for target/frame/actual-design closure. They remain `DOCUMENT_IDENTIFIED_CONTENT_NOT_RECOVERED`.

For Uzbekistan 2022, official WVS/GESIS survey identity and PAPI mode were recovered, but an exact country questionnaire/methodology/sample-design document was not located. Target/frame/actual design therefore remain `DOCUMENT_NOT_LOCATED`.

## D01-D02 / D04-D10 documentary routing harvest

Positive W6 routing recovery is deliberately narrow.

### D01 — country administration / omissions

Great Britain and Northern Ireland methodology forms positively enumerate omitted WVS core and demographic items:

- core: Q91-Q93, Q119, Q139-Q141, Q144-Q145, Q151, Q174-Q175, Q189;
- demographics: the form records Q267-Q278 country-of-parent birth items for immigrants, Q276-Q278 spouse/mother/father education, Q280, Q282, Q283, Q287.

The documents state these exclusions were agreed with WVSA, primarily because the pilot questionnaire exceeded one hour; Q151 and Q189 also had item-specific concerns.

No other W6 country receives a D01 completion by inference.

### D10 — country additions

Great Britain positively documents:

- QUK001-Q50 before demographics;
- Q117B politicians in the corruption battery;
- Q256A UK nations in the closeness battery, explicitly routed by country;
- country-specific lists at Q223, Q260, Q272, Q275, Q281, Q288, Q289, Q290.

Northern Ireland positively documents the same family plus:

- Q254B proud to be Irish;
- Q257B Ireland;
- Q256A UK nations explicitly routed by country.

Only the explicit `routed by country` fact is promoted as a routing predicate. Country-specific item existence is not silently converted into a subgroup predicate.

### D02 / D04 / D08 / D09 residuals

- No W6 document supplied an exact positive D02 respondent-level determinant for Q217-Q220. Q206/Q207 and missing-code incidence are not substituted.
- D04 applies in W6 only to the accepted Political Trust countries Venezuela, Vietnam, and Zimbabwe. No per-respondent Q294 A/B assignment key or replay source was recovered. The accepted 50/50 form law is not treated as a row determinant.
- D08/D09 apply in W6 only to Zimbabwe under accepted Gender Version 2 scope. The exact Version-2 target administration matrix and target subgroup predicates were not recovered from the identified Zimbabwe documents.
- D05/D06 are not applicable to this W6 batch because accepted MENA scope is Iraq/Jordan/Lebanon/Egypt.
- D07 is not applicable because accepted WEE scope is India 2023 only.

## Fail-closed holdings

- No target/frame/design fact was inferred from `I_PSU`, weights, source incidence, neighboring waves, or generic WVS convention.
- No questionnaire target was treated as administered merely because a released column exists.
- No Q294 A/B row membership was inferred from populated-slot complement.
- No Q217-Q220 row determinant was manufactured from Q206/Q207.
- No Gender target matrix was inferred from populated columns.
- `D03`, `D11`, and `D12` were not adjudicated.
- No G-SR07 certification was launched.
- No C05R2B was launched.
- No V553+ or semantic architecture was mutated.
- No architecture selection was attempted.

## Package

The additive W6 return consists of exactly the Authority-83 eight-file package:

- `RESULT.md`
- `RESULT.json`
- `COUNTRY_DOCUMENT_AUTHORITY.csv`
- `COUNTRY_UNIVERSE_RECOVERY.csv`
- `ROUTING_DOCUMENTARY_RECOVERY.csv`
- `DOCUMENT_IDENTITY_AND_PROVENANCE.csv`
- `UNRESOLVED_GAPS.csv`
- `CHANGED_FILES.txt`

No raw survey bytes or large source/document binaries are committed.

## Disposition

`W6_DOCUMENTARY_HARVEST_COMPLETE__GB_NI_POSITIVE_TARGET_FRAME_DESIGN_D01_D10__UKRAINE_POSITIVE_TARGET_COVERAGE_ACTUAL_DESIGN__OTHER_COUNTRY_CLAIMS_FAIL_CLOSED__D02_D04_GENDER_RESIDUALS_PRESERVED__HQ_JOIN_ONLY`
