# C9/P1 candidate boundary — commands and evidence

## Source cuts and exact objects

| Item | Exact value |
|---|---|
| Base | `396bfee9cca0275d040597828848ede4a7da80a7` |
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

Generated boundary artifacts:

```text
92ece56aabce9668050e4aa8082b87367d8caab819314aaf50d91df579977d6e  01_TRACE.jsonl
7fbf9c05e8ed865299fb947ec39632442d9200aee9da805dd36b6cba95b666ba  03_MINIMUM_OWNER_ACTION.tsv
06daf752ca440ead14a79a9945895f34638c89da895798e26b56541d73e932f2  logs/boundary_validation.log
```

## Authority corrections

- `C9-D02 BLOCKED_ISSUER` is superseded: no selected original request was attempted. Status is `NOT_RUN / UNPROVED_SELECTION`.
- The candidate's `TEST_ONLY_SOURCEFREE` `TargetUsePermission` ref is legitimate sourcefree provenance. No original target-use gate was invented.
- Native/current original/science permission is separate and was not minted.
- No AR-0005/0006 or AR-0047–50 packet was demanded or read.

## NOT_RUN / limits

- Actual original35 source/wave/roster selection: `NOT_RUN`.
- Actual current C11 logical release matching a candidate wave: `NOT_RUN`.
- Candidate `EpreOperation`→`I03ExecutionRequest`/`NativeWorkload.requests` mapping: `NOT_RUN` (no existing mapping observed).
- `BatchExecutionRunner` completion, I03/I05 execution, native/S3/science/actor effect: `NOT_RUN`.
- Full 35-wave runtime matrix and full candidate test suite: not run.
- Prior all35 ledger `../05_DECLARED_ESTATE_SCOPE.tsv` is preserved unchanged; its 24 `NOT_RUN` + 11 `FIXTURE_ONLY` source statuses remain estate truth.
- The 35-wave scope in this probe is candidate-plan identity only; it is not actual shared35 occupancy and does not replace the prior ledger.
