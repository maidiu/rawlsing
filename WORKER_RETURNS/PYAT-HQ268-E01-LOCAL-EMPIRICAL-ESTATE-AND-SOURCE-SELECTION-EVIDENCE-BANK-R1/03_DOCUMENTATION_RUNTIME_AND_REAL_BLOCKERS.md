# 03 — DOCUMENTATION, RUNTIME AND THE REAL BLOCKERS

**Mode:** bounded local inspection of project/data/documentation paths only. No whole-machine scan, no survey operations, no execution of any decode, no repository mutation.

---

## A. Documentation and retained products — what exists locally

### A1. Questionnaires and codebooks (immediately reusable, no source read required)

| Location | Contents | Count |
|---|---|---|
| `data/original codebook pdfs/` | Original questionnaires + codebooks as PDF: Afrobarometer r1/r5/r9 codebooks; Arab Barometer W1/W2/W5/W8 questionnaires; Asian Barometer W1/W2/W5/W6 questionnaires; EVS 1981/1990/1999/2008/2017 (CAPI+CAWI); GSS subdir; Latinobarómetro 1995/2011 codebooks + English instruments, 2024 questionnaire; LiTS I/II/III questionnaires + IV questionnaire; South Asia W1/W2; WVS W1/W4/W7 codebook + questionnaire each | **35** |
| `data/FINAL CODEBOOKS/FINAL FINAL CODEBOOKS/` | Normalized CSV codebooks for every CLOSED35 wave **plus 12 Asian Barometer W6 country codebooks**, with `.raw.csv` and `.bak_before_normalization` siblings | **128** |
| `data/FINAL CODEBOOKS/` | `FINAL_CODEBOOKS_SPEC.md`, `EVS_TREND_FILE_codebook.csv`, `WAVE8_ARABBAROMETER_*`, `WVS7_codebook_2.csv`, builder | 10 |
| `data/final_codebooks/` | Semantic layer: `questions_master.csv`, `questions_master_drivers.csv`, `questions_master_semantic.csv`, `codebook_index.json`, `item_content_map.csv`, `driver_source_coverage.csv`, scale-transform registry, onboarding reports | 22 |
| `data/Afrobarometer/` | Per-round codebook CSVs + `AB_R9.MergeCodebook…pdf/txt` | 49 |
| `data/Arabbarometer/` | `ABI_Questionnaire_ENG.pdf`, `ABV_Questionnaire_ENG_v2.pdf`, wave-VIII English instrument, per-wave codebook CSVs | 24 |
| `data/GSS/` | Per-wave `GSS*-codebook.csv` + per-wave `.sav` duplicates | 32 |
| `data/EVS/` | Per-wave instrument PDFs (`ZA4438_bq`, `ZA4460_bq`, `ZA3811_bq`, `ZA4800_q`, `ZA7500_bq_CAPI/CAWI`) + wave folders | 11 |
| `data/LiTS/` | `LITS I/II/III/IV codebook.csv`, `LiTSI/II/III/IV` questionnaire PDFs, `labelbook_lits_iv.xlsx`, builders + 4 alternate `.dta` | 18 |
| `data/WVS/` | `WV1_clean_codebook.csv`, source CSV/SPSS releases, builders, `EPR-2021.json` | 11 |
| `data/South Asia/` | `surveys_southasia_questionnaire_w1.pdf`, `sdsa-set-a-english-final…w2A.pdf`, `SOURCE_OF_AUTHORITY.md`, wave folders, `reports/` | 8 |
| `data/Asian Barometer/` | `SOURCE_OF_AUTHORITY.md`, per-wave codebooks, W1 merged data with `sampling procedures.doc`, builders | 14 |

**Sampling documentation:** present but thin — `data/Asian Barometer/W1 Merged Data/sampling procedures.doc`, `…/W1 Merged Data/Merge/` (merged release), and per-source design notes inside the manual-authority packets. No separate cross-survey sampling frame library was located in the bounded pass.

### A2. Variable dictionaries / registries (immediately reusable)

