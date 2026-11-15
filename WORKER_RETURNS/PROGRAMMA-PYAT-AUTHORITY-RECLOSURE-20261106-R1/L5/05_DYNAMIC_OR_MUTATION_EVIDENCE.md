# L5 — dynamic selection and mutation/severance/restore evidence

## Execution envelope and exact reproducibility

- S0–S1: GitHub connector reading only at immutable `9ba4764bef551b1ce498e5772d60b73d69337d4b`, plus A02 exact branch `836be4f98e821d7d510981aee7dfbbdc318f6f4b`. The protected integration ref was separately observed at `fce43498e16e4709f3c9801e8717f0fdae18126a` when the worker branch was created.
- Git tree metadata enumerated: **9,135 tracked files**, all 21 top-level subtrees nontruncated. This proves names + Git blob SHA-1 and sizes, not local content SHA-256 or runtime loads.
- Full UTF-8 contents read: **177 top-level legacy `data/ddm_build_copy/*.py`** and **151 top-level `rawlsing_next/*.py`**, plus **53** small frozen manifests/authority files and the frozen P10 commissioning court (54 frozen documentary/manifest files total). No packaged original respondent bytes were read. A02 3 precursor files separately fetched (the 27-row estate comes from that branch).
- **1,675** machine-extracted static site-lines across 177 legacy scripts: 608 dynamic/path; 316 file IO; 76 DB; 48 authority-function; 31 env; 596 CLI. This is **line-site enumeration, not AST proof that all calls are covered**. Each has exact file/blob SHA and line in `02_LEGACY_CALLSITES.csv`.
- **8,753** frozen tracked file contents not read (9,135 minus 382 code/manifest/docs; A02 branch separate). Their metadata are still enumerated. No attempt to declare zero unvisited semantic authority files; potential extra dynamic reads are **UNKNOWN**.
- **1,675** site-lines remain not promoted to proven authority-to-current-first-consumer edges; exact count of unobserved dynamic runtime calls is **UNKNOWN**, not zero.
- Local inventories and oldMac: `NOT_AVAILABLE`. A local Python shell exists but no checked-out authorized repo/native source estate or verified original-source permissions; no S2 source/native tests performed.

## Proven static legacy selection paths

| Historical site | Code evidence | Static implication | Required dynamic falsifier |
|---|---|---|---|
| FQRA/QRA | `ddm_v550_question_relation_authority.py:28-34,298-307,448,500-567` | Explicit path > `RAWLSING_QUESTION_RELATION_AUTHORITY_PATH` > `DDM_AUTHORITY_ROOT` > full R1 path; calibration QRA loads separately | Exact env-default audit, 680/20 status semantics, mutate/revoke one file with same source |
| Response semantic binding | `ddm_v550_response_semantics_authority.py:128-146,174-194`; `ddm_v550_response_options.py:527-535` | Manifest SHA and certified set; live map initially `UNRESOLVED_LIVE_BUILD` then governed binding | Alter one accepted response-option source with unchanged source data; confirm bound output changes or typed refusal |
| Per-wave overlays | `ddm_v550_family_overlay.py:78-84,100-201`; `ddm_v550_question_use.py:2297-2318` | Dynamic family+wave filename search, optional missing, source/wave semantic calls | Two conflicting files in competing roots; exact selected accepted revision and no shadow promotion |
| Itinerary/manual overrides | `ddm_v550_question_use.py:46-49,786-800,873-880,1388-1425` | Default manifest + optional override applied to allowed uses; missing/unreadable returns empty | Remove file; require new PRE553 consumer typed refusal if authority claimed |
| Variable aliases | `ddm_v550_var_aliases.py:17,38-98`; `build_determinicity_repository_v550.py:870,1564` | Bounded explicit Latinobarómetro mapping, not universal string surgery | Alias mutation/removal gives exact unresolved/mapped changes |
| V550J family authority/cache | `compile_v550j_joint_response_patterns.py:89,172-269,1332-1346,1497,1725-1737`; `build_v550j_prepared_substrate.py:298-313,342-371` | Explicit registry path and bounded executable release; cache signatures conditional on supplied hashes | Wrong release, missing hash, stale Parquet with same source, fail-closed and exact restore |
| Current PRE553 capability | `pre553_empirical_authority.py:1-5,162,240-264`; `pre553_c11_ingest.py:451-465`; `pre553_authority_maintenance.py:1550-1573` | Exact supplied snapshots/refs and approved lifecycle, but no proven ingest of historic file-specific decisions | Inject sealed historic asset capsule; real first consumer must bind exact accepted scope and refuse corruption |

## Test matrix: NOT_RUN

| Test | Status | Reason / next owner |
|---|---|---|
| Repo manifest-declared SHA versus original physical bytes | NOT_RUN | Local source files absent; asset custodian must grant read-only host/file access |
| A02 27 item physical byte and status cross-check | NOT_RUN | Some origins are Library/local historical sources not exposed in this session; A02/P10 owner |
| OldMac 2,864-file inventory content-hash crosswalk | NOT_RUN | No explicit oldMac file/host permission; local custodian |
| Source-equivalent valid-authority mutation | NOT_RUN | Authorized original S2 source/data + qualified target consumer unavailable; R5/R6 |
| Missing/revoked/wrong-version/conflicting/manual-shadow cases | NOT_RUN | No governed runtime target and original assets; R5/R6 |
| Stale prepared-Parquet cache then restoration exact digest | NOT_RUN | No S2 prepared cache/original source; R3/R6 |
| F1–F4 conditional applicability and all35 original source execution | NOT_RUN | Requires separately authorized source-specific access; Pyat HQ |

## Required future dynamic run receipt

For each original authority input: record exact source bytes SHA-256, selected path/CLI/env order, current authority status and revision, original normalized assertion grain, first caller + first actual consumer, output digest before; mutate one authority fact with unchanged source, show changed field or exact typed refusal; separately missing/version/conflict/revocation/stale cache; restore original bytes and compare exact output digest. Unknown, shadow and nonapplicable must stay distinct.

**Do not turn this static audit into a local runtime claim or seal a positive readiness.**
