# R146 next runnable calls

## Ready metadata preparation (3 sources)

```sh
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R146-ALL35-EXISTING-SOURCE-BINDINGS-R1/runtime/render_source_preparation.py --source-id SRC23
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R146-ALL35-EXISTING-SOURCE-BINDINGS-R1/runtime/render_source_preparation.py --source-id SRC22
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R146-ALL35-EXISTING-SOURCE-BINDINGS-R1/runtime/render_source_preparation.py --source-id SRC30
```

These render grounded reuse preparation only. They do not open a survey file.

## Missing current metadata documents (32 sources)

`records/MISSING_METADATA_DOCUMENTS.json` names each source ID and exact
historical `codebook_path`/metadata status. Stage the exact current document for
the target source, then rerun:

```sh
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R146-ALL35-EXISTING-SOURCE-BINDINGS-R1/runtime/render_source_preparation.py --source-id <SRCxx>
```

## Actual response execution gate

Still requires, per source:

1. independently authorized current source identity/header metadata receipt;
2. exact current edition SHA and header/codebook reconciliation;
3. separate source-response read grant/current resolver (metadata receipt cannot authorize decode);
4. complete native U, scientific roles/topology, Epre and method/consumer authority.

No source response execution is authorized by this return.
