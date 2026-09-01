# FFP007 — FIRST GENUINE CANARY SELECTION + CLAIM-SCOPE BINDING PREPARATION R1

Status: `CANDIDATE_SELECTED__CLAIM_SCOPE_READY_FOR_BOUNDED_PRA__RESPONDENT_EXECUTION_ADMISSION_STILL_EXTERNAL`

Worker mode: bounded candidate-selection / claim-scope preparation only.

This worker does **not** issue PRA, freeze CIM, mint TTAR, set CITC materiality, admit a respondent carrier, infer exposure from missingness, or execute FFX002-R2.

## 1. Ruling

The smallest exact Afrobarometer R5 candidate substrate found that meets the **candidate-selection** form of the FFX002-R2 first-canary floor is:

### Proposed active-position candidates

1. `Q70B` — household receipt of government school-feeding support.
   - candidate role family: `HOUSEHOLD_SOCIAL_PROTECTION_MATERIAL_RELATION`
   - exact qimpl: `question_impl.phase0.311d905b2baab867642e`
2. `Q73A` — respondent/household-facing requirement to pay general sales tax / VAT on goods bought from shops or traders.
   - candidate role family: `FISCAL_INCORPORATION_OBLIGATION_RELATION`
   - exact qimpl: `question_impl.phase0.cae005624221d7b00dd2`
3. `Q73D` — paid-employment-linked requirement to pay employer-deducted income tax.
   - candidate role family: `EMPLOYMENT_LINKED_FISCAL_RELATION`
   - exact qimpl: `question_impl.phase0.391123a4e7d3c8f0fd3b`
4. `Q84` — respondent's own ethnic community / cultural group / tribe.
   - candidate role family: `RELATIONAL_IDENTITY_BACKGROUND_POSITION`
   - exact qimpl: `question_impl.phase0.5a05ce882452ef85debd`

These four candidates arise from three source blocks (`Q70`, `Q73`, `Q84`) and at least three materially different candidate role families. Position heterogeneity is therefore not supplied by one source block alone.

### Position-side sensitivity candidate

5. `Q93C` — respondent frequency of using a mobile phone to send/receive money or pay a bill.
   - candidate role: `SUPPLEMENTARY`
   - candidate family: `DIGITAL_FINANCIAL_PRACTICE_POSITION_SIDE_SENSITIVITY`
   - exact qimpl: `question_impl.phase0.f62bceafa49dd85eb525`
   - ceiling: this is not thereby wealth, class, capital volume, employment relation, or social hierarchy.

### Active-disposition candidates

Two source batteries provide exactly eight separately respondent-facing disposition measurements:

- Q76 battery:
  - `Q76A` — normative judgment of not paying for government services;
  - `Q76B` — normative judgment of not paying owed income taxes.
- Q86 citizenship-rights matrix:
  - `Q86A;Q86B;Q86C;Q86D;Q86E;Q86F`.

The Q86 items retain the exact FFP003 ceiling: `ATTITUDE_OR_DISPOSITION_ONLY`. None is a respondent social-position operand.

### Higher-order configuration

The exact current source structure

`cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4`

is a six-member `MATRIX_GRID` over `Q86A-F`, with complete exact current binding. The smallest lawful order>=3 source-native configuration candidate is:

`J3_NATIVE_Q86ABC := (Q86A,Q86B,Q86C)`

with no many-to-one state collapse and no inferred coexposure. Native substantive response states are preserved. Actual respondent-level J support remains downstream of the current respondent execution binding.

## 2. Exact source ancestry

All selected rows descend from:

- source family / wave: `Afrobarometer / R5`;
- exact source object: `Data/Afro Barometer Round 5.sav`;
- SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`;
- source bytes: `49,689,458`;
- evidenced source rows: `51,587`;
- dataset identity: `Afrobarometer_Round_5_Afro_Barometer_Round_5`;
- exact same-byte alias previously proved: `mergedr5data0.sav`.

Source semantics were checked against `merged_r5_codebook_2.pdf`, SHA-256 `7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735`.

Current routing authority was checked against `C04_FULL_CURRENT_ROUTING_LEDGER.csv`, SHA-256 `c3148341c5a6315c4b060f665595c93c4aa935dfc171aa5faf4c14628f914f90`.

Every selected qimpl row in `01_EXACT_CANARY_CANDIDATE_MATRIX.tsv` has `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY` at the exact current routing grain.

## 3. Common claim-scope candidate

The smallest conservative country scope common to all selected core operands and both disposition batteries is:

`Afrobarometer R5 respondents excluding COUNTRY_ALPHA3 IN {ALG, EGY, MRC, SUD, TUN, SWZ}`

This is a candidate claim scope, not respondent exposure proof.

Additional exact Q73D eligibility remains:

`COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN} AND RESPONDENT_HAS_PAID_EMPLOYMENT == True`

under predicate `C04P.f751f53c113a339f2cb8`.

The current respondent carrier must materialize the required predicate inputs and execute them deterministically. Blank or non-substantive responses are not routing evidence.

## 4. Exact Q03 bounded positional contrast candidate

Candidate Q03:

> Among lawfully exposed Afrobarometer R5 respondents in the common risk set who satisfy the governed Q73D paid-employment eligibility predicate, how do the native disposition-state distributions redistribute between respondents coded `Q73D=0` and respondents coded `Q73D=1`?

Native contrast only:

- `Q73D=0`: not required to pay employer-deducted income tax;
- `Q73D=1`: required to pay employer-deducted income tax.

Do **not** fold `7=Not applicable`, `9=Don't know`, `997=Not asked`, `998=Refused`, or `-1=Missing` into either contrast state.

