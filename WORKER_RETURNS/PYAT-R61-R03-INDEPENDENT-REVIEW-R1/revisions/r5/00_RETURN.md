# R61-R03V R5 independent native qualification return — ACCEPT_SCOPED_LOCAL

**Verdict: `ACCEPT_SCOPED_LOCAL`** for the R5 shared capture/restore validator.
The R4 capture defects are fixed: live checkpoint capture and cold restore use
the same structural/closure/expected-mapping/multiplicity validator; empty
operation ledgers and duplicate fact refs with true flags refuse capture, while
the genuine original pin still restores. Fixed-pin cold restore, prior cold
fault refusals and the retained native governed/D3/HELD/UNKNOWN positives all
pass. No blocking defect remains.

## Exact identity and separation

- Commission: `0f6acf2317ecd561e754af984da256c90c43be86`.
- Settled R61AV decision: `7a36e8091eda463c736f4ca0528d47f061b26cce`.
- Exact candidate/startup: `c912497b25411ebbd3d796db139f32f5bebb6c4c`.
- Author contract: `bae28794fa450bcf6ec500b47fa8886802a0aef2`.
- Author code: `5ba003e6ce0c42b690e7128fb6b7e08f409f5576`.
- Prior R4 review: `61356022db35254193605ae1cf749b1dff29794e`.
- Reviewer branch: `agent/opencode-pyat-r61-r03v-r5-independent-review-r1`.
- Mandatory first-tool preflight passed exactly at the stable worktree, branch
  and HEAD, with only untracked pycache.
- Reviewer EXPECTATIONS were frozen and committed (`15064375f`) before R5
  candidate code inspection.
- Reviewer is the existing distinct R03V reviewer, not author/HQ; same
  account/provider is disclosed and is not institutional or OS isolation.

## Independent replay

| Suite | Result | Evidence |
|---|---|---|
| Author R5 suite | 16 passed, 0 failed/error/skip | `replay/author_suite_junit.xml`, `.log` |
| Retained R01 suite | 32 passed, 0 failed/error/skip | `replay/r01_suite_junit.xml`, `.log` |
| Reviewer fixed-pin/capture probes | 5 passed, 0 failed | `replay/hostile_probes_junit.xml`, `.log` |

Reviewer probes confirm:

- genuine original-pin restore passes; missing and wrong pin refuse;
- the prior fact deletion, fact duplication and expected query/predicate job
  substitution all refuse against the genuine original pin, with genuine
  restore between faults;
- content mutation retaining advertised refs refuses;
- an empty operation ledger with true anti-join flags cannot acquire a capture
  checkpoint;
- duplicated `fact_refs` cannot acquire a capture checkpoint.

The author R5 suite covers the shared validator, genuine fresh-process restore,
no native rerun/budget charge, and the retained governed joint/conditional/D3/
minority/pending/source-value and HELD/UNKNOWN positives.

## Scope, limits and notes

- U43 blob `31e84f49d624f5524906e9e7839d2873106f8249` exact; four-path scope;
  U43/binding/R01/R02/native owner bodies unchanged.
- The R5 source contains a duplicated, immediately shadowed first definition of
  `restore_governed_frontier_ledger`; it is dead code with no behavioral effect
  and is recorded as a code-cleanliness note, not a functional gap.
- Sourcefree TEST_ONLY local trusted host only; no source respondent access.
  Both pin and candidate replaced by a different trusted host is the R61AF
  excluded boundary.
- R04 joined custody/durability, R05 lifecycle/grades, F5-F8 global,
  original35/1890 N11, N12/Sorok, protected CI/production and J52/W52 remain
  NOT_REACHED. No cryptographic issuer/durable custody is claimed.
- No candidate repair, self-adoption, new worker/provider, production merge or
  downstream R04/R05 wake.

## Artifacts and remote verification

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/` JUnit/logs, `evidence/`, `proof_witness.json`,
`manifest.json`, `RESUME.md`. The reviewer branch was pushed non-force. Evidence commit
`88abab210d92843bdc87d5884bf069580227d576` was directly read back at the
remote, as recorded in `evidence/remote_readback.txt`; the final branch tip is
also verified by direct remote readback and reported to the coordinator. The
candidate branch remained at `c912497b25411ebbd3d796db139f32f5bebb6c4c`.
