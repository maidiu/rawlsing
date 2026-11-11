# VOZHD TRII — R5 V4 TRAILING AUDIT67 FAST-CANDIDATE RECERTIFICATION AUTHORITY

Status: `AUTHORIZED__RECERTIFICATION_ONLY__FAST_IMPLEMENTATION_FROZEN__NO_FULL_SOURCE_YET`

Repository: `maidiu/rawlsing`

Control branch:
`agent/vozhd-trii-pre553-substrate-reconstruction-control`

Binding parents:
- `56_POST_R4_ROUND2_FINAL_SYNTHESIS_AND_R5_CARRIER_CONTRACT.md`
- `61_R5_BOUNDED_ACCEPTANCE_AND_FULL_WVS7_LITS1_REAL_SOURCE_COURT_AUTHORITY.md`
- `62_R5_FULL_SOURCE_PROGRESS_TELEMETRY_ADDENDUM.md`
- `63_R5_WVS7_RESOURCE_FAILURE_AND_LONG_COMPACT_ENCODING_REPAIR_AUTHORITY.md`
- `64_R5_LONG_COMPACT_V2_EXACT_VALIDATION_AND_WVS_PREFIX_DENSITY_COURT.md`
- `66_R5_LONG_COMPACT_V2_SERIAL_TURBO_MAXIMIZATION_AUTHORITY.md`
- `67_R5_V4_TRAILING_FULL_AUDIT_OVERLAP_AUTHORITY.md`
- Authority-66 compliance closure at `55d4bae445b5eb837aec6f3c67083e131d8e3b0c`.

Accepted compliant Authority-67 return:
- branch `agent/vozhd-trii-r5-v4-trailing-audit67-modest-return`
- HEAD `84776b595c6c8cf0bfaf9f1b2a10f5618e8d0857`
- disposition `R5_TRAILING_AUDIT67_CORRECT__MODEST_GAIN__HQ_ADJUDICATION_REQUIRED`

Fast performance lead to recertify:
- branch `agent/vozhd-trii-r5-v4-trailing-audit67`
- frozen candidate HEAD `5e781eafe79a8f35921d48dd5c23798de723b352`
- historical committed receipt claims `R5_TRAILING_AUDIT67_VALIDATED__USE_FOR_FULL_WVS7_CERTIFICATION`, but HQ does NOT accept that claim because the hostile/process test surface was incomplete.

Worker branch:
`agent/vozhd-trii-r5-v4-trailing-audit67-fast-recert68`

Exact worker starting HEAD:
`5e781eafe79a8f35921d48dd5c23798de723b352`

---

## 0. HQ ADJUDICATION OF THE TWO AUTHORITY-67 RETURNS

HQ preserves both returns without merge or overwrite.

The compliant modest return is valid evidence and remains banked.

The fast return is a performance lead only until recertified. Its 2M measurements were approximately:
- ordinary certification: `596.385 s`;
- overlap certification: `389.582 s`;
- overlap speedup: `1.530835x`;
- ordinary V4 build: `380.687 s`;
- overlap V4 build: `389.588 s`;
- builder slowdown: about `2.34%`;
- queue peak reported `1`;
- exact carrier/root/inventory/audit parity reported true;
- aggregate RSS about `224 MB`.

These measurements are promising but are NOT accepted selection evidence until the full Authority-67 hostile/process law is satisfied.

The fast implementation's historical `VALIDATED` disposition is therefore treated as:

`PERFORMANCE_LEAD__REQUIRES_AUTHORITY67_RECERTIFICATION`

---

## 1. MISSION

Recertify the frozen fast Authority-67 implementation without changing its execution algorithm.

This court exists to answer exactly:

**DOES THE FAST `5e781e...` TRAILING-AUDIT IMPLEMENTATION STILL PASS THE COMPLETE AUTHORITY-67 HOSTILE/PROCESS COURT AND REPRODUCE ITS PREFERRED PERFORMANCE WHEN MEASURED BY A CORRECT GATE-ENFORCING HARNESS?**

