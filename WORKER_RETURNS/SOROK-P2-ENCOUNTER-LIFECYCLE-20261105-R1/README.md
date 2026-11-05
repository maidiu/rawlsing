# Sorok P2 encounter lifecycle

Additive TEST_ONLY local encounter lifecycle around the accepted
`S45Projection`. It persists local `PORTAL`/`OUTSIDE` mode in a root-bound
sidecar, separate from the canonical actor/world store.

```text
python3 run_lifecycle_cli.py new --state <path>
python3 run_lifecycle_cli.py view --state <path> [--text]
python3 run_lifecycle_cli.py say --state <path> "Can I help?"
python3 run_lifecycle_cli.py do-help --state <path>
python3 run_lifecycle_cli.py attend --state <path>
python3 run_lifecycle_cli.py exit --state <path>
python3 run_lifecycle_cli.py return --state <path>
python3 run_lifecycle_cli.py status --state <path>
python3 run_lifecycle_cli.py lifecycle --state <path>
```

Local sidecar: `<state_root>/.sorok_p2_local/encounter_lifecycle.json`.

- `EXIT` from `PORTAL` persists `OUTSIDE` and creates no world event.
- Fresh commands/opens see `OUTSIDE`; `SAY`/`DO_HELP`/`ATTEND` are refused before real S45 calls.
- `RETURN` while `OUTSIDE` restores local `PORTAL` only; no elapsed life, absence, delivery or actor reaction.
- `RETURN` while `PORTAL` preserves the existing world-return typed hold.
- A sidecar bound to another root is refused (`LOCAL_LIFECYCLE_ROOT_MISMATCH`).
