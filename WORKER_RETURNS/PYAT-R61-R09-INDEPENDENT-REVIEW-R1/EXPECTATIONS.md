# R09V frozen independent expectations (written before candidate inspection)

Reviewer: NEW session, not R09 author ses_e98c8b6c7ffeXtAnuGL58sAeCp.
Candidate/startup: c8dbdd017b216e01dc43e0e15d4e044f3ec6d6e8.
Author code commit: 2cc6ce35112a9b98178556cd07ffd46f6ec815fb.
Seal/authority commit: 3fd3cba5a42caa3853c5bd5b5a881feddf1a4ae2.
Frozen: 2026-10-23T05:35Z (before reading `CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py`,
`tests/universal_runner/`, or `WORKER_RETURNS/PYAT-R61-R09-IMPLEMENTATION-R1/`).

## Scope and grade

Sourcefree TEST_ONLY local prototype. R09V reviews the LOCAL promised guarantee only:
a trusted local runner/verifier must distinguish independently observed actual
process/import/result/run custody from candidate-authored flags/receipts. It does
NOT authorize generic promotion, deployed enforcement, protected CI, science,
original35 issuance, N11/N12, workflow/admin changes, or production adoption.
The existing R00 ceiling and DEPLOYMENT_HOLD for production are preserved.

## Acceptance required from the contracts

A. Evidence identity and manifest
   - Actual reviewer HEAD equals candidate startup; direct remote author branch
     equals the same SHA; changed paths from seal c84842e20 are exactly the
     assigned allowlist (`CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py`,
     `tests/universal_runner/`) plus the author's own returnroot.
   - Report manifest hashes recomputed independently, self-exclusion explicit,
     every listed artifact present and hash-matching.

B. Positive acceptance
   - A genuine fresh native subprocess run of a known baseline is accepted.
   - Acceptance derives from supervisor-captured actual process facts: executable
     and argv, exit status, emitted event(s), actual imported module path and
     bytes/digests, returned value/result, exact candidate commit/tree/policy,
     and a fresh run nonce.
   - Independently frozen expected result (not candidate enumeration) is compared
     to the observed value at an exact assertion.
   - Real imported-owner identity is observed, not merely declared.
   - Cold replay in a new process gives the same decision; nonce must be fresh.

C. Refusal required (each is a falsifier if accepted as PASS)
   F1  Candidate-authored booleans/status/receipt dictionaries, with no
       supervisor-captured process facts, must not be accepted.
   F2  Candidate-selected expected outcomes / policy / manifest must not become
       the oracle (self-pin). External pin mismatch must refuse.
   F3  Wrong/stale/replayed/cross-run-transplanted run nonce must refuse; a
       nonce captured from another run must not authenticate this run.
   F4  Wrong or substituted candidate commit/tree/policy/issuer/key/entrypoint
       must refuse.
   F5  Merely resolving git HEAD/tree without binding the actually executed
       bytes (module/import substitution, dirty path, replaced file after
       resolution) must not qualify a changed candidate.
   F6  Missing native event/call/import, or an exception caught and converted to
       a success-looking status, must refuse. Absence is not success.
   F7  Same-name/status spoof (e.g. candidate returns "PASS" string or a
       look-alike mapping) must refuse; status must be derived from captured
       facts, not trusted candidate text.
   F8  Output substitution/deletion (result value or event payload differs from
       captured run/output) must refuse.
   F9  Malformed and typed inputs (bool where mapping required, int/str/bool
       confusion, missing required keys) must fail closed with a typed refusal,
       not crash-accept or default-permit.
   F10 Unsafe defaults (missing required check, missing binding, missing nonce,
       missing supervisor evidence) must deny, never allow.
   F11 Concurrent/cold reuse: replay or concurrent invocation must not permit a
       previous accepted observation set to vouch for a new run.
   F12 The verifier must not accept an observation object the candidate itself
       can construct and self-authenticate. Trusted-supervisor preconditions
       must be explicit: what the caller must supply from outside candidate
       control, and what the verifier itself actually checks.

D. Targeted mutation and restoration
   - One meaningful false-positive mutation at an exact assertion: baseline
     accepts, mutated verifier/fixture refuses, restored baseline accepts again
     (all in disposable copies inside this returnroot; candidate untouched).

E. Honest capability accounting
   - State which local guarantee is real and which is NOT_REACHED.
   - No claim of protected-CI enforcement, OS sandbox/attestation, external
     issuer/key authority, original science, or deployed R09.
   - Verdict finite: ACCEPT_SCOPED_LOCAL or REVISE, with ranked reproducible
     defects (minimal exact input, observed vs required, contract ref).

## Frozen trusted-runtime exclusions and threat model

- No protected CI/workflow, no branch-protection/admin check, no installed
  required check, no remote runner or hardware attestation. Presence/absence of
  protected CI alone is not grounds to redesign deployment; local guarantee is
  judged on its own stated boundary.
- No external key service or authenticated issuer identity. Any "issuer" is a
  local test identity; it cannot be called externally authenticated.
- No OS isolation between candidate and supervisor beyond ordinary subprocess
  and filesystem semantics on one machine under one user/account. A candidate
  able to rewrite the verifier, its imports, or the Python runtime defeats any
  purely local check; that residual is excluded and must be stated, not silently
  claimed as prevented.
- The *promised* local boundary: verifier code and supervisor live outside
  candidate-writable production/test paths; candidate supplies only inputs that
  are re-derived/checked against externally pinned policy/commit/tree/nonce;
  accepted facts come from supervisor's own process/import/result capture.
- A caller who passes forged "trusted" objects into the verifier is outside the
  guarantee only if the verifier documents and enforces the required external
  provenance. Arbitrary author-supplied expected outcomes may never be treated
  as independent facts.
- Synthetic code cannot issue original science; all35/1890/global obligations and
  Z UNRESOLVED16 remain unchanged. No original data/credentials/external reads.
