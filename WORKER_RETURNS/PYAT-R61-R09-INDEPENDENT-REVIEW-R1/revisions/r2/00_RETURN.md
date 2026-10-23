# R61-R09V R2 — independent hostile review return

**Verdict: `REVISE` (scoped local), with `HOLD` for the central independent-capture
promise.** R2 genuinely repairs several v1 controls and delivers a real committed
C11 ingest/repository positive. It does **not** repair D1/D4: the parent still
accepts and HMAC-seals a **child-authored** observation protocol. The child can
forge the reported result and the reported loaded-byte digest through ordinary
in-process Python interfaces, and the R2 run is accepted. `DEPLOYMENT_HOLD`
remains. This reviewer did not repair or adopt the candidate.

## Exact identity

- R2 startup/candidate: `4a10c82aa8ba2a31938d3d35e12dc42f4456264c`
  (tree `ea3d86fa9760221805b82620a8c30125e1f7fb1c`).
- R2 author code commit: `77f8b4205d8a97f2e9f7ae9e93a3ff913c08a780`
  (tree `272fd70478b0a46d55ac4be29a2009d27228f7fb`).
- R2 repair commission seal: `3d1e4049675cc7e1f5042a6107fea0acf36b2b68`.
- Prior independent review: `05e9ce39640ca6a134031510e762e81fab7d4c57`
  (`REVISE`, D1-D7).
- Author branch `agent/opencode-pyat-r61-r09-local-runner-r1` = startup SHA;
  reviewer branch `agent/opencode-pyat-r61-r09v-r2-independent-review-r1`
  started at the same SHA.
- Verifier blob `7af149e9d0e9cb2bc85c31d370145a86abf078b8`, SHA256
  `3cf9f5e7d07c110a47fff75c02d4169590060daf24518be95d46ddebf9103b8d`.
  Test blob `0e1a5725ceb4efcf78060bbd13257bc46321c140`, SHA256
  `2b00fd2f7207568a2a578aefa50f7293970be07ca41b576e0929f8a422d54de9`.
  C11 fixture blobs `5727edba...` and `537f5c52...`.
- Tools: `/usr/local/bin/python3` 3.11.3, pytest 9.0.2, git 2.43.0,
  Darwin 22.3.0 x86_64. Model/session as commissioned; new reviewer session,
  not author `ses_e98c8b6c7ffeXtAnuGL58sAeCp`. Same provider account is only
  role/session separation, not institutional scientific independence.
- EXPECTATIONS were frozen in commit `ef39f11e4` before reading R2 code or
  author conclusions.

## What R2 genuinely fixes (reviewer-replayed)

- Author focused suite: **14 passed**, 0 failed/errors/skipped, exit 0 (4.81 s),
  reviewer-owned JUnit `evidence/reviewer_author_suite_junit.xml`.
- Bare mapping refuses `UNTRUSTED_OBSERVATION`; rewritten issuer or mutated
  sealed observation refuses `OBSERVATION_AUTHENTICATION_FAILED`.
- Out-of-tree entrypoint refuses before acceptance; naive worktree mutation
  refuses `NATIVE_CUSTODY_FAILED:IMPORT_LOADED_BYTES_NOT_IN_TREE`.
- Non-durable ledger refuses; cold replay with a durable ledger accepts once and
  refuses `NONCE_REPLAYED`; two real concurrent claim processes return exactly
  `CLAIMED`/`REPLAYED`.
- Author `manifest.json` independently recomputed: **8/8** artifacts hash/size
  match, self-exclusion explicit. v1 author reports are byte-unchanged
  (`git diff --exit-code` from the v1 candidate = 0).
- Existing 48-test oracle receipt is retained by exact identity
  (`05e9ce39:.../reviewer_existing_oracle_junit.xml`, SHA256
  `2a11a2cd...5e64`, 48/0/0/0); R2 changes do not couple to that suite. No
  pointless fresh 48-test rerun was performed.

## Actual committed C11 positive (real, scoped)

The committed `tests/universal_runner/native_c11_entry.py` was executed through
the supervisor with an **independent reference computed in a plain process**
(not candidate enumeration): `native_c11_entry.run_native()` imported and called
the actual `ingest_c11_source_release` and `C11Repository.resolve_release_exact`
owners. Both the independent reference and the sealed observation returned:

```json
{"accepted": true, "disposition": "ACCEPTED_C11_LOGICAL_RELEASE",
 "event_count": 2, "m01_m18_count": 18, "release_id": "REL-R09",
 "repository_length": 1}
```

The observation was accepted locally with the actual C11 modules
(`native_c11_case`, `rawlsing_next.pre553_c11_ingest`,
`rawlsing_next.pre553_c11_integrity`, `rawlsing_next.pre553_c11_repository`,
`rawlsing_next.pre553_empirical_authority`,
`rawlsing_next.pre553_empirical_objects`) tree-bound. A wrong frozen expectation
refused `RESULT_MISMATCH`. This is a real local owner/consumer capability delta,
not whole-machine or original35 execution.

