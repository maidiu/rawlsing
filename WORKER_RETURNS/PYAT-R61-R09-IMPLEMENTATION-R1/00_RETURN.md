# R09 — local authenticated native runner verifier

## Return status

- **Engineering candidate:** `LOCAL_CODE_COMPLETE`
- **Disposition:** `HOLD` for independent review and `DEPLOYMENT_HOLD` for production
- **Why not promote:** R09's protected required-check installation and repository-administrator attestation were not available to this code worker. Local verification does not install or prove deployed enforcement, and the existing R00 ceiling is unchanged.
- **Author validation only:** a fresh independent reviewer session is still required. The author has not appointed itself reviewer and has not adopted the candidate.

## Startup and scope verification

- Sealed startup: `c84842e20e1d00d0b036977c9f5006aad5328ae9`
- Branch: `agent/opencode-pyat-r61-r09-local-runner-r1`
- HEAD at launch verified equal to the sealed startup.
- Commission, `NODE.json`, `INPUTS/CONTRACTS.md`, `INPUTS/TESTS.md`, `INPUTS/OVERLAYS.md` and `INPUTS/USER_GRANT.json` were read in full.
- Write scope used: `CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py`, `tests/universal_runner/`, and this return directory.
- No workflow, CI administration, protected setting, key, credential, original data, configuration or unrelated branch was touched. `.r61` operational files remain untracked.

## Plain-English function delivered

`CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py` now provides a local verifier and native test harness with an explicit **externally supplied trusted supervisor boundary**.

A caller supplies:

1. a `TrustedExpectation` frozen outside the candidate, pinning issuer, candidate commit, candidate tree, policy SHA256, run ID, nonce, entrypoint SHA256, exact imported-module digests, exact native event sequence/statuses and expected result; and
2. an observation produced by a trustworthy supervisor.

`LocalNativeSupervisor` demonstrates that boundary locally. It launches a fresh Python interpreter, resolves the candidate tree with real `git rev-parse`, hashes the externally protected policy and entrypoint, traces actual calls in the pinned target module, records actual import audit events, re-hashes imported files **outside the child process**, and captures the returned result. The verifier compares that independently captured observation against the frozen expectation.

A candidate-authored receipt, boolean, trace, attestation, self-pin, same-name status label or candidate-selected policy is never evidence. Any such candidate evidence is refused by construction.

## Accepted capability delta

- A local, native, process-backed positive baseline can now be accepted as `LOCAL_NATIVE_VERIFIED` at ceiling `LOCAL_NATIVE_TEST_ONLY` while production remains `DEPLOYMENT_HOLD`.
- Forged candidate evidence, wrong commit/tree/policy/entrypoint, stale or replayed nonce, fake issuer, missing native event, missing import, changed runtime import, changed result and same-name status spoof are all refused with named reasons.
- This is a local verifier capability, not a deployed required check and not generic promotion authority.

## What was actually executed

Environment:

- OS: Darwin
- Python: `/usr/local/bin/python3` — Python `3.11.3`
- pytest: `9.0.2`
- pyreadstat: `1.3.2` verified but not used by this sourcefree runner work
- Git: `2.43.0`

Commands and exit codes:

| Command | Exit | Result |
|---|---:|---|
| `/usr/local/bin/python3 -m pytest -q -p no:cacheprovider tests/universal_runner --junitxml=WORKER_RETURNS/PYAT-R61-R09-IMPLEMENTATION-R1/junit.xml` | 0 | 13 passed, 0 failed, 0 errors, 0 skipped, 2.853 s |
| `/usr/local/bin/python3 -m pytest -q -p no:cacheprovider tests/universal_execution_oracle --junitxml=WORKER_RETURNS/PYAT-R61-R09-IMPLEMENTATION-R1/existing_oracle_junit.xml` | 0 | 48 passed, 0 failed, 0 errors, 0 skipped, 34.182 s |
| `/usr/local/bin/python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py lint tests/universal_runner/test_universal_runner_verify.py` | 0 | `AST_LINT_PASS` |
| `/usr/local/bin/python3 -m py_compile CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py tests/universal_runner/test_universal_runner_verify.py` | 0 | compile passed |

Focused native tests use real subprocesses and real import/result capture. They do not use mocked native booleans as acceptance evidence.

## Focused positive and hostile coverage

