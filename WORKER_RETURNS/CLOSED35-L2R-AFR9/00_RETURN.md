# CLOSED35-L2R-AFR9 — Afrobarometer Round 9 Four-Binding Documentary Recovery

Repository: `maidiu/rawlsing`

Base: `agent/vozhd-closed35-l2-documentary-fanin-r1@5c582e2325ecc2b37377cd518fe4c456331c81d8`

Worker branch: `agent/rabochii-closed35-l2r-afr9-four-binding-r1`

Canonical source: `Afro Barometer Round 9.sav`

Canonical SHA-256: `3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8`

## Execution boundary

This worker used GitHub/browser repository evidence plus public producer/archival documentary research only.

It did **not** open the canonical SAV, inspect new raw bytes, execute source processing, or infer the four bindings from numeric distributions.

All source-physical facts are inherited from the accepted R9 predecessor estate and are treated as settled.

## Exact commissioned set

Only these four bindings were reopened:

1. `Q78F_EXACT_MERGED_COUNTRY_APPLICABILITY_SET`
2. `Q118_11_EXACT_ROUND9_PRODUCER_BINDING`
3. `V397_A_EXACT_ROUND9_ALIAS_BINDING`
4. `V399_A_EXACT_ROUND9_ALIAS_AND_ROLE_BINDING`

All other CLOSED35-L2-AFR9 holdings remain unchanged.

## Holding

One of the four bindings is closed.

Three remain exact producer-authority residuals.

### 1. Q78F exact merged-country applicability — CLOSED

The recovered documentary record now supports an exact Round-9 partition across the 39-country merged denominator.

Afrobarometer's Round 9 Survey Manual establishes the governing mechanism: national partners begin with the Master Questionnaire, indigenize it, and may block out questions that are inappropriate while preserving question numbering. Country-release codebooks and archived producer/distributor data dictionaries then establish whether Q78F actually belongs to each national Round-9 instrument/data release.

The producer 39-country merged release denominator is the accepted 39-country Round-9 set, 53,444 cases. The archived World Bank/DataFirst country records identify Q78F as an actual Round-9 variable in the applicable releases, while country codebooks/dictionaries that omit the item move directly from Q78E to the country-specific Q79 surface. A 53,444-case merged public cross-check independently reconciles the same partition; it is corroborative only and is not the semantic authority.

**Q78F applicable / fielded — 25 countries:**

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

**Q78F not asked in country — 14 countries:**

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

Therefore the exact merged-country applicability binding is:

`Q78F_APPLICABLE_COUNTRIES = 25-country set above`

`Q78F_NOT_ASKED_IN_COUNTRY = 14-country set above`

The already-settled Round-9 code law remains in force: where the merged carrier represents non-applicability, `94 = Not Asked in Country` is an ordinary semantic applicability code, not physical missingness.

No applicability is inferred from missingness, source adjacency, or the zero incidence of the Q78F `-1` declaration.

### 2. Q118_11 exact Round-9 producer binding — RESIDUAL

The final official 39-country Round-9 merged codebook explicitly documents:

`Q118_1 ... Q118_10 -> Q118OTHER -> withinwt_ea -> withinwt_hh`

It does not contain `Q118_11`.

Recovered archived country-release dictionaries also terminate the spoken-language slot family at country-specific maxima no greater than ten before `Q118OTHER`; examples include:

- Ghana: through Q118_10, then Q118OTHER;
- South Africa: through Q118_10, then Q118OTHER;
- Sierra Leone: through Q118_7;
- Tanzania / Ethiopia: through Q118_5;
- Botswana: through Q118_4.

The accepted canonical merged source nevertheless contains physical `Q118_11`; that fact remains binding and must be preserved.

A public downstream data pipeline independently preserves a Round-9 `Q118_11` with the descriptive label "Other spoken languages_eleventh", which corroborates that the field exists in at least one redistributed merged representation. It is not Afrobarometer producer authority.

No official Round-9 questionnaire, country codebook, merged codebook, release note, data dictionary, or processing note recovered in this court defines `Q118_11`.

Adjudication:

`Q118_11 = CANONICAL_MERGED_PHYSICAL_FIELD__EXACT_PRODUCER_BINDING_UNDOCUMENTED`

The evidence is consistent with a merged/export-layer extension, but does not authorize classifying it more specifically as an administrative extension, later harmonized field, or producer-authorized questionnaire slot.

It therefore remains opaque at semantic producer-binding grain.

