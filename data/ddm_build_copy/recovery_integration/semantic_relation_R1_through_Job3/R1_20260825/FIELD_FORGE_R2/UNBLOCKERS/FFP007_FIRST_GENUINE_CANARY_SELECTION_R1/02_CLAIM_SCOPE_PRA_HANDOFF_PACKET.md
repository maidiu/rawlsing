# FFP007 — EXACT CLAIM-SCOPE / PRA HANDOFF PACKET

Packet status:

`READY_FOR_BOUNDED_PRA_ADJUDICATION__NOT_A_PRA_RECEIPT__NOT_A_FROZEN_CIM`

This packet supplies the exact missing premise identified by FFP003 for a bounded first-canary PRA court: immutable candidate target-use identity, intended operation, source/country/respondent-risk-set scope, and allowed-use boundary.

## A. Immutable source scope

- source family: `Afrobarometer`
- wave: `R5`
- exact source path: `Data/Afro Barometer Round 5.sav`
- exact source SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`
- exact source byte size: `49,689,458`
- evidenced source rows: `51,587`
- exact dataset identity: `Afrobarometer_Round_5_Afro_Barometer_Round_5`
- exact source-codebook identity: `merged_r5_codebook_2.pdf`
- exact codebook SHA-256: `7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735`
- current routing carrier used for selection: `C04_FULL_CURRENT_ROUTING_LEDGER.csv`
- routing carrier SHA-256: `c3148341c5a6315c4b060f665595c93c4aa935dfc171aa5faf4c14628f914f90`

No source acquisition or source-byte substitution is authorized by this packet.

## B. Candidate target-use / intended operation

Candidate target-use identity:

`FFR2_R5_Q03_Q73D_CONDITIONAL_DISPOSITION_REDISTRIBUTION_CANARY@1`

Intended operation:

1. define an exact positively exposed respondent risk set from already-governed R5 source/qimpl routing plus an authoritative current respondent execution binding;
2. retain four PRA-accepted position operands at native source state identity;
3. use native `Q73D=0` versus `Q73D=1` as the bounded Q03 contrast among respondents for whom Q73D was lawfully exposed under its paid-employment predicate;
4. compare native disposition-state distributions for `Q76A,Q76B,Q86A-Q86F` across that contrast;
5. optionally compare the native order-3 Q86 configuration `J3_NATIVE_Q86ABC` if and only if executable same-respondent exposure is positively materialized;
6. expose the exact same common semantic input to each FFX002-R2 view.

The intended operation is descriptive comparison, not causal estimation and not a structural-semantic admission.

## C. Exact candidate respondent risk-set scope

Country scope candidate:

`COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN,SWZ}`

The additional Q73D eligibility condition remains exact and narrower:

`COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN} AND RESPONDENT_HAS_PAID_EMPLOYMENT == True`

under:

- qimpl `question_impl.phase0.391123a4e7d3c8f0fd3b`
- predicate `C04P.f751f53c113a339f2cb8`.

Final respondent risk set `R*` must be materialized only from an authoritative `CURRENT_RESPONDENT_EXECUTION_BINDING_CONTRACT@1` or successor authority that binds:

- exact current R5 respondent identity;
- exact qimpl -> empirical measurement identity;
- exact predicate inputs;
- deterministic predicate result;
- governed exposure state;
- independent response binding;
- source/currentness ancestry.

Forbidden:

`response missingness -> nonexposure`

`source presence -> exposure`

`J candidacy -> executable same-respondent J`

Until that binding is authoritative, this packet authorizes **no execution**.

## D. PRA docket

### D1. Proposed core position rows

| source variable | exact qimpl | candidate role | candidate role family | requested bounded use |
|---|---|---|---|---|
| Q70B | `question_impl.phase0.311d905b2baab867642e` | `ACTIVE_POSITION` | `HOUSEHOLD_SOCIAL_PROTECTION_MATERIAL_RELATION` | native household government school-feeding receipt coordinate |
| Q73A | `question_impl.phase0.cae005624221d7b00dd2` | `ACTIVE_POSITION` | `FISCAL_INCORPORATION_OBLIGATION_RELATION` | native sales/VAT obligation coordinate |
| Q73D | `question_impl.phase0.391123a4e7d3c8f0fd3b` | `ACTIVE_POSITION` | `EMPLOYMENT_LINKED_FISCAL_RELATION` | native paid-employment income-tax obligation coordinate and exact Q03 0-vs-1 contrast |
| Q84 | `question_impl.phase0.5a05ce882452ef85debd` | `ACTIVE_POSITION` | `RELATIONAL_IDENTITY_BACKGROUND_POSITION` | respondent's native ethnic/cultural/tribal affiliation coordinate; no harmonization |

These are nominations only. The PRA court may accept, narrow, reclassify to supplementary/conditioning/exclude, or reject each exact row. It may not generalize its ruling beyond this claim scope without a new act.

### D2. Proposed position-side sensitivity row

| source variable | exact qimpl | candidate role | requested bounded use |
|---|---|---|---|
| Q93C | `question_impl.phase0.f62bceafa49dd85eb525` | `SUPPLEMENTARY` | digital-financial-practice sensitivity / conditioning; native 0-4 order preserved |

Q93C must not be treated as wealth/class/capital/income merely because it concerns mobile money/bill payment.

### D3. Proposed disposition rows

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

Requested bounded role: `ACTIVE_DISPOSITION`.

FFP003 ceiling is incorporated verbatim in effect: Q86A-F are `ATTITUDE_OR_DISPOSITION_ONLY`; attributes of each hypothetical citizenship subject may not become respondent social-position facts.

## E. Position/disposition ancestry separation requirement

The claim requires exact source ancestry separation between the position-side operands and active disposition measurements.

Candidate source blocks:

- position: Q70 / Q73 / Q84;
- position-side sensitivity: Q93;
- disposition: Q76 / Q86.

No active disposition item is used to construct a position operand in this packet. No position operand is used to construct an active disposition state. Any later derived variable that crosses that boundary must fail closed pending explicit ancestry review.

## F. Disposition batteries and higher-order object

### Battery 1

`Q76A,Q76B`

Source semantics: respondent normative judgments of nonpayment behavior; native 1-3 states.

### Battery 2

Exact source structure:

`cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4`

- type: `MATRIX_GRID`
- native label: `Explicit source block Q86`
- members: `Q86A|Q86B|Q86C|Q86D|Q86E|Q86F`
- exact current member binding: complete
- source-level disposition: `CURRENT_J_CANDIDATE`

Lawful order>=3 candidate:

`J3_NATIVE_Q86ABC := (Q86A,Q86B,Q86C)`

No binary recode is required because the substantive Q86 native states are already 0/1. Non-substantive states remain separately typed. The eight possible substantive tuples are source-state products only; a tuple may be counted empirically only for respondents whose same-respondent exposure to all three members is positively proved.

## G. Candidate estimand binding

Candidate estimand:

`UNWEIGHTED_SAMPLE_DESCRIPTIVE_CONDITIONAL_STATE_REDISTRIBUTION@1`

Primary family:

`Delta_D(s) = P_sample(D=s | R*, Q73D=1) - P_sample(D=s | R*, Q73D=0)`

for every active disposition `D` and each preserved native state `s`.

Supplementary J3 family:

`Delta_J3(c) = P_sample(J3_NATIVE_Q86ABC=c | R*, Q73D=1) - P_sample(J3_NATIVE_Q86ABC=c | R*, Q73D=0)`

for each positively observed native substantive tuple `c`, only after executable J authority is established.

Interpretation ceiling:

- unweighted sample description only;
- no causal effect;
- no population generalization;
- no latent social geometry is part of claim identity;
- no graph/layout/class/field interpretation is constitutive.

## H. Weight/design posture

For the first canary candidate, the requested estimand uses **no survey weight**.

This is an explicit FFX002-R2-compatible unweighted sample-descriptive variant, not omission-by-accident.

The PRA/claim court should bind:

`WEIGHT_POSTURE = NONE__EXPLICIT_UNWEIGHTED_SAMPLE_DESCRIPTIVE_TARGET`

If a weighted target is later commissioned, it must be a separate pre-fork estimand/common-input variant with exact governed weight and design authority. It may not silently replace this estimand.

## I. TTAR points

No TTAR is needed for:

- native Q73D 0-vs-1 contrast;
- native Q76 states;
- native Q86 0/1 states;
- exact Q86ABC tuple construction after exposure proof.

TTAR or equivalent typed transform authority **would** be required before:

- collapsing Q76 states;
- treating Q76 native order as continuous distance;
- collapsing/harmonizing Q84 categories;
- cross-country equivalence claims over Q84 category labels;
- collapsing Q93C frequency states;
- converting Q93C to continuous intensity;
- merging non-substantive states;
- transporting this claim across waves/sources.

## J. Representation choices explicitly outside claim identity

The following remain nonconstitutive unless a later competent court says otherwise:

- graph layout;
- dimensionality-reduction algorithm;
- latent class count;
- clustering algorithm;
- visualization geometry;
- node ordering;
- axis orientation;
- label placement;
- method-local supplementary passivation that preserves semantic identity and common-input law.

No representation may redefine the respondent risk set, source state identity, Q03 contrast, estimand, or PRA role.

## K. Exact allowed-use boundary for final PRA

A PRA receipt consuming this packet should be bounded to:

`FFR2_R5_Q03_Q73D_CONDITIONAL_DISPOSITION_REDISTRIBUTION_CANARY@1`

and authorize only the minimum role needed to ask:

> Whether the conditional distribution of the exact Q76/Q86 disposition states differs across the native Q73D 0-vs-1 paid-employment tax-obligation contrast within the positively governed common Afrobarometer R5 respondent exposure risk set, while the same claim-semantic inputs are rendered through the FFX002-R2 multiview experiment.

It must not authorize:

- a general Afrobarometer position ontology;
- STRATA;
- class membership;
- capital volumes;
- field position;
- pressure/hegemony/homology;
- causal interpretation;
- Q86-as-position;
- response missingness as exposure;
- ungoverned category transforms;
- weighted population inference;
- cross-wave/source transport.

## L. Required successor receipts before execution

1. bounded PRA receipt over the exact rows above;
2. authoritative current R5 respondent execution binding covering exact qimpl/predicate/exposure/response chain;
3. claim identity freeze by the competent CIM/claim-semantic court;
4. common semantic input manifest after all authority inputs are fixed;
5. holdout/experiment receipts required by FFX002-R2;
6. CITC materiality/tolerance authority before any cross-view invariance ruling that needs thresholds.

No item in this list is minted by FFP007.

Terminal handoff token:

`FIRST_CANARY_CANDIDATE_SELECTED__EXECUTION_NOT_YET_ADMITTED`
