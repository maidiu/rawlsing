# PYAT #997 — R3 issued Batch/F4/resume proof

## Status

**`R3_ISSUED_QUERY_F4_RESUME_PASS_SCOPED__NOT_G5`**

- Candidate: `2c476e739a263dd0069b54706c6cfa63b07190c1`
- Startup: `bf4e8c9a4f6586071689f3400ca3d24b2d5a0bb5`
- Branch: `agent/pyat997-native-proof-r1`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat997-native-proof`
- Product/test/source edits: **NONE**
- Canonical product diff: **EMPTY**
- This is native executor evidence, **not G5** and not a 998 import.

## Fixture and compiler provenance

A generated TEST_ONLY four-column SAV with **q101, q102, q103, country** was
built with the existing `make_config` fixture constructor plus explicit
q102/q103 response, physical, question and routing entries. The existing
`_native_document` authority/domain normalization was applied. The source has
five respondents and no original35 bytes.

The Q2 body tee produced one S2-C persisted estate with:

- `QuestionVariableBinding` 3
- `RespondentEvent` 15
- `RoutingEligibilityFact` 15
- `EmpiricalCoordinateFact` 5
- `WeightMeasureFact` 0
- 13-family estate: 14 Parquet members
- Source reads `1`, decode calls `1`, cell passes `1`, full C11 builds `0`

The existing `compile_governed_frontier` with policy `j=3,k=2,d=1` generated the
joint q101×q102×q103 query in its runtime catalog. The harness selected that
exact compiled query (not a handwritten query), then used existing
`NativeWorkload`, `IssuedWorkloadRecord`, `TestOnlyDecisionResolver` and
`SavedC11Admission` constructors to create a valid TEST_ONLY issued record.

**Issued workload:** 1 QUERY + 1 DISCOVERY Batch unit. The query is the actual
compiler-catalog q101/q102/q103 query; no production issuer, source permission,
catalog monkeypatch, or direct-I03 bypass was used.

## Actual F4

- Query:
  `urn:rawlsing:pre553:EmpiricalQuerySpec:sha256:8b27ab837310b04e2019e897f3b57a5c8e202cbaf4c1598f6dfb8c1621fb3aa7`
- Fact:
  `urn:rawlsing:pre553:EmpiricalFact:sha256:1870057e3a5797bf9229708a4599a2b9c97fa780783315563bdd8a3e3dd40458`
- `typed_state`: `SUPPORTED`
- Target arity: **3**
- Complete cells: **8**
- Denominator: **5**
- Same-respondent joint, not sums of marginals:

| X/Y/Z | numerator | state |
|---|---:|---|
| 0,0,0 | 1 | OBSERVED_POSITIVE |
| 0,0,1 | 1 | OBSERVED_POSITIVE |
| 0,1,0 | 1 | OBSERVED_POSITIVE |
| 0,1,1 | 0 | OBSERVED_ZERO_IN_SUPPORTED_RISK_SET |
| 1,0,0 | 0 | OBSERVED_ZERO_IN_SUPPORTED_RISK_SET |
| 1,0,1 | 1 | OBSERVED_POSITIVE |
| 1,1,0 | 0 | OBSERVED_ZERO_IN_SUPPORTED_RISK_SET |
| 1,1,1 | 1 | OBSERVED_POSITIVE |

## Batch / readers / fate join

- Batch: **2 units, both COMPLETED**; 1 QUERY + 1 DISCOVERY; 151 result refs
- Normal saved workload: **2 units, both COMPLETED**; 151 output refs
- Partial prefix: 1 unit, resumed prefix 1, full 151 output refs
- Absent checkpoint: resumed prefix 1, full 151 output refs
- No source factory call on saved normal/resume paths
- Joining:
  - result hash:
    `6fcd3753d5931c3fb96e9d59481b7a3dfb5c207020e689c4c5002f66dd54d15d`
  - operations: **2140**
  - preconsumer fates: **536 ELIGIBLE, 1076 HELD, 528 PROHIBITED**
  - positive native-linked operations: **147**
  - discovery candidates exactly joined: **150**
  - pending eligible: **389**
  - issue grants created: **0**
  - preconsumer handoff unchanged: **true**

## Changed source -> changed F4 -> exact restore

- Baseline source SHA:
  `a1875643565211ad1d0f76d0f314cf38e618625ffc7dc46aed1c49677b09eafa`
- Changed source SHA:
  `1fb4c408f141afac7065396a0b079e2abb44eb343870478b3be08f2b7a258f76`
- Changed F4 fact:
  `urn:rawlsing:pre553:EmpiricalFact:sha256:7c5c3c635b04ea3ed79d45c95bb576c75c3f453c8908f2c8d6c75a74a7e2b0a0`
- Restored source SHA equals baseline.
- Restored F4 fact equals baseline exactly.
- Restored logical root:
  `911bf8a3eca490366bfd4d633b9ae33fdcadfea9226ba86793c385a28480e937`
- Restored join hash equals baseline:
  `6fcd3753d5931c3fb96e9d59481b7a3dfb5c207020e689c4c5002f66dd54d15d`

## Fresh process proof

A producer interpreter built the Q2 3-question estate, executed the actual
issued Batch/I03/I05 oracle, wrote a capsule, and exited. The source file was
deleted. A **new interpreter** then opened only `SavedC11Admission` and:

- consumer source opens: **0**
- consumer full C11 repository builds: **0**
- I03 fact refs equal: **true**
- I05 receipt refs equal: **150** receipts
- Batch states/count equal: **2 COMPLETED**
- producer source reads/decode/cell passes: **1/1/1**

Evidence: `evidence/fresh_process_proof.json`,
`evidence/fresh_process_run.txt`.

## Negative witnesses

- forged HELD promotion:
  `Q2_ORIGINAL_FROZEN_FATE_CENSUS_DRIFT`
- Q2/R03 frontier mismatch:
  `Q2_R03_ORIGINAL_FRONTIER_HASH_DRIFT`
- missing receipts: no positive native-linked operations
- wrong root: `DirectEstateError`
- revoked CURRENT:
  `DirectEstateError: current source/operation authority refused`

## Resource accounting

| Measure | Actual |
|---|---:|
| Respondents | 5 |
| Retained estate | 626,679 B |
| Stage | 913,399 B |
| Parent max RSS | 259,137,536 B |
| Source reads | 1 |
| Decode calls | 1 |
| Cell passes | 1 |
| Full C11 builds | 0 |
| Parquet members | 14 |
| Full 100k / 6 GiB | **NOT_RUN** |

The R3 harness launches no child process; its parent max RSS is the
single-process process-tree bound. The fresh producer/consumer separately
record their own process boundaries.

## Gates

- **G1 PASS_SCOPED** — candidate pins, exact TEST_ONLY source fixture, compiler
  joint-query provenance, no product edits.
- **G2 PASS_SCOPED** — actual issued Batch query/I03/I05, NORMAL, changed source,
  exact restore, fresh producer/consumer.
- **G3 PASS_SCOPED** — same-respondent 8-cell F4, denominator 5, 147 positive
  linked operations, held/frontier/missing-receipt/wrong-root/revoked refusals.
- **G4 PASS_SCOPED_SMALL** — resource values above; 100k/6 GiB NOT_RUN.
- **G5 NOT_RUN** — independent nonauthor acceptance required.

## Engineering / science / authority

- Engineering: actual compiler-derived issued Batch query and saved readers
  executed against the persisted Q2 estate.
- Science: no original35 source, current source rights, or scientific issuance.
- Authority: TEST_ONLY sourcefree; no production CURRENT, issuer, source
  permission, host grant, protected merge, or #1002 authority.
- #1006 benchmark: not run.

## Coverage not proved

- Original35 source/rights/science and production CURRENT.
- Universal 100k respondents / 6 GiB.
- Independent nonauthor G5.
- Production Batch query authorization or source permission.
- Any causal/structural/original-population claim.

## Next dependency

Browser #997 owner and a genuinely distinct reviewer can receive this exact
bounded evidence. The next indispensable step is independent G5 on the frozen
candidate plus the full original S1-E/997 scope. Do not treat this as accepted
997 or 998 integration.

## Self-critique

- The fixture is small and TEST_ONLY; not original35.
- The joint query is compiler-catalog exact, but the TEST_ONLY issued record was
  constructed with existing constructors; it is not a production issuer.
- The F4 cell table is actual joint output, not marginal multiplication.
- The R3 harness uses one process; the separate fresh proof supplies the
  producer-exit boundary.
- Batch query and discovery both execute; no query unit was minted beyond the
  compiler-derived TEST_ONLY record.
