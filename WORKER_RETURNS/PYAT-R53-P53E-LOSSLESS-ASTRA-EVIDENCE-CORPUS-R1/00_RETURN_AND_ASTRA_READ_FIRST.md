# PYAT R53 P53E — complete return and Astra read-first

**STATUS:** `PUBLISHED_RETURN__LOSSLESS_CORPUS_READY__INDEPENDENT_SCOPE_CHALLENGE_COMPLETE__HOSTILE_TESTS_8_OF_8_RED__BROWSER_READBACK_UNKNOWN_IN_THIS_HARNESS`.
**ROLE:** bounded source-free S3 evidence-access and audit-custody worker. Not Astra U53A, not U53F author, not Pyat HQ, not a scientific/canonical issuer, not a production editor, not J52/W52 successor.
**MODEL / EXECUTION:** DeepSeek V4.1-Flash, reasoning MAX, user-selected OpenCode session on mainMac; native Git and Python 3.11 standard library only. One accountable worker; no model/harness switch; no second agent dispatch.
**SEALED STARTUP:** `f6fd6cdfebe8f0d76a3aa0e2de150065f261709d`.
**BRANCH:** `agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1`.
**CORPUS GENERATION COMMIT:** `6818390b637b87f3f6205ec8eb42fbe07a2c6962` (the later readback/receipt commit is the branch head; the exact final remote SHA is returned in the worker message and is verifiable with `git ls-remote`).
**ORIGINAL U53F EVIDENCE:** `agent/rabochii-pyat-r53-u53f-universal-execution-codebase-forensics-r1@fdc4d03537e649cd56c19a458ebeb3292298ff3f`.
**REPOSITORY URL:** `https://github.com/maidiu/rawlsing/tree/agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1/WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1`.

## Astra read first

1. `06_ASTRA_MINIMUM_INDEX.md` — <20 KiB handoff with exact shard URLs, topic map, named G50/J42 pointers and null/unknown list.
2. `02_LOSSLESS_ORDERED_SHARD_MANIFEST.json` — authoritative file → chunk → byte/row/SHA mapping.
3. `04_TOPIC_TO_SHARD_LOOKUP.tsv` — topic/file navigation; `TOPIC_CHUNK` rows are complete at chunk granularity, samples are labelled as samples.
4. `05_UNEXAMINED_REF_AND_SCOPE_DENOMINATOR.tsv` — explicit ref/scope frontier; do not turn it into a NO-MISSING claim.
5. `01_ORIGINAL_MANIFEST_INDEPENDENT_RECHECK.json` and `07_NEGATIVE_REASSEMBLY_RESULTS.json` — byte and hostile-integrity receipts.
6. `03_REPRODUCIBLE_SHARD_READBACK_AND_REASSEMBLY.md` — exact reassembly/verification commands.

## What the mission changed

The ~1.7 MB tree ledger, ~37 MB diff shards, ~23 MB leakage ledger and the other >192 KiB U53F evidence files are now available as **331 ordered, newline-aligned, raw-byte text chunks**, each <= **196,608 bytes** (192 KiB). Concatenating each chunk set in part order reproduces the original file **byte-for-byte**. No U53F record was dropped, truncated or selectively excluded. The 28 smaller manifest files remain directly readable at the same immutable U53F ref.

## Pass / fail / partial

