# Historical same-wave exact structural-pressure noncollapse

**Alias:** G1A-FUNC-016 (NOT a new canonical T). **Shared seams:** XS:009;XS:010. **Kind:** S submechanism.

**Source:** [data/ddm_build_copy/ddm_v553_temporal_pressure.py](https://github.com/maidiu/rawlsing/blob/25830fe7462bb9e29bc4087e6ae14f3f84cec377/data/ddm_build_copy/ddm_v553_temporal_pressure.py#L2159) @ 25830fe7462bb9e29bc4087e6ae14f3f84cec377 # 5304b70f9f6522c5ae3893eff215c1d445681983, L2159-2203;2336-2365

**Input shape and risk set:** One V553 wave/group containing multiple separately identified V552 structural fact rows and pressure_score values.

**Transformation:** _build_v553_temporal_key_tables groups and averages matching_fact_pressure.mean(); later key grouping computes structural_pressure_values.mean() and selects one primary fact ID.

**Output and new knowledge:** One numeric pressure value and singleton canonical source-fact field, with complete contributors relegated to diagnostic JSON.

**Meaningful negative/denial:** Two distinct source facts with 0.2 and 0.8 become a 0.5 aggregate; example is constructed reasoning, NOT_RUN. Disallow claim that this is preservation of two exact pressures.

**Later rule/current comparison:** Later accepted TD-R00 G18 and SI-R00 demand independently preserved exact simultaneous pressure identities, no averaging/winner/singleton substitution.

**First reader (observed static vs unproved actual effect):** V553 temporal observation/delta consumers inherit key-grained output; selected source-native FF/N9 reader still not proved.

**Grade:** PINNED_SOURCE_CODE__INFORMATION_COLLAPSE_RISK__NO_NATIVE_RUN; inspected code/issued historical rule, not an executed test or selected real source.

**Discriminating falsifier:** Two distinct measured same-wave V552 source facts under one group must remain separately resolvable, even with same semantic label.

**Evidence rows:** R2:EV:02;R2:EV:03;R2:EV:05. **Outstanding authority:** qualified historical/source-science issuer; selected C11/FF/recipient when applicable; independent receiving; native world/actor owner for any claimed actor continuation.
