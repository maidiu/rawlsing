# SR09-PRE R03 — Asian Barometer raw-source reconnaissance

Status: `COMPLETE__NON_DISPOSITIVE_RECONNAISSANCE`  
Worker: `SR09-PRE-R03`  
Sources: Waves 1, 4, 5 only. Wave 6 was not used as evidence.

## Measured findings

- **Wave 1:** 12,217 rows × 217 variables; `BIG-5`; 199 variables declare SPSS user-missing ranges; 284,794 user-missing cells and 720,729 system-missing cells. `idnumber` is not globally unique (4,721 distinct) but `(country,idnumber)` is injective over all 12,217 rows. Country support is eight codes. Weight topology is eight country-specific `w_*` columns plus `w_all`. Ordered `q097_1..3` slots exist; no native MR-set declaration exists.
- **Wave 4:** 20,667 × 289; `UTF-8`; zero SPSS user-missing cells and zero system-missing cells. Non-substantive-looking states instead occur as ordinary values (for example `q1=-1` labeled `Missing`). `idnumber` is not globally unique (6,729 distinct) but `(country,idnumber)` is injective. Fourteen countries are observed, `region` has 84 observed codes, and two complete weight variables (`w`, `w_cross`) are present. Ordered First/Second/Third structures exist; no native MR-set declaration exists. `q172` is explicitly labeled ASEAN-countries-only.
- **Wave 5:** 26,951 × 308; `UTF-8`; again zero physical user/system missing cells. `IDnumber` is not globally unique (15,982 distinct); even `(COUNTRY,IDnumber)` is non-injective: Hong Kong IDs `704273201` and `704273901` each occur twice. Fifteen country codes are observed; Cambodia remains in the value-label dictionary but is unobserved; Australia (15) and India (18) appear. `Region` has 102 observed codes. One complete weight `w` is present. Three native dichotomy MR sets are declared (`IR3a`, `Q112`, `SE15`), with overlapping membership between `Q112` and `SE15`. India-only ranked `Q106c/d/e` and ASEAN-only `q186` are physically labeled module structures.

## Cross-wave burden

The family cannot be certified under one name-based or missingness-based rule. Wave 1 uses physical SPSS user/system missing states heavily; Waves 4/5 use ordinary values such as `-1` with labels such as `Missing`. File encoding changes BIG-5→UTF-8. Country/region systems expand and shift. Weight topology changes from country-specific columns + `w_all`, to `w`+`w_cross`, to `w`. Same-name variables are especially unsafe as continuity evidence: Wave 4→5 has 176 common names but 158 label changes, 146 value-label dictionary changes, 161 original-type changes, and 156 ordinal moves.

Wave 5's native MR metadata does not require a new generic hazard class: it is a concrete source-specific exercise of the already-governed `MULTIPLE_RESPONSE_TOPOLOGY` law.

## Unresolved authority

Raw bytes establish storage, incidence, labels, ordering, duplicate IDs, missing declarations, MR membership, and explicit module wording. They do **not** by themselves authorize semantic response-state mappings, native-ID identity semantics, routing/risk sets, or weight purpose/estimand. Those remain documentary authority gaps for later source packs.

## Reconnaissance disposition

All three sources: `KNOWN_HAZARD_CLASS__SOURCE_SPECIFIC_FIXTURE_REQUIRED`. No novel hazard class was found. This is not certification.

Token: `PRE553_SR09PRE_R03_ASIAN_BAROMETER_RECON_COMPLETE`
