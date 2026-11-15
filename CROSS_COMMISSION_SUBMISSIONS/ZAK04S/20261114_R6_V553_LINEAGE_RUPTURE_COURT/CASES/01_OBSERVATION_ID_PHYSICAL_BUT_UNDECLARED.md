# OBSERVATION_ID_PHYSICAL_BUT_UNDECLARED

**Provenance:** `data/ddm_build_copy/ddm_v553_temporal_pressure.py` at 6a5c12f04323d74001f9632063ec907f4fc4468e; Git blob 5304b70f9f6522c5ae3893eff215c1d445681983, lines 2466-2595.
**Jurisdiction:** V553_TEMPORAL_OBSERVATION. This is a mechanism/reader case, NOT a newly counted original historical T.

### Original functional requirement and exact input
Input source-qualified resolved temporal key and each wave with V552/V552J structural fact IDs and authorized pressure or probe mode.

### Actual operation
Creates observation_id=v553_obs_{key}_{wave}, preserved in an unprojected pd.DataFrame(rows); writer persists physical columns.

### Output and semantic meaning
Physical observation records can contain observation_id; named required-column schema does not guarantee it.

### False inference or negative behavior
Missing source/permission remains probe/blocked; do not claim observation_id was actually dropped.

### Actual first reader or missing consuming edge
Actual next consumer `_build_v553_cross_wave_delta_index` receives observation_df; its own delta rows do not carry from/to observation IDs.

### Finding and conservation boundary
`EXISTING_OBSERVATION_ID_PHYSICALLY_PRESERVED__CONTRACT_NOT_REQUIRED`. Corrects tempting but false claim that both obs/delta IDs are erased; only delta is projected out.

### Source identities
R6:EV:01;R6:EV:02;R6:EV:03;R6:EV:12

**Execution:** No R6 tests, CI, harness, native historical producer replay, agent, code or branch-engineering changes.
