# SOROK S41 — sequential admitted events for the same continuing person

**RESULT:** `S41_TWO_EVENT_CONTINUING_PERSON__COLD_BETWEEN_AND_AFTER__SAME_ROOT_BRANCH_STORE__SECOND_ACTUAL_C8_E1__CANONICAL_PRIOR_FACT_AND_GENERATION_READSET_BOUND__EVENT_KEYED_READERS__17_OF_17_FOCUSED_TESTS__ENTRYPOINT_0__NO_TARGET__NATIVE_HOLD`.

One accepted S40/S37 person/product is started once, its first event and generated request are committed, the session is closed and reopened, and a second distinct world/E1 event is admitted through `continue_event` on the same actor/root/branch/store and the same keyed C8/C9 state. The second generation cites the first admitted B share as an actual historical source, not a caller boolean. Both event-specific readers remain valid after the second event and after cold reopen.

## Session, base and scope

- Existing OpenCode author `ses_e9387509affeR5dC27RoUy3WSH`; same OpenCode Go / DeepSeek V4.1-Flash MAX; no timeout, new agents, provider/domain/model calls or reviewers.
- Branch `codex/sorok-s41-continuing-person-events`; base accepted S40 `79b0357c7af9b66ad8a28f5b77b46b0348094a23`.
- Write scope only `WORKER_RETURNS/SOROK-20261024-S41-CONTINUING-PERSON-EVENTS-R1/**`.
- S40/S39/S37/S36/M35/language/JOIN-E remain read-only at their pinned cuts.

## Generation-readset repair — REVISE ff12892d

Review `30`/`a81740cf…` reproduced a second defect: the attached canonical history could remain valid while `generation.source_refs` was replaced with `TEST_ONLY_REPLACEMENT_SOURCE`; the second event still read performed/OK and verified warm/cold.

Repair:

- Added `validate_generation_readset` in `s41/history.py`. It requires nonempty unique consumed refs, the canonical history source ref, no unrecognized source refs when the actual generation input records are available, and a matching canonical history reason/`source_hash`/predicate.
- `continue_event` calls it immediately after `producer.generate` and before world advancement/action/C9 effects; `S41EventRefusal` aborts without an actor action or second C9 response.
- Normal continuation bindings persist the actual `generation_sources`; warm/cold event-keyed readers validate the generation readset against them and against the attached canonical history, even when every outer seal is valid.
- The reader refuses absent/replacement/wrong-bound consumed history and keeps event 1 readable.

The unchanged generation-readset reproducer now exits **1** with `S41ReadRefusal: S41_GENERATION_READSET_INVALID: S41_GENERATION_CANONICAL_HISTORY_ABSENT`; it is not counted as passed by exit 0. Both unchanged reviewer reproducers are recorded in `evidence/repro_bad_history.json` and `evidence/repro_generation_readset.json`.

## First history-source repair — REVISE cced4223

Review `29`/`3a22d3a9…` reproduced that a self-sealed unrelated history source (`TEST_ONLY_UNRELATED_SELFSEALED`) with zero `prior_b_event_hash` could still drive `REQUEST_TOOL` and verify warm/cold. Repair:

- `history_record_from_prior` now emits a canonical source ref `TEST_ONLY_S41_HIST_<first_e1_event_id>` and exact prior fields: prior E1 ID/hash, C8 occurrence/content hash, B operation/event hash, actor, branch, event time, prior access witness/source ref/hash and source-actor map.
- `s41/history.py` validates that record against the actual earlier C8 occurrence/source/actor/clock and the sealed earlier generation/access binding, not the history record alone.
- `continue_event` validates the canonical history **before** admitting the second C8 event; generation consumes only the validated canonical source.
- The event-keyed warm/cold reader applies the same validator, so persisted unrelated/wrong-bound history refuses rather than passing a self-sealed summary.
- Added focused regressions for unrelated source ref, wrong B event hash, wrong C8 content hash, wrong access witness hash, wrong E1 hash, wrong actor/branch/time, plus a persisted bad-history event rejected warm and cold.

The unchanged reviewer reproducer now exits **1** with `S41EventRefusal: S41_HISTORY_BINDING_INVALID: S41_HISTORY_SOURCE_REF_NOT_CANONICAL`; it is not counted as passed by exit 0. Evidence is in `evidence/repro_bad_history.json` and `.stderr.txt`.

## What was implemented

