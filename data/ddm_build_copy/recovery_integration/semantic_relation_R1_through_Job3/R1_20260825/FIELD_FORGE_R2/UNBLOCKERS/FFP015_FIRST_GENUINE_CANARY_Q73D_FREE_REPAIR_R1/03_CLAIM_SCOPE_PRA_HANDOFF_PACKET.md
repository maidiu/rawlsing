# FFP015 — Q73D-FREE EXACT CLAIM-SCOPE / DISPOSITIVE PRA HANDOFF R1

Packet status:

`Q73D_FREE_CANARY_SELECTED__EXACT_CLAIM_SCOPE_READY_FOR_PRA`

This packet supplies the exact missing premise required by FFP003 for the finite FFC002 court. It is not a PRA receipt and not a frozen CIM.

## A. Authority envelope

Consumed:

- Global HQ `d3e93ab491dbbdc1763c019f44992b6884456b5b`
- FFX002-R2 `5343862783959a1455735c0a5eb7b330c76f42d5`
- FFP003 `0b69ce72f0ead8c9dad3e89f9ca92993b6c5f8b5`
- FFP004 `0eaee36a8ecddfc221daf91e74f0663c801982fd`
- FFP007 `44f98c639ae72b5963e00eda6793ae5aea327846`
- FFP008 `71530e83219c9fb5b201cae9eeb9c55750dcba79`

Competent role court:

`FFC002 / PRA_BOUNDED_POSITION_ROLE_COURT / EXISTING_VOZHD_HQ_SEMANTIC_ARCHITECTURE_AUTHORITY`

FFC002 may adjudicate only the finite first-claim roles. It may not create a global ontology, promote STRATA, infer roles at runtime, mint source semantics, or repair respondent execution.

## B. Immutable candidate target-use identity

`FFR2_R5_Q03_Q73A_CONDITIONAL_DISPOSITION_REDISTRIBUTION_CANARY@1`

This supersedes FFP007's Q73D-based candidate target-use for preparation purposes only. No CIM is frozen by FFP015.

## C. Exact source scope

