# FIABC-T5 — Test and Qualification Commands

## Execution status

**NOT EXECUTED BY THIS WORKER.**

This commission used GitHub/browser repository tools only.

No repository Python shell was available on this worker surface.

GitHub Actions runs observed on the exact T5 branch: **0**.

No measured P2X was executed.

No PASS result is fabricated.

## 1. Static JSON validation

```bash
python -m json.tool rawlsing_next/fiabc_succession_manifest_schema.json >/dev/null
python -m json.tool rawlsing_next/fiabc_succession_governing_profile.json >/dev/null
python -m json.tool rawlsing_next/tests/fixtures/fiabc_succession_preflight_hostile_cases.json >/dev/null
python -m json.tool WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json >/dev/null
```

## 2. Independent-oracle / freeze hostile court

```bash
python -m pytest -q rawlsing_next/tests/test_pre553_independent_parity_oracle.py
python -m pytest -q rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py
```

Covers:

- post-output/faulty freeze ordering;
- candidate output in expected truth;
- candidate-owned oracle state;
- oracle rewrite/mutation;
- A/B-only agreement;
- C missing;
- candidate identity substitution;
- stale authority closure;
- stale replay root;
- partial frontier;
- collapsed negative-state law;
- same-cardinality WVS frontier substitution.

## 3. I07 mechanized succession preflight

```bash
python -m unittest discover \
  -s rawlsing_next/tests \
  -p 'test_fiabc_succession_preflight.py' \
  -v
```

This includes B05's historical blocker replay and false-PASS fixtures, including repository presence without live consumption, stale/floating evidence, missing source×candidate capability, synthetic production substitution, oracle defects, accounting defects and lifecycle/failure-scope defects.

## 4. I08 final terminal verifier

```bash
python -m pytest -q rawlsing_next/tests/test_fiabc_p2_terminal_verifier.py
```

Covers:

- C11-only false terminal;
- I03-only false terminal;
- partial I05;
- missing cell;
- missing succession PASS;
- invalid oracle independence;
- pairwise agreement without complete oracle match;
- constituent-I03 drift;
- semantic/replay/output drift;
- typed-state collapse;
- lifecycle terminal drift.

## 5. T5 live control hostile court

```bash
python -m pytest -q rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py
```

Covers:

- exact six-cell contract;
- missing current capability;
- old LiTS-C failure reused as current law;
- old WVS-C failure reused as current law;
- frozen candidate owner drift;
- T1 package blob drift;
- T3 isolation blob drift;
- missing T4 accounting surface;
- missing T4 terminal accounting receipt;
- drifted T4 telemetry receipt bytes;
- historical continuation restored as current law;
- R35/105-cell overclaim.

## 6. T1-T4 preservation/regression court

```bash
python -m pytest -q rawlsing_next/tests/test_fiabc_t2_six_cell_execution_binding.py
python -m pytest -q rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py
python -m pytest -q rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py
python -m pytest -q rawlsing_next/tests/test_fiabc_t4_live_accounting.py
python -m pytest -q tests/test_fiabc_telemetry_semantics.py
python -m pytest -q tests/test_fiabc_lifecycle_accounting.py
```

## 7. Real I07 preflight — later controlled local surface only

The real preflight must use a freshly sealed succession manifest whose evidence refs resolve against the exact T5 execution head and a governed P10 lifecycle/failure-scope context.

```bash
python rawlsing_next/ee_p2x_darwin_court_driver.py \
  --preflight \
  --continuation-map WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json \
  --current-court-contract WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json \
  --succession-manifest <REAL_SEALED_SUCCESSION_MANIFEST.json> \
  --succession-lifecycle-context <REAL_GOVERNED_LIFECYCLE_CONTEXT.json> \
  --work-root <FRESH_CONTROLLED_WORK_ROOT> \
  --repo-root <EXACT_T5_CHECKOUT> \
  --lits-path <EXACT_LITS_I_SOURCE> \
  --wvs-path <EXACT_WVS7_SOURCE>
```

The resulting `<FRESH_CONTROLLED_WORK_ROOT>/court/fiabc_t5_succession_preflight.json` must be PASS.

## 8. Real run pattern — recorded only, NOT AUTHORIZED BY THIS WORKER

Only after source-independent qualification, real material oracle freeze, real I07 PASS, R35 convergence and every other Q02 gate is closed:

```bash
python rawlsing_next/ee_p2x_darwin_court_driver.py \
  --run \
  --continuation-map WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json \
  --current-court-contract WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json \
  --succession-preflight-receipt <EXACT_T5_PREFLIGHT_RECEIPT.json> \
  --frozen-upstream-receipt <EXACT_T3_FREEZE_RECEIPT_WITH_MATERIAL_ORACLE_DOCUMENTS.json> \
  --backend-module rawlsing_next.ee_p2x_process_isolated_backend \
  --work-root <FRESH_MEASUREMENT_ROOT> \
  --repo-root <EXACT_QUALIFIED_CHECKOUT> \
  --lits-path <EXACT_LITS_I_SOURCE> \
  --wvs-path <EXACT_WVS7_SOURCE>
```

This command is recorded to make the later mechanical gate deterministic.

It was not executed here.

## Hostile requirement map

| Required hostile case | Mechanized owner |
|---|---|
| oracle frozen after candidate start/output | T3 freeze validator + I05 hostile suite |
| candidate output creates expected truth | accepted I05 hostile suite |
| oracle rewritten after output | `verify_frozen_oracle` mutation test |
| only A/B agree | accepted I05 three-way gate |
| C missing | accepted I05 three-way gate |
| different oracle identities | accepted I05 observation/three-way law |
| stale authority closure | accepted I05 hostile suite |
| stale replay root | accepted I05 hostile suite |
| partial frontier | accepted I05 hostile suite |
| collapsed negatives | accepted I05 hostile suite |
| repository presence without live consumption | accepted I07 hostile suite |
| one current cell missing | I07 + T5 current-contract tests |
| T4 accounting missing | I07 P09 + T5 S16 accounting-receipt validation |
| C11-only | accepted I08 suite |
| I03-only | accepted I08 suite |
| partial I05 | accepted I08 suite |
| lifecycle replay changes terminal | accepted I08 + T5 full replay projection |
| old LiTS-C failure reused | T5 live-control suite |
| old WVS-C failure reused | T5 live-control suite |
