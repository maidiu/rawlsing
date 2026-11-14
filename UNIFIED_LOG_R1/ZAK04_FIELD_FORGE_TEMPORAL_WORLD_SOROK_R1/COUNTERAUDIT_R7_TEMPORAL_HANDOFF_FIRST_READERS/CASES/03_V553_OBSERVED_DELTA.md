# R7 03 V553 OBSERVED DELTA — RECOVERED_POSITIVE_AND_NEGATIVE

**Historical owner cross-reference:** `G1A-FUNC-016`; **domain:** F7. This is a documentary edge, NOT a newly assigned original T. Immutable historical source [`data/ddm_build_copy/ddm_v553_temporal_pressure.py`](https://github.com/maidiu/rawlsing/blob/25830fe7462bb9e29bc4087e6ae14f3f84cec377/data/ddm_build_copy/ddm_v553_temporal_pressure.py) at commit `25830fe7462bb9e29bc4087e6ae14f3f84cec377`, Git blob `5304b70f9f6522c5ae3893eff215c1d445681983`, source line(s) 2432-2674.

**Input/authority/grain:** Per-wave authorized structural pressure and probe scores linked by comparable_temporal_key

**Exact calculation or selection branch:** Distinguish observed_authorized_anchor from probe_only_anchor; calculate authorized structural delta only when both source values exist; report comparability and use permission separately

**Produced knowledge or artifact:** Temporal observation and delta indexes with authorized vs probe types

**Positive:** Two authorized observed anchors yield authorized_comparable delta

**Negative/refusal:** Probe delta can be numeric but delta_interpretation_permission=False

**Observed first reader:** _build_v553_temporal_pressure_field_contract

**Earliest unproved or severed causal/consumer edge:** Crosswave scalar may exist for probe; do not upgrade it into source-qualified historical change

**Discriminating original/modern/negative test:** With one probe/nonpositive key confirm numeric delta is diagnostic and permission false

**Grade:** source inspected S1; no native Python invocation, no original empirical source realization, no replay of these inputs/outputs, no source-qualified modern actor. A code-level status mismatch is a testable defect hypothesis, not an observed runtime incident.
