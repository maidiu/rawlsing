# R61-R09V R2 ranked reproducible defects

Verdict: **REVISE** for the local independent-capture promise (`HOLD` for that
promise). The candidate is not repaired or adopted. All probes are in
`probes/independent_probes_r2.py`; raw outcomes in `evidence/probes_r2.json`;
the failing controls are in `evidence/reviewer_probes_junit.xml`. Candidate
files were never edited (`git diff --exit-code` = 0).

## D1-R2 (critical) — The parent HMAC-seals a child-authored observation

**Minimal input.** A committed support module `native_fixture.py` contains
normal `add`/`double` functions and executes at import time:

```python
import json
_real_dump = json.dump
def _forged_dump(obj, handle, **kwargs):
    forged = dict(obj)
    forged["result"] = {"label": "baseline", "value": 42}
    _real_dump(forged, handle, **kwargs)
json.dump = _forged_dump
```

The committed entrypoint computes `double(add(20, 1)) = 41`, writes a marker
containing `41`, and sets `RESULT = {"label": "baseline", "value": 41}`. The
externally frozen expectation is `42`.

**Observed.** `LocalNativeSupervisor.observe()` returns
`LOCAL_NATIVE_VERIFIED`, `reasons=[]`. The marker proves the actual returned
value was `41`; the parent-sealed observation reports `42`.

**Required.** The accepted result must come from an observation the subject
cannot author or mutate. A parent HMAC over a child-authored JSON protocol does
not prove independent observation. The subject legitimately controls its own
interpreter (`json`, frames, import hooks); these are ordinary subject-accessible
interfaces, not the excluded private parent runtime.

**Contract.** R09V R2 primary job 3-4; R09 acceptance "authenticated event/value
artifacts"; R09 "untrusted authored hashes/booleans/trace names are not
observations"; R2 commission D1: "A parentHMAC over a subject-authored
observationfile/protocol is not independentcapture. Stopping atexit alone must
not be mistaken for removing subjectcontrol."

**Mechanism.** `WRAPPER_SOURCE` builds `payload` from child locals
(`result`, `events`, `loaded_sources`, `import_events`); the parent reads that
JSON at `LocalNativeSupervisor.observe` lines 511-598 and re-seals it. `os._exit`
at line 354 only prevents post-write `atexit` handlers; it does not prevent
in-process monkeypatching or frame mutation.

## D4-R2 (critical/high) — Loaded-byte custody is a child self-report

**Minimal input.** The committed benign `native_fixture.py` has digest
`5205ce76...ff106` (tree blob). The committed entrypoint inserts its own
meta-path finder that intercepts `native_fixture`, compiles malicious source
from a string with `filename=<target_file>`, and executes it (`double` returns
`value*2-1`). It then injects into the wrapper's own `loaded_sources` dict:

```python
loaded_sources["native_fixture"] = {
    "path": TARGET, "loaded_sha256": BENIGN_TREE_DIGEST}
```

It reports `RESULT = 42` while the actual loaded code returns `41` (marker).

**Observed.** `LOCAL_NATIVE_VERIFIED`, `reasons=[]`. The observation reports
`loaded_sha256 == tree_sha256 == 5205ce76...`, `tree_bound=true`, while the
loaded executable code was the malicious string.

**Required.** The parent must independently capture the bytes actually loaded
and executed, or execute only parent-read bytes through a loader the subject
cannot replace or lie about. A child-reported `loaded_sources` digest, even when
the parent compares it to a git blob, does not establish which bytes ran.

**Contract.** R09V R2 job 3-4; R09 "changed runtime import"; R2 commission
"actualexecutedbytes"; prior D4; TESTS T11. The parent currently compares the
child-supplied digest to `_git_blob`, so a child that reports the tree digest
passes while running different bytes.

## D7-R2 (low/medium) — Non-serializable expectation still crashes

**Minimal input.** An authentic observation from a legitimate run plus an
expectation object with `expected_result = {"x": {1, 2}}` (a Python set).

**Observed.** `TypeError: Object of type set is not JSON serializable` from
`typed_digest(expectation.expected_result)` at the unguarded result comparison
(verifier lines 799-803). No typed `REFUSE_NATIVE_QUALIFICATION` decision.

**Required.** A named typed refusal, as with
`EXPECTATION_RESULT_NOT_SERIALIZABLE`. The author's
`test_malformed_typed_inputs_fail_closed_without_crashing` first mutates the
observation; that mutation fails the HMAC and returns early, so the crash path
is never exercised with an authentic observation.

**Contract.** R09V R2 job 3 "malformed/typed inputs"; prior D7.

## Trust-root admission (boundary finding, not the decisive defect)

Any caller can construct `verify.TrustRoot(issuer, key)` and use it end-to-end;
the verifier has no external anchor for which trust root is admissible. Probe
`P5_self_root_caller_accepted` builds an independent attacker root, an attacker
supervisor, an attacker expectation with the same fingerprint, and is accepted.

This is acceptable **only** when the caller and key are genuinely outside
subject control and an external authority pins the root. The docstring states
that precondition but the code does not enforce it. It does not, by itself,
rescue D1/D4 because the parent still seals subject-authored content.

## Controls that genuinely pass in R2

- `P0_legit_baseline` and `P13_actual_c11_positive`: accepted; the C11 positive
  matches an independent plain-process reference.
- `P3_bare_mapping`: `UNTRUSTED_OBSERVATION`.
- `P4_fake_issuer_rewrite`: `OBSERVATION_AUTHENTICATION_FAILED`.
- `P6_nondurable_ledger`: `NONCE_LEDGER_NOT_DURABLE`.
- `P7_cold_replay_first` / `P8_cold_replay_second`: accept once / `NONCE_REPLAYED`.
- `P9_concurrent_nonce`: `CLAIMED` + `REPLAYED`.
- `P11_non_serializable_observation` (mutated HMAC): typed refusal.
- `P12_out_of_tree`: `SUPERVISOR_REFUSED:ENTRYPOINT_OUTSIDE_CANDIDATE_TREE`.
- `P14_c11_wrong_expectation`: `RESULT_MISMATCH`.
- Targeted mutant: intact refuses `RESULT_MISMATCH`; disposable mutant that
  disables only that assertion accepts. Candidate verifier SHA256 is unchanged.

## Capability not reached (scope)

Independent return-value capture; independent loaded-byte custody against a
lying subject; authenticated external trust-root admission; protected CI
required-check enforcement; repository-admin attestation; OS sandbox; external
key service; original source/science; original35/1890; N11/N12; deployed
enforcement. No existing downstream B49/G50/U43/I03/I05/Batch/E04 consumer was
executed; the actual positive is the committed C11 ingest/repository owner on a
synthetic sourcefree fixture.
