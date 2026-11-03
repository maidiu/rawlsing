# PDEV01 GAP-007 repair — actual C11/I03/I05/Batch binding

**BRANCH:** `agent/pyat-pdev01-gap007-sourcefree-r1`  
**STARTUP:** `649a48e13283b003167c4462bbdc6f6250e97e7c`  
**STATUS:** `CANDIDATE__TEST_ONLY__ACTUAL_SYNTHETIC_C11_I03_I05_BATCH_BINDING__INDEPENDENT_REVIEW_REQUIRED`  
**WRITE ROOT:** `WORKER_RETURNS/PDEV01-GAP007/repair/`

## Result

The demonstrated release gap is repaired at the sourcefree receiver edge without production edits.

- Actual synthetic source: 12 rows, 71 columns, source SHA `5009f3c9272dcbfb15a48b17cfff51f9afa67e60d6a2c1364c9aa07bc6732e4f`.
- Actual C11 release ref: `383716e4c9d233df69ef8cd508f7ffa5053d7a7355e7135a170eb1c2b337d9c1` (`R56-SYNTHETIC-RELEASE`).
- Exact P1 plan operation identity preserved: 840 operations; original plan ref `e0d4180cbfc43a1ddc5965ff20afb9cb284676c6c4981d9681d3e35121ac59ea`.
- 210 P1 DISTRIBUTION units bound one-to-one to 210 current I03 queries/predicates and 210 Batch units.
- Actual Batch execution: 210/210 COMPLETED; 210 result refs; 210 `SUPPORTED` synthetic facts.
- 630 unsupported P1 operations (CONDITIONAL/JOINT/HETEROGENEITY/RECURSIVE_BRANCH) retain original operation refs and typed refusal `P1_OPERATION_KIND_HAS_NO_EXACT_CURRENT_I03_BINDING`.
- Actual I05 call: 16 receipts, 30 facts, 16 candidates, complete declared frontier.
- Wrong release refusal: `BatchIntegrityError: exact C11 release unavailable...`.
- Wrong authority/query refusal: `CarrierExecutionBindingError: query_ref exact preimage unavailable...`.

All 840 P1 operations are accounted: 210 executed-bound DIST + 630 typed unsupported; no dropped/invented operations.

## Deliverables

- `replay_repair.py` — executable binding/replay.
- `test_repair.py` — 7 focused tests, all passed, including two fresh-process identity comparisons.
- `01_ACTUAL_RECEIPT.json` — exact trace/output.
- `02_CALLS_AND_ACCOUNTING.md` — receiver calls and accounting.
- `03_LIMITS_AND_REPAIR.md` — limits and smallest repair.
- `actual_trace.stderr`, `test_repair.log`, `test_repair_junit.xml`.

No original data, source rights, new science, production edit, compiler replacement, CI, merge or downstream wake. Distinct independent review required.
