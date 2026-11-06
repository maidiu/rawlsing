# SOROK P2 EXPLICIT INTERVAL REPAIR — INDEPENDENT CLOSURE

## VERDICT

- Exact repair `7a256ed4873155dfad86faf2464110ee6f1e2ad4` (code parent `dde8287a806a802cd8d6a3dc122870f8cf8c5c3a`) — **REVISE**.
- Historical `bdadbc57c2664d3155a97853422e74b6128261f8` REVISE remains unchanged.
- Base `41bf45813fd0adeffd9b54e1306c2022abe96514` accepted41bf scope is preserved; product changed files since 41bf: `0`.

The primary auto-help defect is fixed. Two original secondary closure items remain unfixed: public result key names still violate the applicable projection privacy boundary, and the authored-file receipt still lists nonexistent `__pycache__` entries.

## EXACT COMMANDS AND RESULTS

Snapshot made only under `.local-logs/p2-interval-repair-review/` from committed git objects: accepted product/projection at `41bf`, repair return at `7a256ed`. No author runtime cache, `/tmp`, or shared config was used.

```text
SOROK_P2_BASE_ROOT=<snapshot> TMPDIR=$PWD/.local-logs/p2-interval-repair-review/pytest-tmp PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider   --junitxml=.local-logs/p2-interval-repair-review/focused_repair_6.xml   <snapshot>/WORKER_RETURNS/SOROK-P2-EXPLICIT-INTERVAL-FLOW-20261105-R1/tests
# 6 passed in 66.42s

PYTHONDONTWRITEBYTECODE=1 python3 -B .local-logs/p2-interval-repair-review/probe_repair_oracle.py
# 13 checks pass; 2 fail: public_output_private_keys_absent, pycache_receipt_entries_absent

CLI:
run_explicit_interval_flow.py --base-root <snapshot> continue   --state <state> --request WAIT --mode ACTUAL --span 4
# CONTINUED; do_help=null; do_help_executed=false; user_attempt_executed=false;
# encounter_count 0 -> 0; encounters_unchanged=true; cold_continuity=true

run_explicit_interval_flow.py --base-root <snapshot> do-help   --state <state> --request WAIT
# DO_HELP_EXECUTED; do_help REFUSED/HELP_REFUSE; encounter_count 0 -> 1;
# do_help_executed=true; user_attempt_executed=true; cold_continuity=true
```

## PRIMARY REPAIR PASSES

- WAIT and ABSENCE without interval: HELD, no advance, `do_help=null`, `do_help_executed=false`, `user_attempt_executed=false`, no encounter/user attempt.
- Invalid/missing mode: HELD or REFUSED, no advance, no encounter.
- `apply_explicit_interval`: interval only, no encounter.
- `admit_continuation`/`continue_after_request` observation: CONTINUED, no automatic DO_HELP, encounter count unchanged (`0 -> 0`), cold continuity true.
- `explicit_do_help`: exactly one explicit user DO_HELP attempt per call; encounter count `0 -> 1`; ACTUAL REFUSED/HELP_REFUSE; SCHEDULED_ONLY OK/HELP_ACCEPT with actor REPAIR.
- ACTUAL/SCHEDULED material and C9 contrast preserved; cold continuity true; cut/restore remains covered by the 6 focused tests.
- Actual importer pinned to the snapshot package/projection; no product/source changes.

## REMAINING FAILURES / NARROW REPAIRS

1. **Public field privacy still violated.** Observation and explicit result outputs still contain top-level `admission` and `c9` keys. Both are in the accepted projection `PRIVATE_KEYS`; the values are redacted summaries, but the applicable privacy walker flags the exact paths `<root>.admission` and `<root>.c9` on observation, explicit-actual and explicit-scheduled results.
   - Narrow repair: rename these public fields (e.g. `admission_status`, `c9_public`) or omit them from the public result; keep any detailed engineering data in a separately labeled evidence channel.

2. **Pycache/nonexistent receipt entries still present.** `evidence/result.json` lists three missing files:
   - `p2_explicit_interval_flow/__pycache__/cli.cpython-311.pyc`
   - `p2_explicit_interval_flow/__pycache__/continuation.cpython-311.pyc`
   - `tests/__pycache__/test_explicit_interval_flow.cpython-311.pyc`
   None is present in the committed repair tree.
   - Narrow repair: exclude `__pycache__`/`.pyc` from the authored-file list and recompute the receipt.

## SCOPE / LIMITS / NOT RUN

- Later event `76fdb624afc7674f088d10c349bfe15ffd0b865a` remains separately REVISE; its new repair is running and is not reviewed here. Fan-in `579` candidate is not reviewed.
- No full inherited 55-test estate, no new framework, no unrelated probes. Only the exact 6 interval focused tests plus the original auto-help oracle.
- No product/guide/PROGRAMMA/protected-branch write; no native/human/C8/C9/C12/CAN008/CAN011/ADP/Pyat/absence/security/concurrency claim.
- This is independent review evidence, not self-acceptance.

## EVIDENCE

- `READBACK.json` — exact head/base/verdict and hashes.
- `PROGRAMMA_DELTA.json` / `.md` — compact owner-intake delta.
- `evidence/FOCUSED_6_TESTS.log` / `.xml` — focused repair tests.
- `evidence/INDEPENDENT_ORACLE.json` — original auto-help oracle checks; includes exact failing checks.
- `evidence/CLI_REPROS.json` — observation and explicit-do-help CLI results.
- `evidence/RECEIPT_AND_PRIVACY_AUDIT.json` — exact private keys and missing receipt entries.
- `evidence/SOURCE_HEAD.json` — head, code parent, historical bdad, base, importer origins.
