# PYAT #777 universal source-to-C11 — reproduction commands

All commands run from the repository root with `PYTHONPATH=.`. No private
worktree path, `.r61` runtime or network access is required for fixture proof.

## Status and ledger

```sh
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli status
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli ledger
```

Expected: 35 sources, 18,413 physical slots, 18,276 original items, 18,250
exact joins, 26 unmatched IDs, 1,653 held slots, 24 `NOT_RUN` + 11
`FIXTURE_ONLY`, original execution `NOT_RUN`.

## All 35 fixture releases through the current C11 consumer

```sh
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli prove-all
```

Expected: 35/35 `ACCEPTED_C11_LOGICAL_RELEASE`; every release hash equals the
recorded R157 native receipt; every facade/current-ingest/repository release ref
agrees; no source read.

## One source

```sh
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli prove SRC01
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli prove SRC26
```

## Cold restore

```sh
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli cold-restore SRC26
```

Expected: rebuilt index byte-identical to
`be69b414f0c03ffc70e0888137c4bde5a8114a3890011f7e1a40ebdbf83770f6`;
SRC26 release `528ca5c34f7d9fd3c92ae5832d7be0001fec001a1053a046ba899a1ceda3164f`;
`source_read_performed=false`.

## Negative / refusal evidence

```sh
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli negative
```

Expected: 8/8 checks pass; no original source byte carrier, no original
execution, metadata-only original plan.

## Owner / ABI and provenance

```sh
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli owner-abi
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli provenance
```

Expected: 456 imported files match the exact R157 candidate Git blobs; current
consumer owner hashes are recorded separately.

## Focused tests

```sh
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_universal_source_to_c11.py -q -o addopts=''
```

Expected: `41 passed`.

```sh
PYTHONPATH=. python3 -m pytest \
  rawlsing_next/tests/test_source_configuration_foundation.py \
  rawlsing_next/tests/test_source_configuration_library.py \
  rawlsing_next/tests/test_source_configuration_p3.py \
  rawlsing_next/tests/test_pre553_source_read_admission.py \
  -q -o addopts=''
```

Expected: `37 passed, 2 skipped` (the two R154 loader tests skip because the
R154 runtime/store is not imported into this branch).

## R157 package commands still work

```sh
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli status
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli fixture-call SRC01
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli original-plan SRC01 \
  --source-path /never/opened/SRC01.sav \
  --host universal-source-to-c11 \
  --purpose NEGATIVE_REFUSAL_ONLY \
  --consumer-use NEGATIVE_REFUSAL_ONLY \
  --semantic-scope NEGATIVE_REFUSAL_ONLY
```

The `original-plan` command emits the exact external source-read request without
opening source bytes; original execution remains unauthorized and `NOT_RUN`.

## Write artifacts

```sh
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli \
  --output WORKER_RETURNS/PYAT-777-UNIVERSAL-SOURCE-TO-C11-R1/35_SOURCE_LEDGER.json ledger
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli \
  --output WORKER_RETURNS/PYAT-777-UNIVERSAL-SOURCE-TO-C11-R1/PROVE_ALL_RECEIPTS.json prove-all
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli \
  --output WORKER_RETURNS/PYAT-777-UNIVERSAL-SOURCE-TO-C11-R1/COLD_RESTORE.json cold-restore SRC26
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli \
  --output WORKER_RETURNS/PYAT-777-UNIVERSAL-SOURCE-TO-C11-R1/NEGATIVE_EVIDENCE.json negative
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli \
  --output WORKER_RETURNS/PYAT-777-UNIVERSAL-SOURCE-TO-C11-R1/OWNER_ABI.json owner-abi
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli \
  --output WORKER_RETURNS/PYAT-777-UNIVERSAL-SOURCE-TO-C11-R1/PROVENANCE.json provenance
```
