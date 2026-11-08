# C9 test receipts — sourcefree workload → I03/Batch

## Identity

- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer`
- Branch: `agent/pyat777-source-consumer-20261107-r1`
- Base: `451f8d1e094800d523589cdd4db5159a338db836`
- Protected runtime source: `7a5429ffbc48efd25e28c912da80c822e66bc182`
- Host: `mainMac.lan`, Darwin 22.3.0 x86_64
- Python: `3.11.3`
- Runner: existing local OpenCode; actual model id `opencode-go/deepseek-v4.1-flash`; effort telemetry not separately exposed. Commission target remains DeepSeek V4.1 Flash MAX.
- Seed: `PYTHONHASHSEED=0`; `PYTHONDONTWRITEBYTECODE=1`; temp under the C9 output root.
- No full test suite, 35-source matrix replay, or original-source run was performed.

## Exact command and result

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer
OUT=WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C9_WORKLOAD_AUTHORITY_FIRST_CONSUMER
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR="$PWD/$OUT/tmp" PYTHONPATH="$PWD" \
python3 -B "$OUT/probes/workload_probe.py"
```

Exit `0`. The probe builds a lawful synthetic **nonrespondent DTA** fixture with the existing test package/materialize helper and executes the real non-test universal-workload API.

### Positive sourcefree witness

- `compile_universal_workload:143` → `build_test_only_workload:299` → `execute_universal_workload:229`
- 4 operations compiled / 4 executed
- **4 SUPPORTED RAW facts**: supports `3/3`, `3/3`, `4/4`, `2/2`
- 4 receipts; no-drop anti-join `4 expected / 4 executed`
- authority scope: `TEST_ONLY_SOURCEFREE`
- query authority: `B49-TEST-ONLY-QUERY-AUTH`
- query: `WHOLE_QUESTION_RISK_SET`, `RAW`, `UNCERTAINTY_UNQUANTIFIED`
- `target_use_permission_ids`: **empty**
- source SHA is the synthetic fixture SHA, not an original/shared35 source

### Negative/restoration controls

- wrong source SHA: **0/4 executed**, 4 failed, no-drop false
- wrong host/purpose: `WorkloadAdmissionError: SOURCE_HOST_PURPOSE_MISMATCH`
- restoration: fact refs exactly match the positive run; no-drop 4/4
- all controls use the same real C11/I03/Batch API, not a new engine

### Shared35/P1 boundary

`compile_governed_frontier:473` and an actual shared35 P1 input were **NOT_RUN**:

- it requires a caller-frozen `ScientificFrontier` + `NativePreimageBundle`, `SourceInventory`, `GrammarPolicy`;
- candidate P1 path `d1278613e9e1a5d986ccce15782a697f19cbd722` / blob `c8352c5ab0fbc1a817c38d8ef99d64beef628230` is absent in the inherited object store;
- no exact P1 EpreOperation → catalog/request/Batch binding was observed;
- this is a producer/selection seam, not a missing C11/I03/Batch function.

## Source hashes used

```text
d5f429408451d60d43f5ed2238bb1bf0762c9c966e02bce208157d3b5ee20121  rawlsing_next/pre553_universal_workload.py
05f948dea28508312c3843ae40c1d76dddcfbe8c164695958cc2306bba851fac  rawlsing_next/pre553_issued_workload.py
b330a58f5ac2646469d99f58518aceef44780fa4700f088652224fbd771fde4d  rawlsing_next/pre553_native_workload_binding.py
23b7d5cbcca4fe07a3334d133020c2850e14ab9ad0ab4c159df4a2e48dbef33f  rawlsing_next/pre553_carrier_execution.py
7cd7fd4f8ccf79cb07b037ef9cdda5e60ed3c3ba0631c9f4030d09f4d666be94  rawlsing_next/pre553_empirical_query.py
0c56a0f6f656547a096982a6adab21c9b47d749385411a5d159f2b5390eec8bf  rawlsing_next/pre553_c11_ingest.py
7788feb514ad5eceb71e7d76191b1b80a66688dc64a56b0dc05f4a1b19bbdfcf  rawlsing_next/pre553_source_backed_c11_facade.py
e99dd21140dab44ef377f143bd932413045cd97936f830467a7a06cd44b30b7c  rawlsing_next/pre553_source_native_preimage_adapter.py
```

Probe/output hashes:

```text
2b6e1a9117d800d1affd0ae8799b6c385b4f4bda75e4009f569bf8682f9fdbd1  probes/workload_probe.py
020c549cc6930ff22f7bd35826993e19426a790c57a97f656e2657b1d7f5ea63  probes/workload_probe.json
020c549cc6930ff22f7bd35826993e19426a790c57a97f656e2657b1d7f5ea63  logs/workload_probe.log
```

## Generated artifacts

```text
4b1e6a22f9a517c9897d091123b13a8ef8044fe65addc103243abaf489d59510  probes/build_c9.py
e05ed0876aaba76c9085784b654c4c10b2d3d72771ed2449d5d9247438e41400  01_CASES.jsonl
5a666bafad78ff5f929495371b436013f5208dd3b7fccc9781ee0904a3f15f69  02_PRODUCER_SELECTOR_CONSUMER_TRACE.tsv
169929037b665682ef59fe2a0f9d8588122c575d6281d91ce2cc4793a4cb9800  04_INDISPENSABLE_DEPENDENCIES.tsv
edc695260511a9331dbd2c14536edd49f5ce47d7f33fb3087b9dfbfc6521187b  05_DECLARED_ESTATE_SCOPE.tsv
514d992a3580ddaf7cb2a3c26958a7a9de2d0f3a909e3dc44d7685305debcc58  logs/build_c9.log
da9c89b7c215629bc5a1428cfb89d4eb5108bcd74751c366fdea0cad57dd931f  logs/reporting_validation.log
```

## NOT_RUN / limits

- No original respondent/SAV/DTA/DB read, no asset copy/upload, no original/source-native execution, no native/science/actor effect.
- No actual shared35 source/wave or P1 constructor/frontier was selected; `compile_governed_frontier` is `NOT_RUN`.
- The positive is a sourcefree test-only library witness, not a shared35 estate operation.
- No production/existing-test/HQ/peer/protected write; no new worker; no polling.
- Whole #777 remains incomplete; quota `UNKNOWN`.
