# HIST-01 V2 — FULL-HISTORY AUTHORITY-CONSUMPTION + ARCHIVE NECESSITY COURT

Status: `ISSUED__LOCAL_FULL_HISTORY_CONTINUATION__4794_DOCUMENT_NECESSITY_PROJECTION__C09_BLOCKER`

Repository: `maidiu/rawlsing`

## 0. Mission

Continue HIST-01 from its accepted partial evidence, but do not inherit its incompleteness as a conclusion.

The court has two exact missions:

1. complete the original `ddm_build_copy` → Odin → Dva → Trii → Chetiri producer/consumer authority DAG using a full-history Git-capable checkout;
2. project the user-supplied April–August authority-document archive onto that DAG and determine which of its 4,794 logical documents are actually necessary, successioned, replay/provenance-only, evidentiary-only, dead, unconnected, or unresolved.

The archive is not the historical denominator. Historically reachable consumers are the denominator.

## 1. Required environment

This is a **LOCAL FULL-GIT-HISTORY CODEX TASK**.

Required:

- repository checkout with all reachable refs used by the user's repository history;
- `git log`, `git rev-list`, `git ls-tree`, `git grep`, `git show`, `git cat-file`, `git diff`;
- Python or equivalent for deterministic inventory joins/hashes;
- access to the exact user-supplied archive named below.

No survey SAV/DTA execution is required for this court.

Do not perform broad archaeology outside the repository except for the exact supplied archive and exact already-named historical external inputs when necessary to classify a proved consumer edge.

## 2. Binding inputs

### Prior partial HIST-01

Exact partial worker HEAD:

`08185a88a7ea8d3b2f50847db8f4606cc54258b3`

Treat its return files as provisional evidence, not final truth.

At minimum read by exact commit:

- `returns/HIST-01/README.md`
- `returns/HIST-01/ROOT_COMMIT_PROOF.md`
- `returns/HIST-01/ROOT_SNAPSHOT_MANIFEST.csv`
- `returns/HIST-01/BACKWARD_PRODUCER_INPUT_EDGE_LEDGER.csv`
- `returns/HIST-01/FORWARD_AUTHORITY_EVOLUTION_LEDGER.csv`
- `returns/HIST-01/HISTORICAL_CONSUMER_DEPENDENCY_LEDGER.csv`
- `returns/HIST-01/HISTORICAL_AUTHORITY_OBJECT_LEDGER.csv`
- `returns/HIST-01/HISTORICAL_TO_CURRENT_TIR_CROSSWALK.csv`
- `returns/HIST-01/POTENTIAL_TIR_ORPHAN_LEDGER.csv`
- `returns/HIST-01/CODEX_CONTINUATION_INSTRUCTIONS.md`

### Current HQ intake law

Read:

`HQ/HQ_REC07X_V2_ADOPTION_AND_HIST01_PARTIAL_ARCHIVE_INTAKE.md`

### Authority-document archive

Filename:

`Rawlsing_Authority_Document_Archive_2026-08-24.zip`

Expected size:

`92,475,343 bytes`

Expected SHA-256:

`e3f9e947e522f032998e29a7ff740f8d66e7e08934ca74c232965705dfbe49c8`

Required archive control files:

- `AUTHORITY_DOCUMENT_INVENTORY.csv`
- `AUTHORITY_DOCUMENT_INVENTORY.md`
- `SELECTION_METHOD.md`

Expected inventory facts:

- 4,794 logical documents;
- 4,804 qualifying added paths before logical dedupe;
- 3,875 distinct content hashes;
- 0 extraction failures;
- window 2026-04-24 through 2026-08-24 inclusive;
- newest reachable commit touching each selected path;
- normalized version/revision/date families collapsed;
- source code/SQL/tests/fixtures/caches/archives/binaries/respondent-level data excluded.

If the archive SHA or inventory denominator differs, STOP before necessity classification.

## 3. Stage A — reproduce and complete the Git root proof

Mechanically prove the canonical first committed `data/ddm_build_copy` root.

Current partial candidate:

`a819fb35337ea28c4a83352d0040030b3da83a7a`

Do not trust it merely because the partial return says so.

Use full history to prove:

- ancestry/ref lineage;
- parent/root state;
- complete `git ls-tree -r --long` manifest under `data/ddm_build_copy`;
- every root object classified;
- whether independent earlier `ddm_build_copy` roots exist on other reachable histories;
- which root actually feeds the pre-Vozhd canonical lineage.

If the candidate changes, update all downstream ledgers accordingly.

## 4. Stage B — complete the producer/input DAG

For every historically reachable non-documentation authority-bearing or consumer-bearing object:

- prove actual reads/writes/import/query/generation edges;
- trace producers recursively to terminal leaves;
- trace inputs outside `data/ddm_build_copy` when consumers actually read them;
- identify environment/toolchain/default-order semantics when information-bearing.

