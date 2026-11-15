# V553_KEYED_AUTHORITATIVE_OBSERVATION

**Provenance:** data/ddm_build_copy/ddm_v553_temporal_pressure.py at 6a5c12f04323d74001f9632063ec907f4fc4468e; Git blob 5304b70f9f6522c5ae3893eff215c1d445681983; lines 2310-2660.
**Scope:** F7; original historic T inventory remains open and is not renumbered.

**Before/input:** V552J/source-qualified V552 fact IDs plus comparable multiwave key, wave/clock/scope and permission.

**Actual transformation:** V553 authorizes sparse per-key observed anchors independently from V552J probe; stores structural pressure and delta only where two qualified observations agree.

**Output/knowledge:** Observed_authorized_anchor values and cross-wave authorized delta; unknown gap remains unmeasured, not interpolated.

**Negative and protective behavior:** No eligible pair, missing fact lane, absent permission or unsupported wave => probe_only or blocked; never a fabricated authorized delta.

**Exact first reader and grade:** V553 temporal pressure field builder and exact v553_v554_handoff_index; V554 actual first VALUE reader not established.

**Conservation limit:** Historical R7 scoped original, not newly minted historical identity.

**Evidence IDs:** R5:EV:01;R5:EV:02;R5:EV:03;R5:EV:12;R5:EV:24

**Machine IDs:** R5:OP:01:IN; R5:OP:01:OUT; R5:SH:01:OLD_IN/OLD_OUT/NEW_IN/NEW_OUT; R5:READER:01; R5:AUTH:01; R5:U:01.

**Disposition:** AUTHORIZED_FIELD_PRODUCER_SOURCE_S1__REAL_RUN_OPEN. No new source execution, authority, merge or actor model.
