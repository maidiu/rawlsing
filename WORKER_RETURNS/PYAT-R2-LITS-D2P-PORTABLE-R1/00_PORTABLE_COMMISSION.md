# PYAT R2 — LiTS D2P PORTABLE RETAINED-CHECKPOINT EXPORT — R1

Execution estate: **NoviyMac**

This message itself is the governing commission for NoviyMac. A local Git repository, branch, object store, or WORKER_RETURNS commission file is **not required** on NoviyMac.

## Purpose

Use the already-retained LiTS I05 checkpoint on NoviyMac to export the exact retained preimage/binding evidence needed to close FF02 blockers B001, B002 and B003.

This is checkpoint-only extraction.

Do not reopen or inspect raw LiTS survey data.
Do not rerun I03/I05.
Do not run Candidate A/B/C.
Do not run measured P2X.
Do not reconstruct missing semantics from counts, labels, frequencies, nearest matches, or Git/oracle summaries.

## Exact checkpoint

Expected relative path under the NoviyMac Rawlsing root:

LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json

Required size:

3404445161 bytes

Required SHA-256:

2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726

Required checkpoint identity:

3fab15f37db629f0ee24189620c65eff944d8a36c4b4509abb6b8bb2ea69c33f

Required canonical closure identity:

f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415

## Known blocker definitions

B001:
- required grain: 50-row candidate -> DiscoveryResultReceipt exact-ref mapping
- must preserve each receipt's exact authority_snapshot_refs, dependency_refs, winning_predicate_ref, source-release refs and replay material
- no pairing from an unordered receipt-ref pool

B002:
- required grain: complete 24 AuthoritySnapshot exact-ref/preimage closure
- plus exact per-object authority_snapshot_refs for:
  - 60 EmpiricalFact
  - 63 EmpiricalQuerySpec
  - 35 EmpiricalPredicate
  - 50 DiscoveryResultReceipt
- no inference by object family or historical authority package

B003:
- required grain: exact 18 P2 historical logical members -> current PRE553 candidate mapping
- preferred source: retained 50 cross_schema_logical_candidate_bindings rows including all 18 P2 mappings
- if those rows are not retained, export the exact retained EmpiricalPredicate preimages necessary to reproduce the already-qualified P2 memberwise mapping source-free
- no reconstruction from counts/frequencies/labels/nearest matching

## PHASE 0 — identity gate

Re-run and record the exact identity gate even if it was already checked interactively.

1. Resolve NoviyMac Rawlsing root.
2. Resolve exact checkpoint path.
3. Record hostname, OS/version, architecture, absolute checkpoint path.
4. Record observed file size; require 3404445161.
5. Stream-compute SHA-256; require exact:
   2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726

If size/hash mismatches, STOP before semantic access.

Do not broad-search the filesystem if the known checkpoint path already exists.

## PHASE 1 — streaming extraction boundary

The checkpoint is ~3.4 GB. Do not load the entire document into memory unless you independently prove it is safe.

Use a streaming JSON parser or other bounded-memory technique.

You may create an isolated temporary Python environment and install a parsing-only dependency such as ijson if needed. This must not modify Rawlsing production code or the retained checkpoint.

Read only the minimum checkpoint subtree needed from:

material.canonical_empirical_object_closure

including, as needed:
- public_object_preimages
- preimage_fragments
- explicitly retained cross-schema binding material

Do not inspect unrelated semantic material.

## Exact-data rule

For every exported row/object:

- preserve the exact retained reference/value from the checkpoint;
- preserve nested structures as canonical JSON rather than guessing a flattened schema;
- canonical JSON for packet records means UTF-8 JSON, sort_keys=true, separators=(",",":"), ensure_ascii=false;
- compute a SHA-256 over each exact retained preimage/binding JSON record where requested;
- never replace an exact retained structure with a prose description.

If a required mapping or preimage is not explicitly retained, return a typed content gap. Do not infer it.

## Portable output directory

Create a new plain directory outside the checkpoint tree, for example:

~/Desktop/PYAT_D2P_PORTABLE_EXPORT_20261002/

Do not require .git.

Write exactly these files:

00_RETURN.md
01_CHECKPOINT_IDENTITY.json
02_CANDIDATE_RECEIPT_BINDINGS.jsonl
03_AUTHORITY_SNAPSHOT_CLOSURE.jsonl
04_PER_OBJECT_AUTHORITY_BINDINGS.jsonl
05_P2_LOGICAL_BINDINGS.jsonl
06_B001_B002_B003_CLOSURE.json
07_EXTRACTION_SCRIPT.py
08_PACKET_MANIFEST.json
SHA256SUMS.txt

