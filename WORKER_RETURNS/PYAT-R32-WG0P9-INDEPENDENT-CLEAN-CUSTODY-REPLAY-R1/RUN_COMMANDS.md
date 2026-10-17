# Exact execution commands (clean checkout /tmp/wg0p9_p8)

All suites were run from the P8 candidate court with the pinned P6 bootstrap:

```sh
cd candidate/court
export PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
export PYTHONPATH="$PWD/bootstrap_p6:$PWD/repro"
export WG0M_RUN=phase_b_P5 WG0L_PHASE_B_ADAPTER=phase_b_adapter_v1
export WG0O_WG0N_ROOT=<restored WG0N dir>   # only for WG0O 17

python3 -B -m pytest -c runtime_phase_b/candidate/pytest.ini -q <suite> --junitxml=<out>
```

Suites and results:

- `repro/test_wg0p8_transport.py` (run at P8 return root): 9 passed
- WG0O 17 `reviewer_frozen/02_WG0P7_STAGED/reviewer/tests/test_authority_seam_court.py`:
  16 passed / 1 failed as published (missing WG0N verdict); 17 passed after exact-Git restore
- WG0Q 36 `.../test_authority_body_delta_court.py`: 36 passed
- WG0M 33 `tests/test_descriptor_delta_frozen.py`: 33 passed
- original 65 `tests/test_precommitted_phase_b.py`: 65 passed
- original 3 `tests/p5_mapping/test_original_three_adapter_v1.py`: 3 passed
- J44/K11 `tests/phase_b/test_original_{j,k}_adapter_v1.py`: 44 + 11 passed
- owners 80 `runtime_phase_b/owner_tests`: 80 passed
- fresh 42 `<P8>/candidate/tests/test_source_view_binding.py`: 42 passed
- cold pointer `<P8>/candidate/tests/test_cold_pointer_process.py`: 1 passed after genuine
  cold crash/resume regenerated `owner/` and the sanitized path was restored in the execution copy

Cold and hostiles:

```sh
python3 -B repro/phase_b_cold_worker_v1.py crash  <freshdir>   # exit 23
python3 -B repro/phase_b_cold_worker_v1.py resume <freshdir>   # exit 0
python3 -B <P8>/candidate/repro/cold_pointer_worker.py <folder> # IdentityError, 0 I03
python3 repro/wg0p8_publication.py verify                      # PASS 187/187
python3 repro/wg0p8_publication.py probe-import                # exit 86 (D1 version defect)
```
