# B04 — LMQ-004 SOURCE-NATIVE ROUTING AUTHORITY ACQUISITION — ARAB BAROMETER / AFROBAROMETER / ASIAN BAROMETER R1 — RETURN

## Identity and bounded authority

- Repository: `maidiu/rawlsing`
- Worker branch: `agent/verkhovod-b04-routing-arab-afro-asian-r1`
- Exact starting HEAD verified before execution: `6104e2b63afec98659edaa672fa8b0d8a85a5cf2`
- Governing command: `00_WORKER_COMMAND.md`, under Authority 43.
- Sibling findings consumed: **none**.
- A07-recovered historical routing wrapper SHA-256: `e27ceb340eac5d7124e44b80081e5c0309a342326c045df6d6f6d0cd71910c46`.
- A07-recovered governed 35-wave catalog bundle SHA-256: `b569c3677514e627bccb6f920c7aefd7c1d7bb452eb906ddd8913a69d27dac7d`.

The exact B04 denominator is **127 rows**: Afrobarometer 49, Arab Barometer 30, Asian Barometer 48. Every assigned row crosswalks one-to-one to the A07-recovered current node. All 127 carry historical state `FAIL_CLOSED_UNRESOLVED`; zero carry `FAIL_CLOSED_NO_SOURCE_ROW_MATCH`. Historical state is conserved separately from the new B04 disposition.

## Result

| Family | Assigned | Positive executable | Known absence / nonapplicability | Still unresolved |
|---|---:|---:|---:|---:|
| Afrobarometer | 49 | 0 | 1 | 48 |
| Arab Barometer | 30 | 4 | 5 | 21 |
| Asian Barometer | 48 | 0 | 1 | 47 |
| **TOTAL** | **127** | **4** | **7** | **116** |

## Positive executable routing authority

1. **Arab Barometer II / JO / `q408`** — source-native Q407 routing says response codes 6/7/8/9 go to Q409, leaving Q408 reachable only for Q407 values 1–5. Compiled predicate: `Q407 IN {1,2,3,4,5}`. Hostile positive `Q407=1` => true; hostile negative `Q407=6` => false; replay exact.
2. **Arab Barometer V / QA / `Q412A4`** — official programmer instruction on Q412a: `IF Q409 == 1, 2, 3, 4 OR 5`; item 4 is the assigned stored row. Predicate: `Q409 IN {1,2,3,4,5}`. Positive `Q409=1`; hostile negative `Q409=6` (`I do not use the Internet`); replay exact.
3. **Arab Barometer V / QA / `Q412A9`** — same exact Q412a source-native gate, item 9. Predicate and hostile cases identical to Q412A4; replay exact.
4. **Arab Barometer V / QA / `Q104B_OTHER`** — Q104b is printed only under `IF Q104a == 1`; response category 24 is the exact `Other (please specify)` destination row. Predicate: `Q104A == 1 AND 24 IN Q104B_SELECTIONS`. Positive `{Q104A:1,Q104B_SELECTIONS:[24]}`; hostile negative `{Q104A:1,Q104B_SELECTIONS:[2]}`; replay exact.

All four executable rows pass hostile-positive, hostile-negative, and deterministic replay tests. Machine-readable cases are in `03_B04_LMQ004_ROUTING_ARAB_AFRO_ASIAN_R1_PREDICATE_TESTS.json`.

## Governed known absence or nonapplicability

1. **Afrobarometer R1 / LS / `sapknw`** — official R1 codebook states: not asked in Botswana, Lesotho, and Namibia. Lesotho scope therefore has affirmative source-level nonapplicability.
2. **Arab Barometer II / JO / `ir52010`** — Q501 `IR10` is explicitly Iraq-only.
3. **Arab Barometer II / JO / `eg8117`** — accepted governed source authority records the exact implementation as Egypt-scoped / country-conditional; JO is therefore outside the governed source scope. This is not inferred from the `EG` prefix or question wording.
4. **Arab Barometer II / JO / `eg8033`** — accepted governed source authority records the exact implementation as Egypt-scoped / country-conditional; JO is outside the governed source scope. Again, no prefix inference is used.
5. **Arab Barometer II / JO / `t50111`** — Q501 `T11` is explicitly Tunisia-only.
6. **Arab Barometer II / JO / `t3046`** — the T304 battery is explicitly Tunisia-only; the assigned row is member 6 of that source-native battery.
7. **Asian Barometer W5 / SG / `Q106e`** — accepted source-native authority tied to the official W5 questionnaire preserves Q106e as India-only; Singapore is affirmatively outside scope.

