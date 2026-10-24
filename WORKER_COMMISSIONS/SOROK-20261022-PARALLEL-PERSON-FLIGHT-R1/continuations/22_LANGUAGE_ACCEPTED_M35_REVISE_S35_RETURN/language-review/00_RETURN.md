# Language counterexample-access closure — ACCEPT

Decision: **ACCEPT_LANGUAGE_COUNTEREXAMPLE_ACCESS_CLOSURE**.

## Exact cut

- Corrected language-worker cut: `8d2920da951f98cd8246d7c34cac777928e0c732`.
- Prior reviewed cut: `7ed7dc9afccffb3f27e78832160ab83ac02ffc7d`.
- Base: `76961d2e58e7139ddd63f1758aea19a8026b375f`.
- Correction diff is exactly `LANGUAGE_MEDIATION_R1/language_mediation/index.py`
  (5 added lines) and `LANGUAGE_MEDIATION_R1/tests/test_language_mediation.py`
  (44 added test lines).
- Fetched into a disposable clone; no writes to the manual worker or controller
  attachment worktree. No product code edits, provider/domain launch, or native
  grant.

## Verification

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=LANGUAGE_MEDIATION_R1 \
  python3 -m pytest -q LANGUAGE_MEDIATION_R1/tests
21 passed in 6.16s
```

The preserved original reviewer oracle
`SOROK_REVIEW/oracles/r59_language_counterexample_access.py` was run against the
corrected fixture and returned **2 PASS / 0 FAIL**:

- wrong-branch counterexample receipt after revocation: relation remains
  `INVALID` / `COUNTEREXAMPLE_NOT_ACCESSIBLE`;
- wrong-hash counterexample receipt after revocation: relation remains
  `INVALID` / `COUNTEREXAMPLE_NOT_ACCESSIBLE`.

The added affected test also verifies lawful restoration: after restoring the
real counterexample receipt, both valid relations return and the next
`say(TRIGGER)` resumes `SELF_RELIANCE` with `session.verify()["ok"] is True`.
All 21 tests pass; no historical suite was recensused.

## Result

`_accessible` now requires the counterexample event to exist and the receipt's
`source_event_hash` and `branch_id` to match the current branch before access
is granted. The prior forged-receipt restoration bypass is closed, while lawful
restore access continues to work. The remaining behavior stays finite
`TEST_ONLY` language mediation, not general translation or native/science
authority.

## Receipt

- 21-test output: `evidence/language-8d-tests21.out` SHA-256 `0bb0e760…`.
- Original oracle output against corrected fixture:
  `evidence/language-8d-counterexample.json` SHA-256 `c05c2c4d…`;
  **2 PASS / 0 FAIL** (the oracle's static cut field remains the prior cut).
- Corrected `index.py` SHA-256 `7fe64953…`; test file SHA-256 `61e233fb…`.
- Preserved oracle SHA-256 `d67fe72e…`.
- No provider/domain/native/production action was performed.
