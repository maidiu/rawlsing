# RUPTURE_DIRECTION_REVERSAL_NOT_A_REVERSAL

**Provenance:** `data/ddm_build_copy/ddm_v553_temporal_pressure.py` at 6a5c12f04323d74001f9632063ec907f4fc4468e; Git blob 5304b70f9f6522c5ae3893eff215c1d445681983, lines 2806-2837.
**Jurisdiction:** V553_RUPTURE_CANDIDATE. This is a mechanism/reader case, NOT a newly counted original historical T.

### Original functional requirement and exact input
One delta row with abs(delta_value)>=0.35 and delta_direction up OR down.

### Actual operation
Marks direction_reversal from its single delta; no prior delta, previous direction, series comparison, governed rule_id or rule_version read.

### Output and semantic meaning
Misnamed candidate signal for any qualifying one-step increase/decrease, not demonstrated change of direction across time.

### False inference or negative behavior
No event is asserted (external_event_claim_made=False); interpretation_permission is separately blocked by status mismatch.

### Actual first reader or missing consuming edge
Rupture index and semantic implementation report are the sole source-located consumers; do not promote as event or actor causality.

### Finding and conservation boundary
`S1_SEMANTIC_LABEL_OVERCLAIM__CANDIDATE_ONLY`. The original completion ruling requires rupture annotations disabled absent already governed deterministic rule.

### Source identities
R6:EV:07;R6:EV:08;R6:EV:12;R6:EV:15

**Execution:** No R6 tests, CI, harness, native historical producer replay, agent, code or branch-engineering changes.
