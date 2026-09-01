# FFP018 — FIRST GENUINE CANARY AUTHORITATIVE CIM + ESTIMAND FREEZE R1

Status: `PASS__FIRST_GENUINE_CANARY_EMPIRICAL_PROPOSITION_CIM_FROZEN__COMPARISON_ID_PENDING_CITC`

Exact starting HEAD: `97ad8148a5227e8be6d80e5beaccc4d80db8d5a8`

Claim: `FFR2_R5_Q03_Q73A_CONDITIONAL_DISPOSITION_REDISTRIBUTION_CANARY@1`

## Dispositive freeze

`CLAIM_PROPOSITION_IDENTITY = FROZEN`

`COMPARISON_CLAIM_IDENTITY = PENDING_CITC`

`EMPIRICAL_PROPOSITION_KEY = FFR2_R5_Q03_Q73A_CONDITIONAL_DISPOSITION_REDISTRIBUTION_CANARY@1/EMPIRICAL_PROPOSITION_KEY@1`

`PROPOSITION_HASH = sha256:b967da7084c319193237980e17ac0e40443dad88b6608b9d73abd1eae3e97430`

The exact proposition-hash input is the exact UTF-8 byte content of `01_EMPIRICAL_PROPOSITION_PAYLOAD.json`: sorted JSON object keys, declared semantic array order, compact separators, no trailing newline.

`CIM_REF = FFP018_FIRST_GENUINE_CANARY_CLAIM_IDENTITY_MANIFEST@1`

`CIM_SHA256 = 046666a09de586398e978c2ceb6e9b54e4a939894ccc878a4a67d5dfa91731a2`

The CIM hash is SHA-256 over the exact UTF-8 byte content of `00_CLAIM_IDENTITY_MANIFEST.json`.

## Frozen proposition

Among governed Afrobarometer R5 respondents in `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`, for each active disposition `D` in `{Q76A,Q76B,Q86A,Q86B,Q86C,Q86D,Q86E,Q86F}` and each exact source-native state `s`, the empirical target is:

`Delta_D(s) = P_sample(D=s | R*, Q73A=1) - P_sample(D=s | R*, Q73A=0)`

Native `Q73A=0` is the baseline and native `Q73A=1` the comparison state. Native `Q73A=9` and `Q73A=-1` remain typed source-native evidence outside the contrast. No category collapse or special-state merge is performed.

## Empirical unit / scope / risk set

- carrier: `FFP014_R5_CURRENT_RESPONDENT_CARRIER@1`
- carrier identity: `sha256:6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5`
- governed respondent key: `(COUNTRY, RESPNO)`
- source: `Data/Afro Barometer Round 5.sav`
- source SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`
- exact risk set: `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`
- respondents: `19,210`
- semantic member-set SHA-256: `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`
- physical artifact SHA-256: `c5281c564c1cafdcbe6769013b46834bc4da9bb481e56a172a581fee745cb8dc`
- Library ref: `libfile_2851ba4555a88191a427ba4785ceba81`
- country scope: `COUNTRY_ALPHA3 NOT IN {ALG,BDI,BEN,CAM,CDI,EGY,GHA,GUI,LIB,MAD,MLI,MRC,NGR,NIG,SEN,SRL,SUD,SWZ,TAN,TOG,TUN,ZAM,ZIM}`

## PRA / TTAR

FFP016 is bound without reinterpretation:

- active positions: `Q70B,Q70C,Q73A,Q84`
- supplementary only: `Q93C`
- active dispositions: `Q76A,Q76B,Q86A,Q86B,Q86C,Q86D,Q86E,Q86F`
- PRA commit: `04c604be2ee4e32367f2074fdad380c7c563b740`
- role receipt blob SHA: `76d67a60a9e52bc448d4678f17d29b0d7ef8404e`
- ancestry-disjointness receipt blob SHA: `150e40078aaeb00be559d1d710685696e6aae8b1`

`TTAR_IMPLICATION = NONE__NO_TRANSFORM_PERFORMED`

No Q84 cross-country equivalence, Q93C continuization, category collapse, special-state merge, or cross-source/cross-wave transport is admitted.

## Estimand / weight target

`ESTIMAND = ADMITTED__UNWEIGHTED_SAMPLE_DESCRIPTIVE_CONDITIONAL_STATE_REDISTRIBUTION@1`

`WEIGHT_TARGET = NONE__EXPLICIT_UNWEIGHTED_SAMPLE_DESCRIPTIVE_CLAIM`

This is lawful because the proposition's target is the exact finite admitted FFP017 sample/risk set itself. `NONE` therefore defines the absence of an external weighted population target in this proposition; it does not assert that survey weights are invalid for another separately registered claim.

No population generalization and no causal inference are authorized.

## Semantic input

`SEMANTIC_INPUT_REF = FFP018_CLAIM_COMMON_SEMANTIC_INPUT_BINDING@1`

`SEMANTIC_INPUT_HASH = sha256:6895a6a9dac8833b58a8d426c34c9d9e821b1af12e8f4b7b62c557236f43e417`

The binding covers the exact source SHA, current carrier/respondent identity, FFP017 semantic risk-set identity, FFP016 exact measurement-role/qimpl identities and ancestry disjointness, FFP017 routing/exposure matrix, source-native state preservation, and empty TTAR sequence.

## Evidence metadata, not materiality

Within the exact risk set FFP017 realized:

- `Q73A=0`: `7,466`
- `Q73A=1`: `10,161`
- `Q73A=9`: `1,578`
- `Q73A=-1`: `5`

These are preserved execution/evidence metadata. They set no prevalence, support, uncertainty, or materiality threshold.

`J3_NATIVE_Q86ABC=(Q86A,Q86B,Q86C)` remains an exact source-native same-respondent derived empirical view with support `19,210`; it is not proposition-constitutive and is not the empirical substrate.

## Representation identity

`representation_scope_mode = REPRESENTATION_NEUTRAL`

Exact configuration, local geometry, and direct conditional redistribution are comparison views over the same frozen proposition. No view producer may mutate the CIM. No representation/theory noun is part of proposition identity.

## CITC-reserved unresolved fields

The following remain null/pending and are excluded from `PROPOSITION_HASH`:

- `support_uncertainty_contract_ref/hash`
- `invariant_tolerance_contract_ref/hash`
- confidence/uncertainty regime, if any
- minimum-support rule, if any
- permutation/resampling rule, if any
- TV/distributional tolerance, if any
- recall/preservation cutoff, if any
- `COMPARISON_CLAIM_KEY`
- `COMPARISON_CLAIM_HASH`

The CITC successor must consume exact proposition hash `b967da7084c319193237980e17ac0e40443dad88b6608b9d73abd1eae3e97430` and may add the comparison contract without changing any proposition coordinate.

`EMPIRICAL_REPRESENTATION_OUTPUTS_INSPECTED = NO`

Only authority/evidence and respondent/exposure/risk-set artifacts were inspected; no A/B/C empirical representation outputs were inspected.

`PASS__FIRST_GENUINE_CANARY_EMPIRICAL_PROPOSITION_CIM_FROZEN__COMPARISON_ID_PENDING_CITC`
