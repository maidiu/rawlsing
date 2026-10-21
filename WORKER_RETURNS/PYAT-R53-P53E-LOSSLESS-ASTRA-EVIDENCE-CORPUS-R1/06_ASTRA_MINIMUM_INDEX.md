# PYAT R53 P53E — Astra minimum index (read this first)

**Repository** `maidiu/rawlsing` (private). **Branch** `agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1`.  
**Corpus/readback head** `991625f3efb5f1f3e563c65197c6de10e7d0f880`. **Original U53F evidence** `fdc4d03537e649cd56c19a458ebeb3292298ff3f`.  
**Corpus status** `36/36` U53F manifest files byte-verified; 
331 lossless chunks; 64,562,521 bytes.  
**Browser connector readback** `UNKNOWN_NOT_TESTED_IN_THIS_HARNESS`.  
**GitHub REST/API readback** `PASS`.

> This is a navigation page, not a substitute for the corpus. Every row below is preserved in a lossless shard. 
> U53F classifications are quoted as U53F-authored evidence, not adopted by this return.

## 60-second route

1. Read `02_LOSSLESS_ORDERED_SHARD_MANIFEST.json` for every original → chunk → byte/row/SHA mapping.
2. Use `04_TOPIC_TO_SHARD_LOOKUP.tsv` to jump by topic or source path. `TOPIC_CHUNK` rows are complete at chunk granularity; `TOPIC_SAMPLE`/`TOPIC_FILE_TOP` are explicitly samples.
3. Read `05_UNEXAMINED_REF_AND_SCOPE_DENOMINATOR.tsv` before making any NO-MISSING claim.
4. Read the original small files at the U53F ref; read the eight large originals through the shards.
5. Re-verify with `tools/verify_corpus.py` (see commands below).

## Verified counts

| Item | Value | Source |
|---|---:|---|
| U53F manifest files rechecked | 36/36 | `01_ORIGINAL_MANIFEST_INDEPENDENT_RECHECK.json` |
| Large originals sharded | 8 | `02_…SHARD_MANIFEST.json` |
| Lossless chunks | 331 | `02_…SHARD_MANIFEST.json` |
| Sharded original bytes | 64,373,991 | 331-byte-exact chunks |
| All original bytes | 64,562,521 | 36 manifest files |
| Pinned-tree rows | 7,615 | `git ls-tree -r f148f9ba` equality |
| Material diff rows | 79,487 | `03` parts 50,000 + 29,487 |
| Scan hit rows | 45,431 | `06` physical rows |
| Selected / contributing refs | 966 / 847 | `evidence/ref_inventory.json` recomputation |
| Zero-diff selected refs | 119 | `03` explanation below |
| Closed35 roster rows | 35 | 700-row frozen registry → 35 pairs |
| Unresolved dynamic edges | 9 | `05_UNRESOLVED…tsv` |
| Current remote refs seen | 3,139 | live `git ls-remote`, frozen receipt |
| Unexamined refs denominator | 2,214 | 1,649 U53F-excluded + 565 current-only |

## Shard map — first / middle / last exact links

