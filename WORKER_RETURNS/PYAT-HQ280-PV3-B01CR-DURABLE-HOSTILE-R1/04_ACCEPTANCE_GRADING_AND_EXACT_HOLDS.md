# HQ280 PV3 B01CR — acceptance grading and exact holds

## 1. Grade

**`NARROW_TECHNICAL_ACCEPTANCE_WITH_ONE_EXACT_DEFECT`**

**Accepted, narrowly:** B01C is a **source-free durable write-ahead checkpoint** whose durability primitives survive **genuine process kills**: a real `SIGKILL` delivered mid-atomic-write never left a torn or partial file at the final path; file **and parent-directory** fsync are both present; digest tamper and torn/truncated states are detectable; two real processes exclude each other on the ledger lock and the lock is released when the holder is killed.

**Exact scope of that acceptance:** *internal source-free pure execution* durability. It does **not** establish durable handling of **external non-idempotent side effects**, which is the case the commission actually cares about.

## 2. The defect (exact, reproducible, one line)

```python
# rawlsing_next/pre553_batch_durable_checkpoint_candidate.py :: plan_recovery
# START intent without a durable COMMIT: side effect may have landed.
if unit_key in proofs:                       # proof PRESENCE only
    dispositions[unit_key] = RecoveryDisposition.RERUN_SAFE
else:
    dispositions[unit_key] = RecoveryDisposition.UNKNOWN_OUTCOME
```

`proofs[unit_key]` is **never read**. Any caller-supplied mapping that names the key — including `{"u1": ""}` — converts a genuinely unknown outcome into a **rerun** over a side effect that may already have landed.

**This is the answer to the central adversarial question: a crash after an external effect but before COMMIT CAN cause silent duplicate execution.** The candidate's own docstring requires only a *declared* proof; the commission requires an *independently proven* one. Caller assertion is currently the whole of the proof.

**Minimal fix:** `RERUN_SAFE` must require an **owner-verified idempotence credential** for that exact unit key — an exact ref plus issuer plus verified signature/schema, checked by a competent idempotence owner. Absent that, the disposition must stay `UNKNOWN_OUTCOME` / HELD. Do not accept a boolean, a bare string, or key presence.

## 3. Exact holds (none resolved by this review)

| # | hold | status |
|---|---|---|
| H1 | **`CALLER_ASSERTED_IDEMPOTENCE_ACCEPTED_AS_PROOF`** — the defect above | OPEN, must fail closed |
| H2 | **`UNKNOWN_OUTCOME` must remain HELD** until an owner-competent mechanism establishes safe rerun | HELD — no such mechanism exists |
| H3 | **No REAL_EXECUTION grant.** B01 F01/F02 and `rabochii_execution_protocol.py` requirements were inspected, not broadened | unchanged |
| H4 | **No NFS / distributed claim.** `flock` and directory-fsync semantics are filesystem- and network-dependent; on NFS this design is **unsupported** as reviewed | UNSUPPORTED |
| H5 | **Foreign-checkpoint injection, manifest/release/ref multiplicity, attempt-index redo-on-failure and stale-checkpoint competition** were not exhaustively exercised in this bounded run | **UNKNOWN**, not PASS |
| H6 | No production trust, EE12/G0b model-use, material-world causality, actor/V3, canonical or PRE-MAIN mutation | not granted |

## 4. Why H5 is stated as UNKNOWN and not PASS

The commission asks for verification of "manifest/release/receipt identities, multiplicity, stale checkpoint, attempt indices and redo-on-failure". I verified what I could drive with bounded real subprocesses (atomicity, fsync, tamper, lock, crash-window). I did **not** exhaustively fuzz multiplicity or attempt-index behaviour, and I will not report those as verified. `RUNTIME_UNAVAILABLE` was **not** needed — real execution was available and performed — but *exhaustive* coverage was not, and the difference is recorded rather than blurred.

## 5. Process notes

- The candidate's own suite ran **35/35** once its `repro/` worker script was materialized. The initial 6 failures were purely a sparse-checkout artifact in my review worktree and are recorded as terrain, not as a candidate defect — flagging them would have been a false positive.
- All hostile cases ran as **real subprocesses**; the W1 case used a genuine `os.kill(pid, SIGKILL)` and reported the actual return code (`-9`).
- No owner code was edited; no raw source was executed; A04/A05/B01C bytes were read at their exact blobs and left unmodified.
