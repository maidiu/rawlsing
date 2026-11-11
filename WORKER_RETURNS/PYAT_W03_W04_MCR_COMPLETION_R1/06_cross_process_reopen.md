# W04-COLD-PERSIST-REOPEN

**Status:** `PASS_TESTED_SOURCEFREE_SCOPE` — 17 selected tests passed; not whole-MCR acceptance.

**Execution/implementation cut:** `1c428d59dc53cb76a19c1502a74cfd3bba00a899`
**Evidence:** `proof_06_reopen_junit.xml` (filtered extraction from the single canonical 99-test run)

## Source and test blobs

- `rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py` = `90d498ef2b1c6e3543e984aa479512cd10afca10`.
- `rawlsing_next/tests/test_pre553_w03_w04_completion.py` = `7cd62ffc36091f6e36847f1498d1dc428ebda157`.
- `rawlsing_next/pre553_parquet_carrier.py` = `2c09deeb9b85051cb9d4c36fc12b0a193095e085`.

## Check and result

```text
python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py \
  --junitxml=WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/proof_06_reopen_junit.xml
```

Actual canonical execution: **99 passed in 41.63s**; this obligation's filtered JUnit contains **17 passed** cases covering cold reopen/new-process behavior, exact release selection, canonical Parquet integrity, and safe recovery negatives.

## Independent references

- `reviews/combined-code/00_REVIEW.md` at `2959dda3c95b05db40a399d6d746401f434f5a38`: bounded cold release and persistence findings; no whole acceptance.
- `reviews/persistence/00_REVIEW.md` at `605ce4c409857155eaf8dad7ca4e9c2ae0b15638`: W04 lane review with prior findings; later source repairs are covered by the current tests, not reopened as final acceptance.

## Limits

The filtered JUnit is not a rerun. It does not establish 100k economics, native/source/science/actor rights, or protected receiving.
