# OUT8 runnable patch + tests
Exact inputs OUT6 final source Git blob `aa002cb634e81cb980820c14220a1ab55bc5e015` and all original tests from OUT7. Extract `OUT8_REPRO_SOURCE_AND_TESTS.tar.xz` (Git blob `f6f54252e3faff80cf1321937bf306446db76a77`); apply `patch -p1 < OUT8_EXACT_SOURCE.patch` from the directory containing `outbox_prototype.py`. The patch is relative `a/outbox_prototype.py`/`b/outbox_prototype.py`. Verify resulting Git blob `331840768ce0b5f6f73e5e93094ca0d217ddaebf` and new test Git blob `d23e6cfc441de6fee11855966b16cc7ba6fd544a`.

```bash
python -m pytest -q test_sr_28_falsifier_court.py test_rsr_independent.py test_rsr_cold_replay.py test_cold_repair.py test_rto_hostile.py test_out2_cross.py test_out3_independent_hostile.py test_out4_independent_harness.py test_out6_receipt_repair.py test_out7_independent_hostile.py test_out8_restored_state_repair.py --junitxml=combined247.xml
# actual 245 PASS, 2 preserved historical RED, exit 1
```
Source-free only; exact OUT5 14 unavailable. Full actual JUnit/stdout are retained in local delivered archive; not asserted remotely included.
