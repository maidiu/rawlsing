# VOZHD TRII — R5 WVS7 RESOURCE FAILURE & LONG COMPACT-ENCODING REPAIR AUTHORITY

Status: `AUTHORIZED__TARGETED_LONG_PHYSICAL_ENCODING_REPAIR__NO_ARCHITECTURE_ESCALATION`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Binding parents:

- `56_POST_R4_ROUND2_FINAL_SYNTHESIS_AND_R5_CARRIER_CONTRACT.md`
- `57_R5_LONG_SHARDED_SHADOW_IMPLEMENTATION_AUTHORITY.md`
- `61_R5_BOUNDED_ACCEPTANCE_AND_FULL_WVS7_LITS1_REAL_SOURCE_COURT_AUTHORITY.md`
- `62_R5_FULL_SOURCE_PROGRESS_TELEMETRY_ADDENDUM.md`

Frozen bounded R5 implementation commit: `36bf351dda12f0aa93c9ff426ae54d80143d0bf9`
Receipt closure: `46a9d35d0edecc7dc9182038baeb0d0748c50fdc`

WVS7 failure branch: `agent/vozhd-trii-r5-full-wvs7-real-source-court`
Exact return: `3f39e6af83c7fd7cea600c9c7822dfee3ec13230`

## 0. HQ ADJUDICATION OF THE WVS7 RETURN

HQ independently verified the WVS7 branch is exactly one court-only commit ahead of `46a9d35...`; candidate/runtime code is unchanged.

Verified facts:

- exact WVS7 SHA/shape: PASS;
- Q152-Q157 hostile physical-missing proof: PASS;
- physical events reached: `5,327,336 / 59,595,860`;
- observed pre-seal canonical event serialization bytes: `4,294,967,507`;
- WVS7 hard carrier budget: `4,294,967,296`;
- peak RSS: `150,679,552` bytes;
- elapsed to tripwire: `491.723 s`;
- later seal/reopen/audit/I03/I05/I04/replay/integrity phases correctly not run;
- scratch cleaned;
- disposition: `R5_FULL_SOURCE_BLOCKED__RESOURCE_HARD_GATE`.

Exact observed serialized bytes/event are approximately `806.20` B/event. A linear full-source projection is approximately `48.05 GB` decimal / `44.75 GiB` before additional seal/inventory overhead.

This is a **physical representation failure**.

It is NOT evidence of:

- semantic information loss;
- unbounded memory;
- decoder failure;
- source identity failure;
- C11/I03/I05/I04 contradiction;
- LONG_SHARDED organizational impossibility.

## 1. NAMED FAILED MECHANISM

The failed mechanism is:

`SELF_DESCRIBING_JSON_CANONICAL_ROW_PER_PHYSICAL_CELL`

The V1 carrier serializes each physical cell as a full canonical JSON object containing repeated schema/relation/family/object identity/hash and repeated payload fields. The external-sort run additionally prefixes identity material.

This violates the physical minimality objective even though logical exactness is preserved.

Authority 56 organization-escalation law therefore forbids jumping to QUESTION_BLOCKED_LONG or HYBRID at this point. Lower-risk LONG representation repair has not yet failed.

## 2. REPAIR TARGET

Candidate line remains:

`R5_LONG_SHARDED_TYPED_INCIDENCE`

Organization remains:

`LONG_SHARDED`

The repair SHALL replace self-describing per-event JSON storage with a compact typed physical member encoding while preserving exact reconstruction of the same `R5CanonicalRow` semantic projection.

Preferred implementation:

- independently closed typed Parquet/Zstd LONG shards, or equivalently compact deterministic typed binary members;
- compact event columns/ordinals;
- relation/family/schema constants lifted out of repeated event rows where exactly reconstructable;
- `object_id` reconstructed from exact source identity + row/variable coordinates where the frozen seam already determines it;
- `content_hash` recomputed from the exact reconstructed canonical payload rather than stored as 64 hex characters per event;
- source SHA/schema/seam constants root/member scoped where exact;
- explicit row/variable coordinates retained;
- exact typed raw value retained;
- exact physical missing state/declaration retained;
- exact selected raw label retained;
- exact source-cell locator retained when present;
- no semantic field deletion;
- no frequency/majority/first-seen default inference.

Generic/non-source-cell canonical relations may retain a generic exact escape representation; the 59.6M-event physical-cell relation must not pay generic self-describing-object overhead.

