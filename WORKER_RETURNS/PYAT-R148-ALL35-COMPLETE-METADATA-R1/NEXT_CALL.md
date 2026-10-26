# R148 next calls

## Render complete current preparation

```sh
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R148-ALL35-COMPLETE-METADATA-R1/runtime/render_all35_current_preparation.py --source-id SRC13
```

This works for all 35 sources and prints the grounded current metadata/native
preparation record. It does not open a survey file.

## Actual source-to-native workload gates

Still required per source:

1. exact current source access permission and edition SHA;
2. exact current source-read grant/current resolver (metadata never authorizes decode);
3. complete native U and exact scientific roles/topology/Epre;
4. current query/discovery + M1/M2/FF consumer authority.

The existing accepted native sequence remains: source-read admission -> R04
incidence -> `materialize_native_preimages` -> native projection/catalog ->
`prepare_production_discovery`/`execute_production_workload` -> I03/I05/no-drop
-> M1/M2/FF. No source execution is authorized here.
