# R09 R2 — trusted execution custody repair return

## Return status

- **Revision:** R2 bounded repair of the R09 local verifier.
- **Engineering state:** `LOCAL_CODE_COMPLETE_R2_CANDIDATE`
- **Disposition:** `HOLD` for R2 independent review; `DEPLOYMENT_HOLD` for production.
- **Author validation only:** the distinct R2 reviewer session has not occurred. No self-adoption and no deployed enforcement claim.
- **Startup verified:** `c8dbdd017b216e01dc43e0e15d4e044f3ec6d6e8`, clean tracked tree, direct remote author branch also `c8dbdd017...`.
- **Scope used:** `CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py`, `tests/universal_runner/`, and only `WORKER_RETURNS/PYAT-R61-R09-IMPLEMENTATION-R1/revisions/r2/`. Original v1 return and independent-review return were not modified.

## Commission and review inputs read first

Read in full before repair:

- `3d1e4049675cc7e1f5042a6107fea0acf36b2b68:WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/R09/revisions/r2/00_REPAIR_COMMISSION.md`
- independent review `05e9ce39640ca6a134031510e762e81fab7d4c57`: `00_RETURN.md`, `defects.md`, `EXPECTATIONS.md`, `probes/independent_probes.py`, `evidence/probes_candidate.json`, `evidence/malformed_result.json`, `evidence/identity.json`, `manifest.json`, `proof_witness.json`, `RESUME.md`.

The review verdict was `REVISE`, not adoption. Its seven ranked defects were treated as real function failures.

## Plain-English function delivered

The local verifier now has an **external trust root**, not a magic issuer string:

1. A `TrustRoot` owns a random signing key outside the executed child. The child never receives that key.
2. `LocalNativeSupervisor.observe(...)` seals its captured payload with an HMAC and returns a `TrustedObservation`.
3. `verify_observation(...)` accepts only a sealed observation whose fingerprint matches the externally frozen expectation and whose HMAC still matches its current content.
4. A plain dict, a copied observation, or a post-capture issuer/result/event edit refuses as `UNTRUSTED_OBSERVATION` or `OBSERVATION_AUTHENTICATION_FAILED`.

The child can no longer supply accepted evidence merely by being a dict or by rewriting a string.

## Defect-by-defect repair

### D1 — subject-owned observation overwrite

- The supervising parent reads the child result once and seals it with the external trust-root key.
- The wrapper writes its final payload and exits with `os._exit(0)`, so subject `atexit` handlers cannot overwrite the result after capture.
- Regression `test_subject_observation_overwrite_does_not_change_captured_result`: a committed subject attempts to rewrite the observation to `42` at exit; the captured result remains the actual `41` and the run refuses `RESULT_MISMATCH`.

### D2 — unauthenticated mapping / fake issuer

- Arbitrary dict observations refuse `UNTRUSTED_OBSERVATION`.
- Mutating a sealed observation refuses `OBSERVATION_AUTHENTICATION_FAILED`.
- An attacker-created trust root refuses `TRUST_ROOT_FINGERPRINT_MISMATCH`.
- The optional `candidate_evidence` argument is no longer the boundary; it remains an additional refusal path, not an enablement switch.

### D3 — claimed tree not bound to executed bytes

- The entrypoint is read from the exact candidate commit with `git show <commit>:<path>` and that exact byte string is compiled/executed. Dirty worktree entrypoint bytes are not executed under an old commit label.
- Entrypoint and target paths outside the repository are refused before execution (`ENTRYPOINT_OUTSIDE_CANDIDATE_TREE` / `TARGET_FILE_OUTSIDE_CANDIDATE_TREE`).
- Every imported repository source is associated with its candidate-tree relative path. The parent compares the load-time digest with the exact candidate blob. Missing or outside-tree imports fail custody.

### D4 — after-exit rehash instead of loaded bytes

- A custody meta-path finder reads each imported repository `.py` source once, hashes those bytes, compiles those same bytes, and records the digest.
- The parent compares that **load-time** digest to the candidate commit blob.
- Worktree mutation after commit refuses `NATIVE_CUSTODY_FAILED:IMPORT_LOADED_BYTES_NOT_IN_TREE:<module>`.
- A self-restoring module that changes behavior and restores its own file refuses from the load-time digest; the restored file no longer conceals the execution.

### D5 — default cold replay

- Verification requires a durable ledger; an in-memory ledger refuses `NONCE_LEDGER_NOT_DURABLE`.
- The CLI without a ledger path refuses both cold invocations.
- With a ledger path, first cold invocation accepts and a second cold invocation refuses `NONCE_REPLAYED`.

### D6 — concurrent ledger race

- `NonceLedger` now re-reads its data file inside an exclusive `fcntl.flock` on every claim, then appends and fsyncs.
- Two instances constructed before either consumes cannot both accept.
- `test_cross_process_nonce_claim_is_atomic` starts two real processes against the same ledger and observes exactly `CLAIMED` plus `REPLAYED`.
- Malformed ledger content refuses `NONCE_LEDGER_CORRUPT`; crash after append leaves the nonce consumed, which is the fail-closed retry rule.

### D7 — malformed typed input crash

- Result and expectation digests use a guarded canonical encoder.
- Non-serializable result/expectation refuses with `OBSERVED_RESULT_NOT_SERIALIZABLE` or `EXPECTATION_RESULT_NOT_SERIALIZABLE` rather than raising `TypeError`.

## Positive actual native owner

The positive is no longer only an `add`/`double` toy marker.

