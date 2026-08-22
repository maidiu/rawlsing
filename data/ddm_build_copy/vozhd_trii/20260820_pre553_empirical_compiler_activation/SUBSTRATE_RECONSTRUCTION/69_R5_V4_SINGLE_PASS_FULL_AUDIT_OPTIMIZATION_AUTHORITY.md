# VOZHD TRII — R5 V4 SINGLE-PASS FULL-AUDIT OPTIMIZATION AUTHORITY

Status: `AUTHORIZED__SERIAL_AUDIT_FAST_PATH__OVERLAP_NOT_SELECTED__NO_FULL_SOURCE_YET`

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
- `68_R5_V4_TRAILING_AUDIT67_FAST_RECERTIFICATION_AUTHORITY.md`

Accepted serial V4 base:
`55d4bae445b5eb837aec6f3c67083e131d8e3b0c`

Compliant Authority-67 modest return:
`84776b595c6c8cf0bfaf9f1b2a10f5618e8d0857`

Authority-68 fast recertification return:
`bdbbdca3b63db236ee8347b9a60fc0d96c2cfea1`

Worker branch:
`agent/vozhd-trii-r5-v4-single-pass-audit69`

Exact worker starting HEAD:
`55d4bae445b5eb837aec6f3c67083e131d8e3b0c`

---

## 0. HQ ADJUDICATION OF OVERLAP

HQ banks both trailing-audit overlap lines as correctness evidence but does NOT select either overlap implementation for full WVS7 certification.

Authority-67 compliant return:
- exact parity: PASS;
- 2M overlap speedup: approximately `1.202857x`;
- 2M builder slowdown: approximately `20.04%`;
- disposition: `R5_TRAILING_AUDIT67_CORRECT__MODEST_GAIN__HQ_ADJUDICATION_REQUIRED`.

Authority-68 frozen-fast recertification:
- complete R5 suite: `96 passed / 0 failed / 0 skipped`;
- hostile/process court: `16 passed / 0 skipped`;
- exact carrier/root/inventory/member/audit parity: PASS;
- 2M overlap speedup: `1.2024569053x`;
- 2M builder slowdown: `42.0929716679%`;
- queue/process/resource/integrity gates: PASS;
- disposition: `R5_TRAILING_AUDIT67_FAST_RECERTIFIED__MODEST_GAIN__HQ_ADJUDICATION_REQUIRED`.

The overlap technique is therefore classified:

`R5_TRAILING_AUDIT_OVERLAP_CORRECT__NOT_SELECTED_FOR_FULL_SOURCE__BUILDER_CONTENTION_UNSTABLE`

No overlap implementation is merged into the serial V4 line.

---

## 1. WHY THIS AUTHORITY EXISTS

The accepted `R5CompactLongShardedReader.full_audit()` currently obtains rows through `iter_rows()`.

During one full audit, for each canonical row:

1. `iter_rows()` decodes the compact storage row;
2. `iter_rows()` computes `_logical_wire(row)` to maintain the required per-member logical digest;
3. `iter_rows()` yields the reconstructed row;
4. `full_audit()` computes `_logical_wire(row)` again to maintain the required global logical-stream digest.

Therefore the same canonical logical serialization is generated twice per row during one complete audit.

This is verification overhead, not an evidentiary requirement.

The required audit obligations are:
- verify root self-hash/schema/carrier binding;
- verify inventory hash/length/cardinality/order/schema;
- verify every compressed member hash and byte length before consumption;
- decompress every member;
- reconstruct and canonically validate every stored row;
- verify strict global identity order/no duplicate identities;
- recompute every per-member row count, logical digest, first/last identity, and relation counts;
- recompute the complete global canonical row count, global logical-stream digest, and global relation counts;
- compare all derived facts against the root-bound inventory/root;
- fail closed/quarantine on any mismatch.

None of those obligations requires serializing the same `_logical_wire(row)` twice.

Authority 69 therefore permits a serial single-pass audit fast path in which each row's canonical logical wire is computed exactly once and the same exact bytes update both the per-member digest and the global digest.

---

## 2. FROZEN SEMANTIC / PHYSICAL LAW

READ-ONLY / unchanged:
- source bytes/SHA/decoder law;
- V4 build execution geometry;
- Compact V2 carrier bytes, member boundaries, compression, root and inventory law;
- `_decode_storage` canonicality/reconstruction semantics;
- `_logical_wire` definition and exact bytes;
- typed codec;
- canonical identity ordering;
- object IDs/content hashes;
- C11 M01-M18;
- I03/I05/I04 truth;
- V553-V558/V3/V2 semantics;
- publication/integrity/quarantine semantics.

FORBIDDEN:
- changing `_logical_wire`;
- skipping any row/member/hash/coverage check;
- weakening `_decode_storage` canonical verification;
- trusting builder-reported expected truth;
- sampling/approximating the audit;
- parallel audit/build workers;
- persistent caches/indexes/matrices/bitmaps/Merkle/QBL/HYBRID;
- changing V4;
- full WVS or LiTS under this authority.

---

## 3. AUTHORIZED IMPLEMENTATION SHAPE

