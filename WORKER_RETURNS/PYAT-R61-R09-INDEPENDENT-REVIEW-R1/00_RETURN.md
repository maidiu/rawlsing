# R61-R09V — independent hostile review return

**Verdict: `REVISE` (scoped local).** The candidate's genuine-process positive
works, but the central R09V promise — independently observed actual
process/import/result/run custody rather than candidate-authored evidence —
does not hold. `DEPLOYMENT_HOLD` remains. This reviewer did not repair or adopt
the candidate.

## Exact identity

- Candidate/reviewer startup: `c8dbdd017b216e01dc43e0e15d4e044f3ec6d6e8`
  (tree `102c01243d801feb8587aefe8f8744f820e95d35`).
- Author code commit: `2cc6ce35112a9b98178556cd07ffd46f6ec815fb`
  (tree `4f7102cd42c710b3d2b6ed227eb267b08de15e52`).
- Sealed commission/startup: `3fd3cba5a42caa3853c5bd5b5a881feddf1a4ae2`;
  author flight startup `c84842e20e1d00d0b036977c9f5006aad5328ae9`.
- Author branch remote at review start:
  `agent/opencode-pyat-r61-r09-local-runner-r1` = `c8dbdd017...`.
- Reviewer branch: `agent/opencode-pyat-r61-r09v-independent-review-r1`; its
  remote was also `c8dbdd017...` before this return.
- Code blobs: `CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py`
  `04d06bfe4c0cc3150e6012b2b42d421b00c75551`; test
  `8c77529859fcd1f8f5ee690c768d4bc92e6acf46`.
- Code SHA256: `60f1c359...571a6c`; test `a08cff30...d24f88`; both unchanged
  after all probes (`git diff --exit-code` = 0).
- Tools: `/usr/local/bin/python3` 3.11.3, pytest 9.0.2, pyreadstat 1.3.2,
  git 2.43.0, Darwin 22.3.0.
- Model/session: `opencode-go/deepseek-v4.1-flash`, MAX/Global as commissioned;
  new reviewer session, not author `ses_e98c8b6c7ffeXtAnuGL58sAeCp`.
  Same provider account is role/session separation, not institutional
  scientific independence.

## What was verified

- Actual reviewer HEAD and both direct remote branch SHAs match the candidate
  startup. Changed paths from seal `c84842e20` are exactly the assigned
  allowlist plus the author's own returnroot; no workflow/config/consumer file
  was touched.
- Author `manifest.json` recomputed independently: 7/7 artifacts hash-match;
  explicit self-exclusion is present. Blob and commit/tree claims match.
- Reviewer replay of the author focused suite: **13 passed, 0 failed, 0
  errors, 0 skipped**, exit 0 (1.97 s). Existing oracle regression: **48
  passed, 0 failed, 0 errors, 0 skipped**, exit 0 (40.34 s). JUnit receipts are
  in `evidence/reviewer_author_suite_junit.xml` and
  `evidence/reviewer_existing_oracle_junit.xml`.
- Genuine fresh-subprocess positive (`probes/independent_probes.py` P0): a real
  child ran a synthetic fixture, returned the frozen `{label:baseline,
  value:42}`, emitted the expected `add`/`double` RETURNED events, imported
  `native_fixture` from the expected path/digest, and was accepted as
  `LOCAL_NATIVE_VERIFIED` with ceiling `LOCAL_NATIVE_TEST_ONLY` and
  `DEPLOYMENT_HOLD`.
- Targeted disposable mutant: in a copy under `mutants/`, disabling only the
  `RESULT_MISMATCH` comparison made a wrong-result run accept
  (`evidence/probe_mutant_result_check.json`); the intact candidate refused the
  same run with `RESULT_MISMATCH` (P7). Candidate source was not edited; its
  SHA256 and `git diff --exit-code` are unchanged.

## Ranked defects (full detail and contract refs in `defects.md`)

