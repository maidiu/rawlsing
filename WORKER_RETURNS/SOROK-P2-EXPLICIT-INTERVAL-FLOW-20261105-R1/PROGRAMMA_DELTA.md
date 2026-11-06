# PROGRAMMA_DELTA — SOROK P2 explicit interval continuation R1 repair

**Delta ID:** `SOROK-P2-EXPLICIT-INTERVAL-FLOW-20261105-R1`
**Repair base:** `bdadbc57c2664d3155a97853422e74b6128261f8` (immutable)
**Product base:** `41bf45813fd0adeffd9b54e1306c2022abe96514`
**Result:** `PASS` focused auto-DO_HELP repair.

## Delta

- Removed automatic `adapter.do_help()` from `admit_continuation`.
- Interval/admit/continue now return the public projected opportunity/read
  result only: `do_help: null`, `do_help_executed: false`, unchanged encounter
  count.
- Added separate explicit `explicit_do_help(...)` callable and CLI `do-help`
  operation. Only this operation executes a user DO_HELP attempt.
- Preserved ACTUAL material `0`/C9 false and SCHEDULED_ONLY material `1`/C9 true,
  cut/restore, cold continuity and the original author-only TEST_ONLY grade.
- Updated focused tests, CLI receipts, ordinary return and this delta.

## Not changed

- Historical commit `bdadbc57c...` remains immutable.
- No inherited product, vendor, projection, fan-in, later-lifecycle or
  PROGRAMMA working file was edited.
- No protected PRE-MAIN write, PR697 merge or native/human grant.
- No actor choice, motive, B state, paid counterpart or general autonomous
  absence life was added.

## Next owner action

Existing independent review of the exact repair commit before receiving
acceptance or HQ fan-in.
