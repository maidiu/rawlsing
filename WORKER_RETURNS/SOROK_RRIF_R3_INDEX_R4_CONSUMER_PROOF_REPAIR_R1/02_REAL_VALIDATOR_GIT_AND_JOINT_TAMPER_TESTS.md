# R4 real validator, Git refresh and joint-tamper receipts

## Environment and isolation

- Host: local macOS, S2 full Git + Python + pytest.
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-oindex-r4-consumer-provenance-and-backward-path-fix-20261031`.
- Subject/startup: `e50d32eb6816578145d17dcd637a0b90b3a1ef40`.
- R4 commission head: `4f9214a798b753092d35430f354c2a593658ce8a`.
- Model/editor: user-selected local OpenCode / `opencode-go/deepseek-v4.1-flash`, MAX requested; actual variant/account/quota was not independently instrumented (`UNKNOWN`).
- Test execution is sourcefree: JSON/JSONL, real Git object reads, Python validator, pytest/unittest. No candidate module was imported or executed.

## Exact commands and exits

All commands were run in `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/WORKING_O_INDEX_CANDIDATE_R1` with `PYTHONDONTWRITEBYTECODE=1` and pytest cache disabled.

```sh
python3 validate_index.py --output ../../../WORKER_RETURNS/SOROK_RRIF_R3_INDEX_R4_CONSUMER_PROOF_REPAIR_R1/VALIDATION_INDEX.json
# exit 0; PASS

python3 verify_source_manifest.py > ../../../WORKER_RETURNS/SOROK_RRIF_R3_INDEX_R4_CONSUMER_PROOF_REPAIR_R1/VALIDATION_SOURCE_MANIFEST.json
# exit 0; PASS, rows=167, references=3, errors=[]

python3 -m pytest -o addopts='' -q -p no:cacheprovider test_validate_index.py
# exit 0; 28 passed, 4 subtests passed in 21.38s

python3 -m unittest -v test_validate_index.py
# exit 0; Ran 28 tests in 18.671s — OK
```

Machine receipts: `VALIDATION_INDEX.json`, `VALIDATION_SOURCE_MANIFEST.json`, `PYTEST_RESULTS.txt`, `UNITTEST_RESULTS.txt`.

## Intact positive

```text
validate_index.py PASS
sorok_rows=144
pyat_rows=23
pyat_f_gates=8
four_assets=4
l3_nodes=38
edges=485
traversals=3
owner_slots=46
priority_decisions_made=0
typed_index_cycles=90
source_manifest_sha256=d3f1069784717ef2b4909d3f9d3fac0e55d4df61dd42a6b784629928bc4e83e8
```

```text
verify_source_manifest.py PASS
rows=167, references=3, errors=[]
manifest_digest=f8dc9d608afc78c0a13a5a63f411047a01160114d590bd095350b18ca286e1ea
```

The manifest still resolves **167 source rows + 3 reference sources**: 166 blobs + 1 tree, 21 distinct commits including references. Source `object_id` values are unchanged from the R3 subject (`source_object_ids_unchanged: true`). The changed manifest digest reflects derived `source_kind`, typed source/consumer grades, and the seven `REQUIRED_ONLY:` labels, not different source objects.

## Prior 21-test suite plus R4 negatives

The original 21 tests all still execute in the same file; the total is now 28. The prior four subtests are the four lineage source mutations in `test_damaged_lineage_sources_fail`.

New R4 adversarial tests and exact rejection:

| Test | Mutation | Exact failure |
|---|---|---|
| `test_joint_fake_actual_consumer_fails` | A5 set to ACTUAL in registry + manifest, fake `FORGED/FAKE_CONSUMER.py`, digest recomputed | `ACTUAL consumer forbidden in static index cut`; verifier also reports `actual_consumer`/`forbidden_actual_consumer_evidence` |
| `test_joint_real_unrelated_actual_consumer_fails` | A5 ACTUAL with real B1 object `c0f4588c…:…/bfirst.py` blob `94ffc528…`, digest recomputed | `ACTUAL consumer forbidden in static index cut` |
| `test_joint_source_kind_relabel_fails` | A5 `source_kind` changed to `OWNER_ANCHORED_SOURCE` in registry + manifest | `source_kind is not derived` |
| `test_joint_owner_anchor_promotion_fails` | A5 `source_semantic_grade`/`source_owner_anchor` changed to `OWNER_ANCHORED` in both | `source semantic grade` |
| `test_none_proven_count_drift_fails` | A5 changed from NONE_PROVEN to NOT_A_RUNTIME_MODULE in both, digest recomputed | `expected 112 Sorok NONE_PROVEN` |
| `test_missing_product_reverse_edge_fails` | Removed `L5_S5… -> L4_S5…` reverse edge | `missing reverse edge` |
| `test_missing_product_reverse_path_fails` | Removed `reverse_product_paths["S5"]` | `specific reverse product path` |

The existing ACTUAL-without-evidence test now fails at the stronger hard-reject reason, not merely at a missing field. Existing source-path/blob/timestamp, Pyat, R15 tree, dropped S16, product-forward, orphan and cycle tests remain green/fail-closed.

## ACTUAL consumer policy

The static cut now hard-rejects `ACTUAL` in both validator and Git verifier:

- Sorok `NONE_PROVEN_AT_PREMAIN`: **112**
- Pyat `NONE_PROVEN_AT_PREMAIN`: **23**
- Total: **135**
- `ACTUAL`: **0**

A future ACTUAL row is admissible only with a separate consumer manifest row, Git-resolvable consumer object/edge, named consumer owner or approved authority anchor independent of `source_manifest.json`, positive plus same-consumer fault-negative, and independent reviewer acceptance. No such grant exists here.

## Source semantics

- `source_object_grade = VERIFIED_OBJECT`: the object exists and its type/id/time/tree contents are Git-refreshable.
- `source_semantic_grade = SOURCE_ASSERTED`: source kind and required-consumer prose are authored metadata, not owner-signed semantics.
- `source_owner_anchor = UNVERIFIED_NO_EXTERNAL_OWNER_ANCHOR`: no external original-owner signature is present.
- `consumer_semantic_grade = SOURCE_ASSERTED__NOT_VERIFIED`: a required/named consumer is not a current importer.
- `source_kind` is now derived from object type/path (`source_tree`, `executable_source`, `documentary_definition`, `json_definition_or_evidence`, `opaque_blob`). A joint relabel fails.

Git object existence is therefore **not** science, historical-owner authenticity, current import or adoption.

## Restore

No mutation was applied to the active candidate. Tests mutate temporary copies. After all tests the active candidate was re-executed:

```text
validate_index.py PASS
verify_source_manifest.py PASS, errors=[]
28 tests, 4 subtests OK
```

No historical branch script, native source, survey/respondent data, actor/world code or production consumer was run.
