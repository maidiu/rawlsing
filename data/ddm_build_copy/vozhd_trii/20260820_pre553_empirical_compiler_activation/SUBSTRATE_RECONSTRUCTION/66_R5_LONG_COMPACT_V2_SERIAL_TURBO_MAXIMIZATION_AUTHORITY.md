# VOZHD TRII — R5 LONG COMPACT V2 SERIAL TURBO MAXIMIZATION AUTHORITY

Status: `AUTHORIZED__TARGETED_SERIAL_RUNTIME_MAXIMIZATION__SEMANTICS_FROZEN__PARALLEL12_REJECTED__NO_FULL_SOURCE_YET`

Repository: `maidiu/rawlsing`

Control branch:
`agent/vozhd-trii-pre553-substrate-reconstruction-control`

Validated serial reference HEAD:
`11877f5a043418100773b8a476ee425ec63305cd`

Rejected Parallel-12 evidence HEAD:
`7049660a574456b4a4333c97a277f6b3d8a2c1b3`

Serial-turbo implementation/court branch:
`agent/vozhd-trii-r5-long-compact-v2-serial-turbo66`

Exact serial-turbo starting HEAD:
`11877f5a043418100773b8a476ee425ec63305cd`

Binding parents:
- `56_POST_R4_ROUND2_FINAL_SYNTHESIS_AND_R5_CARRIER_CONTRACT.md`
- `61_R5_BOUNDED_ACCEPTANCE_AND_FULL_WVS7_LITS1_REAL_SOURCE_COURT_AUTHORITY.md`
- `62_R5_FULL_SOURCE_PROGRESS_TELEMETRY_ADDENDUM.md`
- `63_R5_WVS7_RESOURCE_FAILURE_AND_LONG_COMPACT_ENCODING_REPAIR_AUTHORITY.md`
- `64_R5_LONG_COMPACT_V2_EXACT_VALIDATION_AND_WVS_PREFIX_DENSITY_COURT.md`
- `65_R5_LONG_COMPACT_V2_PARALLEL12_COMPILER_AUTHORITY.md`

---

## 0. BANKED EVIDENCE

Compact V2 serial remains the accepted correctness oracle.

Banked serial 2M validation:
- preferred density pass;
- peak RSS about 142 MiB;
- build/seal about 456 s in the original validation court;
- exact reopen/full-audit parity;
- persistent cache count zero.

Authority 65 Parallel-12 returned exact equivalence but worse performance:
- 250k speedup `0.854157813x`;
- 2M speedup `0.884297459x`;
- 2M serial build `418.360303339 s`;
- 2M parallel build `473.099067598 s`;
- parallel peak RSS about 245 MiB;
- exact final disposition `R5_PARALLEL12_CORRECT__NO_PRACTICAL_GAIN__DO_NOT_SELECT`.

Parallel-12 is therefore rejected for full-source selection. This authority does not continue that topology.

The measured failure indicates that multiprocessing overhead, interprocess serialization, extra temporary runs and the unchanged serial reduction/seal path outweigh available CPU parallelism.

---

## 1. MISSION

Maximize the existing **single-process Compact V2** build/audit path by removing avoidable physical-execution overhead while preserving the frozen logical carrier and downstream semantics.

The court SHALL attack four execution costs:

1. tiny external-sort runs and repeated full-data merge passes;
2. expensive compression and durability work on disposable temporary runs;
3. overly small final member shards causing excessive file creation/fsync/hash/open overhead;
4. final gzip compression level if and only if a separately identified physical-relayout candidate preserves preferred density and exact logical/audit parity.

This is a physical execution court, not a semantic redesign.

---

## 2. ABSOLUTE FROZEN LAW

READ-ONLY / semantically unchanged:
- exact source bytes and SHA identity;
- decoder semantics/configuration and source compatibility law;
- `pre553_r5_codec.py` typed-value semantics;
- `pre553_r5_seam.py` physical normalization semantics;
- Compact V2 logical row reconstruction;
- canonical object identity and content-hash law;
- canonical identity ordering law (`_sort_key` semantics);
- C11 M01-M18;
- I03/I05/I04 truth conditions;
- V553-V558/V3/V2 semantics;
- source evidence / structural prior / generated fact / actor knowledge / memory / expression distinctions.

FORBIDDEN:
- multiprocessing/process pools/worker farms;
- changing source decoder semantics;
- changing object IDs or padding numeric ordinals;
- changing canonical logical sort order;
- caches, matrices, bitmaps, Merkle structures or serving indexes;
- source-family-specific semantic compilers;
- QBL/HYBRID escalation;
- changing expected semantic results to accommodate optimization;
- full WVS or LiTS execution under this authority.

---

## 3. WHY THIS COURT EXISTS

