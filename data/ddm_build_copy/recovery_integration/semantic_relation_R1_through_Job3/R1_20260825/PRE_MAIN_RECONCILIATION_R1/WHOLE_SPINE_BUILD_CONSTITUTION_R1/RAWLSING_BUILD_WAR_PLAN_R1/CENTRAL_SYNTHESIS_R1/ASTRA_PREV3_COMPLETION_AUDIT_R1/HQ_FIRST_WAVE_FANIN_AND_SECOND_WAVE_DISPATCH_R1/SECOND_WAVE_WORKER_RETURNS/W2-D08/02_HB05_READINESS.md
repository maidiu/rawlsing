# W2-D08 — HB05 readiness disposition R1

Status:

`HB05_FINAL_EXECUTABLE_TWO_SOURCE_WORKLOAD_MANIFEST = READY_FOR_SEPARATE_COMMISSION`

HB05 remains a **final freeze construction task**, not physical bakeoff execution.

## 1. Exact prerequisite closure

The last accepted B frontier held HB05 only on HB01/WVS7 after Route A, Route C and HB04 common harness closure. HQ has now accepted HB01 full WVS7 source-backed certification.

Historical readiness row R36 classified the missing object as:

`FINAL_C09_EXECUTABLE_WORKLOAD_MANIFEST_NOT_YET_SEALED`

with closing action:

`YES__AFTER_PREREQUISITES`

and with no real-source execution required for the manifest seal itself.

Its explicit dependencies were C05R2B, WVS7 and C08/G1. Those are now satisfied by B16, HB01 and B17 respectively.

## 2. Frozen mandatory source identities

### WVS7

- source SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
- rows: 97,220
- logical variables: 613
- accepted selected-projection SHA-256: `7e69d799e37d26c2e6ae749674d4994a276f93aaf89e43085bed34a5fd122ec9`
- accepted C11 release content hash: `a7053b1169dc42d3af348eb96771fe89476ca30b13dccafb982ea39d7f67ee8d`
- decoder invocation template remains `decode_sav(source_path)`.

### LiTS-I

- source SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- accepted real production return: `40a0a0529fa78765c7fc87f7e1f12260a2335f72`
- accepted production seal blob: `0ebf319c0e6695b077b9ca70b9119007fecfcdcd`
- decoder invocation template remains `decode_dta(source_path, encoding=latin1)` at its compatibility-execution-only ceiling.

HB05 must bind source identities and decoder/config semantics, but it must not invent the final host-specific source paths. Those paths belong to HB07/final C09 launch-packet instantiation.

## 3. Frozen candidate-neutral execution spine

Consume exactly:

- qualified A/B/C intake `49A_HB04_QUALIFIED_ABC_INTAKE_FREEZE_R1.json`, canonical SHA-256 `906973f78cd82678f678a9a803bb3c3c7f9e13b30e39a5f8dc3ea093d4390e88`;
- HB04 implementation freeze `51A_HB04_COMMON_HARNESS_IMPLEMENTATION_FREEZE_R1.json`, canonical SHA-256 `138482116b566482075e191800229f81357541d674646552e8c269e7640a755e`;
- accepted B21Q `46acf0b162bdcac5f47ce9cce0d9bb1d039fae2d`;
- C09 exact order blob `e200a9aed7dbdf103ab9306d0dd19b74662faf1b`;
- C09 measurement/bakeoff law blob `2729ab4dca887f22fb3c90265f10c70020afdd3e`.

No candidate may receive a workload unavailable to another candidate at the same governed semantic grain.

## 4. Minimum logical workload universe to freeze

HB05 must seal an executable manifest that preserves the C09 law's operation universe, including, where semantically applicable:

1. source metadata / exact identity verification;
2. source open/decode setup;
3. broad sequential scan;
4. governed C11 reconstruction sample / hostile C11 case;
5. univariate distribution;
6. 2-way conjunction;
7. 3-way conjunction;
8. 5-way conjunction;
9. conditional distribution;
10. subgroup / risk-set-correct operation;
11. weighted/design operation **only where exact authority exists**;
12. topology-general gather / hostile topology case;
13. representative I05 primitive batch;
14. autonomous discovery program lane only at the exact current authorized search/termination ceiling;
15. provenance / receipt generation;
16. semantic/replay audit primitive;
17. close/reopen and fresh-process repeat;
18. interrupted-build/recovery where the candidate contract defines it;
19. delete-all-caches rebuild;
20. learned/objective service rows required by current law, with exact typed blocked states where their authority is not positively closed.

The manifest must distinguish logical operation identity from candidate-specific physical implementation mechanics.

## 5. Bounded-evidence requirements

Apply current objective-consumer law exactly:

- `SOURCE_LOCAL_CERTIFIED` is not population/design/weighted authority;
- missing routing, risk-set, validation, comparability, composition or other required authority remains typed unavailable/blocked;
- no nearest-source substitution;
- no implicit pooling/backfill;
- no missing-as-zero/false;
- no silent coefficient/dimension/claim-scope renormalization;
- no broad prior by convenience;
- no psychic/driver/type fallback;
- no operation is silently dropped merely because it is currently blocked if the frozen C09 semantic envelope requires its blocked state to remain visible.

HB05 may encode an operation as `BLOCKED_MISSING_AUTHORITY`, `UNAVAILABLE`, `ROUTING_UNKNOWN`, `NOT_APPLICABLE`, or another already-governed exact state when current authority requires that outcome. It may not convert that state to a weaker task for benchmarking convenience.

## 6. Required HB05 output contract

The successor worker should return at least:

- `00_RETURN.md`
- `01_FINAL_EXECUTABLE_TWO_SOURCE_WORKLOAD_MANIFEST.json`
- `02_MANIFEST_AUTHORITY_AND_SOURCE_BINDINGS.tsv`
- `03_EQUAL_WORKLOAD_HOSTILE_COURT.md`
- deterministic canonical SHA-256 for the final manifest
- explicit statement that no A/B/C execution, timing, ranking or selection occurred.

The final manifest should contain:

- mandatory source IDs/hashes;
- decoder/config templates;
- A/B/C frozen intake identity;
- common harness identity;
- operation IDs and semantic request contracts;
- per-source applicability / authority state;
- exact expected positive or typed-negative state class (without inventing numeric/golden values owned by HB06);
- cold/warm/repeat dimensions where required;
- parity-before-performance gate marker;
- candidate-neutral resource-observation hooks, without collecting performance results.

## 7. Hard stops

HB05 must not:

- execute A/B/C;
- collect comparative performance measurements;
- construct the HB06 oracle;
- seal HB07 host-specific paths/scratch/cleanup;
- launch C09;
- rank/select candidates;
- launch OBL037;
- add a third Route-C accelerator;
- weaken source/evidence authority to make the manifest executable;
- revive any OBL063 psychic terminal prerequisite.

## 8. Readiness terminal

`HB05_READY_FOR_PARALLEL_HQ_COMMISSION_WITH_HB06__FINAL_MANIFEST_FREEZE_ONLY`
