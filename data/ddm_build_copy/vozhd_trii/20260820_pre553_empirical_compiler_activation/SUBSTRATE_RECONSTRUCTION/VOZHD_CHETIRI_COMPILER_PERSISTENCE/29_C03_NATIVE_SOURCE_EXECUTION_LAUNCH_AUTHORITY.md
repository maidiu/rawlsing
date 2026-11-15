# VOZHD CHETIRI — C03 NATIVE SOURCE EXECUTION LAUNCH AUTHORITY

Short tag: `VC4/C03-LAUNCH`

Status: `AUTHORIZED__P1A_C03_ONLY__G0_PASSED__NO_ARCHITECTURE_SELECTION`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Binding parent:

- `G0_C02R2_HQ_ADJUDICATION/G0_FINAL_ADJUDICATION.md`
- `12_SEQUENCE_DEPENDENCY_AND_GATE_PROTOCOL.md`
- `21_POST_FORWARD_CROSSWALK_CELL_ASSIGNMENT_AMENDMENT.md`
- `WORKER_ORDERS/C03_NATIVE_SOURCE_EXECUTION_RECON.md`

## 0. AUTHORIZATION

G0 has passed as:

`G0_PASS__SOURCE_BACKED_REMAINS_LAWFUL_ONLY_WITH_EXACT_NAMED_PERSISTENT_SIDE_MATERIAL`

C03 is therefore authorized as the only P1A cell.

C04, C05 and C08 remain locked until C03 returns and HQ accepts it.

C03 measures physical native-source execution terrain only. It may not select A/B/C, decide persistence architecture, change source/decoder/C11 semantics, or interpret reader cost as semantic authority.

## 1. LOCAL SOURCE ROOT

Expected local proving-source root:

`/Users/matthewsmith/Desktop/Rawlsing/data/Data`

Every source read requires exact byte-size/SHA verification against `../SOURCE_BYTE_INVENTORY.csv` before measurement.

## 2. HQ-PINNED PROVING SOURCES

### S1 — ordinary SAV / large real source

File: `WVS Wave 7.sav`

Expected SHA-256:
`2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Expected bytes:
`185163494`

Reader path:
`pyreadstat.read_sav`, frozen default reader configuration.

Why pinned:
- ordinary non-compatibility SAV path;
- 97,220 × 613 large source already repeatedly court-proven;
- appropriate for selected-column/full-read/chunking/setup/amortization measurements.

### S2 — compatibility SAV

File: `EVS 2008.sav`

Expected SHA-256:
`5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379`

Expected bytes:
`63832833`

Reader path:
`pyreadstat.read_sav` with frozen `encoding=latin1` compatibility execution override.

Authority class:
`COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`

Why pinned:
- materially distinct SAV compatibility path;
- contains accepted native multiple-response metadata;
- useful for compatibility/full-frame versus ordinary-path cost comparison.

### S3 — compatibility DTA proving path

File: `LiTS_I.dta`

Expected SHA-256:
`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

Expected bytes:
`139531180`

Reader path:
`pyreadstat.read_dta` with frozen `encoding=latin1` compatibility execution override.

Authority class:
`COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`

Why pinned:
- accepted LiTS physical hostile fixture;
- 29,002 × 1,198 source;
- ordinary values/system-missing distinction already source-censused;
- useful representative DTA execution path.

### S4 — LiTS III hostile DTA path

File: `LiTS_III.dta`

Expected SHA-256:
`368ae5d07a44975a2f0a9ce3b1e564988a966b2632e28075c56a24d60065bcc8`

Expected bytes:
`170487994`

Reader path:
`pyreadstat.read_dta` with frozen `encoding=latin1` compatibility execution override.

Authority class:
`COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`

Why pinned:
- named C03 hostile source for chunk/full-read behavior;
- must be tested fail-closed rather than generalized from LiTS I.

## 3. ORDINARY DTA DISPOSITION

No ordinary/non-compatibility DTA source exists in the current CLOSED_35 corpus.

The four governed `.dta` sources are LiTS I, II, III and IV, and all four are among the six exact compatibility-reader snapshots accepted by SR03.

Therefore C03 SHALL record:

`ORDINARY_DTA_PATH_WITHIN_CLOSED_35 = NOT_AVAILABLE`

It shall not synthesize an ungoverned ordinary-DTA fixture merely to fill the matrix.

## 4. REQUIRED MEASUREMENT EMPHASIS

For each applicable source/path, execute the C03 order's matrix, including when supported:

- metadata-only open;
- full variable metadata extraction;
- selected variables at 1 / 2 / 5 / 10 / 25 / 50 / 100;
- repeated selected-variable sessions;
- sequential full read;
- chunked/row-range read;
- repeated chunked read;
- source open/setup latency;
- decode/normalization latency where separately observable;
- peak RSS;
- transient frame size where observable;
- scratch;
- exact failure mode;
- whether reader forces full-frame allocation;
- whether column selection is physically selective or API-level only;
- whether one session/transient working set can amortize many predicates.

Run enough repetitions to distinguish startup noise from stable cost; report the run count and aggregation method.

The worker should expose hidden parser/full-read work, not infer it from API names.

## 5. G0 PRESERVATION CONSTRAINTS

C03 must carry these accepted facts without re-adjudicating them:

- raw payload remains authoritative/reconstructable from exact source bytes under frozen decoder law;
- semantic question/component/topology/occurrence/routing authority is distinct side material;
- no full duplicate event payload is semantically required by G0;
- source-backed B and hybrid C remain lawful candidates;
- R5 A remains a lawful comparator;
- C03 decides only physical execution terrain.

A large transient decoded wave image is lawful to identify as an execution possibility if exact/regenerable; C03 may not decide whether it should persist.

## 6. RESOURCE / CONCURRENCY HYGIENE

C03 must use its own uniquely named scratch directory and must not inspect, reuse, delete, or mutate scratch owned by other concurrent agents.

Do not touch `/private/tmp/SR03_SOURCE_PHYSICAL_MANIFESTS_C02R2.UeJtmj` or any other unrelated agent scratch.

No source, runtime, R5, database, or authority mutation is permitted.

## 7. REQUIRED RETURN

Use the outputs required by `WORKER_ORDERS/C03_NATIVE_SOURCE_EXECUTION_RECON.md` and the common worker contract, including the 34-row terminal checksum.

The return must identify every exact proving source, SHA, decoder invocation, measurement repetition count, failure/unsupported surface, and scratch disposition.

Allowed final dispositions remain exactly those in the C03 worker order.

STOP token:

`VC4_C03_RETURNED`
