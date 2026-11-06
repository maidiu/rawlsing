# L1 dynamic, severance and restoration evidence

**Status for every original-source/native effect:** `NOT_RUN_SOURCE_AND_DB_UNAVAILABLE`. No original respondent dataset, Postgres connection, external report/codebook corpus, host file rights or S2 native runner was available in this task. Importing V550 modules to exercise a synthetic fixture would not prove original per-source authority and was not substituted for native evidence.

## Reproducible S0 static execution actually performed

At frozen `9ba4764bef551b1ce498e5772d60b73d69337d4b` and current protected `fce43498e16e4709f3c9801e8717f0fdae18126a`, GitHub Contents API enumerated 189 immediate entries in `data/ddm_build_copy` (177 `*.py`) and 157 immediate entries in `rawlsing_next` (151 `*.py`). The 189 immediate legacy entries matched across these refs. The exact source bytes were read without executing those modules, Git-blob-verified against every file's Contents SHA-1, and their SHA-256 fingerprints recorded in `01_SCANNED_FILES.tsv`.

Reproduce on a rights-authorized machine:

1. Materialize `data/ddm_build_copy/*.py` at historic ref, and `rawlsing_next/*.py` at current ref, under `rawlsing_scan/`. Keep the Git Contents path/blob SHA/file byte-length index in `rawlsing_scan/blob_index.json`.
2. Run `python rawlsing_scan/scan_v550.py`, then `python rawlsing_scan/enrich_v550.py`. These scripts AST parse only. Their current-source results expect the 2026-11-06 protected ref above, not whichever branch becomes newest later.
3. Compare `01_SCANNED_FILES.tsv` for 328 verified Git blobs, `02_LEGACY_CALLSITES.csv` 881 exact static candidates, and `03_ASSET_REF_AND_FIRST_CONSUMER.csv` 31 anchored asset-priority cases. The source scanner and byte-index are included under this lane's `evidence/` folder for repeatability; they are not source-code changes.
4. `rg -n '_build_authority_receipt\(' data/ddm_build_copy --glob '*.py'` must return only the definition at wave-shard line 142. A different output means either future code changed or the scanned universe differs.
5. `rg -n -i 'QSM_FULL_QUESTION|v550_v551_response_semantics_contract_binding|response_scale_encoding_registry_35wave|question_relation_registry|position_conditioning_overlay|directionality_authority|first_pass_authority|response_option_map' rawlsing_next --glob '*.py'` returned no hits across the 151 immediate current Python files. This **does not** prove no indirect current consumption from other directories/configurations.

**Recomputed authority file-byte SHA-256:**

| Repo asset | Exact SHA-256 recomputed from Git-exact contents | Verification |
|---|---|---|
| `authority/v550_v551_response_semantics_contract_binding_v1.csv` | `89d0cb28c20f014278a58fcbb269b8726efe8a9580f2d470caa299ab113f00eb` | matches frozen binding manifest; 5,734 bytes |
| `authority/response_scale_encoding_registry_35wave_active_v1.csv` | `d270f59da94029780b0e7f26f78cc0f5ede418ed431b5ababeefd2c5e2a00fc8` | matches frozen scale manifest; 76,430 bytes |
| `manifests/question_use_overrides.csv` | `29e7706b7467f9435e57e78a7c8cf1314d9760f03d4d14d2bcf0d54f51809479` | exact Git blob data |
| `manifests/question_wave_itinerary.csv` | `866eb3ab25fbd9479781c15a0aecbb00a9d547fdc947cc443e8b904262b86eb3` | exact Git blob data |

The file transfer used a line-oriented staging patch that appended one terminal LF; hashes above were recomputed on the **original Git byte length**, not the augmented staging copy. Source-file SHA-1 reconstitution passed all 328/328 cases. The FQRA SHA from `SHA256SUMS.csv` is a **recorded manifest assertion**, not independently recomputed from its 47.8 MB file.

## Not-run native/mutation matrix and required observations

| Witness | Positive native setup | Mutation/severance to perform | Required observable first-consumer effect | Execution |
|---|---|---|---|---|
| L1-M01 FQRA | accepted exact source/wave/country/QRA row and current I03 projection | delete or alter exact row, retain source data | bridge eligibility/coordinate changes or typed refusal; I03 cannot remain silently positive through stale snapshot | `NOT_RUN_SOURCE_UNAVAILABLE` |
| L1-M02 QUC exception | previously certified QUC row with missing active QRA | remove QUC certification / mutate QRA matching | resolve whether :748–765 preserves rights lawfully; issuer-signed rule needed | `NOT_RUN_ISSUER_UNRESOLVED` |
| L1-M03 response | validated original codebook + 236/145 frozen response-binding assets | wrong hash, substitute unsigned/withdrawn report, reverse code label | no fabricated direction/intensity; frozen scale key mismatch refuses | `NOT_RUN_CODEBOOK_UNAVAILABLE` |
| L1-M04 overlays | chosen source/wave 4 exact overlay files | remove first pass, semantic, conditioning, directionality one at time | claimed fields/eligibility shift or typed unresolved; unrelated raw counts may continue | `NOT_RUN_OVERLAY_UNAVAILABLE` |
| L1-M05 source DB | exact respondent-long authority view, source/edition SHA and QSM table | swap view to legacy facet-ready or remove required columns | relation selection/errors and field outputs show chosen mode explicitly | `NOT_RUN_DB_UNAVAILABLE` |
| L1-M06 mapping cache | positive DB mapping query cold and warm | change one governing DB row without query text change | cache invalidates or typed refuses; compare cold/warm row hashes, source SHA and first reader | `NOT_RUN_DB_AND_CACHE_UNAVAILABLE` |
| L1-M07 source structure | accepted question_structure_register CSV | remove/alter split-child classification | no silent reclassification to substantive single-choice | `NOT_RUN_REGISTER_CSV_UNAVAILABLE` |
| L1-M08 aliases | source-native Latinobarómetro 2011/2024 physical vars | remove/alter exact aliased column/ruling | matched response-set, unknown/missing and coverage distinguish truthfully | `NOT_RUN_SOURCE_UNAVAILABLE` |
| L1-M09 shared substrate | accepted V550J registry/release and native prepared cache | revoke release or change response semantics hash | Parquet cache refuses/rebuilds with exact authority, not accepted by mere manifest | `NOT_RUN_L3_JOINT_UNAVAILABLE` |
| L1-M10 cold restore | exact original files and source bytes | restore after each controlled mutation | same computed digest/status/first-consumer result as cold before mutation | `NOT_RUN_NO_MUTATIONS` |

No digest, actual row delta, source/native first consumer, elapsed time or PASS is asserted for M01–M10. All execution results are `NOT_RUN`, and predicted changes above are future test specifications, not observed effects.

## Coverage arithmetic and remaining paths

The 881 AST sites are syntactic candidates, with 344 CLI/env selection calls, 191 I/O checks, 97 candidate authority helpers, 226 output/persistence writes, and 23 SQL/data operations. All have code line and expression; the precise set of runtime-fired sites depends on CLI options, source/wave, local files, DB state and later stage branches. Hence the **dynamic fired-callsite count is UNKNOWN**, not 881. No file was silently omitted from the known 177 legacy or 151 current immediate Python files; one outside-package source import and unbounded local/glob/DB readings remain.

Exact remaining owners: L1 for selected V550 native replay; L5 for report/FQRA/local archives and file SHA receipts; L6 for first-consumer and cache behavior; L3 for joint prepared cache; original issuer for conditional semantic law; L7 for final independent cold receiving.
