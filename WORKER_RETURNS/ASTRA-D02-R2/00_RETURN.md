# ASTRA-D02-R2 — governed PRE553 pyreadstat runtime surface recovery

Status: `PASS__GOVERNED_PYREADSTAT_RUNTIME_SURFACE_PROVED`

Branch: `agent/rabochii-prev3-astra-d02r2-governed-source-runtime-r1`

Commission tip / semantic candidate: `27fd6658955d888da37cc24acfc98540eae26508`

HQ fan-in named by commission: `05167b4cd30dc751cce797a16baa397bc7d0457d`

Exact grain: `PSC04_PRE553_ACCEPTED_PYREADSTAT_RUNTIME_SURFACE_RECOVERY_R1_ONLY`

## Holding

A lawful repo-native governed execution surface has been proved for the already accepted PRE553 DTA decoder. The proof used the existing `Rabochii Governed Bounded Court` GitHub Actions surface on the commissioned branch, with a pinned CPython / dependency recipe and a tiny generated DTA transport fixture. It did not materialize the 139,531,180-byte LiTS carrier, inspect learned outcomes, extend compatibility semantics, or substitute a decoder or reader.

The bounded court executed at evidence SHA:

`884498c84a71c5e39521294034c28725e8350a35`

GitHub Actions run:

`35060888384`

Conclusion: `success`.

The governed court receipt records `result=PASS`, `exit_code=0`, CPython `3.12.14`, and the exact test `rawlsing_next/tests/test_astra_d02_r2_governed_pyreadstat_runtime.py`.

The runtime receipt independently records that the accepted decoder file has observed Git blob SHA:

`13aa733b511dc23e00bfcdf288c5b920e3f09983`

matching the frozen accepted decoder blob exactly, and that `pyreadstat==1.3.6` executed the decoder against a real DTA fixture with reader configuration:

- `reader = pyreadstat`
- `reader_version = 1.3.6`
- `user_missing = true`
- `apply_value_formats = false`
- `encoding = null` for the transport-only probe

The probe decoded 2 rows x 2 variables into 4 physical cells. No alternate reader, shim, compatibility allowlist change, or LiTS carrier materialization occurred.

## Exact reproducible governed runtime recipe for later D03

Use the repository's governed bounded-court Actions surface on Ubuntu with Python `3.12`, and provision exactly:

`python -m pip install --disable-pip-version-check pytest==8.4.2 pandas==2.3.2 pyreadstat==1.3.6`

Then execute the frozen accepted decoder blob `13aa733b511dc23e00bfcdf288c5b920e3f09983` through `rawlsing_next/pre553_physical_decoder.py`. A later D03 that has its own authority to materialize the exact LiTS-I carrier may run that same frozen decoder and its already accepted carrier-specific configuration on this proved runtime surface. D02-R2 itself does not materialize or inspect that carrier.

## Governed evidence

- workflow run: `35060888384`
- job: `104680758768`
- workflow conclusion: `success`
- evidence execution SHA: `884498c84a71c5e39521294034c28725e8350a35`
- PR synthetic merge SHA recorded by court: `b1be43814ecb5963e705f0f7b20346e7a1b21269`
- court spec SHA-256: `7ef8f2276af504261390577875946f58c6d1ea3047680b3b6f881486f92c20be`
- Actions artifact id: `10431958094`
- artifact digest: `sha256:5407f5f49719518277dd6df450cf6c2f57932b3ea9ea4ffd77080afe5962066c`
- artifact contents: `court_receipt.json`, `astra_d02_r2_runtime_receipt.json`

## Authority ceiling

This PASS proves execution-surface capability only. It creates no learned result, no R2/R7/R27 materialization, no semantic authority, no routing authority, no structural admission, and no person/V3 state. No unrelated lane is blocked.

Machine-readable governed receipt: `WORKER_RETURNS/ASTRA-D02-R2/01_GOVERNED_RUNTIME_SURFACE_RECEIPT.json`.

Terminal: `PASS__GOVERNED_PYREADSTAT_RUNTIME_SURFACE_PROVED`
