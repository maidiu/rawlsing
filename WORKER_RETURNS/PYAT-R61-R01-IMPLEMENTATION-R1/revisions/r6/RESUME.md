# R01 R6 resume

Branch: `agent/opencode-pyat-r61-r01-generic-grammar-r1`

Code commit: `3d60f9cb6f43830244fbd79699d1cf4041622d05`

Contract: `e2b87e6c33364e5361ed3c0b10ba5c13e34efbba`

Startup: `4b5fd7a240a6e2d007ba1df2424780e6b5612ea9`

## Reproduce

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_grammar.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r6/junit.xml \
  -o addopts=''
```

Expected: exit `0`, `28 passed`, no skips.

Key tests:

- `test_r6_retained_campaign_owner_d3_lineage_and_restore`
- `test_r6_campaign_snapshot_fresh_process_n1`
- `test_r5_receipt_lineage_generation_and_budget_refusals`
- `test_bounded_adaptive_recurrence_three_generations_actual_native`

## Boundary

- `RetainedRecurrenceCampaign` is the accepted owner path; legacy helpers are
  unqualified utilities.
- Local trusted-host authority only; no R09/protected issuer/global anti-fork.
- R03 remains NOT_STARTED; R04 custody/original science/other holds remain.
- Fresh distinct reviewer required; no self-adoption.
