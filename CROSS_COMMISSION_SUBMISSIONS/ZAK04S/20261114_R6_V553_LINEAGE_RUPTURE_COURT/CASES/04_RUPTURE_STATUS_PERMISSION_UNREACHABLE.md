# RUPTURE_STATUS_PERMISSION_UNREACHABLE

**Provenance:** `data/ddm_build_copy/ddm_v553_temporal_pressure.py` at 6a5c12f04323d74001f9632063ec907f4fc4468e; Git blob 5304b70f9f6522c5ae3893eff215c1d445681983, lines 2635-2674;2806-2837.
**Jurisdiction:** V553_RUPTURE_CANDIDATE. This is a mechanism/reader case, NOT a newly counted original historical T.

### Original functional requirement and exact input
Upstream delta rows typed authorized_comparable if both anchors observed and authorized; otherwise probe_only.

### Actual operation
Rupture uses literal comparable rather than authorized_comparable to grant interpretation_permission; thus all self-produced candidates remain blocked even when structural deltas are authorized.

### Output and semantic meaning
Uninterpretable descriptive rupture-candidate rows; blocked_reason incorrectly says probe_only_temporal_field for an authorized_comparable input.

### False inference or negative behavior
This is positive-lane denial, NOT evidence of a bypass into positive native actor or event causation.

### Actual first reader or missing consuming edge
`_build_v553_structural_rupture_candidate_index` consumes delta_df; generated rupture packet is reported, not native objective event.

### Finding and conservation boundary
`STATIC_UNREACHABLE_POSITIVE_AT_EXACT_PRODUCER_PAIR`. Changing only the literal to permit would still violate missing governed rupture rule/version under accepted architecture.

### Source identities
R6:EV:07;R6:EV:08;R6:EV:09;R6:EV:12;R6:EV:15

**Execution:** No R6 tests, CI, harness, native historical producer replay, agent, code or branch-engineering changes.
