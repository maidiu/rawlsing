# T9S — independent temporal authority court (Phase A frozen)

Phase A preregistration and counterexamples. Phase B runs after the exact T9D
candidate is pushed and read back.

## Layout

| path | meaning |
| --- | --- |
| `00_PHASE_A_PREREGISTRATION_AND_COUNTEREXAMPLES.md` | Phase A narrative, inherited dispositions, reproduced REDs, gate |
| `01_T9S_PRECOMMITTED_PERMISSION_ORACLE.json` | frozen six falsifiers + six positive controls |
| `02_PHASE_A_SOURCE_MANIFEST.json` | Git NUL-blob + sha256 pins of the T9C candidate source |
| `tests/test_t9s_permission_falsifiers.py` | 17 preregistered executable cases |
| `tests/conftest.py` | locates the pinned T9C adapter under the T9R return |
| `repro/reproduce_reds.py` | physically reproduces the four T9R REDs on T9C |
| `repro/build_manifest.py` | rebuilds the source manifest |
| `repro/t9s_binding.py` | typed `CapabilityUnavailable` probes for the two capability gaps |
| `observations/` | JUnit, stdout, reproduced-RED observations |

## Reproduce Phase A

```sh
cd WORKER_RETURNS/PYAT-R27-T9S-TEMPORAL-PERMISSION-INDEPENDENT-R1
PYTHONDONTWRITEBYTECODE=1 python3 repro/reproduce_reds.py
PYTHONDONTWRITEBYTECODE=1 python3 repro/build_manifest.py
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_t9s_permission_falsifiers.py \
  --import-mode=importlib -p no:cacheprovider --junitxml=observations/t9s_preregistered_falsifiers.xml
```

Expected Phase A result: **6 passed, 11 failed, 0 errors, 0 skipped, exit 1** —
the six preregistered RED groups (F1×2, F2×3, F3, F4, F5, F6×3) reproduced on
the pinned T9C adapter, and the six positive controls green. Phase B re-runs the
same frozen suite against T9D.

No real EE12, N9, OC05, N11/N12, Sorok actor, V3, source35 U/Epre or method
adoption is granted by this court.