- family: `Afrobarometer`
- wave: `R5`
- source object: `Data/Afro Barometer Round 5.sav`
- SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`
- source bytes: `49,689,458`
- evidenced respondent rows: `51,587`
- dataset identity: `Afrobarometer_Round_5_Afro_Barometer_Round_5`
- source codebook: `merged_r5_codebook_2.pdf`
- codebook SHA-256: `7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735`
- current routing carrier used: `C04_FULL_CURRENT_ROUTING_LEDGER.csv`
- routing carrier SHA-256 inherited from FFP007: `c3148341c5a6315c4b060f665595c93c4aa935dfc171aa5faf4c14628f914f90`

No source acquisition or source substitution is authorized.

## D. Exact country scope

The common source-administration intersection is:

`COUNTRY_ALPHA3 NOT IN {ALG,BDI,BEN,CAM,CDI,EGY,GHA,GUI,LIB,MAD,MLI,MRC,NGR,NIG,SEN,SRL,SUD,SWZ,TAN,TOG,TUN,ZAM,ZIM}`

This exact narrowing is required by the Q70C replacement. It must remain visible in the claim identity/risk-set construction. It may not be hidden as view-local preprocessing.

## E. Required respondent grain / risk-set contract

Required grain:

`ONE_GOVERNED_ADMITTED_R5_RESPONDENT AS EMPIRICAL ENTITY, WITH EACH CLAIM MEASUREMENT ATTACHED THROUGH POSITIVE ROUTING/EXPOSURE/RESPONSE BINDINGS`

Let `R*` denote respondents satisfying the exact common country scope and positively governed exposure to all claim-required measurements under the future/current respondent execution binding.

The respondent authority must bind:

- exact respondent identity and source membership;
- exact qimpl -> empirical measurement identity;
- source-country predicate inputs;
- deterministic routing predicate results;
- governed exposure states;
- independent response facts;
- source/currentness ancestry;
- same-respondent coexposure for J when used.

Forbidden:

`SOURCE_PRESENCE -> EXPOSURE`

`ROUTING_SPECIFICATION -> EXECUTED_EXPOSURE`

`RESPONSE_MISSINGNESS -> NONEXPOSURE`

`CURRENT_J_CANDIDATE -> EXECUTABLE_SAME_RESPONDENT_J`

No selected claim-constitutive predicate requires `RESPONDENT_HAS_PAID_EMPLOYMENT`.

## F. FFP008 exclusion

`Q73D` is not an active-position candidate, conditioning operand, Q03 contrast, sensitivity operand, or disposition in this claim.

Its FFP008 blocker:

`RESPONDENT_HAS_PAID_EMPLOYMENT__NO_EXACT_GOVERNED_R5_SOURCE_MEASUREMENT_BINDING`

is not adjudicated or approximated here.

## G. Finite FFC002 position docket

Requested `ACTIVE_POSITION` rows:

1. `Q70B`
   - qimpl `question_impl.phase0.311d905b2baab867642e`
   - source meaning: household school-feeding benefit receipt
   - evidence family: household material/public social-protection relation
   - ceiling: not income/class/wealth/capital/employment status
2. `Q70C`
   - qimpl `question_impl.phase0.575fb5e032fab4cd18a4`
   - source meaning: household old-age government social-grant receipt, explicitly not employment-pension semantics
   - evidence family: same household material/public social-protection relation as Q70B
   - ceiling: not respondent age/retirement/prior employment/income/class/wealth/capital
3. `Q73A`
   - qimpl `question_impl.phase0.cae005624221d7b00dd2`
   - source meaning: general sales-tax/VAT legal obligation
   - evidence family: fiscal incorporation/obligation relation
   - ceiling: not tax actually paid/income/class/wealth/employment
4. `Q84`
   - qimpl `question_impl.phase0.5a05ce882452ef85debd`
   - source meaning: own ethnic community/cultural group/tribe
   - evidence family: relational identity; predecessor design recognizes `RELATIONAL_IDENTITY_POSITION` as a bounded candidate kind
   - ceiling: no cross-country equivalence, hierarchy, essentialism, STRATA, or automatic distance

FFP015 does not mint `HOUSEHOLD_SOCIAL_PROTECTION_MATERIAL_RELATION`, `FISCAL_INCORPORATION_OBLIGATION_RELATION`, or any other new ontology token. The evidence-family descriptions above are docket evidence only.

FFC002 must decide whether these exact four rows may be `ACTIVE_POSITION` and whether the docket satisfies the required >=3 authorized analytic-role families. If not, fail the canary rather than relaxing FFX002-R2.

## H. Supplementary / sensitivity docket

`Q93C`

- qimpl `question_impl.phase0.f62bceafa49dd85eb525`
- requested role: `SUPPLEMENTARY`
- exact meaning: frequency of mobile-phone money transfer / bill payment
- native order `0-4` preserved
- ceiling: not wealth,class,capital,income,employment relation,or status hierarchy

Q93C was tested and deliberately not promoted to active position because current evidence does not establish an already-governed structural-position family for that practice.

## I. Active-disposition docket

Preserved without change:

- Q76A `question_impl.phase0.6a1a2eb3ed5d31e7e0cf`
- Q76B `question_impl.phase0.2d7f53868dd52feea700`
- Q86A `question_impl.phase0.67f036c0efb7fb98ff4a`
- Q86B `question_impl.phase0.2fb3a62609dad4c1306d`
- Q86C `question_impl.phase0.5e173e45a10de7c832fd`
- Q86D `question_impl.phase0.b2b6525f8699525e60ea`
- Q86E `question_impl.phase0.2aef51cfcb3d44e4870a`
- Q86F `question_impl.phase0.0bdb38e7f76aadd487da`

Requested role: `ACTIVE_DISPOSITION`.

FFP003 negative ceiling is incorporated exactly in effect:

`Q86A-F = ATTITUDE_OR_DISPOSITION_ONLY`

No hypothetical subject attribute may become a respondent position fact.

## J. Position / disposition ancestry separation

Position source blocks: `Q70 / Q73 / Q84`

Supplementary block: `Q93`

Disposition source blocks: `Q76 / Q86`

No active disposition constructs a position operand. No position item constructs a disposition state. Any later derived operand crossing this boundary fails closed pending explicit ancestry review.

## K. Higher-order native configuration

Exact structure:

`cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4`

`MATRIX_GRID / Q86A-F`

Order-3 candidate:

`J3_NATIVE_Q86ABC := (Q86A,Q86B,Q86C)`

No recode. Native substantive 0/1 states remain exact. Non-substantive states remain typed. Count J tuples only after positive same-respondent coexposure.

## L. Exact bounded Q03 contrast

Contrast operand: `Q73A`.

Native groups:

- `Q73A=0`: not required to pay general sales tax/VAT
- `Q73A=1`: required to pay general sales tax/VAT

Exclude from either contrast state:

- `9=Don't know / haven't found out`
- `997=Not asked`
- `998=Refused`
- `-1=Missing`
- any other non-substantive state present in the governed response binding

Question:

> Within `R*`, how do native Q76A/B and Q86A-F disposition-state distributions redistribute between Q73A=0 and Q73A=1?

Optional secondary target: native `J3_NATIVE_Q86ABC` tuple distribution after executable J authority.

No causal claim.

## M. Estimand / design posture

Candidate estimand:

`UNWEIGHTED_SAMPLE_DESCRIPTIVE_CONDITIONAL_STATE_REDISTRIBUTION@1`

`Delta_D(s) = P_sample(D=s | R*, Q73A=1) - P_sample(D=s | R*, Q73A=0)`

Optional J3:

`Delta_J3(c) = P_sample(J3_NATIVE_Q86ABC=c | R*, Q73A=1) - P_sample(J3_NATIVE_Q86ABC=c | R*, Q73A=0)`

Requested design posture:

`NONE__EXPLICIT_UNWEIGHTED_SAMPLE_DESCRIPTIVE_TARGET`

Interpretation ceiling:

- pooled admitted sample description only;
- no population generalization;
- no causal effect;
- no survey-design standard errors implied;
- raw counts/denominators reported with proportions.

FFP004 authority slots remain open:

`ESTIMAND_AUTHORITY_PENDING_EXACT_CANARY`

`WEIGHT_DESIGN_AUTHORITY_PENDING_EXACT_CANARY`

No weight is silently activated. A weighted population target would be a separate pre-fork common-input variant.

## N. TTAR / semantic-transform boundary

No TTAR is triggered by keeping native Q70B/Q70C 0/1 states, native Q73A 0/1 contrast, native Q76/Q86 states, country-qualified native Q84 categories, or exact Q86ABC tuple products.

Typed transform/equivalence authority is required before any state collapse, ordinal-to-continuous reinterpretation, Q84 cross-country category equivalence, Q93C continuous conversion, special-state merge, or cross-wave/source transport.

## O. Representation firewall

Claim-constitutive before the fork:

- exact source/country scope;
- respondent/risk-set identity;
- exposure/coexposure;
- four PRA-admitted active-position rows;
- Q73A contrast;
- eight PRA-admitted dispositions;
- state/special-state identities;
- estimand/weight-design authority;
- any triggered typed transforms;
- position/disposition ancestry separation.

Representation-local choices may not alter these facts.

Geometry, graph layout, latent class count, clustering, dimensionality, axis orientation, and display ordering do not become claim semantics.

## P. Exact FFC002 question

For target-use:

`FFR2_R5_Q03_Q73A_CONDITIONAL_DISPOSITION_REDISTRIBUTION_CANARY@1`

within source/country/risk-set scope above, adjudicate only:

1. whether Q70B may function as `ACTIVE_POSITION` within its household-benefit ceiling;
2. whether Q70C may function as `ACTIVE_POSITION` within its old-age social-grant ceiling;
3. whether Q73A may function as `ACTIVE_POSITION` and native 0-vs-1 as the bounded Q03 contrast;
4. whether country-qualified Q84 may function as `ACTIVE_POSITION` within its relational-identity ceiling;
5. whether these four accepted rows instantiate at least three authorized analytic-role families without creating a global ontology;
6. whether Q93C remains `SUPPLEMENTARY` for the bounded sensitivity use;
7. whether Q76A/B and Q86A-F may function as `ACTIVE_DISPOSITION`, with Q86A-F bound by `ATTITUDE_OR_DISPOSITION_ONLY`.

The court may accept, narrow, reclassify, or reject exact rows. It may not generalize beyond this target-use without a new act.

## Q. Required downstream receipts before FFX002 execution

1. dispositive FFC002 PRA receipt for this exact docket;
2. authoritative current R5 respondent execution binding proving actual exposure/coexposure and response attachment for this revised scope;
3. competent estimand/weight-design binding;
4. competent CIM freeze consuming the final operands/receipts;
5. common semantic input manifest and hash;
6. FFX002 holdout/support/experiment receipts;
7. CITC materiality/tolerance authority before thresholded cross-view invariance judgments.

None is minted here.

## R. Allowed-use ceiling

This packet does not authorize:

- Q73D or `RESPONDENT_HAS_PAID_EMPLOYMENT` use;
- a global Afrobarometer position ontology;
- STRATA;
- class membership;
- capital volume;
- field position;
- pressure/hegemony/homology;
- causal inference;
- Q86-as-position;
- missingness-as-exposure;
- source-presence-as-exposure;
- ungoverned transforms;
- weighted population inference;
- cross-wave/source transport.

Terminal token:

`Q73D_FREE_CANARY_SELECTED__EXACT_CLAIM_SCOPE_READY_FOR_PRA`
