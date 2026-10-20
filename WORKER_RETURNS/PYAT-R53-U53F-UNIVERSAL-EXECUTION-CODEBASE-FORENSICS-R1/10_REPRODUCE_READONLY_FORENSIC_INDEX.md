# Reproduction — read-only forensic index

All commands are read-only against the shared Git object store; the only writes are under this return directory. No repository test/production code is executed; Python executes only `tools/*.py` (our stdlib/Git indexers).

## Environment

* macOS 13.2.1 x86_64, Python 3.11.3, Git 2.43.0, SQLite stdlib.
* DeepSeek V4.1-Flash (user-routed), OpenCode, single agent, no model/harness switching.
* Sealed startup: `f148f9ba34deb0ae2ad3983fe94bbcef8f004b03`.

## Deterministic run order

```bash
cd <worktree root>
R=WORKER_RETURNS/PYAT-R53-U53F-UNIVERSAL-EXECUTION-CODEBASE-FORENSICS-R1
python3 $R/tools/index_tree.py          # 01, 02, evidence/index_tree_receipt.json
python3 $R/tools/refs_inventory.py      # 03 shards + evidence/ref_inventory.json
python3 $R/tools/leak_scan.py           # 06 + evidence/leak_scan_receipt.json
python3 $R/tools/docs_and_roster.py     # 06B, 08 + evidence/docs_and_roster_receipt.json
python3 $R/tools/graph_build.py         # 04, 05 + evidence/graph_receipt.json
python3 $R/tools/timeline.py            # 07 + evidence/timeline_receipt.json
python3 $R/tools/quality.py             # QUALITY_CHECKS.json (reruns producers and compares hashes)
```

`quality.py` performs checks a–i: census equality, ref ledger, every-edge anchoring, bounded unknowns, scan coverage, exactly-35 roster, canonical negative control + I51 detection, seeded fake fixture leak (temporary copy), and deterministic rerun equality. It writes `QUALITY_CHECKS.json`.

## Scope and limitations

* 7,615 tracked paths at the sealed SHA; 2,615 observed refs; 966 material refs; 79,487 material diff rows; 730 sealed Python paths + 2,587 branch-only Python blobs scanned; 1,398 documents with reference counts.
* Branch-only blobs were materialized read-only from the promisor remote during the run; all required Python blobs are present (0 missing at final check). Remote refs were not re-fetched beyond object availability; ref freshness is frozen at run time.
* Untracked working files outside the sealed tree are UNKNOWN, not assumed absent. No raw SAV/DTA, source secret, credential or respondent record was opened; binaries/archives are classified only.
* Static AST/literal scan only; dynamic reachability, runtime execution and authority issuance are not asserted. Candidate classifications are input to Astra, not findings of final defect.
* Documentation literals are aggregated in `06B_DOCUMENT_REFERENCE_COUNTS.tsv` and timeline anchors; code leakage is in `06_…`.

## Artifacts

| File | Meaning |
|---|---|
| `01_REPOSITORY_SCOPE_AND_COMPLETENESS.json` | sealed SHA, refs, worktrees, env, census counts, manifest hash, limits |
| `02_ALL_PINNED_TREE_FILES.tsv` | every tracked path with mode/blob/size/category |
| `03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.partNN.tsv` | material-ref changed file blobs (index in `03_MATERIAL_BRANCH_DIFF_INDEX.json` when sharded) |
| `04_UNIVERSAL_PRODUCER_CONSUMER_GRAPH.jsonl` | anchored nodes + edges |
| `05_UNRESOLVED_DYNAMIC_AND_MISSING_EDGES.tsv` | unresolved/incompatible stage edges |
| `06_SOURCE_SPECIFICITY_AND_FIXTURE_LEAKAGE.tsv` | all code hits with candidate classification/consumer consequence |
| `06B_DOCUMENT_REFERENCE_COUNTS.tsv` | documentary reference counts (LiTS/q301/universal/canary/1,890) |
| `07_HISTORIC_REQUIREMENT_TO_ACCEPTANCE_PROPAGATION.tsv` | 19-row requirement→acceptance timeline |
| `08_CLOSED35_UNIVERSAL_EXECUTION_COVERAGE.tsv` | exactly 35 source/wave rows, bounded unknowns |
| `QUALITY_CHECKS.json` | mechanical a–i receipts |
| `EVIDENCE_MANIFEST.json` | hashes of this return and pinned external identities |