Current serial defaults are extremely conservative:

- `run_max_rows = 4096`
- `run_max_bytes = 4 MiB`
- `merge_fan_in = 8`
- `shard_max_rows = 16384`
- `shard_max_bytes = 16 MiB`
- temporary sort runs are gzip level 6;
- temporary run files and temporary merge outputs are fsync'd;
- final members are gzip level 6.

At 2M rows the current court produced 123 final members. At full WVS scale, the same geometry would produce thousands of final members and many more intermediate sort runs/merge passes than the 2M proving court.

The current implementation also performs durability work on temporary compiler scratch that is deleted after successful sealing.

Authority 56 requires bounded fail-closed execution and durable sealed publication. It does not require every disposable sort run to survive a machine crash.

---

## 4. REQUIRED IMPLEMENTATION SHAPE

Prefer additive implementation/testing around the accepted serial Compact V2 builder so the original serial implementation remains a correctness oracle.

The turbo candidate MAY parameterize:

- temporary run row/byte limits;
- merge fan-in;
- temporary run compression mode/level;
- temporary-run fsync policy;
- final shard row/byte limits;
- final member gzip compression level;
- phase timing/telemetry.

Temporary scratch may be non-durable. Final sealed members, inventory and root remain durable/fail-closed exactly as required.

No successful build may publish a root before all required final-member/inventory/root durability and integrity checks complete.

---

## 5. PHASE TELEMETRY — MANDATORY

Every court variant SHALL separately report wall time for:

- source decode/open;
- canonical row production if separable;
- initial run generation/sort/write;
- each reduction/merge pass;
- final merge + member sealing;
- member hashing/inventory/root closure;
- reopen;
- full audit.

Also report:

- initial run count;
- merge-pass count;
- max simultaneously open run files;
- final member count;
- peak RSS;
- peak scratch bytes;
- total temporary bytes written if measurable;
- final carrier bytes/density;
- cells/sec for build and audit;
- elapsed and ETA progress heartbeats per Authority 62.

Do not return only a single total wall time.

---

## 6. COURT VARIANTS

### V0 — exact frozen baseline

Use the accepted serial Compact V2 configuration and implementation unchanged.

Purpose: same-machine, same-session reference.

### V1 — LARGE_GEOMETRY_64K

Final carrier layout remains baseline so byte-identical final output is expected.

- run max rows: `65,536`
- run max bytes: `64 MiB`
- merge fan-in: `64`
- temporary compression: deterministic gzip level 6
- temporary fsync: OFF
- final shard rows/bytes: baseline
- final compression: deterministic gzip level 6

### V2 — LARGE_GEOMETRY_256K

Final carrier layout remains baseline so byte-identical final output is expected.

- run max rows: `262,144`
- run max bytes: `256 MiB`
- merge fan-in: `128`, subject to `RLIMIT_NOFILE` safety law below
- temporary compression: deterministic gzip level 6
- temporary fsync: OFF
- final shard rows/bytes: baseline
- final compression: deterministic gzip level 6

### V3 — MAX_GEOMETRY_512K

Final carrier layout remains baseline so byte-identical final output is expected.

- run max rows: `524,288`
- run max bytes: `512 MiB`
- merge fan-in: `128`, subject to file-descriptor safety law
- temporary compression: deterministic gzip level 6
- temporary fsync: OFF
- final shard rows/bytes: baseline
- final compression: deterministic gzip level 6

### V4 — FAST_TEMP_GZIP1

Use the fastest safe geometry among V1-V3.

- temporary compression: deterministic gzip level 1
- temporary fsync: OFF
- final shard layout/compression remain baseline.

Byte-identical final carrier to V0 is required.

### V5 — RAW_TEMP

Use the fastest safe geometry among V1-V3.

- temporary run files: uncompressed framed records;
- temporary fsync: OFF;
- final shard layout/compression remain baseline.

Byte-identical final carrier to V0 is required.

This variant is rejected if projected full-WVS scratch is operationally unreasonable even when 2M speed is superior.

### V6 — LARGE_FINAL_SHARDS

Use the fastest safe temporary geometry/mode from V1-V5.

Test at least:

A. `shard_max_rows = 131,072`, `shard_max_bytes = 128 MiB`

B. `shard_max_rows = 524,288`, `shard_max_bytes = 512 MiB`

Final gzip remains level 6.

These are permitted physical relayouts. Physical root/member boundaries may differ from V0. Exact logical row stream, logical stream digest, source/C11 behavior and full-audit result must remain identical.

### V7 — FAST_FINAL_GZIP1

Only after V6 identifies the best safe shard geometry.

- final member gzip compression level: `1`;
- all logical semantics unchanged.

