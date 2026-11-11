# W03-PREVIOUS-CAPITAL

**Status:** `SOURCE_QUALIFIED_CORRECTED_TESTED_SCOPE` — not a final MCR PASS.

**Execution/implementation cut:** `1c428d59dc53cb76a19c1502a74cfd3bba00a899`
**Frozen source cut:** `46b7325637e68f78ccc7487d4b1abc7009c5ac0b`
**Evidence:** `proof_01_prior_blobs.txt`

## Source and test blobs

- Frozen accepted compact production blob: `986f327aa18053edc61bd837cdded02bbf8388d9` (`rawlsing_next/_pre553_c11_execution_view.py`).
- Frozen accepted prior test blob: `8e8effa58579af0c3326ecd4af7e159947abe4ec` (`rawlsing_next/tests/test_pre553_c11_execution_view.py`).
- Current cut production blob: `0f86148f504c06bc694dd980ae1da8913db929b6`.
- Current cut test blob: `7e8bc4e92daecffa72b1fbc740a77b8ef1a6569b`.
- Current W04 companion blobs: `_pre553_w04_cache.py` `4bb7e933f0a5c3f34366ee9e9013b3714a3e4341`; `pre553_parquet_carrier.py` `2c09deeb9b85051cb9d4c36fc12b0a193095e085`.

## Check

```text
git rev-parse 46b7325637e68f78ccc7487d4b1abc7009c5ac0b:rawlsing_next/_pre553_c11_execution_view.py
git rev-parse HEAD:rawlsing_next/_pre553_c11_execution_view.py
git diff --stat 46b7325637e68f78ccc7487d4b1abc7009c5ac0b..HEAD -- \
  rawlsing_next/_pre553_c11_execution_view.py rawlsing_next/_pre553_w04_cache.py \
  rawlsing_next/pre553_parquet_carrier.py \
  rawlsing_next/tests/test_pre553_c11_execution_view.py \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py
```

Result: frozen blobs are identified; current blobs differ by the bounded W04 policy/recovery corrections and private-policy test setup helper. The differences are explicit and covered by `proof_04_topology_junit.xml` (21 topology tests) and `proof_07`/`proof_09` policy/recovery tests.

## Independent references

- Prior accepted compact basis: `9999c0afac5d7d7eb72ad0df602da4b232a49565`.
- Latest combined source review: `2959dda3c95b05db40a399d6d746401f434f5a38` (`reviews/combined-code/00_REVIEW.md`); W04 F01/F02/F03 source-level repairs pass their prior counterexamples, but the review is not whole-MCR acceptance.
- Cold-order focused review: `bcc176d7719e57d1e88b7f395f0280f72b0a74c5` (`ACCEPT_AT_CC_F01_SCOPE`).

## Limits

This is source/blob qualification and tested-scope evidence only. It does not establish whole-MCR, economic, native/source/science/actor, or protected acceptance. The frozen 43-pass history is prior capital, not current final proof.