This is not a redesign or optimization authority.

---

## 2. FROZEN FAST IMPLEMENTATION LAW

The following implementation behavior at starting HEAD `5e781e...` is frozen for this court:
- one serial V4 builder;
- one spawned trailing auditor process;
- readiness `multiprocessing.Queue(maxsize=8)`;
- builder callback after final member close/fsync;
- readiness message contains member name/ordinal only;
- trailing auditor independently hashes/decompresses/reconstructs rows and computes member/global logical facts;
- final independent root/inventory reconciliation;
- V4 physical output remains byte/root identical to accepted serial V4.

READ-ONLY candidate implementation files:
- `rawlsing_next/pre553_r5_v4_trailing_audit67.py`
- the Authority-67 callback behavior already present in `rawlsing_next/pre553_r5_serial_turbo66.py` at `5e781e...`.

No modification to those implementation files is authorized.

If the required hostile tests expose an implementation defect, return the exact witness and STOP. Do not repair it under Authority 68.

Authorized writes are limited to:
- additive or corrected Authority-68 test files;
- corrected recertification court/harness files;
- small receipts under `.../R5_TRAILING_AUDIT67_FAST_RECERT68/`.

The historical Authority-67 receipts at `5e781e...` remain history and may not be rewritten as if they were accepted HQ evidence.

---

## 3. FROZEN V4 / SEMANTIC LAW

Unchanged:
- source bytes/SHA/decoder law;
- V4 execution configuration;
- typed codec and compact storage semantics;
- canonical identity/order;
- member boundaries/compression;
- root/inventory/member identity law;
- C11 M01-M18;
- I03/I05/I04 truth conditions;
- V553-V558/V3/V2 semantics.

Forbidden:
- parallel compiler workers;
- changing queue capacity above 8;
- changing readiness payload to include expected semantic truth;
- skipping/sampling audit rows;
- caches/indexes/matrices/bitmaps/Merkle/QBL/HYBRID;
- full WVS or LiTS execution;
- tuning after seeing the recertification result.

---

## 4. REQUIRED COMPLETE HOSTILE / PROCESS COURT

Implement real tests covering every Authority-67 requirement:

1. trailing audit exact result equals ordinary sealed `full_audit()`;
2. readiness payload supplies no expected SHA/digest/count/coverage truth;
3. corrupt closed member fails closed;
4. truncated closed member fails closed;
5. duplicate/noncanonical row identity fails closed;
6. skipped/missing readiness ordinal fails closed;
7. duplicate readiness ordinal fails closed;
8. out-of-order readiness is rejected or deterministically governed without semantic reorder;
9. auditor crash/early exit causes no-pass/no-promote;
10. builder crash terminates/joins auditor and leaves no accepted publication;
11. queue/backpressure remains bounded;
12. root/inventory tamper after member audit is detected at final reconciliation;
13. repeated runs and differing `PYTHONHASHSEED` preserve deterministic semantic/physical output;
14. no persistent cache/store remains.

Also explicitly prove:
- readiness queue configured capacity exactly `8`;
- ninth pending admission cannot occur; producer blocks/fails closed rather than exceeding capacity;
- queue telemetry does not use `qsize()` as sole correctness authority;
- distinguish `pending_queue_depth`, `auditor_inflight`, and `outstanding_closed_members` if instrumented by the harness;
- hard invariant `pending_queue_depth <= 8`;
- process exit codes/timeouts/result-channel failures fail closed;
- final success is impossible before root/inventory reconciliation completes.

Tests may use mocks/fault injection/small synthetic carriers. Do not exhaust machine resources merely to test thresholds.

Complete relevant R5 suite required:
`0 failed / 0 skipped`.

---

## 5. CORRECT RECERTIFICATION HARNESS LAW

The Authority-68 harness must enforce BOTH preferred Authority-67 selection gates, not speedup alone.

At 2M compute:

