# 05 — Dynamic I/O and mutation evidence ledger

**S2 / native mutation / severance / restore:** **NOT_RUN**. This chat environment has GitHub source read access but no checked-out private repository, authenticated local respondent DB/Parquet estate, original/manual authority documents or S2 runner with source rights. No speculative native equivalence, synthetic-file substitution, external-source publication or fabricated test receipt.

## Static evidence actually performed

1. Read protected `integration/pre-main-reconciliation-r1@fce43498e16e4709f3c9801e8717f0fdae18126a` tree (9,136 Git blobs, nontruncated), and recursively fetched **73** `data.ddm_build_copy` historical Python modules reachable via named module imports from 36 explicit seed modules. Static recognized import frontier reached zero; dynamic import strings and external libraries remain unproven.
2. Fetched 18 PRE553 candidate modules, 8 legacy downstream-reader/test modules and 3 tracked nonrespondent assets. Code content is indexed by Git blob SHA1 and decoded file-byte SHA256 in `01_SCANNED_FILES.tsv`.
3. Found **501** matched call-expression candidates from named read/load/hash/verify/validate/build/write/merge/groupby operations. Rows in `02_LEGACY_CALLSITES.csv` include exact module/line/expression; it is an overinclusive **regex** register, not a Python AST or executed call graph, and therefore **not a proof that all dynamically bound authority calls were found**.
4. Separately found **16** SQL/execute lines, **14** glob/rglob/iterdir lines, **20** open lines, **2** compound dynamic sites and **142** getattr/importlib/field-reflection matches. The first four classes (52 source occurrences) need review for I/O read-vs-write and concrete path binding; many are transitive V550 acquisition outside this lane's unique issuance. Reflection matches may be ordinary scalar field access, not authority asset acquisition.
5. Validated offline SHA256 implementation against `abc` known digest `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`; the tracked 236-row response-binding CSV hashed to `89d0cb28c20f014278a58fcbb269b8726efe8a9580f2d470caa299ab113f00eb`, equal to its tracked manifest pin. **No current J-family authority release inferred.**

## Dynamic filesystem/SQL locus list (not executed)

