# SOROK P2 later-event continuation

Additive TEST_ONLY sourcefree continuation over the shipped S45-S47 package at `41bf45813fd0adeffd9b54e1306c2022abe96514`.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 -B -m p2_continuation.cli positive --state <new-state>
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 -B -m p2_continuation.cli scheduled --state <new-state>
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 -B -m p2_continuation.cli cut-restore --state <new-state>
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 -B -m p2_continuation.cli cold --state <state> --event-ref <ref>
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 -B -m pytest -q -p no:cacheprovider tests
```

Read `00_RETURN.md` for exact callables, results, limits and holds. No native, human or protected acceptance is claimed.
