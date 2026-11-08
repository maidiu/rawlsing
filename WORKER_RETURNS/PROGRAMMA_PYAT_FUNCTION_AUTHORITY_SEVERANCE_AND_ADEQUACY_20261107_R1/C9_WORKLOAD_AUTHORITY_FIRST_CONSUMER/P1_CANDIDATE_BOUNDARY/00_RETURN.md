# C9/P1 — candidate plan to current Batch first-consumer boundary (C9R reconciled)

**Lane:** issue #777, same existing local OpenCode DeepSeek V4.1 Flash MAX author.
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer`
**Branch:** `agent/pyat777-source-consumer-20261107-r1`
**Starting HEAD:** `d540cfcc44359f8f78aceccf8afb247c4a7ad80d`
**Prior author base:** `396bfee9cca0275d040597828848ede4a7da80a7`
**Sublease:** `C9_WORKLOAD_AUTHORITY_FIRST_CONSUMER/P1_CANDIDATE_BOUNDARY/`
**Correction provenance:** independent review `05a750ad6bcab8124c1f5d86b8867181fa4ee92c`, `C9_P1_EXISTING_SUCCESSOR_INDEPENDENT_REVIEW/REVIEW.json` (C9R-01/C9R-02).
**Preserved historical C9:** the pre-C9R d540 text and negative records remain below as historical scope evidence; the current reconciliation is in this section and `04_BOUNDARY_LEDGER.jsonl`.

## C9R-01/C9R-02 RECONCILIATION (CURRENT)

The d540 empty-`C11Repository` refusal is an **expected negative for the as-built 840 ATLAS candidate manifest**. It is not evidence that the current C11/I03/Batch successor is missing or that the four-operation DTA witness is the only sourcefree first consumer.

The existing current successor is **PDEV01-GAP007 at `d3d6e48791623478fd1d838c7e95a72b77b5cd74`**, reused here from its exact code and receipt without rerun:

- source: 12 rows / 71 columns, synthetic SHA `5009f3c9272dcbfb15a48b17cfff51f9afa67e60d6a2c1364c9aa07bc6732e4f`
- C11 release: `R56-SYNTHETIC-RELEASE`, hash `64cf774b408686394c8caf9969f442b518e365d04c924bafefb6204239c9bf03`
- P1 plan/operation identity: 840 operations, plan `e0d4180cbfc43a1ddc5965ff20afb9cb284676c6c4981d9681d3e35121ac59ea`
- **210 DISTRIBUTION operations bound one-to-one to 210 current I03 queries/predicates and 210 Batch units**
- **210/210 Batch COMPLETED; 210 SUPPORTED synthetic facts**
- **630 non-DIST operations typed `P1_OPERATION_KIND_HAS_NO_EXACT_CURRENT_I03_BINDING`** (`CONDITIONAL 210`, `JOINT 210`, `HETEROGENEITY 105`, `RECURSIVE_BRANCH 105`)
- Batch manifest `6fd0f47cde582407a6afb6f21d3fb5c7d001cc14b03f688f34cce87770eef8ab`
- I05: 16 receipts, 30 facts, 16 candidates, `COMPLETE_FOR_EXACT_DECLARED_FRONTIER`
- exact receipt SHA-256 `bba0de8231ea50b46c1f5d5f73c434d64af2d9bcd9c5ef610876e7955b1256ab`

The PDEV01 path is **test-only/sourcefree** and remains a candidate requiring independent review; it is not production, original35, native or scientific acceptance. It is the existing current Batch/I03/Batch evidence for the 210 DIST subset, so the previous “BatchExecutionRunner completion / I03 execution NOT_RUN” statement is now scoped **only to the as-built 840 candidate manifest**. On that manifest, `BatchExecutionRunner(manifest=plan.batch_manifest, repository=C11Repository())` still refuses at synthetic release `urn:test:programma:c11logicalrelease:release25`; this is expected and not a missing-engine finding.

| Distinction | Status |
|---|---|
| Prior capital: PDEV01 210 DIST current C11/I03/Batch | Existing path reused; 210/210 COMPLETED, 210 SUPPORTED, 630 typed refusals, I05 16/30/16; test-only/sourcefree; no rerun |
| As-built 840 ATLAS candidate manifest | Current `BatchManifest` accepted 840; direct empty-repo runner refused at synthetic release; expected historical negative, not missing engine |
| Actual shared35 selected input | No explicit selected source/wave; first unresolved field `selected_shared35_source_id/wave -> P1 WaveIdentity/EligibleItem`; `NOT_RUN__UNPROVED_SELECTION` |
| Native/original/science effect | `NOT_RUN`; selected metadata identity would not authorize execution |

**C9R-01 disposition:** implemented by scoping the empty-repository negative to the as-built 840 manifest and citing the existing PDEV01 210-DIST path. **C9R-02 disposition:** implemented by reusing the exact PDEV01 210-DIST current C11/I03/Batch receipt, retaining 630 typed refusals, and recording the exact absent shared35 selection field with checked pins.

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

For the **as-built 840 candidate manifest only**, the next direct consumer is `BatchExecutionRunner` (`pre553_batch_runner.py:385`). The minimum legal invocation:

```python
BatchExecutionRunner(manifest=plan.batch_manifest, repository=C11Repository())
```

fails at the first exact synthetic release, before any executor or I03 call:

```text
BatchIntegrityError: exact C11 release unavailable;
no latest/default/fuzzy/nearest fallback
```

This is the expected negative for this manifest; it does **not** prove a missing C11/I03/Batch engine. The existing 210-DIST PDEV01 path is the current successor evidence above.

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

For the **as-built candidate manifest**, there is also no legitimate direct entry into the current I03 receiver. `execute_issued_workload` (`pre553_issued_workload.py:280`) takes `NativeWorkload`, not `BatchManifest`; it builds its own units from `workload.requests` using `r.query_ref` and maps them through:

```text
requests_by_query[unit.job_ref.key]
```

The candidate `job_ref` kind is `PROGRAMMA_PYAT_EPRE_OPERATION`; no current `NativeWorkload.requests`/`I03ExecutionRequest` entry maps it. This is the interface boundary of the as-built candidate, not a missing current C11/I03/Batch engine and not a vague “need issuer.” PDEV01 already demonstrates the existing exact 210-DIST binding for the supported subset.

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

**Proved at prior-capital/current-path scope:** PDEV01-GAP007's existing sourcefree path for **210 of the 840 P1 DISTRIBUTION operations**: 210 exact current I03 query/predicate links, 210 Batch units, 210/210 COMPLETED, 210 SUPPORTED synthetic facts, plus I05 16 receipts/30 facts/16 candidates and 630 typed non-DIST refusals. This is test-only/sourcefree candidate evidence, not production/original35/native/science acceptance.

**Proved at candidate-plan scope:** the exact P1 candidate construction and current `BatchManifest` admission at declared **35-wave candidate-plan** identity: 35 waves, 70 items, 840 operations/units, deterministic no-drop, `TEST_ONLY_SOURCEFREE`, no source bytes, no empirical effect. The 840 ATLAS operations are candidate-plan identity, not actual original35.

**Not proved:** actual selected shared35 source/wave identity, actual shared35 occupancy, a selected shared35 C11 release→I03 query/predicate link, any actual original35 execution, native/scientific/actor effect, or whole35 results. The first unresolved selection field is `selected_shared35_source_id/wave -> P1 WaveIdentity.atlas_id/dataset_id + EligibleItem.item_ref/source_variable_code`; status `NOT_RUN__UNPROVED_SELECTION`. The prior all35 ledger `C9_WORKLOAD_AUTHORITY_FIRST_CONSUMER/05_DECLARED_ESTATE_SCOPE.tsv` is preserved unchanged; its 24 `NOT_RUN` + 11 `FIXTURE_ONLY` source statuses remain the estate truth. R157's 35 declared `C11LogicalRelease` refs are fixture/native-construction metadata, not a selected current input and not execution authority.

## OWNER / ACTION

- **Existing current successor (PDEV01-GAP007):** reuse the exact 210 DIST current C11/I03/Batch path and receipt; do not rebuild it, add an `EpreOperation`→I03 resolver, or rerun it for this bounded return.
- **630 non-DIST operations:** route to the existing operation-kind semantic owners recorded in `04_BOUNDARY_LEDGER.jsonl` / `03_MINIMUM_OWNER_ACTION.tsv`; preserve the original operation refs and typed-refusal reason. Do not infer 630 missing capabilities or expand the engine.
- **Actual selected shared35 input:** if an actual declared source/wave is selected, its owner must name the exact `selected_shared35_source_id/wave` and bind the existing C11 release + I03 query/predicate at the current owner. If none, keep `NOT_RUN__UNPROVED_SELECTION`; metadata identity alone is not execution authority.
- **Source/science current issuer:** no action unless a selected original request is actually attempted; then supply its exact competent decision record. No original target-use gate is required for the sourcefree witness.
- **P1/R157 owner:** keep the candidate as nonissuing sourcefree construction; do not treat the 35 ATLAS waves as actual original35.
- **No-build route:** `NO_BUILD__REUSE_CURRENT_PDEV01_210_DIST_AND_CURRENT_OWNERS`; any true implementation deficiency must be independently qualified before a production code grant.

## BOUNDARIES

No original respondent/SAV/DTA/DB read, source copy/upload, native/S3/science/actor effect, production/runtime/existing-test/HQ/peer/protected write, replacement engine, new universal `NativeSourcePackage`, legacy cache restore, full suite, new worker, or polling. `T01 #770`, `Q86 #774`, `GF1 #691`, `R9 #767`, C1–C8, and prior C9 are untouched. Quota `UNKNOWN`; whole #777 remains false.

## EVIDENCE

- `01_TRACE.jsonl` — 6 historical d540 rows plus 6 C9R reconciliation rows; exact refs/types/authority scope/producer/selector/consumer.
- `02_COMMANDS_AND_EVIDENCE.md` — source cuts, Git blob hashes, exact calls, positive/negative/restoration, `NOT_RUN` boundary, and C9R prior-capital evidence.
- `03_MINIMUM_OWNER_ACTION.tsv` — 4 historical d540 rows marked `HISTORICAL_D540` plus 5 current C9R owner/ABI/dependency rows.
- `04_BOUNDARY_LEDGER.jsonl` — machine-readable prior-capital/current-selection/consumer ledger with all 35 declared shared35 source/release metadata rows and first unresolved field.