## Decisive defects (reproducible; full detail in `defects.md`)

1. **D1-R2 critical — parent seals a child-authored observation.**
   A committed support module monkeypatches `json.dump` in its own interpreter.
   The entrypoint computes the real `double(add(20,1)) = 41`; the patched dump
   rewrites the wrapper payload to `42`. The parent re-seals it with the
   external trust-root HMAC and `verify_observation` returns
   `LOCAL_NATIVE_VERIFIED` with `reasons=[]`. Marker proof: actual returned
   value `41`; sealed result `42`. `os._exit(0)` stops the prior `atexit`
   overwrite but does not stop in-process protocol/result forgery. Probe
   `P1_child_json_dump_forges_result`.
2. **D4-R2 critical/high — loaded-byte custody is child-reported.**
   The entrypoint installs its own meta-path finder, loads malicious code from
   a string compiled with the target filename, injects a fake
   `loaded_sources["native_fixture"]` record carrying the benign tree digest,
   and reports result `42` while the loaded code returns `41`. The parent
   compares the fake digest to the benign git blob (bound), and the run is
   accepted. Probe `P2_child_forges_loaded_bytes_and_result`.
3. **D7-R2 low/medium — malformed expectation still crashes.**
   An authentic observation with an expectation whose `expected_result` is a
   Python `set` raises `TypeError: Object of type set is not JSON serializable`
   at the unguarded result comparison, instead of a typed refusal. The author
   test only exercises a *mutated* observation, which returns early on HMAC
   failure and hides this path. Probe `P10_non_serializable_expectation`.
4. **Trust-root admission boundary (disclosed, not the decisive defect).**
   Any caller can construct its own `TrustRoot`; the verifier has no external
   anchor for which root is admissible. A self-rooted fixture is accepted
   (`P5_self_root_caller_accepted`). This is acceptable only if the caller and
   key really are outside subject control and an external authority pins the
   root; the code documents that precondition but does not enforce it.

## Missing primitive, owner, and options

The central R09V promise cannot be met by another local canary patch. The exact
missing primitive is a **parent-owned observation channel for actual Python
return objects and actual loaded bytes that the subject cannot mutate or
self-report**. The subject's process controls its own `json`/frames/import
system; an HMAC applied by the parent to that self-report authenticates only
that the parent sealed the subject's claims.

- **Owner:** R09/CI engineering plus the host/platform administrator for an
  OS-level execution boundary. Not the current author-only local code path.
- **Option A (minimal honest):** separate-UID/container/VM runner or sandbox,
  with a frozen native harness that imports the subject module and streams the
  actual return object over a parent-owned pipe the subject cannot write.
- **Option B:** kernel/OS tracing/attestation (ptrace/DTrace/eBPF) of the actual
  execution plus a parent-controlled harness for return values.
- **Option C:** explicitly downgrade the local promise to a non-adversarial
  subject. This is a threat-model downgrade and is not accepted for R09V.

D2/D3/D5/D6 controls and the C11 positive are worth preserving. D7 is a small
bounded fix. D1/D4 require the higher-engineering boundary above; this is not a
third minor audit request.

## Real capability vs NOT_REACHED

Real, under a well-behaved subject: genuine subprocess execution, committed
entrypoint bytes, exact tree/commit/policy/run bindings, bare-mapping/issuer
refusal, out-of-tree refusal, mandatory durable ledger, atomic cross-process
nonce, and an actual committed C11 ingest/repository positive with an
independent reference result.

NOT_REACHED / not established: independent capture of actual return values;
independent loaded-byte custody against a lying subject; authenticated external
trust-root admission; protected CI required-check enforcement; repository-admin
attestation; OS sandbox/isolation; external key service; original survey
data/science; original35/1890; N11/N12; generic promotion; deployed enforcement;
whole-machine execution. Browser whole-native runtime remains unqualified.

## Obligations and stopping conditions

All original 35/1,890/global F6/F7/F8 obligations and Z UNRESOLVED 16 are
unchanged. No source/science/rights/N11/N12/production claim is made. No
architecture/science fork was raised; this is a bounded independent-capture
engineering failure with a finite missing primitive. Reviewer wrote only this
returnroot; candidate files are byte-identical (`git diff --exit-code` = 0).
Final non-force push is to the assigned reviewer branch only; the direct
`ls-remote` SHA is stated in the final response.

## Artifacts

`EXPECTATIONS.md`, `defects.md`, `probes/independent_probes_r2.py`,
`probes/mutant_check.py`, `evidence/probes_r2.json`,
`evidence/reviewer_probes_junit.xml`, `evidence/reviewer_author_suite_junit.xml`,
`evidence/mutant_check.json`, `evidence/identity.json`, `proof_witness.json`,
`SHA256 manifest.json` (self-excluded), `RESUME.md`, `REMOTE_VERIFICATION.md`,
and the disposable mutant copy under `mutants/`.