Do not infer edges from names.

Priority partial gaps:

1. `data/final_codebooks/questions_master_drivers.csv`
2. `data/final_codebooks/structural_registries/gss2010_structural_overlay.csv`
3. generated `data/ddm_build_copy/reports/*` overlay packets and exact selection precedence
4. root-era `DATABASE_URL` and live Postgres relations/snapshots
5. exact V550J/joint-registry instances
6. execution-time `DDM_AUTHORITY_ROOT`
7. execution-time `RAWLSING_QUESTION_RELATION_AUTHORITY_PATH`
8. historical adoption/use of `BF -> LS` and `LY -> YE` aliases

## 5. Stage C — complete the forward consumer denominator

Enumerate every historically reachable executable/build/replay/analysis/runtime consumer across the pre-Vozhd line whose behavior depends on an authority-bearing object or implicit information rule.

For each semantic revision of a dependency record:

- exact consumer path/function;
- commit/range;
- authority/input object;
- fields/keys/distinctions consumed;
- direct/transitive/default/environment-mediated mode;
- predecessor/successor/adoption status;
- terminal relevance.

Explicitly search hidden authority in:

- row/file/glob order;
- first/last wins;
- default lookup names;
- aliases;
- null/missing coercion;
- numeric-code ordering;
- package/decoder behavior;
- generated IDs;
- manually copied artifacts;
- generated products later treated as inputs;
- release IDs and environment-selected authority roots.

Do not stop at Odin/Dva/Trii/Chetiri-named directories. Follow actual consumers.

## 6. Stage D — archive recovery pass

After the consumer/producer denominator exists, use the 4,794-document archive as a recovery/index corpus.

For each currently unresolved historical authority object or edge:

1. search the archive inventory by exact path, basename, authority ID, release ID, producer ID, field/schema signature, and known content hash;
2. if a candidate is found, verify archive member SHA against inventory;
3. verify the selected Git commit/path exists in full repository history;
4. trace the exact historical version actually consumed, not merely the archive's newest selected version;
5. use `git log --follow` / commit ancestry to recover older relevant versions when necessary.

Important:

`archive newest version != historically consumed version`

and:

`archive no match != historical absence`

The archive is permitted to point to evidence. It is not permitted to decide lineage.

## 7. Stage E — 4,794-document necessity projection

Create exactly one ledger row per `logical_id` in `AUTHORITY_DOCUMENT_INVENTORY.csv`.

Every one of the 4,794 rows must receive exactly one disposition:

### N1
`TERMINALLY_NECESSARY__EXACT_OBJECT_OR_LAW_MUST_SURVIVE`

Use only where an unsuperseded terminal consumer requires that exact content/law or a lossless exact successor is not available.

### N2
`HISTORICALLY_NECESSARY__INFORMATION_SUCCESSIONED__OLD_CARRIER_NOT_REQUIRED`

The object historically mattered, but every terminally relevant distinction is proved losslessly governed by later authority.

### N3
`REPLAY_OR_PROVENANCE_NECESSARY__CONTENT_REQUIRED_FOR_EXACT_RECONSTRUCTION_OR_AUDIT`

Not live semantic/runtime authority, but exact content is required to reproduce lineage, release identity, source selection, learned-product reconstruction, or governed audit.

### N4
`EVIDENTIARY_ONLY__USEFUL_BUT_NOT_TERMINAL_MACHINE_AUTHORITY`

Evidence/receipt/review useful to humans or courts but not required to preserve Rawlsing behavior or exact governed replay once binding authority/provenance survives.

### N5
`SUPERSEDED_REJECTED_OR_DEAD__NO_TERMINAL_INFORMATION`

Proved rejected, composted, superseded with no unique residual information, or unreachable dead legacy.

### N6
`DOCUMENTATION_HANDOFF_ONLY__NO_INFORMATIONAL_AUTHORITY`

Pure orientation/handoff prose with no unique governing distinction or replay dependency.

### N7
`UNCONNECTED_TO_REACHABLE_CONSUMER__NO_NECESSITY_PROVED`

Archive-qualified document exists but no producer/consumer/adoption/replay dependency to the historically reachable pipeline is proved.

### N8
`UNRESOLVED__DEPENDENCY_OR_SUCCESSION_NOT_YET_PROVED`

Evidence is insufficient to decide necessity safely.

Required fields:

- `logical_id`
- `archive_class`
- `pipeline_part`
- `original_path`
- `selected_commit`
- `archive_sha256`
- `necessity_disposition`
- `historical_authority_object_id`
- `producer_edge_ids`
- `consumer_edge_ids`
- `adoption_or_rejection_evidence`
- `terminal_information_distinction`
- `existing_tir_ids`
- `successor_object_or_law`
- `successor_proof`
- `replay_provenance_requirement`
- `necessity_rationale`
- `confidence_state`

