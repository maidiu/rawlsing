# WG0P2 actual C11 / I03 / batch execution (or exact hold)

All owner dependencies executed. No blocker: every accepted-owner call in the
repair path ran against the live tree. I05 discovery and Route B production
were not exercised because no frontier operation requires them (all fixture
conditionals are HELD/INADMISSIBLE; the joint-conditional proof uses a direct
response-leaf predicate, not discovery). This is honest scoping, not a hold.

## 1. Owner entry points exercised (all real, all in-tree)

| Owner function | Module blob (HEAD) | Use |
|---|---|---|
| `ingest_c11_source_release` (+ `C11SourceReleaseCandidate`, `SourceReleaseManifest`, `build_candidate_replay_manifest`) | `pre553_c11_ingest.py` `37cd35fa2e3420a3eea272a2902e96ab9ba38aba` | 3 synthetic releases ingested into 1 shared append-only `C11Repository` |
| `C11Repository`, `C11LogicalRelease` (`_make_validated_release` path via ingest) | `pre553_c11_repository.py` `67c6eb6494522cd11aab1b93d0e73f9cef6036f3` | Sealed releases; exact-key resolution only |
| `execute_empirical_query` (+ `EmpiricalQuerySpec`, `make_empirical_predicate`) | `pre553_empirical_query.py` `03facecf70890bfd13b80418620d274cbcd69d02` | 3 marginal + 5 MR-indicator + joint-proof + mechanism queries |
| `AuthorityRegistry` | `pre553_empirical_authority.py` `ca65a7fd4d52f0c44447434559b1d09412e7aa39` | Source + query authorities per execution |
| `BatchExecutionRunner.run` (+ `BatchManifest`, `BatchUnitSpec`, `ExecutionOutcome`, `ExecutorBinding`) | `pre553_batch_runner.py` `2d291600b9a10c56d9c6f6de7f7d619f6c52e829` | Deterministic scheduling, provenance-closed COMPLETED receipts |
| `ExactRef`, `AuthoritySnapshot`, `EmpiricalUniverse`, `RespondentIdentity`, `RespondentEvent`, `QuestionVariableBinding`, `RoutingEligibilityFact`, `EmpiricalCoordinateFact`, `TypedAbsence` | `pre553_empirical_objects.py` `a61365b994e5c3c50de0f598fcf40e90abf757b6` / `pre553_c11_integrity.py` `7c59aa13a2b7c8e3ab0dc90a1400df645b0b4bbd` | Native record construction |

Note: `pre553_c11_integrity.py` blob `7c59aa13a2b7c8e3ab0df645b896959b7b1e9b7b1e9` is the live-tree value at repair time (WG0P pinned only runner/objects/c11_repository; all three pins match HEAD exactly).

## 2. Actual commands and exits

```
$ cd /Users/matthewsmith/Desktop/Rawlsing/WORKER_RETURNS/PYAT-USERDIRECT-20261014-R5-WG0P2-WORKLOAD-PRODUCTIVE-REPAIR-R1/repro
$ PYTHONPATH=/Users/matthewsmith/Desktop/Rawlsing:$PWD python3 -m pytest test_wg0p2_repair.py -q -p no:cacheprovider --junitxml=pytest_wg0p2.xml
29 passed in 3.14s   (exit 0)
```

Host: Python 3.11.3, pytest 9.1.1, git 2.39.1, macOS darwin. JUnit: `repro/pytest_wg0p2.xml`. No network, no model calls, no survey microdata (all rows are synthetic fixture cohorts declared in `COHORTS`).

## 3. Real computed results (record → empirical value → batch receipt → consumer)

Releases ingested (one shared `C11Repository`, 3 validated releases):
- `REL-REL-A-W1`: 10 respondents (R1–R6 + H1–H4), 7 questions, risk sets R_ORD/R_RT/R_HH/R_JOINT_ORD_RT
- `REL-REL-A-W2`: 4 respondents, 1 question, risk set R_ORD2
- `REL-REL-B-W2`: 3 respondents, 1 question, risk set R_ORDB (withdrawn; rows present, never queried)

Batch run: 3 units, 3 COMPLETED receipts, `FULL_MANIFEST_COVERAGE`, manifest `8d7c1ce960899799`. The accepted owner's own summary reports `populated_data_execution_claim=False` (synthetic rows are not a populated-data claim; recorded, not overridden).

Consumer effects (from actually computed facts only):

- `OP-WG0P-ORD-01-MARGINAL` — denominator 6; cells `0:1, 1:2, 2:2, 3:1` OBSERVED_POSITIVE, `9:0` OBSERVED_ZERO_IN_SUPPORTED_RISK_SET.
- `OP-WG0P-ORD-05-MARGINAL` — denominator 4; cells `0:0, 1:2, 2:1, 3:1, 9:0`.
- `OP-WG0P-HH-MR-02-MARGINAL` — denominator 4; joint profile cells (5-indicator tuples): the 4 observed household profiles each n=1 (OBSERVED_POSITIVE), 28 empty profiles OBSERVED_ZERO; derived per-option totals food:2, rent:2, health:2, education:1, none:1 (deterministic aggregation of the same computed fact, labeled derived).
- Joint-conditional proof (mechanism, separate source scope): `Q-RT-C GIVEN Q-ORD-A==1` over joint risk set R_JOINT_ORD_RT → SUPPORTED, cells `yes:1, no:1`, denominator 2 (R2/R3 are exactly the `1`-respondents).
- Missing-evidence mechanism: empty risk set → owner returns typed `ZERO_SUPPORT`, denominator 0 (a real typed fact, never a fabricated number).
- Weak small-n mechanism: 3-respondent cohort → exact counts `0:2, 1:1, 2:0, 3:0, 9:0`, denominator 3 (no smoothing, no minimum-n invention).

Changed input (R1 `0`→`3`) changes 01's cells; 02 and 05 cell values byte-identical. Revocation (grant→execute→withdraw) supersedes 04's receipt (retained, not deleted) and leaves W1 values identical. Resume (`max_units=1` then full) reproduces the full-run receipt set exactly; schedule order deterministic across builds.

## 4. Exact holds (no computation claimed)

- HELD marginals/conditionals (16 ops): no I03 execution, no batch unit, retained in `frontier_receipts` with typed reasons.
- INADMISSIBLE conditionals (10 ops): never joined across wave/source/unit; retained with cross reasons.
- I05 discovery / Route B production: not exercised (no frontier operation requires them); functionality exists in-tree, deliberately unused — not a blocker.
