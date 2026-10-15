# OUT7 reproduction

Pin reviewed OUT6 source at 673233571b7d899c309dd26f9b9cd2508404c0b6, native Git blob aa002cb634e81cb980820c14220a1ab55bc5e015. Exact original OUT3 binary Git blob a9c4ee7344526fa335605d76d08def2ac5dcba2a, SHA256 fc876b665bd9af6328deec86aa66e93ec0eebf9048ca7a5a0d7d0630cd48bddd. All original file blob hashes in core archive. Recover the new test from source/test_out7_independent_hostile.py therein.

Run in a clean isolated sourcefree Python+pytest stage:

```bash
python -m pytest -q test_sr_28_falsifier_court.py test_rsr_independent.py test_rsr_cold_replay.py test_cold_repair.py test_rto_hostile.py test_out2_cross.py test_out3_independent_hostile.py test_out4_independent_harness.py test_out6_receipt_repair.py --junitxml=inherited206.xml
python -m pytest -q test_out7_independent_hostile.py --junitxml=new21.xml
python -m pytest -q test_sr_28_falsifier_court.py test_rsr_independent.py test_rsr_cold_replay.py test_cold_repair.py test_rto_hostile.py test_out2_cross.py test_out3_independent_hostile.py test_out4_independent_harness.py test_out6_receipt_repair.py test_out7_independent_hostile.py --junitxml=combined227.xml
```

Real recorded exits 1,1,1 (204 pass/2 fail; 17 pass/4 fail; 221 pass/6 fail). Complete original+new JUnit and logs and 227-case index packaged in OUT7_REMOTE_CORE_EVIDENCE.tar.xz. No waived/skipped tests.