No mass disposition based only on archive class or filename is allowed.

Identical-content hashes may share one proved rationale only when the distinct paths/roles are separately shown not to change consumption or authority identity.

## 8. Stage F — special direct checks from the archive

At minimum investigate these archive-backed candidate families against the proved HIST DAG:

- `data/ddm_build_copy/bindings/question_relation_registry_35wave_active_v1.csv`;
- Section-85 binding authority;
- Section-85 stage-artifact authority;
- bounded joint-configuration authority/adjudications/item crosswalks;
- Section-86 shared respondent-substrate contracts/returns;
- all `survey_microdata_reload_manifest*` objects;
- response-semantics and directionality authority objects actually selected by V550/V551/V552 consumers;
- source/question authority objects referenced by surviving consumer paths;
- release/manifest/provenance objects required to reproduce selected authority state.

The archive inventory currently does not directly show exact-path `questions_master_drivers.csv` or `gss2010_structural_overlay.csv`; verify by full Git history rather than concluding absence.

## 9. Stage G — TIR conservation crosswalk last

Only after the full historical DAG and archive necessity projection are complete, re-adjudicate every historically consumed information distinction against the frozen 68 TIRs.

Allowed states:

- `KNOWN_AND_TIR_ACCOUNTED`
- `HISTORICAL_AUTHORITY_FOUND__INFORMATION_ALREADY_SUCCESSIONED`
- `HISTORICAL_AUTHORITY_FOUND__TERMINAL_INFORMATION_NOT_YET_ACCOUNTED`
- `PRESUMED_BY_CONSUMER__EXACT_AUTHORITY_OBJECT_NOT_YET_RECOVERED`
- `DEAD_LEGACY__NO_TERMINAL_INFORMATION`
- `UNRESOLVED__INSUFFICIENT_HISTORICAL_EVIDENCE`

Do not create a new TIR merely because a historical file is missing. Create/recommend reopening only when a **terminal information distinction** is proved outside the existing 68.

## 10. Required outputs

Write only under:

`.../AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/returns/HIST-01-V2/`

Required:

1. `README.md`
2. `ROOT_COMMIT_PROOF.md`
3. `ROOT_SNAPSHOT_MANIFEST.csv`
4. `FULL_HISTORY_REF_AND_ANCESTRY_RECEIPT.md`
5. `BACKWARD_PRODUCER_INPUT_EDGE_LEDGER.csv`
6. `FORWARD_AUTHORITY_EVOLUTION_LEDGER.csv`
7. `HISTORICAL_CONSUMER_DEPENDENCY_LEDGER.csv`
8. `HISTORICAL_AUTHORITY_OBJECT_LEDGER.csv`
9. `AUTHORITY_ARCHIVE_INPUT_RECEIPT.json`
10. `ARCHIVE_NECESSITY_LEDGER.csv` — exactly 4,794 logical rows
11. `ARCHIVE_CONNECTED_AUTHORITY_DAG.csv`
12. `ARCHIVE_NECESSITY_COUNTS.json`
13. `UNRECOVERED_OR_UNVERSIONED_INPUT_LEDGER.csv`
14. `HISTORICAL_TO_CURRENT_TIR_CROSSWALK.csv`
15. `POTENTIAL_TIR_ORPHAN_LEDGER.csv`
16. `EXHAUSTIVENESS_CHECKLIST.md`
17. `CHANGED_FILES.txt`

## 11. Closure law

Strong closure is permitted only when:

- root/ancestry is mechanically exhaustive;
- every root non-doc object is classified;
- producer/input graph is exhausted or explicitly unresolved;
- forward material mutations are exhausted;
- every reachable historical consumer dependency is enumerated;
- every dependency maps to authority/object/default state;
- all 4,794 archive logical documents are necessity-classified;
- every N1/N2/N3 row is linked to concrete dependency/replay evidence;
- every historical dependency maps to TIR/succession/dead legacy/orphan/unresolved;
- no unaccounted consumer edge remains.

Terminal returns:

`HIST01_V2_COMPLETE__PREVOZHD_AUTHORITY_DAG_AND_ARCHIVE_NECESSITY_EXHAUSTIVE__NO_UNACCOUNTED_TERMINAL_INFORMATION`

or

`HIST01_V2_COMPLETE__TERMINAL_INFORMATION_ORPHAN_FOUND__TIR_UNIVERSE_REOPEN_REQUIRED`

or

`HIST01_V2_PARTIAL__REACHABLE_DEPENDENCY_OR_ARCHIVE_NECESSITY_REMAINS_UNRESOLVED`

or

`HIST01_V2_BLOCKED__FULL_HISTORY_OR_ARCHIVE_INPUT_UNAVAILABLE`

Stop token:

`HIST01_V2_FULL_HISTORY_AND_ARCHIVE_NECESSITY_RETURNED`
