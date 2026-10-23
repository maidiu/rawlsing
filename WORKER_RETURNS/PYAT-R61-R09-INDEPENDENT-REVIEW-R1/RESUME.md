# R61-R09V resume

State: **REVISE** banked. Reviewer branch
`agent/opencode-pyat-r61-r09v-independent-review-r1`. Candidate
`c8dbdd017b216e01dc43e0e15d4e044f3ec6d6e8` was not repaired or adopted.

## Cold restart

From the reviewer worktree:

```
/usr/local/bin/python3 -m pytest -q -p no:cacheprovider tests/universal_runner \
  --junitxml=WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/evidence/reviewer_author_suite_junit.xml

/usr/local/bin/python3 -m pytest -q -p no:cacheprovider tests/universal_execution_oracle \
  --junitxml=WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/evidence/reviewer_existing_oracle_junit.xml

/usr/local/bin/python3 WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/probes/independent_probes.py \
  --out WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/evidence/probes_candidate.json
```

The probe command exits 1 when the seven hostile required-refusal cases are
accepted; that is the defect signal, not an infrastructure failure. It writes
`evidence/probes_candidate.json`. Regenerate the JUnit with the snippet described
in `defects.md`/commit history or keep the banked
`evidence/reviewer_probes_junit.xml`.

Mutant replay (disposable copy only):

```
/usr/local/bin/python3 WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/probes/independent_probes.py \
  --mutant WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/mutants/universal_runner_verify_mutant_disable_result_check.py
```

Expected mutant outcome: wrong-result run becomes `LOCAL_NATIVE_VERIFIED`; the
intact candidate refuses it (`RESULT_MISMATCH`).

## What to preserve

- Candidate code/test files are byte-identical:
  `60f1c359...571a6c` and `a08cff30...d24f88`.
- This returnroot is report-only. `probes/work/` is disposable scratch and may
  be deleted; the mutant copy is a disposable verifier copy, not candidate code.
- Do not weaken the candidate to make probes pass. If a future repair is
  authorized, the exact required amendments are in `defects.md`: parent-owned
  observation capture, authenticated supervisor/issuer, commit-tree-to-executed-
  byte binding, load-time byte digest, mandatory durable atomic nonce ledger,
  and typed malformed-input refusal.

## Boundary

Local TEST_ONLY review only. No protected CI, deployment, administrative,
original-source, scientific, N11/N12, workflow/config or production claim.
All35/1890/global and Z UNRESOLVED 16 remain unchanged. Final non-force push is
to the assigned reviewer branch only.
