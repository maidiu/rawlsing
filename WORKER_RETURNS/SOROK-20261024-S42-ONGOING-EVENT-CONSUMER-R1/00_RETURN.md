# SOROK S42 — reusable ongoing admitted-event consumer

**RESULT:** `S42_REUSABLE_ONGOING_ADMITTED_EVENT_API__VARIABLE_LENGTH_3_AND_5__COLD_REOPEN_BETWEEN_ANY_CALLS__SAME_PERSON_ROOT_BRANCH_STORE_WORLD_C8_C9_C12__9_OF_9_FOCUSED_TESTS__S41_19_OF_19_COMPAT__NO_TARGET__NATIVE_HOLD`.

S41's single hardcoded continuation is replaced by a reusable `S42Session.admit_event` path. Any accepted S41 first event can be followed by any number of valid incoming sources; every call derives a new ordinal, increasing event time, current-world snapshot, predecessor binding and explicit history references. The person/root/branch/store/world/C8/C9/C12 are never restarted, and cold reopen works between every call.

## Session, base and scope

- Existing OpenCode author `ses_e9387509affeR5dC27RoUy3WSH`; same OpenCode Go / DeepSeek V4.1-Flash MAX; no timeout, extra agents, provider/domain/model calls or reviewers.
- Branch `codex/sorok-s42-ongoing-event-consumer`; base accepted S41 `c72a10d284f8869b990db3e6849ed174a51bd784`.
- Write scope only `WORKER_RETURNS/SOROK-20261024-S42-ONGOING-EVENT-CONSUMER-R1/**`.
- S41/S40/S39/S37/S36/M35/language/JOIN-E remain read-only at their pinned cuts.

## What was implemented

- `S42Session` subclasses accepted `S41Session`. `start` reuses the S41 first-event start once; `admit_event` is an unbounded public continuation method on the same actor/root/branch/store.
- `admit_event` reads the latest event binding, derives `ordinal = max + 1`, `event_time = max(current clock, predecessor time) + 1`, accepts a new M35-validated B source, builds a new C8 occurrence from the actual current C12 actor/world snapshot and predecessor, and binds the predecessor explicitly.
- Caller history references are explicit prior admitted E1 IDs/hashes. Each is validated against the real earlier binding/source/C8/E1/access; refs must be strictly ordered by ordinal/time, unique and below the new event. No caller boolean and no fixed first-event-only projection is used.
- The finite S39 guarded comparison and S40 authorized plan/native speech/equivalence/labeled English path remain unchanged. History is passed as canonical sealed source records, not as recency preference, weights or probability.
- `s42/reader.py` provides a unified event-keyed reader over S41 event 1 and all S42 events. It revalidates actual C8/C9/action/language and all histories, and preserves the three S41 history/generation/input-source fixes in the S42 path.
- Incoming exact source replay at the same derived clock is refused before new effects. History duplicates, reordering, missing refs and wrong hashes are refused without corrupting earlier events. OPEN events append no actor action/C9 and remain readable; later events can continue after an OPEN.
- Existing targetless C9/C12 behavior is unchanged: every committed response is `NO_CHANGE/NO_PROPOSAL`, with zero target proposals/rows. T remains no-change.

## Actual evidence

- Focused S42 tests: **9 passed**.
- Accepted S41 compatibility suite: **19 passed**.
- All three unchanged S41 reviewer reproducers: exit **1** with their typed refusals.
- Entrypoint: exit 0; five-event chain with cold reopen before each call.
- 3-event and 5-event chains: distinct E1/C8 identities, increasing clocks, same root/branch, first event bytes preserved, current tool retained (1), no targets, seven/expanded history readers valid, latest ordinal equal to length.
- Chain stream demonstrates consuming older event 1 and event 3 rather than a mandatory first-only projection. Event 2/4 objective incoming sources are REFUSE_TOOL; A's existing tool is never reset.
- Boundary checks: reordered, duplicate, missing, wrong-hash and wrong-branch history refs refused; exact source/clock replay refused; OPEN has no action/C9; a later event after OPEN is admitted; binding/action counts unchanged on refusals.
- S42 persisted input replacement/duplicate tests reject warm and cold while event 1 remains readable.
- Older source/access fault after later additions refuses and restores through the same consumer.
- Evidence: `evidence/chain3.json`, `chain5.json`, `boundary.json`, `test_run.json`, `s41_compat.json`, `s41_reproducers.json`, `source_manifest.json`, `entrypoint.json`.

## Model premises and limits

The synthetic current actor snapshot, entire current C12 world inventory and explicit prior history refs are TEST_ONLY model inputs. `PRIOR_B_SHARE`/`PRIOR_B_REFUSAL` mappings remain the unchanged synthetic adapter premises; no recency preference, aggregation weight, probability distribution, new motive, practice or source/access grant is introduced. Conflicting/insufficient finite rule outcomes remain SYSTEM/MODEL OPEN and never persona silence/indecision.

No native CAN008/CAN011/CAN022/023 rule or grant, C11/native C12, original/human data, A5, T implementation, target, stochastic sampling, provider call or production architecture was added. No launcher/notifier changes, extra workers or accepted-dependency edits.

**Terminal:** `S42_REUSABLE_ONGOING_EVENT_CONSUMER__3_AND_5_EVENT_COLD_STREAMS__SAME_PERSON_STORE_WORLD__EXPLICIT_HISTORY_AND_CANONICAL_INPUT_BOUND__OPEN_NO_ACTION__9_OF_9_TESTS__NO_TARGET__NATIVE_HOLD`. Final commit and remote SHA are verified after push.
