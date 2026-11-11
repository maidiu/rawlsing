# W03-FIRST-CONSUMERS

**Status:** `PASS_TESTED_SOURCEFREE_SCOPE` — 36 selected tests passed; not whole-MCR acceptance.

**Execution/implementation cut:** `1c428d59dc53cb76a19c1502a74cfd3bba00a899`
**Evidence:** `proof_05_consumer_junit.xml` (filtered extraction from the single canonical 99-test run)

## Source and test blobs

- `rawlsing_next/pre553_carrier_execution.py` = `ee9b3af02bfca9238eb72ea45d94073d47769a07`.
- `rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py` = `90d498ef2b1c6e3543e984aa479512cd10afca10`.
- `rawlsing_next/tests/test_pre553_carrier_execution.py` = `bc0db646a803b5bf80dab44d8acb01861d8b3371`.
- `rawlsing_next/tests/test_pre553_i03_grouping.py` = `78683c4098f388eb72d686651b3282b9162e2ed2`.
- `rawlsing_next/tests/test_pre553_w03_w04_completion.py` = `7cd62ffc36091f6e36847f1498d1dc428ebda157`.

## Check and result

```text
python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py \
  rawlsing_next/tests/test_pre553_i03_grouping.py \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py \
  --junitxml=WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/proof_05_consumer_junit.xml
```

Actual canonical execution: **99 passed in 41.63s**; this obligation's filtered JUnit contains **36 passed** cases covering actual I03/I05 typed facts, grouping, Batch/P41 where present, replay, authority/refusal states, and cold-reopen consumers.

## Independent references

- `reviews/combined-code/00_REVIEW.md` at `2959dda3c95b05db40a399d6d746401f434f5a38`: cold release/public-object/consumer material exact for tested fixtures; not whole acceptance.
- `reviews/cold-order-recheck/00_REVIEW.md` at `bcc176d7719e57d1e88b7f395f0280f72b0a74c5`: accepted focused cold-order scope.

## Limits

The filtered JUnit is not a rerun. It establishes tested sourcefree consumer equivalence only, not economic, native/source/science/actor, or protected acceptance.
