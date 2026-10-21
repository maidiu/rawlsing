# P53E — reproducible shard readback, verification and reassembly

**Role:** source-free S3 evidence-access worker; not Astra/U53A, not U53F author, not HQ, not a production editor.
**Pinned original:** `agent/rabochii-pyat-r53-u53f-universal-execution-codebase-forensics-r1@fdc4d03537e649cd56c19a458ebeb3292298ff3f`.
**Corpus branch:** `agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1`.
**Chunk bound:** 196,608 bytes (192 KiB), stricter than the commission's <=200 KiB ceiling.
**Chunk policy:** ordered raw-byte ranges; cuts move back to the last LF within the bound. Only a physical row longer than the bound would be split mid-row; no row in this corpus needed that exception (`mid_row_split_count=0`).

## What was read

All 36 files declared by the U53F `EVIDENCE_MANIFEST.json` were read with `git cat-file blob` at `fdc4d…`, never from a mutable worktree. Eight files above the bound were sharded; the other 28 remain directly readable at the same immutable ref. No manifest-declared file was omitted.

| Shard id | Original (relative to U53F return root) | Bytes | Lines | Chunks |
|---|---|---:|---:|---:|
| S01 | `01_REPOSITORY_SCOPE_AND_COMPLETENESS.json` | 523,645 | 13,352 | 3 |
| S02 | `02_ALL_PINNED_TREE_FILES.tsv` | 1,712,461 | 7,616 | 9 |
| S03 | `03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.part00.tsv` | 23,268,989 | 50,001 | 119 |
| S04 | `03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.part01.tsv` | 14,082,081 | 29,488 | 72 |
| S05 | `06_SOURCE_SPECIFICITY_AND_FIXTURE_LEAKAGE.tsv` | 23,452,783 | 45,432 | 120 |
| S06 | `06B_DOCUMENT_REFERENCE_COUNTS.tsv` | 340,019 | 1,399 | 2 |
| S07 | `evidence/ref_inventory.json` | 468,784 | 10,653 | 3 |
| S08 | `WORKER_RETURNS/…/01_REPOSITORY_SCOPE_AND_COMPLETENESS.json` | 525,229 | 13,342 | 3 |

Totals: **36 originals accounted**, **8 sharded**, **28 direct**, **331 chunks**, **64,562,521 original bytes**, **max chunk 196,608 bytes**.

`02_LOSSLESS_ORDERED_SHARD_MANIFEST.json` is authoritative for every chunk's `part`, `path`, `bytes`, `sha256`, `git_blob`, `byte_start`, `byte_end`, physical `row_start`/`row_end`, `starts_mid_row`, `ends_mid_row` and `newline_count`. Rows are 1-based physical lines including the header row; a final non-LF-terminated line counts as one row.

## Verification receipts

`tools/verify_corpus.py` independently re-reads every original from Git and every chunk from disk; it does not trust the corpus summary.

```bash
cd <worktree root>
R=WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1
python3 $R/tools/verify_corpus.py --json-out $R/receipts/verify_corpus.json
```

Actual result on the published corpus:

- **36/36** U53F manifest files matched declared bytes and SHA-256; **0** mismatches.
- **331/331** chunks matched declared size, SHA-256 and Git blob id.
- **8/8** sharded originals reassembled to byte-identical bytes and identical SHA-256.
- **64,562,521/64,562,521** original bytes conserved; **188,530** direct bytes and **64,373,991** sharded bytes.
- **0** mid-row splits; all chunks <= **196,608** bytes.
- Physical line counts and row intervals conserved; no empty or extra chunk files.

Independent scope challenge (`tools/challenge_scope.py`):

