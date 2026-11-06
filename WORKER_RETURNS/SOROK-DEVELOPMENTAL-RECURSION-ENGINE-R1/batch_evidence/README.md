# Batch engine evidence index

Scope: `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1` only. No production, P2 adapter or model-coordinator file was modified.

- `TEST_ENGINE.log` — exact `pytest -q tests/test_engine.py` result: 42 passed.
- `TEST_COLLECTION.txt` — collected test inventory.
- `HARD_CRASH_RECOVERY.log` — a real child process exits 17 after the owner receipt; the parent observes `RUNNING` + `RESERVED` + no recorded result, then a second process resolves the same operation and finishes all three events.
- `CROSS_PROCESS_EXCLUSIVE.log` — two operating-system processes share the journal; the second waits for the first, then starts from the first batch's actual final clock/state. No duplicate effects.
- `COMMANDS.md` — exact commands executed.
- `SOURCE_PINS.json` — frozen ABI, architecture, contracts and implementation hashes.
- `SANITIZED_PASSPORT.json` — model/runtime, scope, authority and hold declaration.
- `RECEIPT.md` — acceptance mapping and custody summary.
- `hard_crash_recovery.py` — reproducible file-backed owner used by the hard-crash evidence; evidence only.
- `cross_process_exclusive.py` — reproducible two-process exclusivity evidence; evidence only.

The controlled owner is a software fixture. It carries `durable_psychological_transition: MISSING_RULE` explicitly. This packet proves execution, custody and recovery only; it does not issue developmental science.
