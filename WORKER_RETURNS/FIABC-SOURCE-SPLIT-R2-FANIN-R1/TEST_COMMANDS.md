# Qualification commands and results

Run the complete guarded qualification from the fan-in checkout with:

```sh
bash WORKER_RETURNS/FIABC-SOURCE-SPLIT-R2-FANIN-R1/run_guarded_qualification.sh
```

The runner pins `/private/tmp/fiabc-lits-onepass-r1-runtime.kHpXQb/bin/python3.11`, verifies the exact control branch/head and protected branch/head before starting, instruments Python processes with `source_free_guard/sitecustomize.py`, runs without pytest's cache provider, and checks protected-checkout cleanliness at exit. The warm-bytecode hostility test deliberately creates one untracked `.pyc`; the runner removes that exact fixture after the suite.

The captured full output is in `HOSTILE_TEST_OUTPUT.txt`:

- Fan-in, actual-object parity, Worker B/D/E, source-local orchestration, adjacent T3/T4/T5, and process-isolation tests: **102 passed, 65 subtests passed**.
- Protected joined T5 and cache-neutral successor hostile suites: **86 passed**.
- Aggregate: **188 tests passed, 65 subtests passed**.

The ten `SIMPLE_TEST_ONLY` process-envelope probes are synthetic process-isolation fixtures using `fiabc_i06a_process_probe_backend.py`. The guard records these separately. No production Candidate A/B/C process was launched.

The source-free guard blocks survey-format opens, supported survey decoder calls, production candidate-envelope starts, and split/joined `--run` driver starts. The resulting counters and per-process records are in `source_access_telemetry.json`.
