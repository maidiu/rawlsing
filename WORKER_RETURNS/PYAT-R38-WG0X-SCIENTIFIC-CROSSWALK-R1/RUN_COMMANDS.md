# Reviewer replay instructions

Run from this return directory with Python 3.11.3 and pytest 9.1.1 (recorded qualified environment). No package installation, respondent file, credentials, network, source permission, or Git is needed for the normal native replay. `sources/native` is a checked-in relative symlink to `../native`; preserve it when copying.

```sh
python3 -B scientific_crosswalk.py
python3 -B experiment.py
python3 -B reconcile_execution.py
PYTHONPATH=native PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -B -m pytest test_wg0x.py native/rawlsing_next/tests/test_pre553_route_b_production.py native/rawlsing_next/tests/test_pre553_empirical_query.py native/rawlsing_next/tests/test_pre553_discovery_exact.py native/rawlsing_next/tests/test_pre553_batch_runner.py native/rawlsing_next/tests/test_pre553_learned_empirical_adjudication.py -q --junitxml=evidence/reviewer_court.xml
python3 -B cold_replay.py
```

Expected final native court: **133 passed, zero failed/error/skipped** (33 WG0X evidence/harness controls and 100 unchanged native tests). The cold replay uses a relocated copy without `.git`, different hash seed, all 133 tests and real fresh native execution. Both native receipt files were byte-identical. Its temporary copy is removed afterward.

Do **not** regenerate or delete `evidence/EXPERIMENT_EXPECTED.json`. It was committed at `615173a78` before the specific WG0X experiment; SHA-256 `12f6d4880ce343ec9676863858d8bfcf2e801d1845bca72e71a0fc5e9d2dfb61`. It derives from the named inherited fixture declarations, not the transport enumerator. WG0X author knew the inherited tests beforehand; this is a separately fixed expected set and an algorithmically independent anti-join, **not a blinded independent acceptance review**.

`reconcile_execution.py` checks actual native manifest units, actual completed execution receipts, reconstructed native fact/discovery identities and query/predicate dependencies, and selected discovery receipts at both M1 consumers. It does not count echoed request lists as proof of execution. Mutations deleting/substituting/duplicating work or receipts and hiding unvisited work fail. Expected 3/actual 3/executed 3 holds for the positive and missing-weight fixtures. Missing-weight `GOVERNED_WEIGHTED` output is `UNAVAILABLE`; RAW remains separate. M1's positive is drawn from the still-qualified raw discovery and does not clear the weighted hold. Valid-empty discovery remains `VALID_EMPTY`.

Shared Git store optional reconstruction/custody commands:

```sh
python3 -B validate_custody.py
```

This verifies full pinned original P2/QRA and archival Register A/B/V525b/D62 blob preimages, every retained projection ordinal/field and code hashes. Full original preimages remain in the existing shared Git object store, while exact selected metadata projections are retained in this return for offline replay. `prepare_evidence.py` and `recover_owner_rows.py` document extraction; normal reviewers should use the retained immutable projections rather than replace the frozen expectation. `build_genealogy.py` regenerates code locators. `capture_passport.py` performs a fresh live import/marker probe.

Historical failed harness checks remain in `candidate_first.*` (31/33) and `final_court_before_test_fix.*` (132/133). Their causes were test field-name errors and an invalid respondent-reference mutation that the native constructor correctly rejected before the intended wrapper check. The final mutation swaps two existing exact respondent mappings, preserving counts; the fixed preimage check refuses it. Native source/transport/expectation bytes were not changed to obtain green results. Logs/JUnit have host root/hostname redactions only, with digests in `evidence/LOG_SANITIZATION.json`.

No WG0R disposition-repair test is run or accepted here. No current original35 empirical execution is claimed. Independent source/semantic-owner review and candidate-harness review remain separate responsibilities.
