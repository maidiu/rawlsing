# R61-R03V R4 independent native qualification return — REVISE

**Verdict: `REVISE` for the R4 fixed-original-pin successor.** The fixed-pin
cold restore works: genuine restore passes, missing/wrong pin refuses, and the
three prior coordinated fact/job cold probes refuse against the genuine original
pin. The remaining gap is the live checkpoint capture interface, which trusts
anti-join flags/refs instead of running the shared structural/closure/
multiplicity validation, so an incomplete/forged result can acquire a checkpoint.

## Exact identity and separation

- Commission: `3e7d0df8a9c3d6dd37949b1e9abc490afcef739a`.
- R61AV decision: `7a36e8091eda463c736f4ca0528d47f061b26cce`.
- Exact candidate/startup: `8c506f8f239204b004e4b677572898c8dba06811`.
- Author contract: `496bacae2deee56f8c827157a63ea7a7416e9a21`.
- Author code: `61ce7975d822688edd9525a10ad7fa9048f69455`.
- Prior R3 review: `7d8396329ed8ac2df86c82bb46e785a0dc487cde`.
- Reviewer branch: `agent/opencode-pyat-r61-r03v-r4-independent-review-r1`.
- Mandatory first-tool preflight passed exactly at the stable worktree, branch
  and HEAD, with only untracked pycache.
- Reviewer EXPECTATIONS were frozen and committed (`483335fe6`) before R4
  candidate code inspection.
- Reviewer is the existing distinct R03V reviewer, not author/HQ; same
  account/provider is disclosed and is not institutional or OS isolation.

## Independent replay

| Suite | Result | Evidence |
|---|---|---|
| Author R4 suite | 15 passed, 0 failed/error/skip | `replay/author_suite_junit.xml`, `.log` |
| Retained R01 suite | 32 passed, 0 failed/error/skip | `replay/r01_suite_junit.xml`, `.log` |
| Reviewer fixed-pin probes | 3 passed, 2 failed required behaviours | `replay/hostile_probes_junit.xml`, `.log` |

Fixed-pin positives:

- Genuine original-pin restore passes; missing pin and wrong pin refuse.
- Re-running the prior single-fact deletion, fact duplication and expected
  query/predicate job substitution with recomputed internal hashes against the
  genuine original pin: all refuse; genuine restore passes between faults.
- Content mutation retaining advertised refs refuses against the original pin.

Remaining failures (capture boundary):

1. A result whose `operation_ledger` is empty while anti-join flags remain true
   still returns a checkpoint from `freeze_restore_checkpoint()`.
2. A result with duplicated `fact_refs` still returns a checkpoint; no
   multiplicity/fact-catalogue validation at capture.

## Exact minimal missing function

At `GovernedFrontierResult.freeze_restore_checkpoint()`, run the same shared
structural/closure/expected-mapping/multiplicity validation used by the cold
path (or an equivalent pin-free helper) on `self.ledger()` before returning the
checkpoint. Refuse on incomplete operation rows, missing expected candidates/
jobs, missing native receipt/fact closure, duplicate native fact identities or
invalid fact multiplicity.

## Retained positive evidence

- Author R4 15 passed; retained R01 32 passed.
- Real governed joint/conditional/D3/root-parent/minority/pending/source-value
  and HELD/UNKNOWN positives remain.
- Fresh-process genuine restore and no native rerun/budget charge are covered by
  the author suite and the reviewer's fixed-pin positive.
- U43 blob `31e84f49d624f5524906e9e7839d2873106f8249` exact; four-path scope;
  U43/binding/R01/R02/native owners unchanged.

## Limits and NOT_REACHED

Sourcefree TEST_ONLY trusted-host only; no source respondent access. Both pin
and candidate replaced by a different trusted host is the R61AF excluded
boundary. R04 joined custody/durability, R05 lifecycle/grades, F5-F8 global,
original35/1890 N11, N12/Sorok, protected CI/production and J52/W52 remain
NOT_REACHED. No candidate repair, self-adoption, new worker, cryptographic
issuer or production merge.

## Artifacts and remote verification

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/` JUnit/logs, `evidence/`, `proof_witness.json`,
`manifest.json`, `RESUME.md`. The reviewer branch is pushed non-force; direct
remote readback of the evidence commit and final tip is recorded in
`evidence/remote_readback.txt` and reported to the coordinator. The candidate
branch remains at `8c506f8f239204b004e4b677572898c8dba06811`.
