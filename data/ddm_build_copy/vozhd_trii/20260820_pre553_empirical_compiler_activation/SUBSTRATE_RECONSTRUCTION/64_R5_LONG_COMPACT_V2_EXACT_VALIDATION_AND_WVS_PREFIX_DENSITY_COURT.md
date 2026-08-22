# VOZHD TRII — R5 LONG COMPACT V2 EXACT VALIDATION & WVS PREFIX DENSITY COURT

Status: `AUTHORIZED__EXECUTION_ONLY__FROZEN_COMPACT_V2__NO_REPAIR_IN_COURT`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Binding parent:

`63_R5_WVS7_RESOURCE_FAILURE_AND_LONG_COMPACT_ENCODING_REPAIR_AUTHORITY.md`

Validation branch:

`agent/vozhd-trii-r5-long-compact-v2-validation`

Exact validation-branch starting HEAD:

`568e63367cb8871c4b06d43aa5fcb04ead4d4835`

Frozen compact V2 implementation head:

`b643ea6ea08a6ed29e31453135ac9113286d581d`

The commits after `b643ea6...` contain only repair receipt and post-freeze court tests. No candidate implementation code changed after the blind-I05 freeze point.

## 0. MISSION

Independently execute the repaired compact LONG_SHARDED V2 candidate in a trustworthy real Rawlsing checkout.

This cell has **zero design or repair authority**.

It may only:

1. verify branch/head/write scope;
2. run the complete relevant R5 regression/court surface;
3. execute the exact WVS real-source prefix density court at 250k / 1M / 2M physical cells under the decision law below;
4. write small receipts/progress evidence;
5. stop and return a minimal witness on any failure.

Do not modify candidate or accepted runtime.

## 1. READ-FIRST LAW

Read from the control branch before execution:

- Authority 56;
- Authority 57;
- Authority 61;
- Authority 62;
- Authority 63;
- this Authority 64.

The validation branch was cut from the repair branch before Authority 64 existed. Do not rebase merely to obtain the authority file; read it directly from the control branch with `git show`.

## 2. FROZEN WRITE LAW

READ-ONLY during validation:

- all `rawlsing_next/pre553_r5_*.py`;
- all existing accepted PRE553 runtime;
- decoder;
- C11 semantic/integrity/repository;
- I03;
- I05;
- I04;
- V553+;
- V3/V2.

No test expectation may be changed.

No helper/runtime patch may be made.

Allowed writes only under:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/R5_LONG_COMPACT_V2_VALIDATION/`

No source bytes, sealed carriers, scratch trees or large logs are committed.

## 3. EXACT REPAIR SURFACE UNDER JUDGMENT

Physical-only implementation modules:

- `rawlsing_next/pre553_r5_compact_carrier.py`
- `rawlsing_next/pre553_r5_compact_shadow.py`
- `rawlsing_next/pre553_r5_compact_density_court.py`

Court additions:

- `rawlsing_next/test_pre553_r5_compact_carrier.py`
- `rawlsing_next/test_pre553_r5_compact_shadow.py`
- `rawlsing_next/test_pre553_r5_compact_frozen_integration.py`
- `rawlsing_next/test_pre553_r5_compact_blind.py`
- `rawlsing_next/test_pre553_r5_compact_memory.py`

V1 remains untouched as historical/reference terrain.

## 4. G0–G8 REVALIDATION

Run the complete relevant PRE553/R5 suite in the real checkout. At minimum:

`pytest -q rawlsing_next/test_pre553_r5_*.py`

All compact tests must execute; the compact frozen-integration and compact blind-I05 tests may not skip.

Require:

- G0 relevant existing + R5 regression PASS;
- G1 typed codec hostile law remains PASS;
- G2 reconstructed-row/reference parity PASS;
- G3 all mandatory independent destructive oracle controls rejected and benign relayout accepted;
- G4 independent C11 reconstruction/ref/projection parity PASS;
- G5 compact increasing-N memory plateau PASS;
- G6 compact corruption/publication/TOCTOU/CAS PASS;
- G7 compact frozen I03/I05/I04 parity PASS and post-freeze blind-I05 PASS;
- G8 compact determinism/relayout semantic identity PASS.

Any failure or skip in a required compact gate returns:

`R5_LONG_COMPACT_V2_BLOCKED__EXACT_VALIDATION`

with the smallest witness. Do not repair.

## 5. EXACT WVS SOURCE

Use exact WVS Wave 7 SAV source only.

Required SHA-256:

`2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Exact shape:

- rows `97,220`;
- variables `613`;
- physical cells `59,595,860`.

Required decoder:

`decode_sav(source_path)`

No encoding override.

A known exact local path from the prior successful source-identity court is:

