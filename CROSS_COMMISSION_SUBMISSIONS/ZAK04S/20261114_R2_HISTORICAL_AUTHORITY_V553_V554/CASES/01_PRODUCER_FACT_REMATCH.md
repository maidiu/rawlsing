# Historical V552J semantic-score structural-fact resolution

**Alias:** ZAK02:T:0010_AS_UPSTREAM;G1A-FUNC-014 (NOT a new canonical T). **Shared seams:** XS:008;XS:009. **Kind:** S submechanism.

**Source:** [data/ddm_build_copy/ddm_v552j_handoff.py](https://github.com/maidiu/rawlsing/blob/25830fe7462bb9e29bc4087e6ae14f3f84cec377/data/ddm_build_copy/ddm_v552j_handoff.py#L69) @ 25830fe7462bb9e29bc4087e6ae14f3f84cec377 # 476e617370e8947ee1f38b0718243ecfc5ba9e5c, L69-96

**Input shape and risk set:** A V552J packet with run/source/wave/country-or-shard, an optional prejoined structural-fact ID, and a V552 structural-fact index with semantic fields.

**Transformation:** _packet_structural_dimension_resolution retains prejoined source ID but also scores candidate facts on relation-axis, target, driver and question, sorts matches and may report partial_structural_match resolved.

**Output and new knowledge:** A chosen source_v552_structural_fact_id and dimension/status/lineage fields; the selected ID may be a score-ranked candidate, not established issuer-bound.

**Meaningful negative/denial:** Same-scope fact with semantically similar fields but different source-binding should NOT replace an absent exact issuer association; code can choose it under enough score.

**Later rule/current comparison:** Historical TD-R00/SI-R00 explicitly requires exact governed producer association; later qualified implementation not established in this subcourt.

**First reader (observed static vs unproved actual effect):** V553 canonical harmonization and its key-building path are source-called; no selected modern science reader.

**Grade:** PINNED_SOURCE_CODE__CONTRADICTS_LATER_HISTORICAL_ARCHITECTURE; inspected code/issued historical rule, not an executed test or selected real source.

**Discriminating falsifier:** Use two same-scope competing facts and no producer-bound exact join; consumer must refuse descriptive rematch.

**Evidence rows:** R2:EV:01;R2:EV:03;R2:EV:05. **Outstanding authority:** qualified historical/source-science issuer; selected C11/FF/recipient when applicable; independent receiving; native world/actor owner for any claimed actor continuation.
