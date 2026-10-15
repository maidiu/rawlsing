# OCR1 sourcefree reproduction

Unpack archive in a new empty directory and run:

```bash
cd source
python -m pytest -q test_custody_hostiles.py test_positive_lifecycle.py --junitxml=../review/original_31_junit.xml
# expected: exit 0, 31 PASS
python -m pytest -q test_ocr1_independent_hostile.py --junitxml=../review/independent_hostile_junit.xml
# expected: exit 1, 15 PASS and 30 FAIL (45 cases)
```

Candidate source and original tests are exact files extracted from private repo OC1 commit `19438890e43153e2bc4a1ad271b5e19bcef33e1e`. Compute native Git blob preimage with `hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()` and compare `02_EXECUTION_MATRIX.json`. The original four files must match their pinned hashes. Import provenance is the `source/` staging directory, not an accepted implementation module. New reviewer tests execute actual API calls; 30 failures should not be hidden with xfail.

Only source-free fictional corpus and mock signer fixtures are included. No external original survey data, API use, issuance, trusted credentials or real custody.
