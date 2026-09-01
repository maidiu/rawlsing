# FFP017 — FIRST GENUINE CANARY COEXPOSURE + RISK-SET MATERIALIZATION R1

Status: `PASS__FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET_MATERIALIZED`

Exact starting HEAD: `34c0136840757d748c90d6733240ddb675d05c88`

Consumed authority/evidence:

- Global HQ respondent commission `d3e93ab491dbbdc1763c019f44992b6884456b5b`
- FFP014 admitted respondent package `34c0136840757d748c90d6733240ddb675d05c88`
- FFP015 repaired canary `f1d4474c24a0127cf4e37719d2c857664db8b38a`
- FFX002-R2 `5343862783959a1455735c0a5eb7b330c76f42d5`

No PRA, CIM, CITC, FFX002 representation-arm execution, survey weighting, Q03 redistribution, or A/B/C-output inspection was performed.

## Admitted respondent carrier reused

FFP014 current carrier:

- schema/version: `FFP014_R5_CURRENT_RESPONDENT_CARRIER@1`
- carrier identity: `sha256:6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5`
- physical member SHA-256: `f55741a53a4caed3f74980afba2488233caa93dd4f1a2edcfde8d90e2fcce4be`
- rows: `51,587`
- stable Library ref: `libfile_23bfb6d5340881918ac372b6b8b4cf3b`
- respondent identity remains the admitted FFP014 `(COUNTRY, RESPNO)` source identity, namespaced by the current carrier; row order is not identity.

Exact source remains `Data/Afro Barometer Round 5.sav`, SHA-256 `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`, 49,689,458 bytes, 51,587 rows.

The FFP017 SPSS decoder was independently cross-checked against the admitted carrier's existing Q96 and Q73D projections for all 51,587 respondents: mismatches `0`. Q96/Q73D were used only as decoder checksum fields; Q73D exposure was not executed or consumed.

## Exact selected surface

Core claim measurements (12): `Q70B,Q70C,Q73A,Q84,Q76A,Q76B,Q86A,Q86B,Q86C,Q86D,Q86E,Q86F`.

Supplementary only: `Q93C`.

All 13 exact current C04 predicates require only the admitted respondent input `COUNTRY_ALPHA3`; no selected item requires `RESPONDENT_HAS_PAID_EMPLOYMENT` or another ungoverned respondent-semantic input. Exact qimpl/predicate identities and source evidence are frozen in `01_MEASUREMENT_ROUTING_EXPOSURE_MATRIX.tsv`.

The exact C04 compiled predicates are preserved literally, including the historical parser's literal `AND` token in Q70B/Q70C/Q93C predicates. `AND` is absent from the admitted respondent country-token namespace, so it changes no respondent result. It is not silently rewritten in the authoritative predicate record.

## Per-measurement exposure counts

| measurement | exposed | nonexposed | unresolved |
|---|---:|---:|---:|
| Q70B | 49,183 | 2,404 | 0 |
| Q70C | 26,399 | 25,188 | 0 |
| Q73A | 45,598 | 5,989 | 0 |
| Q84 | 44,398 | 7,189 | 0 |
| Q93C | 49,183 | 2,404 | 0 |
| Q76A | 45,598 | 5,989 | 0 |
| Q76B | 45,598 | 5,989 | 0 |
| Q86A | 45,598 | 5,989 | 0 |
| Q86B | 45,598 | 5,989 | 0 |
| Q86C | 45,598 | 5,989 | 0 |
| Q86D | 45,598 | 5,989 | 0 |
| Q86E | 45,598 | 5,989 | 0 |
| Q86F | 45,598 | 5,989 | 0 |

Exposure is computed from C04 predicate inputs only. Response presence, response substance, response missingness, row co-presence, and source-block membership do not participate in exposure/coexposure.

## Core common coexposure risk set

Exact declared common country scope:

`COUNTRY_ALPHA3 NOT IN {ALG,BDI,BEN,CAM,CDI,EGY,GHA,GUI,LIB,MAD,MLI,MRC,NGR,NIG,SEN,SRL,SUD,SWZ,TAN,TOG,TUN,ZAM,ZIM}`

For all 51,587 admitted respondents, this declared scope is exactly equal to the independently executed intersection of positive exposure to all 12 core claim measurements.

`CORE_CLAIM_COMMON_RISK_SET`:

- respondent count: `19,210`
- semantic member-set SHA-256: `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`
- physical artifact SHA-256: `c5281c564c1cafdcbe6769013b46834bc4da9bb481e56a172a581fee745cb8dc`
- Library ref: `libfile_2851ba4555a88191a427ba4785ceba81`

This is the core `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1` materialization.

## Q93C supplementary sensitivity set

FFX002-R2 requires common semantic risk-set identity before representation fork but does not authorize supplementary availability to narrow the core claim by implication. FFP017 therefore materializes a separate core-plus-Q93C sensitivity set.

`SUPPLEMENTARY_Q93C_SENSITIVITY_RISK_SET`:

