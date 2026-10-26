# R145 next actual call

The executable metadata-only receipt command is:

```sh
PYTHONPATH=. /usr/local/bin/python3 \
  WORKER_RETURNS/PYAT-R145-CURRENT-SOURCE-PACKAGE-BINDING-R1/runtime/bind_authorized_metadata_receipt.py \
  --scope .r61/r145-current-source-packages/inputs/METADATA_INPUTS.json \
  --source-id SRC23 \
  --receipt <user-authorized-metadata-receipt.json>
```

The receipt must be externally authorized and metadata/header-only. It must provide
source ID/family/wave, exact edition SHA-256, format, dictionary SHA-256, header
variables, row count, issuer/identity receipt refs and authority state
`EXTERNALLY_AUTHORIZED_METADATA_ONLY`.

It does **not** authorize response decode. The next raw-response step also requires
the separate exact `SourceReadRequest` grant/current resolver and the accepted R04
decoder; only then may the native package/materialize/projection path be called.

Still missing after header receipt: physical header/code reconciliation, exact
source role/topology semantics, U/Epre, design/weight/country/population/time
authority, exact query/frontier law and M1 family rule/binding.