- `git ls-tree -r -z f148f9ba…` vs `02_ALL_PINNED_TREE_FILES.tsv`: **7,615** paths, **0** missing, **0** extra, **0** mode/kind/blob/path mismatches; **510,792,397** bytes matched.
- Refs: **2,615** U53F snapshot records (2,613 actual + 2 mandated pseudo-refs); recomputed material selection **966** (exact set equality); **847** contribute `03` rows; **119** selected refs have `changed_paths=0`.
- Material diff rows: **79,487** = 50,000 + 29,487; per-ref row counts equal `changed_paths`.
- Scan table: **45,431** physical hit rows; 1,228 unique blobs, all locally present; the 11,305 scanned-Python-blob figure remains U53F-authored and is **not** re-derived here.
- Graph **22 nodes / 51 edges**; unresolved edges **9**; timeline **19**; roster **35** from a 700-row frozen registry with 20 rows per pair and no Asian Barometer W6.
- Roster NULLs preserved: **35/35** `source_permission_runtime=UNKNOWN_NOT_GRANTED_IN_THIS_FORENSIC_RUN`, **35/35** `known_original_U_E_pre_scope=NOT_ISSUED / NULL`.

Hostile tests (`tools/adversarial_test.py`, all mutations in a temporary out-of-repo copy): **8/8 expected RED**, clean control and final clean control **GREEN**, real committed middle shard hash unchanged. See `07_NEGATIVE_REASSEMBLY_RESULTS.json`.

## Reassemble one original exactly

Because chunks are raw byte ranges in ascending `part` order, simple concatenation is the reconstruction:

```bash
cd <worktree root>
R=WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1
python3 - <<'PY'
import hashlib, json, pathlib, subprocess
R = pathlib.Path("WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1")
m = json.loads((R / "02_LOSSLESS_ORDERED_SHARD_MANIFEST.json").read_text())
o = next(x for x in m["originals"] if x["path"] == "06_SOURCE_SPECIFICITY_AND_FIXTURE_LEAKAGE.tsv")
b = b"".join((R / c["path"]).read_bytes() for c in o["chunks"])
src = subprocess.check_output([
    "git", "show",
    "fdc4d03537e649cd56c19a458ebeb3292298ff3f:"
    "WORKER_RETURNS/PYAT-R53-U53F-UNIVERSAL-EXECUTION-CODEBASE-FORENSICS-R1/06_SOURCE_SPECIFICITY_AND_FIXTURE_LEAKAGE.tsv",
])
assert b == src, "reconstruction differs"
assert hashlib.sha256(b).hexdigest() == o["actual_sha256"]
print(len(b), hashlib.sha256(b).hexdigest())
PY
```

For a byte range: locate the chunk whose `byte_start <= offset < byte_end` in the manifest; for a row: use `row_start`/`row_end` in the manifest or `04_TOPIC_TO_SHARD_LOOKUP.tsv`.

## Reproduce the whole corpus

```bash
cd <worktree root>
WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/tools/run_all.sh \
  2>&1 | tee WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/receipts/run.log
```

Order: environment receipt → shard build → corpus verification → scope challenge → lookup/denominator → adversarial tests → minimum index. The run is read-only against the original Git objects; writes are confined to this return subtree (and temporary out-of-repo adversarial copies, removed after the tests).

## Readback status

- **Local Git object readback:** PASS for all 36 originals and all 331 chunks.
- **GitHub REST/API readback:** **PASS 33/33** targeted chunks at `6818390b…`, including first/middle/last of every shard and named G50/J42/high-risk chunks; returned bytes and SHA-256 matched exactly. Receipt: `receipts/github_api_readback.json`.
- **Actual Browser GitHub connector readback:** **UNKNOWN / NOT TESTED** in this harness. A Browser-side worker must test the exact shard URLs; this return does not claim Browser readability from local Git or API evidence.

## Bounds

- The original U53F selection is bounded by its name/subject rule. `05_UNEXAMINED_REF_AND_SCOPE_DENOMINATOR.tsv` records 1,649 U53F-excluded refs and 565 current remote-only refs at the frozen live snapshot; it is a denominator, not a NO-MISSING proof.
- Remote-only ref subjects are UNKNOWN where the commit object was not already local. No branch blobs were fetched for the challenge.
- No SAV/DTA respondent record, production code execution, source grant, scientific acceptance, architectural verdict, U53A theory, or HQ acceptance is created by this corpus work.
