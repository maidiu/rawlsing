# V554 legacy country-year data versus canonical keyed V553 handoff

**Alias:** G1A-FUNC-017 (NOT a new canonical T). **Shared seams:** XS:010. **Kind:** S submechanism.

**Source:** [data/ddm_build_copy/ddm_v554_seed_contract.py](https://github.com/maidiu/rawlsing/blob/25830fe7462bb9e29bc4087e6ae14f3f84cec377/data/ddm_build_copy/ddm_v554_seed_contract.py#L229) @ 25830fe7462bb9e29bc4087e6ae14f3f84cec377 # b11b73fc171f6b37976fa579d54700505a69f84c, L229-302;897-985

**Input shape and risk set:** V553 country-year pressure projection, readiness/harmonization reports; no direct value-read of keyed v553_v554_handoff_index in inspected V554 builder.

**Transformation:** _build_seed_affordance_index converts aggregate point_estimate, confidence penalty, pressure_status and global readiness to hardcoded year/national seed strengths and statuses.

**Output and new knowledge:** Legacy synthetic regional and national seed rows; expects anchor_derived for positive regional seed, while matched V553 canonical country-year path emits ready/ready_with_gaps/anchor.

**Meaningful negative/denial:** Heuristic year score and global readiness must not stand in for authorized signed source-keyed sparse pressure; positive region status unreachable for this matched producer pair at code level.

**Later rule/current comparison:** TD-R00 P5 demands V554 exact consumption with all aggregate files absent; later TD-R01 V554 F1/F2/B1 replaces legacy scalar seed ontology architecturally, not proved physically.

**First reader (observed static vs unproved actual effect):** V555 old seed packet is existing historical source reader, not accepted exact V554 F1 consumer.

**Grade:** HISTORICAL_ACTUAL_READER_LOCATED__ACCEPTED_DESIGN_DIFF__NO_EXECUTION; inspected code/issued historical rule, not an executed test or selected real source.

**Discriminating falsifier:** Keep lawful exact sparse V553 facts/limits and remove aggregate field; prove target reader resolves F1 without illicit year-score fallback.

**Evidence rows:** R2:EV:04;R2:EV:07;R2:EV:08. **Outstanding authority:** qualified historical/source-science issuer; selected C11/FF/recipient when applicable; independent receiving; native world/actor owner for any claimed actor continuation.
