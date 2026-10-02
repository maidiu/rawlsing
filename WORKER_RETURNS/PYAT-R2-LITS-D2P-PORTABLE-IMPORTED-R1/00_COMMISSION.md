# LAUNCH IN: OpenCode — Space Bunny Free — STARRIYMAC
# ROLE: PYAT D2P — PORTABLE PACKET GIT IMPORT + INDEPENDENT ACCEPTANCE — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq178-d2p-starriymac-import-review-r1`

Exact commission/base tip:
`7e84783b2bb268ecbb3c75263f2922af6fa978b1`

Execution estate:
**StarriyMac**

Source estate:
**NoviyMac**

This is one combined import + independent review job.

The NoviyMac extraction worker is finished and reported:

Terminal:
`D2P_NOVIYMAC_PORTABLE_CHECKPOINT_EXPORT_PASS__B001_B002_B003_CLOSED__READY_FOR_STARRIYMAC_IMPORT`

NoviyMac packet directory:
`/Users/matthewsmith/Desktop/PYAT_D2P_PORTABLE_EXPORT_20261002`

Reported packet size:
approximately 3.7 MB / 10 files.

Reported `08_PACKET_MANIFEST.json` SHA-256:
`46b38c21f2b331575b12f2eadd09348299ab9c6736983f9f281fd48644ff8106`

Reported checkpoint identity gate:
- bytes `3404445161`
- SHA-256 `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`

Reported closure:
- B001: 50/50 candidate→receipt exact bindings
- B002: 24/24 AuthoritySnapshot closure; 208/208 per-object authority bindings:
  - 60 EmpiricalFact
  - 63 EmpiricalQuerySpec
  - 35 EmpiricalPredicate
  - 50 DiscoveryResultReceipt
- B003: 50/50 retained cross-schema logical binding rows reconstructed from explicit retained contract rows; 18/18 P2 memberwise mappings verified

## Before launch

The user must copy the **entire portable packet directory only** from NoviyMac to StarriyMac.

Do NOT copy the 3.4 GB checkpoint.

On StarriyMac place the directory at a clear local path, preferably:

`/Users/matthewsmith/Desktop/PYAT_D2P_PORTABLE_EXPORT_20261002`

If the actual copied path differs, record it and use that path.

## Governing blocker grain

The authoritative FF02-C blocker inventory requires:

### B001
50-row candidate → DiscoveryResultReceipt exact-ref mapping, including the exact receipt authority/dependency/winning-predicate/source-release/replay bindings. No ordering-based pairing.

### B002
- full 24 AuthoritySnapshot exact-ref/preimage enumeration;
- exact per-object `authority_snapshot_refs` for:
  - 60 facts
  - 63 queries
  - 35 predicates
  - 50 receipts.

**HQ adjudication:** B002 does NOT require embedding the full 3.27 GB EmpiricalFact payload in the portable Git packet. The authoritative remediation is exact AuthoritySnapshot refs/triples plus exact per-object authority_snapshot_refs. The NoviyMac extractor's omission of giant Fact preimage bodies is therefore not itself a blocker if:
- each required per-object binding is exact;
- complete-preimage canonical SHA-256 / byte length / item-count markers are present where the body was withheld;
- nothing required for authority binding was inferred or silently dropped.

Do not re-expand the portable packet merely to carry giant fact payloads.

### B003
Exact 18 P2 historical logical members → current PRE553 candidate mapping.

The original preferred artifact was `cross_schema_logical_candidate_bindings`, but exact retained equivalent material is allowed if it proves the same memberwise mapping without inference.

NoviyMac reports the literal key was absent, and instead exported exact retained rows under:
`FIABC_LITS_CROSS_SCHEMA_LOGICAL_CANDIDATE@1.0.0`

with:
- 50 `native_candidate_provenance` rows;
- 50 `logical_candidate_identity` rows;
- explicit 1:1 join on retained `logical_candidate_key`;
- 18 P2 rows independently identified from retained `lane=="P2"` facts on both sides plus membership in the retained 18-key P2 lane block;
- all 18 rule IDs = `D02_P2_HIGHER_ORDER_K3`;
- 18 distinct current candidate hashes.

This is acceptable only if the packet and saved extraction script substantiate those exact statements directly from retained checkpoint fields. Do not accept a worker prose assertion.

## PHASE 0 — provenance and packet ingress

