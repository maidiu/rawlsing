# SOROK P2 EXPLICIT INTERVAL + LATER EVENT — INDEPENDENT REVIEW

## VERDICTS (separate per exact commit)

- `bdadbc57c2664d3155a97853422e74b6128261f8` (explicit interval; branch head includes code parent `84d6354f829f98655025bd26237eb2a2f878f978`) — **REVISE**.
- `76fdb624afc7674f088d10c349bfe15ffd0b865a` (later event) — **REVISE**.
- Base `41bf45813fd0adeffd9b54e1306c2022abe96514` accepted41bf scope is preserved; no product/guide/protected-branch edit was made.

## COMMANDS AND RESULTS

Snapshot made only under `.local-logs/p2-interval-later-review/` from committed git objects (accepted product/projection at `41bf`, plus the two new return directories). No author runtime cache or `/tmp` path was used.

```text
git archive 41bf45813 -- WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1   WORKER_RETURNS/SOROK-S45-S47-PROJECTION-20261105-R1 | tar -x -C <snapshot>
git archive bdadbc57c -- WORKER_RETURNS/SOROK-P2-EXPLICIT-INTERVAL-FLOW-20261105-R1 | tar -x -C <snapshot>
git archive 76fdb624a -- WORKER_RETURNS/SOROK-P2-LATER-EVENT-CONTINUATION-20261105-R1 | tar -x -C <snapshot>

SOROK_P2_BASE_ROOT=<snapshot> TMPDIR=$PWD/.local-logs/p2-interval-later-review/pytest-tmp-explicit PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider   --junitxml=.local-logs/p2-interval-later-review/explicit_interval_6.xml   <snapshot>/WORKER_RETURNS/SOROK-P2-EXPLICIT-INTERVAL-FLOW-20261105-R1/tests
# 6 passed in 69.87s

TMPDIR=$PWD/.local-logs/p2-interval-later-review/pytest-tmp-later PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider   --junitxml=.local-logs/p2-interval-later-review/later_event_5.xml   <snapshot>/WORKER_RETURNS/SOROK-P2-LATER-EVENT-CONTINUATION-20261105-R1/tests
# 5 passed in 99.41s

PYTHONDONTWRITEBYTECODE=1 python3 -B .local-logs/p2-interval-later-review/probe_interval_later.py
# probe overall false: both findings below reproduced; later causal checks passed
```

## WHAT PASSED

- WAIT alone: `HELD`, `WAIT_UNSUPPORTED_TYPED_HOLD`, no clock/world/event/store change.
- ABSENCE alone: `HELD`, `USER_ABSENCE_LIFE_ADVANCE_MISSING`, no advance (6-test suite).
- ACTUAL interval really changes S42 material/C9: material `1 -> 0`, C9 material ineligible, later events admitted/performed.
- SCHEDULED_ONLY retains material `1`, C9 material eligible.
- S47 C9 used the exact interval source hash for later admitted events; event-local source remained exact cold.
- Later event 3 history contains later event 2's actual event ref, not a label; event 2 identity/source remained intact after event 3.
- Root stayed the same across ACTUAL/SCHEDULED and cold; cut `S46_INTERVAL_CONDITION_REVOKED`, no later event appended, restore used the same source, cold verify passed.
- Later projected `say/do_help/attend/view` nested results contained no private-key hits.

## FINDING 1 — bdadbc57 REVISE: continuation generates an actual user DO_HELP

`p2_explicit_interval_flow.continuation.admit_continuation()` unconditionally calls `adapter.do_help()` after `admit` and `c9`. This is not merely a projected continuation: it invokes the real user DO_HELP attempt and changes canonical state.

Reproducer (state A versus state B; same fresh root/seed, same ACTUAL interval):

```text
state A: product interval ACTUAL span 4 -> product admit
state B: run_explicit_interval_flow.py continue --request WAIT --mode ACTUAL --span 4
```

