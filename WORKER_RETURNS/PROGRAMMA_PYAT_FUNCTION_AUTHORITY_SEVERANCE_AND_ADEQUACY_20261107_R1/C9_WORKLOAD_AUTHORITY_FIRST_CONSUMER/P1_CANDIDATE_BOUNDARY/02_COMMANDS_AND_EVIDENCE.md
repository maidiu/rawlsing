# C9/P1 candidate boundary — commands and evidence (C9R reconciled)

## Source cuts and exact objects

| Item | Exact value |
|---|---|
| Starting HEAD | `d540cfcc44359f8f78aceccf8afb247c4a7ad80d` |
| Prior author base | `396bfee9cca0275d040597828848ede4a7da80a7` |
| Candidate commit | `d1278613e9e1a5d986ccce15782a697f19cbd722` |
| Candidate module | `rawlsing_next/programma_pyat_original35_constructor.py` |
| Candidate module Git blob SHA-1 | `c8352c5ab0fbc1a817c38d8ef99d64beef628230` |
| Candidate test | `rawlsing_next/tests/test_programma_pyat_original35_constructor.py` |
| Candidate test Git blob SHA-1 | `1f96aca99543acf9ec496f31f2c43969220f74bf` |
| Candidate module staged SHA-256 | `1b0c7d4f0220cbcb9385e89b9774ba4fa1d6f094ddcb14aabe51ea2bd4407f1b` |
| Candidate test staged SHA-256 | `5d87d3dc6d3371700ff0af23cbadf477febefd6dc0faf83b75c19ed287eeb1bd` |

The candidate module and test were staged only under this sublease. `git hash-object` of the staged module remains `c8352c5...`; no code was modified. The exact test module was used only for its sourcefree 35-wave input builder; the full candidate suite was not rerun.

## Exact commands

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer
git fetch origin d1278613e9e1a5d986ccce15782a697f19cbd722
git ls-tree d1278613e9e1a5d986ccce15782a697f19cbd722 \
  rawlsing_next/programma_pyat_original35_constructor.py
git show d1278613e9e1a5d986ccce15782a697f19cbd722:rawlsing_next/programma_pyat_original35_constructor.py \
  > .../P1_CANDIDATE_BOUNDARY/vendor/programma_pyat_original35_constructor.py
git show d1278613e9e1a5d986ccce15782a697f19cbd722:rawlsing_next/tests/test_programma_pyat_original35_constructor.py \
  > .../P1_CANDIDATE_BOUNDARY/vendor/test_programma_pyat_original35_constructor.py
