# W04-GOVERNED-DEFAULT

**Status:** `PASS_TESTED_SOURCEFREE_SCOPE` — 3 selected policy tests passed; not host deployment authorization.

**Execution/implementation cut:** `1c428d59dc53cb76a19c1502a74cfd3bba00a899`
**Evidence:** `proof_07_policy_junit.xml` (filtered extraction from the single canonical 99-test run)

## Source and test blobs

- `rawlsing_next/_pre553_c11_execution_view.py` = `0f86148f504c06bc694dd980ae1da8913db929b6`.
- `rawlsing_next/tests/test_pre553_w03_w04_completion.py` = `7cd62ffc36091f6e36847f1498d1dc428ebda157`.

## Check and result

```text
python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py -k cache_policy \
  --junitxml=WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/proof_07_policy_junit.xml
```

Actual canonical execution: **99 passed in 41.63s**; this obligation's filtered JUnit contains **3 passed** cases: authorized private root activates default cache; absent/invalid/unowned/oversize policy refuses without writes; spoofed test marker and legacy directory do not authorize writes.

## Independent references

- `reviews/combined-code/00_REVIEW.md` at `2959dda3c95b05db40a399d6d746401f434f5a38`: W04 F01/F02/F03 source-level repairs pass prior counterexamples; no whole acceptance.
- `reviews/persistence/00_REVIEW.md` at `605ce4c409857155eaf8dad7ca4e9c2ae0b15638`: prior policy defects and later repair context.

## Limits

These are sourcefree policy tests, not a real host deployment decision or private-root authorization. The production host policy/root remains an owner matter. No whole-MCR acceptance.
