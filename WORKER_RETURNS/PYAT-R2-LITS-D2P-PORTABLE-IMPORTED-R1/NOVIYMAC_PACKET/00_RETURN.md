# PYAT R2 — LiTS D2P PORTABLE RETAINED-CHECKPOINT EXPORT — R1

**Terminal:** `D2P_NOVIYMAC_PORTABLE_CHECKPOINT_EXPORT_PASS__B001_B002_B003_CLOSED__READY_FOR_STARRIYMAC_IMPORT`

---

## 1. Estate

| Field | Value |
|---|---|
| estate | `NoviyMac` |
| hostname | `MacBook-Pro.lan` |
| os | `macOS 13.2.1 (Build 22D68)` |
| architecture | `x86_64` (Intel Core i9-9880H @ 2.30GHz) |
| Rawlsing root | `/Users/matthewsmith/Desktop/Rawlsing` |
| portable packet directory | `/Users/matthewsmith/Desktop/PYAT_D2P_PORTABLE_EXPORT_20261002` |

## 2. Checkpoint

Exact checkpoint (governed relative path under the Rawlsing root above):

```
LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/payload/
PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/court/
oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json
```

Absolute path:

```
/Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json
```

### Identity gate — PASS

| | Required | Observed | Result |
|---|---|---|---|
| byte size | `3404445161` | `3404445161` | PASS |
| SHA-256 | `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726` | `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726` | PASS |

Freshly streamed SHA-256, re-run as part of this execution (18.3 s). No broad filesystem search was performed; the governed relative path resolved directly.

### Identity values recorded but not verified

`checkpoint_identity` = `3fab15f37db629f0ee24189620c65eff944d8a36c4b4509abb6b8bb2ea69c33f`
`canonical_closure_identity` = `f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415`

Both are recorded in `01_CHECKPOINT_IDENTITY.json` **as commissioned**. Neither is claimed as verified: no field carrying either identity was located in the permitted retained material that was read. This is a stated non-verification, not an omission.

## 3. Extraction method

Bounded-memory streaming JSON via `ijson` 3.5.1 in an isolated temporary virtualenv outside the repository. The 3.4 GB checkpoint was **never** loaded into memory. One pass, one retained object preimage resident at a time. The checkpoint was opened read-only and was not modified.

Retained material paths read (nothing else):

- `material.canonical_empirical_object_closure.public_object_preimages.item` (234 preimages)
- `material.astra_shaped_empirical_summary.native_candidate_provenance.rows.item` (50)
- `material.astra_shaped_empirical_summary.logical_candidate_identity.item` (50)
- `material.astra_shaped_empirical_summary.P2.item` (18)

`preimage_fragments` (58 fragments) were inspected during recon and confirmed to be `{fragment_hash, value}` C11Internal reference fragments. They are not binding material for B001/B002/B003 and were therefore not exported.

Canonical JSON law applied throughout: UTF-8, `sort_keys=true`, separators `(",", ":")`, `ensure_ascii=false`. All `preimage_sha256` / `receipt_preimage_sha256` / `binding_sha256` values are SHA-256 over the exact canonical retained preimage.

## 4. Output counts

| File | Rows | Required |
|---|---|---|
| `02_CANDIDATE_RECEIPT_BINDINGS.jsonl` | 50 | 50 |
| `03_AUTHORITY_SNAPSHOT_CLOSURE.jsonl` | 24 | 24 |
| `04_PER_OBJECT_AUTHORITY_BINDINGS.jsonl` | 208 | 208 |
| — EmpiricalFact | 60 | 60 |
| — EmpiricalQuerySpec | 63 | 63 |
| — EmpiricalPredicate | 35 | 35 |
| — DiscoveryResultReceipt | 50 | 50 |
| `05_P2_LOGICAL_BINDINGS.jsonl` | 50 | 50 |

Family counts validated exactly. All 208 rows carry non-empty exact retained `authority_snapshot_refs`. No family-level authority substitution.

## 5. Blocker dispositions

### B001 — CLOSED (50 / 50)

Each of the 50 retained `DiscoveryResultReceipt` preimages carries an explicit retained `semantic_fields.candidate_identity.candidate_hash`. The candidate → receipt association is therefore **explicit in retained material**; no ordering-based pairing was used. 50 distinct candidate hashes and 50 distinct receipt refs. Per-receipt exact `authority_snapshot_refs`, `dependency_refs`, `winning_predicate_ref`, `source_release_refs`, and `replay_ref` exported verbatim alongside the full receipt preimage.

### B002 — CLOSED (24 snapshots, 208 / 208 per-object rows)

24 retained `AuthoritySnapshot` preimages exported with their exact retained `AuthorityRef` triples (each snapshot retains exactly one, at retained field `semantic_fields.replay_protocol_ref`; the retained field name is preserved rather than renamed). 208 per-object rows exported with exact retained per-object `authority_snapshot_refs`.

### B003 — CLOSED (50 cross-schema rows, 18 / 18 P2 verified)

The literal key `cross_schema_logical_candidate_bindings` is **absent** from the checkpoint (0 raw occurrences; `cross_schema`, `logical_member`, `memberwise`, `p2_member`, `logical_binding` all return 0 raw hits).