```

Probe:

```sh
OUT=WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C9_WORKLOAD_AUTHORITY_FIRST_CONSUMER/P1_CANDIDATE_BOUNDARY
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR="$PWD/$OUT/tmp" PYTHONPATH="$PWD" \
python3 -B "$OUT/probes/p1_candidate_probe.py"
```

Exit `0`. Probe output: `probes/p1_candidate_probe.json`; log: `logs/p1_candidate_probe.log`.

```text
07afa8ffa0b62a07986a2339a4024690b5332abf9790122caa3c30b7267a8cc4  probes/p1_candidate_probe.py
f55a7778c3b07d7e43293dd89d00b8e68e81465510c7211f49a64b2b352b0add  probes/p1_candidate_probe.json
f55a7778c3b07d7e43293dd89d00b8e68e81465510c7211f49a64b2b352b0add  logs/p1_candidate_probe.log
```

## Positive candidate construction and current BatchManifest admission

Exact candidate fixture result:

```text
roster/declared waves: 35 (ATLAS-00..ATLAS-34)
expected/processed items: 70/70
operations: 840
BatchUnitSpec units: 840
HOLD/ABSTAIN: 0/0
no_drop_ok: true
source_qualification: TEST_ONLY_SOURCEFREE
all35_populated_claim: false
sourced_results_claim: false
plan_ref: e0d4180cbfc43a1ddc5965ff20afb9cb284676c6c4981d9681d3e35121ac59ea
roster_ref: 6f611d3a96c90cb4c109a98012f183928e91a57ce6703b74116c27c577aabc88
BatchManifest: urn:rawlsing:pre553:batch-manifest:sha256:d9164f33d81ea2ec30681af98364e06983967a3a1f784f40d30ab2639553dca5
BatchManifest units == plan batch_units: true
```

The current `BatchManifest` owner accepted all 840 exact units. This is sourcefree construction plus current manifest admission, not empirical execution.

## Actual current Batch execution attempt and exact first unresolved key

```python
BatchExecutionRunner(manifest=plan.batch_manifest, repository=C11Repository())
```

Exact result:

```text
BatchIntegrityError: exact C11 release unavailable; no latest/default/fuzzy/nearest fallback
```

First unit, release and job:

```text
unit_ref: urn:rawlsing:pre553:batch-unit:sha256:0020b4f098ead397eadfd940fcda9ed1e3df5f15b6b0de295df29ad083bc0d1a
first release: urn:test:programma:c11logicalrelease:release25
release hash: 3b0a04a5fb536f38cac2a27d4f55c97a5426fb8d065bb2bc11ee4b4564f96fc7
job_ref kind: PROGRAMMA_PYAT_EPRE_OPERATION
job_ref: urn:programma:pyat:programma_pyat_epre_operation:70bc8124cd93e0c6f68e13b7ee977ebd36fcae9aafe8d986bbff646cadf4fe5f
```

The failure occurs in `C11Repository.resolve_release_exact` invoked at `BatchExecutionRunner.__init__` (`pre553_batch_runner.py:411-418`), before any executor or I03 call. Candidate releases are exact synthetic test refs; they are not in a current C11 repository.

## Current I03 entry does not accept the candidate manifest

`pre553_issued_workload.execute_issued_workload` is the actual current C11/I03 receiving entry:

```text
signature: (workload: NativeWorkload, resolver: CurrentDecisionResolver, *, source_factory, host, purpose, ...)
takes BatchManifest: false
```

It builds its own units from `workload.requests`:

```text
BatchUnitSpec("QUERY", r.query_ref, (release.release_ref,), (r.predicate_ref, workload.decision_ref))
...
requests_by_query = {r.query_ref.key: r for r in workload.requests}
...
requests_by_query[unit.job_ref.key]
```

The candidate unit `job_ref` is a `PROGRAMMA_PYAT_EPRE_OPERATION`, not a `query_ref` from a `NativeWorkload.requests` entry. No existing function maps candidate `EpreOperation` refs into `I03ExecutionRequest`/`NativeWorkload`. That is the second exact boundary; no resolver was invented.

## Negative / restoration

Using the exact candidate fixture and wrong source SHA on wave 0:

```text
wrong batch units: 816
wrong abstentions: 24
wrong reasons: ["SOURCE_SHA_MISMATCH"]
wrong plan_ref: 81c821dc8c75c77f9896b95fec87e0ad08d35a87364dddb968c295057e065cfb
restored batch units: 840
restored plan_ref: e0d4180cbfc43a1ddc5965ff20afb9cb284676c6c4981d9681d3e35121ac59ea
restored_matches_baseline: true
```

## Source hashes of current code used

```text
5071bde0180db05f59386884d5de2bdea503cd26db2024806a92887d2a5a1e04  rawlsing_next/pre553_batch_runner.py
05f948dea28508312c3843ae40c1d76dddcfbe8c164695958cc2306bba851fac  rawlsing_next/pre553_issued_workload.py
77ec0997b8aab0bb00c7d0ca93997fb3f3a041ace1c6661c1efb1185c9affad2  rawlsing_next/pre553_c11_repository.py
9cd1d71440a7e8c1861dda73274529e07211edc14335583e93ad91c0833e9ab4  rawlsing_next/pre553_empirical_objects.py
d5f429408451d60d43f5ed2238bb1bf0762c9c966e02bce208157d3b5ee20121  rawlsing_next/pre553_universal_workload.py
```

Generated boundary artifacts (C9R):

```text
e08ccf42eb89846c92f30ff7a101bd481d70f995c3f9c1466bb4a91233190317  01_TRACE.jsonl
ee347e8cb559f9ee01e83e52dde6a7abbb7955ea42508d9bdda468518b6dfe76  03_MINIMUM_OWNER_ACTION.tsv
09964387b58fa94be6783fc6a789a9f5445253eeb28f198d9d865dc57c8b5e49  04_BOUNDARY_LEDGER.jsonl
3b2f873e46d20b9d14eff215630ec33f57cbe43f0be16004af39fefe0ebc7c0a  logs/c9r_validation.log
```

Historical pre-C9R hashes remain in the commit `d540cfcc44359f8f78aceccf8afb247c4a7ad80d`; the prior negative records are retained as `HISTORICAL_D540` rows in `03_MINIMUM_OWNER_ACTION.tsv` and as the first six `C9P1-*` rows in `01_TRACE.jsonl`.

## C9R prior-capital reconciliation (no rerun)

Independent review target/correction: `05a750ad6bcab8124c1f5d86b8867181fa4ee92c`, C9R-01/C9R-02.

Read-only commands used (no PDEV01 replay, no tests):

```sh
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq \
  show d3d6e48791623478fd1d838c7e95a72b77b5cd74:WORKER_RETURNS/PDEV01-GAP007/repair/replay_repair.py
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq \
  show d3d6e48791623478fd1d838c7e95a72b77b5cd74:WORKER_RETURNS/PDEV01-GAP007/repair/01_ACTUAL_RECEIPT.json
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq \
  show d3d6e48791623478fd1d838c7e95a72b77b5cd74:WORKER_RETURNS/PDEV01-GAP007/repair/04_RECEIPT_RECONCILIATION.json
