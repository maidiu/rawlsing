# Evidence, commands, grading and reproducibility

All commands executed in an isolated local Browser Python/pytest runtime after verifying the source and test Git blobs. These are actual local executions, not copied author claim totals.

```bash
# Extract only the two exact authenticated frozen M1/I2 archives to isolated suites.
python -m pytest -q suites/original/test_kernel.py --junitxml=original37.xml
(cd suites/original && PYTHONPATH=. python -m pytest -q ../i2/test_i2_strict.py --junitxml=../../original_i2.xml)
(cd suites/m2 && python -m pytest -q test_m2.py --junitxml=../../m2_41.xml)
(cd suites/m2 && python -m pytest -q test_kernel.py --junitxml=../../m2_old37.xml)
(cd suites/m2 && python -m pytest -q test_i2_strict.py --junitxml=../../m2_i2.xml)
(cd suites/m2 && python -m pytest -q test_m3_independent.py --junitxml=../../m3_independent.xml)
(cd suites/m2 && python -m pytest -q test_m3_unresolved.py --junitxml=../../m3_unresolved.xml)
```

Observed outcomes respectively: 37/37; 14 PASS/9 RED; 41/41; 18 PASS/19 RED; 13 PASS/10 RED; **32/32 PASS**; **3 RED**. No source/test bytes were edited in original frozen suites. Import used the pinned exact M2 kernel path. See machine receipt for actual stdout/JUnit digests. All three strict P0 failures are `DID NOT RAISE <class 'kernel.Refusal'>`.

The user's portable evidence bundle, `SOROK_HQ329_M3_INDEPENDENT_COURT.zip`, includes complete new 32-positive and three-negative Python test source, seven stdout logs, seven JUnit XML files, case matrix, and environment passport. SHA-256 `94a3d5827ed3b0541285ac30928ddc899fe8b2474e1d8e018c8e93591fd45c3f`. Its ZIP bytes exist as a separate conversation attachment, **not** in this repository branch. The three essential REDs are also directly reproduced by the checked-in portable `05_SOURCE_PREIMAGE_RED_REPRODUCER.py` if an executor stages exactly M2's pinned `kernel.py`.

Boundary: passing noncausal candidate tests establishes representational/mechanical viability, **not** real child psychology, signed source custody, original survey or native PFF/V3 actor. M3 is **not formally fresh independent** because this conversation handled M2 implementation; separate personnel/session remains required for acceptance.
