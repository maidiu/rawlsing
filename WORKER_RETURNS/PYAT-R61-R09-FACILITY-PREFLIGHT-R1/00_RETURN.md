# R61 R09F — finite existing-facility preflight

**Verdict: `FACILITY_GAP`.**

No existing qualified protected broker/native-owner facility was found on the
commissioned host. This is not a universal absence claim: any external
CI/VM/issuer facility was not observed and remains `UNVERIFIED`, not `ABSENT`.
The existing controller is reusable scheduling/receipt machinery, not proof of
protected native capture.

## Identity, authority and scope

- Startup: `3470da602618b5c04b1f28885b5ad1835169e2d5`.
- Branch: `agent/opencode-pyat-r61-r09f-facility-preflight-r1`.
- Direct remote at start: the same SHA
  (`refs/heads/agent/opencode-pyat-r61-r09f-facility-preflight-r1`).
- Authority: R61 sourcefree `TEST_ONLY` grant
  `3189a0db1433095c95bfe0294af53a40355fa1dd`; I2-I3/S3 bounded engineering.
- No original respondent/source/science/production/protected-CI/N11/N12/Sorok
  authority; no J52/W52 wake; no provider/model/account change; no extra
  sessions or subagents.
- Writes are confined to
  `WORKER_RETURNS/PYAT-R61-R09-FACILITY-PREFLIGHT-R1/`. `.r61` remains
  untracked. No credential file, auth/config file, user data or SQLite payload
  was read.
- Inherited evidence read: the R61E decision at HEAD, the R09 V2 independent
  review at `25510c8d84f0ae5e452b301b017bdedf46f40b5c`, controller
  `MAINMAC/CURRENT.md`, controller refs
  `365a6a16c99a82851fdf70d084eccd13d27956d9` and
  `c51b74b7a2a3d498c64387dc1ec95cb0c29a44b3`, and controller source interfaces.

## Method and limits

This was one bounded, non-mutating inventory. It used command availability and
read-only version/status checks, filesystem permission metadata, Git source
inspection at exact refs, and review of existing receipts. It did not install,
start, create or modify services, users, VMs, containers, permissions or
settings. It did not run isolation, ptrace, network, security or credential
tests. It did not rerun the controller pilot or dispatch a live worker. The R09
P1/P2 defects are taken from the independent review; they were not rerun here.

Exact commands and observed exits are in `COMMANDS_AND_EXITS.json`. Source
identities are in `SOURCE_REFS.json`; machine-readable facility findings are in
`FACILITY_INVENTORY.json`.

## What exists

| Asset | Observed state | Evidence | Bearing on the required facility |
|---|---|---|---|
| Host | macOS 13.2.1, Darwin 22.3.0 x86_64, uid 501 `matthewsmith` | `id`, `uname -a`, `sw_vers` in `COMMANDS_AND_EXITS.json` | One ordinary user principal; no service/UID boundary observed. |
| Docker / Podman / Colima / Lima | `ABSENT` | `/usr/bin/which` exits 1 for all four | No container/VM CLI available as an installed facility. External/remote facilities are `UNVERIFIED`. |
| macOS `sandbox-exec` | `PRESENT` at `/usr/bin/sandbox-exec`; usage exits 64 | command availability and controller source | A path-profile primitive exists, but it is not wired to worker/runtime execution and does not create a separate principal. Its use as a broker boundary is `UNVERIFIED`. |
| Controller runtime | `PRESENT` | `src/kernel.ts`, `src/db.ts`, `src/trust.ts`, `src/grants.ts`, `src/process-runner.ts`, `src/pyat-client.ts` at controller HEAD `c51b74b` | Durable SQLite scheduling, grants, HMAC harness attestation, checkout/process custody. Reusable scheduling/receipt machinery. |
| Real controller loop receipt | `PRESENT` | `MAINMAC/REAL_CLOSED_LOOP_RECEIPT.json`, blob `0b203d08741dff2c2df0f5e5c4a8fec93291f7bc` | Worker, reviewer and HQ effects `SUCCEEDED`; status `ACCEPTED_SCOPED`; candidate `9560860b...`. `isolation` remains `UNPROVEN`. This proves scheduling/receipts, not protected capture. |
| Budget/refusal receipt | `PRESENT` | `MAINMAC/REAL_BUDGET_REFUSAL.json`, blob `cce185144779ec9dd6336402b86160ab26f92f8c` | Later call held with `ONE_JOB_BUDGET_EXHAUSTED`, `generating_calls: 0`, effects unchanged. |
| Real native-owner interfaces | `PRESENT` in-process | `rawlsing_next/pre553_c11_ingest.py` blob `37cd35fa2e3420a3eea272a2902e96ab9ba38aba`; `rawlsing_next/pre553_c11_repository.py` blob `67c6eb6494522cd11aab1b93d0e73f9cef6036f3` | `ingest_c11_source_release(candidate, repository)`, `validate_c11_source_release(candidate)`, and `C11Repository.resolve_release_exact(ref)` are real callables. They are not a separately pinned protected runtime. |
| R09 supervisor/verifier | `PRESENT` but same-interpreter | candidate `77f8b420...`, `CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py` blob `7af149e9d0e9cb2bc85c31d370145a86abf078b8` | Child executes entrypoint/imports; parent reads child-authored `observation.json` and HMAC-seals it. Source exclusions include `LOCAL_SUBPROCESS_NOT_A_HOSTILE_CODE_SANDBOX` and `SAME_UID_CAN_REWRITE_VERIFIER_OR_RUNTIME`. |
| External issuer/CI/VM | `UNVERIFIED` | not observed; not inspected | No claim of absence. No existing external admission channel was located. |