| Artifact | Bytes | Notes |
|---|---|---|
| `variables_by_wave_from_db_20260814.csv` | 5,220,571 | DB-extracted variable dictionary by wave |
| `respondent_table_columns_by_wave_from_db_20260814.csv` | 74,174 | Respondent-table column dictionary |
| `question_variables_by_wave_from_db_20260814.csv` | 123 | Question↔variable map (sparse) |
| `data/ddm_build_copy/manifests/question_structure_register.csv` | 26,582,238 | Full question structure register |
| `data/ddm_build_copy/manifests/country_identity_governed_registry.csv` | 298,517 | Governed country identity |
| `data/ddm_build_copy/manifests/respondent_wave_source_registry.json` | 16,335 | Respondent/wave → source registry |
| `Rawlsing_Full_Question_Relation_Authority_Final_R1_20260814/` | (dir) | `QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv`, canonical coordinate registry, authority status counts, `SHA256SUMS.csv` |
| `data/ddm_build_copy/manifests/source_dataset_manifest.csv` / `.yaml` | 7,284 / 13,117 | **All 44 datasets** with path/format/size; `sha256` column is **empty** (identity lives in the tree manifest instead) |

### A3. Established source-specific authorities (reusable as authority, not as data)

Nine manual-authority packets — unzipped and/or zipped:

`manual_authority/Rawlsing_{AFROBAROMETER,ARAB_BAROMETER,ASIAN_BAROMETER,EVS,GSS_ALL_EIGHT_WAVE,LATINOBAROMETRO,LITS,SOUTH_ASIA_BAROMETER,WVS}_…PACKET_….zip`

Unzipped siblings at project root: `Rawlsing_ARAB_BAROMETER_MANUAL_AUTHORITY_PACKET_REBUILT_20260713/`, `Rawlsing_GSS_ALL_EIGHT_WAVE_MANUAL_AUTHORITY_PACKET_20260717/`, `Rawlsing_LATINOBAROMETRO_MANUAL_AUTHORITY_PACKET_REBUILT_20260713/`, `Rawlsing_SOUTH_ASIA_BAROMETER_MANUAL_AUTHORITY_PACKET_20260715_MANUAL_ALIGNED/`, `Rawlsing_WVS_MANUAL_AUTHORITY_PACKET_20260716/`, plus `Rawlsing_EVS_MANUAL_AUTHORITY_PACKET_20260715.zip`.
Several contain `evidence/source_authority_manifest.csv`; hashes for the packets are in `evidence/input_archive_hashes.csv`.
Family-level provenance statements also exist as `SOURCE_OF_AUTHORITY.md` in `data/Asian Barometer/` and `data/South Asia/`.

### A4. Retained C11 / I03 / I05 products

| Product | Location | Status |
|---|---|---|
| **I05 materialization checkpoint (3.4 GB)** | `LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/payload/…/court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json` | See `02_…` |
| `i03_i05_closure_receipt.json` | same payload root (schema `FIABC_LITS_CURRENT_I03_I05_CLOSURE_RECEIPT@1.0.0`) | PASS, 50 candidates / 77 roles / 60 facts, 225 exact refs |
| `current_i05_precheck.json` (×2, byte-identical) | payload root + `LITS_I/` | 83,613 B, SHA `1ffbcb0f…` |
| `ff02_readiness_disposition.json` | payload root | `FF02_READY__NO_SOURCE_REOPEN_REQUIRED` |
| Frozen oracle `current_standard_lits_oracle.json` | 13 files: payload + `zero_source_resume/` + 11 `LOCAL_QUALIFICATION/…` copies; plus `LOCAL_COURTS/…/oracles/LITS_I.standard.json` | all 264,917 B (size-identical); SHA `cb1c6ae6…` recorded for the two custody copies only |
| C11 receipts | `LOCAL_COURTS/FIABC-P2X-DISPOSITIVE-R1-RUN3-20260924/cells/LITS_I/A/receipts/s02_c11_reachability.json`, `s04_i03_execution.json` | stage receipts |
| C11/I03 machinery | `rawlsing_next/pre553_source_backed_c11_facade.py`, `pre553_c11_repository.py`, `pre553_c11_ingest.py`, `pre553_c11_integrity.py`, `pre553_physical_c11_bridge.py`, `fiabc_lits_i_i03_operation_authority.py` (in `LOCAL_QUALIFICATION/FIABC-LITS-I-FRESH-MACHINE-READINESS-R1/checkouts/source-split-control/`) + tests | code present |
| Prior C11/I03/I05 evidence | `LOCAL_QUALIFICATION/…/WORKER_RETURNS/FIABC-LM2-R1H-C11-ORACLE/02_R15_REAL_MATERIAL_C11_RECEIPT.json`, `FIABC-LM2-R1K-R15-R16-ORACLE-CLOSURE/02_R15_COMMON_C11_RECEIPT.json`, `EE-P2R1/09_CARRIER_NEUTRAL_I03_I05_RUNNER_QUALIFICATION_RECEIPT.json`, `FIABC-CANONICAL-TERMINAL-READINESS-R1/18_LITS_RETAINED_I03_FACT_PREIMAGE_CLOSURE.md`, `FIABC-T5/01_POST_I05_ORACLE_MATCH_BINDING.md` | present |
| WVS7 retained carrier | `LOCAL_COURTS/…/cells/WVS7/` (1.4 GB incl. `.work/*.tmp.gz` runs) + `FIABC_LM2_R1E_FROZEN_Q291_PHYSICAL_CELL_CARRIER.json` (83 MB, 97,220 rows, `Q291G5`/`Q291P5`) | WVS, not LiTS |