| Kind | Exact code locus | Operation / needed runtime witness |
|---|---|---|
| SQL_RUNTIME | `data/ddm_build_copy/build_determinicity_repository_v550.py:340` | `exact = pd.read_sql_query(sql, conn, params={"source": wave_source, "waves": wave_candidates})` |
| SQL_RUNTIME | `data/ddm_build_copy/build_determinicity_repository_v550.py:359` | `candidates = pd.read_sql_query(fallback_sql, conn, params={"waves": wave_candidates})` |
| SQL_RUNTIME | `data/ddm_build_copy/build_determinicity_repository_v550.py:501` | `cols = pd.read_sql_query(sql, conn)["column_name"].tolist()` |
| SQL_RUNTIME | `data/ddm_build_copy/build_determinicity_repository_v550.py:719` | `return pd.read_sql_query(sql, conn)` |
| SQL_RUNTIME | `data/ddm_build_copy/build_determinicity_repository_v550.py:786` | `df = pd.read_sql_query(` |
| SQL_RUNTIME | `data/ddm_build_copy/compile_v550j_joint_response_patterns.py:398` | `exists = pd.read_sql_query(` |
| SQL_RUNTIME | `data/ddm_build_copy/compile_v550j_joint_response_patterns.py:504` | `queried = pd.read_sql_query(sql, db_conn)` |
| SQL_RUNTIME | `data/ddm_build_copy/compile_v550j_joint_response_patterns.py:537` | `iterator = pd.read_sql_query(sql, db_conn, chunksize=chunk_size)` |
| SQL_RUNTIME | `data/ddm_build_copy/compile_v550j_joint_response_patterns.py:539` | `queried = pd.read_sql_query(sql, db_conn)` |
| SQL_RUNTIME | `data/ddm_build_copy/ddm_v550_readiness.py:36` | `return pd.read_sql_query(sql, conn, params=params)` |
| SQL_RUNTIME | `data/ddm_build_copy/ddm_v550_readiness.py:97` | `cur.execute(sql, params)` |
| SQL_RUNTIME | `data/ddm_build_copy/ddm_v550_readiness.py:136` | `cur.execute("SELECT COUNT(*) FROM respondent_position_fact")` |
| SQL_RUNTIME | `data/ddm_build_copy/ddm_v550_response_relation.py:82` | `rows = pd.read_sql_query(` |
| SQL_RUNTIME | `data/ddm_build_copy/ddm_v550_response_relation.py:104` | `rows = pd.read_sql_query(` |
| SQL_RUNTIME | `data/ddm_build_copy/ddm_v550_response_relation.py:195` | `rows = pd.read_sql_query(` |
| SQL_RUNTIME | `data/ddm_build_copy/ddm_v550_shared_cache.py:187` | `available = {str(value) for value in pd.read_sql_query(sql, conn, params={"schema": qsm_schema, "table": qsm_table})["column_name"].tolist()}` |
| FILE_DISCOVERY | `data/ddm_build_copy/build_determinicity_repository_v550.py:1007` | `paths_list = sorted(table_dir.glob("*.parquet"))` |
| FILE_DISCOVERY | `data/ddm_build_copy/compile_v550j_joint_response_patterns.py:519` | `existing_chunks = sorted(chunk_dir.glob("chunk_*.parquet"))` |
| FILE_DISCOVERY | `data/ddm_build_copy/compile_v551j_joint_evidence_packets.py:840` | `for child in directory.iterdir():` |
| FILE_DISCOVERY | `data/ddm_build_copy/ddm_v550_bridge.py:1150` | `authority_paths = sorted(resolved.glob("gss*_directionality_authority.csv"))` |
| FILE_DISCOVERY | `data/ddm_build_copy/ddm_v550_bridge.py:1151` | `overlay_paths = sorted(resolved.glob("gss*_directionality_overlay.csv")) if not authority_paths else []` |
| FILE_DISCOVERY | `data/ddm_build_copy/ddm_v550_io.py:679` | `for path in root.rglob("*.csv"):` |
| FILE_DISCOVERY | `data/ddm_build_copy/ddm_v550_process_guard.py:62` | `for run_dir in readiness_root.iterdir():` |
| FILE_DISCOVERY | `data/ddm_build_copy/ddm_v550_question_use.py:905` | `for path in sorted(resolved.glob("gss*_first_pass_authority_table.csv")):` |
| FILE_DISCOVERY | `data/ddm_build_copy/ddm_v550_question_use.py:994` | `for path in sorted(resolved.glob("gss*_semantic_authority_overlay.csv")):` |
| FILE_DISCOVERY | `data/ddm_build_copy/ddm_v550_question_use.py:1023` | `for path in sorted(resolved.glob("gss*_position_conditioning_overlay.csv")):` |
| FILE_DISCOVERY | `data/ddm_build_copy/ddm_v550_question_use.py:1047` | `for path in sorted(resolved.glob("gss*_*.csv")):` |
| FILE_DISCOVERY | `data/ddm_build_copy/ddm_v558_runtime_graft_readiness.py:122` | `files = sorted(repo_relative_path_text(path) for path in governance_root.rglob("*") if path.is_file())` |
| FILE_DISCOVERY | `data/ddm_build_copy/ddm_v558_runtime_input_gate.py:148` | `files = sorted(repo_relative_path_text(path) for path in governance_root.rglob("*") if path.is_file())` |
| FILE_DISCOVERY | `data/ddm_build_copy/ddm_v5_thin_end_to_end.py:622` | `for path in latest_root.iterdir()` |
| DYNAMIC_OPEN | `data/ddm_build_copy/build_determinicity_wave_shard_v550.py:136` | `with path.open("rb") as handle:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/build_source_structure_validator.py:239` | `with MANIFEST_IN.open(encoding="utf-8", newline="") as f:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/build_source_structure_validator.py:393` | `with out_yaml.open("w", encoding="utf-8") as f:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/build_source_structure_validator.py:417` | `with out_yaml.open("w", encoding="utf-8") as f:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/build_source_structure_validator.py:497` | `with VALIDATION_MANIFEST_OUT.open("w", encoding="utf-8", newline="") as f:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/build_source_structure_validator.py:504` | `with PROBLEM_FILES_OUT.open("w", encoding="utf-8", newline="") as f:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/build_source_structure_validator.py:519` | `with TAXONOMY_OUT.open("w", encoding="utf-8") as f:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/build_source_structure_validator.py:534` | `with VALIDATION_REPORT_OUT.open("w", encoding="utf-8") as f:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/compile_v550j_joint_response_patterns.py:357` | `with Path(path).open("rb") as handle:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/ddm_pipeline_boundary_contract.py:97` | `with p.open("rb") as handle:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/ddm_pipeline_boundary_contract.py:156` | `with p.open("rb") as handle:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/ddm_pipeline_boundary_contract.py:362` | `with path.open(newline="", encoding="utf-8-sig") as handle:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/ddm_v550_family_overlay.py:240` | `with open(manifest_path) as handle:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/ddm_v550_family_overlay.py:247` | `with open(fp) as handle:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/ddm_v550_question_relation_authority.py:312` | `with path.open("rb") as handle:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/ddm_v550_response_semantics_authority.py:79` | `with path.open("rb") as handle:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/ddm_v550_shared_respondent_substrate.py:154` | `with path.open("rb") as handle:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/ddm_v550j_registry_classifier.py:88` | `with open(self._path, "r") as f:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/ddm_v551j_packets.py:1038` | `with open(p, "rb") as f:` |
| DYNAMIC_OPEN | `data/ddm_build_copy/ddm_v5_thin_end_to_end.py:540` | `with tmp.open("w", encoding="utf-8") as f:` |
| COMPOUND_DYNAMIC | `data/ddm_build_copy/ddm_v550_bridge.py:1963` | `for fp in sorted(Path(directory).glob("gss*_directionality*.csv")):` |
| COMPOUND_DYNAMIC | `data/ddm_build_copy/ddm_v552_structural.py:263` | `for n,a in {"v552_pressure_component_index":"V552_PRESSURE_COMPONENT_INDEX_SCHEMA","v552_pressure_observation_index":"V552_PRESSURE_OBSERVATION_INDEX_SCHEMA","v` |

