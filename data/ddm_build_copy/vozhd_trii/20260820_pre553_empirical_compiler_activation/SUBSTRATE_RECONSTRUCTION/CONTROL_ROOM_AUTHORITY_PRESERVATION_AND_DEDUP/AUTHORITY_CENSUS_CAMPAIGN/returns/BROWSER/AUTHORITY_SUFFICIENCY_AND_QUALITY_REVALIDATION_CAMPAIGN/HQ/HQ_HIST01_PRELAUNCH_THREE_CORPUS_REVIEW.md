# HQ HIST-01 PRELAUNCH THREE-CORPUS REVIEW

Status: `BINDING_PRELAUNCH_REVIEW__HIST01_V2_MUST_USE_THREE_CORPORA__PRIOR_4794_ONLY_CONTRACT_SUPERSEDED`

Repository: `maidiu/rawlsing`

## 1. Why this review exists

HIST-01 V1 correctly found that the first committed `data/ddm_build_copy` tree is a curated transfer boundary rather than the epistemic origin of the pre-Vozhd pipeline. Before launching HIST-01 V2, two additional user-supplied local archives were inspected together with the already-reviewed Git-based archive.

The new archives materially change the recovery state. The prior HIST-01 V2 wording that treated the April-August Git archive as the sole archive corpus and treated `questions_master_drivers.csv` and `gss2010_structural_overlay.csv` as unrecovered exact objects is no longer accurate.

## 2. Corpus A — Git authority archive

Filename:

`Rawlsing_Authority_Document_Archive_2026-08-24.zip`

Observed size:

`92,475,343 bytes`

Observed SHA-256:

`e3f9e947e522f032998e29a7ff740f8d66e7e08934ca74c232965705dfbe49c8`

Selection basis:

- all reachable remote refs fetched 2026-08-24;
- Git commit window 2026-04-24 through 2026-08-24;
- authority-looking text artifacts;
- newest commit touching each path;
- normalized version families collapsed;
- code/tests/binaries/respondent data excluded.

Inventory:

- 4,794 logical records;
- 3,875 distinct SHA-256 contents.

This remains the exact Git-indexed archive corpus.

## 3. Corpus B — local April-August delta

Filename:

`Rawlsing_Authority_Document_Delta_2026-04-24_to_2026-08-24.zip`

Observed size:

`131,474,926 bytes`

Observed SHA-256:

`103da9799224a8f560fb65f9e6328d9dd5692babf07ce87087c8c6fb80fa6a4f`

Selection basis:

- local root `/Users/matthewsmith/Desktop/Rawlsing`;
- creation-time window 2026-04-24 through 2026-08-24;
- baseline = exact SHA-256 inventory of the first Git-based archive;
- exact contents already present in Corpus A excluded;
- 8,490 novel local candidates found;
- same-path version families and exact-content duplicates collapsed;
- 6,099 retained local documents;
- 2,387 collapsed local paths recorded separately.

Verified inventory facts:

- 6,099 inventory records;
- 6,099 distinct SHA-256 contents;
- **0 exact SHA-256 overlap with Corpus A**.

Therefore Corpus B is not a repackaging of Corpus A. It is a genuinely additional local-only recovery corpus.

## 4. Corpus C — older local authority archive

Filename:

`Rawlsing_Authority_Document_Archive_2025-08-24_to_2026-04-23(1).zip`

Observed size:

`3,143,278 bytes`

Observed SHA-256:

`6774a4c5bfa5a13601763149158c2aa42560f057faeac68f2d3d332c95811992`

Selection basis:

- local root `/Users/matthewsmith/Desktop/Rawlsing`;
- window 2025-08-24 through 2026-04-23;
- legacy source/question/driver/pipeline authority-looking artifacts;
- same-path version families collapsed;
- exact bytes retained.

Inventory:

- 73 logical records;
- 71 distinct SHA-256 contents;
- 9 SHA-256 contents also appear in Corpus B.

The overlap is historically useful: it proves exact-byte continuity for several pre-April authority objects into later retrieval packages.

## 5. Combined corpus denominator

Source inventory rows:

