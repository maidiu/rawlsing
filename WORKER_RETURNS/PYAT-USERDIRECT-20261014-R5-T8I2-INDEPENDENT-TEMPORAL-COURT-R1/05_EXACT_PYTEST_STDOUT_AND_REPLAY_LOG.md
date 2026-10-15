# T8I2 — actual pytest and cold-process replay log

## Exact import and platform

```
python: 3.13.5
pytest: 9.0.2
git: 2.47.3
cwd: /mnt/data/t8i2_court
imported t8f2_temporal_custody.__file__: /mnt/data/t8i2_court/t8f2_temporal_custody.py
git hash-object t8f2_temporal_custody.py:
9a654b55274b2e8052b1cfaa0eef1a079c079f59
bytes: 16165
git hash-object test_t8f2_temporal_custody.py:
22248899d4fba505a2ff9459491a0d726b3ef75c
bytes: 7885
git hash-object test_hq297_t8c.py:
7f7e0c713a669951b40787537138db7a0653daea
bytes: 10525
git hash-object test_review_mandatory_guards_red.py:
83db68fd705372b62778d81f96687a50b744ecca
bytes: 912
git hash-object test_t8i2_hostiles.py:
9b2d6b0d3121988c89f36ff3e43d066e87f80c39
bytes: 7533
```

Actual four invocations from the same directory (output captured as local stdout/stderr and actual JUnit XML, NOT falsely described as raw GitHub-attached XML):

| Command | Exit | XML test summary | Original JUnit XML SHA256 | bytes |
|---|---:|---|---|---:|
| `python -m pytest -q test_t8f2_temporal_custody.py --junitxml=author21.junit.xml` | 0 | tests=21 failures=0 errors=0 skipped=0 time=0.099 | `a0ce6e593aadd5813717d31730c7f295929b5f657ca0263403604bed2d652319` | 2783 |
| `python -m pytest -q test_t8i2_hostiles.py --junitxml=t8i2_hostiles.junit.xml` | 1 | tests=24 failures=17 errors=0 skipped=0 time=0.204 | `712e51dcc04fc2e2f441e9eaabb8f6c4559adafc50e5017f7215c2363451a54d` | 17287 |
| `python -m pytest -q test_hq297_t8c.py --junitxml=t8c19.junit.xml` | 0 | tests=19 failures=0 errors=0 skipped=0 time=0.092 | `79eccd1fcbd4835832749dbe9787cd5ca0478a0b356701a71d7282f686bfd3a3` | 1869 |
| `python -m pytest -q test_review_mandatory_guards_red.py --junitxml=t8r3.junit.xml` | 1 | tests=3 failures=3 errors=0 skipped=0 time=0.080 | `cba01caafa038fe211399e4df098af6802dcf922e432b752160c32a992c7a0b5` | 3168 |

Original *T8F2* author stdout:
```text
.....................                                                    [100%]
21 passed in 0.10s
```

Original *T8I2* hostile stdout summary:
```text
.......FFFFFFFFFFFFFFFFF                                                 [100%]
17 failed, 7 passed in 0.20s
```
The exact 17 failed node names:
```text
test_red_forged_ref_source_retrieve
test_red_forged_ref_version_retrieve
test_red_blank_source_version_in_ref_retrieve
test_red_consumer_source_forgery_resigned
test_red_consumer_version_forgery_resigned
test_red_consumer_ref_unknown_extra_field_resigned
test_red_arbitrary_registry_authority_constructor
test_red_self_rehashed_time_order_inversion
test_red_self_rehashed_historical_request_outside_allowed
test_red_forged_2017_gap_resigned
test_red_self_rehashed_measured_original_data_upgrade
test_red_self_rehashed_fixture_authorization_upgrade
test_red_self_rehashed_n8s_objective_claim
test_red_revocation_invalid_ref_must_not_revoke_authentic
test_red_consumer_different_valid_registry_same_authority_must_be_bound
test_red_cold_replay_unissued_authority_is_not_cryptographic_signature
test_red_malformed_history_authority_metadata_not_validated
```

All 17 acceptance failures reported `Failed: DID NOT RAISE <class 't8f2_temporal_custody.Refusal'>`. There were no interpreter/import/fixture exceptions or test errors. **Two of 17 tests specify issuer-instance binding beyond a simple sourcefree method and are flagged as stronger-custody challenges, not automatically universal method defects.** Raw hostile stdout: 16,204 bytes, SHA256 `d8cf9c9832eb12907713e58efed7f353e83c98bcee23f873162aa3b065260067`. Original T8R three tests against original T8C: two `DID NOT RAISE`, and one bare `ValueError: Invalid isoformat string: 'not-a-date'`; historical only.

## Fresh-process repeatability

A subprocess court ran the same pinned sourcefree compare/consume in **two new Python interpreter processes** (not mere two calls in one registry), both reconstructing `WaveFactRegistry()` and separate test-only `WaveFact` fixtures, with `historical_year=2017`. Their canonical output strings matched exactly:

```json
{"delta":"3/44","intervening":"UNKNOWN_UNOBSERVED_GAP","ra":"ec518ed9a93b492b052c0db1da035214a2b7a2735dd888c4f481f7229e2b862a","rb":"55a160b02951b5eecbb6c327ac91f16cf904b20a96a2f1b98c214b709172a49e","read_digest":"0d0810e366bb8f3031b08591adaf42db738b2d1b92c0ef1e1fe9c0ebc49cf2bf"}
```
`COLD_SEPARATE_PROCESS_IDENTICAL True`, stdout bytes=327, SHA256 `0569dc3dfc542b1dc85c41bc5d413a26885275ac31abc084ade42679dd2f20f5`. This is *fresh-process deterministic recomputation*, **not an authenticated cold-crash/reload of a persisted issued registry**, not an owner N9 import, and not real source custody.

## Reproduction instructions

Stage exactly the first two pinned T8F2 original files beside the separately authored return-owned `repro/test_t8i2_hostiles.py` (do not substitute T8F or rewrite T8F2; verify `git hash-object`). Execute tests in a sourcefree directory with Python 3.13+ and pytest 9.0+; no internet, GitHub, private raw respondent records or added source grants required. For original unchanged T8C and T8R historical suites stage their exact pinned original blobs **in addition**, not as a code replacement. The test file imports `t8f2_temporal_custody` by module path from its working directory. The T8I original 16-test code is intentionally not called unchanged on T8F2's API: its old T8F `compare/consume` signatures differ; the T8F2 21 tests are an adaptation and the 24 T8I2 cases are additional independent **assertions**, not replacement of historical test files.

No unapproved original survey microdata, real EE12/N8E/N9 or protected code mutation.
