# R147 next calls

## Render current metadata preparation

```sh
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R147-ALL35-CURRENT-METADATA-R1/runtime/render_current_source_preparation.py --source-id SRC23
```

Works for all 29 sources with current metadata. Output is metadata preparation
only; no survey file is opened.

## Six sources needing exact current metadata staging

`records/MISSING_METADATA_DOCUMENTS.json` names SRC04, SRC05, SRC06, SRC07,
SRC11 and SRC13 with the exact needed source/family/wave document. Stage the
current document and rerun the command above for that source.

## Still required for actual execution

1. exact current source access identity/edition hash;
2. exact current source-read grant/current resolver for whole-file decode;
3. complete native U and exact scientific roles/topology/Epre;
4. exact query/frontier/learned/FF consumer authority.

Metadata documents and historical packets do not authorize source response access.
