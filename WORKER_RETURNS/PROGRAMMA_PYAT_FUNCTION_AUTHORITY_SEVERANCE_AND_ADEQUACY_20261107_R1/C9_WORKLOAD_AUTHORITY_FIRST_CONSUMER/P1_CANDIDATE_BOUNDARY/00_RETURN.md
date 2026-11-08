# C9/P1 — candidate plan to current Batch first-consumer boundary

**Lane:** issue #777, same existing local OpenCode DeepSeek V4.1 Flash MAX author.
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer`
**Branch:** `agent/pyat777-source-consumer-20261107-r1`
**Base:** `396bfee9cca0275d040597828848ede4a7da80a7`
**Sublease:** `C9_WORKLOAD_AUTHORITY_FIRST_CONSUMER/P1_CANDIDATE_BOUNDARY/`
**Preserved historical C9:** `C9_WORKLOAD_AUTHORITY_FIRST_CONSUMER/00_RETURN.md` and its logs/artifacts are untouched.

## FINDING

HQ's mechanical resolution of C9-D04 is confirmed. The exact candidate commit and blob were fetched and read:

- candidate cut: `d1278613e9e1a5d986ccce15782a697f19cbd722`
- exact module: `rawlsing_next/programma_pyat_original35_constructor.py`
- Git blob **SHA-1** `c8352c5ab0fbc1a817c38d8ef99d64beef628230`
- exact candidate test blob **SHA-1** `1f96aca99543acf9ec496f31f2c43969220f74bf`
- staged under this lease without modification; `git hash-object` still returns `c8352c...`.

The candidate is a real sourcefree constructor, not a missing function. Running its exact test fixture through the exact candidate produced:

| Property | Observed |
|---|---:|
| declared roster | 35 candidate waves (`ATLAS-00`…`ATLAS-34`) |
| items | 70 expected / 70 processed |
| operations | 840 |
| `BatchUnitSpec` units | 840 |
| HOLD / ABSTAIN | 0 / 0 |
| `no_drop_ok` | True |
| `source_qualification` | `TEST_ONLY_SOURCEFREE` |
| `all35_populated_claim` | False |
| `sourced_results_claim` | False |
| `plan_ref` | `e0d4180cbfc43a1ddc5965ff20afb9cb284676c6c4981d9681d3e35121ac59ea` |
| `roster_ref` | `6f611d3a96c90cb4c109a98012f183928e91a57ce6703b74116c27c577aabc88` |
| `BatchManifest` ref | `urn:rawlsing:pre553:batch-manifest:sha256:d9164f33d81ea2ec30681af98364e06983967a3a1f784f40d30ab2639553dca5` |

This is **candidate-plan identity**, not actual original35 estate occupancy. The exact candidate test input is synthetic `TEST_ONLY_SOURCEFREE`; it is not a real source roster or an original wave.

## CURRENT CONSUMER RESULT

The current `BatchManifest` owner accepts all 840 exact `BatchUnitSpec` units. That is the real first consumer at admission grain.

The next actual current consumer is `BatchExecutionRunner` (`pre553_batch_runner.py:385`). The minimum legal invocation:

```python
BatchExecutionRunner(manifest=plan.batch_manifest, repository=C11Repository())
```

fails at the first exact release, before any executor or I03 call:

```text
BatchIntegrityError: exact C11 release unavailable;
no latest/default/fuzzy/nearest fallback
```

The first unresolved key is:

```text
kind: C11LogicalRelease
object_id: urn:test:programma:c11logicalrelease:release25
content_hash: 3b0a04a5fb536f38cac2a27d4f55c97a5426fb8d065bb2bc11ee4b4564f96fc7
```

The first unit and job are:

```text
unit_ref: urn:rawlsing:pre553:batch-unit:sha256:0020b4f098ead397eadfd940fcda9ed1e3df5f15b6b0de295df29ad083bc0d1a
job_ref kind: PROGRAMMA_PYAT_EPRE_OPERATION
job_ref: urn:programma:pyat:programma_pyat_epre_operation:70bc8124cd93e0c6f68e13b7ee977ebd36fcae9aafe8d986bbff646cadf4fe5f
```

There is also no legitimate candidate-manifest entry into the current I03 receiver. `execute_issued_workload` (`pre553_issued_workload.py:280`) takes `NativeWorkload`, not `BatchManifest`; it builds its own units from `workload.requests` using `r.query_ref` and maps them through:

```text
requests_by_query[unit.job_ref.key]
```

The candidate `job_ref` kind is `PROGRAMMA_PYAT_EPRE_OPERATION`; no current `NativeWorkload.requests`/`I03ExecutionRequest` entry maps it. This is the exact first unresolved boundary, not a vague “need issuer.”

## NEGATIVE / RESTORATION

Using the exact candidate fixture:

- wrong source SHA on wave 0 → **816 units**, **24 ABSTAIN**, reason `SOURCE_SHA_MISMATCH`
- restored source SHA → **840 units**, restored `plan_ref` equals baseline exactly
- wrong and restored plan refs differ (`81c821…` vs `e0d418…`)
- no-drop behavior remains explicit

This is construction/no-drop evidence only; it does not execute a source or claim a scientific fact.

## AUTHORITY CORRECTIONS

- **C9-D02 `BLOCKED_ISSUER` is not proved.** No actual selected original request was attempted. This sublease records `NOT_RUN / UNPROVED_SELECTION`; it does not manufacture a blocker or demand an issuer.
- **Query scope `TEST_ONLY_SOURCEFREE` is legitimate without a selected original `TARGET_USE_PERMISSION`.** The candidate fixture carries an exact test-only `TargetUsePermission` ref (`urn:test:programma:targetusepermission:g25`); do not add a missing-original-target-use gate for the sourcefree operation.
- Native/current original/science permission remains separate and was not minted.
- Historical metadata is not a per-query mandatory packet. No AR-0005/0006 relation or AR-0047–50 question-use packet was used because the selected candidate operation does not demand one.

## SHARED SCOPE ACTUALLY PROVED

**Proved:** the exact P1 candidate construction and current `BatchManifest` admission at declared **35-wave candidate-plan** identity: 35 waves, 70 items, 840 operations/units, deterministic no-drop, `TEST_ONLY_SOURCEFREE`, no source bytes, no empirical effect.

**Not proved:** actual original35 source/wave identity, actual shared35 occupancy, actual C11 release identity, any candidate `EpreOperation`→I03 request mapping, `BatchExecutionRunner` completion, native/scientific execution, or whole35 results. The prior all35 ledger `C9_WORKLOAD_AUTHORITY_FIRST_CONSUMER/05_DECLARED_ESTATE_SCOPE.tsv` is preserved unchanged; its 24 `NOT_RUN` + 11 `FIXTURE_ONLY` source statuses remain the estate truth.

## OWNER / ACTION

- **P1 candidate / current Batch-C11-I03 owners:** if an actual selected shared35 operation exists, reuse the existing Batch/C11/I03 owner with an exact real C11 release and existing I03 request/query ref. Do not add an EpreOperation→query resolver in C9.
- **Source/science current issuer:** no action unless a selected original request is actually attempted; then supply its exact competent decision record.
- **P1/R157 owner:** keep the candidate as nonissuing sourcefree construction; select an actual original35 roster/wave separately before any whole35 claim.
- **No-build route:** `NO_BUILD__REUSE_CURRENT_BATCH_C11_I03_OWNERS`; any true implementation deficiency must be independently qualified before a production code grant.

## BOUNDARIES

No original respondent/SAV/DTA/DB read, source copy/upload, native/S3/science/actor effect, production/runtime/existing-test/HQ/peer/protected write, replacement engine, new universal `NativeSourcePackage`, legacy cache restore, full suite, new worker, or polling. `T01 #770`, `Q86 #774`, `GF1 #691`, `R9 #767`, C1–C8, and prior C9 are untouched. Quota `UNKNOWN`; whole #777 remains false.

## EVIDENCE

- `01_TRACE.jsonl` — exact plan/operation/unit/refs/types/authority scope/producer/selector/consumer.
- `02_COMMANDS_AND_EVIDENCE.md` — source cuts, Git blob hashes, exact calls, positive/negative/restoration, `NOT_RUN` boundary.
- `03_MINIMUM_OWNER_ACTION.tsv` — owner/ABI/dependency, authority correction, no-build/repair qualification route.
