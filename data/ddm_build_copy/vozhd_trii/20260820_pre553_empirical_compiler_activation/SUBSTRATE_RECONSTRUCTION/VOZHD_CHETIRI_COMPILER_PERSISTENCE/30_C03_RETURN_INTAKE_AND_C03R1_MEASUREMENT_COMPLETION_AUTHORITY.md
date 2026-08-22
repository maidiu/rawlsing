# VOZHD CHETIRI — C03 RETURN INTAKE & C03-R1 MEASUREMENT COMPLETION AUTHORITY

Short tag: `VC4/C03-INTAKE-R1`

Status: `HQ_REVIEW__CORE_WITNESS_ADMISSIBLE__CELL_ACCEPTANCE_WITHHELD__BOUNDED_MEASUREMENT_COMPLETION_AUTHORIZED`

Repository: `maidiu/rawlsing`

C03 branch: `agent/vozhd-chetiri-c03-native-source-access`

Exact C03 launch head: `e7e32b4d0dcb1fec0554158a2051673291c1ebf7`

Exact C03 return head: `4ba1ed44c0385a9963c0a79eb84332ee5896f6dd`

## 1. HQ INTAKE HOLDING

The C03 return is correctly descended from the exact launch head and changes only the authorized `returns/C03/` scope.

The following C03 evidence is admissible and shall NOT be discarded or rerun for semantic reasons:

- all four HQ-pinned proving sources passed exact source identity gates;
- ordinary SAV, compatibility SAV, compatibility DTA, and hostile LiTS III DTA paths all accepted selected-column reads;
- all four accepted bounded row-range/chunk requests;
- 1/10/100 selected-column observations were materially faster than full-frame reads on every proving source;
- a material per-open/setup floor was observed;
- current observation surfaces did not prove byte-level physical I/O selectivity;
- no semantic, source, decoder, runtime, R5, database, or authority mutation occurred.

This supports a real but intentionally narrow physical conclusion:

`NATIVE_READER_API_SUPPORTS_BOUNDED_SELECTED_AND_CHUNK_REQUESTS__FRESH_CALLS_HAVE_MATERIAL_SETUP_COST__BYTE_LEVEL_PRUNING_UNPROVEN`

HQ does NOT yet accept the worker's final C03 disposition because the mandatory measurement contract was not fully executed/receipted.

## 2. EXACT ACCEPTANCE DEFECTS

### D1 — incomplete width grid

Launch authority 29 required selected-variable measurements at:

`1 / 2 / 5 / 10 / 25 / 50 / 100`

The checked-in capability matrix exposes only:

`1 / 10 / 100`

The missing `2 / 5 / 25 / 50` points must be measured.

### D2 — repetition law not satisfied

Authority 29 required enough repetitions to distinguish startup noise from stable execution cost and required run count + aggregation method.

The returned cost model states that each matrix point is principally one cold-process observation, with only limited extra WVS/repeated-10-column observations.

This does not satisfy the binding repetition law.

### D3 — RSS unit receipt unresolved

The matrix column is labeled `full_peak_rss_kib`, while the raw macOS values are inconsistent with that unit if interpreted literally. HQ will not silently relabel them.

C03-R1 must establish the exact unit by a deterministic calibration/cross-check and return both raw and normalized byte values with the measurement mechanism named.

### D4 — return manifest not sealed

`RETURN_MANIFEST.json` still contains:

`"return_sha": "TO_BE_FILLED_AT_COMMIT"`

and does not fully satisfy the common worker manifest minimum schema.

C03-R1 must seal the exact C03/C03-R1 identities and complete the minimum manifest receipt.

## 3. DISPOSITION

C03 state becomes:

`HQ_REVIEW__CORE_EVIDENCE_ADMISSIBLE__ACCEPTANCE_WITHHELD_PENDING_C03R1`

C04, C05 and C08 remain locked.

No architecture candidate is selected or demoted.

No source/decoder/C11/I03/I05/I04/V553+/V3/V2 law changes.

## 4. C03-R1 ROLE

C03-R1 is a **dumb local measurement-completion executor** suitable for a cost-sensitive local agent.

It may not reinterpret C03, decide architecture, infer I03/I05 feasibility, or make persistence recommendations.

Exact mission:

`COMPLETE_THE_ORDERED_MEASUREMENT_GRID__REPEAT_IT_DETERMINISTICALLY__CALIBRATE_UNITS__SEAL_RECEIPTS__STOP`

Worker branch:

`agent/vozhd-chetiri-c03r1-native-source-measurement-completion`

Launch base:

`CURRENT_EXACT_CONTROL_HEAD_AT_HANDOUT`

