# R91-R04V R3 joined independent native qualification return — ACCEPT_SCOPED_LOCAL

**Verdict: `ACCEPT_SCOPED_LOCAL`.** R3 fixes the sole R2 restored-output-identity
defect. Completed unary outputs restore as actual native `QueryExecutionResult`
objects with equal `query_ref`, facts and release refs; completed governed
discovery restores as a frozen checked `RetainedDiscoveryResultView` with equal
evaluated-frontier, replay, fact/receipt and executed predicate/query identities.
The same consumers work, mutation of the checked discovery view raises
`FrozenInstanceError`, and all prior fixed-pin/partial-cold/manifest/no-rerun
positives remain.

## Exact identity and separation

- R04V R3 commission: `9bbc2b235a63882551580d364a4963324d36aeba`.
- Prior R04V R2 review: `239f492272bd72011f53570020a4b0cdc27dff27`.
- Author R3 commission: `fdd5ff5665e63fba62d635df74959bd487a767ab`.
- Exact candidate/startup: `e6f7b04c49772e07c20ad36f65b9b270a28a49cf`.
- Author contract: `cca9d5d50f6571fc6ca08135bc17f6b33d229833`.
- Author code: `6068ab9e53b652ab603b30f8db55738393daff9b`.
- Reviewer branch: `agent/opencode-pyat-r91-r04v-r3-joined-review-r1`.
- Mandatory root gate passed exactly at the stable worktree, branch and HEAD,
  with only untracked pycache.
- Reviewer EXPECTATIONS were frozen and committed (`7730acfad`) before further
  native test work.
- Reviewer is the existing distinct R04V reviewer, not author/HQ; same
  account/provider is disclosed and is not institutional or OS isolation.

## Independent replay

| Suite | Result | Evidence |
|---|---|---|
| Author R3 focused suite | 6 passed, 0 failed/error/skip | `replay/author_suite_junit.xml`, `.log` |
| Retained R03 suite | 16 passed, 0 failed/error/skip | `replay/r03_suite_junit.xml`, `.log` |
| Reviewer successor probes | 5 passed, 0 failed | `replay/hostile_probes_junit.xml`, `.log` |

Reviewer probes confirm:

- unary restored output is the actual `QueryExecutionResult` with equal
  `query_ref`, facts and release refs to uninterrupted execution;
- governed discovery restored output is the frozen
  `RetainedDiscoveryResultView` with equal evaluated-frontier/replay/fact/
  receipt/executed-predicate/query identities;
- discovery view mutation raises `FrozenInstanceError`;
- external original pin rejects a self-rehashed forged checkpoint; genuine
  restore passes;
- real partial multi-unit prefix -> fresh process -> pending units matches
  uninterrupted output refs/facts/states with no completed-unit rerun.

## Retained positive evidence

- Actual R03 governed capture/restore, original manifest retention, current
  grant/source checks, external original pin, real partial multi-unit cold
  resume, completed-unit no-rerun and pending native execution remain.
- U43 blob exact; native/R03 owner bodies and R04.byte decoder unchanged; two
  authorized code paths only.
- No R05/original science/CI/prod/N11/N12/Sorok/J52/W52 claim.

## Limits and notes

- Sourcefree TEST_ONLY local trusted host only; no source respondent access.
  Both pin and candidate replaced by a different trusted host remains the R61AV
  excluded boundary.
- The discovery completed result remains a `SimpleNamespace` container whose
  `native_result` is the frozen checked view; the output view itself is
  immutable/validated. This is a non-blocking container note.
- No new global durable exactly-once/anti-fork, cryptographic issuer, R09 or R05
  requirement. R05/original science/CI/prod/N11/N12/Sorok/J52/W52 remain
  NOT_REACHED. No candidate repair, self-adoption or production merge.

## Artifacts and remote verification

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/` JUnit/logs, `evidence/`, `proof_witness.json`,
`manifest.json`, `RESUME.md`. The reviewer branch was pushed non-force. Evidence commit
`4138504cb99b3c120e398fb2eb0370a20132b22d` was directly read back at the
remote, as recorded in `evidence/remote_readback.txt`; the final branch tip is
also verified by direct remote readback and reported to the coordinator. The
candidate branch remained at `e6f7b04c49772e07c20ad36f65b9b270a28a49cf`.
