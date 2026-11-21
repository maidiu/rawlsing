# O-INDEX living intake test and source-receipt — 2026-11-21

**Historical receipt.** The 12-case accession execution below applies to its original files. At `3779878d2`, 14 cases passed and the authenticated audit returned zero errors with eight closed-unmerged holds. That check is pinned to `3779878d2`; later documentary revisions require reconciliation.


**Executed at exact source blobs (not independent review, not protected receiving).** Local isolated Python sandbox in this ChatGPT session; **Python 3.13.5**, interpreter `/opt/pyvenv/bin/python3`. The GitHub documentary branch is not a local Git worktree: source bytes were authored locally and the two source Git blob IDs were independently read back from the isolated GitHub branch. This is a bounded *verifier unit* execution, not the R3 original complete index tests or authenticated live GitHub scan.

| File | Source byte count | Git blob SHA (local `git hash-object` = GitHub readback) |
|---|---:|---|
| `check_live_receiving.py` | 11229 | `cd7cdfa641e9025644137f1d3eb77921af0f1362` |
| `test_live_receiving.py` | 4132 | `f136ea6763526be3d2a8972c939f3173de88aa2a` |

**Executed commands and results:**

```text
$ python3 --version
Python 3.13.5

$ python3 -m unittest -q test_live_receiving.py
----------------------------------------------------------------------
Ran 12 tests in 0.002s

OK

$ python3 -m py_compile check_live_receiving.py test_live_receiving.py
exit 0
```

**Causal cases actually tested:** snapshot positive; moved HEAD; stale applied-to-head test; unseen new relevant PR; closed unreceived PR; missing owner; false native science promotion; contradictory MD/JSON revisions; incomplete observation scope; unsupported `INDEPENDENTLY_REVIEWED` promotion; stale readable MD versus changed ledger blob; superseded-without-successor and missing functional-conservation denial.

**Distinct, NOT EXECUTED here:** inherited R3 source validator `validate_index.py` + 21 original author tests; live Git-object refresh `verify_source_manifest.py` requiring full Git checkout; `check_live_receiving.py --live` requiring scoped authenticated GitHub token; executing Nadia/REMONT sourcefree applications; protected MD/JSON CAS or separate hostile reviewer. Eleven original R3 Git blob IDs were checked at the GitHub connector from PR #561 and preserved byte-identically, but **not** asserted to have passed local Git refresh/test suite in this receipt.

**Result:** `EXECUTED_AT_SOURCE_BLOB_SCOPED_CHECKER_12_PASS`. A forged standalone snapshot can make a local fixture appear consistent; only authenticated `--live` plus issuer review can earn live-state status. Any detected new material return must receive an exact-source fate; missing privileges trigger `HQ_CURRENTNESS_HOLD`. Original P/Q REMONT queue remains its owner. No current worker interrupted, no protected branch modified.
