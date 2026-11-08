# P6 cold-reopen CLI demo

Frozen draft779 runtime: `41b21babf72c4c8b0b4b012d3c8b7d7f6247791f`.

This directory contains one connected, ordinary-CLI P6 encounter. Every P6 command is a
separate OS process against the same persisted state, so every invocation cold-reopens and
validates the checkpoint. The checked-in `TRANSCRIPT.md` is generated from actual command
stdout and actual `p4_receipts.json` turns; narration and receipt lines are not authored.

## Copy/paste run

From the repository root:

```sh
PY=/private/tmp/rawlsing-oct28-p1r1/venv/bin/python
STATE=$(mktemp -d /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/p6-cold-demo.XXXXXX)
PYTHONDONTWRITEBYTECODE=1 "$PY" \
  WORKER_RETURNS/SOROK-P6-COLD-DEMO-20261107-R1/run_demo.py --state "$STATE"
```

`run_demo.py` writes `TRANSCRIPT.md`, `actual_run.jsonl`, and `house_history.json` in this
directory (replacing the checked-in transcript with the new actual run). The state stays in
the bounded scratch directory printed by the script. No runtime, source, progress, PR779,
protected, or shared file is edited.

## Encounter covered

1. `new`, then `view`: orientation at the workshop.
2. `say "I can wait while you finish that."`: Nadia continues an actual material task; the
   transcript shows her repair narration, the S46 interval, material `2 -> 1`, and clock advance.
3. `go living room`: actual room entry with a MOVE receipt.
4. `look coaster`: a banal close observation.
5. `look sandals`: close detail with blue thread.
6. `look photo`: matching blue thread in the photograph.
7. `go workshop`, `view`: return and revisit the workshop.
8. `say "I'll leave the mug alone for now."`: explicit choice; no `look mug` command occurs.
9. `go living room`, `view`: revisit the living room.
10. Read-only house evidence: sandals `strap-repair`, photo `photo-exposure`, and
    `photo-exposure.depends_on=["strap-repair"]` with their actual clocks.

The leave-alone check derives looked-at objects from actual receipts: coaster, sandals, and
photo were looked at; bench and mug were not.

## Files

- `run_demo.py`: runnable driver; invokes `run_p6.py` once per command via `subprocess`.
- `inspect_state.py`: read-only P6 house-history evidence helper.
- `TRANSCRIPT.md`: actual run with commands, exits, process times, environment, concise
  human-facing output, and material/time receipts.
- `actual_run.jsonl`: raw command records with full stdout/stderr, parsed output, receipt
  summaries, start times, and elapsed seconds.
- `house_history.json`: actual house history and object material read from the run state.

## Actual producer -> consumer ownership map

- `run_p6.py:experience` (CLI producer) -> `run_p5` re-exports `run_p4.act` and P5 pacing ->
  `speech.admit_speech` / `response.read_response` / `response.express` (actor producers) ->
  P2/P3 world store and `p4_receipts.json` (persisted producer material).
- `run_p4.act` (turn/ledger producer) -> `run_p5.surface` -> `run_p6.experience`
  (invitation/candidate consumer) -> `gaze.render` and `attention.select` -> CLI stdout.
- `run_p6.house.establish` / `perform` / `close_on_repair` (P6 checkpoint producer) ->
  `read_house` / `scene` / `gaze.render` (P6 consumer).
- `pacing.advance_for_action` (S46 interval receipt producer) -> P4 ledger receipt ->
  `run_demo.py` transcript receipt consumer.
- `attention.register` / `save` (`p6_gaze.json` producer) -> `attention.select` (private
  detail-selection consumer). This private profile does not produce actor input.

## Evidence scope and missing handoff

- Scope: sourcefree, test-only, actual received P6/P5/P4/P3 code and actual persisted state
  receipts. This is a demo, not native validation.
- Not claimed: native science, actor authority, human acceptance, PR779 merge, protected
  merge, shared-progress edit, or source/authority edit.
- Recognition is a separate in-flight patch and query-order is a separate proof. Neither is
  exercised or claimed here.
- No necessary interaction failed in the recorded run. If one fails, `run_demo.py` records
  the exact command, stdout, stderr, exit, and time, stops, and exits non-zero; it does not
  auto-repair. Any minimal repair belongs outside the frozen runtime and outside this demo.
