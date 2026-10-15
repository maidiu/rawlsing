# Sourcefree reproduction — HQ301 RTO independent I2 court

Requires Python 3.13+/pytest 9 and an isolated unpacking of the exact HQ300 archive pinned by Git blob `61f5b960ef05a74d10db11b0fae2bca703ae0ae4`. Extract `test_rto_hostile.py` and `rto_cold_driver.py` from the HQ301 evidence bundle next to, or PYTHONPATH-pointed to, that candidate source. No accepted modules or real sources are used.

Commands executed, with the reviewer staging paths replaced by environment-independent paths:

```
PYTHONPATH=./candidate python -m pytest -q ./candidate/test_sr_28_falsifier_court.py ./candidate/test_rsr_independent.py ./candidate/test_rsr_cold_replay.py ./candidate/test_cold_repair.py --junitxml=baseline56.xml
# expected: exit 1 / 55 pass, 1 fail (S27 only)

PYTHONPATH=./candidate python -m pytest -q ./review/test_rto_hostile.py --junitxml=hostile_full.xml
# expected: exit 1 / 28 pass, 29 fail, no xfail/skip

PYTHONPATH=./candidate python -m pytest -q ./candidate/test_sr_28_falsifier_court.py ./candidate/test_rsr_independent.py ./candidate/test_rsr_cold_replay.py ./candidate/test_cold_repair.py ./review/test_rto_hostile.py --junitxml=combined_113.xml
# expected: exit 1 / 83 pass, 30 fail
```

`test_rto_hostile.py` uses a dedicated fresh subprocess `rto_cold_driver.py` executed with `sys.executable` and `os._exit(79)`. Its 4 executed cold cases do not rely on HQ300's prior `cold_repair.py` for their kill/recovery assertions.

`SOURCEFREE_STANDALONE_PYTEST != ACCEPTED_ADP019 != V3_ACTOR != REAL_USER_PERCEPTION != EXACTLY_ONCE_NETWORK`.
