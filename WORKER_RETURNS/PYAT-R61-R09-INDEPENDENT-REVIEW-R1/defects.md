# R61-R09V ranked reproducible defects

Verdict: **REVISE** for the local promised guarantee. The candidate is not
repaired or adopted here. All probes are in
`probes/independent_probes.py`; raw outcomes in
`evidence/probes_candidate.json`; failing controls in
`evidence/reviewer_probes_junit.xml`. Candidate files were never edited.

## D1 (critical) — The untrusted subject writes the observation that verify() accepts

Minimal input: import a target module that registers an `atexit` handler, reads
the wrapper config path from `sys.argv[1]`, rewrites `observation_path` with
`result = {"label":"baseline","value":42}`, and restores its own file to the
expected bytes. The entrypoint is benign and pinned. Probe `P8`.

Observed: the **genuine** `LocalNativeSupervisor.observe()` path returned
`LOCAL_NATIVE_VERIFIED` with no reasons. The marker recorded the pre-forge
wrapper result `{"label":"baseline","value":41}`; the reported result was 42.
The mutated double actually ran, the file was restored, and the parent rehashed
the restored bytes.

Required: the trusted supervisor must own observation capture outside the
subject's address space / file access. The child must not be able to write,
replace, or edit the observation artifact after capture. A subject-authored or
subject-overwritten observation must refuse.

Contract: R09V primary job 3–4; R09 "authenticated event/value artifacts" and
"untrusted authored hashes/booleans/trace names are *not* observations";
INPUTS/OVERLAYS R09 "actual native calls and returned refs".

Mechanism: `WRAPPER_SOURCE` lines 191–200 writes the payload inside the child;
`LocalNativeSupervisor.observe` lines 276–283 trusts that file. The author return
line 28 says the supervisor "captures the returned result" independently; it
does not.

## D2 (critical) — verify() accepts an unauthenticated candidate-authored mapping; "fake issuer" is only a string comparison

Minimal input: build a plain dict with the expected schema, issuer, commit,
tree, policy, run id, nonce, entrypoint digest, fabricated `process.exit_code=0`,
fabricated events/imports/result, and pass it to `verify_observation` without
launching any process. Probe `P1`; the entrypoint marker file remains absent.
Also take a genuine observation issued as `candidate-issued-supervisor`, rewrite
`observation["issuer"] = "trusted-supervisor-A"`, and verify. Probe `P2`.

Observed: both decisions are `LOCAL_NATIVE_VERIFIED` with `reasons=[]`.

Required: observation provenance and issuer identity must be authenticated
(opaque supervisor handle, MAC/signature with a key outside candidate control,
or direct verifier invocation of the supervisor). A self-asserted issuer string
and a caller-constructed dict are not independent facts. The `candidate_evidence`
argument is not a substitute: it is optional and only rejects a non-empty extra
argument; omitting it accepts the forged observation.

Contract: R09V primary job 3 ("challenge whether candidate can forge observations
accepted by verify()"; "fake issuer"); R09 acceptance "forged events/self-pin/
wrong commit/replayed run/missing owner/shape relabel all rejected"; R09V "Do not
permit arbitrary author-supplied expected outcomes to be called independent
supervisor facts."

## D3 (high) — Claimed commit/tree are not bound to executed bytes

Minimal input: run the genuine supervisor on entrypoint/support files created in
the reviewer's temporary directory (not in the repository), with
`candidate_commit`/`candidate_tree` resolving to the repository HEAD. Probe `P3`.

Observed: `LOCAL_NATIVE_VERIFIED`; `git cat-file -e HEAD:<path>` is false for
both executed files. `observation["target_file"]["sha256"]` is recorded but
never compared with the expectation or the claimed tree.

Required: executed entrypoint and imported module bytes must be proven to be the
blobs in the claimed candidate tree (or execution must be restricted to
repository paths bound to that commit). Merely resolving a tree from any commit
must not label unrelated files as that candidate.

Contract: R09V primary job 1 and 3 ("exact candidate/policy/tree/run/nonce
bindings"; "merely resolving git HEAD without binding executed bytes must not
qualify a changed candidate"); NODE R09 "Exact candidate digest plus externally
pinned policy".

## D4 (high) — Import digests are rehashed after child exit, not captured from loaded bytes

Minimal input: a mutated support module that writes a marker at import, runs
`double(value) = value*2 - 1`, and at `atexit` restores the expected original
source. Expectation pins the original digest. Probe `P4`.

Observed: `LOCAL_NATIVE_VERIFIED`; marker exists; the mutated code was loaded;
the reported import digest equals the expected original digest because the
parent hashed the restored file after the child exited.

Required: hash the bytes actually read/executed (read once, hash, execute the
same bytes; or child reports a load-time digest over the loaded bytes and the
parent verifies it). A self-restoring or path-replaced module must refuse.

Contract: R09V primary job 3 ("dirty import/path replacement and actual loaded
bytes"); R09 "changed runtime import"; TESTS T11. This is the same consumed-byte
custody principle later required by R04.byte.

## D5 (high) — Default CLI replay: same run accepted twice in cold processes

Minimal input: dump one genuine observation and one matching expectation to
files; run `universal_runner_verify.py --observation ... --expectation ...`
twice, with no `nonce_ledger_path`. Probe `P5`.

Observed: both cold processes exit 0 and print `LOCAL_NATIVE_VERIFIED`.

Required: a durable externally supplied one-shot nonce ledger must be mandatory
(or the supervisor must issue a single-use nonce bound to the process). Replay
must refuse by default, not only when an optional path is provided.

Contract: R09 acceptance "replayed run ... rejected"; R09V primary job 3
("wrong/stale/replayed run nonce including cold/concurrent use"); author test
only covers an explicitly supplied file ledger.

## D6 (medium) — Concurrent/duplicate ledger instances both accept the same nonce

Minimal input: construct two `NonceLedger(path)` objects before either consumes;
verify the same genuine observation with each. Probe `P6`.

Observed: both decisions `LOCAL_NATIVE_VERIFIED`; the second sees no replay.

Required: atomic cross-process check-and-insert (exclusive lock file, `fcntl`
lock, or atomic durable store), not a process-local `threading.Lock` plus a
load-once file snapshot.

Contract: R09V primary job 3 ("cold/concurrent use where relevant"); R09
acceptance "replayed run ... rejected."

## D7 (low) — Malformed typed result crashes instead of a typed refusal

Minimal input: otherwise valid observation with
`result = {"x": {1, 2}}` (a Python set). `evidence/malformed_result.json`.

Observed: `TypeError: Object of type set is not JSON serializable` from
`typed_digest`/`canonical_json`; no decision record.

Required: fail closed with a named refusal reason for non-serializable or
malformed typed inputs.

Contract: R09V primary job 3 ("malformed/typed inputs").

## Capability not reached (scope, not a ranked defect)

No existing repository native owner/consumer (C11, Route B, I03/I05, Batch, E04,
etc.) was imported or executed. The positive uses a synthetic temporary
`native_fixture`. That proves runner mechanics, not an actual owner/consumer
delta. Protected CI required-check installation, repository-admin attestation,
OS sandboxing, external key/issuer authority, original source/science, N11/N12,
and deployed enforcement are all NOT_REACHED and remain held.
