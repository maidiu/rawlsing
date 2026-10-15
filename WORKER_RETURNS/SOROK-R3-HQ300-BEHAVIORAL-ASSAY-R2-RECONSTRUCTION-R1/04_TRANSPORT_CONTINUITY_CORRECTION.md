# Post-return transport correction — v8 candidate

The sourcefree v6 return at `a7d2be9894bf92f81356adf14141136666e63bd1` reproduced its reported tests and complete mock sweeps, but did not prove active-journal continuity or capture-failure recovery. Its ledger assurance must be read at the tested re-entry grain, not as covering those missing boundaries. No independent R2 acceptance existed or is inferred.

Two newly executed actual-entrypoint probes expose the gaps:

1. Remove the journal after constructing a valid Runner and before its first call. V6 recreated it and issued **one inert mock dispatch**, contrary to the prewritten zero-dispatch contract. The failure was loss of a valid journal, not evidence of a real call or reset of the in-memory spend counter. `receipts/active_ledger_probe/` retains expectations, result and the resulting raw journal.
2. Inject a response-capture write failure after a mock response arrives. V7 could issue a second dispatch without a typed transport-error receipt. `receipts/unresolved_capture_probe/` retains the actual RED. This exposed a forbidden redraw path even though both calls remained inside the local mock budget.

V8 implements active regular-file identity, size, timestamp and exact-tail checks before every append; it never recreates a missing active journal. It reserves a persistent pending-attempt state before dispatch. Only successful capture or a specifically retryable TransportError clears that state. An unknown response/capture outcome holds the trial while open and after journal re-entry. Calls within one Runner are serialized so total-call/spend checks cannot race. These are bounded local-process guarantees, not hostile-host attestation or real-provider idempotency claims.

The 62-test v8 sourcefree suite passes, including the unchanged 23 RMB counterparts and new removal, truncation, inode replacement, metadata-preserving overwrite, append, symlink, retained-charge, concurrent-writer, capture-failure/re-entry and same-runner budget probes. The full frozen replay and raw audit also pass: 21,600 exact request/response pairs; original shallow-policy and budget/origin/belief falsifiers detected. `receipts/transport_repair_v8/result.json` additionally repeats both exact repair probes after the full run. No corpus fact, proposed lawful set or schedule was changed to make the tests pass. Original R1, all earlier freezes and failed probes remain preserved.

Active freeze: `freezes/v8.json`, SHA-256 `58aa322c132eca6b47cb0be4d0eb04aeebf410b099e94511927e00e40c46d0ce`. V6 and v7 source snapshots are in the corresponding `archives/` tarballs and are verified against their original manifests.

The independent I2 review remains an external requirement. The author does not certify this correction scientifically accepted, issue a model-use grant, or call a real model/actor. HQ's next review must use the superseding exact returned candidate and inspect both retained RED probes.