`tests/universal_runner/native_c11_entry.py` executes the existing current native C11 owners:

- `rawlsing_next.pre553_c11_ingest.ingest_c11_source_release`
- `rawlsing_next.pre553_c11_repository.C11Repository.resolve_release_exact`

The sourcefree synthetic C11 fixture is built only through existing native constructors in `tests/universal_runner/native_c11_case.py`. The independently frozen expected result is:

```json
{"accepted": true, "disposition": "ACCEPTED_C11_LOGICAL_RELEASE", "event_count": 2, "release_id": "REL-R09", "repository_length": 1, "m01_m18_count": 18}
```

The test verifies actual import audit events and tree-bound load-time digests for `native_c11_case`, `rawlsing_next.pre553_c11_ingest`, and `rawlsing_next.pre553_c11_repository`. This is a real existing sourcefree native-owner path, not all-universal or original35 execution.

## Exact commands and results

Environment: Darwin, `/usr/local/bin/python3` 3.11.3, pytest 9.0.2, pyreadstat 1.3.2 verified but unused, git 2.43.0.

| Command | Exit | Result |
|---|---:|---|
| `/usr/local/bin/python3 -m pytest -q -p no:cacheprovider tests/universal_runner --junitxml=WORKER_RETURNS/PYAT-R61-R09-IMPLEMENTATION-R1/revisions/r2/junit.xml` | 0 | 14 passed, 0 failed, 0 errors, 0 skipped, 4.08 s |
| `/usr/local/bin/python3 -m pytest -q -p no:cacheprovider tests/universal_execution_oracle --junitxml=WORKER_RETURNS/PYAT-R61-R09-IMPLEMENTATION-R1/revisions/r2/existing_oracle_junit.xml` | 0 | 48 passed, 0 failed, 0 errors, 0 skipped, 30.99 s |
| `/usr/local/bin/python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py lint tests/universal_runner/test_universal_runner_verify.py` | 0 | `AST_LINT_PASS` |
| `/usr/local/bin/python3 -m py_compile` on verifier, test and C11 fixture modules | 0 | compile passed |

## Reviewer-probe replay and deliberate supersession

`reviewer_probes_against_r2.json` replays the independent probe file against the repaired public behavior:

- P1 forged observation: refused.
- P2 fake issuer: refused.
- P3 out-of-tree claimed tree: refused.
- P4 loaded-bytes divergence: refused.
- P5 default CLI replay: both cold CLI runs refused.
- P6 preconstructed ledger replay: refused.
- P7 wrong-result baseline control: refused.
- P8 subject observation overwrite path: refused.

The old reviewer **P0** positive used temporary files outside the repository while labelling them with a repository commit/tree. That is exactly defect D3; it is intentionally no longer accepted. Its successor is the committed C11 native-owner positive above, which is tree-bound and uses a real external trust root and durable ledger.

## Targeted mutation and restoration

- Mutation: in `universal_runner_verify.py`, changed
  `elif typed_digest(observation.get("result")) != ...:` to
  `elif False and typed_digest(...) != ...:`, disabling only `RESULT_MISMATCH`.
- Targeted node: `tests/universal_runner/test_universal_runner_verify.py::test_missing_event_status_spoof_and_wrong_result_are_refused`
- Mutant: **exit 1**, false positive `LOCAL_NATIVE_VERIFIED` where `REFUSE_NATIVE_QUALIFICATION` was required.
- Restored: same node **exit 0**, 1 passed; `git diff --exit-code` on the verifier **0**.
- Raw outputs: `mutation_targeted_failure.txt`, `mutation_restored_pass.txt`.

## Exact candidate code references

- Code/test commit before return artifacts: `77f8b4205d8a97f2e9f7ae9e93a3ff913c08a780`
- Tree: `272fd70478b0a46d55ac4be29a2009d27228f7fb`
- `CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py` blob `7af149e9d0e9cb2bc85c31d370145a86abf078b8`; SHA256 `3cf9f5e7d07c110a47fff75c02d4169590060daf24518be95d46ddebf9103b8d`
- `tests/universal_runner/test_universal_runner_verify.py` blob `0e1a5725ceb4efcf78060bbd13257bc46321c140`; SHA256 `2b00fd2f7207568a2a578aefa50f7293970be07ca41b576e0929f8a422d54de9`
- `tests/universal_runner/native_c11_case.py` blob `5727edbaddba2eab6bc91c4e5fb2917f26b296d2`;
- `tests/universal_runner/native_c11_entry.py` blob `537f5c529d1966464d949e914f40f1b160053aad`.

Changed paths from `c8dbdd017...`:

1. `CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py`
2. `tests/universal_runner/test_universal_runner_verify.py`
3. `tests/universal_runner/native_c11_case.py`
4. `tests/universal_runner/native_c11_entry.py`
5. `WORKER_RETURNS/PYAT-R61-R09-IMPLEMENTATION-R1/revisions/r2/*` (this return only)

## Honest limits

- This is still a local TEST_ONLY verifier. The local subprocess is not a hostile-code sandbox.
- The trust-root key must be supplied from outside subject control. A caller who hands its key to the subject, or a same-UID subject able to rewrite the verifier/runtime, defeats any purely local check; that residual is stated, not claimed prevented.
- Protected CI required checks, repository-admin attestation, external key service, original data/science, N11/N12 and deployed enforcement remain NOT_REACHED and held.
- All 35 / 1,890 / global F6–F8 and Z UNRESOLVED 16 obligations are unchanged.
- The R00 ceiling remains local-only; production remains `DEPLOYMENT_HOLD`.
