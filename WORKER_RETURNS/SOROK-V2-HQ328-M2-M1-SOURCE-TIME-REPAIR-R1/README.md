# Run and publish M2 bounded return

The package is a handoff to a **local Git-capable agent**. Its files are placed under one assigned new subtree. Do **not** commit the ZIP itself, and do not edit any other repository path.

## Direct positive court

```sh
cd WORKER_RETURNS/SOROK-V2-HQ328-M2-M1-SOURCE-TIME-REPAIR-R1
python -m pytest -q test_m2.py --junitxml=execution/local_m2_41.xml
```

Expected: 41 passed. The package also carries exact original pinned M1 and independent I2 `.tar.gz` for strict immutable comparison.

## Exact archival/pinning checks

`frozen_inputs/M1_original_exact_7e91c198.tar.gz` SHA-256 `30b820eda81089c89d9e2df8145860386d33b973f5c7f6a028e7e16b21dbe7b4`.
`frozen_inputs/I2_strict_exact_19f1e86a.tar.gz` SHA-256 `449f9cf8c8db7befc8b2358b776adee636db70f884e7d2fdffa069b07c19d72f`.

Cross-source same-name imports require **separate temporary directories**. Never run the original and repaired suites together in one Python process/import path. The supplied execution/ JUnit files were generated with isolated directories; the normal before/after statuses are in 00_RETURN.md.

**Do not force old legacy tests green by weakening witnesses, omitting timestamps or modifying frozen source.** No accepted CAN/ADP rules are modified; distinct independent I2 comes after this candidate return.
