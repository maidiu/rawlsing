# Draft 713 evidence and commands

## Blob verification

`revisions/r1/01_ACCEPTED_HEADS_AND_BLOBS.json` has 51 selected paths. Independent
comparison of `HEAD:path` against each qualified `source_commit:path`, integrated
blob and source blob: **51 exact, 0 bad**. Key blobs:

- D execution `83ade3390af61f3c176a35caf763b715c673e47f` from `0b38f3c7…`;
- D test `f492abf44c4c224cf02af82112f25b7f829f71d7` from `0b38f3c7…`;
- A production `bc84799e…`; A test `c84ea32d…`;
- E code `d0192e190189b578948d79fe6fedb7953f92f697` from `f708b468…`.

`git diff --name-status fce43498e..HEAD` has 72 additions and **0 protected
modified/deleted paths**. Newer D R11+ joint request code is absent.

## D actual target

```text
TMPDIR=$PWD/.local-logs/pyat-universal35/draft713-review/tmp PYTHONDONTWRITEBYTECODE=1 \
/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -o addopts= \
-p no:cacheprovider --tb=short -v \
rawlsing_next/tests/test_pre553_original35_execution.py::test_governed_facts_queries_become_exact_cold_e_envelopes
# 1 passed in 1.66s
```

Target assertions: 30 facts / 30 envelopes / 30 typed arity refusals / 0
profiles; explicit permission round-trip; no artifact without permission; missing
query preserves prior artifact and leaves no staged temp; replay tamper refuses.

Independent actual-wrapper probe:

```text
positive PASS: 30 facts / 15 ops / 18 candidates
A,A,B refused SOURCE_READ_DECISION_CHANGED_AFTER_CONSUMER
new root: no envelope artifact
same root: existing valid artifact unchanged; no .staged-tmp
```

## Reused receipts

F-reported and accepted unchanged: A correction tests 13 passed; D execution
tests 5 passed; E codec 20 passed. No discrepancy was found, so they were not
rerun. The joined target was run independently.

## Preserved limits

Actual original D facts: 0; SRC15/650s negatives preserved, not rerun. C adapter
join: NOT_RUN; no C scale/performance claim. E authentic profile/handshake:
NOT_CLAIMED. No all35/native/S3/science/protected adoption, source grant,
protected merge/CAS, original-data or whole-estate run.
