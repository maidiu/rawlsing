# Actual author-side test history

Commands were run in the Browser Python 3.13.5 / pytest 9.0.2 container with the standalone stdlib P1 candidate, no native rawlsing checkout.

1. `python make_fixtures.py` — PASS, 13 fabricated frozen JSON fixtures and one authored policy produced with exact content hashes.
2. `python -m pytest -q tests/test_p1_contract.py --junitxml=evidence/p1_junit.xml` — initial 53 passed / 0 failed, after first independent-history/actor tests.
3. Added `prospective_participants`, strict future-fact and speaker/visibility constraints; rerun initially **52 passed / 1 failed**: peer-not-exposed fixture now failed at earlier `ACTOR_VISIBILITY_UNSUPPORTED` rather than the prior `ACTOR_KNOWLEDGE_LIMIT`. This is test-precedence correction, not a claimed new psychological rule. The original expected order was corrected, with the guard retained.
4. Expanded preregistered-style hostile cells — `65 passed / 0 failed`.
5. Added CLI smoke test, docs and final reexecution: `python -m compileall -q p1_contract.py run_demo.py make_fixtures.py tests/test_p1_contract.py` PASS; `python -m pytest -q tests/test_p1_contract.py --junitxml=evidence/p1_junit.xml` — **66 passed / 0 failed / 0 skipped**; `python run_demo.py --coordinate 11` PASS, output at `evidence/p1_demo_receipt.json`.

Claim is *author source-free deterministic court PASS*, not native/independent acceptance. No original 35-wave data or CAN008/CAN011/ADP019/ADP020 production runtime was executed. Exact frozen fixtures and test source are in the same return.


## Completion audit

6. Reproduced all originally recorded controls from the separately fetched/uploaded author bundle at the previously pushed SHA (`a9c4398346dee7eefa47fa2fa944d5330deac5c4`) — 66 PASS / 0 FAIL / 0 SKIP.
7. Added eight hostile controls in `tests/test_p1_completion.py` and **observed 5 RED / 3 PASS** before any repair. Preserved verbatim in `evidence/p1_completion_initial_red.log`.
8. Patched only `p1_contract.py`, retaining the original 66 frozen test bytes and thirteen fixtures. Complete rerun: **74 PASS / 0 FAIL / 0 SKIP** with JUnit and log. Repeated the deterministic CLI demonstration; selection output equals pre-repair bytes; evaluation adds a new digest field. Compileall PASS. No native integration or independent I2 reviewer was executed.
