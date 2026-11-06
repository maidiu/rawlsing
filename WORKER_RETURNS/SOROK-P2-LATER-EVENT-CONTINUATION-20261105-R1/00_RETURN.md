# SOROK P2 later-event continuation — additive runnable return

**RESULT:** `P2_LATER_EVENT_CONTINUATION__REAL_S42_S43_LATER_EVENTS__EARLIER_INTERVAL_ACTIVITY_CONSTRAINS_PROJECTED_DO_HELP__SOURCE_BOUND_S43_EXPRESSION__ATTEND_PRESENTATION_ONLY__CUT_RESTORE_AND_COLD__5_FOCUSED_TESTS__TEST_ONLY_SOURCEFREE__NOT_NATIVE`.

This is additive P2 construction over the independently accepted shipped S45-S47 package at `41bf45813fd0adeffd9b54e1306c2022abe96514`. It adds only `WORKER_RETURNS/SOROK-P2-LATER-EVENT-CONTINUATION-20261105-R1/**`; no shipped product, vendor, projection, PROGRAMMA working file or protected branch was edited. PR697 remains unchanged and unmerged. This return is implementer evidence, not self-acceptance.

## 1. Exact base and reuse

- Base: `41bf45813fd0adeffd9b54e1306c2022abe96514` (accepted scoped TEST_ONLY; PR #697 draft, not merged).
- Shipped product closure: `WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product`; its `SOURCE_MANIFEST.json` SHA-256 is `2535398efa2c376731aec17cd7b2ceda2e0fee477f064ae049870393b838b94b`.
- Projection adapter: shipped `WORKER_RETURNS/SOROK-S45-S47-PROJECTION-20261105-R1/s45_projection`.
- No interval producer, lifecycle, actor rule, memory/practice grant or generated B context was reimplemented or invented. The S46 interval is used only as an existing input API.

## 2. Actual producer → first consumer trace

| Role | Exact callable exercised |
|---|---|
| Later-event producer | `s43.session.S43Session.admit_event` resolved on `s47.session.S47Session` |
| S41 continuation producer | `s41.event.ContinuationProducer.generate` |
| S41 continuation performer | `s41.performer.perform_continuation_attempt` |
| S42 history builder | `s42.event.make_history_records` |
| S42 occurrence builder | `s42.event.build_ongoing_occurrence` |
| Later-event reader | `s45.session.S45Session.read_event` delegating to `s42.reader.read_event` |
| Source-bound expression reader | `s43.session.S43Session.read_s43_event` |
| Event-local C9 reader | `s47.session.S47Session.read_c9_conditioning` |
| Later projected response | `s45_projection.adapter.S45Projection.say/do_help/attend` |

The exercised producer produced real S42 events `TEST_ONLY_BP2_E1_OCC-0002` and `TEST_ONLY_BP2_E1_OCC-0003`, not a narrative fixture. The actual first consumers above read those events, their history refs, S43 repertoire/language and event-local S47 C9 conditioning.

## 3. Positive chain actually executed

Command (also in `evidence/test_run.json` and `evidence/positive.json`):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 -B -m p2_continuation.cli \
  positive --state .local-logs/p2-evidence/positive/state
# exit 0
```

Observed:

- Same root `3bcb21fc22df3255269382ad249f706dd6dd5378cb886af26542991ff516a4f7`.
- Existing S46 ACTUAL interval is the earlier performed actor-world activity: status `PARTIAL`, coverage `[[222,223]]`, material `1 -> 0`, interval source `TEST_ONLY_S47_INTERVAL_S46_STATE_E22149E8875BE71309CFEB56`, source hash `e196c974e43a024055949113f6b875be8c012f1c422d6829d4890e8a46688658`.
- Later S42 event 2 is real and performed; its C9 readset contains the interval source with `objective_material_eligible=false`.
- Later S42 event 3 is real and performed; its history refs include event 2, so the earlier later-event identity is consumed by the later event.
- Event 2 remains identical after event 3: same event hash, same C9 source ref/hash, still in readset.
- S43 source-bound expression is real: `language_status=ACCEPTED`, repertoire `S43_REP_E0D29337FE0F3551E71E7D6D`, native text `¿Puedo usar la herramienta?`, labeled English `May I use the tool?`.
- Projected `SAY` is an attempt (`attempted=true`, `performed=false`).
- Projected `DO_HELP` is an attempt (`attempted=true`, `performed=false`) and an actual refusal (`REFUSED`, `HELP_REFUSE`), constrained by the earlier material-consuming interval.
- Projected `ATTEND` is presentation-only: `NO_CHANGE`, `world_event_created=false`, `clock_changed=false`, `performed=false`.
- Cold reopen returns the same root, same event 2/event 3 C9 source hashes, same S43 repertoire, and `verify().ok=true`.

## 4. Same-root scheduled control

Command: `p2_continuation.cli scheduled --state .local-logs/p2-evidence/scheduled/state`; result `PASS` (`evidence/scheduled.json`).

- Same root as positive.
- Existing S46 `SCHEDULED_ONLY` interval leaves material `1` and coverage `[]`.
- The same later-event chain is admitted.
- Projected `DO_HELP` is still a user attempt, but now `OK` / `HELP_ACCEPT` with actor `REPAIR` performed by A.

This is the causal contrast: the earlier performed interval activity, not a new actor rule, changes the later opportunity.

## 5. Exact dependency cut, refusal, restore and cold

Command: `p2_continuation.cli cut-restore --state .local-logs/p2-evidence/cut/state`; result `PASS` (`evidence/cut_restore.json`).

- Revoke the S46 interval condition before later admission.
- Later event admission refuses with exact `S46_INTERVAL_CONDITION_REVOKED`; no later event is appended.
- Restore reconstructs the same source hash `e196c974...`.
- Later admission succeeds; event-local C9 uses the restored source and `s47_source_in_readset=true`.
- Cold reopen returns the same root and source hash; `verify().ok=true`.

## 6. Tests and evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 -B -m pytest -q \
  -p no:cacheprovider --junitxml=evidence/junit.xml tests
# 5 passed in 84.85s, exit 0
```

Tests cover: positive later-event chain/projection; named producer and first consumers; same-root scheduled control; interval-condition cut/refusal/restore; CLI cold and verify reads.

Evidence: `evidence/positive.json`, `evidence/scheduled.json`, `evidence/cut_restore.json`, `evidence/cold.json`, `evidence/verify_positive.json`, `evidence/source_manifest.json`, `evidence/test_run.json`, `evidence/junit.xml`, `logs/`.

## 7. Grade, limits and holds

- Grade: `TEST_ONLY_SOURCEFREE_P2_LATER_EVENT_CONTINUATION_NOT_NATIVE`; `native=false`; no provider/model calls.
- Test roots/cases are TEST_ONLY sourcefree generated inputs; B remains a sourcefree coactor fixture, not a current B-owned context or independent counterpart.
- No new actor rule, psychological probability, memory/practice acquisition, target proposal, external message/delivery, human usability or native C8/C9/C12/CAN008/CAN011/ADP/Pyat grant is claimed.
- The shipped package's accepted scoped TEST_ONLY review is reused; this additive continuation has not been independently reviewed.
- No protected branch write, no product edit, no PROGRAMMA working-file edit and no global config change.