## The three required questions

### 1. Can a candidate be prevented from reading/writing protected broker runtime and secrets, including same-user process access?

**Not satisfied.** All observed processes, keys and worktrees belong to uid 501.
The shared runtime is `0700 matthewsmith:staff`; `harness.key`, `grant.key` and
`trust.json` are `0600 matthewsmith:staff`; `controller.sqlite` is
`0600 matthewsmith:staff`. Owner-only DAC does not exclude another process
running as the same owner. No dedicated broker UID, service principal, VM,
container or process-access exclusion is configured. The controller's
`sandbox-exec` probe does check selected file-read/write and fake-credential
denials (`reports/SANDBOX_PROBE.json`), but it was not applied to runtime
workers, it does not test same-UID process access, and the profile in
`src/sandbox.ts` allows `process*` and `mach-lookup`. The current
`pyat-client.ts` containment object is explicitly
`PYAT_R60_LOCAL_TEST_UNPROVEN` / `NOT_ATTESTED` / `isolation: UNPROVEN`.

### 2. Is there a separately pinned existing native-owner runtime with real callable interfaces?

**Callables exist; a separately pinned protected runtime does not.** The C11
owner modules are genuine Python interfaces in the repository, and the R09 V2
review records a real C11 ingest/repository positive through them. But the R09
candidate invokes them from the candidate-controlled child interpreter
(`tests/universal_runner/native_c11_entry.py` blob
`537f5c529d1966464d949e914f40f1b160053aad`), whose result and loaded-source
records are written by that child. There is no broker-owned code root, no
independently pinned owner commit separate from candidate-selected changes, and
no broker process that executes the owner itself.

### 3. Is there a supported request/receipt channel with external issuer admission?

**Not satisfied.** The controller verifies signed grants and harness
attestations, but the private keys are local files readable by the same uid and
the verifier runs in the same trust domain. R09's `TrustRoot` is
caller-constructed and parent-held; the independent review's P5 probe accepted
a self-root. The R09 receipt path is: child writes `observation.json`, parent
reads it, parent HMAC-seals the child-authored payload. That authenticates that
the parent sealed a claim, not that the broker observed a real owner execution.
There is no broker-owned request parser, declarative operation allowlist,
broker-authored receipt, or externally pinned issuer admission service.

## Why mere availability is insufficient

The independent review at `25510c8d...` established the central point. P1
rewrites `json.dump` in the subject interpreter and reports actual value `41`
as `42`; P2 compiles substituted source with the benign import digest and
reports `42` while the loaded code returns `41`. Both were accepted as
`LOCAL_NATIVE_VERIFIED`. Those are ordinary in-process Python interfaces, not a
private parent runtime.

Putting the same Python wrapper in a container or under `sandbox-exec` does not
repair this: the candidate and the instrumentation would still share the
interpreter. Same-UID file permissions also do not isolate the candidate from
the controller keys, worktrees or verifier. The required separation is a
different protection domain that does not execute candidate code in the broker
interpreter.

## Exact missing primitive

A **separately protected native-owner execution broker** with:

1. A protected broker principal and code/key root outside candidate read/write
   access, including same-UID process access.
2. A separately pinned approved native-owner runtime. The broker, not the
   candidate, resolves and imports the owner code and exact inputs.
3. A declarative request channel that accepts only validated operation
   identities and exact bound inputs; candidate-supplied call names, code,
   digests and result objects remain untrusted.
4. A broker-authored, issuer-authenticated receipt over the broker's own
   captured return object, with exact owner-code, input, policy, `K`, run,
   nonce and sequence bindings.
5. An independent verifier with an externally pinned issuer identity/public
   key, exact expected results, and a real same-request consumer reference.
6. Atomic nonce/cold-replay handling and typed malformed-input refusal
   preserved.

The broker must prove only broker invocation. It must not be described as
observing arbitrary internal candidate calls. If that stronger claim is ever
required, an independently controlled runtime/instrumentation mechanism is a
separate qualification.

## Competent owner

