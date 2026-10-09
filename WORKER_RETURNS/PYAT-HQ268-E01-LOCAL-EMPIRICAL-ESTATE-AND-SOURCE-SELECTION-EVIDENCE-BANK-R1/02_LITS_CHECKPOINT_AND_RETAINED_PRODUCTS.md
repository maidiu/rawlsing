# 02 — LiTS RETAINED CHECKPOINT AND RETAINED PRODUCTS

**Mode:** identification and characterization only. The 3.4 GB checkpoint was **not** rebuilt, re-exported, copied, uploaded, decompressed, decoded, or bulk-read/hashed in this pass.

---

## 1. The ~3.4 GB retained LiTS checkpoint — FOUND

**Exact location (single regular file):**

```
/Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY/
  PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/
  payload/
  PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/
  court/oracle_producers/LITS_I/
  current_i05_materialization_checkpoint_v3.json
```

| Property | Value |
|---|---|
| Physical type | **Single regular file** (not multi-part, not a directory, no symlinks) |
| Byte size | **3,404,445,161** bytes (≈3.40 GB / 3.17 GiB) |
| Filesystem mtime | 2026-09-23 20:41 |
| Schema | `FIABC_LITS_CURRENT_NEUTRAL_I05_MATERIALIZATION_CHECKPOINT@3.0.0` |
| Document SHA-256 (recorded) | `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726` |
| Checkpoint identity SHA-256 (recorded) | `3fab15f37db629f0ee24189620c65eff944d8a36c4b4509abb6b8bb2ea69c33f` |
| Producer | `python -m rawlsing_next.fiabc_final_oracle_freeze_producers produce-lits` |
| Execution commit | `045d62709bb65084f3ae7b3dda062dfedfa942b4` |
| Execution branch | `agent/rabochii-premain-fiabc-lits-final-canonical-closure-source-retry-r1` |
| Source argument | `/Users/matthewsmith/Desktop/Rawlsing/data/Data/LiTS_I.dta` — **the same physical path that exists today** |

Head/tail of the document were read (bounded): it opens with an `audit` block containing `canonical_empirical_closure_identity`, `canonical_empirical_object_inventory`, `common_execution_binding`, `runtime_catalog`, and closes with `schema` + `source_identity`.

### Source SHA / release and producer ancestry (as recorded, without bulk reading)

```
source_identity = {
  source:   "LITS_I",
  sha256:   7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09,
  rows:     29002,
  variables:1198
}
```

**This pass physically re-hashed `/Users/matthewsmith/Desktop/Rawlsing/data/Data/LiTS_I.dta` and obtained exactly `7cac43e2…8efc09`.** The checkpoint's recorded source identity therefore **links to the bytes currently on this disk**. This is the single most important identity linkage established in R1.

Producer ancestry chain (all locally present, read-only):
`source_identity_telemetry_receipt.json` → one authorized hash pass + one decoder call, exit 0 → `checkpoint_verification_receipt.json` (constructor round-trips, content-hash recomputation, 60/60 fact preimages, 77/77 role bindings all PASS) → `RETURN.json` → `banked_artifact_manifest.json` → `00_RETURN.md` terminal `PASS__FINAL_LITS_RETRY_BANKED_COMPLETE_CANONICAL_EMPIRICAL_CLOSURE__ZERO_SOURCE_RESUME_GREEN__FIABC_ORACLE_FROZEN__FF02_READY__NO_CANDIDATES_RUN`.

**Custody transfer is itself documented:** `LOCAL_CUSTODY/ephemeral_copy_verification.json` (schema `FIABC_LITS_FINAL_SUCCESS_EPHEMERAL_TO_PERSISTENT_COPY_VERIFICATION@1.0.0`) records `status: PASS__FULL_RETURN_TREE_BYTE_IDENTICAL`, `regular_file_count: 35`, `total_regular_file_bytes: 3,405,790,125`, `all_regular_files_sha256_identical: true`, and lists the checkpoint at 3,404,445,161 bytes with SHA-256 `2704fd3f…aa5726`, copied from the ephemeral production root `/private/tmp/fiabc-lits-final-canonical-closure-source-retry-r1/...`.

