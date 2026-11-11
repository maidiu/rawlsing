# W34-REPRODUCIBLE-RETURN

**Status:** `INCOMPLETE_PENDING_INDEPENDENT_RECEIVING` — no final 12-ID or protected acceptance.

**Execution/implementation cut:** `1c428d59dc53cb76a19c1502a74cfd3bba00a899`
**Evidence:** `lanes/mcr/REQUIRED_EVIDENCE_R1/logs/proof_12_full_junit.xml` (55 selected tests) and `proof_12_ci_and_contract.json`.

## Source and test blobs

- `rawlsing_next/_pre553_c11_execution_view.py` = `0f86148f504c06bc694dd980ae1da8913db929b6`.
- `rawlsing_next/_pre553_w03_cold_compact.py` = `06eefd8fe8c1839854a783c78045b170627806f2`.
- `rawlsing_next/_pre553_w04_cache.py` = `4bb7e933f0a5c3f34366ee9e9013b3714a3e4341`.
- `rawlsing_next/pre553_source_backed_c11_facade.py` = `c5f78e1f7385b188eda18ace063557c26a19fd40`.
- `rawlsing_next/pre553_parquet_carrier.py` = `2c09deeb9b85051cb9d4c36fc12b0a193095e085`.
- `rawlsing_next/pre553_carrier_execution.py` = `ee9b3af02bfca9238eb72ea45d94073d47769a07`.
- `rawlsing_next/tests/test_pre553_c11_execution_view.py` = `7e8bc4e92daecffa72b1fbc740a77b8ef1a6569b`.
- `rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py` = `90d498ef2b1c6e3543e984aa479512cd10afca10`.
- `rawlsing_next/tests/test_pre553_w03_w04_completion.py` = `7cd62ffc36091f6e36847f1498d1dc428ebda157`.
- `rawlsing_next/tests/test_pre553_carrier_execution.py` = `bc0db646a803b5bf80dab44d8acb01861d8b3371`.
- `rawlsing_next/tests/test_pre553_i03_grouping.py` = `78683c4098f388eb72d686651b3282b9162e2ed2`.
- `rawlsing_next/tests/test_pre553_source_backed_c11_facade.py` = `daf9368a0c3ff277da0b46c4f27e4686c1de8b12`.
- Workflow blob: `.github/workflows/pyat-w03-w04-physical-economy.yml` = `698e6ae6b5860d6d433546a1b7f56e0286a6c3cd`.

## Executed checks

```text
PYTHONPATH=. python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_c11_execution_view.py \
  rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py \
  rawlsing_next/tests/test_pre553_i03_grouping.py \
  rawlsing_next/tests/test_bench_w03_w04_physical.py \
  rawlsing_next/tests/test_pre553_w03_w04_cold.py \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py \
  CROSS_HQ_CONTROL_ROOM/test_verify_copy_paste_commission_r1.py \
  --junitxml=WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/mcr/REQUIRED_EVIDENCE_R1/logs/selected_99_junit.xml
```

Result: **99 passed in 41.63s**. `lanes/mcr/REQUIRED_EVIDENCE_R1/logs/proof_12_full_junit.xml` is the 55-test six-file subset filtered from that same canonical run.

```text
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py changed \
  --root . --base 46b7325637e68f78ccc7487d4b1abc7009c5ac0b \
  --head 1c428d59dc53cb76a19c1502a74cfd3bba00a899
```

Result: `MECHANICAL_PROOF_GATE_PASS_NOT_SCIENTIFIC_ADOPTION`; 2 witness contracts ran; each baseline PASS and mutation RED (`TARGET_ASSERTION_FAILED`).

```text
python3 CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py --self-test
python3 CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py \
  WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md
```

Result: `PASS_SELF_TEST` with 32 negative mutations rejected; wrapper `PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH` with 12 obligations.

## Independent references

- `reviews/api-binding-recheck/00_REVIEW.md`: `ACCEPT_AT_CCF5_R01_SCOPE` for the verifier API binding only; not whole MCR.
- `reviews/combined-code/00_REVIEW.md`, `reviews/cold-order-recheck/00_REVIEW.md`, `reviews/persistence/00_REVIEW.md`, and `reviews/economic-method-recheck/00_REVIEW.md` as bounded prior reviews; none is final 12-ID/economic receiving.
- Latest author return: `lanes/mcr/API_BINDING_R2/00_RETURN.md`; latest economic protocol return: `lanes/bench/PROTOCOL_R4/00_RETURN.md`.

## Missing / unresolved

- No `delivered_ids.txt`, SHA-bound external `MCR_COMPLETION_EVIDENCE` block, or final validator `--verify-return` is created; these must be emitted after the final package and actual receiving.
- No independent same-SHA code/economic receiver or protected receiving exists.
- `proof_02_cold_rss.json`, `proof_03_cost_comparison.json`, and `proof_10_resource_matrix.json` are absent; their obligations remain INCOMPLETE/NOT_RUN.
- GitHub Actions CI was not run in this lane; only local sourcefree execution is recorded.

## Limits

This is author artifact preparation only. It is not a 12-ID PASS, not an economic acceptance, and not a protected merge or source/native/science/actor authorization.

## Current GitHub execution update

Repaired-source run42986463148 at exactba39a5ab45fc1e4f27dbfa08e2caac47fc4e45ac passed100tests with0failure/error/skip and256-row sourcefree smoke. Actualcompressedartifacts/hashmanifest andJUnit are retained in hq/CI_RUN_42986463148/. This supersedes the earlier lane's NOT_RUN statement for GitHubActions only; local99tests remain historical at1c428d59d. Proof-gate CI step was skipped for workflow_dispatch and is not claimed executed; earlier independent/localtwo-witness proof remains separatelybounded. This obligation andwholegoal remainINCOMPLETE pending100kpairedmeasurements/fullsameSHAreceiving/externalMCRblock.
