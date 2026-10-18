# ONECALL-C0 runnable sourcefree court

Run `python -m pytest -q test_onecall_c0_part*.py --junitxml=onecall_replay_junit.xml`. The 4 split test modules together reproduce all 32 tests in the full local source. Run `python onecall_c0.py --mode ONE_CALL --out onecall.json` and repeat for `TWO_CALL` and `FIXED_PACKET`.

No native B3/CAN008/CAN011 module imported and no external LLM API used. Original complete source/JUnit/cold receipts are additionally in the separate downloadable evidence archive. This branch is test-only and awaits independent I2 review.
