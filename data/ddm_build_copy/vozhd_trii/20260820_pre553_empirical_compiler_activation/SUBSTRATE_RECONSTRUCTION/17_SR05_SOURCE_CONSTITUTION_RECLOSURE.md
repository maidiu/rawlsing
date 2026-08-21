# PRE553 SUBSTRATE RECONSTRUCTION — SR05 SOURCE CONSTITUTION RECLOSURE

Status: `ACCEPTED__FORMAT_NEUTRAL_SOURCE_CONSTITUTION_RECLOSED`

Inputs:

- accepted C11 M01-M18 architecture;
- `09_SOURCE_NATIVE_CONSTITUTION.md`;
- `10_FORMAT_DECODER_CONTRACT.md`;
- `12_WVS_LITS_HOSTILE_FIXTURE_ORACLE.md`;
- accepted SR03 R3 35-source physical census (`16_SR03_R3_ADJUDICATION.md`).

## 1. Holding

The full CLOSED_35 physical census does **not** require reopening C11, I02/I03/I05/I04, or V553-V558 semantics.

The frozen format-neutral boundary is sufficient:

`exact source bytes -> physical decoder -> format-neutral raw incidence -> source authority pack -> governed C11 state`

## 2. Physical classes exercised by the full corpus

SR03 confirms the constitution covers all observed physical classes relevant to this campaign:

- ordinary numeric/string values;
- SAV system missing;
- SAV user-missing discrete/range declarations;
- DTA system missing;
- DTA extended-missing capability (none observed in CLOSED_35, but retained in contract);
- variable labels;
- value-label dictionaries;
- source file encoding metadata;
- explicit reader compatibility configuration;
- variable storage/display/measure metadata;
- native respondent identifiers where present;
- multiple-response-set metadata (18 sets observed across three sources);
- source snapshot and row ordinal replay identity;
- source-specific weights/design variables without premature primary-weight semantics.

No observed source requires destructive normalization or a semantic shortcut at decoder layer.

## 3. Meaning boundary remains binding

The census reinforces rather than weakens the separation between physical fact and governed meaning.

Examples:

- SPSS user-missing is a physical declaration, not one universal semantic absence state;
- LiTS ordinary `6/7/98/99`-style values can carry DK/refusal/not-applicable labels without being Stata missing;
- a reader compatibility encoding is not automatically authoritative source text encoding;
- a native respondent ID is not automatically hard C11 replay identity;
- a source-declared weight variable is not automatically the lawful estimand/primary weight.

All semantic interpretation remains source-authority-pack work.

## 4. Required implementation consequence

The future physical carrier and decoder implementation must preserve the complete source-physical information frontier exposed by SR03. It may not optimize away:

- user-missing codes/ranges;
- system-missing class;
- raw codes;
- label dictionaries;
- row ordinal;
- multiple-response/topology metadata;
- source encoding/config provenance;
- competing weight/design variables.

## 5. Scheduled, non-loose remaining work

The following are explicitly assigned to later gates and are not unresolved SR05 design questions:

- per-source semantic authority and text-encoding authority where compatibility decoding was required -> G-SR07/G-SR08/G-SR09 source certification;
- exact source-vs-legacy loss quantification for the remaining sources -> G-SR09;
- physical carrier product/layout -> G-SR04;
- decoder/C11 runtime implementation -> G-SR06.

## 6. Closure

G-SR05 is closed.

Token:

`PRE553_SR05_ACCEPTED__FORMAT_NEUTRAL_SOURCE_CONSTITUTION_RECLOSED`