## Executable S2 test plan for qualified next owner — all **NOT_RUN**

| Test | Required initial authority/source | Mutation/severance | Expected observable | Restoration obligation |
|---|---|---|---|---|
| M01 family role | Original accepted, executable family registry and exact producer manifest, same source rows | Change single governed item role or revoke release | Component contract and packet change or typed refusal; no self-recertification | Restore original bytes → identical semantic packet digest |
| M02 directionality | Accepted per-wave directionality and response-option map | Invert one governing response direction without altering respondents | V551/V551J direction hash and certified gate change or DENY | Revert and match original output |
| M03 target/topology | Accepted family relation/target and V552 fact authority | Mutate target ID or topology at same source scope | Exact cross-contract conflict or changed valid target, never silent match | Exact replay equality |
| M04 measurement | Source data and released support/effective-N/weight authority | Change threshold/weight authority with same respondents | Support, effective-N and certification branch change or typed refusal; no zero-for-unknown | Exact support and signature replay |
| M05 stale cache | Valid prepared response Parquet + manifest + all pinned original authority hashes | Mutate registry/authority bytes only, keep cache | Cache invalidation and regenerate/refuse by selected mode, not stale-success | Rebuilt cache digest and governed output equality |
| M06 V550J producer | Real canonical V550J Parquet/manifest/readiness | Remove table, corrupt SHA, change scoped run/country or flip typed state | V551J stops with precise missing/mismatch/status codes | Repair yields identical V551J digest |
| M07 V551 producer | V551 v3 canonical three artifacts and manifest | Truncate coverage, swap atoms path, stale SHA, change source/wave | BoundaryContractError or typed nonpositive, no certified J packet | Restore exact packet/index digest |
| M08 V551J packet | Valid J candidate/components/certified/manifest | Flip component role, atom hash, denominator or packet permission and recompute only outer file hash | V552J refuses or strips permission; falsify packet-contract self-consistency attack with original authority | Exact byte/digest restoration |
| M09 V552 fact | Valid V552 structural fact + temporal key + manifest | Remove exact-scope fact, corrupt score status, make observed zero unresolved | No `ALLOW` joint row, no temporal-field permission | Exact join/audit replay |
| M10 producer chain | Both full current producer manifests | Omit upstream file args at pipeline final verifier; swap nested hash | Consumer cannot claim full chain; require explicit pinned upstream check | Verified complete ancestry when supplied |
| M11 J to PRE553 | Accepted legacy J case + separately issued exact PRE553 authority snapshot | Mutate manual J ruling and independently supplied snapshot, source respondents unchanged | Actual PRE553 first consumer changes or DENYs, proves all negative states and no fixture substitution | Exact source and current result replay |
| M12 incompatibility | Full local code checkout/sourcefree test installation | Import and invoke legacy runtime-safe V552J entrypoint | Confirm static ABI mismatch, label HISTORICAL/HOLD or repair by owner | No silent replacement of canonical v1.0 join |

All S2 scenarios require preflight permissions and an explicit source-owner/runner attestation; originals may remain local and must not be copied into GitHub. For every test, store: tool/model, command/env/CLI precedence, immutable source/authority byte SHA256, version/status, row/wave/shard, before/after/restored digests, exception type, actual downstream reader, and run restrictions. A mock or sourcefree fixture can test contracts, **not** original native semantic provenance.

## No-drop/remaining ownership

- **Unvisited recognized static import dependencies:** 0 within the 73-module closure.
- **Out-of-selection repository blobs:** 9034; do not treat as zero unvisited project files.
- **Dynamic I/O candidate sites not S2-resolved:** 52; separate 142 reflection/field occurrences remain triage-only.
- **Original physical authority paths resolved/byte-read:** 0 from the local estate; one tracked compact binding CSV was byte-hash verified as a Git object.
- **Original-source acceptance/replay and current PRE553 J first-consumer closure:** 0.
- **Future owner:** S2 qualified local code/native provenance investigator + original J-family/response/structural issuer; Pyat HQ to integrate HOLD; independent nonauthor to review exact SHA.
