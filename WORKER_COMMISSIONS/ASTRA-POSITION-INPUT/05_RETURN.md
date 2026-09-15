# D12 — PSC05 T01 Exact M10 Position Source/Applicability Packet — Return

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-prev3-astra-position-input-r1`

Commission tip: `0fdf5fe811347fec697ed8f3952ed69b9e5d8ff6`

Authorized grain: `PSC05_T01_EXACT_M10_POSITION_MATERIALIZATION_SOURCE_APPLICABILITY_PACKET_ONLY`

Library: `NOT USED`

## Terminal

`D12_BLOCK__NO_EXACT_SOURCE_OWNED_POSITION_LEVEL_WITNESS__D13_NOT_WOKEN`

## Determination

D12 is complete at its commissioned source/applicability-packet grain.

The exact frozen T01 semantic candidate is qualified and source-provenanced, but the accepted evidence does **not** bind a real position instance. The packet therefore returns the required typed missing-input blocker rather than substituting generic semantics for real-world witness facts.

The following source-owned position-instance inputs are missing:

- `EXACT_OBJECTIVE_ACTOR_OR_ENTITY_IDENTITY`
- `PRODUCTIVE_ASSET_CONTROL_INSUFFICIENT_FOR_INDEPENDENT_PRODUCTION` at actor-instance grain
- `ACTIVE_WAGE_LABOUR_SALE_RELATION` at actor-plus-counterpart instance grain
- `EXACT_EMPLOYER_OR_COUNTERPART_IDENTITY`
- `EXACT_INSTITUTIONAL_RULE_CONTEXT`
- `EXACT_VALID_TIME_OR_CURRENTNESS`

The M10/Wright evidence supports the reusable structural relation semantics, but not those actor-indexed instance facts. T01 itself expressly preserves this boundary: its exact employer/counterpart and institutional-rule entries are requirement kinds, not concrete witness values; it emits no real actor/entity fact; and it leaves valid-time/currentness to a later fact lane.

## Exact evidence used

- Dispatch authority: `a70cd2ef7d2b77c700bd8795f491079be554ae6b`
- T01 governed return: `b577200b8eab79b02f88aeba0997482d21d3c4e7`
- T01 return blob: `020007dd112654609f072048c53edf28b1e28e6b`
- T01 qualification artifact blob: `f3feb4421242994a4c2561cf3cef5ddb6a498400`
- Approved M10 source-worker tip: `0ebca9ff111bea63838f9b68c8e5c3cb93d9d128`
- M10/Wright source-ledger blob: `606de007e0f6dcb28e552bd8c959f3c4ec1fd2a7`
- HQ decision state: `9cdfffdfd0c2ac38bef4b02858cbd21f04aa4ecf`
- HQ T-series fan-in blob: `237ebebfd1e7804c3dda2ceb20294308887c2e56`
- HQ PSC-activation blob: `2b125ad22c87f23fb2135dd06c131115ac13b653`

Qualified semantic candidate:

`urn:rawlsing:prev3:objective-position-admission-candidate:sha256:60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505`

Candidate hash:

`60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505`

## Bundle

- `01_SOURCE_APPLICABILITY_PACKET.json` — exact evidence registry, six-field instance audit, four-constitutive-predicate audit, applicability determination, typed missing-input report, and D13 gate.
- `02_REPLAY_FIXTURE.json` — source-bound rejection cases for generic pattern, inferred actor, abstract relation, abstract rule context, semantic-only candidate, and build-time substitution.
- `03_RUN.py` — deterministic validator for the packet and replay fixture.
- `04_RUN_OUTPUT.json` — recorded validation result.

Packet SHA-256:

`8fb2f9774309dd35d50387bb4764a6543856661da2ba7a8da9c7be8f4e1194ab`

Replay fixture SHA-256:

`6148ebc6d65473452bb703558dce7dd9c2cd330182113a49376545cd5a2a4dd0`

Recorded validator result:

```json
{"D13_wake": false, "candidate_hash": "60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505", "library_used": false, "missing_instance_predicate_count": 6, "packet_sha256": "8fb2f9774309dd35d50387bb4764a6543856661da2ba7a8da9c7be8f4e1194ab", "rejected_substitution_case_count": 6, "task_status": "BLOCKED_TYPED_MISSING_INPUT", "terminal": "D12_BLOCK__NO_EXACT_SOURCE_OWNED_POSITION_LEVEL_WITNESS__D13_NOT_WOKEN", "validation": "PASS"}
```

## Successor gate

`D13_wake = false`

No position fact was emitted. No downstream reconciliation was performed.

D13 may wake only after competent source evidence supplies a complete real witness tuple at the required Q73A/Q84 position-instance grain.

## Preserved boundaries

- No semantic recomputation.
- No generic pattern, class/job label, abstract relation, rule semantics, or inferred actor was promoted into a real witness.
- No build/retrieval timestamp was used as validity/currentness.
- No mechanism or channel rule was minted.
- No topology was constructed.
- No V3/person state was entered.
- OBL063 semantics remain quarantined.
- Library was not used.
- MAIN and PRE-MAIN were not mutated.
