# T9S — independent temporal authority court (Phase A + Phase B complete)

Phase A froze the counterexamples before T9D existed; Phase B executed them and
the original suites against the pushed T9D repair
`d4969f513be0b3691f1bbf45813d17fc171a51a7` and returned
`ACCEPT_SOURCEFREE_TEMPORAL_AUTHORITY_PROVENANCE_REPAIR`
(`05_PHASE_B_INDEPENDENT_VERDICT.md`).

## Layout

| path | meaning |
| --- | --- |
| `00_PHASE_A_PREREGISTRATION_AND_COUNTEREXAMPLES.md` | Phase A narrative and gate |
| `01_T9S_PRECOMMITTED_PERMISSION_ORACLE.json` | frozen six falsifiers + six controls |
| `02_PHASE_A_SOURCE_MANIFEST.json` | T9C source pins (Phase A) |
| `03_PHASE_A_COMPLETION_AND_GATE_STATUS.md` | Phase A completion + WAIT record |
| `04_PHASE_A_PUBLICATION_RECEIPT.json` | Phase A remote readback |
| `05_PHASE_B_INDEPENDENT_VERDICT.md` | **final independent verdict** |
| `06_PHASE_A_TEST_CORRECTIONS.md` | two Phase A test-authoring bug fixes (transparency) |
| `tests/test_t9s_permission_falsifiers.py` | 17 preregistered cases (17/0 on T9D) |
| `tests/test_t9s_postinspection_controls.py` | 12 post-inspection controls (12/0) |
| `phase_b/` | pinned T9D candidate source + all frozen suites + SOURCE_MANIFEST |
| `repro/stage_phase_b.py` | pins the exact T9D source under phase_b/ |

## Reproduce Phase B

```sh
cd WORKER_RETURNS/PYAT-R27-T9S-TEMPORAL-PERMISSION-INDEPENDENT-R1
PYTHONDONTWRITEBYTECODE=1 python3 repro/stage_phase_b.py
export PYTHONPATH="$PWD/phase_b/pinned_candidate:$PWD/phase_b/pinned_candidate/native"
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_t9s_permission_falsifiers.py \
  --import-mode=importlib -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_t9s_postinspection_controls.py \
  --import-mode=importlib -p no:cacheprovider
```

No real EE12, N9, OC05, N11/N12, Sorok actor, V3, source35 U/Epre or method
adoption is granted by this court.
