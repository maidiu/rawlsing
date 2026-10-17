# Actual author-side test history

Commands were run in the Browser Python 3.13.5 / pytest 9.0.2 container with the standalone stdlib P1 candidate, no native rawlsing checkout.

1. `python make_fixtures.py` — PASS, 13 fabricated frozen JSON fixtures and one authored policy produced with exact content hashes.
2. `python -m pytest -q tests/test_p1_contract.py --junitxml=evidence/p1_junit.xml` — initial 53 passed / 0 failed, after first independent-history/actor tests.
3. Added `prospective_participants`, strict future-fact and speaker/visibility constraints; rerun initially **52 passed / 1 failed**: peer-not-exposed fixture now failed at earlier `ACTOR_VISIBILITY_UNSUPPORTED` rather than the prior `ACTOR_KNOWLEDGE_LIMIT`. This is test-precedence correction, not a claimed new psychological rule. The original expected order was corrected, with the guard retained.
4. Expanded preregistered-style hostile cells — `65 passed / 0 failed`.
5. Added CLI smoke test, docs and final reexecution: `python -m compileall -q p1_contract.py run_demo.py make_fixtures.py tests/test_p1_contract.py` PASS; `python -m pytest -q tests/test_p1_contract.py --junitxml=evidence/p1_junit.xml` — **66 passed / 0 failed / 0 skipped**; `python run_demo.py --coordinate 11` PASS, output at `evidence/p1_demo_receipt.json`.

Claim is *author source-free deterministic court PASS*, not native/independent acceptance. No original 35-wave data or CAN008/CAN011/ADP019/ADP020 production runtime was executed. Exact frozen fixtures and test source are in the same return.
