# First consumer and tests

**PRE-MAIN:** `8e44ca9c751049d65e6def47600b5c073ee04b29`
**Status:** sourcefree only; no raw survey, native P07, actor, source, scientific or production authority.

## 1. Actual current consumers/importers

`test_receipts/lineage_probe.json` is the static import/call witness.

| Capability | Current path | Actual current consumer | Production consumer? |
|---|---|---|---|
| R61 grammar | `universal_grammar/*` | `pre553_native_workload_binding`, `pre553_universal_workload`, tests | NO |
| R61 workload | `pre553_universal_workload.py` | tests only | NO |
| R61 issued transport | `pre553_issued_workload.py` | `pre553_native_workload_binding` (itself test-only chain) | NO |
| Batch scheduling | `pre553_batch_runner.py` | issued/native binding/test chain | NO |
| Learned-world composition | `pre553_learned_world_composition.py` | tests only | NO |
| B5 lifecycle | `pre553_learned_product_lifecycle.py` | learned-world composition + tests | NO top-level production import |
| R61 evidence cache | ABSENT | none | NO |
| Production binding/source read admission | ABSENT | none | NO |
| S06 trusted replay wrapper | ABSENT | none | NO |
| HQ282 durable batch/P01 | ABSENT | branch-only P01 consumer; no current import | NO |

**Finding:** every six-lineage capability is either current test-only or absent
current. There is no named current production receiver for any of the six.

## 2. Fault matrix actually exercised

| Fault | Exact receiving assertion | Result |
|---|---|---|
| Wrong source edition / wrong source | `test_universal_workload.py::test_r03_wrong_source_edition_and_duplicate_job_refused`, `test_r03_source_value_fault_changes_dependent_fact_and_restores` | PASS in 16/16 current workload tests |
| Forged issuer record | `test_receipts/test_d3_faults.py::test_forged_issuer_record_is_refused_before_source_open` | 1/1 PASS: `CURRENT_AUTHENTICATED_ISSUER_RECORD_REQUIRED` |
| Duplicate replay / completed retry | `test_pre553_batch_runner.py::test_completed_receipt_cannot_be_retried_or_rewritten`; `test_r03_count_preserving_substitution_and_duplicate_fail_antijoin` | PASS in 107/107 batch/learned/prod/replay suite; 16/16 workload |
| Crash/restart durable batch | Current: no durable checkpoint store; `execute_issued_workload` rejects `prior_receipts` and requires external fact/receipt custody. Candidate B01D: real SIGKILL after durable side effect before COMMIT, 48/48 tests | Current GAP; candidate PASS |
| Partial checkpoint | `test_pre553_batch_runner.py::test_max_units_throttle_cannot_masquerade_as_full_coverage`; `test_universal_workload.py::test_r05_capture_rejects_empty_ledger_and_duplicate_fact_refs` | PASS in current suites |
| Release authenticity / exact authority | `test_pre553_replay_audit.py` exact historical authority, tamper and selector probes; `test_universal_workload.py::test_r04_fixed_original_checkpoint_genuine_and_hostile`; B5 `test_h22_checkpoint_restart_and_replay_identity_are_exact` | PASS in current suites |
| Missing actual consumer | `test_receipts/lineage_probe.py` | No production import; all six current capabilities test-only/absent |
| All35 construction | `test_receipts/lineage_probe.py` | `original35_roster`/`reconcile_estate_workloads` zero callers; `compile_universal_workload` one bundle and one test caller |

## 3. Exact test receipts

| Run | Scope | Result | Log |
|---|---|---|---|
| Current grammar | `test_universal_grammar.py` | 32 passed | `test_receipts/current_grammar.log` |
| Current workload | `test_universal_workload.py` | 16 passed | `test_receipts/current_workload.log` |
| Current batch/learned/prod/replay | four suites | 107 passed | `test_receipts/current_batch_learned_prod_replay.log` |
| Current B5 + forged issuer | lifecycle 39 + D3 fault 1 | 40 passed | `test_receipts/current_b5_and_faults.log` |
| Candidate B01D | durable checkpoint/recovery | 48 passed | `test_receipts/candidate_b01d_48.log` |
| Candidate P01 | V2 durable consumer integration | 25 passed | `test_receipts/candidate_p01_25.log` |
| Candidate S06 | trusted release replay wrapper | 26 passed | `test_receipts/candidate_s06_26.log` |
| Candidate A04/A04T | binder + v2 verifier | 82 passed, 2 skipped, 1 stale self-check failure | `test_receipts/candidate_a04_85.log` |
| Candidate R03 | universal workload R4 | 15 passed | `test_receipts/candidate_r03_15.log` |

The A04T single failure is
`test_accepted_owners_a04_a04s_a05_untouched`: its own new verifier files are
outside the test's old baseline `b68de0dd`, so the test's self-check is stale.
It is not counted as a candidate capability failure. Author/reviewer evidence
for A04S/A04T is preserved separately.

## 4. Missing first consumer

- HQ282/P01 has a **branch-only** Field Forge consumer and a sourcefree candidate
  test receipt. No current PRE-MAIN import or production receiver exists.
- R61 grammar/workload have test callers only.
- R61 evidence binding, production binding and S06 have no consumer at all.
- No current N9/N10W or original E04 consumer is proven for any lineage.

**REAL_RECEIVER_MISSING** applies to all six unless a separate owner names one.
This is not a request to invent an adapter; it is the first missing edge.
