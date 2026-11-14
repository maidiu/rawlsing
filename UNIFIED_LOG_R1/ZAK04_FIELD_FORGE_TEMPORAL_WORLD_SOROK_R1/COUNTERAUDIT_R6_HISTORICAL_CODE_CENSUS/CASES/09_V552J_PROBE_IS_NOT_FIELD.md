# 09 V552J PROBE IS NOT FIELD — F7 original-first mechanism analysis

Source identity: historical `25830fe7462bb9e29bc4087e6ae14f3f84cec377` blob `a3e6bf17386b58beb0c14b2d79d9e4a9e405c300`; protected `6a5c12f04323d74001f9632063ec907f4fc4468e` blob `e8bd6376720a2de132b384e7771d71d8d39cf261`. Historical ID or owner: `G1A-FUNC-014 / G1A-FUNC-016`. Case `R6:C:09_V552J_PROBE_IS_NOT_FIELD` is a seam comparison only; **0 canonical historical T identities created**.

## Historical computation
[Historical function `_v553_compatibility_frame L140;compile_v552j_run L151`](https://github.com/maidiu/rawlsing/blob/25830fe7462bb9e29bc4087e6ae14f3f84cec377/data/ddm_build_copy/compile_v552j_structural_handoff.py) — `data/ddm_build_copy/compile_v552j_structural_handoff.py`.

**Inputs/denominator/source grain:** V552J exact observed join with certified producer scope

**Transformation (what actually happens):** Emits ready_for_v553_probe but temporal_field_allowed=False and v553_temporal_field_row_count=0

**Output and learned information:** V553 single-wave probe index, not temporal field row

**Negative/admission rules:** Even ALLOW join does not grant temporal field

**First selected or statically identified reader:** V553 canonical inspector validates zero temporal field count

## Present operation
[Current function `_temporal_gate L249`](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/m1_temporal_v554_admission_dedup.py) — `rawlsing_next/m1_temporal_v554_admission_dedup.py`.

**Inputs/authority:** M1 temporal basis with signalled completeness

**Transformation:** Gates basis; no automatic observed-wave temporal field

**Output:** M1 temporal decision, not V552J temporally estimated pressure

**Negative/refusal:** Missing temporal basis refuses

**First bounded reader:** M2 basis reader

## Differential verdict
**Unproved edge:** High priority negative: V552J permission is probe-only; temporal field remained absent intentionally

**Decisive counterfactual/negative test:** Hostile mutate temporal_field_allowed True without issuer; original handoff integrity must fail

**Evidence grade:** S1 code-body and static read. No execution witness, no actual same-source source-to-N9-to-Sorok science, no parity certification. These interfaces have different source grains and cannot be called superseded without selected source-reader mechanism verification.