- **Host/platform administrator** for the protection domain: a disposable
  macOS VM or a dedicated non-admin service UID, filesystem ownership/ACLs,
  process isolation and a local socket. The current host has no installed
  container/VM CLI; that is an observed gap, not a claim that no external
  facility exists.
- **R09/CI engineering** for the broker protocol, pinned owner loading,
  receipt/ledger implementation and verifier.
- **Repository administrator** for the pinned owner code root and any
  protected-CI integration. Protected-CI deployment is a separate grant and
  remains out of scope.

## Minimum specific permission and smallest disposable qualification

**Minimum permission requested:** host-administrator authorization to create
one disposable environment (preferably a disposable macOS VM; alternatively one
dedicated non-admin `r61-broker` UID on a disposable host) with two principals;
repository-administrator permission to place the approved owner code at a
read-only, non-candidate-writable pinned path; and authority to create an
Ed25519 receipt key in the broker/issuer domain and pin its public key in the
verifier. No production credentials, provider changes, protected-CI
deployment or live worker dispatch.

**Smallest disposable qualification:**

1. **Principals.** Candidate principal runs only candidate code and its
   worktree. Broker principal owns `/opt/r61-broker` (`0700`), the pinned owner
   snapshot (`0500`/read-only), `issuer.key` (`0600`), the durable nonce
   ledger and the Unix socket (`0660`). The broker checks peer credentials and
   accepts only the candidate UID.
2. **Owner pin.** Freeze the exact C11 owner code commit/tree/blobs
   (`rawlsing_next/pre553_c11_ingest.py`,
   `pre553_c11_repository.py`, and their existing imports) in the broker root.
   The candidate cannot modify that root. The broker loads only from it; no
   candidate `PYTHONPATH`, cwd, module shadow or entrypoint is used.
3. **Request.** Accept only `R61_R09_BROKER_REQUEST@1` with a bounded typed
   schema: `operation` in `{C11_INGEST_SOURCE_RELEASE,
   C11_RESOLVE_RELEASE_EXACT}`, candidate commit, pinned owner commit/tree,
   input payload digest, policy digest, `K`, run id, one-shot nonce, monotonic
   sequence and exact consumer ref. Reject unknown keys, oversized values,
   caller-supplied call names/code/digests and malformed types with named
   refusals.
4. **Execution and receipt.** The broker independently resolves the pinned
   input and owner code, calls `ingest_c11_source_release(candidate,
   C11Repository())` or `C11Repository.resolve_release_exact(ref)`, captures
   the returned object itself, canonicalizes it, and emits
   `R61_R09_BROKER_RECEIPT@1` signed by `issuer.key` with receipt id,
   request binding, owner code identity, input/policy/`K`/run/nonce/sequence,
   result and previous-receipt digest. The candidate never receives the key or
   broker code and cannot author the receipt.
5. **Verification.** A separate verifier has the pinned issuer public key and
   owner commit/tree. It checks signature, exact bindings, atomic nonce/cold
   replay, independent expected result, and the real same-request consumer
   resolution. It does not accept candidate receipts, bare mappings, caller
   roots or self-reported digests.
6. **Qualification cases.** Run one positive C11 ingest/repository case with an
   independently computed expected result; then P1 (`json.dump` forgery), P2
   (loader/substituted-source forgery), wrong owner code/commit/tree, wrong
   input/policy/`K`/issuer, wrong nonce/sequence, cold replay, candidate key
   read/write attempts, and D7 malformed typed input. Require every forgery and
   wrong binding to refuse. Mutate the consumer assertion, show failure, restore
   and re-pass. Confirm the candidate cannot write trusted code or obtain
   signing material.
7. **Acceptance.** Only exact broker receipts for exact requests are accepted;
   no candidate-authored observation is accepted; no claim is made that broker
   execution proves arbitrary internal candidate calls. The environment is
   disposable and sourcefree TEST_ONLY.

## Scope retention

Independent capture and generic promotion remain `HOLD`; protected deployment
remains separately held. The accepted C11 positive and prior verifier/ledger
controls remain useful scoped assets. All prior returns are immutable. This
return makes no adoption, production, source/science, original35/1890,
global F6/F7/F8, N11/N12 or Sorok claim. The original 35/1,890/global F6/F7/F8
and Z UNRESOLVED 16 denominators are unchanged.

## Artifacts

- `00_RETURN.md` — this report.
- `FACILITY_INVENTORY.json` — machine-readable observations and gap.
- `SOURCE_REFS.json` — exact commits/trees/blobs.
- `COMMANDS_AND_EXITS.json` — exact commands, exits and bounded output hashes.
- `proof_witness.json` — evidence index and non-claims.
- `REMOTE_VERIFICATION.md` — startup and final remote verification method.
- `RESUME.md` — exact continuation state.
- `collect_commands.py` — reproducible command collector.
- `manifest.json` — SHA256/size manifest, self-excluded.
