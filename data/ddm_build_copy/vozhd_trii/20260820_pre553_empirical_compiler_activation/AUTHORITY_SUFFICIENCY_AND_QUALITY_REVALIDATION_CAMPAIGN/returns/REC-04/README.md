# REC-04 — QRA700 / O07 Response-Geometry Census

Status: `COMPLETED__BOUNDED_QRA700_CENSUS_RETURN`

Exact starting HEAD: `e410799cc7afa95e758ebe774f141e053e2bb711`

Worker: `agent/vozhd-trii-rec04-qra700-o07-geometry`

TIR: `TIR-012`, `TIR-013`, `TIR-021`.

## Governing boundary

REC-04 is a bounded court over exactly the 700 rows of `question_relation_registry_35wave_active_v1.csv`. It does not create a universal QRA. QRA absence outside these 700 rows is not evidence of missing directionality. P2/current response authority outside QRA remains separately governed.

No QRA, O07, response authority, P2 authority, compiler, or runtime artifact is mutated. Semantic direction is never inferred from numeric code order. DK/refusal/no-answer/IAP/not-asked/missing/source-special states never become substantive anchors. Topology alone never creates polarity.

## Exact census result

- `PASS__BOUNDED_QRA_ASSERTION_UPHELD`: **680**
- `SUCCESSOR_CANDIDATE__QRA_ASSERTION_DEFECTIVE`: **4**
- `CONFLICT__O07_RECONCILIATION_REQUIRED`: **10**
- `SOURCE_LIMITED__FAIL_CLOSED`: **6**
- total: **700**

Current QRA defects: exactly **4** — Latinobarómetro 1995 `p26`; LiTS III `q814d`; Arab Barometer II `q5182`; Arab Barometer II `eg8117`.

Exact current O07 corrections implicated: **11**. Ten are source-supported QRA assertions with conflicting retrieved O07 classes; LiTS III `q814d` is the eleventh and requires both QRA-anchor and O07-class successor reconciliation. Exact O07 correction membership is owned only by `QRA_O07_11_ROW_RECONCILIATION.csv`.

All 30 previously reviewed O07 explicit unresolved states remain unresolved. Exactly three intersect QRA700: Latinobarómetro 2024 `S20A`, `Q7NOIJ`, `Q8NOIJ`. REC-04 also preserves source-limited QRA rows Latinobarómetro 1995 `p53`, `p63`, and Latinobarómetro 2011 `S1NICC7`, giving exactly six fail-closed QRA rows.

Latinobarómetro 2024 `Q49STA`, `Q49STB`, `Q49STC` are one source-native response-geometry cluster. Only `Q49STA` lies inside QRA700; its QRA assertion is upheld and its retrieved O07 `NOMINAL` class is a correction candidate. No O07 correction is counted for `Q49STB/C` because their current row classes were not recovered in this court.

## `QRA700_FULL_SOURCE_CENSUS.csv` encoding

The census is an exact-order compact carrier. After header `s`, data row position `0..699` is the exact zero-based row ordinal of the governing QRA700 carrier. Each one-character state code expands through the legend below.

Tuple fields:

`source_evidence | source_topology | lawful_directionality | anchor/polarity_state | special_presence | o07_agreement | rec04_classification`

Meaning:
- source evidence: `B` = exact source/response authority bound; `L` = source-limited.
- lawful directionality: `Y` yes; `N` no; `U` unresolved/fail closed.
- anchor/polarity: `Q` current QRA geometry upheld; `C` current QRA assertion defective with exact successor candidate in the successor ledger/subcourt; `-` no signed anchor required; `L` source-limited.
- special presence: `P` source-native non-substantive special state present; `N` none detected in the bound option set.
- O07 agreement: `A` retrieved current O07 class agrees; `C` bounded compatibility/retrieval conflict signal; `U` exact current O07 class not independently retrieved. **This is not the O07 correction denominator.** Only the 11-row reconciliation ledger establishes exact current O07 corrections.
- REC-04 class: `P` upheld; `S` QRA successor candidate; `C` O07 reconciliation required; `L` fail closed.

State-code legend:

```text
0|B|administrative|N|-|N|C|P
1|B|administrative|N|-|P|C|P
2|B|binary_context|N|-|P|C|P
3|B|binary_contrast|N|-|N|C|P
4|B|binary_contrast|N|-|P|C|P
5|B|binary_contrast|Y|Q|N|A|P
6|B|binary_contrast|Y|Q|N|C|C
7|B|binary_contrast|Y|Q|P|A|P
8|B|binary_factual|N|-|N|C|P
9|B|binary_factual|N|-|P|C|P
A|B|binary_factual|Y|C|N|U|S
B|B|binary_tradeoff|N|-|P|C|P
C|B|context_index|N|-|N|C|P
D|B|context_index|N|-|P|C|P
E|B|continuous_context|N|-|N|C|P
F|B|continuous_context|N|-|P|C|P
G|B|continuous_numeric|N|-|N|C|P
H|B|continuous_numeric|N|-|P|C|P
I|B|derived_tradeoff_scale|N|-|N|C|P
J|B|forced_contrast|N|-|P|C|P
K|B|interview_context|N|-|P|C|P
L|B|mixed_scalar|N|-|P|C|P
M|B|multiselect|N|-|N|C|P
N|B|multiselect|N|-|P|C|P
O|B|multiselect_child|N|-|P|C|P
P|B|multiselect_indicator|N|-|N|C|P
Q|B|nominal_choice|N|-|N|C|P
R|B|nominal_choice|N|-|P|C|P
S|B|nominal_choice|Y|C|N|U|S
T|B|nominal_context|N|-|P|C|P
U|B|open_text|N|-|N|C|P
V|B|ordinal_context|N|-|N|C|P
W|B|ordinal_context|N|-|P|C|P
X|B|ranked_choice|N|-|P|C|P
Y|B|ranking_or_multiselect|N|-|P|C|P
Z|B|scalar|N|-|P|C|P
a|B|scalar|Y|C|N|A|S
b|B|scalar|Y|C|N|C|S
c|B|scalar|Y|Q|N|A|P
d|B|scalar|Y|Q|N|C|C
e|B|scalar|Y|Q|P|A|P
f|B|scalar_coordinate|N|-|N|C|P
g|B|scalar_coordinate|N|-|P|C|P
h|L|binary_contrast|U|L|N|C|L
i|L|open_or_continuous|U|L|N|U|L
j|L|scalar|U|L|N|C|L
```

## Return state

`REC04_CURRENT_QRA_DEFECT_COUNT = 4`

`REC04_EXACT_O07_CORRECTIONS_IMPLICATED = 11`

`REC04_SOURCE_LIMITED_QRA_ROWS = 6`

`REC04_QRA_OR_O07_MUTATION = NONE`

`REC04_UNIVERSAL_QRA_CREATED = NO`