1. **D1 critical — the untrusted subject writes the observation.** An imported
   module can read the wrapper config, overwrite `observation_path` at
   `atexit`, and restore its own file. The genuine supervisor then accepted a
   run whose pre-forge result was 41 as the expected 42 (probe P8).
2. **D2 critical — `verify()` accepts an unauthenticated mapping.** A fabricated
   observation with no process at all is accepted; a fake issuer is accepted by
   rewriting the issuer string. The optional `candidate_evidence` guard is
   bypassed by omitting it (P1/P2). This directly contradicts the claim that
   candidate-authored evidence is refused by construction.
3. **D3 high — commit/tree are not bound to executed bytes.** Executed files
   outside the repository are accepted while labelled with the repository
   HEAD commit/tree; `target_file.sha256` is recorded but never checked
   (P3).
4. **D4 high — imported bytes are rehashed after child exit, not captured at
   load.** A module that mutates itself and restores the expected bytes at exit
   is accepted; the marker proves the mutated code ran (P4).
5. **D5 high — default CLI replay.** The same observation/expectation is
   accepted twice by two cold CLI processes when no optional nonce ledger is
   configured (P5).
6. **D6 medium — concurrent ledger race.** Two `NonceLedger` instances built
   before either consumes both accept the same nonce; no cross-process atomic
   check (P6).
7. **D7 low — malformed typed result raises `TypeError` instead of a typed
   refusal** (`evidence/malformed_result.json`).

## Real capability vs NOT_REACHED

Real, but only under a non-adversarial caller and well-behaved subject: the
candidate compares a genuine child's exit/result/events/import digests against
an externally formed expectation and refuses wrong commit/tree/policy/entrypoint,
nonce mismatch with a supplied ledger, missing events/imports, wrong result and
a same-name status mismatch. The author controls that do this are real and pass.

NOT_REACHED / not established: the promised independent custody over a hostile
candidate; authenticated supervisor/issuer identity; commit-tree-to-executed-
bytes binding; actual-loaded-byte custody; mandatory cold replay resistance;
safe concurrent replay refusal. No existing repository native owner or consumer
(C11/RouteB/I03/I05/Batch/E04) was executed; the positive fixture is synthetic.
Protected CI required-check enforcement, repository-admin attestation, OS
sandboxing, external key authority, original source/science and N11/N12 remain
held. Absence of protected CI is not used to redesign the deployment; this
return only judges the local promise.

## Trusted-runtime exclusions preserved

No protected CI/workflow, branch protection, admin attestation, external issuer
or key service, OS isolation, original survey data, credentials, external home
reads, provider/model switch, subagents or extra sessions. A candidate able to
rewrite the verifier, its imports, or Python itself defeats any purely local
check; that residual is excluded and is not claimed as prevented. The local
child is explicitly not a hostile-code sandbox, but the delivered supervisor
also fails the weaker promised boundary because the subject writes the result
artifact.

## Obligations and stopping conditions

All 35/1,890/global F6/F7/F8 obligations and Z UNRESOLVED 16 are unchanged; no
scientific/rights/N11/N12 or production claim is made. No material
architecture/science fork was encountered, so no Astra necessity card was
raised. The exact bounded verdict is established within the 60-minute budget
and banked before minute 45. Reviewer wrote only this returnroot; candidate
files are byte-identical. Final non-force push is to the assigned reviewer
branch only, with direct `ls-remote` verification reported in
`REMOTE_VERIFICATION.md` and the final response.

## Artifacts

`EXPECTATIONS.md` (frozen before candidate inspection), `defects.md`,
`probes/independent_probes.py`, `evidence/probes_candidate.json`,
`evidence/reviewer_probes_junit.xml`, `evidence/probe_mutant_result_check.json`,
`mutants/universal_runner_verify_mutant_disable_result_check.py`,
`evidence/identity.json`, `evidence/malformed_result.json`, test JUnit receipts,
`proof_witness.json`, `SHA256 manifest.json` (self-excluded), `RESUME.md`,
`REMOTE_VERIFICATION.md`.
