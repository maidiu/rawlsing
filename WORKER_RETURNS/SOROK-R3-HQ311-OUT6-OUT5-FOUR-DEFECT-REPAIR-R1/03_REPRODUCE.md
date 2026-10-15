# Reproduce OUT6 at source-free grade

1. From pinned OUT4 author `2afa3022e5551df71b739cf8689e832db85e1196`, extract `stage/outbox_prototype.py` and the unchanged 137-case / OUT4 29-case test modules into a safe isolated directory. Verify original source native Git blob `c7bb4169d43c715de7dd113b24d3ce897e37beab`.
2. Apply `patch -p1 < OUT6_EXACT_SOURCE.patch` inside a directory containing `outbox_prototype.py`. Confirm resulting native blob `aa002cb634e81cb980820c14220a1ab55bc5e015`.
3. Recover exact `test_out3_independent_hostile.py` from independent OUT3's pinned `OUT3_EXECUTED_EVIDENCE.tar.xz` Git blob `a9c4ee7344526fa335605d76d08def2ac5dcba2a`.
4. `xz -dc test_out6_receipt_repair.py.xz > test_out6_receipt_repair.py`; verify native Git blob `c1bbfdddf0cffe9a5988aaa11b13e5065dc01406`.
5. Execute `python -m pytest -q test_sr_28_falsifier_court.py test_rsr_independent.py test_rsr_cold_replay.py test_cold_repair.py test_rto_hostile.py test_out2_cross.py test_out3_independent_hostile.py test_out4_independent_harness.py test_out6_receipt_repair.py --junitxml=after_combined206.xml`. Observed `204 PASS / 2 RED`, exit 1. New OUT6 tests separately `18 PASS`, exit 0. The subprocess cold tests execute actual separate Python processes. Original 2 REDs are expected; no skip/xfail.
6. Exact OUT5 14 original tests are NOT remotely accessible; do not substitute these 18 new tests as exact original acceptance.
