# V550 response-option runtime integration contract — SAV-derived R2

## Status

R2 supersedes the earlier SAV-derived package. It fixes two issues found by second-pass QA:

1. raw Latinobarómetro alias replicas are **not** duplicated into the runtime response-option map; identifier resolution is performed by an explicit governed crosswalk before QSM/response-option joins;
2. the historical 700-contract validation reports the actual runtime row counts for context/admin variables instead of displaying synthetic zeros.

The runtime authority build is based on:

- the nine current manual response-option authority packets included under `authority_inputs/`;
- the raw SPSS dictionaries derived from the supplied Latinobarómetro 1995, 2011, and 2024 `.sav` files (raw SAV SHA-256 values recorded in `MANIFEST.json`);
- the three Latinobarómetro first-pass authority tables included under `authority_inputs/` as the source-binding → governed-question bridge;
- the prior `V550_response_option_map.csv` only for rows whose `question_id` is absent from every current manual packet; those rows are retained only as quarantined, non-directional legacy lookup rows.

The older `ddm_build` response-option map is not authority and is not used to restore inferred signs.

## Canonical runtime map

`V550_response_option_map_reconciled_sav_derived_r2.csv`

- **350,066** rows are the current nine manual authority packets projected onto the established 71-column runtime schema.
- **42,506** legacy-only rows are retained but explicitly quarantined.
- **0** raw alias replica rows are present.
- **392,572** total rows.
- **28,239** rows carry current response-direction authority.
- quarantined legacy rows carry **0** `response_direction`, **0** `response_intensity`, and **0** `polarity` values.
- zero exact duplicate rows.

The GSS source packet contains five additional GSS-specific diagnostic fields not present in the established 71-column runtime schema: `source_questionnaire_response_label`, `is_see_codebook`, `is_other_unscaled`, `special_subtype`, and `is_not_imputable`. Those fields remain preserved in `authority_inputs/gss_response_option_authority.csv`; R2 does **not** silently redefine the runtime schema to add them.

## Latinobarómetro raw identifier law

`latinobarometro_sav_to_authority_binding_registry.csv` covers all **775** current Latinobarómetro response-authority variables:

- 1995: 196 authority variables;
- 2011: 389;
- 2024: 190.

Every binding is source-wave scoped, and every raw identifier is taken from the corresponding SAV dictionary.

### Direct one-to-one aliases

`latinobarometro_sav_direct_identifier_alias_authority.csv` contains **359** aliases that genuinely require identifier resolution:

- 2011: 215;
- 2024: 144.

Each row resolves exactly one raw SAV variable to exactly one governed authority variable. There are no raw→multiple-authority collisions within wave.

Examples include:

- 2011 `P14ST.A` → `P14ST_A`;
- 2011 `P16N.D` → `P16N_D`;
- 2024 `P12STGBS.A` → `Q12STGBSA`;
- 2024 `P14ST.C` → `Q14STGBSCC`;
- 2024 `P28ST` → `Q28STA`;
- 2024 `P28ST.A` → `Q28STB`;
- 2024 `P39STGBS.A` → `Q39STGBSA`;
- 2024 `P56ST.12` → `Q56N12`;
- 2024 raw `P6NOIJ` → governed `P6NIOJ`.

No global `.`↔`_` rewrite and no global `P`→`Q` rewrite is authorized.

`latinobarometro_sav_direct_alias_resolution_audit.csv` independently proves for all 359 aliases that:

1. the raw variable exists in the SAV dictionary;
2. the first-pass source binding exists and resolves to the same governed `question_id`;
3. the governed authority target exists in the current Latinobarómetro manual packet;
4. the canonical runtime target rows exactly equal the current manual packet rows over the runtime schema.

All 359 are PASS.

### One-to-many families

`latinobarometro_sav_family_binding_authority.csv` contains **110 raw SAV member columns** belonging to **13** governed 2024 authority families.

These are not direct aliases. Examples include `Q23STM` (three ranked raw columns) and `Q48ST` (eleven checkbox columns). A family member must not inherit the family response-option scale through ordinary alias canonicalization.

## Mandatory QUC/V550 identifier resolution order

For a raw respondent variable:

1. preserve `raw_var_code` exactly;
2. resolve exact source + wave + raw identifier against canonical authority identity;
3. if the raw identifier differs from authority identity, use `latinobarometro_sav_direct_identifier_alias_authority.csv`;
4. if the raw identifier appears in `latinobarometro_sav_family_binding_authority.csv`, route to the family-aware handler instead of the direct alias path;
5. only after identity resolution, join `authority_var_code` to QSM and to `V550_response_option_map_reconciled_sav_derived_r2.csv`;
6. retain both raw and authority IDs in row provenance;
7. if no exact governed resolution exists, block rather than invent normalization.

**The runtime response-option map is not an identifier alias registry.** Its exact `var_code` rows are canonical authority identities (plus quarantined legacy lookup rows), not alternate raw spellings.

## Response-direction gate

The included historical `35wave_active_response_semantics_contract_inventory.csv` contains 700 contracts:

- 236 `CERTIFIED_ACTIVE_RESPONSE_SCALE`;
- 254 `CONTEXT_NO_RESPONSE_SCALE`;
- 210 `ADMINISTRATIVE_NO_RESPONSE_SCALE`.

Against R2:

- **236/236** certified active scales have the expected current packet hash, contract hash, substantive-category count, and complete `response_direction` + `response_intensity` coverage for the certified substantive categories;
- **464/464** context/admin contracts have zero signed response rows;
- 354 of those 464 have unsigned runtime response-option rows (7,445 rows total); 110 have no runtime response-option rows;
- all **700/700** court rows are PASS.

The response packet field `is_substantive=true` means a non-missing/substantive answer option and does **not** by itself imply a signed directional scale. For context/admin contracts, the historical inventory's `substantive_category_count=0` means no certified signed response scale applies. Therefore `contract_coverage_status` outranks row-level `is_substantive` for the V551 direction gate.

V551 must require signed response fields **only** for `CERTIFIED_ACTIVE_RESPONSE_SCALE` contracts.

## Scope boundary

The 700-contract court is the supplied historical court, SHA-256 recorded in `MANIFEST.json`. It does not certify a subsequently generated fresh 700-variable selection. After the fresh selection is frozen, run the same contract-coverage court against that exact selection before V551.

## Authority precedence

Current manual response-option packets outrank predecessor `response_option_map` inference. Quarantined legacy rows cannot create signed response authority. Blank current directionality must never be backfilled from old `inferred_from_response_family` values.