Do not copy the 3.4 GB checkpoint into this packet.

## 01_CHECKPOINT_IDENTITY.json

Include at least:

{
  "schema": "PYAT_D2P_CHECKPOINT_IDENTITY@1",
  "estate": "NoviyMac",
  "hostname": "...",
  "os": "...",
  "architecture": "...",
  "rawlsing_root": "...",
  "checkpoint_absolute_path": "...",
  "observed_bytes": 3404445161,
  "observed_sha256": "2704fd3f...",
  "required_sha256": "2704fd3f...",
  "checkpoint_identity": "3fab15f...",
  "canonical_closure_identity": "f264dd8...",
  "identity_gate": "PASS"
}

Do not claim checkpoint_identity or canonical_closure_identity PASS unless those identities are explicitly present/verified in retained checkpoint material. If the file hash passes but either identity is not observable in the permitted retained subtree, record that honestly.

## 02_CANDIDATE_RECEIPT_BINDINGS.jsonl — B001

Exactly 50 records are required for PASS.

Each JSONL record must contain:

{
  "candidate_hash": "<exact retained candidate hash>",
  "discovery_result_receipt_ref": <exact retained ref structure>,
  "authority_snapshot_refs": <exact retained sequence>,
  "dependency_refs": <exact retained sequence>,
  "winning_predicate_ref": <exact retained ref or null if exact retained object is legitimately null>,
  "source_release_refs": <exact retained sequence>,
  "replay_ref": <exact retained replay/root/ref structure>,
  "receipt_preimage_sha256": "<sha256 of canonical retained receipt preimage JSON>",
  "receipt_preimage": <exact retained receipt preimage JSON>
}

The candidate_hash -> receipt mapping must be explicit in retained checkpoint material.

Do not pair candidates to receipts by ordering.

Do not use the Git-standard oracle's unordered 50-ref pool.

If an exact candidate->receipt mapping is absent:
B001 remains OPEN and the overall disposition is a retained-preimage content gap.

## 03_AUTHORITY_SNAPSHOT_CLOSURE.jsonl — B002 part 1

Exactly 24 records are required for PASS.

Each record:

{
  "authority_snapshot_ref": <exact retained snapshot ref>,
  "authority_ref_triples": <exact retained underlying AuthorityRef triple(s)/structure>,
  "preimage_sha256": "<sha256 canonical retained preimage>",
  "preimage": <exact retained AuthoritySnapshot preimage>
}

Do not flatten or rename underlying AuthorityRef members if their retained representation differs from an assumed schema.

## 04_PER_OBJECT_AUTHORITY_BINDINGS.jsonl — B002 part 2

Exactly 208 records are required:

- 60 EmpiricalFact
- 63 EmpiricalQuerySpec
- 35 EmpiricalPredicate
- 50 DiscoveryResultReceipt

Each record:

{
  "object_family": "<exact family/schema identifier>",
  "object_ref": <exact retained ref>,
  "authority_snapshot_refs": <exact retained sequence>,
  "preimage_sha256": "<sha256 canonical retained object preimage>",
  "preimage": <exact retained object preimage>
}

Validate exact family counts.

No family-level authority substitution.

## 05_P2_LOGICAL_BINDINGS.jsonl — B003

Preferred PASS mode:

Export exactly the retained 50 cross_schema_logical_candidate_bindings rows, preserving each exact row in a wrapper:

{
  "export_mode": "RETAINED_CROSS_SCHEMA_LOGICAL_BINDING",
  "row_index": <stable checkpoint-retained index if one exists, otherwise sequential packet index only>,
  "binding_sha256": "<sha256 canonical exact retained binding row>",
  "binding": <exact retained binding row>
}

Then independently count/verify that exactly 18 of the retained rows/members are the already-qualified P2 memberwise mappings.

Do not invent a classifier for P2 if the retained binding rows do not explicitly carry the needed logical-member identity.

Fallback mode only if the 50 rows are not retained:

Export exact retained EmpiricalPredicate preimages sufficient to reproduce the 18 P2 memberwise logical mappings source-free:

{
  "export_mode": "RETAINED_PREDICATE_PREIMAGE",
  "predicate_ref": <exact retained ref>,
  "preimage_sha256": "...",
  "preimage": <exact retained predicate preimage>
}

If neither exact retained binding rows nor sufficient exact predicate preimages exist, B003 remains OPEN.

## 06_B001_B002_B003_CLOSURE.json

Record mechanically:

