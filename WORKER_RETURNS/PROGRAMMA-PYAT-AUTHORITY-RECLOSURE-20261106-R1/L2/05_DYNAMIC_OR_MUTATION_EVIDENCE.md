# L2 static and sourcefree mutation/severance/restore evidence

**Execution level:** S1 exact frozen-source inspection + locally authorized **S2 sourcefree diagnostic**. No original respondents, original manual authority source bytes, all35 native runtime, or downstream empirical calibration. Runner: Linux Python/pandas 2.2.3; `pyarrow` absent, so full V551/V552 Parquet CLI roundtrip **NOT_RUN**.

## Immutable source basis

- Frozen reference: `maidiu/rawlsing@9ba4764bef551b1ce498e5772d60b73d69337d4b` (tree `908ff8ee325166d1e36cac14ae4cdd13e78cb228`).
- At launch protected `integration/pre-main-reconciliation-r1` was later observed at `fce43498e16e4709f3c9801e8717f0fdae18126a`; historic L2 module reads deliberately pinned to frozen SHA. Reverify HEAD before any receiving; this is no protected write.
- GitHub blob SHA local `git hash-object` match checked, e.g. `ddm_v551_atoms.py=d07e9a0c8f552b9a53bb1e775281fdf9a68e29e0`, `compile_v552_structural_ddm.py=0f9a28749ed5858a4814ec8e8fa6b53000f343de`, registry CSV `2a45215854d1feb4ba0a779edcb29479143ab613`.
- Content SHA-256 of tracked registry CSV `d270f59da94029780b0e7f26f78cc0f5ede418ed431b5ababeefd2c5e2a00fc8`; manifest `4e70fef731e5e7918c0cebd8aa888b8672fb9e2d6f1f0a35c6c65c060737c50d`. Binding CSV `89d0cb28c20f014278a58fcbb269b8726efe8a9580f2d470caa299ab113f00eb`; manifest `5bcfea51b6a62a20aceb7b16dbf122a5dd60e5b236e64e7edb6948322ba396ec`.

## Reproduce without modifying repo authority

In a checkout of the frozen historical code, from repo root:

```bash
python3 WORKER_RETURNS/PROGRAMMA-PYAT-AUTHORITY-RECLOSURE-20261106-R1/L2/evidence/static_inventory.py
PYTHONPATH=. python3 WORKER_RETURNS/PROGRAMMA-PYAT-AUTHORITY-RECLOSURE-20261106-R1/L2/evidence/sourcefree_probe.py
PYTHONPATH=. python3 -c "import data.ddm_build_copy.ddm_v551_conditional"
```

The inventory script prints deterministic JSON with complete scanned-file TSV, syntactic I/O CSV and counts; the preserved `01_SCANNED_FILES.tsv` and `evidence/STATIC_IO_CALLSITES.csv` are its capture. Static inventory is not a dynamic coverage claim. The sourcefree probe reads the actual tracked CSV+manifest, copies them to a temporary directory, mutates **only temporary copies**, rehashes a temporary manifest where explicitly tested, restores exact original copies, and calculates on **one synthetic bridge row**.

### Observed sourcefree output (2026-11-06)

```text
certified_registry_row_count=145
missing_registry_rejected=BLOCKED_MISSING_V551_SCALE_AUTHORITY
wrong_version_rejected=BLOCKED_SCALE_REGISTRY_MANIFEST_SCHEMA
wrong_hash_rejected=BLOCKED_SCALE_REGISTRY_MANIFEST_HASH_MISMATCH
changed_rule_after_fresh_load=L2_SYNTHETIC_CHANGED_RULE
duplicate_key_rejected=BLOCKED_SCALE_REGISTRY_IDENTITY
review_required_row_accepted_by_v551_loader=True
same_process_cache_stale_after_manifest_matched_mutation=True
restoration_exact_digest=True
synthetic_v551_promotable=True
synthetic_v552_pressure_score=0.5
synthetic_v552_conditional_audit_rows=0
conditional_input_ignored_in_pressure=True
synthetic_scale_mutation_changed_v551_v552_pressure=(np.float64(0.5), np.float64(0.25))
revocation_rejected=BLOCKED_UNCERTIFIED_SCALE_AUTHORITY
unknown_registry_key=NONPROMOTABLE_REPAIRABLE:missing_exact_response_semantics_contract_authority
```

The synthetic active response category was chosen from a real registry key with `DIRECTIONAL_MAGNITUDE`, but the source/wave/country/question/row and measurement were entirely artificial. The pressure is **not a source-qualified empirical estimate**. In the isolated copy, changing scale semantics to `ORDINAL_COORDINATE` and giving synthetic geometry `neutral=0, negative=-1, positive=2` changed signed intensity and V552 weighted result from 0.5 to 0.25. This proves the **mechanical** registry→V551 atom→V552 pressure dependency. It does not prove that either synthetic ruling is admissible.

Negative probes cover missing file, wrong schema version, wrong content SHA, duplicate key, revoked status, unknown contract key; restoration succeeded at exact file digest. The altered review-status row was accepted by V551 despite `REVIEW_REQUIRED`, revealing a concrete local validator gap. A rewritten *matched* temporary manifest plus altered row passed because the loader checks hash agreement, not separate original issuance; the V550 binder has stricter `NO_REVIEW` and cardinality checks (`ddm_v550_response_semantics_authority.py:161-169`). The long-lived in-memory cache read a stale row until reset. Neither test establishes a production attack path or real certified-row defect.

### Additional code-path check

`PYTHONPATH=. python3 -c "import data.ddm_build_copy.ddm_v551_conditional"` at frozen source failed:

```text
ImportError: cannot import name 'MIN_ATOM_SUPPORT' from 'data.ddm_build_copy.ddm_v551_atoms'
```

`ddm_v551_conditional.py:18` also imports `SOURCE_TABLE_PRIORITY`, neither declared in the frozen `ddm_v551_atoms.py`. This is a historical auxiliary module, **not** the current canonical V551 compile import graph. Treat as a blocked optional path, not evidence the canonical V551 compiler failed.

## Untested cells: positive HOLD, not implicit PASS

| Test cell | Result / reason | Competent owner |
|---|---|---|
| Real V550 bridge read and materialized row SHA | `S2_NATIVE_NOT_RUN`: no bridge run file, original survey source or authority ledger mounted | L1/L5 |
| V551 canonical Parquet write+re-read and V552 strict verifier | `S2_PARQUET_NOT_RUN`: `pyarrow` unavailable and no original run; static code inspected | L2/receiver |
| All 35 source/wave actual categories/permissions | `S3_NOT_AUTHORIZED`: scientific issuance and original source rights absent | L1/L5 and original issuer |
| Original 13 manifest-referenced authority bytes | `S2_ASSET_NOT_AVAILABLE`: no files in frozen tracked tree; hashes only declared by manifest | L5 |
| Wrong V551 artifact digest, state, count and scope mutation with a real bundle | `S2_NATIVE_NOT_RUN`: no producer run files; static error paths anchored `compile_v552_structural_ddm.py:165-238` | L2/receiver |
| Cross-session cache expiry/evict, revocation/authority source update | `S2_NATIVE_NOT_RUN`: current neo connector not bound to files | L6 |
| All current neo-pre553 first consumers and actual source mutation | `S2_NATIVE_NOT_RUN`: sampled eight current modules; no real source-to-snapshot factory verified | L6 |
| Independent hostile review/merge | `NOT_RUN` and prohibited for this author | L7 then CAS/HQ |

No source-native all35 acceptance claim, no actor V553 entitlement, no claimed structural semantics beyond the test's synthetic formula.
