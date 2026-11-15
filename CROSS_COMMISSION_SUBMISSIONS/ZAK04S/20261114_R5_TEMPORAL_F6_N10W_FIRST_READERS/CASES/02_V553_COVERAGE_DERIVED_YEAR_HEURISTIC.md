# V553_COVERAGE_DERIVED_YEAR_HEURISTIC

**Provenance:** data/ddm_build_copy/ddm_v553_temporal_pressure.py at 6a5c12f04323d74001f9632063ec907f4fc4468e; Git blob 5304b70f9f6522c5ae3893eff215c1d445681983; lines 446-606;1084-1202.
**Scope:** F7; original historic T inventory remains open and is not renumbered.

**Before/input:** V553 wave overlay certification counts and readiness/uncertainty dimensions, not signed per-key structural facts.

**Actual transformation:** Computes coverage ratio minus contradiction/absence/uncertainty penalties, then year and possible gap rows.

**Output/knowledge:** v553_year_indexed_pressure_over_time and v553_country_year_pressure_field numeric heuristic, pressure statuses ready/ready_with_gaps or anchor/cautious.

**Negative and protective behavior:** Missing waves or blocked comparability remains limited; lexical pressure label is not observed signed structural pressure.

**Exact first reader and grade:** V554 stand-alone seed builder and thin V5 fallback consume heuristic values.

**Conservation limit:** Do not confuse pressure_intensity with source-keyed authorized_structural_pressure_value.

**Evidence IDs:** R5:EV:04;R5:EV:05;R5:EV:09;R5:EV:24

**Machine IDs:** R5:OP:02:IN; R5:OP:02:OUT; R5:SH:02:OLD_IN/OLD_OUT/NEW_IN/NEW_OUT; R5:READER:02; R5:AUTH:02; R5:U:02.

**Disposition:** HEURISTIC_PRODUCER_SOURCE_S1__NOT_AUTHORIZED_TEMPORAL_EQUIVALENCE. No new source execution, authority, merge or actor model.
