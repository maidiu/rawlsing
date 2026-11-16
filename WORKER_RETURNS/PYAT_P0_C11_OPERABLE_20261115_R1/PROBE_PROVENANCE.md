# Probe provenance

The accepted J5 reuse-court probe files were copied read-only from
`WORKER_RETURNS/PYAT_COUNTRY_REUSE_COURT_20261115/probe/` at
`0b37420cf9daa4a49fa2b1e67da9850736836603`:

`build_estate.py`, `court_instrumentation.py`, `fixture_1006.py`,
`instrument_1006.py`, `make_manifest.py`, `ops.py`, `preflight.py`,
`query_1006.py`, `run_court.py`, `state_probe.py`, `summarize.py`.

New reviewer probes in this return:

- `run_prepared.py` — matched 128-respondent / 100-operation baseline vs
  prepared session.
- `wide_fixture.py`, `run_wide.py` — 64-respondent × 30-question realistic-width
  synthetic estate and 20-operation matched comparison.
- `measure_build.py`, `measure_open.py` — construction/cold-open measurements.
- `verify_wide_oracle.py` — native in-memory oracle parity (also recorded in
  `evidence/parity_wide_oracle.json`).

All fixtures are TEST_ONLY sourcefree; no original source or science is used.
