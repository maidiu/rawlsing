# RFA-06B — local R2-only owner execution

**Do not resume R1.** Do not copy R1 freeze, raw attempts, scoring files or blind exports to R2. R1's three reported primary outputs are exclusively diagnostic.

In a local repository clone on `agent/rabochii-sorok-r15-rfa06b-renderer-court-identity-binding-r2`, enter `SOROK_PRODUCT_CONTROL_ROOM/experiments/RENDERER_FEASIBILITY_R1/anthropic_court_r2/`. Use Python 3.11+ and install the pinned dependencies.

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --requirement requirements.txt
python3 validate_renderer_court_r2.py --expect-empty
```

Set `ANTHROPIC_API_KEY` through your local shell environment; do not embed it in repository files. The preflight checks its presence without displaying it.

The **required sequence** is:

```sh
python3 run_anthropic_renderer_court_r2.py --preflight
python3 run_anthropic_renderer_court_r2.py --freeze
python3 run_anthropic_renderer_court_r2.py --smoke
```

Ordinary preflight is offline: no billable Messages request. It verifies the twenty inherited packets, the exact schema, pair parity, key presence, SDK version, all sixty new assignments, every ID binding and prior-run collisions. The new `EXPERIMENT_FREEZE_R2.json` includes the exact twenty source/payload hashes, request identity compiler, request-specific grammar, original output schema, randomized R2 manifests, model/API/SDK settings and all R2 harness source-file hashes. It is local-only and never overwrites R1.

`--smoke` is an explicitly requested billable **non-primary** `R2SMOKE-0001` call. Before any primary execution, the persisted smoke must be `SCHEMA_VALID` under the full original schema, have an exact returned `fixture_id = RF001`, match the provider schema const and model-visible required ID, and have no local structural errors. A mismatch or schema failure means **R2 COURT = HOLD**. Do not tune the prompt or silently repeat that semantic sample.

**Only when the R2 smoke passes**, intentionally start the clean sixty-run primary court:

```sh
python3 run_anthropic_renderer_court_r2.py
```

This performs ten cases × WP/N × three independent samples in the new frozen run order. Resuming the command skips completed candidate evidence. Only documented no-candidate operational errors qualify for limited retries. `--force-rerun R2RUN-XXXX` never overwrites raw attempts and should be exceptional and explicitly justified.

After primary execution:

```sh
python3 run_anthropic_renderer_court_r2.py --export-blinded
python3 validate_renderer_court_r2.py --require-complete
```

Send scorers only `results/blinded/R2RUN-XXXX.json`, not the private condition mapping, prompt receipts, provider usage or freeze. Preserve local R2 raw evidence separately; do not add it to Git. Independent condition-blinded scoring and later unblinding remain outside this harness.

**The harness itself makes no claim of Nadia-specific realization success.**