`4,794 + 6,099 + 73 = 10,966`

Distinct exact SHA-256 contents across all three corpora:

`10,036`

Do not confuse either count with the historical consumer denominator.

The consumer DAG remains the authority-necessity denominator. The three corpora are recovery/index evidence projected onto that DAG.

## 6. Major recovery: questions_master_drivers.csv

HIST-01 V1 classified:

`data/final_codebooks/questions_master_drivers.csv`

as consumer-proved but exact-object-unrecovered.

Corpus B contains exact bytes:

`Rawlsing_GSS_P3C_Joint_Authority_Codex_Ready_Cumulative_R4/Rawlsing_GSS_P3C_Joint_Authority_WORKING_HANDOFF_R4/04_AUTHORITY_EVIDENCE/questions_master_drivers.csv`

Observed size:

`16,864,669 bytes`

Observed SHA-256:

`d62accad0e956f739eada0718e4fb222429e7a90ed7889fff6f4f292b1a8a011`

Observed shape:

- 28,983 rows;
- 40 columns.

The same exact hash is independently pinned by:

- `R8_FINAL_FILE_MANIFEST.csv`;
- the GSS P3C R4 `FILE_MANIFEST.csv`;
- `Rawlsing_RETRIEVAL_PACKAGE_20260808/staging/04_QSM_ONTOLOGY_AUTHORITY/SHA256SUMS.txt` at canonical path `data/final_codebooks/questions_master_drivers.csv`;
- nested retrieval-package SHA manifests.

Corpus C additionally contains the older `data/final_codebooks/README.md`, which explicitly defines `questions_master_drivers.csv` as the **final driver-normalized master** and says the final-codebook family is rebuilt by `data/FINAL CODEBOOKS/build_final_codebooks.py`.

Current state is therefore:

`CANDIDATE_EXACT_HISTORICAL_BYTES_RECOVERED__ROOT_RUN_VERSION_AND_PRODUCER_LINEAGE_STILL_REQUIRE_PROOF`

It is no longer lawful to describe this object simply as unrecovered.

## 7. Proven continuity: questions_master.csv

Corpus C contains:

`data/final_codebooks/questions_master.csv`

SHA-256:

`74c69463163512fcb872181d92b04bf16755cf9c82a0f90e34fb2585a7015f75`

Size:

`31,737,473 bytes`

Shape:

- 15,615 rows;
- 19 columns.

Corpus B's 2026-08-08 retrieval package contains the same object under the same canonical logical path with the **same exact SHA-256**.

This proves byte-for-byte continuity of the base normalized question master from the pre-April local substrate into the August retrieval corpus.

Other exact old-to-later continuities include `content_keys.csv`, `item_content_map.csv`, `codebook_index.json`, the final-codebook README/spec, and selected source codebooks.

## 8. Major recovery: gss2010_structural_overlay.csv

HIST-01 V1 classified:

`data/final_codebooks/structural_registries/gss2010_structural_overlay.csv`

as consumer-proved but exact-object-unrecovered.

Corpus B contains exact bytes:

`p3c_r184_restore_20260802/Rawlsing_Codex_Ready_Cumulative_P3C_Closure_R184_20260802/repository_git/03_SEMANTIC_REFERENCE/gss2010_structural_overlay.csv`

Observed size:

`235,816 bytes`

Observed SHA-256:

`fe503dd46c842ac53b0410bf73fd6a93c98cd4362958229f52684afb66c70751`

Observed shape:

- 390 rows;
- 14 columns.

The same exact hash is independently pinned by:

- the P3C R184 `SHA256SUMS.csv`;
- `MULTIPART_SHA256SUMS.csv`;
- the pre-V553 freeze audit source inventory;
- multiple J-family handoff SHA manifests;
- the 2026-08-08 retrieval package under canonical path `data/final_codebooks/structural_registries/gss2010_structural_overlay.csv`.

Current state is therefore:

`CANDIDATE_EXACT_HISTORICAL_BYTES_RECOVERED__ROOT_RUN_VERSION_AND_ADOPTION_LINEAGE_STILL_REQUIRE_PROOF`