This is a physical carrier candidate, not expected to be byte-identical to V0.

It may survive only if:
- exact logical row-stream parity passes;
- full audit passes;
- corruption/fail-closed tests pass;
- real-WVS density remains <= `36 B/cell` preferred gate;
- projected full WVS canonical carrier remains <= `2 GiB` preferred storage gate.

If gzip level 1 fails preferred density, retain level 6 and do not escalate codec family under this authority.

---

## 7. FILE-DESCRIPTOR SAFETY LAW

Before any fan-in > 8 court:

- read process soft/hard `RLIMIT_NOFILE`;
- reserve at least 64 descriptors for runtime/system use;
- actual merge fan-in SHALL be `min(requested_fan_in, soft_limit - 64)`;
- actual fan-in must remain >= 16 for V2/V3 or that variant returns blocked;
- record requested and actual fan-in in receipts;
- do not raise OS limits automatically under this authority.

---

## 8. RESOURCE SAFETY LAW

Aggregate process RSS:

- `< 2.0 GiB`: preferred normal envelope;
- `2.0-3.0 GiB`: allowed for a court only if throughput materially improves;
- `>= 3.0 GiB`: stop admitting additional buffered work / finish or abort safely;
- `>= 3.5 GiB`: HARD ABORT, cleanup scratch, return resource witness.

Scratch during 250k/2M courts:

- warning at `4 GiB`;
- hard abort at `8 GiB`;
- filesystem free space must never fall below `5 GiB`;
- RAW_TEMP must report measured scratch bytes per input cell and projected full-WVS scratch.

No full-source authorization is implied by passing these prefix resource gates.

---

## 9. COURT ORDER — FAST ELIMINATION

1. Verify exact branch/start HEAD and current control authority.
2. Implement instrumentation and variants without changing frozen semantics.
3. Run complete relevant R5 suite. Required: 0 failed, 0 skipped.
4. Add targeted tests for:
   - temporary fsync removal cannot publish partial root;
   - temp gzip6/gzip1/raw all yield identical final V0 bytes when final layout is frozen;
   - large-run geometry preserves exact canonical ordering;
   - high fan-in duplicate/noncanonical identity detection;
   - corruption and interrupted-temp-run failure closes safely;
   - cleanup succeeds after success/failure;
   - deterministic rerun/hashseed behavior.
5. Run V0-V5 on exact WVS 250k.
6. Eliminate any variant that:
   - is slower than V0 by >5%;
   - violates resource gates;
   - fails exact byte/root identity where required.
7. Advance the fastest surviving V1-V5 candidate plus V0 to exact WVS 2M.
8. If the winning temporary candidate is not at least `1.20x` faster than V0 at 2M, report that fact but still proceed to V6 because final-shard geometry attacks a separate cost.
9. Run V6 shard variants at 250k; advance the fastest safe shard variant to 2M.
10. Run V7 gzip1 final candidate at 250k; if preferred density passes and build improves materially, advance to 2M.
11. Reopen/full-audit every 2M finalist.
12. Produce one final recommended serial configuration based on **total build + reopen/audit wall time**, not build alone.
13. Clean all scratch.
14. Commit/push only authorized implementation/tests/small receipts.
15. STOP. Do not run full WVS or LiTS.

---

## 10. EXACT SOURCE

WVS7 source:
`/Users/matthewsmith/Desktop/Rawlsing/data/Data/WVS Wave 7.sav`

Required SHA-256:
`2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Required shape:
`97,220 x 613`

2M court means exactly 2,000,000 physical source cells plus the frozen metadata/variable rows required by the existing density court law.

---

## 11. ACCEPTANCE / DISPOSITIONS

A candidate may be recommended for full-source recut only after exact semantic/replay/integrity parity.

Preferred outcome:

`R5_SERIAL_TURBO_VALIDATED__MATERIAL_SPEED_GAIN__READY_FOR_FULL_SOURCE_AUTHORITY`

If only modest improvement:

`R5_SERIAL_TURBO_VALIDATED__MODEST_GAIN__HQ_DECISION_REQUIRED`

If no useful improvement:

`R5_SERIAL_TURBO_CORRECT__NO_PRACTICAL_GAIN__RETAIN_SERIAL_V2`

If physical gzip1 wins but changes final root/layout:

`R5_SERIAL_TURBO_PHYSICAL_RELAYOUT_VALIDATED__PREFERRED_DENSITY_PASS__HQ_SELECTION_REQUIRED`

If any hard resource/integrity failure:

`R5_SERIAL_TURBO_BLOCKED__EXACT_WITNESS_RETURNED`

Required return token:

`PRE553_R5_LONG_COMPACT_V2_SERIAL_TURBO66_RETURNED`

Then STOP and return exact measurements to HQ.
