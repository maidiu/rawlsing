# RFA-06C — owner-local execution, scoring seal and explicit unblinding

Run only in a checked-out local clone of `maidiu/rawlsing` on branch `agent/rabochii-sorok-r15-rfa06c-referent-repair-cross-model-screen-r1`. Enter `SOROK_PRODUCT_CONTROL_ROOM/experiments/RENDERER_FEASIBILITY_R1/anthropic_cross_model_screen_r1/`. Use Python 3.11+.

**Prerequisite:** the owner's original RFA-06B R2 folder must still contain all sixty authentic Opus records under `../anthropic_court_r2/results/raw/`. They remain private; the new court never writes into R2. R1 diagnostic outputs are forbidden in this screen.

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --requirement requirements.txt
python3 validate_cross_model_court.py --expect-empty
```

The validator reopens all twenty inherited RFA-05B packets at their original Git blob hashes, checks exact R2 source and execution manifest hashes, all ten cases in both arms, semantic referent classes, physical target negative controls, preselected Opus replicates and the fresh 40/60 manifests. It makes no provider calls.

Set `ANTHROPIC_API_KEY` through your local environment/credential helper without committing it, copying it into a file or sending it through ChatGPT.

```sh
python3 run_cross_model_court.py --preflight
python3 run_cross_model_court.py --freeze
python3 run_cross_model_court.py --smoke-sonnet
python3 run_cross_model_court.py --smoke-haiku
```

- Ordinary `--preflight` checks local credentials present, dependency versions and immutable request parity without a generation.
- `--freeze` writes local-only `EXPERIMENT_FREEZE_R1.json`, including all twenty source packet hashes, exact inherited R2 source/compiler hashes, 42 compiled new-request/schema hashes (40 primary + 2 smoke), both randomization manifests, provider/SDK settings, original output schema/rubric and all authoring source-file hashes.
- Each `--smoke-*` is a **separate intentional billable non-primary** RF001_N message call. Require exact returned model identifier, schema-valid candidate, current fixture ID const, zero corrected structural issues and persistent response receipt. One failed smoke puts that model on HOLD. This runner requires **both** to pass before the primary screening schedule begins. Never silently substitute another model or tune a prompt to force a pass.

**Only after both smoke gates pass**, deliberately issue the 40 new billable generations:

```sh
python3 run_cross_model_court.py
```

The schedule is randomized across model, case and arm. Interrupted execution resumes by preserving terminal candidates. Captured invalid/poor/refused candidates are not semantically retried; recorded transport errors without a candidate have at most two bounded operational retries. Inspect the private raw results locally.

Next, with all sixty original R2 Opus raw records still present, run:

```sh
python3 run_cross_model_court.py --build-blinded-bundle
python3 validate_cross_model_court.py --require-complete
python3 score_and_unblind.py --prepare
```

This builds `results/receipts/OPUS_R2_FULL_RECHECK_R1.json`, preserving original R2 structural statuses and adding corrected referent-review results, then creates **exactly sixty** scorer-safe `results/blinded/BLIND-CM-XXXX.json` items. Scorers are given only these bundles and the blank `results/scoring/BLINDED_SCORES.json`, plus RFA-05 source rubric and case-specific oracle access as independently permitted. **Never give scorers** the private new execution manifest, `BLIND_MAPPING_PRIVATE_R1.json`, R2 source run IDs, model names, WP/N assignments, token/latency receipts, or the operator repository checkout containing those secrets.

Each scorer must enter complete 0/1/2 scores for all fifteen unchanged rubric dimensions, hard-failure codes, `substantive_lawful` boolean and narrative evidence notes for all sixty observations. Do not convert mechanical referent flags automatically into a substantive failure.

Once all sixty scores are final, the owner seals them:

```sh
python3 score_and_unblind.py --seal
python3 score_and_unblind.py --verify-seal
```

**Only after successful complete SHA-256 seal verification** may the owner explicitly invoke:

```sh
python3 score_and_unblind.py --unblind
```

Unblinding writes a private model×arm comparison report with exactly 20 primary observations per model, scores/hard-failure distributions and observed tokens/latency; it separately describes the forty Opus secondary replicates. No intermediate mapping preview or pre-seal model comparison is allowed. Provider pricing is context only; token counts are not invoices.

All `results/`, the freeze, secrets and raw responses are `.gitignore`d. Do not force-add them to Git. This study tests objective actor rendering given hand-authored inputs, not full Rawlsing production or future character longevity.