## 9. Generated reports/overlay gap materially narrowed

Corpus B contains 304 report-path authority/evidence objects, including many exact `data/ddm_build_copy/reports/*` objects that the curated Git root omitted.

Recovered families include first-pass authority tables, semantic authority overlays, directionality authority, response authority, V550 question-use contracts, source-structure outputs, and downstream validation/bridge material across GSS, WVS, EVS, LiTS, Afrobarometer, Arab Barometer, Asian Barometer, Latinobarometro, and South Asia.

Examples include exact report-tree objects for:

- GSS 2010 first-pass + semantic overlay;
- WVS W1/W4/W7;
- EVS historical waves;
- LiTS 2006/II/III/IV;
- Latinobarometro 1995/2011/2024;
- Arab Barometer I/II/V/VIII;
- Asian Barometer waves;
- South Asia W1/W2;
- Afrobarometer waves.

HIST-01 V2 must therefore treat the generated-overlay frontier as:

`MATERIAL_RECOVERY_CORPUS_PRESENT__EXACT_RUN_SELECTION_AND_PRECEDENCE_NOT_YET_PROVED`

not as generic payload absence.

The consumer's filename/wave/suffix/first-existing-candidate selection rules still require exact historical version/run tracing.

## 10. Database/runtime provenance materially improved but not closed

Corpus C contains pre-transfer documents such as:

- `BUILD_STATUS.md`;
- `v2/POSTGRES_SURVEY_LOAD_STATUS.md`;

which explicitly describe `DATABASE_URL`, `survey_microdata_respondents`, `survey_microdata_responses`, WVS `respondents`/`responses`, driver aggregates, loaders, source routing, and microdata fallback/walkback behavior.

Corpus A contains the 17 `survey_microdata_reload_manifest*` objects preserved in Git.

Corpus B additionally contains live-database contract/validation/provenance material.

This materially strengthens historical database reconstruction, but the **exact root-era live Postgres snapshot identity** is not yet proved. Keep that exact-snapshot question open unless a receipt/hash/version binding is recovered.

## 11. BF->LS / LY->YE adoption evidence recovered

HIST-01 V1 treated the embedded mappings as historically unexplained.

Corpus A contains `question_relation_registry_35wave_active_v1.yaml` and its schema. They explicitly declare:

- `country_identity_replacements`;
- `Afrobarometer R1: BF -> LS`;
- `Arab Barometer I: LY -> YE`;
- hard law that LS and YE are the current country identities.

This proves later governing/adoption evidence for the replacement rule.

It does **not** by itself prove what every earlier consumer meant by the embedded code constant, whether the replacement was semantically valid, or whether every reachable root-era run exercised it.

Reclassify the HIST frontier as:

`GOVERNING_REPLACEMENT_AUTHORITY_LOCATED__HISTORICAL_CONSUMER_USE_AND_SEMANTICS_STILL_TO_TRACE`

## 12. Necessity law for the archives

None of the three archives is itself authority merely by inclusion.

Do not preserve 10,966 files because they exist.

The required projection is:

`archive/local object -> exact producer/consumer/adoption/replay edge -> information distinction -> terminal successor/dead/replay/unresolved disposition`

Exact-content dedupe is allowed for byte identity, but path/selection identity must remain separate when a consumer chooses by path, filename, precedence, environment root, or release identity.

## 13. Consequence for HIST-01 V2

The prior 4,794-only V2 contract is superseded before execution.

HIST-01 V2 must:

1. validate and ingest all three corpora;
2. create a 10,966-row source-record ledger;
3. prove/reproduce the 10,036 exact-content-object union;
4. use full Git history plus local package provenance to connect recovered local bytes to historical consumers;
5. treat `questions_master_drivers.csv` and `gss2010_structural_overlay.csv` as recovered candidate exact objects rather than missing files;
6. re-adjudicate generated overlays from the recovered local report corpus;
7. preserve exact root-era DB snapshot identity as unresolved until proved;
8. crosswalk terminal information to the 68 TIRs only after historical dependency closure.

C09 remains blocked on HIST-01 closure or an explicit accepted residual historical uncertainty disposition.
