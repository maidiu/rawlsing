# CLOSED35-L2-AFR5 — Routing, Weight, and Coordinate Authority

## Court boundary

Canonical source root is fixed as Afro Barometer Round 5.sav, SHA-256 c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651.

This worker did not open raw survey bytes, execute the source, or run P2X. Physical facts cited below are inherited from accepted Authority71/72 and S35 packets. New authority in this return comes only from producer documentation.

## 1. Q10B / Q47C routing and code 997

### Q10B

The final July-2015 merged codebook defines Q10B as physical attack and lists only 0-3, 9, 998 and -1. It does not list 997.

Afrobarometer's July-2015 revision note is stronger on routing history: Tanzania's Q10B had an incorrect Swahili translation ("feared theft in the home" instead of "physical attack"), so Q10B was dropped in the revised Tanzania dataset.

That closes a routing fact: TAN_Q10B_DOCUMENTED_DROPPED_IN_FINAL_REVISION.

It does not close the numeric-code proposition Q10B=997. No producer document recovered here explicitly says that the final merged carrier encodes the dropped Tanzania observations as 997. The exact code meaning therefore remains DOCUMENTARY_AUTHORITY_UNKNOWN.

### Q47C

The final merged codebook defines Q47C (rating South Africa) with 0-10, 98, 99 and -1; it omits 997. Neighboring merged entries such as Q47D explicitly print 997=Not asked, demonstrating that Afrobarometer could and did state 997 when intended. Neighbor semantics are not transferable.

The South Africa R5 national codebook explicitly says "Question Number: Q47C-Not asked." This closes a country-routing fact: SAF_Q47C_DOCUMENTED_NOT_ASKED.

It still does not close Q47C=997. No producer document recovered explicitly binds code 997 on Q47C to that South Africa not-asked state. Exact code meaning remains DOCUMENTARY_AUTHORITY_UNKNOWN.

### Physical system missing versus numeric special codes

Authority71 already established that Q47C has both a declared numeric 997 user-missing state and SPSS system-missing incidence. Documentary evidence does not authorize collapsing them. Under S35 physical law they remain distinct physical states. Because the producer documents recovered here do not assign system-missing an application/routing semantic, system missing must not be interpreted as not asked, refused, don't know, or missing-code -1 merely from incidence.

## 2. Administrative routing carriers

Authority71 identifies WEST.AFR, EAST.AFR, SOUTHERN, NORTH.AF, and R1.ONLY..R4.ONLY as exact raw routing/filter-looking carriers.

Official Round-5 documentation strongly documents question-level country routing, including explicit "not asked" statements and Arab/Afrobarometer country modules. But no producer document recovered by exact-name searches binds the above administrative field names to a legal routing function.

Disposition: OPAQUE_RAW_ROUTING_METADATA / DOCUMENTARY_AUTHORITY_UNKNOWN.

They may survive source realization as physical/administrative fields. They may not be semantic owners for eligibility until producer authority is recovered.

## 3. Country coordinate authority

The final merged R5 codebook names COUNTRY_ALPHA, not COUNTRY.

COUNTRY_ALPHA is labeled "Country in alphabetical order" with values 1-35. The printed map lists 1 Algeria through 35 Zimbabwe but omits a printed label for code 10. This is producer authority for COUNTRY_ALPHA only.

Authority71's exact source reconnaissance instead identifies a raw carrier named COUNTRY with a different source-native coding/dictionary. No exact-release producer document recovered here names that carrier or binds it to COUNTRY_ALPHA.

Later Afrobarometer codebooks retain historical country coordinate concepts, but cross-wave reuse is expressly forbidden by this court. Secondary harmonization tables were not admitted as source authority.

Disposition for exact raw COUNTRY -> official R5 country identity: DOCUMENTARY_AUTHORITY_UNKNOWN.

## 4. Weight and design authority

### Exact final-release codebook carriers

The July-2015 merged codebook contains:

- WITHINWT — "Within country weighting factor." It adjusts the sample based on individual selection probabilities, explicitly naming region, gender, urban/rural distribution, household size and enumeration-area size.
- COMBINWT — "Multi-country weighting factor." It applies the selection-probability adjustment and treats every country as if its sample were the same size; the codebook says it should be used when reporting multi-country results.

No ACROSSWT, AFRICAWT or AFCOMBWT entry was found in the final merged R5 codebook. Therefore those names are not admitted as exact final-release source carriers by this worker.

### Design construction

Afrobarometer's official Weights Protocol says that, from Round 4 onward, comprehensive within-country weights are based on individual selection probabilities and are identified as WITHINWT. It explicitly states that Round 5 is weighted to the enumeration-area level, with stratification and the sampling frame entering the calculation; rural designs may additionally include SSU probability.

The Round-5 codebook's country technical forms describe nationally representative, clustered, stratified, multistage area-probability samples and country-specific deviations. No single flattened design claim may erase those country forms.

### Documented use by estimand

The producer's sampling guidance and R5 manual provide a lawful-use distinction:

1. National descriptive statistics / frequencies / cross-tabulations: use WITHINWT where present.
2. Cross-national descriptive comparisons and equal-country multi-country reporting: use COMBINWT.
3. Relationship/coefficient analyses under the R5 reporting protocol: disable WITHINWT and COMBINWT before contingency, correlation or regression coefficients.
4. Exceptional "Africa" distributions: the R5 manual discusses AFCOMBWT but simultaneously labels the assumption that the surveyed countries represent Africa as unwarranted. Because AFCOMBWT is absent from the final merged codebook, this is retained only as method-protocol history, not an admitted exact source carrier.
5. Later manuals retrospectively call ACROSSWT the equal-country sample-size constituent for R2-R5 and say COMBINWT combines WITHINWT and ACROSSWT. Because ACROSSWT is absent from the exact July-2015 merged codebook, that statement does not by itself authorize an exact carrier in this canonical source.

There is therefore no universal "default R5 weight." Producer authority is estimand-specific.

## 5. Closure matrix

- WITHINWT role/construction/use: CLOSED at documented national-descriptive scope.
- COMBINWT role/use: CLOSED at documented multi-country-descriptive scope.
- Weight-off rule for relationship/coefficient analysis: CLOSED as Afrobarometer R5 reporting protocol.
- ACROSSWT/AFCOMBWT as exact canonical-source carriers: DOCUMENTARY_AUTHORITY_UNKNOWN; do not inject.
- Q10B Tanzania routing circumstance: CLOSED as "dropped" in July-2015 revision; Q10B=997 exact semantic binding remains UNKNOWN.
- Q47C South Africa routing circumstance: CLOSED as "not asked"; Q47C=997 exact semantic binding remains UNKNOWN.
- Exact raw COUNTRY to official R5 coordinate binding: UNKNOWN.
- WEST.AFR / EAST.AFR / SOUTHERN / NORTH.AF / R1.ONLY..R4.ONLY semantic routing roles: UNKNOWN.

The unresolved items are semantic-authority gaps, not permission to normalize or infer around the source.
