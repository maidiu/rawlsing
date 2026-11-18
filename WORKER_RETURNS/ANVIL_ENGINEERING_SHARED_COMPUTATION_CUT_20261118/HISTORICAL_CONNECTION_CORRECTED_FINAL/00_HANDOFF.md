# Historical → current shared computation — corrected final account

## Status

**Documentary correction only. Supersedes author report `56eb6d084070e4a177809902909d636b0b215c6f`.**

- Review: `8c5da4d4a3a08c002275f28bfc886fe7d1da95a1`
- Disposition: `REVISE_EXACT_DOCUMENTARY_DEFECT`
- Product: `68aa7cac7cce7057fefd458ef4a06bec2dede1b2` — unchanged
- Product/tests/prototypes/benchmarks in this correction: **none**
- Old return preserved as superseded history
- Source facts independently verified; **this corrected text is not asserted independently accepted**
- Authoritative machine account: `historical_connection_corrected.json`

## Resolved review defects

### 1. Substrate grain — LONG, not wide

The old prepared substrate is **long respondent-variable records**, not a
one-row-per-respondent wide frame with question columns.

- **62 prepared + 5 additive = 67 required columns**, not 68.
- Artifact `row_count=25067` means **25,067 long rows**, not 25,067
  respondents.
- Long keys include `respondent_id`, `var_code`, `question_id`,
  `response_value`, `response_label`; grain columns include
  `source_norm`, `canonical_wave_norm`, `country_code_norm`,
  `respondent_id_norm`, `var_code_norm`.

The unsupported “old wide / current long causes cost” claim is removed. Both
old and current preparation are long-form.

### 2. Output count and consumption — 26 configured paths, not 22

The frozen manifest lists **26 output paths**, not 22.

`shared_respondent_substrate_mode=write` and one substrate with
`row_count=25067` prove the writer produced the substrate. The output list is
**writer-configured output evidence**; it does **not by itself prove all 26
products consumed that substrate**.

Actual downstream consumer evidence is separate:

- `compile_v550j_joint_response_patterns.py:1690-1725` loads/caches the
  explicit prepared country substrate.
- `1750-1759` uses that loaded frame for family products.
- The historical artifact is limited: it proves substrate write plus
  configured outputs, not all-product run consumption.

### 3. `babb256` source identity — local SHA-256 only

All six old local-file SHA-256 values match the frozen files, but
`babb256…` is a **bundle header / commit label**, not proven commit-to-each-file
identity for the local tree.

Source grade:

```text
LOCAL_SHA256_ONLY__BABB256_COMMIT_TO_FILES_NOT_PROVED
```

No invented Git blobs or file-level commit identity.

## Corrected mechanism comparison

### Old

PostgreSQL question-row extraction, then **one-time per-country
harmonization**, persisted as a **long respondent-variable prepared country
substrate** with schema, manifest, validation, content hash and `COMPLETE`
marker. It can be loaded **without reharmonization or DB access**.

Relevant paths:

- `build_determinicity_repository_v550.py:708-784, 787-825`
- `build_determinicity_wave_shard_v550.py:1328-1353, 1380-1389, 1391-1445`
- `ddm_v550_shared_respondent_substrate.py:25-105, 332-346, 565-637, 640-655`
- `build_v550j_prepared_substrate.py:316-374, 408-416`
- `compile_v550j_joint_response_patterns.py:1214-1236, 1690-1725, 1750-1759`
- `Rawlsing_V550_Fused_GSS_Proof_babb256_20260803/evidence/shard_manifest.json:56-81, 90-101`

### Current

Canonical **long 13-family** DirectEstateI03Session estate, temporary SQLite
`members(family,respondent,ref,gid,off)` with
`members_resp_idx(family,respondent,ref)`, one posting-index build per prepared
context, and per-query routing/object resolution. There is **no
query-independent selector** established in the frozen 68aa snapshot.

The canonical estate already avoids reharmonizing raw source per query. The
old one-time country harmonization and current canonical-estate preparation
must not be equated as identical costs.

## Cost layers

| Layer | Correct status |
|---|---|
| Redundant row-group reads | Repaired: R3 3,965 → locality G5 50 |
| Release index build | Shared per prepared session; one build per context |
| Routing/object validation | Still repeated for changing predicates/targets |
| Compatibility-specific core | Narrow exact-core only |
| Facts/member refs/output | Per-operation by design |

The grouped scope correctly shares exact RAW/WEIGHTED sibling cores
(selected/raw: 1 build, 1 hit). It does not share different target/predicate
cores (selected/f2: 2 builds, 0 hits), and is not proof of arbitrary distinct
query sharing or old all-product parity.

## Remaining decision for BrowserHQ/user

The selector is an **inference/candidate**, not forced architecture:

- **Narrow path:** does existing canonical-estate access need a small reusable
  authenticated routing/target lookup over the existing members index first?
- **Broader path:** does evidence justify persisting a derived long
  prepared-country view?

This is not a choice of backend or generic new architecture. A persistent long
substrate is a broader representation decision; the old artifact does not
establish a wide one-row-per-respondent frame or require that option.

No new production patch is requested. The existing two-edit grant covers only
the already-completed corrections; no three-owner historical-grant campaign is
proposed.

## Review resolution

| Defect | Correction |
|---|---|
| Long vs wide | Corrected: long rows, 67 columns, 25,067 long rows |
| 26 vs 22 / consumption | Corrected: 26 writer-configured paths; consumption evidence separate; run claim limited |
| `babb256` identity | Corrected: local SHA-256 only; bundle header identifies commit label only |

**HQ can receive this text correction proportionately without another G5 loop
unless new meaning is introduced.** Source facts are independently verified;
the corrected report itself is not claimed independently accepted.

**STOP after commit/push/remote verification.**