| Shard (original) | Chunks | Bytes | First | Middle | Last |
|---|---:|---:|---|---|---|
| `S01_01_REPOSITORY_SCOPE`<br>`01_REPOSITORY_SCOPE_AND_COMPLETENESS.json` | 3 | 523,645 | [first](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S01_01_REPOSITORY_SCOPE/part-0000.txt) | [middle](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S01_01_REPOSITORY_SCOPE/part-0001.txt) | [last](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S01_01_REPOSITORY_SCOPE/part-0002.txt) |
| `S02_02_ALL_PINNED_TREE_FILES`<br>`02_ALL_PINNED_TREE_FILES.tsv` | 9 | 1,712,461 | [first](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S02_02_ALL_PINNED_TREE_FILES/part-0000.txt) | [middle](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S02_02_ALL_PINNED_TREE_FILES/part-0004.txt) | [last](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S02_02_ALL_PINNED_TREE_FILES/part-0008.txt) |
| `S03_03_MATERIAL_DIFF_PART00`<br>`03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.part00.tsv` | 119 | 23,268,989 | [first](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S03_03_MATERIAL_DIFF_PART00/part-0000.txt) | [middle](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S03_03_MATERIAL_DIFF_PART00/part-0059.txt) | [last](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S03_03_MATERIAL_DIFF_PART00/part-0118.txt) |
| `S04_03_MATERIAL_DIFF_PART01`<br>`03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.part01.tsv` | 72 | 14,082,081 | [first](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S04_03_MATERIAL_DIFF_PART01/part-0000.txt) | [middle](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S04_03_MATERIAL_DIFF_PART01/part-0036.txt) | [last](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S04_03_MATERIAL_DIFF_PART01/part-0071.txt) |
| `S06_06B_DOCUMENT_REFERENCE_COUNTS`<br>`06B_DOCUMENT_REFERENCE_COUNTS.tsv` | 2 | 340,019 | [first](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S06_06B_DOCUMENT_REFERENCE_COUNTS/part-0000.txt) | [middle](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S06_06B_DOCUMENT_REFERENCE_COUNTS/part-0001.txt) | [last](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S06_06B_DOCUMENT_REFERENCE_COUNTS/part-0001.txt) |
| `S05_06_SOURCE_SPECIFICITY`<br>`06_SOURCE_SPECIFICITY_AND_FIXTURE_LEAKAGE.tsv` | 120 | 23,452,783 | [first](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S05_06_SOURCE_SPECIFICITY/part-0000.txt) | [middle](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S05_06_SOURCE_SPECIFICITY/part-0060.txt) | [last](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S05_06_SOURCE_SPECIFICITY/part-0119.txt) |
| `S08_NESTED_01_REPOSITORY_SCOPE`<br>`WORKER_RETURNS/PYAT-R53-U53F-UNIVERSAL-EXECUTION-CODEBASE-FORENSICS-R1/01_REPOSITORY_SCOPE_AND_COMPLETENESS.json` | 3 | 525,229 | [first](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S08_NESTED_01_REPOSITORY_SCOPE/part-0000.txt) | [middle](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S08_NESTED_01_REPOSITORY_SCOPE/part-0001.txt) | [last](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S08_NESTED_01_REPOSITORY_SCOPE/part-0002.txt) |
| `S07_EVIDENCE_REF_INVENTORY`<br>`evidence/ref_inventory.json` | 3 | 468,784 | [first](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S07_EVIDENCE_REF_INVENTORY/part-0000.txt) | [middle](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S07_EVIDENCE_REF_INVENTORY/part-0001.txt) | [last](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S07_EVIDENCE_REF_INVENTORY/part-0002.txt) |

## Topic → primary shards (ordered lookup)

| Topic | Matching rows (chunk-count sum) | Top shards |
|---|---:|---|
| `T1_SOURCE_NATIVE_AUTHORITY_ROLE_WORKLOAD` | 79,862 | `S03_03_MATERIAL_DIFF_PART00`, `S05_06_SOURCE_SPECIFICITY`, `S04_03_MATERIAL_DIFF_PART01`, `S02_02_ALL_PINNED_TREE_FILES`, `S06_06B_DOCUMENT_REFERENCE_COUNTS` |
| `T2_B49_G50_I51_U43` | 2,009 | `S03_03_MATERIAL_DIFF_PART00`, `S05_06_SOURCE_SPECIFICITY`, `S04_03_MATERIAL_DIFF_PART01`, `S02_02_ALL_PINNED_TREE_FILES`, `S06_06B_DOCUMENT_REFERENCE_COUNTS` |
| `T3_C11_ROUTEB_I03_I05_BATCH` | 8,690 | `S05_06_SOURCE_SPECIFICITY`, `S03_03_MATERIAL_DIFF_PART00`, `S04_03_MATERIAL_DIFF_PART01`, `S02_02_ALL_PINNED_TREE_FILES`, `S06_06B_DOCUMENT_REFERENCE_COUNTS` |
| `T4_E41_J42_P41_LEARNED_M1_M2_B5_FF_F5_F8_N9_N10_E04` | 84,799 | `S05_06_SOURCE_SPECIFICITY`, `S03_03_MATERIAL_DIFF_PART00`, `S04_03_MATERIAL_DIFF_PART01`, `S02_02_ALL_PINNED_TREE_FILES`, `S06_06B_DOCUMENT_REFERENCE_COUNTS` |
| `T5_HQ_COMMISSION_ACCEPTANCE_DRIFT_HISTORY` | 27,586 | `S05_06_SOURCE_SPECIFICITY`, `S03_03_MATERIAL_DIFF_PART00`, `S04_03_MATERIAL_DIFF_PART01`, `S02_02_ALL_PINNED_TREE_FILES`, `S06_06B_DOCUMENT_REFERENCE_COUNTS` |

