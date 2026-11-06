# PROGRAMMA_DELTA — Sorok P2 product fanin R1

**Delta ID:** `SOROK-P2-PRODUCT-FANIN-20261105-R1`
**Base accepted:** `41bf45813fd0adeffd9b54e1306c2022abe96514`.
**Sources:** lifecycle `79b90e4a57cbd1b738a9b9484677736d1b6415ab`; interval repair `7a256ed4873155dfad86faf2464110ee6f1e2ad4` (code `dde8287a806a802cd8d6a3dc122870f8cf8c5c3a`; historical `bdadbc57c...` preserved); later-event `76fdb624afc7674f088d10c349bfe15ffd0b865a`.
**Grade:** `TEST_ONLY_SOURCEFREE_P2_PRODUCT_FANIN_NOT_NATIVE`.
**Result:** 7 fanin tests and 6 affected interval-repair tests pass; cold CLI sequence passes; one S47 root; zero help attempts on observation; explicit do-help is the single action.

## Added

- Exact import of the three additive `WORKER_RETURNS` source directories, with evidence preserved and tree hashes recorded.
- `P2ProductFanin`: one compatible S47 root with accepted lifecycle boundary, explicit interval input, and later-event source-bound admission/read.
- `run_fanin_cli.py`: actual throughline CLI with `new`, `view`, `say`, `do-help`, `attend`, `exit`, `return`, `status`, `lifecycle`, `interval`, `later-event`, `opportunity`, `verify`.
- Focused tests/evidence for positive ACTUAL, SCHEDULED_ONLY contrast, attempt-vs-observation, ATTEND no world activity, outside block/local return, cut/restore, UNKNOWN/refusal, privacy and cold CLI.

## Semantics

- `OUTSIDE` blocks only user encounter actions; local `RETURN` restores `PORTAL` with no canonical actor/world mutation.
- Explicit interval is supplied input, not WAIT/absence-caused actor choice.
- Later-event observation is not a user attempt. Only explicit `do-help` performs user DO_HELP.
- Historical interval `admit_continuation` auto-called `do_help`; repair `7a256ed4` makes it observation-only and adds separate `explicit_do_help`. Fanin avoids `admit_continuation`; its callsite did not need change and explicit do-help remains the accepted lifecycle action. The repaired cut is AUTHOR_TESTED pending independent review.

## Not changed

No accepted base/vendor/projection/PR697 edits, no PROGRAMMA working-file changes, no native/science/human/B grant, no fabricated absence/activity/delivery or actor reaction.

## Holds

Independent review of this fanin is NOT_RUN; latter2 review separately pending; inherited full estate NOT_RUN; no self-acceptance.