`OVERLAP_SPEEDUP = ordinary_total_certification / overlap_total_certification`

`BUILDER_SLOWDOWN = (overlap_builder_seconds / ordinary_builder_seconds) - 1`

Preferred automatic selection requires ALL:
- exact carrier/root/inventory/member parity;
- ordinary `full_audit()` == trailing audit exactly;
- all hostile/process/resource gates PASS;
- `OVERLAP_SPEEDUP >= 1.25x`;
- `BUILDER_SLOWDOWN <= 10%`;
- pending queue depth never exceeds 8.

Do not emit `VALIDATED` if any one of those is false.

The harness must record exact source SHA, queue capacity, pending/in-flight/outstanding peaks where available, builder blocked seconds, process counts, RSS, scratch, cleanup, and no persistent cache/store.

---

## 6. REAL-WVS PREFIX RECERTIFICATION

Exact source:
`/Users/matthewsmith/Desktop/Rawlsing/data/Data/WVS Wave 7.sav`

Required SHA-256:
`2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Required shape:
`97,220 x 613`

Run only:

### RECERT-250K
- ordinary accepted V4 + post-build full audit;
- frozen fast `5e781e...` overlap candidate.

### RECERT-2M
Same comparison at `2,000,000` physical cells.

Do not rerun V0/V1/V2/V3/V5/V6/V7.
Do not rerun the compliant modest implementation.
Do not run full WVS or LiTS.

Require exact equality of:
- root bytes;
- inventory bytes;
- member order/count;
- every member byte/hash/length/logical digest/coverage descriptor;
- canonical row count;
- logical stream digest;
- physical root;
- ordinary and trailing full-audit result.

Measure:
- ordinary V4 build;
- ordinary audit;
- ordinary total certification;
- overlap builder time;
- overlap total certification;
- speedup;
- builder slowdown;
- auditor finish lag;
- pending queue peak;
- auditor in-flight peak if measured;
- outstanding closed-member peak if measured;
- builder blocked seconds;
- builder/auditor/aggregate RSS;
- scratch peak;
- cleanup;
- exact parity.

---

## 7. DISPOSITIONS

If all exactness/process/resource gates pass AND:
- speedup `>=1.25x`;
- builder slowdown `<=10%`;

return:

`R5_TRAILING_AUDIT67_FAST_RECERTIFIED__USE_FOR_FULL_WVS7_CERTIFICATION`

If exact and speedup `>=1.15x` but preferred selection gate(s) miss:

`R5_TRAILING_AUDIT67_FAST_RECERTIFIED__MODEST_GAIN__HQ_ADJUDICATION_REQUIRED`

If exact and speedup `<1.15x`:

`R5_TRAILING_AUDIT67_FAST_RECERTIFIED__NO_PRACTICAL_GAIN__DO_NOT_SELECT`

If hostile tests expose candidate defect:

`R5_TRAILING_AUDIT67_FAST_RECERT_BLOCKED__IMPLEMENTATION_WITNESS_RETURNED`

If process/resource/integrity gate fails:

`R5_TRAILING_AUDIT67_FAST_RECERT_BLOCKED__PROCESS_RESOURCE_OR_INTEGRITY`

No self-repair under this authority.

---

## 8. RECEIPTS / STOP LAW

Write only small receipts under:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/R5_TRAILING_AUDIT67_FAST_RECERT68/`

At minimum:
- `RESULT.md`;
- `RESULT.json`;
- `HOSTILE_PROCESS_RECEIPT.json`;
- `AUDIT_EQUIVALENCE.json`;
- `PROCESS_RESOURCE_RECEIPT.json`;
- `CHANGED_FILES.txt`.

Do not rewrite/delete historical Authority-67 receipts.
Do not commit source bytes, carrier members or scratch.

Required return token:

`PRE553_R5_TRAILING_AUDIT67_FAST_RECERT68_RETURNED`

Then STOP. Full WVS and LiTS remain forbidden until HQ adjudicates the return.
