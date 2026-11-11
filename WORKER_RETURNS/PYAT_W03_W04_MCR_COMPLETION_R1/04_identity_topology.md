# W03-SEMANTIC-TOPOLOGY

**Status:** `PASS_TESTED_SOURCEFREE_SCOPE` — 21 selected tests passed; not whole-MCR acceptance.

**Execution/implementation cut:** `1c428d59dc53cb76a19c1502a74cfd3bba00a899`
**Evidence:** `proof_04_topology_junit.xml` (filtered extraction from the single canonical 99-test run)

## Source and test blobs

- `rawlsing_next/_pre553_c11_execution_view.py` = `0f86148f504c06bc694dd980ae1da8913db929b6`.
- `rawlsing_next/tests/test_pre553_c11_execution_view.py` = `7e8bc4e92daecffa72b1fbc740a77b8ef1a6569b`.
- `rawlsing_next/tests/test_pre553_w03_w04_completion.py` = `7cd62ffc36091f6e36847f1498d1dc428ebda157`.

## Check and result

```text
python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_c11_execution_view.py \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py \
  --junitxml=WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/proof_04_topology_junit.xml
```

Actual canonical execution: **99 passed in 41.63s**; this obligation's filtered JUnit contains **21 passed** cases covering exact topology, zero/missing/rank/routing/non-event families, replay, mutable-ref refusal, and cache stale/poison negatives.

## Independent references

- `reviews/cold-order-recheck/00_REVIEW.md` at `bcc176d7719e57d1e88b7f395f0280f72b0a74c5`: `ACCEPT_AT_CC_F01_SCOPE`.
- `reviews/combined-code/00_REVIEW.md` at `2959dda3c95b05db40a399d6d746401f434f5a38`: bounded source-level findings; no whole 12-ID acceptance.

## Limits

The JUnit is a filtered view of the one canonical run, not a rerun. It is S2 sourcefree evidence, not a native/source/science or protected acceptance.
