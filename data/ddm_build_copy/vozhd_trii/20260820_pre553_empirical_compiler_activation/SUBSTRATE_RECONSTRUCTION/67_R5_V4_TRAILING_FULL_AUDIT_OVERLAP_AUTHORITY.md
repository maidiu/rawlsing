# VOZHD TRII — R5 V4 TRAILING FULL-AUDIT OVERLAP AUTHORITY

Status: `AUTHORIZED__TARGETED_CERTIFICATION_PIPELINE_OVERLAP__V4_FROZEN__NO_FULL_SOURCE_YET`

Repository: `maidiu/rawlsing`

Control branch:
`agent/vozhd-trii-pre553-substrate-reconstruction-control`

Accepted V4 compliance HEAD:
`55d4bae445b5eb837aec6f3c67083e131d8e3b0c`

Worker branch:
`agent/vozhd-trii-r5-v4-trailing-audit67`

Exact worker starting HEAD:
`55d4bae445b5eb837aec6f3c67083e131d8e3b0c`

Binding parents:
- `56_POST_R4_ROUND2_FINAL_SYNTHESIS_AND_R5_CARRIER_CONTRACT.md`
- `61_R5_BOUNDED_ACCEPTANCE_AND_FULL_WVS7_LITS1_REAL_SOURCE_COURT_AUTHORITY.md`
- `62_R5_FULL_SOURCE_PROGRESS_TELEMETRY_ADDENDUM.md`
- `63_R5_WVS7_RESOURCE_FAILURE_AND_LONG_COMPACT_ENCODING_REPAIR_AUTHORITY.md`
- `64_R5_LONG_COMPACT_V2_EXACT_VALIDATION_AND_WVS_PREFIX_DENSITY_COURT.md`
- `66_R5_LONG_COMPACT_V2_SERIAL_TURBO_MAXIMIZATION_AUTHORITY.md`
- Authority-66 compliance-closure receipts at HEAD `55d4bae445b5eb837aec6f3c67083e131d8e3b0c`.

---

## 0. BANKED V4 RESULT

HQ banks the Authority-66 narrow compliance closure:

`R5_SERIAL_TURBO_V4_COMPLIANCE_CLOSED__READY_FOR_FULL_SOURCE_HQ_AUTHORITY`

Verified 2M WVS result:
- complete relevant suite: `77 passed / 0 failed / 0 skipped`;
- V4 build: `389.066875439 s`;
- V0 build: `468.739862739 s`;
- V4 build speedup: `1.2047796724x`;
- total serial build+reopen+audit speedup: `1.1312577497x`;
- V4 and V0 are exact-equal in canonical row count, logical digest, physical root, root bytes, inventory bytes, member count/order, every member byte length/hash/logical digest/coverage descriptor and full-audit result;
- V4 peak RSS: `200540160` bytes;
- V4 peak scratch: `78693265` bytes;
- density: `14.4385385 B/cell`;
- projected full-WVS carrier: `0.8013817659 GiB`;
- safety governors passed;
- scratch cleaned;
- no OS file-limit increase.

Frozen V4 execution configuration:
- `run_max_rows = 65536`;
- `run_max_bytes = 67108864`;
- `merge_fan_in = 64`;
- disposable temporary compression = deterministic gzip level `1`;
- temporary fsync = `false`;
- final `shard_max_rows = 16384`;
- final `shard_max_bytes = 16777216`;
- final member compression = deterministic gzip level `6`;
- final carrier bytes/root remain baseline-identical.

V4 is selected as the accepted serial build execution path for the next full-source court unless later HQ authority supersedes it.

---

## 1. WHY THIS AUTHORITY EXISTS

Authority 61 imposes a WVS7 hard wall-time gate of `<= 4 hours` for the combined build + seal + inactive promote + sealed reopen + full audit path, while also separately requiring full audit `<= 2 hours`.

The clean 2M V4 court linearly projects approximately:
- build: `3.22 h`;
- full audit: `1.74 h`;
- combined serial certification: `4.97 h` before accounting for the additional full-source merge pass.

Therefore a direct serial full-WVS court is presently expected to collide with the binding combined hard gate even though build and audit separately project within their individual hard limits.

The audit is verification/certification work, not carrier composition. It need not remain wall-clock-serial with final member production if exact independent verification can trail immutable closed members and still compare its complete result against the final sealed root/inventory before any inactive promotion is accepted.

