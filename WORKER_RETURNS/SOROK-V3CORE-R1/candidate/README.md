# SOROK V3CORE-R1 candidate

Sourcefree historical-development adapter. Not native, not science issuance,
not canonical C9/C12.

## Run

```sh
cd candidate
PYTHONPATH=$PWD:$PWD/vendor:$PWD/vendor/py3deps PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest -o addopts='' -q -p no:cacheprovider tests
```

```sh
PYTHONPATH=$PWD:$PWD/vendor:$PWD/vendor/py3deps PYTHONDONTWRITEBYTECODE=1 \
  python3 tools/run_courts.py
```

```sh
PYTHONPATH=$PWD:$PWD/vendor:$PWD/vendor/py3deps PYTHONDONTWRITEBYTECODE=1 \
  python3 tools/first_consumer_probe.py
```

## Layout

- `v3core_adapter/` — adapter; only three annual steps are admitted.
- `vendor/v3/` — exact historical V3 donor source.
- `vendor/v2/` — V2 surface closure for the unchanged golden-run test.
- `vendor/i1/` — exact I1 candidate consumed by the first consumer.
- `vendor/py3deps/` — PyYAML 6.0.3 only.
- `tests/` — fault, quarantine, scheduler, render, derived, cold-reload and
  first-consumer courts.
- `tools/` — court runner, cold probe, first-consumer probe, contract and hash
  inventory.
- `evidence/` — executed results.

## Authority

`TEST_ONLY_SOURCEFREE_NO_SCIENCE_ISSUANCE`. The adapter does not write I1's C12
database, does not create a rival C9 store, and does not claim a native person.
