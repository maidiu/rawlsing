# Local owner procedure — RFA-06A

Run in a **local clone of maidiu/rawlsing**, on branch `agent/rabochii-sorok-r15-rfa06a-anthropic-renderer-court-harness-r1`, inside `SOROK_PRODUCT_CONTROL_ROOM/experiments/RENDERER_FEASIBILITY_R1/anthropic_court_r1/`. Python 3.11+ is recommended. Do not run through ChatGPT or paste a key into a conversation/source file.

```sh
git checkout agent/rabochii-sorok-r15-rfa06a-anthropic-renderer-court-harness-r1
cd SOROK_PRODUCT_CONTROL_ROOM/experiments/RENDERER_FEASIBILITY_R1/anthropic_court_r1
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --requirement requirements.txt
python3 validate_renderer_court.py --expect-empty
```

Set the key in the **local shell environment**, not a file and not a command checked into Git. The interactive prompt approach avoids entering it in shell history:

```sh
read -r -s -p 'Anthropic API key: ' ANTHROPIC_API_KEY; echo
export ANTHROPIC_API_KEY
python3 run_anthropic_renderer_court.py --preflight
```

On shells without `read -s`, use the shell's secure environment-secret facility. The tool checks only that a key exists and never prints it. **Ordinary preflight makes zero provider requests.** Optional *non-generative* token counting, explicitly requested separately, uses `--preflight --count-tokens`.

Freeze **before any primary billable Messages request**. This produces an ignored local `EXPERIMENT_FREEZE_R1.json` containing exact SHA-256 fingerprints of all twenty semantic payloads, original schema, API projection, runner/core/validator, binding receipt, manifests, config, dependency versions and API contract:

```sh
python3 run_anthropic_renderer_court.py --freeze
```

Optional ONE non-primary billable connectivity probe (not scored; never counted as primary): `python3 run_anthropic_renderer_court.py --smoke`. To deliberately launch the **60 billable primary model samples** in sealed randomized order:

```sh
python3 run_anthropic_renderer_court.py
```

If interrupted, execute the same command again; completed provider responses are not resent. Genuine transport failures with no captured candidate are documented and can be retried. A semantically weak, schema-invalid, truncated, or refused provider response **must be retained as evidence**, not rerendered. A deliberate `--force-rerun RUN-XXXX` creates a new evidence attempt and should only be used with a documented scientific reason; doing so may require issuing a new experiment version before making claims about primary estimates.

After local execution:

```sh
python3 run_anthropic_renderer_court.py --export-blinded
python3 validate_renderer_court.py --require-complete
```

Raw evidence appears under `results/raw/` with append-only `RUN-XXXX-A0001.json` attempt IDs. The scorers receive **only** `results/blinded/RUN-XXXX.json`, not the private mapping manifest, raw attempts, prompts, input-hash metadata, or freeze. If blinded exports have already been issued to scorers, the export command refuses to overwrite changed selections.

To prepare GitHub review, inspect and redact any sensitive content **outside the tracked files**, then provide a separately curated, non-secret receipt with counts/aggregate transport statuses and relevant static validation output. By default `.gitignore` excludes raw provider responses, tokens, freeze, blinded exports, `.env*` files and local virtual environments. Do not use `git add -f` on those paths. The repository-stored private schedule must not be given to scorers until their judgements are sealed.

End of primary sampling does **not** mean Nadia passed. A separately commissioned, condition-blinded evaluation and an explicit later unblinding are required. Full local evidence should be backed up privately before any attempt to re-run.