1. Verify StarriyMac Git repo is `maidiu/rawlsing`.
2. Fetch/checkout this exact branch.
3. Verify HEAD/commission lineage.
4. Locate the copied portable packet directory.
5. Copy packet contents into:

`WORKER_RETURNS/PYAT-R2-LITS-D2P-PORTABLE-IMPORTED-R1/NOVIYMAC_PACKET/`

Do not modify any imported packet file during copy.

6. Record:
- source local path;
- destination repo path;
- copy method;
- byte count;
- file count.

No production files may change.

## PHASE 1 — independent packet integrity verification

Independently compute SHA-256 and byte size for all ten imported files.

Verify `SHA256SUMS.txt` against the actual imported bytes.

Verify reported `08_PACKET_MANIFEST.json` SHA-256 equals:

`46b38c21f2b331575b12f2eadd09348299ab9c6736983f9f281fd48644ff8106`

Review the reported manifest/return circularity deviation:

- NoviyMac omitted `00_RETURN.md` from the manifest's own file list because `00_RETURN.md` records the manifest's hash;
- `SHA256SUMS.txt` covers both.

HQ view: this is **not automatically blocking**. Determine whether the combined packet provides a non-circular complete hash binding:
- SHA256SUMS binds all final files;
- return binds manifest hash;
- manifest binds extraction outputs/prohibition counters.

Reject if any hash is stale or inconsistent.

Do not rewrite imported files to “fix” them.

## PHASE 2 — checkpoint identity evidence review

Inspect:

- `01_CHECKPOINT_IDENTITY.json`
- `00_RETURN.md`
- `07_EXTRACTION_SCRIPT.py`

Verify the packet consistently reports:
- estate = NoviyMac;
- observed bytes = `3404445161`;
- observed SHA-256 =
  `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`;
- identity gate PASS;
- no raw LiTS source locator/read is present in the extraction script;
- checkpoint is the only authorized large input.

NoviyMac disclosed that checkpoint_identity and canonical_closure_identity were commissioned but not separately claimed verified because no explicit permitted field carrying them was found.

Do not convert that disclosure into a false PASS.

Determine whether the **document hash + exact retained canonical closure content** is sufficient for this export acceptance grain. The FF02 blockers bind to the exact checkpoint document SHA; they do not require inventing a second field if the checkpoint body does not self-carry it.

## PHASE 3 — independently review extraction script

Read `07_EXTRACTION_SCRIPT.py` line by line.

Verify:

- deterministic checkpoint-only extraction;
- bounded-memory or otherwise justified memory behavior;
- exact hash gate happens before semantic dereference;
- no raw survey locator;
- no decoder invocation;
- no I03/I05;
- no Candidate A/B/C;
- no P2X;
- no semantic inference from values/counts/frequencies;
- exact retained field extraction;
- canonical JSON hashing is implemented as commissioned;
- count/uniqueness checks fail closed;
- B001 pairing is explicit retained association, not ordering;
- B002 authority refs are extracted from each retained object;
- B003 join uses explicit retained logical keys/lane facts, not empirical similarity.

If the script contains an ambiguous reconstruction step, return CHANGES_REQUIRED.

## PHASE 4 — B001 independent review

Inspect all 50 records in:

`02_CANDIDATE_RECEIPT_BINDINGS.jsonl`

Require:

- exactly 50 records;
- 50 distinct candidate hashes;
- 50 distinct receipt refs;
- each candidate→receipt relationship grounded in an explicit retained `candidate_identity.candidate_hash` or equally exact field inside the retained receipt/preimage;
- exact authority_snapshot_refs;
- exact dependency_refs;
- exact winning_predicate_ref or legitimate exact null;
- exact source_release_refs;
- exact replay ref/root;
- receipt preimage hashes syntactically valid and internally consistent with included retained body where body is included.

No ordering-based pairing.

Return B001:
`CLOSED_ACCEPTED` only if all pass.

## PHASE 5 — B002 independent review

Inspect:

`03_AUTHORITY_SNAPSHOT_CLOSURE.jsonl`
`04_PER_OBJECT_AUTHORITY_BINDINGS.jsonl`

Require:

- exactly 24 AuthoritySnapshot records;
- 24 distinct exact snapshot refs;
- exact retained AuthorityRef triple/structure present per snapshot;
- exactly 208 per-object binding rows;
- exact family counts:
  - 60 EmpiricalFact
  - 63 EmpiricalQuerySpec
  - 35 EmpiricalPredicate
  - 50 DiscoveryResultReceipt;