The same retained material is present under retained contract **`FIABC_LITS_CROSS_SCHEMA_LOGICAL_CANDIDATE@1.0.0`**: 50 `native_candidate_provenance` rows joined 1:1 to 50 `logical_candidate_identity` rows on the explicit retained `logical_candidate_key`. Each row carries the memberwise mapping from the historical logical member (`logical_condition_atom_ids`, `logical_query_template_id`) to the current candidate (`pre553_i05_candidate_hash`) with `current_predicate_ref` and `current_query_ref`.

18 rows verified as the already-qualified P2 memberwise mappings from **explicit retained identity only**, on three independent retained facts:

1. `lane == "P2"` on the retained `native_candidate_provenance` row;
2. `lane == "P2"` on the retained `logical_candidate_identity` row (agrees; the script fails closed on disagreement);
3. `logical_candidate_key` is present in the retained 18-key P2 lane block.

All 18 carry retained `rule_id` `D02_P2_HIGHER_ORDER_K3` and 18 distinct `pre553_i05_candidate_hash` values. **No P2 classifier was invented.**

## 6. Ambiguity and content gap

### 6.1 Deferred EmpiricalFact payload — disclosed deviation

The 60 `EmpiricalFact` retained preimages total **3,276,820,474 canonical bytes** (~69 MB each; largest single preimage 69,629,493 bytes). The bulk is two fully enumerated retained members: `dependency_refs` (up to 53,905 refs) and `semantic_fields.source_empirical_provenance_refs`. NoviyMac had **800 MiB free** at extraction time, so a literal full-preimage `04` was physically impossible to write here and would in any case have produced a 3.3 GB packet, defeating the portable-transfer premise.

Adjudicated by HQ during execution: export exact authority bindings plus deferred-payload digests.

Applied as follows, for all 60 EmpiricalFact rows:

- `authority_snapshot_refs`, `object_ref`, `object_family` — **complete and exact** (this is the B002 closure criterion, and it is intact);
- every non-deferred preimage member — preserved verbatim;
- each deferred member replaced by an explicit `$deferred_retained_member` marker recording its `member_path`, `retained_canonical_bytes`, `retained_canonical_sha256`, `retained_item_count`, and the retained checkpoint SHA-256;
- `preimage_sha256` still covers the **complete unmodified retained preimage**, so every row remains verifiable against the checkpoint.

Nothing was inferred, summarized, silently dropped, or reconstructed. The withheld bytes are recoverable byte-exactly by HQ from the verified retained checkpoint using the recorded digests.

Total withheld across the packet: 3,276,820,474 bytes across 60 objects.

### 6.2 Manifest file-list deviation

`08_PACKET_MANIFEST.json` lists files `01`–`07`. `00_RETURN.md` is intentionally excluded, because this document must record the manifest's own SHA-256 and including it would create a hash circularity with no fixed point. `00_RETURN.md` and `08_PACKET_MANIFEST.json` are both covered by `SHA256SUMS.txt`, which is authoritative and internally consistent. No recorded hash is stale.

### 6.3 Non-verified identities

See §2. Recorded, not claimed verified.

### 6.4 No retained-content gap in the blocker grain

None. Every binding and preimage required by B001, B002, and B003 at the closure grain was present in retained material. The only absent item is the literal `cross_schema_logical_candidate_bindings` key name, whose content is retained under the contract name documented in §5/B003.

## 7. Packet SHA-256

**`08_PACKET_MANIFEST.json` SHA-256:**

```
46b38c21f2b331575b12f2eadd09348299ab9c6736983f9f281fd48644ff8106
```

Per-file digests for the whole packet are in `SHA256SUMS.txt`.

## 8. Prohibition audit

| Prohibition | Count | Evidence |
|---|---|---|
| Raw LiTS DTA/source data opened, read, hashed, or stat'd | 0 | Only the verified checkpoint was read; it was the sole large payload authorized |
| Source decoder invoked | 0 | No Rawlsing module imported; `ijson` streaming parser only |
| I03 rerun | 0 | — |
| I05 rerun | 0 | — |
| Candidate A/B/C run | 0 | — |
| Measured P2X run | 0 | — |
| Semantic mappings inferred | 0 | All rows are retained values; `zero_reconstructed_semantic_rows: true` |
| Git/oracle summaries substituted for retained preimages | 0 | No Git operation attempted; no `.git` present and none required |
| Retained checkpoint modified | 0 | Opened read-only; SHA-256 identical before and after extraction |
| Rawlsing production code modified | 0 | Isolated venv in temp dir; no repo writes |
| Git operations attempted | 0 | Commission explicitly disclaimed the need |
| Commit / push from NoviyMac | 0 | Nothing committed, nothing pushed |

Reproduction: `python3 07_EXTRACTION_SCRIPT.py --outdir <dir>` regenerates the packet deterministically from the verified checkpoint and fails closed on any count drift, missing exact field, or identity mismatch. The script contains no raw survey locator and invokes no Rawlsing source decoder.

---

`D2P_NOVIYMAC_PORTABLE_CHECKPOINT_EXPORT_PASS__B001_B002_B003_CLOSED__READY_FOR_STARRIYMAC_IMPORT`