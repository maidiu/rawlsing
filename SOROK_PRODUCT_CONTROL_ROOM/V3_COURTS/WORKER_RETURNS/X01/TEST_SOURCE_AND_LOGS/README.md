# X01 test source and logs

All source access was read-only. No survey/raw data, provider call, native rule or production edit is present.

## Replay

Set `RAWLSING_STAGING_ROOT` to the user-confirmed staging root (the parent of `v3/`):

```sh
export RAWLSING_STAGING_ROOT=<USER_HOME>/Desktop/Rawlsing/Rawlsing_code_bundle_staging
python3 -B run_v3_tests.py v3/tests/test_connector_and_field_injection.py
python3 -B probe_v3_x01.py > probe_v3_x01_output.json
python3 -B probe_v3_x01_one_parent.py > probe_v3_x01_one_parent.json
python3 -B probe_v3_x01_backbone.py > probe_v3_x01_backbone.json
```

The runner supplies a read-only `yaml.safe_load` via the system Ruby Psych parser because PyYAML is absent in the qualified Python. It converts numeric YAML keys back to ints so the original age-bracket tests are not changed by JSON stringification. It does not install packages or edit source.

## Files

| File | Purpose |
|---|---|
| `run_v3_tests.py` | Historical V3 test runner with the read-only YAML bridge. |
| `probe_v3_x01.py` | Main baseline/child-model/shards probe. |
| `probe_v3_x01_output.json` | Main probe output. |
| `probe_v3_x01_one_parent.py` / `.json` | One-present-parent dilution probe. |
| `probe_v3_x01_backbone.py` / `.json` | `backbone_state_from_identity` integration/provenance probe. |
| `test_connector_and_field_injection_pytest.log` | 11 passed. |
| `test_wave4_pytest.log` | 14 passed. |
| `test_llm_contract_pytest.log` | 18 passed. |
| `test_v5_baseline_load_pytest.log` | 8 passed. |
| `v3_tests_full_improved_bridge.log` | Full `v3/tests`: 150 passed, 1 environment/data failure (country canonicalization). |
| `v3_tests_full.log` | Full suite with the simpler bridge: 149 passed, 2 failed; extra failure is the Ruby-JSON numeric-key artifact. |
| `environment_probe.txt` | Host/Python/Ruby/pytest versions, source hashes, archive caveat. |

## Source identity

`SOURCE_IDENTITIES.json` has the 31/31 S50 exact rows, additional required-file hashes, YAML hashes and the archive caveat. The local staging zip is `3f2c5ed9…`, not the TD-R05 archive `953c9149…`; archive-level exactness is not claimed. The 31 S50 file hashes and independent authority-file hashes are the evidence.

## Tests not run / limits

No current S44/S49/C9/C12/S50 person integration, no C12 person, no native rule/source/actor, no LLM/provider call, no raw survey data, no V2 conversation run. Historical tests are not current product proof.