- every per-object row has exact object ref + authority_snapshot_refs;
- every referenced snapshot resolves into the 24-row closure;
- no per-family inferred substitution;
- no fabricated null authority refs.

### Giant EmpiricalFact preimage deviation

For any Fact body withheld due to NoviyMac disk constraint, require explicit marker containing:
- complete retained canonical preimage SHA-256;
- exact byte length;
- exact item count where applicable;
- exact authority_snapshot_refs exported separately.

Do not require embedding the multi-GB body.

This is sufficient at B002 grain because B002's missing evidence was per-object authority binding + full snapshot enumeration, not portable storage of all response provenance.

Return B002:
`CLOSED_ACCEPTED` only if all required authority grain closes.

## PHASE 6 — B003 independent review

Inspect:

`05_P2_LOGICAL_BINDINGS.jsonl`
`07_EXTRACTION_SCRIPT.py`

The literal `cross_schema_logical_candidate_bindings` key was reportedly absent.

Determine whether the exported retained equivalent is exact and memberwise.

Require:

- exactly 50 cross-schema logical candidate output rows/bindings at the exported current logical grain;
- exact 1:1 retained join key;
- no duplicate logical key on either side unless explicitly governed and explained;
- all 18 P2 member mappings identifiable from explicit retained fields;
- P2 identification does not rely on empirical values/counts/frequencies;
- 18/18 P2 keys match retained P2 lane block membership;
- lane P2 agreement on both retained joined row sources where reported;
- rule ID `D02_P2_HIGHER_ORDER_K3` for the 18 mappings if reported;
- 18 distinct current candidate hashes;
- all binding JSON hashes recompute from included exact retained binding body.

If these conditions hold, accept the retained contract-equivalent representation as B003 closure.

Return B003:
`CLOSED_ACCEPTED`.

## PHASE 7 — prohibition audit

Review packet, script and local shell history/receipts available to this worker for contradictions.

Required accepted claims:

- raw LiTS source reads: 0
- raw source hashes/stats: 0
- source decoder calls: 0
- I03: 0
- I05: 0
- Candidate A/B/C: 0
- P2X: 0
- production mutations: 0
- Git operations on NoviyMac: 0

The retained checkpoint read/hash is allowed and is not raw survey access.

Do not claim more than packet evidence supports.

## PHASE 8 — Git import and independent acceptance record

If B001/B002/B003 all independently pass:

1. retain imported NoviyMac packet byte-for-byte under:
   `WORKER_RETURNS/PYAT-R2-LITS-D2P-PORTABLE-IMPORTED-R1/NOVIYMAC_PACKET/`

2. create StarriyMac review files:

- `WORKER_RETURNS/PYAT-R2-LITS-D2P-PORTABLE-IMPORTED-R1/00_IMPORT_AND_REVIEW.md`
- `01_PACKET_INTEGRITY_REVIEW.json`
- `02_B001_B002_B003_INDEPENDENT_REVIEW.json`
- `03_PROHIBITION_AND_PROVENANCE_REVIEW.json`
- `04_FINAL_DISPOSITION.json`

3. commit and push only return/import-review files.

No production code changes.

## Allowed dispositions

- `APPROVE_D2P_PORTABLE_EXPORT_AT_DECLARED_GRAIN__B001_B002_B003_CLOSED`
- `CHANGES_REQUIRED_D2P_PORTABLE_PACKET`
- `D2P_PACKET_INTEGRITY_FAILURE`
- `D2P_B001_B002_B003_REVIEW_BLOCKER`

PASS terminal:

`D2P_STARRIYMAC_IMPORT_AND_INDEPENDENT_REVIEW_RETURNED__HQ_FANIN_READY`

Blocked terminal:

`D2P_STARRIYMAC_IMPORT_AND_INDEPENDENT_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

## Important scope statement

This job is the independent acceptance required by C4B's wake condition.

A PASS closes:
`C4B-LITS-ORACLE-PREIMAGE-CUSTODY-001`

at the retained preimage/custody grain.

It does NOT authorize:
- raw-source C4 execution;
- fresh LiTS decode;
- source warrant;
- C7;
- PRE-V3→V3.

After PASS, HQ will fan in:
- C4A exact combined tree
- C4B freezes
- accepted D2P retained LiTS custody export
- C4C3 Darwin runtime freeze

into one executable C4 freeze candidate for one final independent integration review before any source warrant.