## Deliberate nonclosures

The remaining **116 rows** stay `STILL_UNRESOLVED__SOURCE_AUTHORITY_INSUFFICIENT`. No closure was inferred from ordinary question text, observed release coverage, missing metadata, neighboring-wave behavior, or adjacency in a codebook. Examples of refused counterfeit closure include Arab II `t916` (Tunisia appears in the wording but no qualifying exact row-scope ruling was recovered), Arab I `q714` (semantic dependence does not itself prove a printed routing gate), and Asian W5 `SE9B` / `SE10_1` (W4 prints occupational skips, but cross-wave inheritance is prohibited).

## Authority-code dictionary used by the exact row ledgers

- `AFROR1_SAPKNW_LS_NOT_ASKED` — affirmative R1 Lesotho nonapplicability.
- `ARABII_IR10_IRQ_ONLY` — exact Iraq-only source ruling.
- `ARABII_EG811_EGYPT_SCOPE` — accepted governed Egypt-only scope ruling for EG811 member 7.
- `ARABII_EG803_EGYPT_SCOPE` — accepted governed Egypt-only scope ruling for EG803 member 3.
- `ARABII_T11_TUNISIA_ONLY` — exact Tunisia-only source ruling.
- `ARABII_T304_TUNISIA_ONLY` — exact Tunisia-only T304 battery ruling.
- `ASIANW5_Q106E_INDIA_ONLY` — accepted governed India-only source-native scope ruling.
- `ARABII_Q408_Q407_SKIP` — source-native Q407 skip gate compiled for q408.
- `ARABV_Q412A_Q409` — official Q409 programmer gate compiled for Q412A4/Q412A9.
- `ARABV_Q104B_OTHER` — official Q104a gate plus exact selected `Other` category membership.
- `NO_QUALIFYING_SOURCE_AUTHORITY` — no exact qualifying affirmative routing/nonapplicability authority recovered; row remains fail-closed.

## Source-byte anchors

- `merged_r1_codebook2.pdf` SHA-256 `f603d9f5f95a3898dc42661b3cf8da749f874594b8770fe5fd5fb44f696eb537`
- `merged_r5_codebook_2.pdf` SHA-256 `7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735`
- `AB_R9.MergeCodebook_25Jun24.final_.pdf` SHA-256 `1afd1a78d26b01336dff1cb7b1fa5edbeae00361d935227decb08d4ffac20281`
- `Arab Bar W1 Questionnaire_ENG.pdf` SHA-256 `0814f77bcfdad3c78d5e46f49012437f25ddcbfe8bea3e565d7a26874bab4118`
- `Arab Bar W2 Questionnaire_English.pdf` SHA-256 `7087ea18ff4ab25377adb83587217cf82f7114719334ae53308063d558a75536`
- `ABV_Questionnaire_ENG_v2.pdf` SHA-256 `cd750ce6f73dfb7750ce4d7e72a8ef220f9c6694300aea97c7f4403db404a73d`
- `ABS4_Core_Questionnaire.pdf` SHA-256 `5be5ed726287f83c6bf723ae563e434f7d17f623e630b31b6ba1b92d2cdcbba0`
- Asian Barometer W1 `CoreQs-May25rev.doc` SHA-256 `df6c6c76ce685ccea2301d476cf5ff9b325fbbbce22e6a89597de25f68dd931d`
- Asian Barometer W1 `Wave1_codebook_20170327.txt` SHA-256 `f6c9b4bddebf0b8e7f6aff1ce844b8b9b53e89725a09f04cbdb22b3f72669347`
- Asian Barometer W5 `ABS5_Core_Questionnaire_20190805.pdf` SHA-256 `1e60e96baf88f48a75c64056080b37f981ad66441fc5521bbb21d14ad9c41758`

## Validation / return to HQ

- exact assigned denominator: **127 / 127 PASS**
- A07 crosswalk uniqueness: **127 unique current nodes PASS**
- exact row identity reconciliation: **127 / 127 PASS**
- historical failure-state conservation: **PASS**
- disposition exhaustiveness: **4 + 7 + 116 = 127 PASS**
- hostile positive execution: **4 / 4 PASS**
- hostile negative execution: **4 / 4 PASS**
- deterministic replay: **4 / 4 PASS**
- sibling blindness: **maintained**

This worker return does **not** claim complete LMQ-004 routing closure. It returns an exact bounded delta: **11 assigned rows lawfully closed, 116 remain source-authority insufficient and fail-closed**.

`B04_LMQ004_ROUTING_ARAB_AFRO_ASIAN_R1_COMPLETE`
