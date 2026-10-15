# OC5 reproducibility and explicitly missing proof
Only a single sourcefree private-repository Git closure qualifies the full commissioned court. Required exactly pinned paths:

- OC4 `repro/custody_protocol.py` from `0caaec590f6a8bf6744f22dc9c948c5fe233bc94`, required Git blob `af2b7e943018077cb36808b5af1cd67704624bec`;
- OC1 `repro/dummy_corpus.py`, `repro/test_custody_hostiles.py`, `repro/test_positive_lifecycle.py` from `19438890e43153e2bc4a1ad271b5e19bcef33e1e`;
- OCR1 `test_ocr1_independent_hostile.py` from its pinned evidence `aba637265bea2358790fea50d0e7abc98141e472` (archive decompression required);
- OC2 `repro/test_oc2_regressions.py` from `a61d5794271038fb20c94a75eaee401a66613ce9`;
- OC3 `test_oc3_independent_hostile.py` from compressed evidence at `9cd47a829473a6e92392582b4f01f2c564aa5dce`, archive native Git blob `068b158363b96d5a7cdc03eb059efb8a8d159b26` and reported archive SHA256 `7a3d7913a5c388569f654aaf83a0a64c9b16de28065551a3e7a7d3749be33837`;
- OC4 `repro/test_oc4_repair_controls.py` from the OC4 return, blob `c139a877aa4586ec5ab729d333c40037840721d4`;
- OC5 new test file in this return.

Verify exact native blob with `hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()`; inspect imported `custody_protocol.__file__` and `dummy_corpus.__file__`. Put those source files only in an isolated permitted sourcefree temporary directory (do NOT execute original survey sources).

Then run:
```bash
python -m pytest -q test_custody_hostiles.py test_positive_lifecycle.py test_ocr1_independent_hostile.py test_oc2_regressions.py test_oc3_independent_hostile.py --junitxml=oc5_inherited.xml
python -m pytest -q test_oc4_repair_controls.py --junitxml=oc5_oc4.xml
python -m pytest -q test_oc5_candidate_hostiles.py --junitxml=oc5_new.xml
```
Retain stdout/stderr, JUnit, exact per-case matrix, hashes/import paths and verdict. In this OC5 session, these commands were **not executed**, so any purported 131/36/new counts except the isolated excerpt 2/4 are NOT OC5 evidence. No new permission or trust registry follows from running them.
