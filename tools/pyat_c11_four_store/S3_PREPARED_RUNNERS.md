# PYAT S3 prepared economics — opt-in research runner pack

**Grade: isolated experimental source code, not executed against original source, not independent G5, not production/PROGRAMMA receiving.** These runners only extend the existing four-store benchmark and original I03 kernel. No new issuer, C11 evaluator, saved estate, source-rights rule, or storage backend.

Use the **exact repaired benchmark ancestor** `1a9b5c39adc3c51c2473caef23c0ae01ab9764ba` (PR #1271), with the small opt-in `execute_issued(...,prepared_session=...)` hook from this candidate. The hooks do **not** modify the normal `execute_issued(store,verified,operation)` caller. Do not run original-source tests on a different host or under a broader purpose than the original R2 decision permits.

## A — same original Q103, genuinely reused native session

This is the **important** runner. It reuses the original S3 `permanent.sqlite`, original thirteen-family audit, original Q103 source/predicate/authority and existing I03/S04. It performs one source admission, one full audit, one original Q103 construction, and independently compares a few *fresh native sessions* with **1/10/100 executions on one already-prepared native session**. All output must exactly match original S3 native output. No “100 distinct Q103s” are claimed.

```sh
ROOT="$HOME/Desktop/PYAT_C11_PORTABLE_20261121"
S3_RUN="$ROOT/output/20261122T021200734912-88072"
CONFIG="$ROOT/worktree/tools/pyat_c11_four_store/bundle.json"
PYAT_BENCH_PYTHON="$ROOT/pyat-c11-bench-venv/bin/python" \
  sh tools/pyat_c11_four_store/run_s3_prepared.sh \
  --config "$CONFIG" --existing-run "$S3_RUN" \
  --mode native-repeat --counts 1,10,100 --fresh-samples 3
```

For shorter initial proving, use `--counts 1,10 --fresh-samples 1`. This does *not* rebuild S3, write to SQLite, or repeat 7-minute Q103 reconstruction per execution. It **does** deliberately repeat the entire original 13-family body audit once and original-source issuance once per invocation. Those costs are reported separately. Output: `S3_RUN/native_replays/S3-prepared-.../prepared_report.json`, `progress.jsonl`.

## B — 1/10/100 genuinely distinct **physical-only** questions

```sh
PYAT_BENCH_PYTHON="$ROOT/pyat-c11-bench-venv/bin/python" \
  sh tools/pyat_c11_four_store/run_s3_prepared.sh \
  --config "$CONFIG" --existing-run "$S3_RUN" \
  --mode physical-distinct --counts 1,10,100 --physical-repeats 3
```

This uses the original 100 source-native indexed questions, compares their digests/counts with original S3 physical probes, and never calls an original native-scientific issuer. **A 25-ms SQL GROUP BY is NOT a 25-ms I03 operation.**

## C — WVS7 respondent-scale ***sourcefree physical*** envelope

This creates a disposable, *new* S3 physical SQLite under a scratch root, using fake respondent/question/event bodies and the exact existing S3 indexed store and 13-family audit. **Not** authentic WVS7 SAV, not a synthetic *scientific* query, not an empirical C11 release, and not a native I03 measurement. It tests physical row/index scaling only; synthetic body compression and event/semantic topology differ from real surveys.

```sh
mkdir -p "$HOME/Desktop/PYAT_S3_SCRATCH"
PYAT_BENCH_PYTHON="$ROOT/pyat-c11-bench-venv/bin/python" \
  sh tools/pyat_c11_four_store/run_s3_sourcefree_scale.sh \
  --work-root "$HOME/Desktop/PYAT_S3_SCRATCH" \
  --cases 1500:1,7337:1,30000:1,97220:1,97220:10 \
  --max-cells 1500000
```

Small smoke first: `--cases 8:1,8:2 --max-cells 16`. For 97,220×100 event construction (**9.72 million synthetic events**) the default 1.5-million-cell safety cap deliberately refuses; never treat this as a routine run. By default it removes **only** the new synthetic SQLite files *it created*, leaving small `report.json`/`progress.jsonl` and `summary.json` receipts. `--keep-synthetic-db` is opt-in; sourcefree outputs do not belong in Git.

## What will actually decide next engineering work

1. Compare **fresh I03+S04** versus **already prepared I03+S04** within one verified original source and identical query. Require exact source/fact/S04 output each time.
2. Split the one-time costs: source admission, 13-family audit, Q103 issuance/reconstruction, native session construction, native execution. The native 11.97-second original result did **not** include the separate ~7-minute Q103 reconstruction.
3. Once prepared reuse is positive, plug S3 into the *existing* G4 S02/S03/S04 prepared-session/Batch first readers (e.g. #1247), not an invented second service. Use only independently authorized distinct native questions; until then, keep B as physical-only and C sourcefree-only.
4. Evaluate on a single host and freeze exact candidate SHA, Python environment, SQLite, runtime version, positive/adverse outcomes, CPU/RSS, and S3 SQLite stat/hash-neutrality. A failed CURRENT check must fail closed.

**Known boundary:** Q103 is one original recorded-response operation on SRC04. No 100 genuine distinct original I03 operations are authorized by this pack. Results from A are TEST_ONLY adapter, B is physical-only, C is sourcefree synthetic physical. Protected source/rights/semantic G5 and G4+paired CURRENT_PROGRESS receiving are separate. None of these runners changes S3 to the accepted canonical storage architecture.

## Installation (guarded, isolated, no branch update)

1. Unzip this runner pack outside the repository.
2. Create a **new detached worktree** at the exact repaired PR #1271 SHA.
3. Execute `python3 /ABSOLUTE/PATH/pyat_s3_runners/install_s3_runners.py --repo /ABSOLUTE/PATH/NEW_WORKTREE`. The installer demands a completely clean exact-SHA worktree before editing any file. It never commits, merges, pushes, or changes the prior S3 database.
4. In that worktree, run `PYAT_BENCH_PYTHON=/path/to/bench/python sh tools/pyat_c11_four_store/run_all.sh --self-test` and `PYAT_BENCH_PYTHON=/path/to/bench/python /path/to/bench/python -m unittest -v tools.pyat_c11_four_store.test_prepared_s3_runners`. Both must pass before launching source-authorized work.

The installer makes one additive `native.py` change: optional `prepared_session` for `execute_issued`, checked against exact native session type, exact source/store/routing-plan identity, and SQLite read-only state. The default call path remains byte-for-byte equivalent except for the optional branch. User-visible proof must report the **actual detached-worktree code SHA** (or uncommitted diff hash), not ancestor `1a9b5c...` as if it contains these runners.
