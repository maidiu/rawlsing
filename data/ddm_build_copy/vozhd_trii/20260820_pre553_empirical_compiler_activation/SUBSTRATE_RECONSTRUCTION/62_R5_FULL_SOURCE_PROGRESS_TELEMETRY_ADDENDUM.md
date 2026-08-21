# VOZHD TRII — R5 FULL-SOURCE PROGRESS TELEMETRY ADDENDUM

Status: `BINDING_EXECUTION_TELEMETRY_ADDENDUM__NO_SEMANTIC_EFFECT__NO_CANDIDATE_MUTATION`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Binding parent:

- `61_R5_BOUNDED_ACCEPTANCE_AND_FULL_WVS7_LITS1_REAL_SOURCE_COURT_AUTHORITY.md`

This addendum changes no semantic, physical-carrier, integrity, replay, query, discovery, admission, resource, or acceptance law. It adds only bounded live execution telemetry so a long full-source court can truthfully report `this-far / this-much` while it is running.

---

## 0. BRANCH / AUTHORITY READ LAW

The two full-source court branches were intentionally cut from receipt-closure HEAD:

`46a9d35d0edecc7dc9182038baeb0d0748c50fdc`

before Authorities 61 and 62 were committed on the control branch.

Therefore workers SHALL NOT mutate or rebase the frozen court branches merely to copy authority prose into them.

After checking out the exact court branch/HEAD, workers must read Authorities 61 and 62 directly from:

`agent/vozhd-trii-pre553-substrate-reconstruction-control`

for example via an exact read such as:

`git show agent/vozhd-trii-pre553-substrate-reconstruction-control:<authority-path>`

or another read-only equivalent.

The court branch exact starting HEAD remains `46a9d35d0edecc7dc9182038baeb0d0748c50fdc` and frozen implementation remains `36bf351dda12f0aa93c9ff426ae54d80143d0bf9`.

---

## 1. REQUIRED LIVE PROGRESS SURFACES

Each full-source worker SHALL maintain, in worker-private scratch during execution:

1. `PROGRESS_LOG.jsonl` — append-only machine-readable heartbeat history;
2. `PROGRESS_LATEST.json` — atomically replaced latest heartbeat snapshot;
3. one concise human-readable heartbeat line written to stdout at the same cadence.

These are execution telemetry only.

They are NOT semantic authority, expected truth, replay authority, integrity authority, acceptance evidence by themselves, or a correctness-bearing cache.

Loss/corruption of progress telemetry may not change empirical results. If telemetry writing itself fails, record the telemetry failure and continue only if the court's correctness path is unaffected.

No corpus-sized progress structure may be retained in memory.

---

## 2. HEARTBEAT CADENCE

Emit an immediate heartbeat:

- at court start;
- after source identity verification;
- at every phase transition;
- immediately before and after seal/promote/reopen/audit/query/discovery/admission/replay/cleanup boundaries;
- on any warning/tripwire/failure/exception;
- at successful completion.

During a long-running phase, emit a heartbeat whenever EITHER is reached first:

- `60 seconds` since the previous heartbeat; OR
- `500,000` additional physical cells/events processed in a countable event phase.

For phases not naturally counted in events, use the 60-second heartbeat and the phase-native bounded counter described below.

Heartbeat generation must be O(1) bounded telemetry and must not trigger full rescans merely to compute progress.

---

## 3. REQUIRED HEARTBEAT FIELDS

Every JSON heartbeat SHALL contain at least:

- `timestamp_utc`;
- `source` (`WVS7` or `LITS_I`);
- `court_branch`;
- `candidate_commit`;
- `phase`;
- `phase_ordinal`;
- `phase_count`;
- `elapsed_seconds_total`;
- `elapsed_seconds_phase`;
- `status` (`RUNNING`, `PASS_PHASE`, `WARNING`, `BLOCKED`, `FAILED`, `COMPLETE`);
- `current_rss_bytes` where measurable;
- `peak_rss_bytes` so far;
- `persistent_cache_count` (must remain `0`);
- `worker_count` (must remain `1` unless higher authority changes it).

Where a phase has a governed total, also include:

- `units_name`;
- `units_done`;
- `units_total`;
- `fraction_done`;
- `percent_done`.

For source traversal/build, `units_name` SHALL be `physical_cells_events` and totals are frozen by Authority 61:

