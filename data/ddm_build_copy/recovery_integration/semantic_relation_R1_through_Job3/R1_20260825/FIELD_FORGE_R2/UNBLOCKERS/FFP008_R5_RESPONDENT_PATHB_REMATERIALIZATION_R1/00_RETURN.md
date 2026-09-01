# FFP008 — R5 RESPONDENT PATH-B REMATERIALIZATION TERMINALIZATION R1

Status: `BLOCKED__EXACT_FINITE_PREDICATE_INPUT_BINDING_GAP`

Terminal ruling:

`BLOCKED__Q73D_RESPONDENT_HAS_PAID_EMPLOYMENT_INPUT_HAS_NO_EXACT_GOVERNED_R5_SOURCE_MEASUREMENT_BINDING`

## What passed

The immediately preceding FFP008 workspace was recovered and validated rather than expensively rerun. The exact already-governed source object is byte-identical to the commanded object: `Data/Afro Barometer Round 5.sav`, 49,689,458 bytes, SHA-256 `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`, 51,587 respondent rows.

Existing O08 source authority proves Afrobarometer R5 respondent grain as one adult citizen survey respondent with source key fields `(COUNTRY, RESPNO)`. The exact source contains 51,587 populated unique composite keys and zero duplicates. Row order is not identity.

The prior deterministic reconstruction script was recovered and revalidated locally; its exact SHA-256 is `ca0afd16475d9cabfbcac8b09ad68612c8ced680a3bb3051f9b1ea8a828ce774`. Two prior independent runs are byte-identical at root, inventory, member, and witness; their exact hashes are banked in `01_VALIDATED_PATH_B_EVIDENCE_AND_BLOCKER.json`. Those provisional artifacts are **not admitted CURRENT** because the script crosses the semantic gap described below.

## Exact blocker

Current C04 authority freezes Q73D as `question_impl.phase0.391123a4e7d3c8f0fd3b -> Afrobarometer:R5:Q73D -> C04P.f751f53c113a339f2cb8` with predicate:

`COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN} AND RESPONDENT_HAS_PAID_EMPLOYMENT == True`

C04's own preserved compiler constructs `RESPONDENT_HAS_PAID_EMPLOYMENT` from the source-native phrase **“has paid employment”**. It does not bind that abstract predicate symbol to Q96 or any other respondent measurement. FFX001-D requires that later respondent-input binding separately.

The recovered FFP008 script supplied the missing edge itself by treating Q96 values `2/3` (“Yes, part time/full time” to **“Do you have a job that pays a cash income?”**) as `RESPONDENT_HAS_PAID_EMPLOYMENT=True`. That equivalence is not already governed. It is materially nontrivial because the same native R5 source separately conditions Q73D on **paid employment / wages / employer** and Q73E on **self employment / earnings from your business or job**. Code is not competent to collapse those source distinctions.

The frozen provisional carrier also contains 4,819 rows with Q96 in `{2,3}` and source-native Q73D state `7 = Not applicable`. This is recorded only as hostile evidence against treating the Q96 mapping as self-proving; it is **not** used to infer exposure or nonexposure.

Therefore FFX001-D Gate C4 is not proved and Gates C5-C6 cannot lawfully mint a definite current exposure witness. The prior provisional witness is preserved as rejected evidence only.

## Smallest missing premise

> An exact governed respondent-level R5 source measurement or governed deterministic expression that owns `RESPONDENT_HAS_PAID_EMPLOYMENT` for Q73D.

No source reacquisition is required. No respondent-carrier rerun is required unless the finite input-binding adjudication changes the fields required in the carrier.

## Admission

`CURRENT_RESPONDENT_EXECUTION_BINDING_PACKAGE = NOT_ADMITTED`

`FFC001_ADMISSION = FAIL_CLOSED__ONE_FINITE_MISSING_PREDICATE_INPUT_BINDING`

No PRA, CIM, CITC, FFX002, source acquisition, row-order identity, or response-missingness inference was performed.