Conditional targets:

- each of `Q76A,Q76B,Q86A-Q86F` at native state identity;
- supplementary higher-order target `J3_NATIVE_Q86ABC` if same-respondent exposure is positively established.

No causal effect, latent class, field, pressure, homology, or structural mechanism is asserted by Q03.

## 5. Candidate estimand and design posture

Candidate estimand identity:

`UNWEIGHTED_SAMPLE_DESCRIPTIVE_CONDITIONAL_STATE_REDISTRIBUTION@1`

For each disposition `D` and native substantive state `s`:

`Delta_D(s) = P_sample(D=s | R*, Q73D=1) - P_sample(D=s | R*, Q73D=0)`

where `R*` is the positively governed common respondent exposure risk set.

For the order-3 native Q86 configuration, if executable same-respondent J is admitted:

`Delta_J3(c) = P_sample(J3_NATIVE_Q86ABC=c | R*, Q73D=1) - P_sample(J3_NATIVE_Q86ABC=c | R*, Q73D=0)`

This is explicitly:

- sample-descriptive;
- unweighted;
- noncausal;
- not a population target;
- not a substitute for a separately governed weighted estimand.

`WITHINWT` or any other weight is **not** silently activated here. FFX002-R2 permits an explicit unweighted sample-descriptive target; if a governed weighted target is later desired it must be registered as a separate pre-fork estimand/common-input variant with exact weight/design authority.

Report raw denominators/state counts alongside proportions. Non-substantive states must remain typed and visible rather than being used to infer exposure.

## 6. FFX002-R2 floor crosswalk

| Floor requirement | FFP007 candidate ruling |
|---|---|
| >=4 ACTIVE_POSITION candidates | `PASS_CANDIDATE__PRA_PENDING` — Q70B, Q73A, Q73D, Q84 |
| >=3 independently supportable position-role families | `PASS_CANDIDATE__PRA_PENDING` — social-protection/material; fiscal-incorporation/employment-fiscal; relational identity |
| no single source block as sole position heterogeneity | `PASS` — Q70, Q73, Q84 |
| >=1 position sensitivity candidate | `PASS_CANDIDATE` — Q93C supplementary |
| >=8 respondent-facing dispositions | `PASS_SOURCE_SEMANTIC` — Q76A/B + Q86A-F |
| >=2 disposition blocks/batteries | `PASS_SOURCE_SEMANTIC` — Q76 and Q86 |
| lawful order>=3 higher-order subset | `PASS_SOURCE_STRUCTURE_CANDIDATE` — native Q86 ABC matrix subset; executable respondent J still pending |
| exact Q03 contrast -> conditional redistribution | `PASS_CANDIDATE` — Q73D 0 vs 1 -> Q76/Q86 state distributions |
| estimand + weight/design posture | `PASS_CANDIDATE` — explicit unweighted sample-descriptive target; weighted target remains separate authority path |
| current respondent execution | `EXTERNAL_DEPENDENCY_NOT_CLOSED_BY_FFP007` |
| PRA | `NOT_ISSUED__HANDOFF_READY` |
| CIM | `NOT_FROZEN` |

Therefore the mandated rejection token is **not** returned at this preparation grain. The source/qimpl substrate is sufficient to hand to the bounded PRA/claim-scope court, but FFX002 execution remains prohibited until respondent execution and PRA dependencies are positively closed.

## 7. Exact remaining authority boundaries

### PRA

FFP007 only nominates roles. Final role status must be issued by the competent bounded PRA court. No `ACTIVE_POSITION` or `ACTIVE_DISPOSITION` status in this package is authoritative until that court accepts the exact claim scope and allowed-use boundary.

### Respondent execution

FFP002 did not itself establish a current respondent carrier/execution binding. This package therefore depends externally on an authoritative instantiation of:

`CURRENT_RESPONDENT_EXECUTION_BINDING_CONTRACT@1`

covering this exact R5 source, respondent identity, qimpl-to-measurement binding, predicate inputs/results, exposure states, and response binding.

### CIM

The proposition in this package is a candidate claim-scope binding only. FFP007 does not freeze claim identity.

### TTAR

No TTAR is required for the proposed Q73D 0-vs-1 contrast or for preserving native Q76/Q86 states. Any category collapse, ordinal-to-continuous reinterpretation, cross-item equivalence, or cross-context transport would require separate typed authority before fork.

### Materiality

No thresholds/tolerances are set. That remains CITC jurisdiction.

## 8. Targeted Library use

Repository/known-commit evidence was used first. Targeted Library retrieval was limited to:

- exact R5 codebook wording/value semantics;
- exact current C04 routing rows absent from the commanded starting tree;
- exact current source-structure/J-candidate row needed to pin the Q86 structure identity.

No broad project archaeology was used to create roles or relax the FFX002-R2 floor.

## 9. Handoff

The exact claim-scope/PRA handoff packet is:

`02_CLAIM_SCOPE_PRA_HANDOFF_PACKET.md`

Terminal worker state:

`CANDIDATE_SELECTED__CLAIM_SCOPE_READY_FOR_BOUNDED_PRA__RESPONDENT_EXECUTION_ADMISSION_STILL_EXTERNAL`