- `s41/session.S41Session.start` reuses the accepted S40 start once, then writes an event-keyed `S41_ADMITTED_EVENT` binding for event 1.
- `S41Session.continue_event` admits a later source-bound REFUSE_TOOL stimulus into the **same** keyed C8 journal and C9 store, using `ContinuationProducer`. It builds the second C8 occurrence from the current C12 actor/world state, not the seed snapshot; current tool inventory, position, clock, prior action and language history are retained.
- The second event's generated comparison consumes a sealed historical source record mapped from the first actual C8 B operation (`SHARE_TOOL → PRIOR_B_SHARE`), with exact first E1/C8/source refs. Caller-supplied prior-share/refusal assertions are filtered out.
- The second speaking action uses the accepted S40 plan → native Spanish speech → three-way equivalence → labeled English view. A nonverbal action would remain nonverbal; a denied `REQUEST_TOOL` appends no speech/action. The second C9 response remains targetless `NO_CHANGE/NO_PROPOSAL`.
- `s41/bindings.py` stores each event's generation/attempt/action/C8/C9/plan/artifacts/admission/projection and history in its own sealed `S41_ADMITTED_EVENT` episode. It does not overwrite the first event's `meta.c8/s36/s39_generation` or append a second S39 global generation episode.
- `s41/reader.py` reads by admitted E1 event ID/hash, re-reads the actual C8 occurrence and actual C9 response/receipt rows, validates the event's language/projection/admission, and checks the prior history link. `read_latest` returns the second event; reading event 1 after event 2 uses event 1's own metadata and receipts.
- `s41/event.py` includes a bounded OUT9 continuation adapter because accepted `read_out9` hard-requires exactly one occurrence ID. The adapter reuses the same `C8ReadOnlyConsumer`, event ingress and proof verifier, verifies the later occurrence/state digest, and retains the prior occurrence bytes. This is the exact existing interface conflict and no new owner/journal was invented.
- A current-world inventory check in `s41/performer.py` refuses a `REQUEST_TOOL` when the workshop tool was actually removed by an existing `take_tool` action; the same S40 performer handles the admitted cases.

## Model premises

1. The current synthetic actor snapshot is derived from the actual C12 state at continuation time; the historical M35 seed state is not reapplied.
2. The mapping `witnessed prior C8 B SHARE_TOOL → existing PRIOR_B_SHARE predicate` is an explicit synthetic continuation-adapter premise, not empirical psychology.
3. S39's finite guarded comparison rule and S40's finite language registry remain unchanged model premises.
4. Incoming second B REFUSE_TOOL is an objective world occurrence; it does not overwrite A's current tool inventory or determine A's response by itself.

## Actual two-event evidence

| | Event 1 | Event 2 |
|---|---|---|
| Source operation | `SHARE_TOOL` | `REFUSE_TOOL` |
| E1 event ID | `TEST_ONLY_BP2_E1_OCC-0001` | `TEST_ONLY_BP2_E1_OCC-0002` |
| C8 occurrence | `OCC-0001` | `OCC-0002` |
| Event time | 242 | 243 |
| Generated option | `REQUEST_TOOL` | `REQUEST_TOOL` |
| Performer | ADMITTED | ADMITTED |
| Native / English | `¿Puedo usar la herramienta?` / `May I use the tool?` | same |
| C9 | `OBSERVED_IMMEDIATE_OBJECT_ORIENTATION`, `NO_CHANGE/NO_PROPOSAL` | same |
| Target proposals/rows | `[]` / 0 | `[]` / 0 |
| History | none | canonical first actual E1/C8/source/access, `PRIOR_B_SHARE`; actual generation readset includes it |

The first event is read after the second with its own response reference. A's tool remains available (1) after the second REFUSE_TOOL event. Root actors remain A/B; branch actors remain A/B/U. Cold reopen between and after the events returns both readers valid and the latest event as ordinal 2.

Boundary evidence:

- OPEN second event: C8 occurrence remains admitted, generation `OPEN_CHOICE_SET`, no actor action, no second C9 response, no language; first event untouched. Duplicate `continue_event` refuses `S41_ALREADY_CONTINUED`.
- Wrong second source actor/recipient/owner/hash/clock/operation and non-later event time do not append actor action or C9 response and preserve event 1.
- Tampered actual prior-history source and revoked access refuse at the generation boundary; restoring the actual history/access returns unique `REQUEST_TOOL`; event 1 bytes and binding remain.
- Actual `take_tool` current-world action then second event: performer `DENIED` (`TOOL_NOT_AVAILABLE_IN_CURRENT_WORLD`), no speech/action, C9 valid-empty `RECEIVABLE_NO_OBSERVED_UPTAKE`, zero target.
- Second-event plan/projection mismatch is refused by the event-keyed reader while event 1 remains valid; cold reopen refuses.

Focused tests: **17 passed** (`junit/s41_full.xml`); entrypoint exit 0; both unchanged reviewer reproducers exit 1 with typed refusals (`S41_HISTORY_BINDING_INVALID` and `S41_GENERATION_READSET_INVALID`). No broad inherited rerun.

## Reused roots/cuts

S40 `79b0357c…` five key files exact; S39 `e41513fa…`; S37 `e1f3c1da…`; S36 `8da78d80…`; language `8d2920da…`; M35 `4170fbf1…`; JOIN-E `7bf2da30…`. `evidence/source_manifest.json` records exact local/imported origins and the accepted S40/S39/S37 manifests’ exact flags.

## Limits

Wholly TEST_ONLY sourcefree continuation. No native CAN008/CAN011/CAN022/023, C11/native C12, original/human data, A5, acquired practice, motive/trust change, stochastic choice or general planner. Event/history facts are not a new practice or psychological transformation. No provider/domain/model calls, extra workers/reviewers, controller/M35/S37/S39/S40 edits, target fabrication or native/source/human grants.

**Terminal:** `S41_TWO_EVENT_CONTINUING_PERSON__COLD_BETWEEN_AND_AFTER__SAME_ROOT_BRANCH_STORE__CANONICAL_PRIOR_FACT_AND_GENERATION_READSET_BOUND__EVENT_KEYED_READERS__17_OF_17_TESTS__NO_TARGET__NATIVE_HOLD`. Final commit and remote SHA are verified after push and reported in the final handback.