### A5. Reusable now vs. needs new source-processing authority

**Immediately reusable (no source read, no new authority):**
1. All 35 CLOSED35 + 9 additional source files as *physical identity objects* (stat/hash only).
2. The 3.4 GB LiTS-I checkpoint, its frozen oracle, precheck, closure receipts and FF02 readiness — consumed in place, `source_reopen_required: false`.
3. 35 original questionnaire/codebook PDFs, 128 normalized codebook CSVs, semantic question master registers.
4. Variable dictionaries and question-relation authority CSVs.
5. Nine manual-authority packets + `SOURCE_OF_AUTHORITY.md` files.
6. Established manifests (tree SHA manifest, `source_dataset_manifest.*`, `SHA256SUMS.csv` families).

**Would require new source-processing authority (explicitly NOT done here):**
1. Any decode/row extraction from any `.sav`/`.dta` — including re-deriving codebooks from raw sources.
2. Any fresh candidate / P2X measurement run against LiTS-I or WVS7.
3. Re-hash or re-materialization of the 3.4 GB checkpoint (bulk read).
4. Closing the authority-path binding defect in §C3 (requires a governed commit/path repair or an issued authority change).

---

## B. Interpreter / tool availability (versions only; no survey operations)

| Tool | Version | Notes |
|---|---|---|
| `python3` (system project) | **3.11.3** at `/usr/local/bin/python3` | pandas 2.3.1, **pyreadstat 1.3.2**, numpy 2.3.2, scipy 1.16.3, PyYAML 6.0.3, pyarrow 22.0.0 |
| **Pinned project runtime** | **CPython 3.11.3** at `LOCAL_QUALIFICATION/FIABC-LITS-PRIMARY-MACHINE-BOOTSTRAP-R1/runtime-py3113/bin/python` | pandas 2.3.1, **pyreadstat 1.3.6**, **pyarrow 25.0.1**, numpy 2.3.2, scipy 1.16.3, PyYAML 6.0.3 — **this is the runtime named in the recorded readiness receipts** |
| `git` | 2.43.0 | available |
| `psql` | present (`/usr/local/bin/psql`) | client only |
| `sqlite3` | present (`/usr/bin/sqlite3`) | available |
| `shasum`, `openssl` | present | used for the two narrow hashes |
| `R` / `Rscript` | **absent** | |
| Stata | **absent** | |
| `julia`, `duckdb`, `jq` | **absent** | |
| Hardware / OS (from receipts + `sysctl`) | MacBookPro15,1, Intel Core i9-9880H, 17,179,869,184 bytes RAM (16 GiB), macOS 13.2.1 / Darwin 22.3.0, x86_64 | matches recorded readiness |
| Free storage now | **12 GiB / 466 GiB (98 % used)** on `/System/Volumes/Data` | see §C4 |

Both SAV and DTA decoding are covered locally by `pyreadstat` in either interpreter. No tooling gap blocks *reading* the estate.

---

## C. The true physical blockers, in three distinguished statuses

### 1. PHYSICALLY_PRESENT

| Item | Evidence |
|---|---|
| All 44 source files in `data/Data` (40 SAV + 4 DTA) | `stat`; 44/44 readable; sizes + mtimes match the 2026-08-23 SHA manifest exactly |
| All 35 CLOSED35 source identities | 1:1 mapping to registry indices 01–35, no gaps |
| 9 additional Asian Barometer Wave 6 country releases | present; correctly *outside* CLOSED35 |
| LiTS-I physical source `data/Data/LiTS_I.dta` | SHA-256 `7cac43e2…8efc09` **physically reproduced this pass**, equal to the checkpoint's recorded source identity |
| The ~3.4 GB LiTS-I retained checkpoint | single regular file, 3,404,445,161 bytes, exact path recorded in §02 |
| Frozen oracle, precheck, closure/parity/verification receipts, custody-copy verification | present with agreeing SHA-256 records |
| Questionnaires / codebooks / variable dictionaries / manual-authority packets | §A1–A3 |
| C11 / I03 / I05 machinery modules and receipts | §A4 |
| Python runtimes incl. the pinned `runtime-py3113` | §B |