git show d81bc2c67baf933461ae6cfca468f24779cc7e44:source_pre553_validation/integration/SOURCE_LIBRARY_INDEX.json
```

Existing successor `PDEV01-GAP007` at `d3d6e48791623478fd1d838c7e95a72b77b5cd74`:

```text
replay_repair.py Git blob SHA-1: b2bd2f115506fa1e4aa0d053f20e3677bea81f01
01_ACTUAL_RECEIPT.json SHA-256: bba0de8231ea50b46c1f5d5f73c434d64af2d9bcd9c5ef610876e7955b1256ab
04_RECEIPT_RECONCILIATION.json SHA-256: 4b5ac21902e99f29e202fde669b43078ddefe5de498a4ccca541c6dff6a3e528
synthetic source SHA-256: 5009f3c9272dcbfb15a48b17cfff51f9afa67e60d6a2c1364c9aa07bc6732e4f
C11 release: R56-SYNTHETIC-RELEASE / 64cf774b408686394c8caf9969f442b518e365d04c924bafefb6204239c9bf03
P1 plan: e0d4180cbfc43a1ddc5965ff20afb9cb284676c6c4981d9681d3e35121ac59ea
Batch manifest: 6fd0f47cde582407a6afb6f21d3fb5c7d001cc14b03f688f34cce87770eef8ab
```

Observed existing current path:

- 840 P1 operations accounted: 210 `BOUND_I03_QUERY` + 630 `TYPED_REFUSAL` (`CONDITIONAL 210`, `JOINT 210`, `HETEROGENEITY 105`, `RECURSIVE_BRANCH 105`).
- 210/210 Batch receipts `COMPLETED`; 210 SUPPORTED synthetic facts.
- 210 first-consumer links are exact current I03 query/predicate -> Batch units; predicate is stored at `replay_repair.py:123-127` and consumed at `:146-147`/`:165-166`.
- I05 `execute_governed_frontier`: 16 receipts, 30 facts, 16 candidates, `COMPLETE_FOR_EXACT_DECLARED_FRONTIER`.
- This is sourcefree/test-only candidate evidence, not production/original35/native/science acceptance. No rerun was performed; exact code/receipt reused.

PDEV01 is the existing current path for the **210 DIST subset**. It does **not** make the as-built 840 ATLAS candidate manifest directly executable, and it does not prove actual shared35 selection.

## Current shared35 selection trace (metadata only)

Checked declared artifacts:

- `C5_SOURCE_ESTATE_PRODUCER_CONSUMER/06_ALL35_SOURCE_DISPOSITIONS.tsv`: 35 source IDs; 24 `NOT_RUN` + 11 `FIXTURE_ONLY`.
- `source_pre553_validation/integration/SOURCE_LIBRARY_INDEX.json` at `d81bc2c67baf933461ae6cfca468f24779cc7e44`: 35 `C11LogicalRelease` fixture refs; no selected current P1 operation.
- `C9_WORKLOAD_AUTHORITY_FIRST_CONSUMER/05_DECLARED_ESTATE_SCOPE.tsv`: all 35 `NOT_RUN__NO_P1_SHARED35_WORKLOAD_INPUT`.
- P1 candidate/PDEV01: 35 `ATLAS-00..ATLAS-34` synthetic candidate waves and `Q00A...` synthetic items; not actual source IDs.

First unresolved field:

```text
selected_shared35_source_id/wave
  -> P1 WaveIdentity.atlas_id/dataset_id
  -> EligibleItem.item_ref/source_variable_code
  -> exact C11LogicalRelease
  -> exact EmpiricalQuerySpec/I03 query + predicate
  -> BatchUnitSpec
