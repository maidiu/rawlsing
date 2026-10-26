# RX02 supporting evidence

Read-only sourcefree probes against original V3. No source edits, provider calls or raw data.

| File | Purpose |
|---|---|
| `rx02_review_probe.py` / `.json` | Independent source identity check, charge arithmetic, groove/channel, route-history selection flip, single-winner, duplicate hostage, ratchet, transaction residue, categorical trace, buffer and event-semantics probes. |
| `x02_probe_flow_copy.py` / `x02_probe_rerun.json` | X02's pinned probe re-run against the same source; output matches the X02 JSON exactly. |
| `run_x02_tests.py` / `x02_17files_pytest.log` | The 17 historical V3 test files reconstructed from X02's grouped receipt; **82 passed** in 11.28s. |
| `environment_probe.txt` | Target/sealed SHAs, host/Python/Ruby, zero provider/raw/source edits. |

Set `X02_SOURCE_ROOT` to the local staging root, `RX02_RAWLSING_REPO` to the authenticated repo for the git-show source-identity read, `X02_S50_MANIFEST` to the S50 `01_SOURCE_IDENTITIES.json`, and `X02_STAGING_ZIP` to the local staging zip. The test runner uses a read-only Ruby Psych YAML bridge with numeric-key conversion because PyYAML is absent.
