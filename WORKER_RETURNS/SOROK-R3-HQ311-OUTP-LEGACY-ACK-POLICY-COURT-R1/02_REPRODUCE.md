# OUTP scoped executable witness reproduction

This is **not** an OUT2, OUT3, OUT4 or OUT5 source implementation test. It demonstrates that the *selected* frozen semantic negative invariants do not decide the two new policy choices. Review the original pinned S01–S28 (native Git blob `782ba75ee94f24908100b1f3464e7035497d546c`) and adopted ADP019 authority before giving any of its fixture return values semantic weight.

```bash
cd outp_policy
python --version
python -m pytest --version
python -m pytest -q test_policy_witness.py --junitxml=policy_witness_junit.xml
```

Observed: Python 3.13.5, pytest 9.0.2, 21 PASS / 0 FAIL / 0 SKIP (exit 0). `policy_witness.py` and `test_policy_witness.py` are new test-only models, not original outbox prototypes.

No exact OUT5 original tests are published on the branch reported by HQ311; do not claim their reproduction.