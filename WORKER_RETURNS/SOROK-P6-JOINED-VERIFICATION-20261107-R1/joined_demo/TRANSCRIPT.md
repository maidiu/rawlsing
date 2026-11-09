# Actual P6 cold-reopen CLI run

- Frozen runtime: `41b21babf72c4c8b0b4b012d3c8b7d7f6247791f`
- Runtime path: `<REDACTED_WORKTREE>/WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py`
- Started: 2026-11-08T00:52:48+00:00
- State: `<EPHEMERAL_STATE>`
- Output: `<REDACTED_WORKTREE>/WORKER_RETURNS/SOROK-P6-JOINED-VERIFICATION-20261107-R1/joined_demo`
- CWD: `<REDACTED_WORKTREE>`
- Python: `<PYTHON_BINARY>` (3.11.3)
- Platform: `macOS-13.7.8-x86_64-i386-64bit`
- Environment: `PYTHONDONTWRITEBYTECODE=1`; no source or runtime edits.
- Every P6 command below is a separate OS process; each invocation validates the cold checkpoint.

## Commands and actual user-visible output

### 1. new

```text
$ <PYTHON_BINARY> <REDACTED_WORKTREE>/WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py --state <EPHEMERAL_STATE> new
```

`exit 0 | 8.16s`

clock 248; room workshop
A doorway leads from the workbench into the living room.
available: bench, mug
detail: The bench stands beside the doorway.
  The finishing worker is already at the workshop bench.
  You come up the stairs and stop at the open workshop door.

### 2. orientation

```text
$ <PYTHON_BINARY> <REDACTED_WORKTREE>/WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py --state <EPHEMERAL_STATE> view
```

`exit 0 | 3.52s`

clock 248; room workshop
A doorway leads from the workbench into the living room.
available: bench, mug
detail: The bench stands beside the doorway.
  The finishing worker is already at the workshop bench.
  You come up the stairs and stop at the open workshop door.

### 3. Nadia works while the user waits

```text
$ <PYTHON_BINARY> <REDACTED_WORKTREE>/WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py --state <EPHEMERAL_STATE> say 'I can wait while you finish that.'
```

`exit 0 | 7.58s`

clock 249; room workshop
A doorway leads from the workbench into the living room.
available: bench, mug
detail: The bench stands beside the doorway.
  You say, “I can wait while you finish that.”
  Nadia makes a repair.
admission: ADMITTED

receipt: SAY 'I can wait while you finish that.'; clock 248 -> 249
  P4 speech: ADMITTED; request_edge=False; text='I can wait while you finish that.'
  uptake: PERCEIVED_NO_INSPECTION_REQUEST; mode=None
  material/time: REALIZED 248 -> 249; material 2 -> 1; free_hours 11 -> 10
  actual action event: TEST_ONLY_BP4_WORLD_EVT_c472b0e2d10720d0689c53ee6fa2c5886709aec673691a2a7e60b7d828e7c7a7

### 4. room entry

```text
$ <PYTHON_BINARY> <REDACTED_WORKTREE>/WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py --state <EPHEMERAL_STATE> go 'living room'
```

`exit 0 | 9.05s`

clock 250; room living room
The workbench is through the doorway. A low shelf runs along the wall.
available: coaster, photo, sandals
detail: A round cork coaster lies on the shelf.
  You go into the living room.
admission: ADMITTED

receipt: GO living room; clock 249 -> 250
  performed MOVE: You go into the living room.
  material/time: REALIZED 249 -> 250; material 1 -> 0; free_hours 10 -> 9
  actual action event: TEST_ONLY_BP4_WORLD_EVT_f58c299840118f5d21ca3ac703242e24db7d80e21c8ccd85cf54e7531833dced

### 5. banal observation

```text
$ <PYTHON_BINARY> <REDACTED_WORKTREE>/WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py --state <EPHEMERAL_STATE> look coaster
```

`exit 0 | 11.70s`

clock 253; room living room
The workbench is through the doorway. A low shelf runs along the wall.
available: coaster, photo, sandals
detail: A round cork coaster lies on the shelf.
  A shallow ring marks the cork.
admission: ADMITTED

receipt: INSPECT_OBJECT coaster; clock 250 -> 253
  performed INSPECT: A shallow ring marks the cork.
  material/time: NOT_PERFORMED 250 -> 253; material 0 -> 0; free_hours 9 -> 9
  interval reason: MATERIAL_EXHAUSTED

### 6. sandals linked history

```text
$ <PYTHON_BINARY> <REDACTED_WORKTREE>/WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py --state <EPHEMERAL_STATE> look sandals
```

`exit 0 | 15.02s`

clock 256; room living room
The workbench is through the doorway. A low shelf runs along the wall.
available: coaster, photo, sandals
detail: A pair of brown sandals lies beneath the shelf.
  Blue thread crosses the left strap. The cork at the heel is dark.
admission: ADMITTED

receipt: INSPECT_OBJECT sandals; clock 253 -> 256
  performed INSPECT: Blue thread crosses the left strap. The cork at the heel is dark.
  material/time: NOT_PERFORMED 253 -> 256; material 0 -> 0; free_hours 9 -> 9
  interval reason: MATERIAL_EXHAUSTED

