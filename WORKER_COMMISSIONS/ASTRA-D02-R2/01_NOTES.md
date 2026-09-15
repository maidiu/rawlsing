# ASTRA-D02-R2 — governed runtime recovery notes

Commission branch: `agent/rabochii-prev3-astra-d02r2-governed-source-runtime-r1`

Commission tip: `27fd6658955d888da37cc24acfc98540eae26508`

Accepted decoder path: `rawlsing_next/pre553_physical_decoder.py`

Accepted decoder Git blob: `13aa733b511dc23e00bfcdf288c5b920e3f09983`

Prior typed failure: local execution could neither import nor provision `pyreadstat`; the already accepted decoder therefore never executed there.

## Recovery choice

The repository already contains the governed bounded-court GitHub Actions surface at `.github/workflows/rabochii-governed-bounded-court.yml`. This lane uses that existing surface rather than inventing a second runner.

The environment delta is intentionally narrow and nonsemantic: pin `pyreadstat==1.3.6` together with the court's test dependencies on Python 3.12, then execute the already accepted decoder. The court spec is `.rabochii/court_spec.json` and the commissioned proof test is `WORKER_COMMISSIONS/ASTRA-D02-R2/test_governed_pyreadstat_runtime.py`.

The proof uses a tiny generated DTA transport fixture. It does **not** materialize `LITS-2006-data.dta`, does not add a carrier SHA, does not alter the frozen compatibility allowlist, does not supply an encoding override, and does not use pandas or any other reader in place of the accepted decoder. `pyreadstat.write_dta` plus pandas are used only to construct the tiny input fixture; the read path under proof is `rawlsing_next.pre553_physical_decoder.decode_dta` and its `pyreadstat` backend.

The proof asserts the accepted decoder Git blob before execution, requires `pyreadstat==1.3.6`, executes both metadata and cell iteration through the accepted DTA decoder, and emits `.rabochii/astra_d02_r2_runtime_receipt.json`. The generic bounded court also emits `.rabochii/court_receipt.json`; both are uploaded as governed workflow artifacts.

## Authority boundary

This lane proves execution capability only. It creates no LiTS learned result, no R2/R7/R27 materialization, no new compatibility semantics, no source-text encoding authority, no response semantics, no routing or structural authority, and no person/V3 state.

The draft PR used for CI is a trigger surface only and is not to be merged into MAIN or semantic PRE-MAIN.
