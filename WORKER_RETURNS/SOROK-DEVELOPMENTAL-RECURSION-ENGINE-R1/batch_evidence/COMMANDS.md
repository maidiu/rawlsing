# Exact commands

Working directory:

```text
WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1
```

Compilation and core tests:

```bash
python3 -m py_compile developmental_recursion/engine.py
python3 -m pytest -q tests/test_engine.py
python3 -m pytest --collect-only -q tests/test_engine.py
```

Hard process crash after an owner receipt, followed by recovery in a new process:

```bash
python3 batch_evidence/hard_crash_recovery.py
```

Two-process exclusive execution over one journal and one durable owner:

```bash
python3 batch_evidence/cross_process_exclusive.py
```

Whitespace and patch hygiene from the worktree root:

```bash
git diff --check
```

Observed results:

```text
42 passed in 0.60s
hard_crash_exit=17, batch_after_crash=RUNNING, reservation=RESERVED, recorded_result=null
recovery event_ids=[e1,e2,e3], statuses=[REALIZED,REALIZED,REALIZED], consequences=[MISSING_RULE x3]
cross-process owner_order=[a1,a2,a3,b1,b2,b3], duplicate_effects=0, verified=true
```
