> **Superseded execution order (2026-08-03):** Do not run the live respondent canaries yet. Section 86 now governs the next step: first implement the V550 shared respondent substrate and V550J no-database co-execution contract, then prove the structure with synthetic data. The live-canary instructions below remain the later empirical gate after Section 86 is complete.

# Codex execution instructions — bounded nine-source J-chain

## 1. Preserve the verified parent checkpoint

Keep the R184 checkpoint ZIP and restored database unchanged as rollback authority. Create a new branch from the Section 85 commit and a separate output directory for the canary.

## 2. Unpack the preserved canary archive

From Section 85:

```bash
bash unpack_canary_archive.sh /absolute/path/to/canary_work
```

The extracted canary root is:

```text
/absolute/path/to/canary_work/universality_9family_20var_v550_552_after_bridge_repair_20260729T074523Z
```

## 3. Regenerate and verify bounded authority

```bash
python3 85_V550J_BOUNDED_NINE_FAMILY_AUTHORITY_ADAPTER_AND_CANARY/code/build_bounded_v550j_authority.py \
  --repo-root "$PWD" \
  --canary-root /absolute/path/to/canary_work/universality_9family_20var_v550_552_after_bridge_repair_20260729T074523Z \
  --output-dir 85_V550J_BOUNDED_NINE_FAMILY_AUTHORITY_ADAPTER_AND_CANARY/authority \
  --adjudications-path 85_V550J_BOUNDED_NINE_FAMILY_AUTHORITY_ADAPTER_AND_CANARY/inputs/BOUNDED_JOINT_CONFIGURATION_ADJUDICATIONS.json

python3 85_V550J_BOUNDED_NINE_FAMILY_AUTHORITY_ADAPTER_AND_CANARY/code/audit_canary_archive_truth.py \
  --section 85_V550J_BOUNDED_NINE_FAMILY_AUTHORITY_ADAPTER_AND_CANARY \
  --canary-root /absolute/path/to/canary_work/universality_9family_20var_v550_552_after_bridge_repair_20260729T074523Z
```

## 4. Prove the live respondent database contract

Use the live respondent-level pipeline database, not the R184 authority-only database. The checker must find one of the governed long-response views, a respondent identifier, all nine source-wave-country scopes, and every configured item before execution is permitted.

```bash
python3 85_V550J_BOUNDED_NINE_FAMILY_AUTHORITY_ADAPTER_AND_CANARY/code/check_live_respondent_database.py \
  --section 85_V550J_BOUNDED_NINE_FAMILY_AUTHORITY_ADAPTER_AND_CANARY \
  --db-url "$LIVE_PIPELINE_DATABASE_URL" \
  --output /absolute/path/to/bounded_nine_j_chain/reports/LIVE_RESPONDENT_DATABASE_CONTRACT_RETURN.json
```

Do not proceed unless the return status is `PASS_LIVE_RESPONDENT_DATABASE_CONTRACT`. A failure means the host lacks the required respondent substrate; it does not authorize reconstructing joint responses from aggregate V550 tables.

## 5. Generate a host-specific plan before execution

```bash
python3 85_V550J_BOUNDED_NINE_FAMILY_AUTHORITY_ADAPTER_AND_CANARY/code/run_bounded_nine_v550j_v551j_v552j.py \
  --repo-root "$PWD" \
  --section 85_V550J_BOUNDED_NINE_FAMILY_AUTHORITY_ADAPTER_AND_CANARY \
  --canary-root /absolute/path/to/canary_work/universality_9family_20var_v550_552_after_bridge_repair_20260729T074523Z \
  --output-root /absolute/path/to/bounded_nine_j_chain \
  --db-url "$LIVE_PIPELINE_DATABASE_URL" \
  --plan-only
```

Inspect `reports/bounded_nine_canary_execution_plan.json`. It must contain exactly nine scopes and association mode `off`.

## 6. Execute the GSS control first

```bash
python3 85_V550J_BOUNDED_NINE_FAMILY_AUTHORITY_ADAPTER_AND_CANARY/code/run_bounded_nine_v550j_v551j_v552j.py \
  --repo-root "$PWD" \
  --section 85_V550J_BOUNDED_NINE_FAMILY_AUTHORITY_ADAPTER_AND_CANARY \
  --canary-root /absolute/path/to/canary_work/universality_9family_20var_v550_552_after_bridge_repair_20260729T074523Z \
  --output-root /absolute/path/to/bounded_nine_j_chain \
  --db-url "$LIVE_PIPELINE_DATABASE_URL" \
  --scope GSS
```

Stop and preserve evidence on any failed gate.

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

No full 35-wave canonical files may be generated. No production-completeness claim is authorized.
