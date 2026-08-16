> **Superseded execution order (2026-08-03):** Do not run the live respondent canaries before their required upstream substrate is available. The historical live-canary instructions below remain an empirical gate, not permission to synthesize missing respondent data.

# Codex execution instructions — bounded nine-source J-chain

## Current G4 producer-contract status

Section85 acceptance consumes exact merged producer manifests under
`rawlsing_pipeline_boundary_v1`. It never infers readiness from nonzero row
counts, legacy readiness booleans, free-text status, or the mere presence of a
JSON document.

The exact merged contracts used by Section85 are:

```text
V551J schema v2.2.3 / compiler v551j_joint_evidence_contract_v2_2_3
V552J schema v1.0   / compiler v552j_structural_join_v1
```

V551J and V552J acceptance verifies typed state, exact run/source/wave and
country-or-shard identity, manifest-declared canonical Parquet artifacts, and
producer-declared serialized SHA-256. V552J additionally verifies the exact
V551J and V552 upstream manifest hashes recorded by the producer.

A producer may have `run_integrity_status=PASS` while an evidence-dependent
operation is not permitted. `VALID_EMPTY`, `NOT_APPLICABLE`, review-only
`PRESENT/DENY`, and `APPLICABLE_UNRESOLVED/DENY` are not compiler corruption.

## 1. Preserve the verified parent checkpoint

Keep the R184 checkpoint ZIP and restored database unchanged as rollback
authority. Create a separate output directory for the canary.

## 2. Unpack the preserved canary archive

```bash
bash section85/unpack_canary_archive.sh /absolute/path/to/canary_work
```

The extracted historical canary root is:

```text
/absolute/path/to/canary_work/universality_9family_20var_v550_552_after_bridge_repair_20260729T074523Z
```

Historical V551/V552 producer material that predates the merged contracts must
not be silently adapted. The G4 runner fails closed unless the canary inputs
contain exact current V551 and V552 producer manifests and bytes.

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

Use the governed respondent-level pipeline database, not an authority-only
database. The checker must find a governed long-response relation, respondent
identity, all requested scopes, and configured items.

```bash
python3 section85/code/check_live_respondent_database.py \
  --section section85 \
  --db-url "$LIVE_PIPELINE_DATABASE_URL" \
  --output /absolute/path/to/bounded_nine_j_chain/reports/LIVE_RESPONDENT_DATABASE_CONTRACT_RETURN.json
```

Do not reconstruct joint responses from aggregate V550 tables if the respondent
substrate is unavailable.

## 5. Generate the exact G4 plan

```bash
python3 section85/code/run_bounded_nine_v550j_v551j_v552j.py \
  --repo-root "$PWD" \
  --section section85 \
  --canary-root /absolute/path/to/canary_work/universality_9family_20var_v550_552_after_bridge_repair_20260729T074523Z \
  --output-root /absolute/path/to/bounded_nine_j_chain \
  --db-url "$LIVE_PIPELINE_DATABASE_URL" \
  --plan-only
```

Inspect `reports/bounded_nine_canary_execution_plan.json`. It must show the
active G4 exact-producer hooks and current CLIs:

- V551J receives `--v551-manifest-path` and the exact producer run identity;
- V552J uses `compile_v552j_structural_handoff.py` with
  `--v551j-manifest-path` and `--v552-manifest-path`;
- obsolete V551J V552-context flags and the provisional V552J
  `--v551j-run-root`/`--strict` interface are absent.

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

Stop and preserve evidence on any failed producer-integrity gate. If producer
integrity passes but typed downstream permission is not `ALLOW`, preserve that
as an integrity-pass/evidence-operation-not-permitted result rather than
relabelling it as corruption.

## 7. Execute eight non-GSS canaries

After the GSS control passes, run without `--scope`. The runner stops on the
first failure by default. Use `--continue-on-failure` only for a deliberate
diagnostic sweep after preserving the first failure.

## 8. Acceptance boundary

The tranche passes only when all requested evidence-dependent scopes complete:

```text
live respondent rows
→ V550J governed patterns
→ V551J exact v2.2.3 producer contract
→ V552J exact v1.0 structural join contract
```

A scope does not pass merely because a manifest exists or contains rows. The
relevant producer must have valid exact contract/version/scope/hash binding and
explicit downstream permission for the evidence-dependent operation.

True `OBSERVED_ZERO` remains a measurement. `VALID_EMPTY`, `NOT_APPLICABLE`, and
`APPLICABLE_UNRESOLVED` remain absence/unresolved states and must never be
converted into numeric zero.

No production-completeness claim is authorized by this bounded canary.
