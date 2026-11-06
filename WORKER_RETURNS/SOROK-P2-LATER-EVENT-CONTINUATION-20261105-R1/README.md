# SOROK P2 later-event continuation

Additive TEST_ONLY sourcefree continuation over the accepted shipped S45-S47
product at `41bf45813fd0adeffd9b54e1306c2022abe96514`.

This repair separates public output from privileged engineering evidence and
makes DO_HELP an explicit user action.

## Public CLI

```text
PYTHONPATH=$PWD python3 -B -m p2_continuation.cli positive --state <new-state>
PYTHONPATH=$PWD python3 -B -m p2_continuation.cli scheduled --state <new-state>
PYTHONPATH=$PWD python3 -B -m p2_continuation.cli cut-restore --state <new-state>
PYTHONPATH=$PWD python3 -B -m p2_continuation.cli cold --state <state> --event-ref <ref>
```

Public positive/scheduled output is observation-only: no user DO_HELP, zero
encounter increment, and no internal `c9`/`s43`/plan/source/history/readset/root
fields.

Explicit user actions:

```text
python3 -B -m p2_continuation.cli positive --state <state> --do-help
python3 -B -m p2_continuation.cli scheduled --state <state> --do-help
python3 -B -m p2_continuation.cli do-help --state <state>
```

`--say` and `--attend` are also explicit opt-in flags.

Privileged engineering evidence is separate:

```text
python3 -B -m p2_continuation.cli positive --state <state> \
  --engineering-out .local-logs/positive-engineering.json
```

## Public API

- `run_positive_public`, `run_scheduled_public`
- `public_report`, `public_cut_restore_report`, `public_cold_report`
- `privacy_hits`
- Explicit `project_do_help()` / CLI `do-help`
- Preserved primitives: `produce_input_interval`, `admit_later_event`,
  `read_later_event`, `cold_read`

## Tests

```text
SOROK_P2_BASE_ROOT=<checkout>/.local-logs/p2-later-repair/base \
TMPDIR=<return>/logs/tmp PYTHONPATH=<return> PYTHONDONTWRITEBYTECODE=1 \
python3 -B -m pytest -q -p no:cacheprovider \
  --junitxml=<return>/evidence/junit.xml <return>/tests
```

See `00_RETURN.md` for exact results, oracle reproduction and limits. No native,
human or protected acceptance is claimed.