## 3. ABSOLUTE FROZEN LAW

The repair may change physical representation/execution only.

It SHALL NOT alter:

- frozen decoder behavior;
- `R5PhysicalCellRecord` information content;
- canonical reconstructed `R5CanonicalRow` relation/family/object_id/content_hash/payload;
- typed codec semantic inverse;
- source-variable/source-metadata truth;
- source missing-state/declaration distinctions;
- topology/routing/weight/design/provenance meaning;
- C11 semantic constructors/invariants;
- I03/I05/I04 semantics;
- ExactRef/content-hash semantics;
- V553+/V3/V2;
- whole-machine closure.

No QBL, HYBRID, matrix, bitmap, Merkle, persistent cache, parallel scheduler or source-family semantic branch is authorized.

## 4. REPAIR BRANCH

Branch:

`agent/vozhd-trii-r5-long-compact-v2-repair`

Exact starting HEAD:

`46a9d35d0edecc7dc9182038baeb0d0748c50fdc`

Authorized runtime write scope:

- `rawlsing_next/pre553_r5_carrier.py`;
- if mechanically necessary, additive physical-only helpers named `rawlsing_next/pre553_r5_compact_*.py`;
- R5 tests `rawlsing_next/test_pre553_r5_*.py`;
- small repair receipts under `.../R5_LONG_COMPACT_V2_REPAIR/`.

All other accepted/frozen runtime is read-only.

## 5. DENSITY GATE BEFORE FULL SOURCE

The repaired candidate SHALL NOT immediately consume another full WVS7 run.

First run exact WVS7 source prefixes with the real frozen decoder and repaired final sealed member format.

Required checkpoints:

- at least 250,000 events;
- 1,000,000 events;
- 2,000,000 events unless an earlier hard failure occurs.

At each checkpoint report **actual sealed canonical member + inventory/root bytes**, not uncompressed logical-wire bytes, and actual scratch peak separately.

Compute actual steady-state bytes/event and projected full WVS7 steady-state bytes.

Frozen decision thresholds:

- preferred-density target: `<= 36 B/event` (approximately <= 2 GiB WVS7);
- hard-density target: `<= 72 B/event` (approximately <= 4 GiB WVS7);
- if 1M+ representative-event actual sealed density is `> 72 B/event`, STOP: `R5_LONG_COMPACT_V2_BLOCKED__DENSITY_HARD_GATE`;
- if `36 < density <= 72`, return measured evidence for HQ practical/storage adjudication; do not self-pass to full source;
- if `<= 36`, density gate PASS and bounded/full semantic courts may proceed.

## 6. REQUIRED REPAIR COURT

Before any full-source rerun, require:

1. complete fresh R5 unit/regression suite;
2. old JSON-row versus compact-member reconstructed `R5CanonicalRow` identity on hostile bounded fixtures;
3. exact content-hash recomputation parity;
4. signed-zero/type/missing-declaration/label/Unicode/control-text parity;
5. independent C11 reconstruction/ref parity;
6. all G3 oracle mutants still rejected and benign relayout accepted;
7. fixed-bound increasing-N memory plateau;
8. corruption/inventory/member/TOCTOU/publication/CAS fail-closed behavior on the new member format;
9. cacheless frozen I03/I05/I04 parity including blind-I05 protocol;
10. determinism/relayout semantic identity;
11. exact WVS7 prefix density gate above.

If repair requires semantic weakening, STOP with `R5_LONG_COMPACT_V2_BLOCKED__FROZEN_CONTRACT_CONTRADICTION`.

## 7. LiTS V1 COURT

The pristine branch `agent/vozhd-trii-r5-full-lits1-real-source-court` SHALL NOT execute the failed JSON-row V1 candidate. Its result would not add decision-relevant evidence after the WVS7 representation hard-gate witness.

Preserve the branch untouched as historical launch state. A LiTS court will be reissued only against a repaired candidate that passes the density and bounded equivalence gates.

## 8. FORWARD LAW

If compact LONG V2 passes all bounded/equivalence/density gates, HQ may authorize fresh WVS7 and LiTS full-source courts against the repaired implementation.

Only if compact LONG cannot satisfy the frozen storage/practical boundaries without semantic loss does Authority 56 permit consideration of `QUESTION_BLOCKED_LONG`.

No third broad architecture/design campaign is authorized.
