# D r5 evidence and commands

## Tests

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_original35_operations.py
# 9 passed in 30.24s

PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_original35_execution.py
# 3 passed in 121.43s (manifest/path/no-resolver, not a positive wrapper proof)
```

## Sourcefree production-wrapper probe

Faithful TEST_ONLY_SOURCEFREE SAV/config, selected `A/B/Y`, coordinate `G`;
actual `execute_native_compiler_source`, current compiler/facts, no mocks.

- Positive, resolver sequence `A,A,A,A`: accepted; 30 facts, 15 expected
  operations, 18 candidates, anti/op-anti true, `native=false`.
- Changed decision at final consumer call, sequence `A,A,A,B`: refused with
  `SOURCE_READ_DECISION_CHANGED_AFTER_CONSUMER`.
- Changed decision between wrapper pre-call and decode pre-call, sequence
  `A,B,B,A`: **accepted** with the same 30/15/18 result. B differs only in
  `decision_ref` and remains `CURRENT_GRANTED`; the post-consumer comparison
  returns to A.
- Revoked final decision, sequence `A,A,A,revoked`: refused.

The blocking issue is that `before_decision` is an extra resolver call, while the
decoder resolves its own pre-decision; the post check does not bind the decision
actually used by `decode_with_source_read_permission`.

## Held/unselected alias

The B suite's held-Y positive and full-plan/partial-bundle refusal pass. The
sourcefree positive still produces 15 expected operations, so the alias repair
does not drop eligible operations to bypass the missing native ref.

## Preserved floors

- Current route-qualified frontier: 7 sources / 694 operations / 683 eligible /
  11 held; 28 sources with no explicit route-qualified frontier.
- Historical non-F1 scope remains 20 sources / 991 operations.
- Route: 676 eligible / 4,705 unknown / 249 unavailable.
- Plan: 18,276 items / 18,413 slots / 18,467 operations.
- F exact positive receipt: 30 facts / 15 ops / 18 candidates; compilation
  `fdc6f3f9…`; ledger `233d2272…`. The independent probe matched counts and
  anti-joins on a distinct sourcefree config, not byte-identical F fixture hash.

## Boundaries

No original data, original 600 s decode, full-estate floor, E/native handshake,
native facts, science or protected acceptance. No product/test/guide/progress/
controller edit; no code repair or self-acceptance.