{
  "schema": "PYAT_D2P_BLOCKER_CLOSURE@1",
  "B001": {
    "status": "CLOSED|OPEN",
    "candidate_receipt_rows": 0,
    "required": 50,
    "reason": "..."
  },
  "B002": {
    "status": "CLOSED|OPEN",
    "authority_snapshots": 0,
    "required_authority_snapshots": 24,
    "per_object_rows": 0,
    "required_per_object_rows": 208,
    "family_counts": {
      "EmpiricalFact": 0,
      "EmpiricalQuerySpec": 0,
      "EmpiricalPredicate": 0,
      "DiscoveryResultReceipt": 0
    },
    "reason": "..."
  },
  "B003": {
    "status": "CLOSED|OPEN",
    "export_mode": "...",
    "cross_schema_rows": 0,
    "p2_memberwise_mappings_verified": 0,
    "required_p2_memberwise_mappings": 18,
    "reason": "..."
  },
  "zero_reconstructed_semantic_rows": true
}

Do not mark a blocker CLOSED merely because the required object family exists. Required exact mapping/preimage grain must be present.

## 07_EXTRACTION_SCRIPT.py

Save the exact script used to perform the extraction and validation.

It must:
- use bounded-memory/streaming access appropriate for the 3.4 GB file;
- contain no raw survey locator;
- not invoke Rawlsing production decoders;
- deterministically generate the packet from the verified checkpoint;
- validate counts before PASS;
- fail closed on ambiguity or missing fields.

Do not include the checkpoint itself.

## 08_PACKET_MANIFEST.json

After every other output is finalized, create:

{
  "schema": "PYAT_D2P_PORTABLE_PACKET_MANIFEST@1",
  "estate": "NoviyMac",
  "checkpoint_sha256": "2704fd3f...",
  "files": [
    {
      "path": "00_RETURN.md",
      "bytes": <integer>,
      "sha256": "<hex>"
    }
  ],
  "pass_state": "...",
  "raw_lits_source_access": 0,
  "source_decoder_calls": 0,
  "i03_runs": 0,
  "i05_runs": 0,
  "candidate_abc_runs": 0,
  "p2x_runs": 0,
  "production_mutations": 0
}

Include every packet file except 08_PACKET_MANIFEST.json itself and SHA256SUMS.txt, then separately record the final manifest's own SHA in 00_RETURN.md.

## SHA256SUMS.txt

Generate ordinary lowercase SHA-256 lines for:

00_RETURN.md
01_CHECKPOINT_IDENTITY.json
02_CANDIDATE_RECEIPT_BINDINGS.jsonl
03_AUTHORITY_SNAPSHOT_CLOSURE.jsonl
04_PER_OBJECT_AUTHORITY_BINDINGS.jsonl
05_P2_LOGICAL_BINDINGS.jsonl
06_B001_B002_B003_CLOSURE.json
07_EXTRACTION_SCRIPT.py
08_PACKET_MANIFEST.json

Sort by filename.

## 00_RETURN.md

State:

- estate = NoviyMac;
- exact checkpoint absolute path;
- observed size/hash;
- identity gate outcome;
- extraction method;
- exact counts for every output;
- B001/B002/B003 disposition;
- any ambiguity/content gap encountered;
- packet directory absolute path;
- SHA-256 of 08_PACKET_MANIFEST.json;
- explicit prohibition audit.

PASS terminal:

D2P_NOVIYMAC_PORTABLE_CHECKPOINT_EXPORT_PASS__B001_B002_B003_CLOSED__READY_FOR_STARriyMAC_IMPORT

Use exact spelling in machine fields:
- source estate: NoviyMac
- Git/HQ import estate: StarriyMac

If any blocker remains:

D2P_NOVIYMAC_PORTABLE_CHECKPOINT_EXPORT_BLOCKED__HQ_ADJUDICATION_REQUIRED

## Hard prohibitions

Do not:
- open/read/hash/stat raw LiTS DTA/source data;
- invoke a source decoder;
- rerun I03 or I05;
- run Candidate A/B/C;
- run P2X;
- infer missing semantics;
- substitute Git/oracle summaries for missing retained preimages;
- modify the retained checkpoint;
- modify Rawlsing production code;
- attempt Git operations merely because the old checkout has no .git.

The only large payload authorized for reading/hashing is the exact verified retained checkpoint.

## Completion behavior

Do not attempt to push or commit anything from NoviyMac.

When complete, report:
1. PASS/BLOCKED terminal;
2. portable packet directory;
3. manifest SHA-256;
4. exact B001/B002/B003 counts/status;
5. any content gap.

The user will transfer only the small portable packet directory to StarriyMac for governed Git import and independent review.