Read-only evidence object:

C03 exact return `4ba1ed44c0385a9963c0a79eb84332ee5896f6dd`.

The worker may read only the C03 return bundle from that exact commit plus governing/source/decoder authorities. It may not merge/cherry-pick C03.

## 5. PINNED SOURCES

Use the same four exact sources and frozen reader paths from Authority 29:

1. `WVS Wave 7.sav` — ordinary SAV;
2. `EVS 2008.sav` — `encoding=latin1` compatibility SAV;
3. `LiTS_I.dta` — `encoding=latin1` compatibility DTA;
4. `LiTS_III.dta` — hostile `encoding=latin1` compatibility DTA.

Verify exact byte size and SHA before measurement.

Do not introduce an ordinary DTA fixture outside CLOSED_35.

## 6. FIXED MEASUREMENT HARNESS

For EACH of the four sources, execute exactly these fresh-process cases:

- metadata-only open;
- selected columns: `1, 2, 5, 10, 25, 50, 100`;
- 1,000-row / 10-column bounded chunk;
- sequential full read.

Column selection rule:

- obtain native variable order from the frozen reader's metadata surface;
- for width `N`, select the first `N` native variables in exact source order;
- record the exact variable list or a deterministic hash plus first/last names.

Chunk rule:

- first 10 native variables in source order;
- `row_offset=0`;
- `row_limit=1000`;
- use the frozen source-specific reader invocation.

Repetition rule:

- execute **3 fresh child-process repetitions per case**;
- do not reuse a decoded frame between repetitions;
- report all 3 raw wall times;
- report median, min, max;
- report raw peak-RSS measurement for every run;
- report the measurement mechanism and exact unit.

This is a measurement-completion court, not a performance-maximization exercise.

## 7. RSS UNIT CALIBRATION

Before source benchmarking, run one deterministic memory calibration child process that allocates and touches a known `64 MiB` byte buffer and sleeps briefly.

Measure its peak RSS using:

1. Python `resource.getrusage(...).ru_maxrss` raw value; and
2. `/usr/bin/time -l` maximum-resident-set output if available on the host.

Record both raw observations and their ratio.

Infer the reporting unit only from the host evidence. If the two surfaces cannot establish a trustworthy normalization, retain raw values and return:

`RSS_UNIT_NOT_CLOSED__DO_NOT_NORMALIZE`

Do not guess.

## 8. REQUIRED OUTPUTS

Write only under:

`VOZHD_CHETIRI_COMPILER_PERSISTENCE/returns/C03R1/`

Required:

- `AUTHORITY_READ_RECEIPT.md`
- `SOURCE_IDENTITY_RECEIPT.csv`
- `RSS_UNIT_CALIBRATION.md`
- `C03R1_RAW_RUNS.csv`
- `C03R1_AGGREGATED_MEASUREMENTS.csv`
- `C03R1_COMPLETENESS_MATRIX.csv`
- `C03R1_DELTA_TO_C03.md`
- `C03R1_EXECUTION_RESULT.json`
- `RETURN_MANIFEST.json`
- `CHANGED_FILES.txt`
- `SCRATCH_CLEANUP_RECEIPT.md`

Do NOT regenerate the 34-row semantic checksum. HQ already has the C03 checksum and C03-R1 has no semantic jurisdiction.

## 9. C03-R1 ALLOWED STATUSES

Exactly one:

- `C03R1_COMPLETE__ORDERED_MEASUREMENT_GRID_AND_REPETITIONS_RETURNED__HQ_ACCEPTANCE_REQUIRED`
- `C03R1_BLOCK__PINNED_SOURCE_IDENTITY_FAILURE`
- `C03R1_BLOCK__FROZEN_READER_EXECUTION_FAILURE`
- `C03R1_BLOCK__LOCAL_RESOURCE_HARD_GATE`
- `C03R1_BLOCK__REQUIRED_MEASUREMENT_NOT_EXECUTABLE`

C03-R1 may NOT issue a C03 architecture/execution-feasibility disposition.

## 10. SCRATCH / CONCURRENCY LAW

Use unique C03-R1 scratch only.

Do not inspect, reuse, delete, or mutate scratch owned by any other agent.

No source, runtime, R5, database, test, semantic-authority, or governing-authority writes.

## 11. RETURN TO HQ

Return only:

- exact start SHA;
- exact worker branch;
- exact return SHA;
- source identity gate result;
- case count expected/executed;
- repetitions per case;
- RSS calibration result;
- missing/unexecuted cases;
- scratch cleanup status;
- exact C03-R1 status;
- output paths;
- STOP token.

STOP token:

`VC4_C03R1_RETURNED`
