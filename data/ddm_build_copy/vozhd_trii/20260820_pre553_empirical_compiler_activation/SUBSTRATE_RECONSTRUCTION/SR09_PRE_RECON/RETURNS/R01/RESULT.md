# SR09-PRE R01 — Afrobarometer raw-source reconnaissance

Status: **AUTHORIZED__NON_DISPOSITIVE**  
Token: `PRE553_SR09PRE_R01_AFROBAROMETER_RECON_COMPLETE`

## Transport and byte gate

The Library transport bundle `surveys.zip` was materialized to worker-private scratch and verified at **158,180,333 bytes**, SHA-256 `f68d2b33ec0eeb973699963e4c7122d624b99a541b40277e4daed8b87dc9d05f`. Only the three assigned members were extracted. All three matched the R01 frozen hashes before probing and matched again after probing. No alternate filesystem source was substituted.

## Source dispositions

All three sources: **`KNOWN_HAZARD_CLASS__SOURCE_SPECIFIC_FIXTURE_REQUIRED`**, with additional **`DOCUMENTARY_AUTHORITY_GAP`**. No new hazard class outside the frozen taxonomy was observed. No source is certified here.

### Round 1

- 21,531 cases; 144 variables; nominal/calculated case size 146; strict UTF-8 metadata decode.
- Zero SPSS user-missing declarations and zero system-missing cells in the full scan.
- Yet semantic-looking codes are ordinary values: e.g. `SUPDEM` raw `4` = label “Don't know”, `97` = “Not applicable”, `98` = “Refused to answer”, `99` = “Missing”, all physically `OBSERVED_STORAGE_VALUE`.
- `REFNUMB` is injective (21,531/21,531). `CASENUMB` is not: 19,937 distinct, 1,594 duplicate excess rows; even `COUNTRY+CASENUMB` leaves 169 duplicate excess rows.
- Five distinct weight-like fields occur (`WITHINWT`, `ACROSSWT`, `COMBINWT`, `AFRICAWT`, `AFCOMBWT`).

### Round 5

- 51,587 cases; 348 variables; nominal/calculated case size 557; strict UTF-8 metadata decode.
- 84 variables declare SPSS discrete user-missing `997`; all 84 exercise it, totaling **1,342,300 user-missing cells**. Four variables exercise **4,336 system-missing cells**.
- `RESPNO` is injective (51,587/51,587).
- Physical routing clues include `WEST.AFR`/`EAST.AFR`/`SOUTHERN`/`NORTH.AF` FILTER indicators and `R1.ONLY`..`R4.ONLY`. These are not treated as authoritative questionnaire logic.
- Ordinary codes labeled “Missing”/“Don't know” coexist with format-declared missingness; e.g. `Q71A=-1` is ordinary despite label “Missing”.
- `WITHINWT` and `COMBINWT` remain physically distinct weight-like variables.

### Round 9

- 53,444 cases; 427 variables; nominal/calculated case size 915; strict UTF-8 metadata decode.
- 32 variables exercise **583,491 system-missing cells**. Only `Q78F` declares user-missing `-1`, and that declaration is **not exercised**: zero user-missing cells.
- `RESPNO` is injective (53,444/53,444).
- `Q47C=94`, labeled “Not asked in the country”, is an ordinary observed storage value, not format missingness.
- Eleven ordered language slots `Q118_1`..`Q118_11` are physically separate. Code `9996` (“No further response”) is ordinary; slots 5–11 additionally exercise system missing. Slot order/cardinality must survive replay.
- Four weight-like fields encode parallel old/new families: old EA-level `WITHINWT`/`COMBINWT` and new HH-level `V397_A`/`V399_A`. Their raw row-0 values differ.

## Cross-wave drift

R1 shares only four exact variable names with R5 and R9 (`COUNTRY`, `URBRUR`, `WITHINWT`, `COMBINWT`). R5 and R9 share 142 exact names, but among those, 111 labels, 120 value-label dictionaries, 28 missing declarations, and 6 physical types differ. Exact-name reuse can be actively misleading: R5 `Q99` is a numeric vote-party item with a declared missing code; R9 `Q99` is a 255-byte respondent-message string. `Q100`, `Q101`, and `Q102` likewise move across sponsor/gender/race/interview-language items.

This is a certification burden, not semantic authority: source snapshot/version must dominate bare variable-name continuity.

## Documentary authority gaps

Raw SAV bytes establish physical layout, values, labels, declarations, and measured incidence. They do **not** establish: canonical respondent identity/scope; lawful country/region cross-round mappings; analytical weight/design roles or old/new weight selection; questionnaire routing/form/module semantics; or cross-wave conceptual equivalence. Repository code searches for `Afrobarometer` and `Afro Barometer` returned no matching checked-in source documentation, so those questions remain deferred to governed documentary authority.

## Full-scan declaration

A full sequential data-stream scan occurred for **all three sources**. This was necessary because compressed SAV storage is sequential and the mission required exact exercised missingness, measured ID uniqueness, routing/topology evidence, and replayable row/variable sentinels. No full scan was used to infer semantics.

## Generic SAV contract assessment

No novel physical behavior outside the frozen generic SAV decoder contract was observed. The burden is source-specific fixture construction and later authority, not a new decoder class.

`PRE553_SR09PRE_R01_AFROBAROMETER_RECON_COMPLETE`
