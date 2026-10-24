# R91-R04V R2 joined independent native qualification return — REVISE

**Verdict: `REVISE` for R04_JOINED R2.** R2 fixes the actual governed-result
capture, external original pin, original manifest retention and real partial
multi-unit cold restart; the reviewer independently proved the partial
multi-unit fresh-process resume the author had only shown in-process. One
remaining output-identity gap prevents ACCEPT: completed native outputs are
rehydrated as mutable facts-only `SimpleNamespace` views, not actual native
owner output objects or checked immutable views carrying the original output
identities.

## Exact identity and separation

- R04V R2 commission: `6482c4f7435ef5c7d93b0a68804b821481505d9f`.
- Prior full commission/oracle: `4d78c019d7c34c1ca2448e04f6a5e94248f35ba0`
  and `50b8bee9e59d4c13fffeda319e257b37b5593356`.
- Author R2 commission: `10044de629b5add38c751f2aa21ad6cefc64e808`.
- Exact candidate/startup: `dfeaab23998291be81abe4caecd08de663053eaa`.
- Author contract: `7b84cf20df2fc2bfea3b00e57f42047df55cb5e0`.
- Author code: `c0c4b9e15a84546ca200d8da85bd3979832e7b1e`.
- Reviewer branch: `agent/opencode-pyat-r91-r04v-r2-joined-review-r1`.
- Mandatory root gate passed exactly at the stable worktree, branch and HEAD,
  with only untracked pycache.
- Reviewer EXPECTATIONS were frozen and committed (`d400edf93`) before further
  native test work.
- Reviewer is the existing distinct R04V reviewer, not author/HQ; same
  account/provider is disclosed and is not institutional or OS isolation.

## Independent replay

| Suite | Result | Evidence |
|---|---|---|
| Author R2 focused suite | 5 passed, 0 failed/error/skip | `replay/author_suite_junit.xml`, `.log` |
| Retained R03 suite | 16 passed, 0 failed/error/skip | `replay/r03_suite_junit.xml`, `.log` |
| Reviewer successor probes | 3 passed, 1 failed required behaviour | `replay/hostile_probes_junit.xml`, `.log` |

Reviewer passes:

- actual R03 governed `NativeDiscoveryExecution` capture/restore with exact
  facts and original manifest;
- external original pin rejects a self-rehashed forged checkpoint;
- real partial multi-unit prefix -> fresh process -> pending units, matching
  uninterrupted output refs/facts/states (independently proving the partial
  cold requirement the author had only shown in-process).

Remaining failure:

- completed resume reconstructs `native_outputs` as mutable
  `SimpleNamespace(facts=...)`; the original `QueryExecutionResult.query_ref`
  and native output identity are lost, and a same consumer expecting the owner
  output contract fails. Discovery views are likewise a facts-only
  `SimpleNamespace(native_result=...)` rather than an actual/checked owner view.

## Exact minimal missing function

Reconstruct actual native owner output objects (`QueryExecutionResult` and the
actual discovery result) or a frozen checked view carrying all identity-bearing
output fields (query/evaluated-frontier/replay/fact identities and
associations), and validate it before releasing completed cached facts. A
mutable facts-only namespace is insufficient.

## Retained positive evidence

- Actual governed capture/restore, original external pin, original manifest,
  real partial multi-unit resume, completed-unit non-rerun and pending-unit
  Batch execution pass.
- Author focused 5/5; retained R03 16/16.
- U43 exact; R03/native owner bodies and R04.byte decoder unchanged; two
  authorized code paths only.
- No R05/original science/CI/prod/N11/N12/Sorok/J52/W52 claim.

## Limits and NOT_REACHED

Sourcefree TEST_ONLY trusted-host only; no source respondent access. Both pin
and candidate replaced by a different trusted host remains the R61AV excluded
boundary. No new global durable exactly-once/anti-fork, cryptographic issuer,
R09 or R05 requirement. R05/original science/CI/prod/N11/N12/Sorok/J52/W52
remain NOT_REACHED. No candidate repair or unauthorized native-owner edit.

## Artifacts and remote verification

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/` JUnit/logs, `evidence/`, `proof_witness.json`,
`manifest.json`, `RESUME.md`. The reviewer branch is pushed non-force; direct
remote readback of the evidence commit and final tip is recorded in
`evidence/remote_readback.txt` and reported to the coordinator. The candidate
branch remains at `dfeaab23998291be81abe4caecd08de663053eaa`.