This authority therefore tests only whether the already-required full audit may lawfully and exactly overlap the V4 final-member sealing phase.

It does NOT remove, weaken, sample, shorten, approximate or redefine the full audit.

---

## 2. FROZEN SEMANTICS AND BUILD LAW

READ-ONLY / unchanged:
- exact source bytes, SHA and decoder law;
- typed codec semantics;
- source-native seam semantics;
- Compact V2 storage bytes;
- canonical row reconstruction;
- object ID/content-hash law;
- canonical identity order;
- final V4 member bytes and boundaries;
- V4 root/inventory/member identity law;
- C11 M01-M18;
- I03/I05/I04 truth conditions;
- V553-V558/V3/V2 semantics;
- source evidence / structural prior / generated fact / actor knowledge / memory / expression distinctions.

FORBIDDEN:
- parallel build workers;
- changing V4 run geometry or compression;
- changing final member layout/compression;
- changing root schema or logical digest definition;
- Merkle/hash-tree replacement;
- caches, matrices, bitmaps, serving indexes;
- QBL/HYBRID/source-family architecture escalation;
- skipping any member or row;
- trusting builder-reported member facts as audit truth;
- full WVS or LiTS execution under this authority.

---

## 3. AUTHORIZED EXECUTION TOPOLOGY

Exactly one V4 builder remains the sole compositional compiler.

Authority 67 additionally permits exactly one independent **trailing audit process**.

Topology:

```text
V4 SERIAL BUILDER
    |
    | closes + fsyncs final member N
    v
small readiness notification only
    |
    v
INDEPENDENT TRAILING AUDITOR
    |
    | opens immutable closed member N from disk
    | independently hashes length/SHA
    | decompresses every row
    | reconstructs/validates canonical row
    | recomputes per-member logical digest/count/coverage
    | maintains full global ordered logical-stream digest/count
    v
AUDIT RESULT ACCUMULATOR

BUILDER finishes inventory/root
    |
    v
SEALED ROOT / INVENTORY
    |
    v
AUDITOR independently verifies root + inventory bindings
and compares its already-computed complete stream result
    |
    v
PASS or FAIL-CLOSED
```

The readiness channel may communicate only bounded execution facts necessary to know that a numbered member is closed and safe to read, e.g. member ordinal/name. It may NOT communicate expected SHA, logical digest, counts, coverage or semantic expected truth from builder to auditor.

The auditor must derive those facts itself from the member bytes and later compare them to the sealed root-bound inventory.

`builder_count = 1`
`trailing_auditor_count = 1`
`persistent_cache_count = 0`

This two-process topology is certification overlap only and is not a parallel compiler.

---

## 4. EXACT AUDIT EQUIVALENCE LAW

The trailing audit must be semantically identical to the accepted post-build `R5CompactLongShardedReader.full_audit()` result.

It SHALL independently establish across every closed final member, in exact member order:
- compressed member SHA-256;
- compressed byte length;
- successful gzip decode;
- exact compact-row canonicality/reconstruction;
- strict global canonical identity ordering;
- no duplicate identities;
- per-member row count;
- per-member logical digest;
- first/last identity;
- relation counts;
- global canonical row count;
- global logical-stream SHA-256 over the exact `_logical_wire(row)` byte stream;
- global relation counts.

After final root/inventory sealing it SHALL independently:
- verify root self-hash / expected physical root;
- verify inventory SHA/length/cardinality/order/schema;
- compare every independently derived member SHA/length/logical digest/count/coverage descriptor against the root-bound inventory;
- compare global row count and global logical-stream digest against root;
- return the exact same `full_audit()` result object as an ordinary sealed post-build audit.

No final certification PASS exists until the root/inventory are sealed and all trailing-audit facts reconcile with them.

---

## 5. PUBLICATION / FAILURE LAW

The audit may trail build, but successful inactive promotion/certification may not be accepted until both builder and trailing auditor finish and reconcile.

Any auditor failure, crash, timeout, unreadable member, hash mismatch, row reconstruction failure, ordering failure, inventory/root mismatch or missing notification causes fail-closed court failure.

No serial-audit fallback may silently convert a failed overlap court into a pass.

For bounded diagnostic purposes, a post-failure serial audit may be run only after the overlap result is already classified failed and must be labeled diagnostic.

Builder failure terminates/joins auditor and cleans scratch.

Auditor failure signals builder/court coordinator to stop as soon as safely possible; no valid promotion/pass is permitted.

---

