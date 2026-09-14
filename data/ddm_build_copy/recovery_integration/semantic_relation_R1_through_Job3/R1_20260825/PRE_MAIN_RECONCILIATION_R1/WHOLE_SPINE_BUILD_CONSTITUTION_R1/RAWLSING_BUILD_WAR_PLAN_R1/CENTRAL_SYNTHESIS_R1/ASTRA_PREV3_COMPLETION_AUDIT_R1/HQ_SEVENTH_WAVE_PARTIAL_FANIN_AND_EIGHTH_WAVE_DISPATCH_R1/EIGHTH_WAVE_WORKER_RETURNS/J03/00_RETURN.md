# J03 — LiTS-I q301 source-local state semantic authority — governed return

Status: **PASS**

Terminal:

`J03_PASS__Q301_SOURCE_LOCAL_STATES_1_7_AND_SYSTEM_MISSING_RESOLVED__6_NOT_APPLICABLE__7_DONT_KNOW`

Exact grain:

`LITS_I_Q301_SOURCE_LOCAL_STATE_SEMANTIC_AUTHORITY_R1_ONLY`

Branch:

`agent/rabochii-prev3-w8-j03-lits-q301-source-state-semantics-r1`

Commission tip:

`1f12e8ef941e6054176c56925eb66e7ee027b0cf`

Commission blob:

`0933637ec7870588692af340a8fcca3cb475bef2`

## 1. Exact source identities

Exact LiTS-I carrier inspected:

- `LITS-2006-data.dta`
- bytes: `139531180`
- SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- rows: `29002`

Official source questionnaire:

- `LiTSI_Questionnaire.pdf`
- bytes: `240732`
- SHA-256: `b94bdcf4a9f2e2e025bf35e5364f79acf0b1f5fa05c035064e674fa58a921eae`
- authority locator: page 10, `Q.3.01`, Show Card 8

Source codebook identity recorded:

- `LITS I codebook.csv`
- bytes: `208277`
- SHA-256: `91698cbc22d7498c3587bcacd7f96be47323d2bc9867cec5103e954e5099eb0c`

Direct semantic adjudication in this worker is grounded in the official respondent-facing Q3.01 questionnaire plus the released DTA's own variable/value-label metadata and physical observations. No downstream target/product semantics were used to infer source meanings.

## 2. Q3.01 family authority

The official questionnaire declares one explicit shared Q3.01 scale before listing all eleven Q301 statements:

- `1 = Strongly disagree`
- `2 = Disagree`
- `3 = Neither disagree nor agree`
- `4 = Agree`
- `5 = Strongly agree`
- `6 = Not applicable`
- `7 = Don't know`

Both commissioned variables occur under this same declared scale:

- q301_2: `The political situation in this country is better today than around 1989`
- q301_7: `All things considered, I am satisfied with my life now`

Therefore the source-state semantic authority is family-wide for Q3.01. q301_2 and q301_7 do not differ in code meaning at this layer.

## 3. Exact source-local semantic ledger

| Native state | Governed source-local semantic state | Class |
|---|---|---|
| `1` | `SUBSTANTIVE_SCALE_POINT__STRONGLY_DISAGREE` | source-native substantive |
| `2` | `SUBSTANTIVE_SCALE_POINT__DISAGREE` | source-native substantive |
| `3` | `SUBSTANTIVE_SCALE_POINT__NEITHER_DISAGREE_NOR_AGREE` | source-native substantive |
| `4` | `SUBSTANTIVE_SCALE_POINT__AGREE` | source-native substantive |
| `5` | `SUBSTANTIVE_SCALE_POINT__STRONGLY_AGREE` | source-native substantive |
| `6` | `SOURCE_SPECIAL__NOT_APPLICABLE` | typed inapplicable special state |
| `7` | `SOURCE_SPECIAL__DONT_KNOW` | typed nonresponse special state |
| physical/system missing | `PHYSICAL_SYSTEM_MISSING__REASON_UNSPECIFIED` | physical null; no reason inferred |

Critical ruling:

`6 = NOT_APPLICABLE`

`7 = DONT_KNOW`

These are source-native meanings, not downstream target dispositions.

## 4. Physical carrier observations

q301_2 observed counts:

- `1`: 4377
- `2`: 6440
- `3`: 5226
- `4`: 6972
- `5`: 1882
- `6`: 1774
- `7`: 2327
- system missing: 4
- total: 29002

q301_7 observed counts:

- `1`: 2889
- `2`: 6112
- `3`: 6511
- `4`: 10334
- `5`: 2479
- `6`: 224
- `7`: 442
- system missing: 11
- total: 29002

All observed native states needed by the commissioned workload are accounted for. No additional numeric native state is present in either variable.

## 5. Documentation / physical metadata comparison

There is no code-assignment conflict between the official questionnaire and the released DTA metadata for codes 1–7.

One exact wording variant is preserved rather than silently normalized:

- official questionnaire code 3: `Neither disagree nor agree`
- released DTA metadata code 3: `neither disagree not agree`

Disposition:

`TEXT_VARIANT_RECORDED__NO_CODE_ASSIGNMENT_CONFLICT`

The official respondent-facing questionnaire wording governs the source-document statement; the physical DTA metadata string remains preserved as observed evidence. This wording variance has no bearing on codes 6 or 7.

## 6. Content-addressed artifacts

Semantic ledger:

- `01_SOURCE_LOCAL_STATE_SEMANTIC_LEDGER.json`
- canonical ledger material SHA-256: `37fa3395b61902b7049d4c26f09e62af314cea7a30783d21ab87e4512f46febb`

Evidence receipt:

- `02_SOURCE_EVIDENCE_RECEIPT.json`
- canonical evidence material SHA-256: `b0ec1beb09d114f926ef610198771a4caebd8b345db2efc5cb9b13626a644c9d`

## 7. Authority ceiling preserved

J03 does **not** decide whether codes 6, 7, or system missing are:

- inside a product target domain;
- resolved non-target states;
- excludable from a query denominator;
- grounds for denominator mutation;
- sufficient to restore learned-world positive execution.

No q301 recoding occurred. No denominator mutation occurred. No target-domain widening occurred. No learned-product execution or structural admission occurred. No V3/person/OBL063 semantics were introduced.

No production code changed and no pytest run is claimed.

## 8. Successor gate

Return to HQ for reconciliation with J02's generic source-state -> product-target-disposition contract.

J02 may consume only the source-local semantic facts established here:

- q301 codes 1..5 are substantive agree/disagree scale points;
- q301 code 6 is source-native `Not applicable`;
- q301 code 7 is source-native `Don't know`;
- physical/system missing is a separate null state with reason unspecified;
- q301_2 and q301_7 share the same Q3.01 code semantics.

HQ/J02 must separately decide the product-target and denominator consequences. J03 supplies no authority for those consequences.

Terminal:

`J03_PASS__Q301_SOURCE_LOCAL_STATES_1_7_AND_SYSTEM_MISSING_RESOLVED__6_NOT_APPLICABLE__7_DONT_KNOW`