| Control | Test node | Required observation |
|---|---|---|
| Known baseline positive | `test_trusted_baseline_is_accepted_locally_but_not_promoted` | Actual process returns `{"label":"baseline","value":42}`, exact events/imports accepted, production still held |
| Forged candidate receipt/self-pin | `test_candidate_authored_receipt_cannot_replace_supervisor_evidence` | `CANDIDATE_AUTHORED_EVIDENCE` |
| Wrong commit | parametrized `test_wrong_commit_tree_policy_or_entrypoint_is_refused` | `CANDIDATE_COMMIT_MISMATCH` |
| Wrong tree | same parametrized test | `CANDIDATE_TREE_MISMATCH` |
| Wrong policy | same parametrized test | `POLICY_MISMATCH` |
| Wrong entrypoint digest | same parametrized test | `ENTRYPOINT_DIGEST_MISMATCH` |
| Cold replay / stale nonce | `test_stale_nonce_and_cold_replay_are_refused` | `NONCE_REPLAYED` and `NONCE_MISMATCH` |
| Fake issuer | `test_fake_issuer_is_refused` | `ISSUER_MISMATCH` |
| Missing native event | `test_missing_native_event_from_actual_process_is_refused` | `NATIVE_EVENT_ANTI_JOIN`, result itself still matched |
| Missing native import | `test_missing_expected_native_import_is_refused` | `NATIVE_IMPORT_ANTI_JOIN` and missing import event |
| Same-name status spoof | `test_same_name_status_spoof_from_actual_process_is_refused` | same `add`/`double` names, `double` status `RAISED`, `NATIVE_EVENT_STATUS_MISMATCH` |
| Changed runtime import + cold restore | `test_changed_runtime_import_refused_then_cold_restore_accepted` | changed digest refused, restored file accepted in a fresh process |
| Wrong result | `test_wrong_result_from_actual_process_is_refused` | `RESULT_MISMATCH` |

## Targeted mutation and restoration

- Mutation: in `universal_runner_verify.py`, changed
  `if actual_status != expected_status:` to
  `if False and actual_status != expected_status:`, disabling only the same-name status-spoof refusal.
- Targeted command: `/usr/local/bin/python3 -m pytest -q -p no:cacheprovider tests/universal_runner/test_universal_runner_verify.py::test_same_name_status_spoof_from_actual_process_is_refused`
- Mutant result: **exit 1**, exact assertion failure `assert 'LOCAL_NATIVE_VERIFIED' == 'REFUSE_NATIVE_QUALIFICATION'`; the mutation did not crash an import.
- Restoration: original condition restored; same targeted command **exit 0**, 1 passed.
- `git diff --exit-code -- CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py` after restoration: **exit 0** (clean).
- Raw outputs are in `mutation_targeted_failure.txt` and `mutation_restored_pass.txt`.

## Exact candidate references

- Code commit: `2cc6ce35112a9b98178556cd07ffd46f6ec815fb`
- Code tree: `4f7102cd42c710b3d2b6ed227eb267b08de15e52`
- `CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py` blob: `04d06bfe4c0cc3150e6012b2b42d421b00c75551`; SHA256 `60f1c359fa0f1c6cd5d91b59243d129b8073b7ef4b7580918342d79b7b571a6c`
- `tests/universal_runner/test_universal_runner_verify.py` blob: `8c77529859fcd1f8f5ee690c768d4bc92e6acf46`; SHA256 `a08cff30dd1386198a2768f4bf6ad60a0a9bd3f0831e5614f8e9e5cd50d24f88`

Exact changed code/test paths:

1. `CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py`
2. `tests/universal_runner/test_universal_runner_verify.py`

Return artifacts are listed with hashes in `manifest.json`.

## Trusted-runtime exclusions

- Protected CI required-check installation was not performed.
- Repository-administrator required-check attestation was not performed.
- No production keys or secrets were used.
- No original survey data was read.
- No original science, rights, F6/F7/F8 or N11/N12 issuance is claimed.
- The local subprocess harness is **not** a hostile-code sandbox. A real trusted supervisor must isolate untrusted candidate code and capture observations outside its control.
- The same model/provider cannot establish organizational scientific independence. Independent review remains reserved for the distinct later session/worktree.
- Local green does not authorize generic promotion.

## Artifacts

- `00_RETURN.md` — this return
- `proof_witness.json` — exact tests, result counts, mutation/restoration witness
- `RESUME.md` — cold restart instructions and held boundary
- `junit.xml` — focused native test receipt
- `existing_oracle_junit.xml` — unchanged existing oracle regression receipt
- `mutation_targeted_failure.txt` — targeted mutant failure output
- `mutation_restored_pass.txt` — restored targeted pass output
- `manifest.json` — SHA256 for the above report artifacts; excludes only itself