`04_TOPIC_TO_SHARD_LOOKUP.tsv` has the exact source path, blob, physical row, shard and byte range. 
`TOPIC_CHUNK` coverage is complete at chunk granularity; samples are labeled as samples.

## Named exact pointers (G50/J42 and high-risk files)

| Label | Source path | Shard | Row | Link |
|---|---|---|---:|---|
| `NAMED_B49` | `WORKER_RETURNS/PYAT-R51-I51-B49-G50-JOINED-PRODUCER-R1/candidate/g50/native_i05.py` | `shards/S05_06_SOURCE_SPECIFICITY/part-0063.txt` | 21578 | [open](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S05_06_SOURCE_SPECIFICITY/part-0063.txt) |
| `NAMED_G50` | `WORKER_RETURNS/PYAT-R50-G50-GOVERNED-OPERATION-GRAMMAR-R1/g50/native_i05.py` | `shards/S05_06_SOURCE_SPECIFICITY/part-0063.txt` | 21542 | [open](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S05_06_SOURCE_SPECIFICITY/part-0063.txt) |
| `NAMED_I51` | `WORKER_RETURNS/PYAT-R51-I51-B49-G50-JOINED-PRODUCER-R1/candidate/g50/native_i05.py` | `shards/S05_06_SOURCE_SPECIFICITY/part-0063.txt` | 21578 | [open](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S05_06_SOURCE_SPECIFICITY/part-0063.txt) |
| `NAMED_J42` | `WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-CONSUMER-R1/runtime/e41_driver.py` | `shards/S05_06_SOURCE_SPECIFICITY/part-0062.txt` | 21166 | [open](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S05_06_SOURCE_SPECIFICITY/part-0062.txt) |
| `NAMED_E41` | `WORKER_RETURNS/PYAT-R41-E41-FULL-EMPIRICAL-F1F4-COMPUTED-POSSIBILITY-R1/e41_e04_service.py` | `shards/S05_06_SOURCE_SPECIFICITY/part-0062.txt` | 21027 | [open](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S05_06_SOURCE_SPECIFICITY/part-0062.txt) |
| `NAMED_P41` | `WORKER_RETURNS/PYAT-R41-P41-GENERIC-PROGRESSIVE-N10E-N10W-SERVING-R1/runtime/fixture.py` | `shards/S05_06_SOURCE_SPECIFICITY/part-0062.txt` | 21086 | [open](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S05_06_SOURCE_SPECIFICITY/part-0062.txt) |
| `NAMED_U43` | `WORKER_RETURNS/PYAT-R43-U43-ORIGINAL35-PROSPECTIVE-WORKLOAD-R1/inputs/wg0x/reused_wg0r_fixture.py` | `shards/S05_06_SOURCE_SPECIFICITY/part-0062.txt` | 21305 | [open](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S05_06_SOURCE_SPECIFICITY/part-0062.txt) |
| `HIGH_SIGNAL_ee_p2x_darwin_stage_backend.py` | `rawlsing_next/ee_p2x_darwin_stage_backend.py` | `shards/S05_06_SOURCE_SPECIFICITY/part-0091.txt` | 32724 | [open](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S05_06_SOURCE_SPECIFICITY/part-0091.txt) |
| `HIGH_SIGNAL_native_i05.py` | `WORKER_RETURNS/PYAT-R50-G50-GOVERNED-OPERATION-GRAMMAR-R1/g50/native_i05.py` | `shards/S05_06_SOURCE_SPECIFICITY/part-0063.txt` | 21542 | [open](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S05_06_SOURCE_SPECIFICITY/part-0063.txt) |
| `HIGH_SIGNAL_r51_joined_source_producer.py` | `WORKER_RETURNS/PYAT-R51-I51-B49-G50-JOINED-PRODUCER-R1/candidate/r51_joined_source_producer.py` | `shards/S05_06_SOURCE_SPECIFICITY/part-0063.txt` | 21592 | [open](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/shards/S05_06_SOURCE_SPECIFICITY/part-0063.txt) |

