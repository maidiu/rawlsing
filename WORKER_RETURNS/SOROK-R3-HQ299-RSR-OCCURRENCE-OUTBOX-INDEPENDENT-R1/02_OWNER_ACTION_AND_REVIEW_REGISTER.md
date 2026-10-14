# HQ299 RSR — independent owner-decision register

**Not an adoption instrument.** Source-free evidence at pinned implementation scope only. The reviewer independently reran the original 28/28 and added 17 new controls (5 PASS, **12 observed FAIL**) and two real subprocess cold replays (2 PASS). The below is **not** a finding that accepted ADP-019, CAN-022 or CAN-025 runtimes failed: their production modules were not imported.

| ID | Direct finding | Decision for SR prototype | Competent next owner action |
|---|---|---|---|
| RSR-01 | Exact original Python 28 tests and original blobs reproduced independently | `ACCEPT_REPRODUCTION_ONLY` | Keep original fixture/tests immutable; maintain lower proof label than 28 full oracle outcomes |
| RSR-02 | Original S27's test changes mug after payload `world_owner=NADIA`, whereas its **frozen** S27 requires `HOLD_MISSING_MATERIALIZATION_OWNER` and unchanged mug | `FROZEN_ORACLE_MISMATCH` | World/material-owner plus ADP-019 reviewer: require actual issuer ref and valid material-effect receipt; do not accept payload string as authorization |
| RSR-03 | S28 admits, emits, then restores *pre-admission* snapshot; never checks that absent causal time is DEFER | `FROZEN_ORACLE_MISMATCH` | ADP-019 event-time/scheduler owner supplies and verifies missing-causal-time refusal; untouched causal cursors |
| RSR-04 | S17 checks in-memory admit without actual kill/recovery; the independent `os._exit(79)` test loses in-memory admission if not externally persisted | `ATOMICITY_UNPROVEN` | Transaction/outbox owner must durably commit event, cursor, receipt and outbox intent together; crash checkpoints before/after persisted commit |
| RSR-05 | UserProjection.perceive accepts event without offer/delivery; `offer` and `emit` accept nonexistent event IDs | `GHOST_ACCESS_AND_EMISSION` | Client/surface/outbox owner must bind occurrence ID to positive admission/actor/user scope; no delivery/ACK→human-perceived equation |
| RSR-06 | `snapshot` and `restore` omit opportunity state; opportunities persist incorrectly in same object and disappear after cold rehydrate | `REPLAY_STATE_INCOMPLETE` | Owner adds full exact per-user opportunity identity and replay in transactional outbox; never narrate perceived on replay |
| RSR-07 | Candidate input, returned event and shallow snapshot share mutable dictionaries; accepted content hash can disagree with current content | `IMMUTABLE_EVENT_INTEGRITY_FAILURE_AT_PROTOTYPE_GRAIN` | ADP-019 durable event owner uses immutable deep/content-addressed copies, validating exact artifact/authority/causal-parent/effect binding and stable event ref |
| RSR-08 | Different source_refs replay as same candidate if payload matches; missing causal-time and empty source refs accepted | `ADMISSION_BINDING_MISSING` | ADP-019/CAN-025 owner binds full envelope, proposal/semantic/renderer/authority hashes, effective causal time and identity; zero causal write on missing input |
| RSR-09 | False testimony correctly leaves `world_state['employment']='fired'` unchanged in one positive test; however unrelated `objective_employment_transition='quit'` sidecar is admitted into the event as unchecked payload | `FALSE_TESTIMONY_ONLY_PARTLY_PROVED` | Actor/testimony-event owner must admit only the utterance as utterance and reject/unbind objective factual effects absent the world owner's own rule |
| RSR-10 | Outbox ACK does not automatically mark perceived, a positive bounded invariant; however no real client transport/dedup or per-user delivery identity was executed | `TRANSPORT_EXACTLY_ONCE_UNPROVEN` | Delivery owner tests realistic duplicate physical send with stable per-client ID, idempotent ACK, crash/retry, and cannot infer perception even on ACK |
| RSR-11 | Original S04 asserts `event.content_hash == event.content_hash`; S19 appends memory without ADP016; S23 accepts an empty payload without missing/VALID_EMPTY comparison | `ORACLE_COVERAGE_GAPS` | Independent oracle custodian freezes actual two different user allowlists, ADP016 encoded-memory witness, and valid-empty vs missing-authority distinctions; do not edit old oracle |
| RSR-12 | Previous HQ298 separate Browser supplement `sr_prototype.py` and JUnit 31/31 reported in archive; this reviewer did not re-import that separately implemented binary archive | `SUPPLEMENT_REPLAY_LIMIT` | A future narrow court may independently stage/archive-hash that *other* author prototype if claiming independent agreement across both, without conflating the two executions |

## Exact source/owner separation

- **ADP-019 accepted authority:** `V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE@1.0.0`; only its ADMIT establishes one V3 external event from an exact complete envelope. Its current authority document Git blob `5c38772ea193e5a3f20da23c16df086a153ab2f2` at the HQ299 base. The SR Python `OccurrenceLedger.admit` is a *standalone mock*, **not the accepted owner**.
- **CAN-025 accepted authority:** `V2_TO_V3_EXTERNAL_EVENT_PACKAGING_CONTRACT@1.0.0` Git blob `7bf380f5e6cef1f7a0d28d5ecc1ae65e5fde9ebb`; packaging READY/cursor/render identity does not create an event. SR prototype does not import the real package schema.
- **CAN-022 accepted authority:** `V2_RENDER_ADMISSION_PROMPT_CONTRACT@1.0.0` Git blob `5b85c67f74112c19fa72acf2cd4de226f73ecf47`; rendered wording must not authorize gesture, material effect or event. No model called here.
- **CAN-015 accepted authority:** `V2_PHENOMENOLOGICAL_PROJECTION_RULE@1.0.0` Git blob `cd976fb9b3b84b09068a57607adea09a33abf4ad`; projection cannot confer objective history or a user/actor memory.

## Reproduction vs semantic acceptance

`REPRODUCED_ORIGINAL_28_PYTEST = PASS`  
`COLD_HARNESS_PERSISTED_REPLAY = PASS_WITH_EXTERNAL_PERSISTENCE`  
`COLD_UNPERSISTED_ADMISSION_SURVIVES_CRASH = FALSE`  
`INDEPENDENT_STRICT_BOUNDARY_CASES = 5_PASS_12_FAIL`  
`SR_ORIGINAL_28_EQUAL_28_FROZEN_ORACLE_SATISFACTION = NOT_PROVEN`  
`ADP019_CAN022_CAN025_IMPLEMENTATION_AT_OWNER_GRAIN = NOT_RUN`  
`PHYSICAL_USER_PERCEPTION_OR_EXACTLY_ONCE_TRANSPORT = NOT_PROVEN`  
`RECOMMENDATION = ACCEPT_SCOPED_TEST_REPRODUCTION__HOLD_STRONGER_TRANSACTION_AND_ACCESS_ADOPTION`

The distinct next step is one narrowly owned durable transaction+per-user projection implementation/repair and independent oracle court, not a product or V3 wake. No I3 escalation is warranted absent an actual contradiction between competent *accepted* authorities; this is an implementation/proof gap in an isolated prototype.
