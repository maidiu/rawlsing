# Codex installation and execution instruction

Copy this entire directory into the current Rawlsing Git worktree as:

```text
87_PRE_V553_LAYER1_35WAVE_CONTRACT_AUDIT/
```

Do not modify V550J, V551J, V552, or V552J before first running the plan and current implementation.

## 1. Verify the additive harness

```bash
python3 87_PRE_V553_LAYER1_35WAVE_CONTRACT_AUDIT/validation/validate_layer1_program.py \
  --handoff-zip 87_PRE_V553_LAYER1_35WAVE_CONTRACT_AUDIT/inputs/layer1_governed_35wave_catalogs.zip
```

Expected: `PASS`, five unit tests, 35 scopes, and 1,260 deterministic plan rows at the default 36-variable target.

## 2. Generate the plan only

```bash
python3 87_PRE_V553_LAYER1_35WAVE_CONTRACT_AUDIT/code/run_layer1_35wave_contract_audit.py \
  --handoff-zip 87_PRE_V553_LAYER1_35WAVE_CONTRACT_AUDIT/inputs/layer1_governed_35wave_catalogs.zip \
  --repo-root "$PWD" \
  --output-root /absolute/path/to/rawlsing_layer1_plan
```

Review the selected variables and morphology gaps before live execution. A morphology absent from a wave is not automatically a defect; the catalog may contain no qualifying implementation.

## 3. Execute Layer 1

```bash
python3 87_PRE_V553_LAYER1_35WAVE_CONTRACT_AUDIT/code/run_layer1_35wave_contract_audit.py \
  --handoff-zip 87_PRE_V553_LAYER1_35WAVE_CONTRACT_AUDIT/inputs/layer1_governed_35wave_catalogs.zip \
  --repo-root "$PWD" \
  --env-file "$PWD/.env" \
  --output-root /absolute/path/to/rawlsing_layer1_live_audit \
  --execute
```

The harness finds the current Section-35 all-wave runner, derives its runtime root, intersects each planned scope with the live structural/canonical registries, seeds an applicable current J-family, and invokes the current fused pipeline through V552J.

## 4. Execution discipline

- Run GSS 2010 first with `--only-scope 'GSS|2010|US'`.
- Then run the nine-source family band one scope at a time.
- Only after those are understood, run all 35 active waves.
- Keep `--association-mode off` unless the audit explicitly enters the association lane.
- Do not package the shared respondent substrate.
- Do not coerce legitimately blocked scopes into passing.
- Commit the additive harness separately from any repairs discovered by execution.

## 5. Required checkpoint after execution

Package:

- the exact Git commit and self-contained bundle;
- plan and variable-selection outputs;
- all nonrespondent stage outputs;
- `RUN_STATUS.json`;
- privacy scan;
- field inventory;
- basic conservation checks;
- exact commands/stdout/stderr from the current runner;
- no respondent-level data.
