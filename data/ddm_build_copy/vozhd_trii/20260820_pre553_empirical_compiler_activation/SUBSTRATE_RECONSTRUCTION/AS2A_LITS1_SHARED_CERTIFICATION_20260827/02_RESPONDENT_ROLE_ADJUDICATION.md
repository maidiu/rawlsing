# AS2A LiTS-I respondent-role adjudication

Status: `PART_A_PASS__LOSSLESS_BOUNDED_BRIDGE_CLOSED`

Source: `LiTS_I.dta` `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`.

## Binding role law

The source-native questionnaire states that Sections 1-2 are answered by the head of household or another knowledgeable household member, while Sections 3-7 are answered by the person selected at the bottom of Section 1 with no substitutions. It separately records last-birthday/Kish-grid and current head/knowledgeable-member IDs.

Therefore `ONE_PHYSICAL_ROW != ONE_SEMANTIC_RESPONDENT_FOR_EVERY_SLOT`.

### Bounded proving release row identity

Each source row receives exactly one internal C11 `RespondentIdentity` for the selected Sections-3-7 respondent, keyed only by exact source SHA + 1-based physical row ordinal + semantic role token. Native `id`, Table-2/Table-3 IDs, `serial`, and other native identifiers remain attributes/provenance and do not replace replay identity.

### Sections 1-2

All household-roster and housing/expense slots are source-preserved but nonparticipating in the first bounded C11 proving release. This avoids attributing reporter/household/member material to the selected person. Household member slots 1-12 remain explicitly ordered topology in the 1,198-slot ledger.

### Sections 3-7

The respondent role is positively `SELECTED_RESPONDENT__NO_SUBSTITUTION`. To avoid semantic invention, the first minimal proving release positively projects only `q301_2` and `q301_7`, the two unconditional Section-3 items whose exact LiTS-2006 response contracts are present in the accepted active response-semantic binding. Other selected-respondent slots remain nonparticipating until exact response/routing authority is needed.

### Coordinates and weights

`country`, `city`, `region`, `tablec`, and `tabled` are raw source-context coordinate candidates only; no cross-release harmonization is claimed. `weight_0`, `weight_1`, and `weight_2` remain distinct source-preserved candidates. The proving release is RAW/unweighted and emits no `WeightMeasureFact`.

### Part-A closure

- `UNACCOUNTED_LITS1_SOURCE_SLOT = 0`
- `UNRESOLVED_RESPONDENT_ROLE_REQUIRED_FOR_PROVING_SCOPE = 0`
- `UNRESOLVED_ROUTING_APPLICABILITY_REQUIRED_FOR_PROVING_SCOPE = 0`

The four Authority-82 unknowns remain unchanged.
