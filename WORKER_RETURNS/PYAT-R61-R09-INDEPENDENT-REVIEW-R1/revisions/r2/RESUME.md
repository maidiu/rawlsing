# R61-R09V R2 resume

State: **REVISE** banked; central independent-capture promise **HOLD**. Reviewer
branch `agent/opencode-pyat-r61-r09v-r2-independent-review-r1`. Candidate
`4a10c82a...` / code `77f8b4205...` was not repaired or adopted.

## Cold restart

From the reviewer worktree:

```
/usr/local/bin/python3 -m pytest -q -p no:cacheprovider tests/universal_runner \
  --junitxml=WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/revisions/r2/evidence/reviewer_author_suite_junit.xml

/usr/local/bin/python3 WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/revisions/r2/probes/independent_probes_r2.py \
  > WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/revisions/r2/evidence/probes_r2.json

/usr/local/bin/python3 WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/revisions/r2/probes/mutant_check.py \
  > WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/revisions/r2/evidence/mutant_check.json
```

The probe command exits 1 when the three required-refusal cases are accepted or
crash; that is the defect signal, not an infrastructure failure. Fixtures are
disposable under `probes/work/` and are removed by the probe script.

## What to preserve

- Candidate verifier/test bytes unchanged; SHA256 `3cf9f5e7...03b8d` and
  `2b00fd2f...54de9`; `git diff --exit-code` = 0.
- The actual C11 positive is real and matches an independent plain-process
  reference; keep it.
- The controls that pass: bare mapping/issuer refusal, out-of-tree refusal,
  mandatory durable ledger, cold and concurrent replay refusal, C11 wrong
  expectation refusal, targeted mutant/restoration.
- The decisive failures are `P1_child_json_dump_forges_result` (D1-R2) and
  `P2_child_forges_loaded_bytes_and_result` (D4-R2), plus
  `P10_non_serializable_expectation` (D7-R2). The first two cannot be repaired
  by another local canary patch; they require the parent-owned observation
  channel described in `00_RETURN.md`/`defects.md`.

## Boundary

Local TEST_ONLY review only. No protected CI, deployment, administrative,
original-source, scientific, N11/N12, workflow/config or production claim.
All35/1890/global and Z UNRESOLVED 16 remain unchanged. Final non-force push is
to the assigned reviewer branch only.