### 2. PRESENT_BUT_IDENTITY_OR_CONSUMER_UNVERIFIED

| Item | What is verified | What is not |
|---|---|---|
| 42 of 44 source files (all except `LiTS_I.dta`, `South Asia Wave 1.sav`) | recorded SHA-256 exists in an established manifest; byte size and mtime match exactly | no fresh hash in this pass → **byte identity is documentary, not independently re-proven** |
| The 3.4 GB checkpoint itself | three independent recorded SHA-256 statements agree (`2704fd3f…`); custody copy verified byte-identical at transfer time | the 3.4 GB file was **deliberately not hashed** (bulk read excluded) → documentary identity only |
| 15 alternate/duplicate copies outside `data/Data` (4 LiTS + 8 GSS + 1 Latinobarómetro + 2 Asian Barometer) | same recorded SHA-256 as canonical in the same manifest run | not re-hashed; equal *recorded* hash ≠ re-proven equality |
| Consumer path for the checkpoint | FF02 readiness `NO_SOURCE_REOPEN_REQUIRED`, zero-source resume PASS with 0 decoder calls, modules present on disk | this pass did **not execute** the consumer (read-only mandate) |
| CLOSED35 census grades (20 P / 15 B) | historical representation-census record with immutable-commit evidence (EV035/EV036/EV040) | that is a *documentary* census, **not** a fresh rerun and not a statement about file presence |

### 3. GENUINELY_MISSING_OR_INACCESSIBLE

Nothing in the source estate or the LiTS checkpoint falls here. The genuine items are **authority/context defects that block re-running measurement**, not missing files:

| # | Genuine blocker | Precise statement | Blocks |
|---|---|---|---|
| **C1** | **Authority-path binding does not resolve in any local git tree** | The measured run of 2026-09-26 stopped with `CourtAuthorityStop("immutable commit unavailable")` for commit `3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f` and authority path `…/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/**AS2A_LITS1_SHARED_CERTIFICATION_20260827**/01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv`. **Verified read-only in this pass:** commit `3ce639e…` *is* present in three local checkouts, but the requested path has **0 matches** at that commit in *every* local repository; the file exists in the git tree only under the sibling directory **`banked_as2a/`**, and on disk only inside nested `_be1_immutable/…` snapshots. The directory `AS2A_LITS1_SHARED_CERTIFICATION_20260827/` has **0 entries** at `3ce639e`. | Any new candidate/P2X measurement run; **not** checkpoint consumption |
| **C2** | **No `.git` at the project root; commit availability is per-checkout and uneven** | `…/Rawlsing` is not a git repository. Producer commit `045d6270…` is present in `FIABC-LITS-executed-role-closure-repair/` (with `origin = https://github.com/maidiu/rawlsing.git`); protected execution head `16f5e7d5…` is present **only** in `LOCAL_QUALIFICATION/FIABC-LITS-I-MEASURED-SOURCE-RUN-R1-HQD107/protected-clean-16f5e7d/` and absent from five other local checkouts. | Re-derivation of commit-anchored authority from an arbitrary checkout |
| **C3** | **Storage headroom** | `/System/Volumes/Data`: 466 GiB total, **433 GiB used, 12 GiB free (98 %)**. The earlier readiness return recorded 614 MiB at its own live check. | Any run that must write multi-hundred-MB/GB durable state; *not* in-place reading |
| **C4** | **Session/power condition for future measured runs** | Documented and unmet by default: the machine idles to sleep after one minute on AC; any future run must keep lid open, user logged in, and run as a child of `caffeinate -dimsu` in a supervised terminal. `PreventSystemSleep=0` at last audit. | Any long measured run (procedural, not a missing file) |

**Explicitly not blockers, and not elevated to required service inputs:**
- Ghana — not investigated; nothing here makes it a service input.
- Any survey family — no family is required by default; the checkpoint is consumed without reopening LiTS at all.
- A raw `.dta` and its derived retained checkpoint are recorded as **two distinct objects**; the absence of one would not imply absence of the other. Here, **both** are physically present.
- The 9 Asian Barometer Wave 6 country files are additional releases, not gaps.
- Nothing was classified missing because it is absent *on another machine*.

---

## D. Terminal

```
LOCAL_EMPIRICAL_ESTATE_VERIFIED__RETURN_FOR_HQ
```
