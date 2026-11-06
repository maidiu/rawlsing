# D r2 evidence and commands

## Exact frontier probes

Sourcefree SRC01 fixture, baseline hash `ead771ea05deeb530a8e47a4dfc7e920b32208fe4839fb0ce569e192f4ebc0c8`.

| Probe | Result |
|---|---|
| Extra operation | `Original35OperationError: GOVERNED_FRONTIER_NOT_EXACTLY_PLAN_DERIVED` |
| Duplicate operation | refused; duplicate operation ID reported |
| Substituted alias/material | refused with `frontier: false` and extra operation material |
| Missing operation | refused with missing `(op_id, material)` |
| Changed inventory material | refused with `inventory: false` |
| Changed policy material | refused with `policy: false` |
| Changed operation identity | refused with extra `PROBE` identity |
| Exact restore | accepted; baseline hash reproduced |

## Planned mutation

Rebuilt plan value/conditioner mutation:

- compilation changed: yes;
- expected jobs changed: yes;
- executed fact refs changed: yes;
- restored compilation hash and facts exact: yes.

The mutation was bound with rebuilt inventory/policy/frontier as well as via implicit rebuild, so the identity gate does not suppress intended plan changes.

## All35 accounting

`build_original35_operation_plan` over the accepted R157 full config set, then `account_all35_frontiers`:

- 35 source rows; 20 explicit frontiers; 15 no-request rows;
- 991 frontier operations; 21 eligible; 970 held-or-unknown;
- all 35 rows have non-zero F1 operation counts;
- all 15 no-request rows have 0 F2/F3/F4 operations;
- 18,276 items; 18,413 physical slots; 18,467 plan operations;
- counts: EXECUTABLE_RAW 5,630, HELD 4,655, INAPPLICABLE 8,131, DEFERRED 51, ABSTAIN 0.

Current route evidence: 676 qualified, 4,705 unknown, 249 unavailable; candidate raw remains 5,630 and is not labelled route-qualified.

## Commands

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_operations.py \
  -p no:cacheprovider --tb=short
# 8 passed in 31.10s
```

Reviewer probes used the existing sourcefree `_frontier_bundle` / `_fixture_config`
helpers and the accepted R157 config documents via `_packs` / `_presence`.
No original 600s decode, native wrapper run, or whole-estate fixture floor was run.

## Preserved F positives / limits

- Previous F review `f2c477cee…` accepted OriginalItemID/physical-code and unknown-route
  subscopes; the current 8-test suite retains the identity/unknown-route test.
- Native wrapper remains HOLD: direct read bypass, default 3 items, arbitrary coordinate,
  synthetic IDs/person unit, no facts.
- Actual native/FieldForge/science, D 600s end-to-end and all35 original-scale execution
  are NOT_RUN; sourcefree accounting is engineering evidence only.
- No A/C/E/guide/progress/controller/protected edit, no code repair, no native grant.
