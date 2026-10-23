# R61-R09V R2 frozen independent expectations

Reviewer role: NEW reviewer session, not R09 author `ses_e98c8b6c7ffeXtAnuGL58sAeCp`.
Assigned reviewer branch: `agent/opencode-pyat-r61-r09v-r2-independent-review-r1`.
Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r09v-r2`.
Exact R2 startup/candidate: `4a10c82aa8ba2a31938d3d35e12dc42f4456264c`.
R2 author code commit named by commission: `77f8b4205d8a97f2e9f7ae9e93a3ff913c08a780`.
R2 repair commission seal: `3d1e4049675cc7e1f5042a6107fea0acf36b2b68`.
Prior independent review: `05e9ce39640ca6a134031510e762e81fab7d4c57` (REVISE; D1-D7).
Authority: user R61 grant `3189a0db1433095c95bfe0294af53a40355fa1dd`; sourcefree TEST_ONLY.
Frozen: 2026-10-23T06:12Z, **before** reading R2 candidate code, R2 tests, or any R2
author return/conclusion. Sources read only: R09 original commission + NODE,
R09/R2 repair commission, R09V commission, INPUTS/CONTRACTS/TESTS/OVERLAYS/
USER_GRANT/FLIGHT, and the prior independent review at `05e9ce39`.

## Scope and grade

Local TEST_ONLY prototype qualification only. The question is whether the
GENERIC independent local capture function now holds: whether accepted
observations are independently obtained from an actual candidate-owned native
execution, rather than authored, sealed, authenticated, or overwritten by the
untrusted subject. This does NOT authorize generic promotion, deployed
enforcement, protected CI, repository-admin attestation, original science,
original35/1890 issuance, N11/N12, workflow/config changes, source access, or
production adoption. R00 ceiling and DEPLOYMENT_HOLD remain.

## Identity and custody checks

A1. Actual reviewer HEAD equals `4a10c82a...`; candidate/startup tree and parents
    recorded. Direct remote `refs/heads/agent/opencode-pyat-r61-r09-local-runner-r1`
    equals the same startup commit, and reviewer remote starts at the same.
A2. R2 changed paths from the prior candidate/commission seal are exactly the
    R09 write allowlist (`CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py`,
    `tests/universal_runner/`) plus R09 author returnroot R2 artifacts. v1
    author reports and prior reviewer reports are byte-unchanged. No workflow,
    config, lockfile, R00 gate, or existing native owner edited.
A3. Exact blob/commit/tree/SHA256 of verifier, tests, imported modules and
    entrypoints recorded from actual HEAD, plus direct remote identity.
A4. Author R2 manifest recomputed: every listed artifact present, size and
    SHA256 match, explicit self-exclusion. Author claims are not the oracle.
A5. Reviewer writes only
    `WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/revisions/r2/`; probes,
    fixtures and mutants stay inside it; candidate files byte-identical after
    all work (`git diff --exit-code` = 0).

## Central D1: whole independent capture, not canary/HMAC theatre

The promised boundary is independent observation of the actual subject process,
imports, calls, returned objects, stream/output, and run identity. Parent
possession of a handle/key and a MAC/signature over a child-authored artifact or
child-authored protocol does **not** prove independent observation. Stopping
`atexit` alone does not remove subject control.

D1-R2 falsifiers (any accepted = REVISE/HOLD, not PASS):

1. Subject, through an ordinary subject-accessible interface (imported module,
   config file, observation/result file, event/message stream, stdout/stderr,
   environment, argv, fixture, plugin hook, import hook, cwd), can overwrite,
   substitute, delete, replay, or spoof the observation/result that the
   supervisor accepts, including after capture and before verification.
2. Parent HMAC/signature/wrapping over a subject-authored or subject-writable
   observation/event stream is accepted as independent custody.
3. A subject-authored observation or event with no genuine process, or with a
   fabricated exit/event/import/result, is accepted. This includes a bare
   mapping, `candidate_evidence` omission, issuer rewrite, magic issuer string,
   digest reseal, or self-root.
4. The subject can cause the parent to derive accepted facts from a file or
   stream the subject controls after the fact (including restore/self-repair at
   exit), rather than from bytes/facts captured or protected by the parent.
5. Capture is only a subprocess's self-report with no independent cross-check
   of the actual execution object/returned value (where the subject can emit
   the protocol itself).

The excluded residual is the genuinely private runtime: a subject able to
rewrite the verifier, its interpreter, or the parent's private memory/process
(debugger/ptrace, same-UID write to verifier files, malicious Python runtime).
Exclusions must be explicitly documented and must not be used to excuse
subject-accessible artifact/config/stream substitution. The review must
distinguish these realms with concrete probes.

## Signature, issuer, trust root, keys

S1. A genuine externally authenticated issuer must not authenticate forged
    content that originated inside the untrusted subject; signature validity of
    a subject-supplied payload is not content independence.
S2. Trust-root admission must not accept a root/key/issuer supplied or changed
    by the untrusted subject or by the same untrusted claim/expectation pair.
    Changing a key on both the untrusted claim and the untrusted expectation is
    not external trust.
S3. Fake issuer strings, self-declared roots, digest reseals, exported/leaked
    keys, and admission of arbitrary caller trust material must refuse.
S4. A bare mapping, forged typed observation, or caller-constructed "trusted"
    object must not pass merely because it has the expected schema/issuer.

## Executed-byte and tree custody

B1. Executed entrypoint and imported module bytes must be bound to the exact
    claimed candidate commit/tree/allowlist, not merely resolved by git HEAD,
    name, or post-exit hash.
B2. Loaded-byte custody must cover actual bytes read/executed: alternate
    import/package routes (`sys.path`, zip/import hooks, `sitecustomize`,
    `__pycache__`, namespace/path shadowing, symlinks, cwd, `PYTHONPATH`,
    `-m`, package re-execution), dirty replacement, self-mutating modules, and
    restore-after-load must not pass.
B3. `target_file`/import digests must be compared to independently frozen
    expectations; recording without checking is not custody.
B4. Missing required entrypoint/import/event/call, or an exception swallowed
    into a success-looking status, must refuse; absence is not success.
B5. Same-name/status spoof and output substitution (result value, event
    payload, returned object) must refuse.

## Replay, nonce, ledger, crash/retry, concurrency

R1. Replay protection must be mandatory and fail-closed by default, with an
    externally supplied durable one-shot nonce/ledger, not an optional path.
R2. Same observation/expectation replayed in a cold new process must refuse.
R3. Concurrent processes/instances must have atomic check-and-insert across
    processes (lock/atomic store), not process-local lock plus stale snapshot.
R4. Crash/retry must have defined, tested behavior: a consumed nonce is not
    silently reusable; a failed/partial run cannot become accepted by retry.
R5. Cross-run transplant of a nonce/observation or changing run ownership must
    refuse.
R6. Malformed, non-JSON, typed-confused, missing-key, and oversized inputs must
    fail closed with a typed refusal, not crash, default-permit, or traceback.

## Actual committed C11 positive (not toy-only)

P1. A genuine, actual committed C11 ingest/repository/native-owner positive is
    executed from the exact candidate tree, with an independently frozen
    expected result (not candidate enumeration).
P2. Actual calls/imports/returned objects and their exact module paths,
    digests, and call identities are captured/recorded; a synthetic
    add/double or temporary fixture alone does not satisfy the C11 positive.
P3. Same-consumer mutation/severance must fail the intended assertion; the
    original candidate must be restored and the positive re-pass. A mismatch
    that merely causes an unrelated import crash is not evidence.
P4. Cold replay of the C11 positive (fresh process) must produce the same
    decision/result within the appropriate local ceiling; concurrent nonce
    proof must also be shown.
P5. The C11 positive must remain TEST_ONLY/local and must not claim whole
    machine, original35, source/science, or deployed enforcement.

## Existing and historical obligations

H1. Prior P0-P8 and D1-D7 remain historical witnesses; their exact API may be
    versioned. Successor probes must demonstrate the intended guarantee; an
    import/type/signature crash does not count as a successful safety refusal.
H2. Preserve all genuine prior positives and the R00 ceiling; no weakening of
    promised guarantees to make tests green.
H3. The prior 48-test existing-oracle receipt may be retained by exact identity
    if no concrete new coupling risk is found; otherwise replay it. R2 focused
    tests are replayed with reviewer-owned JUnit.
H4. All 35/1,890/global F6/F7/F8 and Z UNRESOLVED 16 remain unchanged.
H5. Target one meaningful assertion-level mutant in a disposable copy inside
    this returnroot, show baseline pass -> mutant failure -> restored pass; the
    candidate is never edited.

## Verdict rule and missing-function duty

Return exactly one finite verdict under the original local promise:
`ACCEPT_SCOPED_LOCAL` only if the whole capture boundary and required positive/
refusal controls actually hold; otherwise `REVISE` (or bounded `HOLD` if an
unavailable primitive is genuinely required). If the central custody promise
still fails after R2, report the exact missing primitive/function, its owner,
and minimal implementation or host/scope options (with why ordinary bounded
repair is or is not sufficient). Do not produce a third minor canary audit, do
not downgrade the threat model, and do not raise architecture/science process
unless an actual architecture/science change is required. No author repair, no
self-adoption, no new authority, no deployment.

## Frozen trusted-runtime exclusions

- No protected CI/workflow, branch protection, admin attestation, installed
  required check, remote runner, or hardware attestation.
- No external key service, certificate authority, or institutionally
  authenticated issuer; any local issuer is a test identity.
- No OS isolation beyond ordinary subprocess/filesystem semantics under one
  user; no container/VM/seatbelt/namespace boundary is installed or claimed.
- The residual threat is a subject that can write the verifier/its imports/
  interpreter/parent memory or otherwise escape ordinary subject interfaces.
  That residual is excluded and disclosed, never silently claimed prevented.
- The promised local boundary is only: verifier code and supervisor outside
  candidate-writable production/test paths; candidate supplies inputs that are
  re-derived/checked against externally pinned policy/commit/tree/nonce; the
  accepted facts come from the supervisor's own actual process/import/result
  capture, not from subject-authored artifacts or protocols.
- Synthetic code cannot issue original science, rights, N11/N12, or deployed
  enforcement. No original data, credentials, private files, listeners,
  privileges, provider/model switch, subagents, or extra sessions.