### 7. photo linked history

```text
$ <PYTHON_BINARY> <REDACTED_WORKTREE>/WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py --state <EPHEMERAL_STATE> look photo
```

`exit 0 | 17.26s`

clock 259; room living room
The workbench is through the doorway. A low shelf runs along the wall.
available: coaster, photo, sandals
detail: A photograph leans against the wall on the shelf.
  In the photograph, brown sandals lie on a step. Blue thread crosses the left strap.
admission: ADMITTED

receipt: INSPECT_OBJECT photo; clock 256 -> 259
  performed INSPECT: In the photograph, brown sandals lie on a step. Blue thread crosses the left strap.
  material/time: NOT_PERFORMED 256 -> 259; material 0 -> 0; free_hours 9 -> 9
  interval reason: MATERIAL_EXHAUSTED

### 8. return to workshop

```text
$ <PYTHON_BINARY> <REDACTED_WORKTREE>/WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py --state <EPHEMERAL_STATE> go workshop
```

`exit 0 | 20.36s`

clock 260; room workshop
A doorway leads from the workbench into the living room.
available: bench, mug
detail: The bench stands beside the doorway.
  You go into the workshop.
admission: ADMITTED

receipt: GO workshop; clock 259 -> 260
  performed MOVE: You go into the workshop.
  material/time: NOT_PERFORMED 259 -> 260; material 0 -> 0; free_hours 9 -> 9
  interval reason: MATERIAL_EXHAUSTED

### 9. revisit workshop

```text
$ <PYTHON_BINARY> <REDACTED_WORKTREE>/WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py --state <EPHEMERAL_STATE> view
```

`exit 0 | 13.58s`

clock 260; room workshop
A doorway leads from the workbench into the living room.
available: bench, mug
detail: The bench stands beside the doorway.
  You go into the workshop.

### 10. leave the mug alone

```text
$ <PYTHON_BINARY> <REDACTED_WORKTREE>/WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py --state <EPHEMERAL_STATE> say 'I'"'"'ll leave the mug alone for now.'
```

`exit 0 | 27.90s`

clock 261; room workshop
A doorway leads from the workbench into the living room.
available: bench, mug
detail: The bench stands beside the doorway.
  You say, “I'll leave the mug alone for now.”
admission: ADMITTED

receipt: SAY "I'll leave the mug alone for now."; clock 260 -> 261
  P4 speech: ADMITTED; request_edge=False; text="I'll leave the mug alone for now."
  uptake: PERCEIVED_NO_INSPECTION_REQUEST; mode=None
  material/time: NOT_PERFORMED 260 -> 261; material 0 -> 0; free_hours 9 -> 9
  interval reason: MATERIAL_EXHAUSTED

### 11. revisit living room

```text
$ <PYTHON_BINARY> <REDACTED_WORKTREE>/WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py --state <EPHEMERAL_STATE> go 'living room'
```

`exit 0 | 25.90s`

clock 262; room living room
The workbench is through the doorway. A low shelf runs along the wall.
available: coaster, photo, sandals
detail: A photograph leans against the wall on the shelf.
  You go into the living room.
admission: ADMITTED

receipt: GO living room; clock 261 -> 262
  performed MOVE: You go into the living room.
  material/time: NOT_PERFORMED 261 -> 262; material 0 -> 0; free_hours 9 -> 9
  interval reason: MATERIAL_EXHAUSTED

### 12. final view

```text
$ <PYTHON_BINARY> <REDACTED_WORKTREE>/WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py --state <EPHEMERAL_STATE> view
```

`exit 0 | 16.75s`

clock 262; room living room
The workbench is through the doorway. A low shelf runs along the wall.
available: coaster, photo, sandals
detail: A photograph leans against the wall on the shelf.
  You go into the living room.

### 13. read-only house history evidence

```text
$ <PYTHON_BINARY> <REDACTED_WORKTREE>/WORKER_RETURNS/SOROK-P6-COLD-DEMO-20261107-R1/inspect_state.py --state <EPHEMERAL_STATE>
```

`exit 0 | 11.05s`

## House history evidence

Epoch: 248; root: `d747d2c208fb0fe3610c9f08d728d5f358758feee6be5164e07475e4431950c6`

```text
bench-installation: object=bench clock=234 depends_on=[]
photo-exposure: object=photo clock=244 depends_on=['strap-repair'] depicts=sandals
strap-repair: object=sandals clock=239 depends_on=[]
```

## Leave-alone check

Looked at: coaster, sandals, photo.
Not looked at in this encounter: bench, mug.
The explicit leave-alone choice was the final say: "I'll leave the mug alone for now."

## Evidence and scope

- Raw command records, stdout/stderr and timings: `actual_run.jsonl`.
- House history: `house_history.json`.
- Scope: sourcefree, test-only, actual P6/P5/P4/P3 code and actual state receipts.
- Missing handoff: recognition is a separate in-flight patch and query-order is a separate proof; neither is claimed here.
- Not claimed: native science, actor authority, human acceptance, PR779 merge, protected/shared-progress edits.