## Null, unknown, inaccessible, dynamically unresolved

- **9** U53F unresolved/incompatible edges are preserved in `05_UNRESOLVED_DYNAMIC_AND_MISSING_EDGES.tsv`; they are not resolved by this return.
- **35/35** roster rows keep `source_permission_runtime=UNKNOWN_NOT_GRANTED_IN_THIS_FORENSIC_RUN` and `known_original_U_E_pre_scope=NOT_ISSUED / NULL`.
- **1,649** U53F-excluded refs (1,648 non-material + 1 same-as-sealed) and **565** current remote-only refs (25 new heads + 539 pull refs + 1 HEAD) are in the denominator. No NO-MISSING claim is made.
- **119** of the 966 U53F-selected refs have `changed_paths=0`; only **847** contribute the 79,487 rows. This is a clarification, not a row loss.
- U53F's 11,305 scanned-Python-blob coverage is author-reported; this return independently counts the 45,431 hit rows and confirms all 1,228 unique hit blobs are locally present.
- The U53F manifest/01/remote receipt name earlier heads (`f148f9ba`/`872aaee`) while the pinned final head is `fdc4d…`. Content hashes pass; the head metadata is an apparent self-reference defect.

## Verify and reassemble

```bash
cd <worktree root>
R=WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1
python3 $R/tools/verify_corpus.py --json-out /tmp/p53e_verify.json
# reassemble one original exactly (raw byte concatenation):
python3 - <<'PY'
import json, pathlib
R=pathlib.Path('WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1')
m=json.loads((R/'02_LOSSLESS_ORDERED_SHARD_MANIFEST.json').read_text())
o=next(x for x in m['originals'] if x['path']=='06_SOURCE_SPECIFICITY_AND_FIXTURE_LEAKAGE.tsv')
b=b''.join((R/c['path']).read_bytes() for c in o['chunks'])
assert b == __import__('subprocess').check_output(['git','show','fdc4d03537e649cd56c19a458ebeb3292298ff3f:'+'WORKER_RETURNS/PYAT-R53-U53F-UNIVERSAL-EXECUTION-CODEBASE-FORENSICS-R1/'+o['path']])
print(len(b), __import__('hashlib').sha256(b).hexdigest())
PY
```

## Limits

- No Browser connector is present in this harness. GitHub API readback is reported separately; actual Browser UI readback remains **UNKNOWN** unless a Browser-side worker tests it.
- No source/respondent data, production code execution, source grant, scientific adoption, architecture verdict, U53A theory, or HQ acceptance is created.
- The U53F material-ref selection is bounded by its name/subject rule; the denominator above is the explicit frontier, not proof of absence.
- Remote-only ref subjects are UNKNOWN where the commit object was not already local; this return did not fetch every branch.

## Exact paths

- [`00_RETURN_AND_ASTRA_READ_FIRST.md`](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/00_RETURN_AND_ASTRA_READ_FIRST.md)
- [`01_ORIGINAL_MANIFEST_INDEPENDENT_RECHECK.json`](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/01_ORIGINAL_MANIFEST_INDEPENDENT_RECHECK.json)
- [`02_LOSSLESS_ORDERED_SHARD_MANIFEST.json`](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/02_LOSSLESS_ORDERED_SHARD_MANIFEST.json)
- [`03_REPRODUCIBLE_SHARD_READBACK_AND_REASSEMBLY.md`](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/03_REPRODUCIBLE_SHARD_READBACK_AND_REASSEMBLY.md)
- [`04_TOPIC_TO_SHARD_LOOKUP.tsv`](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/04_TOPIC_TO_SHARD_LOOKUP.tsv)
- [`05_UNEXAMINED_REF_AND_SCOPE_DENOMINATOR.tsv`](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/05_UNEXAMINED_REF_AND_SCOPE_DENOMINATOR.tsv)
- [`07_NEGATIVE_REASSEMBLY_RESULTS.json`](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/07_NEGATIVE_REASSEMBLY_RESULTS.json)
- [`tools/verify_corpus.py`](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/tools/verify_corpus.py)
- [`tools/reassemble.py`](https://github.com/maidiu/rawlsing/blob/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/tools/reassemble.py)

