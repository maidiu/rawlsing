# W04-ATOMIC-LIFECYCLE

**Status:** `PASS_TESTED_SOURCEFREE_SCOPE` — 7 selected recovery tests passed; not whole-MCR acceptance.

**Execution/implementation cut:** `1c428d59dc53cb76a19c1502a74cfd3bba00a899`
**Evidence:** `proof_09_recovery_junit.xml` (filtered extraction from the single canonical 99-test run)

## Source and test blobs

- `rawlsing_next/pre553_parquet_carrier.py` = `2c09deeb9b85051cb9d4c36fc12b0a193095e085`.
- `rawlsing_next/tests/test_pre553_w03_w04_completion.py` = `7cd62ffc36091f6e36847f1498d1dc428ebda157`.

## Check and result

```text
python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py -k recovery \
  --junitxml=WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/proof_09_recovery_junit.xml
```

Actual canonical execution: **99 passed in 41.63s**; this obligation's filtered JUnit contains **7 passed** cases covering aborted/torn publication, concurrent builders, directory/file fsync failure, retention orphan cleanup, and carrier aborted publish.

## Independent references

- `reviews/persistence/00_REVIEW.md` at `605ce4c409857155eaf8dad7ca4e9c2ae0b15638`: W04 persistence findings; later repairs are current tested state, not reopened final acceptance.
- `reviews/combined-code/00_REVIEW.md` at `2959dda3c95b05db40a399d6d746401f434f5a38`: bounded source-level review.

## Limits

The filtered JUnit is not a rerun. It does not establish 100k economics or protected/native acceptance.
