# DELTA_ID_PROJECTED_AWAY

**Provenance:** `data/ddm_build_copy/ddm_v553_temporal_pressure.py` at 6a5c12f04323d74001f9632063ec907f4fc4468e; Git blob 5304b70f9f6522c5ae3893eff215c1d445681983, lines 2596-2676.
**Jurisdiction:** V553_TEMPORAL_RELATION. This is a mechanism/reader case, NOT a newly counted original historical T.

### Original functional requirement and exact input
At least two wave observations for same comparable_temporal_key, signed authorized or probe pressure and wave IDs.

### Actual operation
Appends delta_id based only on from/to wave IDs, then forces DataFrame rows through schema whose required_columns omit delta_id.

### Output and semantic meaning
Actual delta table still has temporal key, waves, signed differences and typed authorization—but loses the authored delta_id field.

### False inference or negative behavior
Same wave pair across two different pressure keys would ALSO collide on that ID if it were preserved; both defects require distinct future checks.

### Actual first reader or missing consuming edge
`_build_v553_temporal_pressure_field_contract` looks up delta_id and cannot recover it from this projected table.

### Finding and conservation boundary
`S1_DETERMINISTIC_PROJECTION_LOSS__NO_R6_RUN`. Do not claim whole delta content absent: temporal key and wave pair are still in table.

### Source identities
R6:EV:04;R6:EV:05;R6:EV:06;R6:EV:12

**Execution:** No R6 tests, CI, harness, native historical producer replay, agent, code or branch-engineering changes.