### 3. V397_A exact Round-9 alias binding — RESIDUAL

Producer documents close the logical Round-9 weight succession:

- `withinwt_ea` = older EA-level within-country weight;
- `withinwt_hh` = newer HH-level within-country weight incorporating the household/adult-selection correction;
- `withinwt_hh` is the producer-selected Round-9 analytical successor at the previously settled descriptive-weight scope.

Archived country releases use those producer long names directly.

The final official merged codebook also uses the long names `withinwt_ea` and `withinwt_hh`. It does **not** use or define `V397_A`.

The inherited accepted canonical-source evidence separately proves that the physical field immediately following `WITHINWT` is `V397_A`, and that its native label matches the logical new-HH within-country role. That convergence is strong evidence about likely lineage, but the commissioned burden is an **exact producer alias binding**, and no producer or archived producer-distributor record recovered here states:

`V397_A = withinwt_hh`

No naming-convention inference is authorized.

IBM SPSS documentation further shows that suffixes such as `_A` can be generated under multiple unrelated duplicate-name/import/name-generation mechanisms. Thus `_A` itself cannot lawfully identify an Afrobarometer semantic status.

Adjudication:

`V397_A = ROLE-COMPATIBLE_WITH_WITHINWT_HH__EXACT_PRODUCER_ALIAS_UNRECOVERED`

The exact alias binding remains residual.

### 4. V399_A exact Round-9 alias and role binding — RESIDUAL

The inherited source court fixes four distinct canonical weight carriers in order:

`WITHINWT / V397_A / COMBINWT / V399_A`

and preserves source-native old/new EA/HH-level labels.

Previously settled producer authority closes the generic combined-weight purpose for merged multi-country descriptive analysis, but the final official Round-9 merged codebook does not document `COMBINWT`, `V399_A`, `combinwt_ea`, or `combinwt_hh`.

A downstream public Round-9 architecture uses the explicit long names `combinwt_old_ea` and `combinwt_new_hh`; this is useful provenance corroboration but is not Afrobarometer producer authority and cannot bind the canonical short carrier.

No exact Round-9 producer document recovered here states:

`V399_A = combinwt_new_hh`

or otherwise defines `V399_A`'s role.

As with `V397_A`, `_A` cannot be semantically decoded from software naming conventions.

Adjudication:

`V399_A = CANONICAL_WEIGHT_CARRIER__NEW-HH-COMBINED_ROLE_CORROBORATED_ONLY__EXACT_PRODUCER_ALIAS_AND_ROLE_UNRECOVERED`

The exact alias and role binding remains residual.

## Updated exact UNKNOWN set

The previous four-item exact unknown set is reduced to exactly three:

1. `Q118_11_EXACT_ROUND9_PRODUCER_BINDING`
2. `V397_A_EXACT_ROUND9_ALIAS_BINDING`
3. `V399_A_EXACT_ROUND9_ALIAS_AND_ROLE_BINDING`

`Q78F_EXACT_MERGED_COUNTRY_APPLICABILITY_SET` is removed from the unknown set.

## Realization consequence

A source-specific realization may now bind Q78F country applicability exactly to the 25/14 partition in this return.

It must continue to:

- preserve `Q118_11` physically but semantically opaque;
- preserve `V397_A` without asserting `V397_A = withinwt_hh`;
- preserve `V399_A` without asserting `V399_A = combinwt_new_hh` or another producer role;
- preserve all previously closed Round-9 semantics unchanged;
- fail closed on any workload that requires one of the three residual exact bindings.

## Documentary sources recovered/admitted

Producer / producer-distributor:

- Afrobarometer, *Round 9 Survey Manual*.
- Afrobarometer, *Merged Round 9 codebook — 39 countries* / final merged codebook.
- Afrobarometer Round-9 country questionnaires/codebooks.
- World Bank Microdata Library / DataFirst archived Afrobarometer Round-9 country data dictionaries and 39-country merged catalog, identifying Afrobarometer network institutions as producers.

Corroborative only:

- public 53,444-case merged query cross-check used to reconcile the Q78F 25/14 country partition;
- basedosdados public Round-9 schema/architecture preserving `Q118_11` and long-name weight families;
- IBM SPSS documentation showing that `_A` suffixes are not uniquely semantic.

## Terminal

`CLOSED35_L2R_AFROBAROMETER_R9_RESIDUAL_AUTHORITY_FROZEN__EXACT_UNKNOWN_SET_RETURNED`