Observed:
- A encounters: `[]`; B encounters: `["DO_HELP"]`.
- B contains one extra user event; B canonical store hash differs from A.
- B result contains `do_help.user_attempt.control = "DO_HELP"`, `attempted=true`; ACTUAL refusal still performs the user attempt, SCHEDULED_ONLY actually accepts and actor `REPAIR` is performed.
- The source `request` remains WAIT/ABSENCE and the supplied `mode` is interval input, not actor intent; the defect is the unconditional user action, not mode masquerading as intent.

Narrow repair:
- Remove `adapter.do_help()` from `admit_continuation`; return only interval/admit/C9/view (or `view_before_do_help`).
- If a DO_HELP consequence is required, require an explicit user action flag/call (`project_do_help`/CLI `do-help`) or a clearly labeled scenario command; do not generate it from a continuation request.
- Secondary privacy/evidence: public result uses key names `admission` and `c9` (values are redacted summary fields), which a strict projection privacy walker flags; rename/redact these public keys if the walker applies. The explicit `evidence/result.json` authored-file list also references a generated `p2_explicit_interval_flow/__pycache__/continuation.cpython-311.pyc` that is absent from the committed tree; exclude `__pycache__` and recompute the receipt.

## FINDING 2 — 76fdb624 REVISE: private engineering state in CLI output; scenario calls user DO_HELP

The primitive continuation (`produce_input_interval` + `admit_later_event`) does **not** call DO_HELP: two later-event admissions yielded zero encounter records. However, the advertised `positive` scenario/CLI calls `project_do_help()` unconditionally, generating an actual user DO_HELP attempt.

The `positive` CLI/report also prints private engineering state: 61 projection privacy-walker hits across `c9`, `s43.plan_hash`, `s43.source_event_id`, `s43.private_generation_sources_in_plan`, `history_refs`, `readset_refs`/selected refs, `target_proposals`, `attempt_status`, and root identity. The nested projected `say`, `do_help`, `attend`, and `view` results themselves were clean (0 private-key hits).

Reproducer:

```text
cd <snapshot>/WORKER_RETURNS/SOROK-P2-LATER-EVENT-CONTINUATION-20261105-R1
PYTHONPATH=$PWD python3 -B -m p2_continuation.cli positive --state <fresh-state>
# ok=true causal chain; output contains 61 privacy-walker hits in engineering fields
# positive scenario calls project_do_help; primitive admit_later_event does not
```

Narrow repair:
- Redact/gate engineering `c9`/`s43`/history/plan/source/root fields from CLI/API outputs; expose only public projection results or a public summary.
- Separate the `positive`/`scheduled` scenario commands from any user-facing continuation, or require an explicit user DO_HELP flag/action. The primitive causal chain can remain unchanged.

## LIMITS / NOT RUN

- Full inherited 55-test estate was not rerun. No broad source census was performed; only the two new returns' focused source lists were checked.
- No native C8/C9/C12, CAN008/CAN011, ADP, Pyat, human validation, absence/life simulation, external delivery, provider/model call, tamperproof security, general concurrency or protected PRE-MAIN write was attempted or accepted.
- The later-event privacy finding applies to the engineering CLI/report surface; projected nested results were clean. If `positive` is formally declared evidence-only and never user-facing, that part may be re-scoped by the owner, but the current CLI prints it.
- This return is independent review evidence, not self-acceptance.

## EVIDENCE

- `READBACK.json` — exact heads, hashes, verdicts.
- `PROGRAMMA_DELTA.json` / `.md` — compact owner-intake delta.
- `evidence/FOCUSED_INTERVAL_6_TESTS.*`, `evidence/FOCUSED_LATER_5_TESTS.*` — focused test runs.
- `evidence/INTERVAL_FINDINGS.json`, `evidence/LATER_FINDINGS.json` — redacted findings; no private plan/source/history values copied.
- `evidence/CLI_REPROS.json` — exact CLI reproductions.
- `evidence/NEW_SOURCE_AUDIT.json`, `evidence/SOURCE_HEAD.json` — focused source/head checks.
