# RX04 independent evidence

- `run_v3_tests.py` — read-only V3 test wrapper. It imports the original historical tests from the extracted staging tree and supplies `yaml.safe_load` through the local Ruby Psych parser. Numeric YAML keys are converted back to integers.
- `v3_64.log` — 64 focused historical tests passed (21.82s).
- `distribution_smoke.log` — 1 distribution test passed (302.02s); X04 reported 152s for the same test, an environment timing difference only.
- `s48_12.log` — exact-cut S48 `9fe0d066e4bf61ab6819a1f56e42d6d07956c2f7` 12 tests passed (13.58s), with `M35_JOIN_E_RETURN` and read-only S48 source.
- `probe_rx04.py` / `probe_rx04.json` — independent sourcefree probe for scheduler counts, band/ledger behavior, empty/parse/fallback paths, derived writes, annotation leakage, rupture severity, and direct render isolation.
- `environment_probe.txt` — host, Python, Ruby, Git and model/provider facts.

The 64 + 1 + 12 = 77 reproduced X04 grouping. No live provider or native C9/C12 test was run.
