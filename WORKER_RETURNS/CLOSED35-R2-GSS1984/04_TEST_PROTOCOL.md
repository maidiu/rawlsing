# CLOSED35-R2-GSS1984 — Future A/B/C Qualification Test Protocol

Status:

`TESTS_AUTHORED__NOT_EXECUTED`

This protocol is synthetic/source-independent at this commission stage.

No raw GSS1984 carrier was opened. No real-source processing, A/B/C execution, I05 run, or measured P2X occurred.

## Qualification invariant

Every candidate must consume the same frozen:

`GSS1984_SEMANTIC_OWNER_V1`

Candidate-local semantic interpretation is disallowed even if two candidates happen to produce equal values on one fixture.

Qualification order:

```text
canonical source identity
-> exact reader/config binding
-> R35 physical receipts at EC01+EC09+EC10+EC12+EC14
-> freeze GSS1984_SEMANTIC_OWNER_V1
-> synthetic source-specific rejection tests
-> candidate-neutral semantic digest comparison
```

A semantic pass cannot repair a failed physical receipt.

## T01 — Three-form collapse

Mutation:

collapse X/Y/Z into one undifferentiated form state or a two-form state.

Required result:

`REJECT`

Reason:

the accepted GSS1984 topology is three-form. The owner must preserve exact form identity where documentarily bound.

## T02 — Household slots converted to unordered set

Fixture:

four synthetic occurrences whose governed ranks are 1, 2, 10, and 14, including repeated equal values.

Mutation:

store only an unordered unique-value set.

Required result:

`REJECT`

Occurrence count, rank, and identity must survive even when values repeat.

## T03 — Physical adjacency used as household rank

Fixture physical order:

`where1, where10, where11, where12, where13, where14, where2, ...`

Mutation:

assign occurrence rank from physical ordinal adjacency.

Required result:

`REJECT`

Semantic rank must follow the governed slot identity, not lexicographic storage order.

## T04 — MAS / SAQ conflation

Mutation:

map MAS and SAQ to one module coordinate, or treat either as MAIN.

Required result:

`REJECT`

The accepted instrument set preserves MAIN, MAS, and SAQ as distinct identities.

## T05 — Module membership inferred from missingness

Fixture:

a variable cell is physically missing while exact module membership authority is unavailable.

Expected:

`BOUNDED_UNKNOWN__VARIABLE_MODULE_MEMBERSHIP_UNMAPPED`

Required rejection:

any candidate that infers MAS, SAQ, or MAIN membership from that missing cell.

## T06 — Longitudinal identity invention

Fixture:

two rows in different GSS releases expose the same native `id`.

Expected:

no respondent join.

Each row remains keyed by its own source SHA + row ordinal.

Required result for cross-release join:

`REJECT`

## T07 — Automatic survey-design semantics from carrier names

Fixture:

physical carriers named `VPSU` and `VSTRAT` are present.

No exact governed downstream estimand/variance-use authority is supplied.

Expected:

- preserve both carriers;
- analytical use state = `BOUNDED_UNKNOWN__WEIGHT_DESIGN_USE_UNMAPPED`;
- no variance estimator is silently selected.

Required result for automatic design activation:

`REJECT`

## T08 — FORMWT default invention

Fixture:

`FORMWT` is physically present.

No exact governed analytical intent/estimand binding is supplied.

Expected:

- preserve `FORMWT`;
- default analytical selector = none;
- weight-use state remains bounded UNKNOWN.

Required result for implicit `FORMWT` selection:

`REJECT`

## T09 — Routing inferred from missingness

Fixture:

target cell is SYSTEM_MISSING or user-missing/IAP while the exact variable×form/module route is unbound.

Expected:

`BOUNDED_UNKNOWN__ROUTING_APPLICABILITY_UNMAPPED`

Physical state remains independently preserved.

Required result if missingness becomes NOT_ASKED, SKIPPED, FORM_NOT_ADMINISTERED, or MODULE_NOT_ADMINISTERED:

`REJECT`

## T10 — Later/earlier GSS law leakage

Mutations include:

- import 1973 X/Y-only form law;
- import 1993 A/B/C ballot topology;
- import 2002 six-version routing;
- import 2010/2016 phase/mode law;
- import 2024 AmeriSpeak/GSS Next weight domains;
- import 1972 design negative admissions.

Required result:

`REJECT`

Only exact GSS1984 authority may fill a GSS1984 semantic field.

## T11 — Source SHA drift

Fixture:

same filename or same-looking metadata with any SHA other than:

`1da2df0c0e0692817081a46856deeaa6c78891101e53cf0139a971de16f7ac18`

Required result:

`REJECT__SOURCE_IDENTITY_DRIFT`

## T12 — Candidate-specific semantic divergence

Provide A/B/C with identical:

- canonical source identity;
- physically equivalent edge receipts;
- GSS1984 semantic owner;
- exact documentary bindings;
- declared analytical intent, if one is supplied.

Expected:

identical semantic projection.

Fail if any candidate differs on:

- form identity;
- module identity;
- occurrence rank;
- routing/applicability state;
- bounded UNKNOWN state;
- analytical weight/design authority;
- replay identity;
- longitudinal support state.

## T13 — Compound edge partial-pass laundering

Fixture:

candidate satisfies EC01, EC10, and EC12 but reorders EC09 household occurrences.

Expected:

overall GSS1984 qualification failure.

Likewise, a correct EC09 topology cannot excuse lost weight/design carriers or routing-carrier destruction.

EC14 requires simultaneous preservation.

## Required later evidence

The later A/B/C court must record:

- canonical SHA;
- reader/config identity;
- R35 I01 metadata receipt;
- R35 I02 parentage receipt for any derivative candidate;
- R35 I03 whole-source physical-equivalence receipt at all five edge classes;
- semantic owner identity;
- T01-T13 verdicts;
- candidate semantic digest;
- explicit bounded UNKNOWN states without forced resolution.

## Current execution boundary

`TESTS_AUTHORED__NOT_EXECUTED`

No browser claim in this return is a real-source test PASS.
