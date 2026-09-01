# FFP007 — EXACT CLAIM-SCOPE / PRA HANDOFF PACKET R2 CORRECTED

Packet status:

`READY_FOR_BOUNDED_PRA_ADJUDICATION__ROLE_FAMILY_EVIDENCE_NOT_ROLE_AUTHORITY__NOT_A_PRA_RECEIPT__NOT_A_FROZEN_CIM`

This packet supplies the exact missing premise identified by FFP003: immutable candidate target-use identity, intended operation, exact source/country/respondent-risk-set contract, and allowed-use boundary.

## A. Authority envelope

Exact consumed authority:

- Global HQ commission `d3e93ab491dbbdc1763c019f44992b6884456b5b`
  - FFC001 `RESPONDENT_EXECUTION_BINDING_ADMISSION`
  - FFC002 `PRA_BOUNDED_POSITION_ROLE_COURT`
- FFX002-R2 `5343862783959a1455735c0a5eb7b330c76f42d5`
- FFP002 `232f5996d7115d12e3a3c46cd44219bd6caed381`
- FFP003 `0b69ce72f0ead8c9dad3e89f9ca92993b6c5f8b5`
- FFP004 `0eaee36a8ecddfc221daf91e74f0663c801982fd`

FFC002 is the only commissioned role-adjudication lane relevant here. FFP007 may nominate exact rows and present role-family evidence; it may not create role-family vocabulary, issue PRA, create a global ontology, promote STRATA, or infer roles at runtime.

## B. Immutable source scope

