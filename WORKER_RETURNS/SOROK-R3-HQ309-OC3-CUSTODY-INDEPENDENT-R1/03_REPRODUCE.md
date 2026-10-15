# OC3 independent evidence reproduction

Pin OC2 candidate from `a61d5794271038fb20c94a75eaee401a66613ce9` and original/independent tests from OC1 `19438890e43153e2bc4a1ad271b5e19bcef33e1e` and OCR1 `aba637265bea2358790fea50d0e7abc98141e472`. Verify native blobs in `02_HASH_RECEIPTS.json`; extract the independently authored new test source from `OC3_REMOTE_CORE_EVIDENCE.tar.xz`. The package also contains the actual combined 131-case and new 36-case JUnit XML. All frozen sources were executed with Python 3.13.5 and pytest 9.0.2 in an isolated source-free stage, not a production import.

```bash
python -m pytest -q test_custody_hostiles.py test_positive_lifecycle.py test_ocr1_independent_hostile.py test_oc2_regressions.py --junitxml=oc3_inherited_95.xml
python -m pytest -q test_oc3_independent_hostile.py --junitxml=oc3_new_hostile.xml
python -m pytest -q test_custody_hostiles.py test_positive_lifecycle.py test_ocr1_independent_hostile.py test_oc2_regressions.py test_oc3_independent_hostile.py --junitxml=oc3_combined.xml
```

Expected real exit codes are **1, 1, 1** with 89/6, 26/10 and 115/16 respectively. The six inherited failures remain actual REDs; no test is waived. The complete local evidence bundle (separately user-linked) preserves all three commands' raw stdout/JUnit, full 131-case JSON matrix and exact pinned module bytes; this pushed compact archive preserves combined/new JUnit, new Python test, prereg and hash receipts. `OCR1 C07` persisted recovery remains NOT_REACHED. No real grants, signers, model calls or acceptance.
