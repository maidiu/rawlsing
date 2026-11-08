# P6 cold-reopen CLI demo

Frozen draft779 runtime: `41b21babf72c4c8b0b4b012d3c8b7d7f6247791f`.

This directory contains one connected, ordinary-CLI P6 encounter. Every P6 command is a
separate OS process against the same persisted state, so every invocation cold-reopens and
validates the checkpoint. The checked-in `TRANSCRIPT.md`, `actual_run.jsonl`, and
`house_history.json` are the exact original demo recording from head
`5adcb372cfacea1281fe1a69f972a55bf0752992`; the portable replay driver does not modify them.

## Copy/paste run

From the repository root:

```sh
PY="${PY:-python3}"
PYTHONDONTWRITEBYTECODE=1 "$PY" \
  WORKER_RETURNS/SOROK-P6-COLD-DEMO-20261107-R1/run_demo.py
```

Use the checkout's existing interpreter, or set `PY` to a checkout-specific venv interpreter
if that is where the dependencies are installed. No worker-specific scratch path is required.
The driver prints the fresh `state:` and `output:` directories before running.

To choose the locations explicitly:

```sh
PY="${PY:-python3}"
PYTHONDONTWRITEBYTECODE=1 "$PY" \
  WORKER_RETURNS/SOROK-P6-COLD-DEMO-20261107-R1/run_demo.py \
  --out /path/to/new-empty-output --state /path/to/new-empty-state
```

Each run writes `TRANSCRIPT.md`, `actual_run.jsonl`, and `house_history.json` into the printed
output directory. By default that is a new OS temp directory outside the tracked evidence.
The driver refuses a non-empty output or state directory, and refuses the checked-in evidence
directory itself. No runtime, source, progress, PR779, protected, or shared file is edited.

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

- `run_demo.py`: portable replay driver; invokes `run_p6.py` once per command via
  `subprocess` and writes new evidence to a fresh output directory by default.
- `inspect_state.py`: read-only P6 house-history evidence helper.
- `TRANSCRIPT.md`: exact original run with commands, exits, process times, environment,
  concise human-facing output, and material/time receipts. Recorded timings remain visible,
  including the later 20.43s, 30.61s, and 30.75s processes.
- `actual_run.jsonl`: exact original raw command records with full stdout/stderr, parsed
  output, receipt summaries, start times, and elapsed seconds.
- `house_history.json`: exact original house history and object material read from the run
  state.

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

## Portable routing validation

A focused validation on the updated driver used one `new` command (not a replay of the
encounter):

- Default output resolved to a fresh OS temp directory outside this demo directory.
- Output equal to this checked-in evidence directory was refused.
- Pre-populated state and output directories were refused.
- The one-command routing run exited 0: `new` in 9.23s, house helper in 2.90s, and
  `TRANSCRIPT.md`, `actual_run.jsonl`, `house_history.json` were written only to the temp
  output.
- The three checked-in evidence files were byte-identical before and after:
  `11da7a804aa3603997716794802ac4a65a90f490b3a6eea6a3151f0499496493` (`TRANSCRIPT.md`),
  `7421fc2bd9dba4e08e3c00f39ec4943441d1eeb5e32101673e98b4f080924ae4` (`actual_run.jsonl`),
  `87ca6dd35cdf29a5d97598f5bce855b27313ab12b0d45d95332795c7f4336e53`
  (`house_history.json`).

The original 13-record encounter recording was reused unchanged; only output routing was
validated.

## Evidence scope and missing handoff

- Scope: sourcefree, test-only. P6/P5 are unreceived candidates; P4/P3 are protected. This
  uses their received code and actual persisted state receipts only. It is a demo, not
  native validation.
- The checked-in `TRANSCRIPT.md`, `actual_run.jsonl`, and `house_history.json` are the exact
  original demo head `5adcb372cfacea1281fe1a69f972a55bf0752992` recording, unchanged by this
  portable output-routing update.
- Not claimed: native science, actor authority, human acceptance, PR779 merge, protected
  merge, shared-progress edit, or source/authority edit.
- Recognition is a separate in-flight patch and query-order is a separate proof. Neither is
  exercised or claimed here.
- No necessary interaction failed in the recorded run. If one fails, `run_demo.py` records
  the exact command, stdout, stderr, exit, and time, stops, and exits non-zero; it does not
  auto-repair. Any minimal repair belongs outside the frozen runtime and outside this demo.
