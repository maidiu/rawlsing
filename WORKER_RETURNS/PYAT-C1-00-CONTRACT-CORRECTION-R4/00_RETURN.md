# PYAT C1-00 — exact UNKNOWN-currentness key synchronization — R4 return

Status: `C1_00_R4_EXACT_SELECTION_KEY_SYNCHRONIZATION_READY_FOR_INDEPENDENT_REREVIEW`

Terminal: `C1_00_R4_EXACT_SELECTION_KEY_SYNCHRONIZATION_READY_FOR_INDEPENDENT_REREVIEW`

Assigned branch:
`agent/rabochii-pyat-hq126-c1-00-contract-correction-r4`

Commission tip:
`4482f28e436a6ef48e66f9aefda40d354c3866f5`

Exact base / R3 return head:
`696210c2aca2c42b49eed1fe9f75dfca5bf2e93c`

This is a documentary exact-identity synchronization only. C1-01 was not implemented or executed. Production code/tests were not edited. Raw survey source reads: **0**. Historical R3 artifacts were not modified.

## 1. Independent owner-native derivation

Frozen current B5 owner:

`rawlsing_next/pre553_learned_product_lifecycle.py`
blob:
`a11c9eb73abab9be118ef4f0b6e325e676059f27`

Owner law:

1. `SelectionKey.semantic_projection()`;
2. `SelectionKey.ref -> _record_ref("SELECTION_KEY", semantic_projection)`;
3. `_record_ref -> semantic_hash(projection)`;
4. `semantic_hash -> sha256(canonical_json(projection).encode("utf-8"))`;
5. `LearnedProductLifecycleExecutor.selection_key(...)` constructs and registers that exact key.

Exact frozen R3 fixture refs:

- product family:
  `UNKNOWN-CURRENTNESS-FAMILY | urn:test:c1:r3:UNKNOWN-CURRENTNESS-FAMILY | 17e74d0419dbc1ee5c6c5aed6457bf6ae39bcfa54bdcb127e429727c03f5b1a9`
- selection scope:
  `UNKNOWN-CURRENTNESS-SCOPE | urn:test:c1:r3:UNKNOWN-CURRENTNESS-SCOPE | f8484aa71432f9f3db01fe855d5a67f34e61cde0ab0292072ebd556132d318f4`
- selection purpose:
  `UNKNOWN-CURRENTNESS-PURPOSE | urn:test:c1:r3:UNKNOWN-CURRENTNESS-PURPOSE | ce9057a86c14a0817bd06dd65a0ce7def2efe153cbeaf90f534d4a78095d427b`
- `consumer_context_partition_ref = null`

The exact owner-native semantic projection canonicalizes to 728 UTF-8 bytes and recomputes SHA-256:

`53683ac6353055af69af9f2d5cb93d889ccc5338b6aa915990c6a541ad942cb6`

Therefore the correct exact SelectionKey ref is:

`B5Lifecycle:SELECTION_KEY | urn:rawlsing:pre553:b5-lifecycle:selection_key:sha256:53683ac6353055af69af9f2d5cb93d889ccc5338b6aa915990c6a541ad942cb6 | 53683ac6353055af69af9f2d5cb93d889ccc5338b6aa915990c6a541ad942cb6`

The competing current-packet hash

`a0c54c568eee1351a67ecfee43c297e82aba509daf4bce6932b5ae7331ca03cd`

does **not** equal the owner-native recomputation from the exact frozen R3 fixture projection and is therefore classified:

`STALE_WRONG_FOR_EXACT_FROZEN_R3_FIXTURE`.

The historical R3 fixture's `53683ac...` identity was correct. R4 does not rewrite that historical artifact.

Exact derivation:
`WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R4/01_SELECTION_KEY_IDENTITY_RECOMPUTATION.json`

blob:
`1c242cc135d74476c90a73fcdcc7a2ffd36f6287`

## 2. Current packet propagation

The genuinely SelectionKey-dependent current packet files are exactly:

1. `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/analytical_contract.md`
   - blob: `0abe15f7e7365832fdd1dcfab45d2e831774f99a`
   - active exact identity synchronized to `53683ac...`
   - `a0c54c...` remains only in explicit stale/wrong explanatory prose.

2. `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/fixture_oracle_manifest.json`
   - blob: `3ea3a5938c72e00bb35593f607e1bf33299085fc`
   - active `selection_key_ref` synchronized to `53683ac...`
   - `a0c54c...` remains only under explicit `stale_wrong_ref` fields.

Administrative R4 state/bookkeeping was updated in:

3. `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/worker_return.json`
   - blob: `e03452cdaa62af07a8dcdca711bf409b1bae830c`
   - correct and stale refs are explicitly distinguished.

No other current C1 packet file contains either candidate hash.

Exact propagation audit:
`WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R4/02_PROPAGATION_AUDIT.json`

blob:
`f88d76605d6874d3f8577d057513c42807eff87e`

## 3. Preserved accepted identities

R4 finds no SelectionKey dependency in accepted R3-B, R3-D, R2-A, or R2-E identity preimages.

Therefore these remain unchanged:

- R3-B corrected query authority:
  `b59ef578314515268fa7b280a8480b4c95c80c9cfd831c39c2bfc4214b6fd767`
- R3-D forward evidence:
  `fe5cd7783ac84f0298fb7f56a621d7b0e494bd9348d080dc68ceee09abb546f5`
- R3-D reverse evidence:
  `b54201c8ba8743922e51627e621cc4f3d1c563a43b70167a0720fbb0028ccf72`
- accepted R2 A value-bearing condition relation
- accepted R2 E determinant/replay/invalidation closure.

No unrelated documentary hash was churned.

## 4. Explicit SelectionKey-ref recomputation check

R4 adds the previously missing deterministic check:

`recomputed_sha256 == 53683ac6353055af69af9f2d5cb93d889ccc5338b6aa915990c6a541ad942cb6`

Result: **PASS**.

The SHA-256 self-test `sha256("abc")` also reproduces the standard expected digest.

## 5. Changed blobs before this final return

Current packet:

- `analytical_contract.md` -> `0abe15f7e7365832fdd1dcfab45d2e831774f99a`
- `fixture_oracle_manifest.json` -> `3ea3a5938c72e00bb35593f607e1bf33299085fc`
- `worker_return.json` -> `e03452cdaa62af07a8dcdca711bf409b1bae830c`

R4 return artifacts:

- `01_SELECTION_KEY_IDENTITY_RECOMPUTATION.json` -> `1c242cc135d74476c90a73fcdcc7a2ffd36f6287`
- `02_PROPAGATION_AUDIT.json` -> `f88d76605d6874d3f8577d057513c42807eff87e`
- `03_UPDATED_BLOB_MANIFEST.json` -> `90c50bd4a338cd84ff2bbe727b2b65a7030315d7`

The updated blob manifest intentionally records its own self-reference limitation and freezes all prior changed blobs.

## 6. Scope / execution

- raw survey source reads: **0**
- C1-01 execution: **none**
- production-code edits: **none**
- production-test edits: **none**
- historical R3 artifact edits: **none**

Fresh independent R4 rereview remains mandatory before HQ may freeze C1-01.

The exact final branch head is the commit containing this return file; a Git commit cannot truthfully embed its own SHA in its own content. The exact committed branch-tip SHA is therefore reported by the worker immediately after this commit.

`C1_00_R4_EXACT_SELECTION_KEY_SYNCHRONIZATION_READY_FOR_INDEPENDENT_REREVIEW`
