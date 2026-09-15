# N04-R4B — GOVERNED RETURN

Worker: `N04-R4B`

Branch: `agent/rabochii-prev3-n04r4b-routing-binding-r1`

Commission grain: `N04_R3_159_ROUTING_APPLICABILITY_REF_BINDING_R1_ONLY`

Terminal: `PASS__N04_R4B_159_ROUTING_STATES_ACCOUNTED__ZERO_APPLICABLE_CURRENT_REFS__159_UNRESOLVED_PRESERVED`

## Result

The exact N04-R3 routing-residual surface contains **159** unique current `question_implementation_id` values. Every one of those IDs carries the accepted N02-R2 exact-ID disposition `UNRESOLVED_ROUTING_APPLICABILITY_AUTHORITY`.

Accordingly this lane binds **0** `routing_applicability_ref` values. It does not convert unresolved rows into applicable/current routing, known absence/nonapplicability, or outside-jurisdiction states.

Complete selected-ID accounting is committed in `02_SELECTED_159_ROUTING_ACCOUNTING.jsonl.zlib.b64` (lossless zlib/base64; replay expands the full canonical JSONL).

- selected rows: **159**
- unique selected IDs: **159**
- sorted selected-ID stream SHA-256: `dfe518e369047eff7978e0a9b1161989cf97c1254ac577479e5c7c38b3671a12`
- decoded accounting JSONL SHA-256: `ca237bdd68001a93d89624a5d9b3a5a98926c77fa9fe123056a030269e3d3563`
- accounting JSONL bytes: **87315**

Preserved states:

- applicable/current routing ref bound: **0**
- governed known absence/nonapplicability: **0**
- outside routing-bearing jurisdiction: **0**
- unresolved routing/applicability authority: **159**

The typed residual remains `routing_applicability_ref` for all 159 IDs.

## Authority and replay

Accepted routing authority: N02-R2 `b01c5620c592274fa9acd0eab1c9ef38e79071a3`, canonical replayed row stream SHA-256 `0f0b367275c931efec69918a82a1b78355f6b6050b6c2017990061578bef6ad0`.

Predecessor: N04-R3 `8e0266703bbf3b060abcd6fbe53c7ef6c49062c5`.

Deterministic replay is implemented by `rawlsing_next/n04_r4b_routing_applicability_binding.py`. It selects the predecessor's exact routing-residual status directly, replays the N03-R2 ledger carrying the N02-R2 exact-ID sidecar, asserts all 159 routing dispositions are unresolved, and asserts byte equality with the committed accounting artifact.

No Library access was used. No routing inference from question text, labels, adjacency, or statistics was used. Routing currentness was not treated as semantic currentness. No response-semantics or candidate-kind adjudication was performed. MAIN and semantic PRE-MAIN were not modified.

Encoded zlib/base64 accounting SHA-256: `ceef9f7ff18aedcdd14917aaf427fd71a0f75b21a661b4532f1c7072cad5271e`; encoded bytes: **7108**.
