# SOURCE CERT PREP71 R07 — FUTURE EXECUTION ORDER

Status: `PREPARED__NON_DISPOSITIVE__DO_NOT_EXECUTE_NOW`

This file is an execution order for later HQ courts. This R07 preparation return does **not** run G-SR08, does **not** certify any LiTS source, and does **not** touch WVS70.

## Governing common chain

For every source, execute in this exact order:

1. **source SHA** — materialize the frozen Library transport, verify ZIP byte size/SHA-256, extract only the named source member, and verify the exact source-member SHA-256 and byte size.
2. **decoder/config** — use exactly `decode_dta(source_path, encoding="latin1")` with status `COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`. The `latin1` argument is a deterministic compatibility execution choice only.
3. **hostile physical fixtures** — replay all source rows in `HOSTILE_FIXTURES.csv` that assert cell state/raw value/row identity.
4. **metadata/topology fixtures** — replay source encoding/reader config, weight surfaces, repeated/ranked topology, routing/module topology and country/ID metadata.
5. **documentary semantic assertions** — apply only claims explicitly present in `DOCUMENTARY_AUTHORITY_MAP.csv`; unresolved claims in `AUTHORITY_GAPS.csv` remain unresolved.
6. **exact carrier/C11 equivalence assertions** — only after steps 1–5 pass, compare the future carrier against exact source-native physical information required by the governing source constitution.
7. **negative/fail-closed fixtures** — reject silent source substitution, missing-state collapse, ordinary semantic-code coercion, label-driven semantic invention, default-weight invention, row-ID collapse, topology flattening, encoding escalation, or reader fallback.
8. **future disposition gate** — issue only the disposition authorized by the later court. This preparation packet itself cannot certify or fail a source.

## LiTS I — designated future DTA proving source

Source: `LiTS_I.dta`
SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
Transport: `LiTS_I.dta.zip`
Decoder: `decode_dta(source_path, encoding="latin1")`

When HQ launches the future DTA proving court, use LiTS I as the designated proving source. **Do not launch G-SR08 from this preparation return.**

Mandatory LiTS-I proof terrain:

- conserve 29,002 rows × 1,198 variables;
- preserve Stata system missing independently from ordinary values;
- assert zero observed extended `.a`–`.z` missings;
- preserve ordinary `q201=98` / `q301_1=6`-class semantic-looking codes as ordinary physical values;
- preserve `q105_12` even though all 29,002 rows are system missing;
- preserve first/second priority topology;
- preserve `weight_0`, `weight_1`, `weight_2` as separate candidates;
- assert accepted SR03 weight incidence exactly: **29,000 ordinary + 2 Stata system-missing cells in each of the three weight columns**;
- do not choose a default weight;
- do not promote `latin1` compatibility to intended source-text encoding.

Packet gate: `PACKET_READY__SOURCE_SPECIFIC_HOSTILE_COURT_REQUIRED`.

## LiTS II

Source: `LiTS_II.dta`
SHA-256: `c43d0e1821c51398817d7dfdfad2c0a4a5bb0d492f6a58096670e623bb6130e9`
Transport member: `surveys/LiTS_II.dta`

Mandatory terrain:

- conserve 38,864 × 627;
- replay the 3,118 system-missing cells as the accepted localized `age5564` / `age65` burden;
- preserve `-99/-98/-97`-class ordinary source values;
- preserve `SerialID`, country carriers, PSU/HH/select fields independently;
- keep `weight` and `XCweight` distinct;
- source documentation may establish democratic-vs-federal weighting distinction, but no universal default may be invented;
- preserve ranked first/second priority slots.

Packet gate: `PACKET_READY__SOURCE_SPECIFIC_HOSTILE_COURT_REQUIRED`.

## LiTS III

Source: `LiTS_III.dta`
SHA-256: `368ae5d07a44975a2f0a9ce3b1e564988a966b2632e28075c56a24d60065bcc8`
Transport member: `surveys/LiTS_III.dta`

Mandatory compound terrain:

- conserve 51,206 × 1,290 and zero extended missings;
- `ID` may be replayed as an injective source attribute, but source row ordinal remains universal replay identity;
- **never** promote `hhid` to replay identity: it is system-missing on 28,625 rows and noninjective at country+hhid scope among present rows;
- preserve **308 `PR*` + 308 `SR*` variables** as distinct respondent/module namespaces;
- use the source questionnaire + codebook only for explicit primary/secondary-role mappings; do not infer unmapped applicability from missingness;
- replay a variable such as `q112_1` where ordinary refusal code and physical system missing coexist;
- preserve `weight_population`, `weight_sample`, `weight_one` independently; no default.

Packet gate: `PACKET_READY__COMPOUND_HOSTILE_COURT_REQUIRED`.

## LiTS IV

Source: `LiTS_IV.dta`
SHA-256: `14e1032755c4f42d8d3dc61647097ccd7605ba281551e53953c76d22a223cd1c`
Transport member: `surveys/LiTS_IV.dta`

Mandatory compound terrain:

- conserve 37,478 × 1,319 and zero extended missings;
- execute the governed `decode_dta(source_path, encoding="latin1")` path;
- retain the accepted negative regression that pandas 2.2.3 with `convert_missing=True, convert_dates=True` fails in Stata elapsed-date conversion, while the accepted raw-state pandas probe with `convert_dates=False` succeeds; **do not substitute either pandas route for the governed decoder**;
- retain source-text authority as unresolved despite successful compatibility execution or independent UTF-8 metadata reporting;
- preserve **134 `*_skip` variables** and **10 visit blocks** as routing/topology carriers; use questionnaire `ASK IF` rules only where explicitly mapped;
- preserve `weight`, `weight_pop`, `weight_trt`, `weight_pop_trt` independently and replay complementary base/top-up missingness;
- official technical documentation may support general design/post-stratification/population weighting; it does not authorize the unproven `TR` token binding or a universal default;
- preserve IV country coding source-scoped (questionnaire explicitly gives code 1 = Albania).

Packet gate: `PACKET_READY__COMPOUND_HOSTILE_COURT_REQUIRED`.

## Stop conditions

Stop and return to HQ without certification if any of these occurs:

- ZIP or member SHA/size mismatch;
- governed decoder/config cannot be reproduced;
- any hostile physical fixture fails;
- a source row is dropped or deduplicated on native ID;
- ordinary semantic-looking DTA codes are converted to missing;
- PR/SR or skip/visit topology is flattened;
- any weight candidate is silently selected/dropped;
- `latin1` compatibility is represented as source-text authority;
- LiTS-IV reader fallback occurs silently;
- a semantic assertion is needed that remains listed as unresolved in `AUTHORITY_GAPS.csv`.