| Claim | Result | Receipt |
|---|---|---|
| Every U53F manifest-declared file rechecked at `fdc4d…` | **PASS** 36/36; 64,562,521/64,562,521 bytes; 0 SHA/size mismatches | `01_ORIGINAL_MANIFEST_INDEPENDENT_RECHECK.json` |
| Large originals sharded losslessly | **PASS** 8 originals → 331 chunks; 0 mid-row splits; max chunk 196,608 B | `02_LOSSLESS_ORDERED_SHARD_MANIFEST.json` |
| Each sharded original reassembles to original bytes | **PASS** 8/8 byte-identical and SHA-identical | `receipts/verify_corpus.json` |
| Rows and byte ranges conserved | **PASS** all chunk offsets/rows contiguous; no extra/missing chunk | `tools/verify_corpus.py` |
| Tree ledger equality at `f148f9ba…` | **PASS** 7,615 paths; 0 missing/extra/mismatch; 510,792,397 bytes | `receipts/scope_challenge.json` |
| U53F 966-ref selection independently recomputed | **PASS** exact set equality; 847 contribute rows; 119 zero-diff | `receipts/scope_challenge.json` |
| 79,487 material diff rows | **PASS** 50,000 + 29,487; per-ref counts match `changed_paths` | `03_…part00/01.tsv`, `evidence/ref_inventory.json` |
| 45,431 scan hit rows | **PASS** physical rows counted; 1,228 unique blobs all locally present | `06_…tsv`, `receipts/scope_challenge.json` |
| 11,305 scanned-Python-blob coverage | **PARTIAL** U53F-authored; not re-derived by this access mission | `evidence/leak_scan_receipt.json` |
| Graph 22 nodes / 51 edges; 9 unresolved | **PASS** parsed and edge anchors checked | `04_…jsonl`, `05_UNRESOLVED…tsv` |
| Closed35 roster 35 rows from 700-row registry | **PASS** exact pair set; 20 rows/pair; no Asian Barometer W6 | `08_…tsv`, `receipts/scope_challenge.json` |
| Source permission / original U/E_pre NULLs preserved | **PASS** 35/35 UNKNOWN/NOT_GRANTED and 35/35 NOT_ISSUED/NULL | `08_…tsv` |
| Hostile mutation detection | **PASS** 8/8 expected RED; clean controls GREEN; real shard unchanged | `07_NEGATIVE_REASSEMBLY_RESULTS.json` |
| Local Git readback of all chunks | **PASS** all 331 chunk hashes and blob ids | `receipts/verify_corpus.json` |
| GitHub REST/API readback of first/middle/last and named G50/J42 shards | **PASS** 33/33 API targets; 0 failures | `receipts/github_api_readback.json` |
| Actual Browser GitHub connector readback | **UNKNOWN / NOT TESTED** — no Browser connector in this OpenCode host | `receipts/github_api_readback.json` |
| U53F manifest head self-reference | **APPARENT DEFECT** content hashes pass, but `01`/manifest/remote receipt name earlier heads; see below | `receipts/scope_challenge.json` |

## Counts and their sources

- **36** U53F manifest files; **8** sharded, **28** direct; **331** chunks; **64,562,521** original bytes. Source: `02_LOSSLESS…json`; independent verification in `receipts/verify_corpus.json`.
- **7,615** tracked paths and **510,792,397** tracked bytes at `f148f9ba…`. Source: independent `git ls-tree -r -z` equality against `02_ALL_PINNED_TREE_FILES.tsv`.
- **2,615** U53F ref records (2,613 actual + 2 mandated pseudo-refs); **966** selected; **847** contribute rows; **119** selected refs have `changed_paths=0`; **1,649** excluded (1,648 non-material + 1 same-as-sealed). Source: independent re-run of the U53F name/subject rule over the frozen `01` snapshot and `evidence/ref_inventory.json`.
- **79,487** diff rows = 50,000 + 29,487; **45,431** scan hit rows; **22/51** graph nodes/edges; **9** unresolved edges; **19** timeline rows; **35** roster rows from **700** registry rows; **1,398** document-reference rows. Source: `03`, `04`, `05`, `06`, `06B`, `07`, `08` and `receipts/scope_challenge.json`.
- **2,214** unexamined-ref denominator = 1,649 U53F-excluded + 565 current remote-only refs at the frozen live snapshot (25 new heads + 539 pull refs + 1 HEAD). Source: `05_UNEXAMINED…tsv`; live `git ls-remote` receipt `receipts/remote_refs_snapshot.tsv`.

## Independent challenge findings / anomalies

1. **Manifest head self-reference.** All 36 file hashes match, but `01_REPOSITORY_SCOPE…json` names `f148f9ba…`, `EVIDENCE_MANIFEST.json` names `872aaee…`, and `evidence/remote_verification.json` verifies `872aaee…`; the pinned final U53F head is `fdc4d…`. This is an apparent head-metadata defect, not a content-hash failure. U53F's `quality_all_pass=true` does not cover this self-reference.
2. **966 selected refs vs 847 contributing refs.** 119 selected refs have zero changed paths. The 79,487 rows are correct; the 966 figure is a selection count, not a row-contributor count.
3. **Nested return artifacts.** The U53F manifest includes a nested `WORKER_RETURNS/…` copy (`01` 525,229 bytes; `02` 45-byte stub; one nested receipt). All are retained byte-exactly; they are not treated as authoritative where a top-level counterpart exists.
4. **Bounded selection, not completeness.** U53F selected 966 refs by a name/subject rule. This return adds an explicit denominator of 1,649 excluded and 565 current remote-only refs. It does **not** claim no missing evidence.
5. **Scan coverage.** The 45,431 hit rows are independently counted; the 11,305 target count is U53F-authored and not re-derived. All 1,228 unique hit blobs are locally present; no branch blobs were fetched for this challenge.
6. **Roster.** The 35 rows are recomputed from the frozen 700-row registry by `(source_family, canonical_wave)`, not by name search. Source permissions remain UNKNOWN and original U/E_pre remains NULL; no right is inferred.
7. **Remote drift.** The live remote acquired one additional P53T branch between the first and second challenge snapshots and more since the U53F run. The exact frozen enumeration is in `receipts/remote_refs_snapshot.tsv`; remote-only subjects are UNKNOWN where the commit object was not local.

