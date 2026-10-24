# S42 ongoing-event consumer — REVISE

Decision: **REVISE**.

## Exact cut

- Candidate: `65029da42af560abf23d8746a9e961dd29764a39`.
- Branch: `codex/sorok-s42-ongoing-event-consumer`; remote matches.
- Base: accepted S41 `c72a10d284f8869b990db3e6849ed174a51bd784`.
- Reused cuts: M35 `4170fbf…`, S36 `8da78d8…`, S37 `e1f3c1d…`, S39
  `e41513f…`, S40 `79b0357…`, S41 `c72a10d…`, language `8d2920d…`, JOIN-E
  `7bf2da3…`.
- Reviewed in a disposable fixture. No product edits, provider/model calls,
  extra agents, launcher/notifier changes, or native/science action.

## Checks that pass

```text
PYTHONPATH=<S42 return> python3 -B -m pytest -q \
  <S42 return>/tests -p no:cacheprovider
9 passed in 9.78s
```

The `run_s42.py` entrypoint exits 0 with a five-event stream, cold reopen
before calls, distinct E1/C8 identities, increasing event times, same root/branch,
preserved first event, retained current-world tool, zero targets, and cold
verification true. The focused tests cover 3/5-event streams, OPEN followed by
a later event, history reorder/duplicate/missing refusals, same-source replay,
persisted input replacement/duplicate refusal, and older source fault/restore.

## Remaining defect

The event-keyed reader does not validate the persisted **predecessor binding**
against the actual prior binding/C8 continuation. A fully admitted third event
whose real predecessor is event 2 can persist event 1 as its
`predecessor`; it reads `OK`, performed true, with warm and cold verification
true.

```json
{
  "event2_status": "OK",
  "event2_e1_event_id": "TEST_ONLY_BP2_E1_OCC-0002",
  "actual_predecessor_for_event3": "TEST_ONLY_BP2_E1_OCC-0002",
  "c8_predecessor_for_event3": "TEST_ONLY_BP2_E1_OCC-0002",
  "persisted_predecessor_for_event3": "TEST_ONLY_BP2_E1_OCC-0001",
  "event3_status": "OK",
  "event3_read_status": "OK",
  "event3_performed": true,
  "warm_verify_ok": true,
  "cold_event3_status": "OK",
  "cold_verify_ok": true
}
```

`s42/reader.py:_read_s42_event` validates history refs/generation input and the
C8 source/clock/actor, but does not compare `binding["predecessor"]` with the
actual predecessor (or the C8 `s42_continuation.predecessor_e1_*` fields).
The persisted predecessor substitution therefore passes warm and cold.

## Required repair

- Bind and validate each event's actual predecessor identity, including the
  predecessor E1/C8 hash, ordinal, time, branch/actor, and the C8
  `s42_continuation` predecessor fields.
- Apply the check in the warm/cold event-keyed reader and before later events
  are admitted; reject a missing, replaced, or out-of-order predecessor while
  preserving earlier events.
- Add a regression for a fully admitted event with a substituted predecessor.

## Receipt

- 9-test output: `evidence/s42-tests-9.out` SHA-256
  `ee4d2ad727ce5acf9cc50901e6a51ff855922d1fd3adbf7cabf2e9772b46ec01`.
- Entrypoint: `evidence/s42-entrypoint.json` SHA-256
  `5d8cfae0d4aac0657efeb91742164694858b2bc9d313a6489f8e08c0ddf7b204`.
- Predecessor reproducer: `evidence/repro_predecessor_binding.py` SHA-256
  `9d80981e0bfc17094eaee880ae84740a93c903329204d91d30e068c52aac2ae9`;
  output `evidence/s42-predecessor-repro.json` SHA-256
  `6428e3521c0122ad42fa28ffc1f5b1b52517b3aff0abdf6bcfb11b3e57aabaac`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed.
