# Exact commands — P3 store ABI repair

Working directory:

```text
WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1
```

Unit checks:

```bash
python3 -m pytest -q tests/test_state_store.py
python3 -m pytest --collect-only -q tests/test_state_store.py
```

Actual owner integration command (run unchanged; expected nonzero while the separate owner crash-fixture import defect remains):

```bash
python3 -m pytest -q tests/test_p3_owner.py
```

Observed:

```text
51 passed

1 failed, 6 passed, 1 skipped
failure: test_real_subprocess_crash_boundary_recovers_prepared_base
ModuleNotFoundError: No module named 'developmental_recursion'
```

Schema generation:

```bash
python3 - <<'PY' > evidence/storage-abi-repair/SCHEMA.sql
# temporary fresh PsycheStore; dump sqlite_master DDL and user_version
PY
```

Scope/hygiene:

```bash
git diff --check
git diff --name-only 8cc2914b1089cfc113ae1737941bd2a9efde622b -- \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/evidence/storage
```

The second command is empty: prior storage evidence is unchanged.
