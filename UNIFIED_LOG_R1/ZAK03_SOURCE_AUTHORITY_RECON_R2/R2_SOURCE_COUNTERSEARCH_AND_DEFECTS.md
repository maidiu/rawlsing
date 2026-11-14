# ZAK-03 R2 — source-search and opponent-reference audit

## Verified location-and-meaning findings

| Item | Expected / first lookup | Broad search / recovered source | Truthful grade |
|---|---|---|---|
| B49 selector `select_source_rules` | Protected `rawlsing_next/pre553_inherited_source_rules.py` missing at expected ref | Same file path **alternate commit** `b5600da96358f8526471d635a1befa8daa3f098b`, blob `5f6efaceb18d92a362d065d12fdca4076d53fa16`, line 409; follow S01 roadmap creation clue | FOUND_CANDIDATE; NOT_PROVED_PROTECTED |
| R157 C11 config factory | Not found at old expected adoption point | `rawlsing_next/source_configuration/factory.py@d81bc2c67baf933461ae6cfca468f24779cc7e44#3f31f20e70a1ddd7c3880d21ecfaa6870b0c699a`, line 516 | FOUND_CANDIDATE; CURRENT_SELECTED_ADOPTION_UNPROVED |
| V550 position composition | Missing from opponent's 11 T entries | `data/ddm_build_copy/ddm_v550_position_distribution.py@9253064bc9423a0f0ccda4fbdea43c2f54f800c6#651329254244e9f42a8d88c2721ccae6bd768073`, lines 12–132 | NEW ORIGINAL T0012; S1 CODE |
| V550 relation co-signature | Missing from opponent's 11 T entries | `data/ddm_build_copy/ddm_v550_clouds.py@9253064bc9423a0f0ccda4fbdea43c2f54f800c6#dfc878e87d984a1a3d7000a0c726bdc444f9945f`, lines 327–353,924–1011 | NEW ORIGINAL T0013; S1 CODE |
| V550 attitude co-travel | Missing from opponent's 11 T entries | Same `ddm_v550_clouds.py` blob, lines 671–811,1014–1041 | NEW ORIGINAL T0014; S1 CODE |
| V552 conditional reader | Previous report describes V551 conditional output, real V552 handoff unclear | `data/ddm_build_copy/ddm_v552_structural.py@9253064bc9423a0f0ccda4fbdea43c2f54f800c6#0df56d70cb3880dee723df00aea2207acd525260`, lines 253–259 | PARAMETER_PRESENT_UNUSED; NOT global absence |

## Precise correction to an inherited interpretive finding

The V550 `position_distribution` producer outputs `position_field,position_value,n_unweighted,n_weighted,pct_unweighted,pct_weighted,weight_status` with denominator equal to all nonblank respondent values for that **position field**. It does **not** output question, response, `P(response|position)`, or response-conditional denominator. The prior N006 analysis's imputation of response-conditional meaning is not supported **for this source table**. `position_indicator_summary` remains a separate named possible source; a negative search has NOT been established for it. This is semantic precision, not source/structural authority issuance.

## R1 referential-integrity corrections

- Missing data shapes: `SHAPE:UNIVERSE`, `SHAPE:NATIVE_PACKAGE` — R2 ZIP registers source-graded dictionary meanings.
- Dangling modern OP aliases (full `ZAK03:OP:` prefix): `M09:0007`, `M08:0007`, `M11:0010`, `M09:0011` — R2 ZIP adds qualified source-related-only current operation records; those **do not** assert T-specific old semantic effects.
- Literal `NO_PROVED_CURRENT_MATCH` in operation identifier columns (2 rows) — R2 ZIP leaves the corresponding link empty and preserves the explicit absence of proof in its difference field.
- Narrative labels and `NONE` in `COVERAGE.found_operation_ids` — moved to `qualification` or replaced with blank, not upgraded to formal OP IDs.
- Documentary join QA after repairs: **0** unresolved references in checked `OPERATION_TRACES` shape IDs, `MECHANISM_RECONCILIATION` operation IDs, `COVERAGE` operation/evidence/search IDs. This is not substantive implementation validation.

## Unsearched corpus and exact next search clues

`V540–V548` ordinary/J and predecessor origins, `PRE_VOZHD`, `VERKHOVOD`, most `DVA`, `TRII`, `CHETIRI` and `LONG_MEMORY` T×domain searches remain incomplete. Candidate clues include `vozhd_trii/20260820_pre553_empirical_compiler_activation`, `vozhd_dva/20260817_downstream_completion`, `W44_CHETIRI_INHERITANCE/CAMPAIGN_MAP.md`, N006 TRII substrate archive, Authority39/40, `recovery_integration/semantic_relation_R1_through_Job3` and the R1 `SOURCE_SEARCH_LOG.tsv`. No global `NOT_FOUND` or same-grain conservation inference from these open regions.

**Boundaries:** No source rights, original35 production selection, current non-test first reader, FF/Sorok actor science, new execution, independent receiving or protected adoption asserted.
