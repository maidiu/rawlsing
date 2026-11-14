# PYAT #997 — R4 compiler-issuance correction

## Status

**`CORRECTION_COMPLETE__R3_QUERY_CLAIM_WITHDRAWN__COMPILER_ISSUED_DISCOVERY_PASS__NO_ELIGIBLE_QUERY_FOUND__NOT_G5`**

- Candidate: `2c476e739a263dd0069b54706c6cfa63b07190c1`
- Startup: `11d6f480349a09b871414c3dc1c3f4fa3e680797`
- Branch: `agent/pyat997-native-proof-r1`
- Product/test/source edits: **NONE**
- Canonical product diff: **EMPTY**
- This is author correction / existing-compiler evidence, **not G5**.

## Explicit withdrawal

The R3 claim of a compiler-issued Batch QUERY/F4 and a two-unit
PARTIAL/ABSENT is **withdrawn**.

Withdrawn:

- compiler-issued Batch QUERY
- compiler-issued F4
- two-unit compiler-issued PARTIAL/ABSENT
- the R3 manual `NativeWorkload` / `IssuedWorkloadRecord` replacement of
  `compilation.issued`

Preserved from prior immutable history:

- P0 one-source 13-family persisted S2-C estate
- direct q101 mechanical I03 SUPPORTED 5/5
- discovery/I05 150 candidate receipts, 147 positive-linked operations
- 75/75 test-patch proof (Browser-owned, not adopted)
- fresh source/body boundary (its manual Batch QUERY is not accepted)
- all35 historical ledger in the independent review

## G5 mismatch reproduced

The independent witness was run against this exact checkout:

```text
compiler_has_query_unit: false
manual_has_query_unit: true
same_compiler_record: false
same_compiler_workload: false
joint_query_in_compiler_plan: []
f4_like_dispositions: ["PROHIBITED"]
red: true
```

Evidence: `evidence/witness_reproduction.txt` (exit code 1).

## Actual unchanged compiler record

`compile_governed_frontier` returned, unchanged:

```text
workload.requests    = 0
workload.discoveries = 1
record.expected_jobs = [DISCOVERY only]
```

Exact record:

- decision:
  `TEST_ONLY_DECISION|urn:rawlsing:b49:test_only_decision:r03-discovery-cfc02dd9c78ecc3f-2026-11-13|7c5b8e6a47621e519a9c593ff61d6b4fb89c4fcc786f1b72c435db8dc24ba4fa`
- expected job: DISCOVERY authority
  `…8a4d8fa80d9cc44124a894d4c6e8bece4a5cade5a6078d078fbf3e66442e2f88`
- envelope SHA-256: `a7c9521c06780904290523cf51c26f52a1ba785a0202342bb72aead62d3eca2f`
- record and workload equal before/after execution: **true**

No `NativeWorkload`, `IssuedWorkloadRecord`, request, discovery or
`replace(compilation, issued=...)` was created by the correction harness.

## Actual compiler-issued execution

- NORMAL: **1 unit, COMPLETED**, 150 output refs
- COMPLETED checkpoint resume: **1 completed result**, 150 output refs,
  equal to full
- source opens: **0**
- full C11 repository builds: **0**

PARTIAL/ABSENT against a two-unit workload is **not proved**: the actual
compiler-issued workload has one DISCOVERY unit.

## Direct q101 is standalone only

Direct q101 I03:

`urn:rawlsing:pre553:EmpiricalFact:sha256:b7666641c966a6530412dfb4730539852fbf6f6ca21e6bdd77e958b5a0048231`

Typed state `SUPPORTED`, but this is a mechanical direct I03 query, not a
compiler-issued Batch QUERY and not original P1 issuance.

## Actual F4-like negative

The 12 F4-like `JOINT` / `CO_TRAVEL` `SAMPLE` operations over
q101/q102/q103 are all:

```text
PROHIBITED
```

The selected joint catalog query is absent from every `plan.records`
`query_refs`. It is not eligible compiler issuance.

## Existing fixture consultation

Searched existing S1-C/R03/native tests for an unchanged
`compile_governed_frontier` query issuance example. The accepted path uses its
issued DISCOVERY workload; `compile_universal_workload` is a separate
single-target test-only path, not the unchanged `compile_governed_frontier`
`.issued` contract. No policy/claim-class switch was made.

## Resource

| Measure | Actual |
|---|---:|
| Respondents | 5 |
| Questions | 3 |
| Source reads / decode / cell passes | 1 / 1 / 1 |
| Full C11 builds | 0 |
| 13-family Parquet members | 14 |
| Retained bytes | 626,698 B |
| Stage bytes | 913,418 B |
| Parent max RSS | 223,649,792 B |
| 100k / 6 GiB | **NOT_RUN** |

The correction harness launches no child process; parent max RSS is the
single-process tree bound.

## Product P1 negative remains open

`join_saved_source_operation_fates` accepted the R3 manual replacement when
comparing against the already-replaced `compilation.issued.record`. The
Browser P1 owner has received the exact G5 RED for guard repair. **No product
edit was made here.** Correcting the harness stops the attack; it does not
close the product defect or make G5 pass.

## Gates

- **G1 `FAIL_ORIGINAL_QUERY_ISSUANCE / CORRECTION EXACT`** — actual compiler
  emits 0 QUERY; query absent from plan; 12 F4-like operations PROHIBITED.
- **G2 `PARTIAL_SCOPED`** — compiler-issued discovery NORMAL/COMPLETED and
  preserved P0/direct q101/discovery are real; no eligible compiler QUERY.
- **G3 `PARTIAL_SCOPED`** — F4 is not issued/eligible; negatives and
  PROHIBITED fates preserved.
- **G4 `PASS_SCOPED_SMALL`** — resource values above; 100k NOT_RUN.
- **G5** — independent review remains `REVISE_EXACT_DEFECT`; this correction is
  not acceptance.

## Single Browser/R03 owner question

**Which existing lawful TEST_ONLY sourcefree claim/fixture is intended to issue
an actual eligible QUERY unit under the unchanged
`compile_governed_frontier`, or what exact missing R03/issuer binding must its
rightful owner implement?** The current compiler emits zero QUERY requests and
all 12 q101/q102/q103 F4-like operations are PROHIBITED.

## Remaining holds

- S2-A native kernel (`pre553_direct_estate_i03.py` `8b4d5ca`) remains a
  separate HOLD.
- Browser test-patch adoption remains Browser-owned.
- Original35/source/current/science, protected merge, #998 full joined,
  #1001 full scale, #1006, N11/N12 and 100k/6 GiB remain separate holds.
- No new engine, registry, issuer or science policy.

## Courts

- **Engineering:** actual compiler-issued discovery NORMAL/COMPLETED passes;
  actual QUERY issuance is absent. R3 query/F4/PARTIAL/ABSENT claims withdrawn.
- **Science:** sourcefree TEST_ONLY 5-respondent generated fixture only; no
  original35 science or original population/causal claim. F4 numeric output is
  mechanically real but attached to PROHIBITED/unissued operations.
- **Authority:** TEST_ONLY only; no production CURRENT, issuer, source
  permission, protected merge, or authority grant.

## Self-critique

- The correction does not turn the absent compiler query into a positive.
- It does not close the Browser P1 guard defect or G5.
- It preserves prior false claims as immutable history while withdrawing them
  in this new receipt.
- The q101 direct result is retained as a mechanical standalone only.
