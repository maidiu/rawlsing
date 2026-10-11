# B01C — Owner and protocol contract

## 1. Accepted owners this candidate binds to (all UNMODIFIED)

| Owner | File | What the candidate uses |
|---|---|---|
| Batch unit identity | `pre553_batch_runner.BatchUnitSpec` | `unit_ref`, `release_refs`, `semantic_input_refs` as the durable unit key |
| Batch manifest | `pre553_batch_runner.BatchManifest` | `manifest_hash`, `manifest_ref` — the binding identity of every checkpoint |
| Execution receipt | `pre553_batch_runner.UnitExecutionReceipt` | `projection()` for persistence; the typed constructor for exact rehydration |
| Runner / resume | `pre553_batch_runner.BatchExecutionRunner` | `next_attempt_index()`, `pending_units()`, `run()`, and `prior_receipts=` for resume |
| Receipt admission | `pre553_batch_runner.record_receipt` | the owner's own contiguity and no-retry-after-complete law |
| Exact refs | `pre553_empirical_objects.ExactRef` | typed rehydration with full `kind/object_id/content_hash` verification |
| Hashing | `pre553_empirical_objects.semantic_hash` | intent hashing, reusing the accepted owner |
| Repository | `pre553_c11_repository.C11Repository` | only via the runner's exact release resolver |

**No owner is subclassed, wrapped, patched or replaced.** The candidate supplies
inputs (`prior_receipts`) and receives outputs (`UnitExecutionReceipt`).

## 2. The F-02 protocol contract, and why it is NOT relaxed

`rabochii_execution_protocol.py` requires, for `REAL_EXECUTION`:

```
checkpoint_state.mode == "WRITE_AHEAD"
checkpoint_state.volatile_result_pending  (boolean)
checkpoint_state.recompute_cost           (in RECOMPUTE_COSTS)
checkpoint_state.durable_checkpoint_ref   (null or nonempty string)
# and when volatile_result_pending is true:
#   next legal action must be PERSIST_CHECKPOINT
```

This candidate **satisfies that vocabulary** without editing the validator:

| Protocol token | Candidate realization |
|---|---|
| `mode == "WRITE_AHEAD"` | `UNIT_STATE_INTENT = "START_INTENT_WRITTEN"`, written **before** any owner side effect |
| `durable_checkpoint_ref` | `DurableCheckpoint.checkpoint_ref` — a real `ExactRef` whose `content_hash` is the SHA-256 of the complete checkpoint document |
| `volatile_result_pending` | `DurableCheckpointStore.save()` is atomic; a partially written checkpoint is never observable at the live path |

**Explicit non-actions:** the candidate does not import `rabochii_execution_protocol`,
does not call or modify `validate_court_spec`, does not weaken any validator, and
does not grant REAL_EXECUTION approval. Verified by
`test_accepted_owners_and_protocol_are_not_modified_by_this_candidate`.

## 3. The exact identity chain preserved

```
BatchManifest.manifest_hash  +  manifest_ref
        │
        ├── release_refs (every unit's exact C11LogicalRelease)
        ├── unit_keys    (every unit_ref.key)
        └── protocol_profile = DEVELOPMENT_SOURCE_FREE
                    │
                    ▼
        DurableCheckpoint.content_digest  ──►  checkpoint_ref (ExactRef)
                    │
                    ├── UnitRecord(state=START_INTENT_WRITTEN, intent_hash, …)
                    └── UnitRecord(state=COMMITTED, receipt_projection, receipt_hash)
                                    │
                                    ▼
                    UnitExecutionReceipt  (accepted owner type, digest-verified)
                                    │
                                    ▼
                    BatchExecutionRunner(prior_receipts=…)   [ACCEPTED OWNER]
```

A checkpoint is **refused** if its manifest hash, manifest ref, release refs,
unit set or protocol profile differs from the manifest it is offered against.

## 4. Durability contract (and the gap it closes)

Existing proven pattern, `ee_p2x_darwin_court_driver._atomic_write_bytes`:

```python
tmp = mkstemp(dir=parent)
write(data); flush(); os.fsync(fd)
os.replace(tmp, path)          # <-- no parent-directory fsync
```

`os.replace` is only **durable** once the containing directory entry is synced.
This candidate adds the missing step:

```python
os.replace(tmp, path)
_fsync_dir(path.parent)        # os.open(dir, O_RDONLY) + os.fsync(fd)
```

Atomicity and exclusivity come from the same file the EE-P2X court already
proves: temp file in the same directory, `fsync` before rename, `fcntl.flock`
for the exclusive writer.

## 5. Recovery contract

| Durable state | Disposition | Rerun permitted? |
|---|---|---|
| `COMMITTED`, receipt rehydrates and reproduces its digest | `ALREADY_COMMITTED` | no — owner forbids retry after complete |
| `START_INTENT_WRITTEN`, no idempotence proof | **`UNKNOWN_OUTCOME`** | **no — HELD** |
| `START_INTENT_WRITTEN`, caller-supplied idempotence proof | `RERUN_SAFE` | yes, explicitly justified |
| absent | `NEVER_STARTED` | yes |

## 6. Inherited, unchanged

B01's P17 — a rewritten adaptive checkpoint re-executes an *equal* work set and
reaches the *equal* terminal state but yields a **different** `checkpoint_ref`,
because checkpoint identity is sensitive to visit **order**. This candidate does
not alter adaptive checkpoint semantics, does not canonicalise visit order, and
does not claim identity convergence. Safety holds; determinism does not.