## Hostile integrity results

Mutations were made only in a temporary out-of-repo copy of the corpus:

| Test | Expected | Actual |
|---|---|---|
| Middle shard byte flip | RED | **RED** |
| Missing shard | RED | **RED** |
| Duplicate shard over next part | RED | **RED** |
| Reordered shards | RED | **RED** |
| Candidate with duplicate row | RED | **RED** |
| Altered claimed source blob | RED | **RED** |
| Misleading summary metadata (bytes/chunks) | RED | **RED** |
| Candidate/summary omitting one line | RED | **RED** |
| Clean control / final clean control | GREEN | **GREEN** |

The verifier recomputes bytes, SHA-256, Git blob ids, chunk sequence, row intervals and totals; it does not trust manifest summary metadata. The real committed middle-shard SHA was rechecked unchanged after the tests.

## Readback status

- **Local Git object readback:** PASS. Every chunk was read from disk, hashed, and reconstructed against the pinned original.
- **GitHub REST/API readback:** PASS 33/33 targets at `6818390b…`, including first/middle/last of every shard, the named G50 and J42 chunks, and named high-risk-file chunks. Returned base64 decoded content matched local bytes and SHA-256 exactly.
- **Actual Browser GitHub connector:** **UNKNOWN / NOT TESTED**. This OpenCode host has no Browser connector. API readback proves GitHub can serve the exact bytes; it does **not** prove a Browser UI/connector can render them. Astra/Browser-side readback of the first, middle, last and named shards is still required if Browser evidence is to be claimed.

## Outstanding limitations

- No source/respondent SAV/DTA, secret, protected host, production code execution or local test suite was used.
- The 8 sharded files are the U53F large evidence files; the 28 small files were verified but deliberately not duplicated. They remain at `fdc4d…` and are indexed in `02` and `04`.
- The original U53F selection is bounded; `05` is a denominator, not proof of absence.
- The 11,305 Python-scan coverage and U53F's candidate classifications remain U53F-authored evidence, not adopted findings.
- Remote-only ref subjects are UNKNOWN where commits were not local; no bulk branch fetch was performed.
- The U53F head-metadata anomaly is recorded, not repaired. No original U53F byte was rewritten.
- No architecture adjudication, U53A theory, source grant, N11/N12 wake, scientific acceptance or HQ acceptance is created.

## Authority and custody

This return is an **evidence-access and custody artifact only**. It does not adopt U53F's hypotheses, decide Astra's questions, repair production code, authorize source access, grant scientific meaning, or resume J52/W52. The user STOP and all original permissions remain unchanged. All writes are confined to this return subtree; the only external writes were temporary adversarial copies outside the repository, removed after the tests.

## Deliverables in this subtree

`00_RETURN_AND_ASTRA_READ_FIRST.md`, `01_ORIGINAL_MANIFEST_INDEPENDENT_RECHECK.json`, `02_LOSSLESS_ORDERED_SHARD_MANIFEST.json`, `03_REPRODUCIBLE_SHARD_READBACK_AND_REASSEMBLY.md`, `04_TOPIC_TO_SHARD_LOOKUP.tsv`, `05_UNEXAMINED_REF_AND_SCOPE_DENOMINATOR.tsv`, `06_ASTRA_MINIMUM_INDEX.md`, `07_NEGATIVE_REASSEMBLY_RESULTS.json`, `tools/`, `shards/`, `receipts/`.

**Execution log:** `receipts/run.log` — SHA-256 `63d9f68cc4a6c39dcde8e32ba873f9f8c0d5577bd9c13e0c99edb5552da0947a`.
