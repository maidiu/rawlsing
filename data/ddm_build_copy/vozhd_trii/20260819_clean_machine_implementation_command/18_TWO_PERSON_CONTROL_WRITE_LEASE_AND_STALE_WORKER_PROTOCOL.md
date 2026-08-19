# 18 — TWO-PERSON CONTROL, WRITE LEASES & STALE-WORKER INVALIDATION

## 1. Purpose

Fast parallel construction creates two characteristic failure modes:

1. one worker silently changes shared reality while siblings continue against the old one;
2. multiple workers make locally reasonable edits to the same shared surface and integration becomes conflict resolution by accident.

This protocol forbids both.

## 2. Shared-contract two-person rule

No C1/C2 shared-contract change becomes authoritative from the act of one worker, one domain Vozhd, or one General Staff owner alone.

Minimum acceptance:

- owning General Staff authority signs semantic correctness;
- G6 signs dependency/synchronization completeness.

For C2, the existing wider approvals in `04_INTERFACE_DAG_AND_CHANGE_CONTROL.md` remain required in addition to these two mandatory signatures.

Inspectorate may veto integration after approval if hostile review exposes drift or incompleteness.

C3 remains Campaign-Vozhd/higher-authority territory.

## 3. Shared write lease

Every shared canonical file/schema/registry/migration surface has one active write lease at a time.

The COP records:

- resource path/registry ID;
- current owner;
- lease purpose;
- base SHA/version;
- affected interfaces;
- start state;
- release receipt.

Workers may read shared surfaces freely under authority. They may not concurrently mutate the same shared semantic resource from separate branches.

A lease is semantic ownership of the edit transaction, not semantic ownership of the underlying concept.

## 4. Worker-local write surfaces

Rabochii implementation branches should default to worker-owned paths/modules/tests.

If a task genuinely requires a shared file edit, the worker must possess an explicit write lease in its order. Otherwise it returns a change request or integration patch request rather than modifying the file.

## 5. Stale-worker invalidation

When any frozen dependency changes, G6 determines the transitive affected-worker set from the DAG/interface registry.

Affected workers enter:

`STALE_DEPENDENCY__NO_CROSS_INTERFACE_PROGRESS`

They may preserve local work but may not:

- emit a final conformant result;
- cross the changed interface;
- merge/integrate;
- claim sibling compatibility.

To resume, the worker must issue a `DEPENDENCY_REFRESH_RECEIPT` binding:

- old dependency version/hash;
- new dependency version/hash;
- code/tests reviewed;
- semantic diff impact;
- rebase/compatibility action;
- hostile fixture rerun IDs;
- parent Vozhd acceptance.

## 6. Dependency epochs

The Campaign Vozhd/G6 may group compatible shared contracts into a numbered `COMMAND_DEPENDENCY_EPOCH`.

Every worker order records the epoch plus exact individual hashes.

Epochs are convenience only; exact hashes remain authority.

A worker from an older epoch cannot be integrated merely because Git merges cleanly.

## 7. Interface-change broadcast

Every accepted shared change triggers one machine-readable broadcast containing:

- change ID/class;
- old/new contract IDs/hashes;
- exact semantic change;
- affected producer/consumer set;
- stale worker set;
- required fixture reruns;
- required migration/replay checks;
- next legal actions.

No change is considered operationally complete until G6 proves the broadcast reached every affected command or records an explicit blocked/stopped unit.

## 8. Concurrent discovery, serialized legislation

Multiple workers may independently investigate a shared problem and propose competing contract changes.

Only the authorized owning staff process may legislate the shared result.

Therefore:

`PARALLEL_RECONNAISSANCE_ALLOWED`

but

`PARALLEL_SHARED_CONTRACT_MUTATION_FORBIDDEN`.

## 9. Merge-conflict law

A textual Git merge conflict on a shared semantic surface is presumptive evidence of coordination failure.

Integration Command must not solve it by choosing lines manually unless the owning authority has already issued one canonical post-conflict contract version.

Semantic conflict is resolved in authority space first, then code is reconciled.

## 10. Emergency stop

Any Vozhd, G6, Inspectorate, or Integration Command may issue:

`SEAM_STOP__DEPENDENCY_INCONSISTENCY`

when workers are observed implementing incompatible frozen assumptions.

The stop applies only to the affected seam/transitive consumers unless whole-machine integrity requires broader suspension.

Speed is restored by narrowing the stop, not by ignoring it.