## 6. RESOURCE / BACKPRESSURE LAW

The builder may not outrun the auditor without bound.

Use a bounded readiness queue with maximum `8` pending closed members. Preferred target is <=4 pending members.

If queue is full, builder may block after safely closing a member until auditor catches up. Blocking is lawful; semantic output may not change.

Aggregate builder + auditor RSS:
- preferred `< 2 GiB`;
- `2-3 GiB` warning/allowed only if useful;
- `>= 3 GiB` stop additional admission where applicable;
- `>= 3.5 GiB` HARD ABORT;
- Authority-61 absolute hard `4 GiB` remains binding.

Scratch/file-space governors from Authority 66 remain active.

The auditor may hold only bounded per-member state plus global digest/count/coverage accumulators. No corpus-scale row collection.

---

## 7. REQUIRED HOSTILE TESTS

Before real-source prefixes, add tests proving:

1. trailing audit exact result equals ordinary sealed `full_audit()`;
2. builder expected SHA/digest/count is not supplied as auditor expected truth;
3. corrupted closed member is detected by auditor;
4. truncated member is detected;
5. duplicate/noncanonical identity is detected;
6. skipped/missing readiness ordinal is detected;
7. duplicate readiness ordinal is detected;
8. out-of-order readiness is either deterministically buffered within the bounded protocol or rejected; no semantic reorder;
9. auditor crash causes fail-closed no-pass/no-promote;
10. builder crash terminates auditor and cleans scratch;
11. queue backpressure remains bounded;
12. root/inventory tamper after member audit is detected at final reconciliation;
13. repeated/hashseed runs are deterministic;
14. no persistent cache/store remains.

Complete relevant R5 suite required: `0 failed / 0 skipped`.

---

## 8. REAL-WVS PREFIX COURT

Use exact source:
`/Users/matthewsmith/Desktop/Rawlsing/data/Data/WVS Wave 7.sav`

Required SHA-256:
`2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Required shape:
`97,220 x 613`

Run only:

### OA-250K
- accepted V4 build;
- ordinary serial post-build reopen/full audit;
- overlapped trailing audit build/certification.

Require byte/root-identical build outputs and exact audit-result equality.

### OA-2M
Same exact comparison at `2,000,000` physical cells.

Measure separately:
- V4 build-only wall time;
- ordinary serial post-build audit wall time;
- ordinary total certification wall time;
- overlap wall time from build start until trailing-audit/root reconciliation complete;
- overlap speedup against ordinary total certification;
- time auditor starts relative to build;
- auditor finish lag after builder root seal;
- queue depth current/peak;
- builder blocked seconds on audit backpressure;
- builder RSS, auditor RSS, aggregate peak RSS;
- audit rows/sec;
- final exact equality.

Do not rerun V0, V1-V3, V5-V7.

---

## 9. ACCEPTANCE LAW

Required exactness is absolute.

Preferred selection threshold:
- overlap total certification speedup `>= 1.25x` at 2M;
- V4 build slowdown caused by auditor `<= 10%`;
- exact full-audit equality;
- all resource/fail-closed gates pass.

If exact and `>=1.15x` but `<1.25x`:
`R5_TRAILING_AUDIT67_CORRECT__MODEST_GAIN__HQ_ADJUDICATION_REQUIRED`

If exact and `<1.15x`:
`R5_TRAILING_AUDIT67_CORRECT__NO_PRACTICAL_GAIN__DO_NOT_SELECT`

If preferred threshold passes:
`R5_TRAILING_AUDIT67_VALIDATED__USE_FOR_FULL_WVS7_CERTIFICATION`

Any semantic/integrity mismatch:
`R5_TRAILING_AUDIT67_BLOCKED__AUDIT_NONIDENTITY`

Any process/resource violation:
`R5_TRAILING_AUDIT67_BLOCKED__PROCESS_OR_RESOURCE_GATE`

---

## 10. RECEIPTS / STOP LAW

Write only small receipts under:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/R5_TRAILING_AUDIT67/`

At minimum:
- `RESULT.md`;
- `RESULT.json`;
- `AUDIT_EQUIVALENCE.json`;
- `PROCESS_RESOURCE_RECEIPT.json`;
- `CHANGED_FILES.txt`.

No source bytes, carrier members or scratch committed.

Required return token:

`PRE553_R5_TRAILING_AUDIT67_RETURNED`

Then STOP. Full WVS and LiTS remain forbidden until HQ adjudicates this return.
