# CLOSED35-L2R-AFR9 — Exact Four-Binding Adjudication

## Scope lock

This adjudication does not revisit any binding closed by `CLOSED35-L2-AFR9`.

Only the four commissioned residuals are adjudicated.

## Decision matrix

| Binding | Decision | Exact result |
|---|---|---|
| `Q78F_EXACT_MERGED_COUNTRY_APPLICABILITY_SET` | **CLOSED** | 25 applicable / 14 Not Asked in Country |
| `Q118_11_EXACT_ROUND9_PRODUCER_BINDING` | **RESIDUAL** | canonical physical field; no exact R9 producer definition recovered |
| `V397_A_EXACT_ROUND9_ALIAS_BINDING` | **RESIDUAL** | role-compatible with producer `withinwt_hh`; exact producer alias not recovered |
| `V399_A_EXACT_ROUND9_ALIAS_AND_ROLE_BINDING` | **RESIDUAL** | physical new-HH combined-like carrier; exact producer alias and role not recovered |

## A. Q78F exact country binding

### Producer routing law

The Round-9 network process permits country instruments to block out master-question items that are inappropriate while retaining numbering. Q78F is therefore source-country-applicability data, not a universally routed R9 core question.

### Exact 39-country partition

Applicable / fielded (25):

- Botswana
- Burkina Faso
- Cabo Verde
- Cameroon
- Congo-Brazzaville
- Eswatini
- Ethiopia
- The Gambia
- Ghana
- Guinea
- Liberia
- Madagascar
- Mali
- Mauritania
- Morocco
- Mozambique
- Niger
- Senegal
- Seychelles
- Sierra Leone
- South Africa
- Sudan
- São Tomé and Príncipe
- Tanzania
- Zambia

Not asked in country (14):

- Angola
- Benin
- Côte d'Ivoire
- Gabon
- Kenya
- Lesotho
- Malawi
- Mauritius
- Namibia
- Nigeria
- Togo
- Tunisia
- Uganda
- Zimbabwe

The partition exhausts the official 39-country merged denominator:

`25 + 14 = 39`.

### Binding rule

A source-specific realization may set a country-level Q78F applicability predicate from this exact set.

It must not:

- derive applicability from Q78F missingness;
- derive applicability from Q78A-E adjacency;
- treat `-1` declaration incidence as country routing evidence;
- generalize this set to other Afrobarometer rounds.

The prior semantics `Q78F = EU influence` and `-1 = Missing` remain settled.

## B. Q118_11 exact producer binding

The strongest producer documentary boundary is negative but exact:

- final merged codebook: Q118_1 ... Q118_10, then Q118OTHER;
- archived country dictionaries: country-specific maxima up to ten, then Q118OTHER;
- no recovered producer R9 surface names Q118_11.

The canonical source's physical Q118_11 therefore cannot be deleted, but its existence is not producer questionnaire authority.

Classification:

`UNDOCUMENTED_CANONICAL_MERGED_FIELD`

Do **not** sharpen this to one of:

- producer-authorized questionnaire slot;
- administrative extension;
- harmonized extension;
- data-manager extension;

unless an exact R9 producer processing/release document is recovered.

Permitted realization:

`preserve Q118_11 identity/order/raw state -> semantic role UNKNOWN`

Forbidden:

`Q118_11 = eleventh language response` merely because downstream schemas or the physical label say so.

## C. V397_A exact alias

Producer vocabulary:

`withinwt_ea`
`withinwt_hh`

Canonical physical vocabulary:

`WITHINWT`
`V397_A`

The correspondence is highly constrained by order and label, but the court was expressly forbidden to infer naming conventions. No exact producer source recovered the literal token `V397_A` or an alias crosswalk.

Decision:

`V397_A_EXACT_ROUND9_ALIAS_BINDING = UNKNOWN`

Corroborated role hypothesis, **not admission**:

`V397_A ~= withinwt_hh`

No source-specific realization may turn `~=` into `=`.

## D. V399_A exact alias and role

Producer authority already closes the generic combined-weight analytical role inherited from the predecessor packet.

But the recovered exact R9 producer merged codebook does not map a canonical short carrier to the new HH-level combined weight. The literal `V399_A` is absent from recovered producer documentation.

Decision:

`V399_A_EXACT_ROUND9_ALIAS_AND_ROLE_BINDING = UNKNOWN`

Corroborated family-shape hypothesis, **not admission**:

`V399_A ~= new-HH combined-weight carrier`

No realization may name it `combinwt_hh` / `combinwt_new_hh` without exact producer binding.

## E. Why `_A` does not close either alias

IBM documents multiple mechanisms that can append letter suffixes to resolve name collisions or duplicate names. Therefore:

`_A != producer semantic ontology`

It cannot establish:

- alternate wording;
- harmonized alias;
- routing variant;
- country module;
- old/new weight status;
- merge-generated variable class.

Only a producer or authoritative release-processing crosswalk can do so.

## F. Residual exact unknown set

Exactly three residuals remain:

1. `Q118_11_EXACT_ROUND9_PRODUCER_BINDING`
2. `V397_A_EXACT_ROUND9_ALIAS_BINDING`
3. `V399_A_EXACT_ROUND9_ALIAS_AND_ROLE_BINDING`

No other AFR9 documentary holding is reopened or downgraded.

## G. Court disposition

Because the commissioned set is not fully closed, PASS is not issued.

Terminal:

`CLOSED35_L2R_AFROBAROMETER_R9_RESIDUAL_AUTHORITY_FROZEN__EXACT_UNKNOWN_SET_RETURNED`
