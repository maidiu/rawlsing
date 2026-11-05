# SOROK current-B seam check R1

**Grade:** `TEST_ONLY_ENGINEERING_SOURCE_OWNER_HOLD_NOT_NATIVE`

Bounded P3 execution over exact pins S48 `9fe0d066`, S49 `6604f2d9`,
S50 `515b9a8e`, S51 `2a4cdd2d`, S52 `c821b488`.

The check traces the actual sampled S44/S45 B actor identity, world state and
C9/ADP017 access into S48/S49 independent generation, BP4 world performance and
the normal S42 admission boundary. It then records the exact source/first
importer disposition at each later pin.

## Run

```text
python3 WORKER_RETURNS/SOROK-CURRENT-B-SEAM-20261105-R1/run_current_b_seam.py
```

The default invocation uses the in-checkout exact closure stages under
`.runtime/closures/` and `.runtime/source-tree` and writes:

- `evidence/current_b_seam.json`
- `evidence/source_manifest.json`
- `evidence/probe_s49.json`, `probe_s50.json`, `probe_s51.json`, `probe_s52.json`
- `evidence/junit/*_hold.xml`
- `logs/probe_*.log`, `logs/*_hold.log`, `logs/harness_stdout.log`

Options:

- `--source-root PATH` — repository/worktree containing the pinned commits.
- `--s49-stage/--s50-stage/--s51-stage/--s52-stage PATH` — exact closure roots.
- `--work-dir`, `--logs-dir`, `--evidence-dir`, `--json-out`.

Exit `0` means every source-manifest, probe and focused HOLD test check passed.
Exit `1` means a check failed. Exit `2` means staging, manifest or probe error.

## Boundary

No product code, expected psychology or other worker return is modified. The
result is a source-owner HOLD disposition, not a native B generation, choice,
paid counterpart or C8/C9/C12 authority.