- source family: `Afrobarometer`
- wave: `R5`
- source path: `Data/Afro Barometer Round 5.sav`
- source SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`
- source bytes: `49,689,458`
- evidenced rows: `51,587`
- dataset identity: `Afrobarometer_Round_5_Afro_Barometer_Round_5`
- codebook: `merged_r5_codebook_2.pdf`
- codebook SHA-256: `7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735`
- routing carrier: `C04_FULL_CURRENT_ROUTING_LEDGER.csv`
- routing carrier SHA-256: `c3148341c5a6315c4b060f665595c93c4aa935dfc171aa5faf4c14628f914f90`

No source acquisition, source-byte substitution, or source-semantic widening is authorized.

## C. Immutable candidate target-use identity and operation

Target-use identity:

`FFR2_R5_Q03_Q73D_CONDITIONAL_DISPOSITION_REDISTRIBUTION_CANARY@1`

Intended operation:

1. consume an independently admitted current R5 respondent execution binding;
2. retain exactly the PRA-admitted position rows from the finite docket below at native source identity;
3. use native `Q73D=0` versus `Q73D=1` as the bounded Q03 contrast only among respondents lawfully exposed under Q73D's paid-employment predicate;
4. compare native disposition-state distributions for `Q76A,Q76B,Q86A-Q86F`;
5. optionally compare `J3_NATIVE_Q86ABC` only after positive same-respondent coexposure is materialized;
6. expose the same frozen semantic inputs to every admitted FFX002-R2 Q03 view.

This is descriptive conditional redistribution, not causal estimation and not structural-semantic admission.

## D. Candidate respondent risk-set contract

Conservative common source-country scope:

`COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN,SWZ}`

Q73D exact additional eligibility:

`COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN} AND RESPONDENT_HAS_PAID_EMPLOYMENT == True`

- qimpl: `question_impl.phase0.391123a4e7d3c8f0fd3b`
- predicate: `C04P.f751f53c113a339f2cb8`

Final respondent risk set `R*` must be materialized by `CURRENT_RESPONDENT_EXECUTION_BINDING_CONTRACT@1` or a competent successor and must bind exact current respondent identity, qimpl -> empirical measurement, predicate input values, deterministic predicate result, governed exposure state, independent response binding, and replayable source/currentness ancestry.

Forbidden implications:

`SOURCE_PRESENCE -> EXPOSURE`

`ROUTING_SPECIFICATION -> EXECUTED_EXPOSURE`

`RESPONSE_MISSINGNESS -> NONEXPOSURE`

`CURRENT_J_CANDIDATE -> EXECUTABLE_SAME_RESPONDENT_J`

Until FFC001 positively closes that chain, this packet authorizes no execution.

## E. Finite FFC002 PRA docket

Only the claim-role vocabulary already carried by FFX002/FFP004 is used as the requested role: `ACTIVE_POSITION`, `ACTIVE_DISPOSITION`, `SUPPLEMENTARY`, `CONDITIONING`, `DIAGNOSTIC`, `EXCLUDE`.

### E1. Proposed core position rows

| source variable | exact qimpl | requested role | source-semantic family evidence — nonauthoritative | requested bounded use |
|---|---|---|---|---|
| Q70B | `question_impl.phase0.311d905b2baab867642e` | `ACTIVE_POSITION` | household material/public-benefit relation | native household school-feeding receipt coordinate |
| Q73A | `question_impl.phase0.cae005624221d7b00dd2` | `ACTIVE_POSITION` | fiscal incorporation/obligation relation | native sales/VAT obligation coordinate |
| Q73D | `question_impl.phase0.391123a4e7d3c8f0fd3b` | `ACTIVE_POSITION` | employment-linked fiscal relation | native paid-employment income-tax obligation coordinate and Q03 contrast |
| Q84 | `question_impl.phase0.5a05ce882452ef85debd` | `ACTIVE_POSITION` | relational-identity-family evidence | respondent ethnic/cultural/tribal affiliation at native category identity |

The fourth column is **evidence**, not a formal role assignment. FFP007 does not mint `HOUSEHOLD_SOCIAL_PROTECTION_MATERIAL_RELATION`, `FISCAL_INCORPORATION_OBLIGATION_RELATION`, `EMPLOYMENT_LINKED_FISCAL_RELATION`, `RELATIONAL_IDENTITY_BACKGROUND_POSITION`, or any similar ontology token.

The existing PRA vocabulary evidenced in predecessor material includes `RELATIONAL_IDENTITY_POSITION` as a recognizable candidate kind, but even that role is not issued here. FFC002 must rule the exact Q84 use.

For the FFX002 family floor, FFC002 must positively establish at least three authorized analytic-role families. The source-semantic docket supplies three materially independent questions for that court:
1. household material/public-benefit relation — Q70B;
2. fiscal/employment relation — Q73A/Q73D;
3. relational identity — Q84.

If FFC002 does not authorize at least three families and at least four ACTIVE_POSITION rows, the canary fails closed.

### E2. Position-side sensitivity row

| source variable | exact qimpl | requested role | source-semantic evidence | ceiling |
|---|---|---|---|---|
| Q93C | `question_impl.phase0.f62bceafa49dd85eb525` | `SUPPLEMENTARY` | respondent digital-financial practice/access frequency | not wealth, class, capital volume, income, employment relation, or hierarchy |

FFC002 may instead assign `CONDITIONING` or `EXCLUDE`; no stronger position role is presumed.

### E3. Disposition rows

Q76:
- Q76A `question_impl.phase0.6a1a2eb3ed5d31e7e0cf`
- Q76B `question_impl.phase0.2d7f53868dd52feea700`

Q86:
- Q86A `question_impl.phase0.67f036c0efb7fb98ff4a`
- Q86B `question_impl.phase0.2fb3a62609dad4c1306d`
- Q86C `question_impl.phase0.5e173e45a10de7c832fd`
- Q86D `question_impl.phase0.b2b6525f8699525e60ea`
- Q86E `question_impl.phase0.2aef51cfcb3d44e4870a`
- Q86F `question_impl.phase0.0bdb38e7f76aadd487da`

Requested role: `ACTIVE_DISPOSITION`.

FFP003 ceiling governs Q86A-F exactly: `ATTITUDE_OR_DISPOSITION_ONLY`. The nationality, parentage, sex, marital, migration, employment, or citizenship attributes of a hypothetical subject may not become respondent position facts.

## F. Position/disposition ancestry separation

Candidate position blocks: `Q70 / Q73 / Q84`

Position sensitivity: `Q93`

Disposition blocks: `Q76 / Q86`

No active disposition item constructs any candidate position row. No position item constructs a disposition state. Any later derived operand whose ancestry crosses the boundary fails closed pending exact source-ancestry/PRA review.

## G. Disposition batteries and higher-order object

Battery 1: `Q76A,Q76B`

Battery 2: `Q86A,Q86B,Q86C,Q86D,Q86E,Q86F`

Exact Q86 source structure: `cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4`

- `MATRIX_GRID`
- `Explicit source block Q86`
- complete exact current member binding
- source-level `CURRENT_J_CANDIDATE`

Order>=3 candidate: `J3_NATIVE_Q86ABC := (Q86A,Q86B,Q86C)`

The eight substantive binary tuples are source-state products only. An empirical tuple may be counted only when FFC001/current respondent execution proves same-respondent exposure to all three measurements. No response blankness or source co-presence can substitute.

## H. Exact Q03 contrast and candidate estimand

Q03 contrast: `Q73D=0` vs `Q73D=1` among `R*` satisfying the exact paid-employment eligibility predicate.

Do not fold `7`, `9`, `997`, `998`, or `-1` into either contrast state.

Candidate estimand:

`UNWEIGHTED_SAMPLE_DESCRIPTIVE_CONDITIONAL_STATE_REDISTRIBUTION@1`

`Delta_D(s) = P_sample(D=s | R*, Q73D=1) - P_sample(D=s | R*, Q73D=0)`

Optional J3 estimand after coexposure admission:

`Delta_J3(c) = P_sample(J3_NATIVE_Q86ABC=c | R*, Q73D=1) - P_sample(J3_NATIVE_Q86ABC=c | R*, Q73D=0)`

Interpretation ceiling: sample-descriptive, noncausal, no population generalization, no latent/field/class/STRATA inference.

Exact authority slots retained from FFP004:

`ESTIMAND_AUTHORITY = ESTIMAND_AUTHORITY_PENDING_EXACT_CANARY`

`REQUESTED_WEIGHT_DESIGN_POSTURE = NONE__EXPLICIT_UNWEIGHTED_SAMPLE_DESCRIPTIVE_TARGET`

`WEIGHT_DESIGN_AUTHORITY = WEIGHT_DESIGN_AUTHORITY_PENDING_EXACT_CANARY`

Thus FFP007 proposes an unweighted target but does **not** govern the `NONE` posture itself. A competent pre-fork authority must bind it before execution. No survey weight is silently activated.

## I. TTAR / transform boundary

No semantic/equivalence transform is required for native Q73D 0-vs-1, native Q76 states, native Q86 0/1 states, or exact Q86ABC tuple construction after exposure proof.

Separate typed authority is required before Q76 state collapse or ordinal-to-continuous treatment, Q84 category collapse/harmonization/cross-country equivalence, Q93C collapse or continuous treatment, special-state merging, cross-wave/source transport, or any derived state that changes sameness, order, grouping, or comparability.

## J. FFX002 preparation-floor handoff

| requirement | handoff state |
|---|---|
| four ACTIVE_POSITION candidates | `Q70B;Q73A;Q73D;Q84` — PRA pending |
| three role-family evidence bases | household material/public-benefit; fiscal/employment; relational identity — FFC002 authority pending |
| no single position block | Q70/Q73/Q84 |
| sensitivity candidate | Q93C — `SUPPLEMENTARY` requested |
| eight disposition candidates | Q76A/B + Q86A-F |
| two batteries | Q76 + Q86 |
| order>=3 config | Q86ABC source-native candidate |
| Q03 | Q73D 0-vs-1 -> Q76/Q86 redistribution |
| estimand | explicit candidate; authority pending |
| weight/design | exact unresolved authority slot retained |
| respondent exposure/coexposure | FFC001 pending |
| PRA | FFC002 pending |
| CIM | not frozen |

Fail-closed rules:

1. If FFC002 returns fewer than four ACTIVE_POSITION rows or fewer than three authorized analytic-role families:
`CANARY_REJECTED__NO_GOVERNED_R5_CANDIDATE_MEETS_FFX002_R2_ADMISSION_FLOOR`

2. If FFC001 cannot establish actual common respondent exposure/coexposure for the required measurements/J subset:
`CANARY_REJECTED__NO_GOVERNED_R5_CANDIDATE_MEETS_FFX002_R2_ADMISSION_FLOOR`

3. If exact estimand/weight-design authority remains unbound, execution remains blocked even if PRA/respondent admission pass.

## K. Exact allowed-use boundary

Any PRA receipt consuming this packet must be bounded to:

`FFR2_R5_Q03_Q73D_CONDITIONAL_DISPOSITION_REDISTRIBUTION_CANARY@1`

and only to asking whether native Q76/Q86 disposition distributions differ across the native Q73D 0-vs-1 paid-employment tax-obligation contrast within the positively governed common R5 respondent risk set, with identical semantic inputs across FFX002-R2 views.

It must not authorize a general Afrobarometer position ontology, STRATA, objective class membership, capital volumes, field position, pressure/hegemony/homology, causal interpretation, Q86-as-position, response missingness as exposure, ungoverned transforms, weighted population inference, or cross-wave/source transport.

## L. Successor receipts required before FFX002 execution

1. FFC002 bounded PRA receipt over this exact finite docket;
2. FFC001 authoritative current R5 respondent execution binding;
3. competent binding of exact estimand and weight/design posture;
4. competent CIM/claim-semantic freeze consuming those receipts;
5. common semantic input manifest after all authority inputs are fixed;
6. FFX002 holdout/experiment receipts and empirical support checks;
7. CITC materiality/tolerance authority before any thresholded cross-view invariance ruling.

None is minted by FFP007.

Terminal handoff token:

`FIRST_CANARY_CANDIDATE_SUBSTRATE_SELECTED__PRA_AND_RESPONDENT_COEXPOSURE_PENDING`