### Retained respondent / product coverage

| Dimension | Retained value |
|---|---|
| Respondents (source rows) | **29,002** |
| Source variables | **1,198** |
| Empirical candidates | **50** (49 `DISCOVERED_RESULT_SUPPORTED` + 1 `VALID_EMPTY`) |
| Query roles | **77 / 77 bound and closed** |
| Supported empirical facts | **60 / 60** with full preimages |
| Canonical object inventory | `EmpiricalFact@1.0.0` ×60, `EmpiricalQuerySpec@1.0.0` ×63, `EmpiricalPredicate@1.0.0` ×35, `AuthoritySnapshot@1.0.0` ×24, `DiscoveryAuthority@1.0.0` ×1, `DiscoveryResultReceipt@1.0.0` ×50, `EmpiricalUniverse@1.0.0` ×1 |
| Canonical empirical closure identity | `f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415` |
| Contracts | `PRE553_CARRIER_NEUTRAL_C11_I03_I05_EXECUTION_BINDING@1.0.0`, `PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0`, `PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0` |
| C11 logical release | `LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669`, content hash `192926fa…436df43f` |
| Execution / replay identity | `e547bfc6…3b85c5` / `dbd18f3c…428640` |

### Known reuse interface

- Canonical packet pointer: `…/current_i05_materialization_checkpoint_v3.json#/material/canonical_empirical_object_closure`
- Resume mode: `RESUME_VERIFIED_PARITY_READY_I05_CHECKPOINT` — verified with **0 source hash passes, 0 decoder calls, 0 candidate processes, 0 candidate outputs**
- `ff02_readiness_disposition.json` → `status: FF02_READY__NO_SOURCE_REOPEN_REQUIRED`, `source_reopen_required: false`, retrievable classes: `EmpiricalFact`, `EmpiricalQuerySpec`, `EmpiricalPredicate`, `AuthoritySnapshot`, `DiscoveryAuthority`, `DiscoveryResultReceipt`, `EmpiricalUniverse`, `unrecoverable_downstream_object_classes: []`
- Frozen companion oracle: `current_standard_lits_oracle.json`, 264,917 bytes, SHA-256 `cb1c6ae6f9ddef15d41897451ac9f60208d4615ea60ddbeaef8874ba1000e3f4`

### Can it be consumed in place by the authorized machinery?

**Yes — as recorded, and with the machinery present locally.**

- The producer/consumer module `rawlsing_next/fiabc_final_oracle_freeze_producers.py` exists in multiple local checkouts (`FIABC-LITS-executed-role-closure-repair/`, `FIABC-P2X-protected-b53/`, `FIABC-P2X-protected-b53-retry1/`, `FIABC-QF1-qualification-checkout/`, `LOCAL_QUALIFICATION/FIABC-LITS-I-SOURCE-LOCAL-HQD108/control-repair/`, and the HQD107 control variants).
- The C11 facade `rawlsing_next/pre553_source_backed_c11_facade.py` is present both live and as an immutable snapshot inside the custody payload.
- In-place reload is *demonstrated*, not asserted: the recorded zero-source resume re-validated the checkpoint's canonical JSON digest and complete object closure with **zero source access**, and re-materialized the frozen oracle byte-for-byte (`verify_frozen_oracle` PASS, identity `e5d66db4…18a98a`).
- Independent parity anchor: `astra_substantive_parity_receipt.json` (schema `FIABC_LITS_ASTRA_SUBSTANTIVE_PARITY_RECEIPT@1.0.0`) reports `status: PASS__CURRENT_LITS_EMPIRICAL_SUBSTANCE_EXACTLY_CONSERVES_ACCEPTED_ASTRA_D04_R2`, all 12 sections PASS.

### Genuine missing dependency for *this* checkpoint

**None found.** It does not need the raw `.dta`, a rebuild, or a re-export to be read. Its recorded document SHA-256 was **not independently re-hashed in this pass** (that would require bulk reading 3.4 GB, which was excluded by instruction), so its byte identity rests on: (a) two agreeing producer receipts, (b) `banked_artifact_manifest.json`, and (c) `ephemeral_copy_verification.json`. Status: **PRESENT_BUT_IDENTITY_UNVERIFIED (documentary, three agreeing independent records)**.

