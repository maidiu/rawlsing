> **Superseded execution order (2026-08-03):** Do not run the live respondent canaries yet. Section 86 now governs the next step: first implement the V550 shared respondent substrate and V550J no-database co-execution contract, then prove the structure with synthetic data. The live-canary instructions below remain the later empirical gate after Section 86 is complete.

# Codex execution instructions — bounded nine-source J-chain

## Current typed-state gate status

Section 85 acceptance now consumes `rawlsing_pipeline_boundary_v1` typed producer
state. It does **not** infer readiness from nonzero row counts, legacy readiness
booleans, or the mere presence of a JSON document.

At Gate G2, V551 v3.0 is frozen and its Section 85 consumer contract is active.
The final V551J and V552J producer-bound acceptance hooks are still gated by G3B
and G4 respectively. Until those producer contracts merge, the bounded runner is
expected to fail closed at the typed acceptance gate rather than reinterpret the
legacy readiness documents. Do not weaken that gate to make the historical
canary pass.

## 1. Preserve the verified parent checkpoint

Keep the R184 checkpoint ZIP and restored database unchanged as rollback authority. Create a new branch from the Section 85 commit and a separate output directory for the canary.

## 2. Unpack the preserved canary archive

From Section 85:

```bash
bash section85/unpack_canary_archive.sh /absolute/path/to/canary_work
```

The extracted canary root is:

```text
/absolute/path/to/canary_work/universality_9family_20var_v550_552_after_bridge_repair_20260729T074523Z
```

## 3. Regenerate and verify bounded authority

```bash
python3 section85/code/build_bounded_v550j_authority.py \
  --repo-root "$PWD" \
  --canary-root /absolute/path/to/canary_work/universality_9family_20var_v550_552_after_bridge_repair_20260729T074523Z \
  --output-dir section85/authority \
  --adjudications-path section85/inputs/BOUNDED_JOINT_CONFIGURATION_ADJUDICATIONS.json

python3 section85/code/audit_canary_archive_truth.py \
  --section section85 \
  --canary-root /absolute/path/to/canary_work/universality_9family_20var_v550_552_after_bridge_repair_20260729T074523Z
```

## 4. Prove the live respondent database contract

Use the live respondent-level pipeline database, not the R184 authority-only database. The checker must find one of the governed long-response views, a respondent identifier, all nine source-wave-country scopes, and every configured item before execution is permitted.

```bash
python3 section85/code/check_live_respondent_database.py \
  --section section85 \
  --db-url "$LIVE_PIPELINE_DATABASE_URL" \
  --output /absolute/path/to/bounded_nine_j_chain/reports/LIVE_RESPONDENT_DATABASE_CONTRACT_RETURN.json
```

Do not proceed unless the return status is `PASS_LIVE_RESPONDENT_DATABASE_CONTRACT`. A failure means the host lacks the required respondent substrate; it does not authorize reconstructing joint responses from aggregate V550 tables.

## 5. Generate a host-specific plan before execution

```bash
python3 section85/code/run_bounded_nine_v550j_v551j_v552j.py \
  --repo-root "$PWD" \
  --section section85 \
  --canary-root /absolute/path/to/canary_work/universality_9family_20var_v550_552_after_bridge_repair_20260729T074523Z \
  --output-root /absolute/path/to/bounded_nine_j_chain \
  --db-url "$LIVE_PIPELINE_DATABASE_URL" \
  --plan-only
```

Inspect `reports/bounded_nine_canary_execution_plan.json`. It must contain exactly nine scopes and association mode `off`. The preflight also records whether the V551J and V552J typed producer hooks are still awaiting G3B/G4.

## 6. Execute the GSS control first

```bash
python3 section85/code/run_bounded_nine_v550j_v551j_v552j.py \
  --repo-root "$PWD" \
  --section section85 \
  --canary-root /absolute/path/to/canary_work/universality_9family_20var_v550_552_after_bridge_repair_20260729T074523Z \
  --output-root /absolute/path/to/bounded_nine_j_chain \
  --db-url "$LIVE_PIPELINE_DATABASE_URL" \
  --scope GSS
```

Stop and preserve evidence on any failed gate. A typed producer may have
`run_integrity_status=PASS` while an evidence-dependent operation remains
unpermitted; the runner records those as separate states rather than relabeling
the run as corrupt.

## 7. Execute eight non-GSS canaries

After the GSS control passes, run without `--scope`. The runner stops on the first failure by default. Use `--continue-on-failure` only for a deliberate diagnostic sweep after preserving the first failure.

## 8. Acceptance boundary

The tranche passes only when all nine scopes complete:

```text
live respondent rows
→ V550J governed patterns
→ V551J joint-evidence packet/certification contract
→ V552J runtime-safe structural handoff
```

For V551J and V552J, completion means typed producer integrity plus the required
operation-specific downstream permission under the final merged producer
contract. A nonempty report or positive row count is insufficient.

No full 35-wave canonical files may be generated. No production-completeness claim is authorized.
