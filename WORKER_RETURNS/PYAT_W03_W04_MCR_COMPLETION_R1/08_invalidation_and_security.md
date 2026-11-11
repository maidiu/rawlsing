# W04-AUTHORITY-INVALIDATION

**Status:** `PASS_TESTED_SOURCEFREE_SCOPE` — 1 selected invalidation test passed; not whole-MCR acceptance.

**Execution/implementation cut:** `1c428d59dc53cb76a19c1502a74cfd3bba00a899`
**Evidence:** `proof_08_invalidation_junit.xml` (filtered extraction from the single canonical 99-test run)

## Source and test blobs

- `rawlsing_next/_pre553_c11_execution_view.py` = `0f86148f504c06bc694dd980ae1da8913db929b6`.
- `rawlsing_next/tests/test_pre553_w03_w04_completion.py` = `7cd62ffc36091f6e36847f1498d1dc428ebda157`.

## Check and result

```text
python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_c11_execution_view.py \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py -k invalidation \
  --junitxml=WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/proof_08_invalidation_junit.xml
```

Actual canonical execution: **99 passed in 41.63s**; this obligation's filtered JUnit contains **1 passed** case covering source/projection/authority/release/replay/schema invalidation and stale/poison refusal paths.

## Independent references

- `reviews/combined-code/00_REVIEW.md` at `2959dda3c95b05db40a399d6d746401f434f5a38`: bounded source-level findings.
- `reviews/persistence/00_REVIEW.md` at `605ce4c409857155eaf8dad7ca4e9c2ae0b15638`: prior invalidation/persistence review context.

## Limits

The filtered JUnit is not a rerun. It does not establish whole-MCR, economic, native/source/science/actor, or protected acceptance.
