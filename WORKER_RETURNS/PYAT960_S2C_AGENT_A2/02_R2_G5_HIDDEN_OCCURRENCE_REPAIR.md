# PYAT S2-C A2 R2 — bounded G5 hidden-occurrence causal repair

## Frozen counterexample (independent nonauthor receiving)

The independent G5 reviewer executed exact A2 R1 `8375e260e55da09b3c5a89122839d8c7deba67bb` in the qualified Linux Lima VM: **29/29 focused and 91/91 inherited PASS**. Its hostile G3 case nevertheless reproduced a material defect.

With a lawful two-event candidate, reviewer removed one row from `event_locator.parquet`, set `event_locator_count=1` and `family_counts["RespondentEvent"]=1`, rehashed the locator member and repinned the manifest SHA while preserving both event bodies and the original held S2-B direct I02 roots. The original native I03 returned one positive count rather than two, a changed false `EmpiricalFact` ref and `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET` for an actually positive cell. This is G3 hidden-occurrence / actual G2 first-consumer proof failure.

Reviewer evidence was supplied as local paths, **not accessed by this GitHub author environment**:
- `/Users/matthewsmith/s2b-work/pyat-s2c-g5-evidence/LOCAL_S2C_G5_RESULTS.json`, SHA-256 `8c3dcc60119b3635ba0605ead48164fccd58eccccce58e8e70a4aba120bec914`
- `/Users/matthewsmith/s2b-work/pyat-s2c-g5-evidence/LOCAL_S2C_G5_EXECUTION_RETURN.md`, SHA-256 `90faa6f63098692a54829059b36284ef1ba918fbe8b76a611b06f36daec10c05`

## Exact repair at frozen code and test SHA

**A2 R2 executable code/test SHA:** `b7b697b69f0acea12174937ee824c19ac34ac284`.

Only these files changed from the received R1 cut:
- `rawlsing_next/pre553_source_direct_parquet_estate.py`: after authenticating the manifest and all member hashes, cold opening verifies the actual `RespondentEvent.parquet` and `event_locator.parquet` footer event census against each other and against declared counts; verifies row-group topology and per-group counts. This catches the exact coherent re-pin + retained event bodies *before* the native fact can be issued. The physical contents are only opened after the independent CURRENT check.
- `rawlsing_next/pre553_direct_estate_i03.py`: the already-required temporary native SQLite index build now streams matching bounded **event projection rows and posting rows** per row group. Every posting must match its physical body's ref, respondent, native/canonical/component selector, state, group and offset. Duplicate/omitted/mispositioned postings cannot masquerade as complete merely because counts match. The original full object-shaped evaluator remains untouched. No complete event-body C11 graph or whole-file `pq.read_table` is materialized.
- `rawlsing_next/tests/test_pre553_direct_estate_i03.py`: two adversarial first-consumer tests. (1) exact G5 two-event/one-locator attack repins locator hash, counts and external manifest digest; actual native I03 must refuse instead of returning a false fact. (2) equal-count duplicate posting re-pin must refuse positional/selector mismatch. Test (1) first checks the genuine unmodified oracle fact.

This is one causal G3 repair, not a new architectural gate. Direct I02 `C11_DIRECT_SOURCEFREE_RELEASE` and reconstructed historical `C11LogicalRelease` remain distinct and unchanged. All prior native G2 positive tests, B-F01–F04, typed-lane negatives and original35/issuer scope still apply.

## New executable verification is mandatory

**NEW R2 tests NOT_RUN.** Do not cite R1's 29/29 / 91/91 as R2 results. The author only verified text commits and GitHub blob identities. The local qualified Linux runner must execute an isolated clean worktree pinned to `b7b697b69f0acea12174937ee824c19ac34ac284` (not `8375e260...`, not the moving branch HEAD, not this documentation commit):

```bash
git fetch origin agent/pyat960-s2c-agent-a-counter-20261113-r1
git worktree add --detach ../pyat-s2c-a2-r2-test b7b697b69f0acea12174937ee824c19ac34ac284
cd ../pyat-s2c-a2-r2-test
test "$(git rev-parse HEAD)" = "b7b697b69f0acea12174937ee824c19ac34ac284" || exit 1

PYTHONPATH=. python3 -m pytest -vv -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_source_direct_parquet_estate.py \
  rawlsing_next/tests/test_pre553_direct_estate_i03.py

PYTHONPATH=. python3 -m pytest -vv -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py
```

**Expected (not observed):** 31 focused tests (29 prior + 2 negatives) and 91 inherited. Independently rerun the exact nonauthor G5 attack against the repaired code (not only the authored test). Record original fact refs, false-fact refusal, changed/restore, fresh-process native first reader, CURRENT-before-bytes, B-F01–F04, retained bytes, temp peak disk, memory, cold/query latency and source-open count. Do not claim 100k/6GiB from 2 respondents.

A passing local runner is **not** the independent G5 ruling. Have one genuinely nonauthor receiver adjudicate the original S2-C G1–G5 against the exact new SHA. Only a reproduced in-scope frozen G1–G4 breach justifies another specific repair. No open-ended hardening, self-issued authority, S2-D, source-native use, or protected merge.

**Disposition:** `A2_R2_G5_HIDDEN_EVENT_CAUSAL_REPAIR_COMMITTED__NEW_TESTS_NOT_RUN__INDEPENDENT_G5_PENDING__NO_MERGE`.
