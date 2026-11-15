# V554_STANDALONE_COUNTRY_YEAR_READER

**Provenance:** data/ddm_build_copy/ddm_v554_seed_contract.py at 6a5c12f04323d74001f9632063ec907f4fc4468e; Git blob b11b73fc171f6b37976fa579d54700505a69f84c; lines 897-1000;229-315.
**Scope:** N9; original historic T inventory remains open and is not renumbered.

**Before/input:** V553 full run root with country-year heuristic parquet and optional year-indexed fallback.

**Actual transformation:** Prefer country-year table and feed DataFrame rows into regional year seed strength; no read of v553_temporal_pressure_field keyed values or authorized handoff.

**Output/knowledge:** Regional seed source_pressure_ids and scalar bounded pressure from heuristic point_estimate.

**Negative and protective behavior:** Status requires anchor_derived or linear_interpolated for positive/constrained; source writer defaults to anchor/ready/blocked/cautious.

**Exact first reader and grade:** V555 handoff index receives resulting V554 seeds, not original authorized temporal key.

**Conservation limit:** Standalone source cut may differ from thin orchestrated input selection.

**Evidence IDs:** R5:EV:05;R5:EV:09;R5:EV:10;R5:EV:11;R5:EV:24

**Machine IDs:** R5:OP:05:IN; R5:OP:05:OUT; R5:SH:05:OLD_IN/OLD_OUT/NEW_IN/NEW_OUT; R5:READER:05; R5:AUTH:05; R5:U:05.

**Disposition:** STATIC_STANDALONE_HEURISTIC_FIRST_READER. No new source execution, authority, merge or actor model.
