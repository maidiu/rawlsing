# 20 V553 MODELLED VS R05 SNAPSHOT — F7 original-first mechanism analysis

Source identity: historical `25830fe7462bb9e29bc4087e6ae14f3f84cec377` blob `5304b70f9f6522c5ae3893eff215c1d445681983`; protected `6a5c12f04323d74001f9632063ec907f4fc4468e` blob `fdda8b2f887bd1fb7703bc5fb8ce1fefc52ca09d`. Historical ID or owner: `G1A-FUNC-016`. Case `R6:C:20_V553_MODELLED_VS_R05_SNAPSHOT` is a seam comparison only; **0 canonical historical T identities created**.

## Historical computation
[Historical function `_build_interpolated_pressure_rows L606;build_v553_temporal_pressure_field L3169`](https://github.com/maidiu/rawlsing/blob/25830fe7462bb9e29bc4087e6ae14f3f84cec377/data/ddm_build_copy/ddm_v553_temporal_pressure.py) — `data/ddm_build_copy/ddm_v553_temporal_pressure.py`.

**Inputs/denominator/source grain:** V552 signed pressure anchor years, V553 wave harmonization and rupture

**Transformation (what actually happens):** Model interpolated year intensity/uncertainty between observed anchors, with known absence

**Output and learned information:** V553 modelled and observed pressure rows and gaps

**Negative/admission rules:** No harmonization/rupture authority ⇒ nonpositive

**First selected or statically identified reader:** Historical V554 seed affordance reads temporal field

## Present operation
[Current function `_execute_p41_world L667;select_r05_world_view L819`](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/pre553_universal_world_binding.py) — `rawlsing_next/pre553_universal_world_binding.py`.

**Inputs/authority:** TEST_ONLY learned consumer + pinned world catalog valid_at/asof

**Transformation:** Select hard-coded synthetic T0/T1 snapshots and check P41 receipts

**Output:** R05 typed sourcefree world with temporal_changed; nonoperative native N9

**Negative/refusal:** Unobserved pair or same clocks/values refuses

**First bounded reader:** Actual sourcefree P41 first reader, actor_executions=0

## Differential verdict
**Unproved edge:** Fixed synthetic snapshots are not historical observed-wave pressure nor modelled V553 interpolation

**Decisive counterfactual/negative test:** Prove same-source observed first/second wave with issuer and actual as-of N9 plus negative

**Evidence grade:** S1 code-body and static read. No execution witness, no actual same-source source-to-N9-to-Sorok science, no parity certification. These interfaces have different source grains and cannot be called superseded without selected source-reader mechanism verification.