## 2. Distinguishing other LiTS-related retained objects (there is only ONE ~3.4 GB checkpoint)

A machine-wide scan for files >1.5 GiB (excluding unrelated media) returned exactly **one** object above 3 GiB — the checkpoint above. Other LiTS-adjacent retained objects are smaller and are **not** checkpoints:

| # | Object | Path | Bytes | What it actually is |
|---|---|---|---|---|
| 1 | **`current_i05_materialization_checkpoint_v3.json`** | `LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/payload/.../court/oracle_producers/LITS_I/` | **3,404,445,161** | **THE retained LiTS-I I05 materialization checkpoint (the 3.4 GB object).** Single file, schema `@3.0.0`. |
| 2 | `current_standard_lits_oracle.json` (13 copies total) | custody payload; `zero_source_resume/`; 11× `LOCAL_QUALIFICATION/…` | 264,917 each | Frozen standard LiTS oracle — the *consumer-facing* product of the same run, not a checkpoint. SHA `cb1c6ae6f9ddef15d41897451ac9f60208d4615ea60ddbeaef8874ba1000e3f4` is recorded for the two custody copies; the other 11 are size-identical only (not hashed here). |
| 3 | `LOCAL_COURTS/FIABC-SOURCE-LOCAL-LITS-I-R1-20260924/court/oracles/LITS_I.standard.json` | as named | 264,917 | Same oracle bytes staged into a court directory (identical size; documentary identity) |
| 4 | `lits_a_r5/` sharded carrier | `LOCAL_COURTS/FIABC-P2X-DISPOSITIVE-R1-RUN3-20260924/cells/LITS_I/A/durable/lits_a_r5/` | 2,121 × `.r5z` ≈ 216 MiB + `root.json` + `member_inventory.jsonl` (1,479,183 B, SHA `0d825556…`) | **Multi-part retained object**, schema `PRE553_R5_LONG_SHARDED_CARRIER@2.0.0`, carrier id `R5_LONG_SHARDED_TYPED_INCIDENCE_V1`, `canonical_row_count: 34,745,595`, `member_encoding: GZIP_COMPACT_JSONL@2.0.0`. This is a long-format incidence realization, **not** the checkpoint. |
| 5 | `ee_p2x_backend_state.json` | `LOCAL_COURTS/.../cells/LITS_I/A/durable/` | 10,833,598 | P2X backend stage state |
| 6 | `FIABC_LM2_R1E_FROZEN_Q291_PHYSICAL_CELL_CARRIER.json` | `FIABC-LITS-executed-role-closure-repair/WORKER_RETURNS/FIABC-LM2-R1F-CARRIER-ARCHAEOLOGY/LOCAL_OUTPUT/` | 83,340,882 | **WVS Q291** (`Q291G5`,`Q291P5`, `row_count: 97,220`) physical cell carrier. Despite living under a LiTS-named checkout this is a **WVS** product — do not treat as LiTS. |
| 7 | `pre553_source_backed_c11_facade.py` immutable snapshots | custody payload + court owner modules | 25,996 (SHA `9406f84b…`) | C11 facade code snapshot used by the receipt chain |

## 3. Status of the checkpoint

**PRESENT_BUT_IDENTITY_OR_CONSUMER_UNVERIFIED** — narrowly:

- **Presence: PHYSICALLY_PRESENT.** Full path, exact byte size, regular-file type confirmed by `stat`.
- **Consumer: verified in-record.** FF02 readiness green, zero-source resume PASS, machinery modules present on disk.
- **Byte identity: documentary, not re-proven here.** Three independent recorded SHA-256 statements agree (`2704fd3f…`), but this pass did not hash 3.4 GB.
- **Source identity: PHYSICALLY VERIFIED** — the checkpoint's recorded source SHA was reproduced against the physical `LiTS_I.dta`.

**GENUINELY_MISSING for this object: nothing.**