- respondent count: `19,210`
- semantic member-set SHA-256: `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`
- physical artifact SHA-256: `c7f5ec4ca3001f38d8f2e0ceb2b5d2dc86437ddbee278731cad5a2459c201117`
- Library ref: `libfile_1fda761ed63c8191b1963a82411b6403`

The two sets are empirically member-identical because every core-risk respondent is already Q93C-exposed. They remain distinct logical risk-set variants because Q93C is supplementary, not claim-constitutive.

## Q73A native contrast membership

Within the 19,210-member core coexposure risk set:

- exposed + native `Q73A=0`: `7,466`
- exposed + native `Q73A=1`: `10,161`
- typed non-contrast `Q73A=9`: `1,578`
- typed non-contrast `Q73A=-1`: `5`

No other Q73A state occurs inside the core risk set. The 0/1 states are not collapsed with special/non-substantive states.

Contrast-membership artifact:

- SHA-256: `425a23d2b70e902e832ba7d989abc7d861e0c132046da3965687d685411d0c02`
- Library ref: `libfile_f63ff5f49bfc8191a61fe5c63a124dd7`

No Q03 redistribution is computed here.

## Executable J3_NATIVE_Q86ABC

Actual same-respondent exposure to Q86A, Q86B, and Q86C is positively proved for all 19,210 core-risk respondents before any response tuple is formed.

`J3_NATIVE_Q86ABC = (Q86A,Q86B,Q86C)` therefore has:

- same-respondent coexposed support: `19,210`
- exact native tuple states observed: `38`
- semantic support-inventory SHA-256: `94eda179f7886f3419bcf16c4e7c9b45451676f9361b2700566c8c2c75cf9ed3`
- respondent-fact artifact SHA-256: `c8e26789d271dd1b3975a82223d58414bfc8b33664a853beaf06cec3aedecc17`
- respondent-fact Library ref: `libfile_2355b085cff4819184c8a6fb3116bd9b`
- support-inventory artifact SHA-256: `472e4b873b1cff882c57b54dab5b66d19b5cd434b9392ead755c6f8d8e287fbf`
- support-inventory Library ref: `libfile_bcfa905b21188191a7fc1e84dd251a59`

All source-native states, including special states, remain exact tuple members. No many-to-one collapse was applied.

## Independent response and exposure carriers

Selected response facts:

- rows: `670,631` = `51,587 respondents × 13 measurements`
- SHA-256: `98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709`
- Library ref: `libfile_2befdf759ad88191b608ff30bed717ed`

Selected exposure facts:

- rows: `670,631`
- SHA-256: `0920c350aeb900b5922cf3872f86609de6a8cebb8d3991680dc9ee40e85b06ce`
- Library ref: `libfile_0cf848f0ca6c8191a5c992e473517a18`

Response facts contain respondent + measurement + native response state but no exposure result. Exposure facts contain respondent + qimpl + measurement + predicate input/result + exposure state but no response state. They are joinable only through governed respondent and exact measurement identity.

Q84 response-state identity remains country-qualified. No cross-country Q84 category equivalence is asserted.

## Deterministic replay / hostile receipt

Executed builder SHA-256: `69f4341e904a297e6d73cae3df6de552542d34b3b61eb7e6f7e6aec677d30c6b`.

Two independent complete runs from the exact source, admitted FFP014 carrier bytes, admitted FFP014 respondent identity mapping, and exact C04 predicate carrier produced byte-identical outputs for every artifact.

Replay receipt SHA-256: `548b88be3a5df043e8e5129b7b46f3660d2c451f9bb177afb381f7829679f209`; Library ref: `libfile_bea346c880bc81918d13c193a1888f09`.

Every uploaded heavy artifact was then rematerialized from Library and compared byte-for-byte with its executed local artifact: all PASS.

Explicit hostile confirmations:

- missing response used as nonexposure: `NO`
- substantive response used as exposure proof: `NO`
- row co-presence used as coexposure: `NO`
- source-block membership used as coexposure: `NO`
- row order used as identity: `NO`
- unresolved predicate input coerced false: `NO`
- survey weights applied: `NO`
- representation outputs inspected: `NO`

## Unresolved / noncomparable register

Selected-surface exposure unresolved rows: `0`.

Preserved external unresolved edge:

`Q73D / C04P.f751f53c113a339f2cb8 / RESPONDENT_HAS_PAID_EMPLOYMENT = EXPOSURE_BINDING_UNRESOLVED`

Q73D is excluded from this repaired canary and from every FFP017 risk-set operation. Its unresolved state is neither repaired nor generalized away.

Additional retained ceilings:

- Q84 native categories remain country-qualified and non-harmonized.
- Q73A special states remain typed non-contrast states.
- Q86A-F special states remain exact native states; J3 does not collapse them.
- Q93C remains `SUPPLEMENTARY` and does not define the core claim risk set.

Unresolved/noncomparable manifest SHA-256: `fe841b49a8d7b4f0bfb1a9943fb18e0c63511966510b5c7f95da81c3d204baf6`; Library ref: `libfile_f3e43dcab7708191874b370b4c9d16fa`.

`PASS__FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET_MATERIALIZED`
