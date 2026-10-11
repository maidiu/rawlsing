# PYAT HQ280 PV3 B01CR — Independent durable write-ahead checkpoint crash/recovery hostile

**TERMINAL:** `HQ280_PV3_B01CR_INDEPENDENT_DURABLE_CHECKPOINT_RUNTIME_HOSTILE_RETURNED__NONISSUING__GITHUB_PUSHED`
**VERDICT:** `DURABILITY_CORE_PASSES_REAL_CRASH_WINDOWS__ONE_EXACT_DEFECT__CALLER_ASSERTED_IDEMPOTENCE_ACCEPTED_AS_PROOF`
**Branch:** `agent/reviewer-pyat-hq280-pv3-b01cr-durable-hostile-r1` @ `7763ee38cadde298758ba7324a8d0e62693ba0cd`
**Candidate:** B01C `88a2b4c1916c73d30cae4c2ffe48d083eb2e0667` — module blob `57b8cc426eaf073213217a7ee7179b9f9cacb3d0`, test blob `62e1273c4e8c88a2940c2ca60b8f3c0d06fd4f31`, **both verified exact**.

## 1. Actual runtime

| run | result |
|---|---|
| B01C candidate suite | **35 passed**, exit 0 (first attempt showed 6 failures that were purely a sparse-checkout artifact — B01C's `repro/` worker script was not materialized; materialising it restored 35/35. Recorded honestly as terrain, not defect.) |
| `rabochii_execution_protocol` suite | see `repro/protocol_suite.log` |
| my own crash hostiles | **6 cases**, exit 0 — real subprocesses, one real `SIGKILL` |

Python 3.11.3, macOS 13.7.8 x86_64.

## 2. THE ANSWER TO THE CENTRAL ADVERSARIAL QUESTION

> **Can a crash after an external effect but before COMMIT cause silent duplicate execution?**

**YES — if the caller names the unit key.** The accepted candidate at `plan_recovery` decides:

```python
# START intent without a durable COMMIT: side effect may have landed.
if unit_key in proofs:                       # <-- ONLY the key's PRESENCE is tested
    dispositions[unit_key] = RecoveryDisposition.RERUN_SAFE
else:
    dispositions[unit_key] = RecoveryDisposition.UNKNOWN_OUTCOME
```

`proofs[unit_key]` is **never read**. There is no owner check, no issuer, no signature, no schema, no competence verification. `idempotence_proof={"u1": ""}` — or `{"u1": "definitely idempotent, trust me"}` — flips a genuinely unknown outcome to `RERUN_SAFE` and proposes the unit for **rerun over a side effect that may already have landed**.

This directly contradicts the module's own contract comment that `RERUN_SAFE` is "reachable ONLY with a **declared** idempotence proof" and the commission's rule: *do not accept caller-asserted idempotence as independently proven idempotence*. **Caller assertion is currently the whole of the proof.**

**Required fix:** `RERUN_SAFE` must require an **owner-verified** idempotence credential (exact ref + issuer + verified signature/schema) for that exact unit key; `UNKNOWN_OUTCOME` must remain a **HOLD** otherwise. Until then this is an exact defect, not a residual.

## 3. What genuinely PASSES (real crash windows, real processes)

| id | hostile | observed | verdict |
|---|---|---|---|
| **W1** | **real `SIGKILL` mid atomic write** (tmp→fsync→replace→dir fsync) | `returncode -9`; final path either absent or fully parseable; **no torn or partial file ever visible at the final path** | **PASS** — disk atomicity holds under a genuine crash |
| W2 | torn/truncated mutation (truncate to 50%) | parse refused | PASS |
| W3 | content tamper vs returned digest | digest differs → detectable | PASS |
| **W4** | parent-directory fsync path | `os.fsync(handle.fileno())` present; `_fsync_dir(path.parent)` after `os.replace`; dir opened `O_RDONLY` | **PASS** — the candidate genuinely closes the missing-dir-fsync gap it claims to close |
| **W5** | process locking, two real processes | second writer **refused** (`CheckpointLockError`) while held; lock **released** after the holder was `SIGKILL`ed | PASS — no stale-lock deadlock observed |
| W6 | forged caller idempotence proof | `RERUN_SAFE`, proof unverified | **FAIL ← the finding** |

## 4. Structural credit

The candidate's write-ahead model is **soundly shaped**: `UnitRecord.state ∈ {INTENT, COMMITTED}` means a durable **intent** is written before the side effect and a durable **COMMIT** after, so a crash between them *is representable* as an unknown outcome. `RecoveryDisposition.UNKNOWN_OUTCOME` exists and is documented as a HOLD. The defect is not the model; it is that the **upgrade path out of the hold is unguarded**.

## 5. Grading and exact holds

**Narrow positive (credited):** B01C is a **source-free durable checkpoint mechanism** whose atomicity, dir-fsync, tamper detection and lock behaviour all survive genuine process kills. **Narrow scope:** this is *internal source-free pure execution* durability; it does **not** establish durably-idempotent **external non-idempotent** side effects.

**Exact holds (separate, none resolved here):**
1. `RERUN_SAFE` requires a **caller-supplied key presence only** → **`CALLER_ASSERTED_IDEMPOTENCE_ACCEPTED_AS_PROOF`** (must fail closed to HELD).
2. `UNKNOWN_OUTCOME` is **HELD** — and must remain held until an owner-competent mechanism establishes safe rerun. **Not** established.
3. No **REAL_EXECUTION** grant; B01 F01/F02 and `rabochii_execution_protocol.py` requirements were inspected, not broadened.
4. **No NFS/distributed claim** — `flock` durability and dir-fsync semantics are filesystem/network dependent; on NFS this design is **unsupported** as reviewed.
5. Multiplicity, attempt-index redo-on-failure and stale-checkpoint competition were **not** exhaustively exercised (bounded run); they remain **UNKNOWN** here rather than asserted.

**Terminal:** `HQ280_PV3_B01CR_INDEPENDENT_DURABLE_CHECKPOINT_RUNTIME_HOSTILE_RETURNED__NONISSUING__GITHUB_PUSHED`.