```

Status: `NOT_RUN__UNPROVED_SELECTION`. No selected current shared35 C11 release → I03 query/predicate → Batch link exists in these declared artifacts. This is not a global absence claim and not an invented issuer gate. R157 fixture release refs are metadata/native-construction evidence, not execution authority. A selected metadata identity would still stop before original source/native/scientific effects.

## 630 non-DIST operation-kind owners

| Kind | Count | Existing owner references | Exact P1 binding |
|---|---:|---|---|
| CONDITIONAL | 210 | `pre553_empirical_query.execute_empirical_query` condition predicate; `field_forge_conditional_support.produce_exact_conditional_support_profile` (GT2 scope, not generic P1) | not observed |
| JOINT | 210 | `_pre553_query_common._parse_target_plan` target/joint order; `pre553_empirical_query` multi-target; `field_forge_conditional_support` consumes joint fact (GT2) | not observed |
| HETEROGENEITY | 105 | `pre553_discovery_exact` stratum rules; `I03GroupedExecutionScope` grouped execution (not a P1 heterogeneity binding) | not observed |
| RECURSIVE_BRANCH | 105 | `pre553_recursive_handoff.RecursiveBranchHandoff` / `execute_exact_bounded_discovery_with_handoffs`; `pre553_universal_workload.compile_governed_frontier` / `execute_governed_frontier` | not observed |

These are existing semantic owners for routing, not a claim that 630 capabilities are missing. No engine was implemented or expanded.

## Authority corrections

- `C9-D02 BLOCKED_ISSUER` is superseded: no selected original request was attempted. Status is `NOT_RUN / UNPROVED_SELECTION`.
- The candidate's `TEST_ONLY_SOURCEFREE` `TargetUsePermission` ref is legitimate sourcefree provenance. No original target-use gate was invented.
- Native/current original/science permission is separate and was not minted.
- No AR-0005/0006 or AR-0047–50 packet was demanded or read.
- A selected-original metadata identity does not authorize execution; stop before original source/native/scientific effects.

## NOT_RUN / limits

- Actual original35 source/wave/roster selection: `NOT_RUN__UNPROVED_SELECTION`.
- Actual current shared35 C11 logical release matching a selected source/wave: `NOT_RUN` (R157 has 35 declared fixture refs only; none selected).
- Actual shared35 `selected_source_id/wave -> P1 WaveIdentity/EligibleItem -> I03 query/predicate -> Batch` link: `NOT_RUN`.
- As-built 840 candidate manifest direct `BatchExecutionRunner` completion: `NOT_RUN`; empty `C11Repository` refusal is expected and is not a missing-engine result.
- Existing PDEV01 210 DIST current I03/Batch path: **reused from exact code/receipt; no rerun**.
- Native/S3/science/actor effect and original execution: `NOT_RUN`.
- Full 35-wave runtime matrix and full candidate test suite: not run.
- Prior all35 ledger `../05_DECLARED_ESTATE_SCOPE.tsv` is preserved unchanged; its 24 `NOT_RUN` + 11 `FIXTURE_ONLY` source statuses remain estate truth.
- The 35-wave scope in this return is candidate-plan identity only; it is not actual shared35 occupancy and does not replace the prior ledger.
