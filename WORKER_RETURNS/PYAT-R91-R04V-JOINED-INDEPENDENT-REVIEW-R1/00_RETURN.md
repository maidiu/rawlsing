# R91-R04V joined independent native qualification return — REVISE

**Verdict: `REVISE` for the R04_JOINED joined custody/restart candidate.** The
author's unary complete-workload sequence resumes without rerun at that narrow
grain, and the retained R03 suite passes. It is not a real joined partial
governed-native-frontier resume: actual R03 governed discovery results are not
consumable, the checkpoint is self-hashed without the R61AV external original
pin, and completed resume loses native outputs/facts and the original manifest.
R04_JOINED is not accepted; no self-adoption, production merge or R05 wake.

## Exact identity and separation

- R04V commission: `4d78c019d7c34c1ca2448e04f6a5e94248f35ba0`.
- User grant/R04 commission: `0f0f08373486a733b8946b82bfd576c17e506006`.
- Exact candidate/startup: `a88ccd140f30fe621140ee98841c6ce57ae9cab4`.
- Author contract: `b93b95adca3b803fc4f4c17acc712686e800377c`.
- Author code: `ef1e71628c0a89753c0c6aeea3c35c5fb06e29eb`.
- Accepted R03 base: `c912497b25411ebbd3d796db139f32f5bebb6c4c`; accepted R03
  review `d15de915ea3388894c0f8839d28db3b23bc00367`.
- Reviewer branch: `agent/opencode-pyat-r91-r04v-joined-independent-review-r1`.
- Mandatory root gate passed exactly at the stable worktree, branch and HEAD,
  with only untracked pycache.
- Reviewer EXPECTATIONS were frozen and committed (`1fd6dc642`) before further
  native test execution.
- Reviewer is the existing distinct R04V reviewer, not author/HQ; same
  account/provider is disclosed and is not institutional or OS isolation.

## Independent replay

| Suite | Result | Evidence |
|---|---|---|
| Author R04 focused suite | 3 passed, 0 failed/error/skip | `replay/author_suite_junit.xml`, `.log` |
| Retained R03 suite | 16 passed, 0 failed/error/skip | `replay/r03_suite_junit.xml`, `.log` |
| Reviewer joined custody probes | 0 passed, 3 failed required behaviours | `replay/hostile_probes_junit.xml`, `.log` |

The three failures are product gaps, not setup/import crashes:

1. Actual R03 governed-issued `NativeDiscoveryExecution` is rejected by
   `capture_joined_checkpoint` with `EXACT_NATIVE_WORKLOAD_RESULT_REQUIRED`;
   only unary `NativeWorkloadResult` is accepted.
2. A forged joined checkpoint with altered receipt/output refs and recomputed
   entry/checkpoint hashes is accepted; no separately provisioned original
   external pin is required.
3. Completed resume returns `native_outputs=()` and a synthetic manifest instead
   of the original native outputs/facts/manifest, so a same consumer cannot
   obtain the retained completed facts.

## Exact missing function / dependency

1. Extend the authorized `pre553_issued_workload.py` joining interface to
   consume the actual R03 governed-issued `NativeDiscoveryExecution` (its
   authority/grammar/frontier, manifest/unit, receipts, native result/outputs
   and facts), or return the exact additional R03 caller/adapter path and
   invocation dependency if it is truly indispensable. Do not claim automatic
   governed-discovery wiring without implementing it.
2. Require a separately provisioned original joined checkpoint pin (R61AV
   boundary): capture on the trusted live result, retain the pin outside the
   submitted checkpoint, and check it on cold restore/resume. A self-hashed
   candidate checkpoint must not authorize completed facts.
3. Retain/rehydrate actual completed native outputs/facts and the original
   manifest/unit identity, not only reconstructed Batch receipts/output refs.
4. Capture and resume a real partial multi-unit native prefix
   (`execute_issued_workload(max_units=...)`/Batch partial receipts) with
   completed units not rerun and pending units honestly pending; rejecting all
   non-COMPLETED receipts is not partial resume.

## Retained positive evidence

- Author R04 focused 3/3; retained R03 16/16.
- Unary complete-workload sequence: completed workloads are not rerun; revoked
  and wrong-source cases refuse; fresh-process checkpoint test passes at that
  narrow grain.
- U43 blob exact; R04.byte reused read-only; two authorized code paths; R03/
  native owner bodies unchanged.
- No R05/original science/CI/prod/N11/N12/Sorok/J52/W52 claim.

## Limits and NOT_REACHED

Sourcefree TEST_ONLY trusted-host only; no source respondent access. No new
global durable exactly-once/anti-fork, cryptographic issuer, R09, or R05
requirement is imposed. R04.byte historical custody is not re-litigated.
R05+/original science/CI/prod/N11/N12/Sorok/J52/W52 remain NOT_REACHED. No
candidate repair or unauthorized native-owner edit is performed.

## Artifacts and remote verification

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/` JUnit/logs, `evidence/`, `proof_witness.json`,
`manifest.json`, `RESUME.md`. The reviewer branch is pushed non-force; direct
remote readback of the evidence commit and final tip is recorded in
`evidence/remote_readback.txt` and reported to the coordinator. The candidate
branch remains at `a88ccd140f30fe621140ee98841c6ce57ae9cab4`.
