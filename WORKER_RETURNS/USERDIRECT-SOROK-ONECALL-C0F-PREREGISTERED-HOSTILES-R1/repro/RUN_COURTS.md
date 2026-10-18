# ONECALL-C0F — exact fully Git-contained runnable independent court

This new `repro/` tree is a **postfreeze publication transport only**. It contains exact unmodified byte blobs of C0 final source/tests and independent C0F test source. No frozen preregistration expectation, scientific code, production module, original survey or actor authority has been changed.

## Source custody

- Reviewer independent Phase-A freeze: `1daad754b01a1a3b2f866cc4c47c2f800f63d451` (C0 source had not been inspected).
- Final C0 author source: `66d012c469ee1791c61f1d623079520697508243`. Exact `onecall_c0.py` source Git blob `f45e4f5573495f060503f92b7630ec83531ced4d`, SHA256 `3f0da92095f8355c7512d49ac546c846b6026d3775533ba56be7e148e11abfa1`.
- Exact independent prereg A01–A32 C0 test Git blob `0a727662fc1790ec9a56f566dfe6eb19a93fe8c7`, SHA256 `cc9278886e782bbd49dafc340ffe96b8c4650146d1d98cabc457f2ddc86563a8`. The translation fixture is postfreeze and the separate Phase-A expectations were not edited.
- Exact independent R32–R43 test Git blob `b736392c1f9fb5aba86c7ac6e056d49405ed7f88`, SHA256 `6d4811ef66fde35d022abdc9a5e2e1e36b0d9d2eb0e84c0d3aad4e29d4929f5f`. This is explicitly a postfreeze hostile addition, not a rewritten preregistration.
- Original Phase A reference files here are exact prior-frozen Git blobs, not generated from C0 implementation.

## Execute from clean private-repo checkout

```sh
cd WORKER_RETURNS/USERDIRECT-SOROK-ONECALL-C0F-PREREGISTERED-HOSTILES-R1/repro
python -B frozen/materialize_frozen_matrix.py
python -B -m pytest -q --junitxml=author_junit.xml test_onecall_c0_part{1,2,3,4}.py
# 32 PASS — expected exit 0
python -B -m pytest -q --junitxml=preregistered_junit.xml test_phase_b_preregistered_against_c0.py
# 22 PASS / 10 FAIL — expected exit 1; DO NOT xfail/skip
python -B -m pytest -q --junitxml=additional_junit.xml test_phase_b_postfreeze_distinct_hostiles.py
# 4 PASS / 8 FAIL — expected exit 1; DO NOT xfail/skip
(cd frozen && python -B -m pytest -q --junitxml=phasea_junit.xml test_phase_a_oracle.py)
# 45 PASS on independent reference only — not a C0 acceptance test
python -B onecall_c0.py --mode ONE_CALL --out cold_onecall.json
python -B onecall_c0.py --mode TWO_CALL --out cold_twocall.json
python -B onecall_c0.py --mode FIXED_PACKET --out cold_fixed.json
```

The two independent suites are intentionally RED on the exact unmodified C0 author candidate. They are not invalid test failures to “repair” in the reviewer return. The sourcefree C0 author tests being green does not satisfy missing owner/actor semantics.

## Real existing receipts (no fabrication)

Complete original generated XML including real 18 failures and raw stdout is in the separately verified local conversation archive `C0F_PHASE_B_INDEPENDENT_EXECUTION_AND_HOSTILES.tar.gz` (SHA-256 `1fca6fe1c4c8a53d6c65469f0a3e6ff6a442e911942029450f0dc534cca86f60`), and the larger self-contained source/cold/JUnit capsule `ONECALL_C0F_FINAL_EXECUTABLE_COURT_R1.tar.xz` (SHA-256 `19ac443e247a76638d5aa644e3874fcbb68cd1cba5890deb3fec9b40c6e33cd3`). The exact original and terminal rerun JUnit digests and case failures are in `ACTUAL_EXECUTION_RECEIPTS.json`. These two compressed conversation artifacts are **not claimed as Git blobs**; Git *does* now publish the exact importable source and runnable tests that regenerate their JUnit.

**Verdict:** `C0_REAL_SOURCEFREE_SCHEDULER_POSITIVE_CONFIRMED__PREREG_I2_AUTHORITY_BOUNDARY_RED__NATIVE_PSYCHOLOGY_AND_RELEASE_HOLD`. Zero LLM provider calls, original survey operations, native B3 imports, or issuer/actor rights.
