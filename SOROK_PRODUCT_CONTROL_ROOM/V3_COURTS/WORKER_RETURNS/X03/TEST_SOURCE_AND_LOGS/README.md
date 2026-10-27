# X03 executable evidence

- `run_v3_tests.py` — read-only pytest wrapper. It imports the original V3 tests from the extracted staging tree and supplies `yaml.safe_load` through the local Ruby Psych parser. Numeric YAML keys are converted back to integers so age-bracket tests are not altered by JSON string keys.
- `focused_tests.log` — 71 focused original-source tests passed. Command: `RAWLSING_STAGING_ROOT=<source> python3 run_v3_tests.py test_metabolization_effects.py test_step_logic.py test_v5_framework_dormancy.py test_invariants.py test_wave4.py test_architecture_invariants.py test_step_sanity.py test_llm_contract.py test_v5_baseline_load.py test_v5_alienation.py`.
- `probe_x03.py` / `probe_x03.json` — direct read-only probes of the seven assigned mechanisms. The probe makes no LLM call and writes only its JSON output.
- `environment_probe.txt` — host, Python, Ruby, Git and model facts.

The tests establish historical code behavior at their tested grain. They do not establish current C9/C12 integration, scientific validity, native actor law or source permission.
