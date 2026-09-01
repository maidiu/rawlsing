# FFP002 — WAVE-2 HANDOFF R1

## Handoff status

`WAVE2_RESPONDENT_EXECUTION = NOT_READY__ONE_BOUNDED_PATH_B_BLOCKER`

Do not reacquire source data. Do not resurrect `public.respondent_fact`, V542/DuckDB, current mutable Postgres relations, or R5 replay capital as current empirical truth by implication.

## Exact source basis

Use only this source object as the presently identified Path-B basis unless a later competent act supersedes it:

- family: `Afrobarometer`
- wave/release: `R5 / Round 5`
- source: `Data/Afro Barometer Round 5.sav`
- dataset identity: `Afrobarometer_Round_5_Afro_Barometer_Round_5`
- SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`
- bytes: `49,689,458`

No new source acquisition is indicated.

## What is already proved and must not be reopened

For FFX001-C's bounded witness:

- current qimpl: `question_impl.phase0.391123a4e7d3c8f0fd3b`;
- source family/wave/raw variable: `Afrobarometer / R5 / Q73D`;
- routing: `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY`;
- exact predicate: `C04P.f751f53c113a339f2cb8`;
- compiled predicate: `COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN} AND RESPONDENT_HAS_PAID_EMPLOYMENT == True`;
- Contract@2 already closes `CURRENT qimpl -> current source implementation -> exact routing disposition -> exact predicate specification`.

Therefore no routing, conversion, source-candidacy, or predicate-specification cleanup belongs in the respondent-carrier recovery act.

## What remains to be frozen before rematerialization

A successor must return one explicit deterministic reconstruction contract for the exact R5 source hash above containing, at minimum:

1. source respondent-record identity semantics;
2. stable respondent identity / join-key derivation independent of row order and mutable database-local IDs;
3. exact country/form/split/wave identity fields required to bind current routing scope to each respondent;
4. exact source-variable -> respondent-measurement expression for the selected qimpl witness (`Q73D` first);
5. exact source-variable/expression -> predicate-input bindings for `COUNTRY_ALPHA3` and `RESPONDENT_HAS_PAID_EMPLOYMENT`;
6. explicit missing/refusal/not-asked semantics sufficient to avoid inferring exposure from missingness or response presence;
7. deterministic cardinality/reconciliation expectations against the exact source input;
8. deterministic output schema and serialization sufficient for replay-stable hashing;
9. authority signatures/refs showing source selection and empirical identity/reconstruction competence at this exact scope;
10. an explicit ceiling that the recipe is re-expression only and may not clean routing/conversion, invent semantic IDs, or acquire data.

Only after that contract is frozen may a separate worker rematerialize the respondent carrier and report its immutable ref/version/SHA-256. Only after that output identity exists may FFC001 perform the actual bounded admission.

## First-broken arrows to close

Already closed:

`CURRENT_QIMPL -> CURRENT_SOURCE_IMPLEMENTATION -> ROUTING_DISPOSITION -> PREDICATE_SPECIFICATION`

Still open:

`CURRENT_SOURCE_IMPLEMENTATION -> CURRENT_RESPONDENT_CARRIER_MEASUREMENT`

`CURRENT_RESPONDENT_CARRIER_MEASUREMENT -> STABLE_RESPONDENT_KEY_AND_SCOPE`

`PREDICATE_FIELDS -> ACTUAL_GOVERNED_RESPONDENT_INPUT_VALUES`

`PREDICATE_EXECUTION -> ACTUAL_MEASUREMENT_EXPOSURE -> RESPONSE_STATE`

The first three are the bounded reconstruction/admission seam. The final exposure/response arrows remain downstream execution semantics and must not be inferred merely from carrier reconstruction.

## Finite next proposition

Commission one bounded worker, under FFC001 plus the competent empirical identity owner, to **freeze but not yet execute** the deterministic Path-B R5 source-to-respondent reconstruction contract above. Its output must be a recipe/identity contract, not respondent data.

If and only if that worker can prove source-native identity semantics and exact Q73D/predicate-input bindings from already-governed material, the following worker may rematerialize and hash the carrier. If it cannot, return that exact source-semantic/identity field as the new bounded blocker.
