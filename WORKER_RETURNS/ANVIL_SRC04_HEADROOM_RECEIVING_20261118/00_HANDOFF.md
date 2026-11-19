# SRC04 compact-run headroom receiving snapshot

## Verdict

**Disk headroom: PASS at the final observed snapshot.**

**Safe launch: HOLD for custody/freeze review.**
No source was opened, no writer was launched, no stopped file was copied or
deleted by this receiving step, and no guard was reduced.

## Exact free-space reconciliation

Intended volume: `/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117`
(and `MEASUREMENT_PREP/private-runtime`, same filesystem).

Final observed snapshot `2026-11-19T00:58:54.443676+00:00`:

- free: **44,723,630,080 B** (41.65 GiB)
- startup working-room floor: **26,907,826,727 B**
- startup margin: **17,815,803,353 B**
- in-flight free floor: **8,589,934,592 B**
- current margin over full R3 terminal stage: **18,045,149,544 B**

The startup and in-flight floors are separate. Passing the 8 GiB in-flight floor
does **not** mean the 26.91 GB startup gate passed; at this snapshot both pass.

## Composition of the existing floor

The exact compact caller/runner at `e35a9c79ea02035d9345d70205a3373ffeded913`
uses:

- R3 terminal stage: **26,678,480,536 B**
- duplicate replay journal: **8,360,588,401 B**
- practical staging budget: **18,317,892,135 B**
- plus startup reserve: **8,589,934,592 B**
- startup floor: **26,907,826,727 B**
- in-flight floor: **8,589,934,592 B**
- RAM cap: **6,442,450,944 B**

The remaining practical staging is one projection spool plus one writer stage,
not the duplicate journal. R3 terminal file composition:

| remaining/duplicate component | bytes |
|---|---:|
| `.s2b-direct-stage-t6pz7m04.tmp` incomplete SQLite stage | 13,810,065,408 |
| `.s1e-body-journal-wwfwjnoy` (single-pass removes this duplicate) | 8,360,588,401 |
| `.s1e-i02-spool-6iefwk6i` | 4,505,034,543 |
| `.s2b-direct-stage-t6pz7m04.tmp-journal` | 2,792,184 |
| **R3 terminal total** | **26,678,480,536** |

The ~13.8 GB incomplete SQLite stage was present at the first observation.
During this bounded receiving step, a separate external process (PID 7340,
not this return) removed the stopped private scratch. At the final snapshot the
stage path is absent and the private run directory retains only receipts/logs
(12 KB). This return did not copy, delete, or alter those stopped files. That
external change is a **custody/freeze issue** for receiving, not a reason to
lower any guard.

## Phase actually bounded by existing evidence

- **R3**: bounds the in-flight writer staging phase only, through
  `FREE_FLOOR_BREACH` at 26,678,480,536 B terminal stage. It did **not** reach
  Parquet publication, a complete estate, or a cold reader. Terminal ingest had
  2,194,021 complete lines, routing at 887,855/1,298,649, no later coordinate
  family lines, and no committed SQLite census.
- **Width512 success**: bounds a synthetic full writer publication at
  1,313.718 s, peak scratch 3,303,748,113 B, retained 220,252,287 B. It is not
  original SRC04 and does not bound the 13.8 GB original writer stage.
- **Writer cap timing**: bounds a 512×600 proof stage to `WALL_600S` with sink
  add 117.1075 s and unattributed proof residual ~475.4275 s; no publication.
- The `e35a` compact runner’s tiny fixture compression shows exact payload/roots
  parity, but its ~93% fixture saving is **not** applied to reduce the full-scale
  guard.

## Existing authorized arguments and destination

Existing pinned inputs (read-only reuse):

- candidate tree:
  `/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/evidence/anvil-src04-candidate-31rqm9z_/candidate`
- candidate patch file:
  `OWNER/WORKER_RETURNS/ANVIL_ALL35_CONSTRUCTION_ONLY_CANDIDATE_20261118/candidate.patch`
  SHA-256 `ffa4520f965e4f2fd22ea5043d0c80528f44a47f94afdb763d3b77c21ca3a08f`
- base config:
  `IMPLEMENTER/WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/inputs/SRC04/source.config.repaired.v2.json`
  SHA-256 `5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5`
- private final runtime config:
  `MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/SRC04.post_alignment.runtime.config.json`
  SHA-256 `dd5cf699070eaf3c528d97bd126d7bfd8166a7885010b0b95202cdf00ab34421`;
  canonical `ba886d87763fdeb4d91df784b9672d6604081c9eaf81fd9ef6b3d334d4a387e0`
- binding dir:
  `MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118`
- private runtime destination:
  `MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438`
  (directory mode `0700`; config mode `0600`)
- source path is supplied only by the exact grant binding; `--authorized-source-launch`
  remains required.
- Existing caller README's `--work-root` is a placeholder; the exact private
  work-root for a successor run is not uniquely frozen in the existing return.
  This must be supplied by the authorized owner; it is not inferred here.

## Safe-launch statement

**Do not launch from this receiving return.** Disk headroom now passes, but:
- this commission forbids a source launch;
- the stopped R3 private scratch was externally removed during observation, so
  the frozen stopped-file custody premise is not stable;
- the exact launch work-root is not frozen in existing evidence.

The next operation, if authorized by the competent owner, is a single exact-head
preflight against the existing caller with the above inputs, after custody owner
confirms the cleanup and supplies the exact private work-root. No guard change or
new experiment is authorized.

## Status

- `disk_headroom`: PASS at final snapshot
- `startup_floor`: 26,907,826,727
- `in_flight_floor`: 8,589,934,592
- `safe_launch`: HOLD for custody/work-root freeze
- `source_access`: none
- `writer_launch`: none
- `stopped_file_copy_or_delete_by_this_return`: none
- `new_experiment_or_benchmark`: none
- `guard_reduced`: false
- `optimization_handoff`: none beyond the already-evidenced single-pass removal
  of the duplicate journal; its tiny fixture compression is not a guard basis.
