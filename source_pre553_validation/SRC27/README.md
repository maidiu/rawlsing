# R157 LITS full supported-scope return (SRC27–SRC30)

This lane binds the four LiTS DTA waves to the frozen R157 source-configuration
interface and now **positively exercises every declared supported
question/response slot and every declared coordinate shape** through permitted
nonrespondent physical-cell fixtures. It does **not** read original respondent
files, execute an original source, or issue an original empirical workload.

## What is here

- `rawlsing_next/source_configuration/data/SRC27/` — canonical lane builders and
  the SRC27 config/item ledger/exact-name correspondence.
- `.../SRC28/`, `.../SRC29/`, `.../SRC30/` — source configs, full item-accounting
  ledgers and exact-name correspondence records.
- `source_pre553_validation/SRC27..SRC30/fixture.json` and
  `fixture.config.json` — **full supported-scope** nonrespondent fixtures and
  separately identified fixture configs. Five fixed rows; every supported
  response slot and every declared coordinate has a cell in every row.
- `source_pre553_validation/SRC27..SRC30/representative_*` — preserved prior
  representative fixtures/results. These are prior positives, not the full
  supported-scope proof.
- `source_pre553_validation/SRC27..SRC30/validation_results.json` — actual
  full-supported native release traces, expected/actual counts and states.
- `source_pre553_validation/SRC27..SRC30/exception_ledger.json` — exact
  residuals and the full-supported/original-execution distinction.
- `source_pre553_validation/SRC27/full_scope_manifest.json` and
  `LANE_RETURN.json` — lane-wide paths, hashes, counts and next edge.

## Full supported fixture result

| Source | Supported questions | Coordinate slots | Response events | Coordinate facts | Routing facts | Native release |
|---|---:|---:|---:|---:|---:|---|
| SRC27 | 128 | 3 | 640 | 15 | 640 | `607a9c8f…` |
| SRC28 | 315 | 2 | 1,575 | 10 | 1,575 | `acf10f86…` |
| SRC29 | 51 | 4 | 255 | 20 | 255 | `a0c2b88e…` |
| SRC30 | 313 | 3 | 1,565 | 15 | 1,565 | `887110e1…` |
| **Total** | **807** | **12** | **4,035** | **60** | **4,035** | 4 positive releases |

All expected response states, canonical values, routing states and coordinate
states matched the explicit pre-call oracles. The P3 fixture-scoped key path
produced five exact fixture key witnesses per source.

## Source configuration scope

Every source item and physical slot is accounted. The original configs prepare
280 / 542 / 1,165 / 1,073 response-bound questions respectively; the declared
supported set is 128 / 315 / 51 / 313 because routing-unknown items and exact P2
response-authority-gap items are not promoted to supported scope. They remain
fully serialized with exact residuals, not called “unselected.”

## Reproduce

```sh
PYTHONPATH=. python3 rawlsing_next/source_configuration/data/SRC27/lits_full_bindings.py
PYTHONPATH=. python3 source_pre553_validation/SRC27/build_full_scope_fixtures.py
PYTHONPATH=. python3 source_pre553_validation/SRC27/run_validation.py
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py -q -o addopts=''
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_p3.py -q -o addopts='' \
  -k 'not r154_loader_delegates_prepared_construction_not_issued_workload and not r154_prepared_path_wrong_source_refusal_and_restore'
```

The two deselected P3 loader tests require a tracked `WORKER_RETURNS/.../r154_load.py`
file that is skip-worktree and absent in this worktree; that file is outside the
LITS write terrain and was not modified.

## Boundary

The native releases are nonrespondent fixture releases with
`NONRESPONDENT_FIXTURE_ONLY` authority. Original source execution is
`NOT_PERFORMED_UNDER_R157_PREPARATION`; fixture validation does not establish
original scientific results or execution permission. Original workload issuance
is separate. See each `validation_results.json` and `exception_ledger.json` for
exact call traces, refusals, skips and residuals.
