# PYAT #997 — J2 R6 native execution return

**Disposition:** `R6_NATIVE_EXECUTION_COMPLETE__SEVEN_FILE_COURT_GREEN_89_OF_89__ORIGINAL_MANUAL_QUERY_SUBSTITUTION_REFUSED__FATE_RECEIPTS_GREEN_18_OF_18__INDEPENDENT_G5_PENDING`
**Scope:** execution evidence only. This return does **not** accept R6, certify G5, or close #997.
**Executor:** existing activated J2 worker, `opencode-go/deepseek-v4.1-flash#max`; 1017 checkpoint **UNVERIFIED** here. No replacement HQ, subagent, model/provider/account/effort/VM change, install, protected merge, or source/science-rights claim.

## 1 — Frozen cuts

| Item | Value |
|---|---|
| Branch | `agent/pyat997-r6-execute-20261115` |
| Documentary HEAD | `c368ff30189d8fdd5c1a8036a5b6e265d822f80b` |
| Code/test cut | `9ac034dd0734cdd000b4b73583f883dbcec2dfa6` |
| Independent rejection | `8b03c121a2f6d9c7a9c2e0513a03545780d14c3c` |
| Parent Browser R5 | `2c476e739a263dd0069b54706c6cfa63b07190c1` |

`git diff 9ac034dd0..HEAD` is only `WORKER_RETURNS/PYAT997_P1_ISSUER_BINDING_R6/00_HANDOFF.md`; the product/test tree is identical. Blob SHAs are in `evidence/blob_shas.txt` and `receipt.json`.

The worktree index was populated but its working tree was empty on arrival. I restored tracked blobs from its own HEAD with `git restore --source=HEAD --worktree .`; no product/test content was authored or changed. Writes were confined to this return directory.

## 2 — Qualified native runtime

```text
Darwin mainMac.lan 22.3.0 x86_64
Python 3.11.3 (/usr/local/bin/python3)
pyarrow 22.0.0
duckdb 1.5.2
pyreadstat 1.3.2
pytest 9.0.2
```

Existing runtime only; no install or VM configuration.

## 3 — Exact seven-file R6 handoff court

Command (the handoff says `python`; the qualified host exposes the same interpreter as `python3`):

```bash
python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py \
  rawlsing_next/tests/test_pyat997_s1e_saved_source_bridge.py \
  rawlsing_next/tests/test_pyat997_s1e_source_saved_body_bridge.py \
  rawlsing_next/tests/test_pyat960_s1e_source_i02.py \
  rawlsing_next/tests/test_pyat960_s1e_body_transport.py \
  rawlsing_next/tests/test_pre553_source_direct_parquet_estate.py \
  rawlsing_next/tests/test_pre553_direct_estate_i03.py
```

**Result:** exit `0`; **89 passed in 27.63s**; wall 28.43s; max RSS 160,337,920 B; peak footprint 127,037,440 B.
Evidence: `evidence/r6_seven_file_pytest.stdout.txt`, `.stderr.txt`, `.exit.txt`, collection list `evidence/r6_seven_file_collected.txt`.

This covers the full J2 court at R6: native source→13-family saved body→cold I03/I05 positives, missing/mixed/held/mutated/wrong-root/wrong-CURRENT negatives, SAV/DTA changed-fact and exact restore, direct q101 denominator-5, discovery/I05, and exact fate/receipt joins. No sibling #1029 test or execution evidence was transferred.

## 4 — Original 8b03 manual QUERY substitution witness

Ran the exact `witness_issuer_binding.py` from `8b03c121…` (SHA-256 `831fe169712926ff33e8f6795eff61b1535c67ac89e6a8b46125e2aaff4c0dff`) against the R6 product cut, using its own R3 harness extracted from `8b03…` into disposable scratch.

**Exit:** `1` — the witness's intended **RED** finding on the historical R3 substitution, not an R6 test failure.

```text
compiler_issued:        workload_requests=0, workload_discoveries=1, expected_jobs=[DISCOVERY]
manual_r3_issued:       workload_requests=1, workload_discoveries=1, expected_jobs=[DISCOVERY, QUERY]
same_compiler_record:   false
same_compiler_workload: false
joint_query_in_plan:    []
f4_like_operations:     12, all disposition=PROHIBITED (JOINT/CO_TRAVEL, SAMPLE)
red:                    true
```

So the original compiler still issues **0 QUERY / 1 DISCOVERY**; the q101/q102/q103 joint QUERY is not in the compiler plan and all 12 matching F4-like frontier operations are `PROHIBITED`.

Evidence: `evidence/original_8b03_manual_query_witness.json`, `.stderr.txt`, `.exit.txt`, witness copy and SHA.

## 5 — Exact R6 refusal of the invented QUERY with a matching resolver

```bash
python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py \
  -k 'original_r03_compiler_issuer_cannot_be_replaced or unaltered_compiler_discovery' -v
```

**Result:** exit `0`; **4 passed, 20 deselected in 3.22s**.

| Case | R6 result |
|---|---|
| `self_issued_query` + matching `TestOnlyDecisionResolver` | refused `R03_COMPILER_ISSUED_JOB_OR_PLAN_DRIFT` before any native receipt |
| `different_discovery_decision` | refused `R03_COMPILER_ORIGINAL_ISSUER_IDENTITY_DRIFT` |
| `self_reissued_u_root` | refused `R03_COMPILER_SOURCE_U_ENVELOPE_DRIFT` |
| unaltered compiler discovery | admissible without execution: 0 completed units, 0 positive links |

Evidence: `evidence/r6_exact_refusal_cases.stdout.txt`, `.stderr.txt`, `.exit.txt`.

## 6 — S1-C fate receipts

```bash
python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat_r3_s1c_source_operation_fates.py
```

**Result:** exit `0`; **18 passed in 88.80s**; wall 89.31s; max RSS 216,334,336 B.
Evidence: `evidence/r3_s1c_fate_receipts.stdout.txt`, `.stderr.txt`, `.exit.txt`.

## 7 — Limits and non-claims

- Controlled **TEST_ONLY_SOURCEFREE** execution only. No original35 source, science, or permission right is claimed.
- The separately held **#999 S2-A native body-truth tamper risk remains disclosed and unfixed**; this return makes no integrity-fix claim.
- R6 adds no F4 eligibility or governed QUERY issuance. Genuine governed QUERY issuance remains a **separate J3 obligation** and is not an R6 prerequisite.
- No `#1029` sibling execution/test transfer; no wholesale merge.
- No 100k/6 GiB, production CURRENT, protected merge, or #998 full-integration claim.
- No product/test modifications; no background jobs left behind.

## 8 — Custody

All files are under `WORKER_RETURNS/PYAT997_R6_EXECUTION_20261115/`. The same original independent reviewer `ses_e30a442d8ffeYBbXi7rPUpPxoc` is reserved to receive this after HQ terminal intake. HQ owns intake and the next reviewer action. **Stop finite pass.**
