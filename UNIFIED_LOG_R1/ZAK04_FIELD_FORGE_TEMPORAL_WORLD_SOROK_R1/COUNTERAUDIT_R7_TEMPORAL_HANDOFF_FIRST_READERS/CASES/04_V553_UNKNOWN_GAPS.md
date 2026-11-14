# R7 04 V553 UNKNOWN GAPS — RECOVERED_ABSENCE_INVARIANT

**Historical owner cross-reference:** `G1A-FUNC-016`; **domain:** F7. This is a documentary edge, NOT a newly assigned original T. Immutable historical source [`data/ddm_build_copy/ddm_v553_temporal_pressure.py`](https://github.com/maidiu/rawlsing/blob/25830fe7462bb9e29bc4087e6ae14f3f84cec377/data/ddm_build_copy/ddm_v553_temporal_pressure.py) at commit `25830fe7462bb9e29bc4087e6ae14f3f84cec377`, Git blob `5304b70f9f6522c5ae3893eff215c1d445681983`, source line(s) 2675-2947.

**Input/authority/grain:** Observation anchors and explicit missing years

**Exact calculation or selection branch:** For authorized sparse key, record unknown_gap_preserved, interpolation_method=none; main field keeps pressure_level=None in unobserved years

**Produced knowledge or artifact:** Sparse temporal field with typed unknown_gap and no interpolation permission

**Positive:** Observed authorized anchors may be admitted

**Negative/refusal:** Missing-year inference forbidden independent of optional legacy interpolation flag

**Observed first reader:** _build_v553_v554_handoff_index

**Earliest unproved or severed causal/consumer edge:** Legacy heuristic interpolated table can coexist with authoritative unknown-gap field; they must not be merged

**Discriminating original/modern/negative test:** Source-false midpoint year must remain unknown in authoritative field even if --allow-interpolation used

**Grade:** source inspected S1; no native Python invocation, no original empirical source realization, no replay of these inputs/outputs, no source-qualified modern actor. A code-level status mismatch is a testable defect hypothesis, not an observed runtime incident.