Prefer an additive audit implementation rather than modifying the accepted carrier reader in place during this court.

Authorized write surfaces include:
- `rawlsing_next/pre553_r5_single_pass_audit69.py`;
- `rawlsing_next/pre553_r5_single_pass_audit69_court.py`;
- `rawlsing_next/test_pre553_r5_single_pass_audit69.py`;
- small receipts under `.../R5_SINGLE_PASS_AUDIT69/`.

The fast path may use the accepted reader's root/inventory verification helpers or independently reproduce the same checks, but it must not bypass them.

For every decoded row:

```text
row = exact compact decode + canonical validation
wire = exact _logical_wire(row)      # compute ONCE
member_digest.update(wire)
global_digest.update(wire)
```

The single-pass implementation must return exactly the same audit result object as accepted `R5CompactLongShardedReader.full_audit()`.

No persistent output other than small receipts.

---

## 4. HOSTILE EQUIVALENCE COURT

Before real-source prefixes, prove at least:

1. single-pass result exactly equals ordinary `full_audit()`;
2. `_logical_wire` call count is one per canonical row in the single-pass fast path, not two;
3. corrupted compressed member fails closed;
4. truncated gzip member fails closed;
5. member hash/length mismatch fails closed before trusted consumption;
6. inventory hash/length/cardinality/order/schema mismatch fails closed;
7. root self-hash / expected-root mismatch fails closed;
8. per-member logical digest/count mismatch fails closed;
9. per-member first/last identity mismatch fails closed;
10. per-member relation-count mismatch fails closed;
11. duplicate/noncanonical global identity ordering fails closed;
12. global row-count mismatch fails closed;
13. global logical-stream digest mismatch fails closed;
14. quarantine/fail-closed behavior remains equivalent where the accepted reader requires it;
15. repeated runs / differing `PYTHONHASHSEED` are deterministic;
16. no persistent cache/store remains.

Complete relevant R5 suite required:
`0 failed / 0 skipped`.

---

## 5. REAL-WVS PREFIX COURT

Source:
`/Users/matthewsmith/Desktop/Rawlsing/data/Data/WVS Wave 7.sav`

Required SHA-256:
`2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Required shape:
`97,220 x 613`

Use the already accepted serial V4 builder to produce exact byte/root-identical carriers.

Run only:

### SP-250K
- one V4 build;
- ordinary accepted post-build `full_audit()` timing;
- single-pass audit69 timing against the same sealed carrier.

### SP-2M
Same comparison at `2,000,000` physical cells.

Do not rebuild the carrier merely to compare the two audit methods if the same sealed prefix carrier can lawfully serve both serial audit measurements within the court.

Do not rerun V0/V1-V3/V5-V7.
Do not run overlap.
Do not run full WVS.
Do not run LiTS.

---

## 6. REQUIRED EXACTNESS

Ordinary and single-pass audits must be exactly equal in:
- physical root id;
- canonical row count;
- logical stream digest;
- relation counts;
- every member/inventory/root integrity verdict;
- fail-closed behavior for hostile mutations.

Carrier bytes/root/inventory/member files may not change because the audit is read-only.

---

## 7. PERFORMANCE / RESOURCE LAW

At each checkpoint measure:
- ordinary audit wall time;
- single-pass audit wall time;
- audit speedup = ordinary / single-pass;
- rows/sec for each;
- peak RSS;
- scratch/spool peak where measurable;
- `_logical_wire` call count ordinary vs single-pass in bounded instrumentation;
- exact equality result.

Selection thresholds at 2M:

If exact and speedup `>= 1.20x`:
`R5_SINGLE_PASS_AUDIT69_VALIDATED__USE_FOR_FULL_WVS7_CERTIFICATION`

If exact and speedup `>= 1.08x` but `< 1.20x`:
`R5_SINGLE_PASS_AUDIT69_CORRECT__MODEST_GAIN__HQ_ADJUDICATION_REQUIRED`

If exact and speedup `< 1.08x`:
`R5_SINGLE_PASS_AUDIT69_CORRECT__NO_PRACTICAL_GAIN__DO_NOT_SELECT`

Any semantic/integrity mismatch:
`R5_SINGLE_PASS_AUDIT69_BLOCKED__AUDIT_NONIDENTITY`

Any process/resource violation:
`R5_SINGLE_PASS_AUDIT69_BLOCKED__PROCESS_OR_RESOURCE_GATE`

RSS remains under Authority-61 bounds.
Persistent cache/store count must remain `0`.

---

## 8. RECEIPTS / STOP LAW

Write only small receipts under:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/R5_SINGLE_PASS_AUDIT69/`

At minimum:
- `RESULT.md`;
- `RESULT.json`;
- `HOSTILE_EQUIVALENCE_RECEIPT.json`;
- `RESOURCE_RUNTIME_RECEIPT.json`;
- `CHANGED_FILES.txt`.

No source bytes, carrier members, giant logs or scratch committed.

Required return token:

`PRE553_R5_SINGLE_PASS_AUDIT69_RETURNED`

Then STOP. Full WVS and LiTS remain forbidden until HQ adjudicates this return.
