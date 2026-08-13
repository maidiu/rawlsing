# Phase-D successor response-semantics projection — provenance R1

## Status

`FROZEN_SOURCE_PROJECTION__NO_RESPONDENT_OUTCOMES_USED`

This artifact repairs the `V550_RESPONSE_SEMANTICS_EMPTY` input gap exposed by the first successor archetype-conformance run. It does **not** change the frozen candidate ladder, Job3 semantic posture, routing truth, M6 ancestry, or Phase-D validator semantics.

## Transport clarification

The encoded `.b64` wrapper is a transport representation. The materialized CSV is the governing frozen payload. See `../execution/PREFLIGHT_TRANSPORT_NOTE_R2.md` for the active retry clarification. The existing materialized CSV SHA-256 remains the authoritative byte-level integrity pin.

## Backward authority check

The cumulative R5 architecture already requires a canonical V550 response-option map before determinicity and defines one row per source/wave/variable/value option. It explicitly forbids trusting numeric response values without response-option provenance and gives `pdf_response_text` as a lawful option source. No prior governed response-option mapping for these exact twelve frozen anti-erase variables was found in the R5 or R10H packaged ancestry inspected for this repair.

## Governing source-native authority

Archive:

`Rawlsing_SourceNative_Questionnaire_Structure_Authority_R1_20260812.zip`

SHA-256:

`e88cc035ca1d846e68ee208ec991f61f636d67ebbd19312057c8e44c37ff740d`

Authority law preserved from that pack:

`NATIVE_PDF_OR_OFFICIAL_CODEBOOK_TEXT_GOVERNS_STRUCTURE; R10_FIELDS_SUPPLY_IDENTITY_AND_DIAGNOSTIC_CROSSWALK_ONLY`

### LiTS II

Primary native questionnaire:
- document id: `DOC-a797ba54bf0273b6`
- file: `LiTSII_Questionnaire.pdf`
- page 7: `q305_1`, `q305_2` spending-priority response codes 1–8 and DK 97
- page 8: `q306a`–`q306d` YES=1, NO=2, DK=97; `q311` response codes 1–3 and DK 97
- page 9: `q312a` agreement scale 1–5, Refused=6, DK=7

### Asian Barometer W4

Primary native questionnaire:
- document id: `DOC-58185f41e3ecefc0`
- file: `ABS4_Core_Questionnaire_Final_20140529.pdf`
- page 15: `q104`, `q108`; common agreement scale 1 Strongly agree, 2 Somewhat agree, 3 Somewhat disagree, 4 Strongly disagree, 7 Do not understand the question, 8 Can't choose, 9 Decline to answer
- page 20: `q143`, `q145`; same common agreement scale

The supporting W4 questionnaire variant carries the same relevant scales; R1 projects from the primary document only.

## Projection

`ANTI_ERASE_RESPONSE_OPTION_AUTHORITY_R1.csv.gz.b64` materializes deterministically to `ANTI_ERASE_RESPONSE_OPTION_AUTHORITY_R1.csv`.

- 69 option rows
- 12 exact frozen variables
- no respondent-level values
- no observed co-travel or candidate outcomes used
- exact source wording preserved in `value_label_raw`
- mapping status: `SOURCE_NATIVE_RESPONSE_OPTION_AUTHORITY_R1`
- source column: `pdf_response_text`
- normalization basis: `PRIMARY_NATIVE_QUESTIONNAIRE_EXACT_TEXT_TRANSCRIPTION`
- normalization confidence: `low`

The `low` confidence value is intentional: R5's frozen V550 confidence law assigns PDF response text to the low tier even where transcription is exact. This repair does not silently upgrade that rule.

Materialized CSV SHA-256:

`d9bcc4e9cf80c6e70fdf38d7fd260c5b60f4f8a4696fbea0c8e6d4fbff5ee1f7`

## Scope lock

The projection may be used only to supply answer semantics for the already-frozen Phase-D anti-erase ladder. It may not:
- create or promote a typed semantic relation;
- reorder or expand the ladder;
- infer labels from raw respondent values;
- alter canonical V550 response maps in place;
- activate V552 or later stages.
