# ASTRA-D02 — PSC04 accepted LiTS decoder capability

Status: `BLOCKED__EXACT_CARRIER_VERIFIED__ACCEPTED_PRE553_PYREADSTAT_BACKEND_UNAVAILABLE_ON_EXECUTION_SURFACE`

Branch: `agent/rabochii-prev3-astra-d02-source-execution-r1`

Commission tip: `50de465a9c04faafca812390fd59a1c8b09fddd7`

HQ adoption base: `98279580ffcccdd764663107aa65835fb6929228`

Exact grain:

`PSC04_EXACT_PRE553_PYREADSTAT_EXECUTION_SURFACE_PROOF_ONLY`

## Holding

D02 executed only the bounded capability question authorized by the Astra dispatch. It does not materialize R2/R7/R27, does not inspect learned outcomes, and does not substitute any decoder or reader.

The exact commissioned Library carrier was materialized under the lane's `EXACT_ONLY` permission:

- file id: `file_0000000036dc81f8b8b546e356590a03`
- version: `1`
- filename: `LITS-2006-data.dta`
- bytes: `139531180`
- observed SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- expected SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

The accepted decoder is the exact Git blob `13aa733b511dc23e00bfcdf288c5b920e3f09983` (`rawlsing_next/pre553_physical_decoder.py`). Inspection confirms that this carrier SHA is frozen in its compatibility allowlist as `latin1`, and that the DTA path requires `pyreadstat`, `apply_value_formats=False`, and `user_missing=True`.

## Execution result

The current execution surface is Python `3.13.5` on Linux x86_64. `import pyreadstat` fails with `ModuleNotFoundError`.

D02 then exercised the only repair authority granted to this lane: bounded environment provisioning. `python -m pip install pyreadstat` failed because the execution environment cannot resolve/reach the package index (`Temporary failure in name resolution`); no package was installed.

Therefore the exact accepted decoder could not be executed against the exact carrier. No compatibility backend was replaced, no pandas/Stata fallback was used, and no synthetic `pyreadstat` shim was introduced.

## Exact blocker

`D02_BLOCK__AUTHORIZED_EXECUTION_SURFACE_CANNOT_IMPORT_OR_PROVISION_PYREADSTAT__ACCEPTED_PRE553_DECODER_NOT_EXECUTED`

This blocker is local to D02's wake edge. Per the adopted Astra map:

- D03 remains held because positive accepted-decoder capability has not been proved;
- D04 consequently remains held on its D03 feeder;
- no other independently authorized lane is blocked by this result.

## Authority ceiling

This return proves execution capability failure only. It creates no learned result, no R2/R7/R27 member extension, no semantic authority, no routing authority, no structural admission, and no person/V3 state.

Required capability receipt is committed as `01_EXECUTION_CAPABILITY_RECEIPT.json`.

Terminal: `BLOCKED__EXACT_CARRIER_VERIFIED__ACCEPTED_PRE553_PYREADSTAT_BACKEND_UNAVAILABLE_ON_EXECUTION_SURFACE`
