# OC4 source-free reproduction

Copy `repro/custody_protocol.py` from this return into a NEW isolated source-free stage, together with pinned:
- OC1: `test_custody_hostiles.py`, `test_positive_lifecycle.py`, `dummy_corpus.py` at `19438890e43153e2bc4a1ad271b5e19bcef33e1e`
- OCR1: `test_ocr1_independent_hostile.py` from `aba637265bea2358790fea50d0e7abc98141e472`
- OC2: `test_oc2_regressions.py` from `a61d5794271038fb20c94a75eaee401a66613ce9`
- OC3: exact `test_oc3_independent_hostile.py` in archive `OC3_REMOTE_CORE_EVIDENCE.tar.xz` Git blob `068b158363b96d5a7cdc03eb059efb8a8d159b26`

Commands (all actually executed by OC4 worker):
```bash
python -m pytest -q test_custody_hostiles.py test_positive_lifecycle.py test_ocr1_independent_hostile.py test_oc2_regressions.py test_oc3_independent_hostile.py --junitxml=oc4_combined.xml
# exit 1: 121 PASS / 10 FAIL
python -m pytest -q test_oc3_independent_hostile.py --junitxml=oc4_oc3.xml
# exit 1: 34 PASS / 2 FAIL
python -m pytest -q test_oc4_repair_controls.py --junitxml=oc4_new.xml
# exit 0: 36 PASS
```
For prior 115/16 use the pinned original OC2 candidate blob `f117f380c524db5b1eae0ce280be23f1c4bf2c23` with all 131 tests unchanged.
