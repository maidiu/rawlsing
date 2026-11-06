# PROGRAMMA_DELTA — Sorok P2 product fanin R1

**Delta ID:** `SOROK-P2-PRODUCT-FANIN-20261105-R1`
**Base accepted:** `41bf45813fd0adeffd9b54e1306c2022abe96514`.
**Sources:** lifecycle `79b90e4a57cbd1b738a9b9484677736d1b6415ab`; interval `bdadbc57c2664d3155a97853422e74b6128261f8`; later-event `76fdb624afc7674f088d10c349bfe15ffd0b865a`.
**Grade:** `TEST_ONLY_SOURCEFREE_P2_PRODUCT_FANIN_NOT_NATIVE`.
**Result:** 6 focused tests pass; cold CLI sequence passes; one S47 root; no auto DO_HELP.

## Added

- Exact import of the three additive `WORKER_RETURNS` source directories, with evidence preserved and tree hashes recorded.
- `P2ProductFanin`: one compatible S47 root with accepted lifecycle boundary, explicit interval input, and later-event source-bound admission/read.
- `run_fanin_cli.py`: actual throughline CLI with `new`, `view`, `say`, `do-help`, `attend`, `exit`, `return`, `status`, `lifecycle`, `interval`, `later-event`, `opportunity`, `verify`.
- Focused tests/evidence for positive ACTUAL, SCHEDULED_ONLY contrast, attempt-vs-observation, ATTEND no world activity, outside block/local return, cut/restore, UNKNOWN/refusal, privacy and cold CLI.

## Semantics

- `OUTSIDE` blocks only user encounter actions; local `RETURN` restores `PORTAL` with no canonical actor/world mutation.
- Explicit interval is supplied input, not WAIT/absence-caused actor choice.
- Later-event observation is not a user attempt. Only explicit `do-help` performs user DO_HELP.
- The upstream interval helper `admit_continuation` auto-calls `do_help`; fanin avoids it and records the concrete defect.

## Not changed

No accepted base/vendor/projection/PR697 edits, no PROGRAMMA working-file changes, no native/science/human/B grant, no fabricated absence/activity/delivery or actor reaction.

## Holds

Independent review of this fanin is NOT_RUN; latter2 review separately pending; inherited full estate NOT_RUN; no self-acceptance.