- WVS7: `59,595,860`;
- LiTS I: `34,744,396`.

Also include when available without extra unbounded work:

- `source_rows_done` / `source_rows_total`;
- `variables_total`;
- `members_closed`;
- `canonical_bytes_written_so_far`;
- `staging_bytes_so_far`;
- `scratch_bytes_so_far`;
- `throughput_units_per_second_recent`;
- `eta_seconds_estimate`.

`eta_seconds_estimate` is explicitly NONAUTHORITATIVE and may be null until enough recent throughput exists.

---

## 4. PHASE-NATIVE PROGRESS COUNTERS

Use the strongest truthful denominator available without changing execution.

At minimum:

### SOURCE_VERIFY / HOSTILE_MICROPROOF
Report file/hash/shape verification substep and hostile microproof completion state.

### DECODE_BUILD
Report physical cells/events processed over the exact full-source frontier, plus rows processed where available.

### SEAL_INVENTORY / INACTIVE_PROMOTE / SEALED_REOPEN
Report members completed/total when total is known; otherwise members completed plus named substep.

### FULL_AUDIT
Report audited canonical rows/events over sealed canonical logical count.

### I03
Report frozen hostile I03 cases completed/total.

### BLIND_I05
Report frozen blind-frontier candidates completed/total only after the candidate/physical-root/config/workload-disclosure freeze and blind selector commitment required by Authority 61. Progress telemetry MUST NOT reveal or alter any pre-commitment blind selection process.

### I04
Report frozen I04 cases completed/total.

### REPLAY_RECONSTRUCTION
Report selected hostile replay/reconstruction cases completed/total.

### INTEGRITY_FAULTS
Report frozen fault cases completed/total.

### CLEANUP
Report named cleanup substeps and final absence/presence of prohibited persistent stores/carrier residue.

---

## 5. HUMAN-READABLE STDOUT HEARTBEAT

At each heartbeat, print one concise line suitable for a user watching the worker, e.g.:

`[R5/WVS7][DECODE_BUILD] 12,400,000 / 59,595,860 events (20.81%) | rows 20,229/97,220 | RSS 412 MiB peak 438 MiB | canonical 286 MiB | elapsed 00:31:42 | recent 7,900 ev/s | ETA ~01:39:00`

The exact formatting may differ, but it must visibly answer:

- what phase is running;
- how much is done;
- how much total exists when known;
- percent complete when meaningful;
- elapsed time;
- current/peak RSS;
- current storage progress where meaningful.

Do not spam one line per row/event.

---

## 6. FAILURE / INTERRUPTION LAW

On any block, tripwire, exception, external termination, or controlled stop:

1. append one final `BLOCKED` or `FAILED` heartbeat if possible;
2. atomically update `PROGRESS_LATEST.json`;
3. preserve the progress log as court evidence if small and safe;
4. do not convert a partial frontier into a pass;
5. report exact `units_done / units_total` and last completed phase/substep.

A progress line is never permission to resume from a partial canonical artifact unless an explicit resumability authority exists. Current full-source courts assume fresh exact execution unless Authority 61 separately permits otherwise.

---

## 7. FINAL RECEIPT / COMMIT LAW

At normal completion or court block, commit a small final copy under the relevant source-specific receipt directory:

- `PROGRESS_LOG.jsonl`;
- `PROGRESS_FINAL.json`.

`PROGRESS_FINAL.json` shall summarize:

- final disposition;
- total elapsed time;
- phase timings;
- exact final frontier reached;
- peak RSS;
- canonical/staging/scratch peak bytes;
- member count;
- whether every required phase reached completion;
- whether prohibited persistent storage/cache count remained zero;
- cleanup disposition.

If the raw heartbeat log becomes unexpectedly large, commit a bounded complete or phase-sampled log plus its byte length/SHA-256 and preserve the full worker-private copy through adjudication. Under the mandated cadence it should normally remain small.

---

## 8. NO CHANGE TO ACCEPTANCE LAW

This addendum adds observability only.

All pass/block/resource/runtime/equivalence/integrity dispositions remain exactly governed by Authority 61.

The progress logger may observe the candidate/court; it may not become part of the candidate's semantic or correctness path.

Required acknowledgment in each worker return:

`R5_FULL_SOURCE_PROGRESS_TELEMETRY_COMPLIED`