`/Users/matthewsmith/Desktop/Rawlsing/data/Data/WVS Wave 7.sav`

If that path is unavailable, use the exact authorized Library transport and verify the extracted SAV SHA before execution.

## 6. PREFIX DENSITY EXECUTION

Use only:

`rawlsing_next.pre553_r5_compact_density_court`

Run checkpoints sequentially.

### 6.1 250,000 cells

Run and receipt the exact sealed prefix.

This checkpoint is an early measurement, not by itself final selection authority. If it hits a source/integrity/RSS hard failure, stop. Otherwise continue to 1M even if density is above preferred so the representative decision checkpoint is measured.

### 6.2 1,000,000 cells

Measure actual final:

- member bytes;
- inventory bytes;
- root bytes;
- total canonical steady-state bytes;
- sealed bytes / physical cell;
- projected full WVS bytes/GiB;
- peak RSS;
- scratch peak;
- build time;
- sealed reopen/full-audit time;
- run/shard counts;
- logical/audit digest equality.

Decision:

- `<= 36 B/event`: continue to 2M;
- `> 36 and <= 72 B/event`: STOP and return `R5_LONG_COMPACT_V2_DENSITY_RETURNED__HQ_ADJUDICATION_REQUIRED`;
- `> 72 B/event`: STOP and return `R5_LONG_COMPACT_V2_BLOCKED__DENSITY_HARD_GATE`.

### 6.3 2,000,000 cells

If 1M passed preferred density, run the 2M exact prefix.

Decision:

- `<= 36 B/event`: density PASS;
- `> 36 and <= 72 B/event`: `R5_LONG_COMPACT_V2_DENSITY_RETURNED__HQ_ADJUDICATION_REQUIRED`;
- `> 72 B/event`: `R5_LONG_COMPACT_V2_BLOCKED__DENSITY_HARD_GATE`.

No full WVS source run is authorized in this cell.

## 7. RESOURCE LAW

Peak RSS hard ceiling remains `4 GiB`; preferred remains `< 2 GiB`.

`persistent_cache_count = 0`

`worker_count = 1`

Scratch/staging is measured separately and cleaned after each checkpoint.

Do not count uncompressed logical-wire or transient sort bytes as canonical steady-state carrier bytes. Canonical density is the **actual sealed members + inventory + root**. Report scratch separately.

## 8. PROGRESS LAW

Apply Authority 62 progress telemetry semantics.

At minimum print a visible heartbeat every 250,000 emitted WVS physical cells and at major build/reopen/audit transitions.

For each checkpoint write a small progress/final receipt with:

- cells done / checkpoint;
- source rows reached where available;
- elapsed time;
- current/peak RSS;
- scratch peak;
- sealed canonical bytes once available;
- actual bytes/event;
- projected full WVS size;
- disposition.

## 9. REQUIRED RECEIPTS

Write small evidence only under the validation receipt directory, including:

- `VALIDATION_RESULT.md`
- `VALIDATION_RESULT.json`
- `TEST_RECEIPT.json`
- `WVS_PREFIX_250K.json`
- `WVS_PREFIX_1M.json` if reached
- `WVS_PREFIX_2M.json` if reached
- `PROGRESS_LOG.jsonl`
- `CLEANUP_RECEIPT.json`
- `CHANGED_FILES.txt`

## 10. ALLOWED FINAL DISPOSITIONS

Exactly one:

- `R5_LONG_COMPACT_V2_VALIDATED__PREFERRED_DENSITY_PASS`
- `R5_LONG_COMPACT_V2_DENSITY_RETURNED__HQ_ADJUDICATION_REQUIRED`
- `R5_LONG_COMPACT_V2_BLOCKED__DENSITY_HARD_GATE`
- `R5_LONG_COMPACT_V2_BLOCKED__EXACT_VALIDATION`
- `R5_LONG_COMPACT_V2_BLOCKED__SOURCE_IDENTITY`
- `R5_LONG_COMPACT_V2_BLOCKED__RESOURCE_HARD_GATE`
- `R5_LONG_COMPACT_V2_BLOCKED__INTEGRITY_OR_RECONSTRUCTION`
- `R5_LONG_COMPACT_V2_BLOCKED__TRUSTWORTHY_CHECKOUT_UNAVAILABLE`

Required token:

`PRE553_R5_LONG_COMPACT_V2_VALIDATION_RETURNED`

Then STOP.

## 11. FORWARD LAW

Only HQ may adjudicate the return.

A preferred-density PASS does not itself authorize serving or full WVS/LiTS execution. If HQ accepts it, HQ will create fresh full-source WVS7 and LiTS I courts against the repaired candidate.

QUESTION_BLOCKED_LONG/HYBRID remain unauthorized unless compact LONG itself fails the frozen practical/storage boundary without semantic weakening.
