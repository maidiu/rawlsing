# 06 — EXACT AUTHORITY AND CONSUMER MISSING EDGES, PLUS LOCAL-VS-TRANSFER REPORT

**Mode:** documentary. Read-only against the working tree, local git object stores, the local archives/zips, and (for authority documents only) the remote branch via authenticated `gh`. **No `git fetch`, no `git add`, no file created or modified inside the repository.** Extracted reading copies live only under `/tmp/rawlsing_empirical_readiness_20261009/`.

**Authority reference frame:** `HQ_HANDOFF/LATEST.json` on branch `agent/hq249-prev3-service-demand-working-paper-r1` @ `dfc81f9d0b2694041ca9991b7c35db5f8fc3a` — `last_hq_decision HQD-2026-10-08-247`, `hq248_decision HQD-2026-10-08-248`, `hq249_decision HQD-2026-10-08-249`, `hq249_active_branches []`, `measured_execution_authorized_via_warrant false`, `raw_live_warrant_c7_actor_holds true`, `c4_adopted false`, `hq182_hold_lifted false`, `source_hold_unchanged true`, `operating_mode OPENCODE Space Bunny`, `hq_operating_law SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md`, `commission_io_law` and `concurrency_law` mandatory. Default-branch HEAD `25830fe7462bb9e29bc4087e6ae14f3f84cec377` contains **no** `PYAT_CONTROL_ROOM` (404) — every control-room document must be read from that branch.

---

## A. Authority missing edges — exact

### A1. Source-side authority

| ID | Missing edge | Exact locator | State | Class |
|---|---|---|---|---|
| **A-1** | Fresh SHA-256 for the two Afrobarometer files in the recommended bundle | `data/Data/Afro Barometer Round 5.sav` (49,689,458 B), `data/Data/Afro Barometer Round 9.sav` (70,621,348 B) | **Not hashed this pass.** R1 status `DOCUMENTARY_ONLY_NOT_REHASHED`; only `LiTS_I.dta` was physically re-hashed (`7cac43e2…8efc09`) | **local action, one-time** |
| **A-2** | Adoption of the Afrobarometer R5 same-source release | release `R5_GT34_Q2_Q69B_Q86A_SAME_SOURCE_CANDIDATE_R1`, terminal `PASS__GT34_Q2_Q69B_Q86A_SAME_SOURCE_RELEASE_MATERIALIZED__NO_ADOPTION`, holding `OBL049: LAWFULLY_CLOSABLE_AT_HQ_FAN_IN` | Materialized, court PASS (run `34014116929`, job `101434850326`, `6 passed, 55 warnings`), **not adopted** | **HQ decision** |
| **A-3** | Comparable-wave products for one accepted Afrobarometer R5↔R9 construct | `Rawlsing_P2_Afrobarometer_Accepted_Longitudinal_Continuity_Edges_v1.csv` (46,257 B, SHA `03cb2e90…bde93cc`) — 114 R5↔R9 edges, **51 `QUESTION_AND_RESPONSE`** | Continuity authority **accepted**; wave products **do not exist** for any of the 51 pairs | **new materialization** (pipeline proven for R5 Q2) |
| **A-4** | Pair-specific authority for an EVS 1990↔2008 temporal claim | `Rawlsing_P2_EVS_Accepted_Longitudinal_Continuity_Edges_v1.csv` — that exact pair has **5** edges | Would be **incompetent** as proposed by HQ249 D3; competent EVS pairs are 1990↔1999 (226) and 1999↔2008 (221) | **HQ-notice: D3 hypothesis fails here** |
| **A-5** | WVS7 callable governed projection / R5 compact carrier | EE-P2X blockers `R8C-WVS7-A-R5-COMPACT-CARRIER`, `R8C-WVS7-B-GOVERNED-PROJECTION-BINDING` | Proved gaps: *"No accepted WVS7 R5 compact carrier, R5LongShardedReader binding, or callable preparation binding exists; building one from the SAV would create forbidden carrier/projection work"*; *"no callable WVS GovernedC11Projection … Deriving one would add prohibited semantic/projection imp[lementation]"* | **blocked under prior law** — not on the recommended bundle's path |
| **A-6** | WVS7 produced learned product | `wvs7_standard_oracle_acceptance.json`: `candidate_outputs_seen: 0`, `candidate_processes: 0`; frozen expectation `candidate_count 46`, `query_role_count 58` | Expectation frozen (`FROZEN_READ_ONLY`, oracle identity `e546c155…42ef00`); **product absent** | not on recommended path |
| **A-7** | `WORKER_RETURNS/EE-R9L/01_PRODUCTION_CLOSURE_EVIDENCE.json` | authority commit `c88d2a92521de1f2ef85e41279194d7d4f5434cb`, cited by `EE-P2X/05_LITS_I_C_TERMINAL_BINDING_BLOCKER.json` | `git cat-file -t` **fails in all three local repos** (`FIABC-QF1-qualification-checkout`, `FIABC-P2X-protected-b53`, `FIABC-P2X-protected-b53-retry1`) | **TRANSFER REQUIRED** |
| **A-8** | EVS trend source `ZA7503` | declared in `…/manifests/survey_microdata_reload_manifest_EVS_TREND.json` as `/Users/matthewsmith/Desktop/Rawlsing/data/Data/EVS 1981-2017 TREND ZA7503_v3-0-0.dta`, 224,434 rows × 635 cols, 142,515,579 responses | **0 files match** anywhere under the tree | **TRANSFER REQUIRED** (blocks HQ249 E2 as written) |
| **A-9** | R1 blocker C1 — LITS slot-ownership projection exclusion ledger | cited as `…/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/AS2A_LITS1_SHARED_CERTIFICATION_20260827/01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv` | **OVERTURNED.** The file exists locally at `LOCAL_COURTS/FIABC-P2X-DISPOSITIVE-R1-RUN3-20260924/_be1_lits_projection/_be1_immutable/3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/AS2A_LITS1_SHARED_CERTIFICATION_20260827/` — **50,972 B**, alongside `04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json` (5,275 B) | **local, resolved** |
| **A-10** | Accepted within-source continuity-edge files for 5 families | `Rawlsing_P2_{Afrobarometer,WVS,EVS,GSS,Arab_Barometer}_Accepted_Longitudinal_Continuity_Edges_v1.csv` | **0 matches** under `/Users/matthewsmith/Desktop/Rawlsing` (full `find`). Present only inside `/Users/matthewsmith/Desktop/RawlsingsExcess.zip` at `RawlsingsExcess/Rawlsing_J_Family_Authority_Strategy_Handoff_v10_20260731/{09,10,12,15,19}_P2_*_PASS1/`. The 2026-08-23 combined manifest still lists them as live tree files | **local, but must be relocated/extracted under governance** |

### A2. Runtime / repository-side authority

| ID | Missing edge | Exact locator | State | Class |
|---|---|---|---|---|
| **A-11** | `rawlsing_next.pre553_runtime_authority` on the executing driver's path | EE-P2X wake: *"provide the exact repository-resident production runtime-authority dependency"*; observed as `ModuleNotFoundError` for `LITS_I/A/S02` and `LITS_I/B/S03` | **Not a missing file.** Present at `FIABC-QF1-qualification-checkout/rawlsing_next/pre553_runtime_authority.py` and in ≥10 other checkouts, plus `WORKER_RETURNS/RAWLSING-DUAL-ESTATE-RESOURCE-ATLAS-R1/documentary_copies/repository_snapshot/rawlsing_next/`. This is a **driver sys.path defect**, not a transfer gap | **local fix** |
| **A-12** | `WORKER_RETURNS/ASTRA-D04-R2/*` (required by the LiTS-C blocker: product SHA `47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d`, semantic replay `301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5`) | authority commit `e631de162c582423639b7067a4f36b29f8aa4d89` | **Blobs are in the local git object store, not checked out:** `git ls-tree -r -l e631de16… -- WORKER_RETURNS/ASTRA-D04-R2/` returns `00_RETURN.md` (7,259), `01_TYPED_LEARNED_EMPIRICAL_PRODUCT.json` (9,511, blob `26fa18d1…`), `02_77_ROLE_EXECUTION_RECEIPT.json` (1,766, blob `211e19bb…`), `03_SOURCE_AND_REPLAY_RECEIPT.json` (6,005, blob `b2c70e99…`). No `WORKER_RETURNS/ASTRA-D04-R2` directory exists in any working tree | **local materialization** (`git show`), no network |
| **A-13** | `WORKER_RETURNS/EE-R10L/02_CURRENT_19_ROLE_RUNTIME_BINDINGS.json` (`PARTIAL__RUNTIME_PREDICATE_REFS_RECOVERED__SEMANTIC_ATOM_CONTENT_HASH_PREIMAGES_NOT_YET_MATERIALIZED`) | authority commit `1d01bd7a1763bea642947557b924a7cfc6d15db6` | Blobs present locally (≥10 files listed by `git ls-tree -r -l`); **not checked out** | **local materialization** |
| **A-14** | Six-cell terminal state of the two-source run | `LOCAL_COURTS/FIABC-P2X-DISPOSITIVE-R1-RUN3-20260924/ee_p2x_stage_ledger.json` (schema `RAWLSING_EE_P2X_DARWIN_STAGE_LEDGER@1.0.0`, branch `agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`, head `a954e2d6676843da8427ef2439b5d1ef33478359`, manifest `9acc2f38…`, `source_order [LITS_I, WVS7]`) + `fiabc_driver_progress.jsonl` (17 events, stalled at stage 52/102) | All six cells `CELL_TERMINAL` with `state: CANDIDATE_LOCAL_FAILURE`; `LITS_I/A/S03_PARITY_ORACLE_GATE: PASS` then `S04_I03_EXECUTION: CANDIDATE_LOCAL_FAILURE`. `WORKER_RETURNS/EE-P2X/00_RETURN.md`: *"No final two-source measured PASS was claimed"*, status `BLOCKED__CANDIDATE_RUNTIME_AND_FINAL_VERIFIER` | **documented; not curable by transfer** |
| **A-15** | Protected head `16f5e7d5f691e908d85dc1dd26b8a59a29f668f4` | only checkout: `LOCAL_QUALIFICATION/FIABC-LITS-I-MEASURED-SOURCE-RUN-R1-HQD107/protected-clean-16f5e7d/` | Single-locus (R1 blocker C2) | **local, fragile** |
| **A-16** | Registered AT07 issuer (registrar / journal / epoch) | HQ249 §6: HQ holds narrow source-free `AT07_BIDIRECTIONAL_100` warranty, *"no installed registrar/journal/epoch"*, local Mac *"lacks independently controlled verifier administration"* | absent | **HQ / external** |

### A3. Document and manifest defects (exact, reproducible)

| ID | Defect | Evidence |
|---|---|---|
| **D-1** | **Cross-wave atlas manifest describes a different artifact at a non-existent path** | `data/ddm_build_copy/manifests/crosswave_atlas_file_manifest.csv` has 17 rows, **all `status=present`**, all pointing at `/Users/matthewsmith/Desktop/Rawlsing/outputs/crosswave_driver_atlas/…`. Root `outputs/` contains only `universality_20var_36wave_v550_552j_20260816T115854Z` and `…T115908Z` — **no `crosswave_driver_atlas` directory**. The real atlas is at `rawlsing_authority_documents_pack_20260627T040000Z/outputs/crosswave_driver_atlas/atlas_data.json`, **17,775,035 B**, **SHA-256 `55f306eec8ff30e846c58afd77fe10f8f32faa5c50d1b66a8c614db7077fd2e2` (computed this pass)**. Manifest records **17,770,643 B** / SHA `4713eee8566dafc651846bd02ff4fc441f201aa08f83af9da904ef436373c0bc` → size delta **4,392 B**, SHA cannot match. The four `csv_exports/*.csv` rows (`FamilySummary`, `WaveSummary`, `SharedGlossary`, `RegionalGlossary`) are recorded `present` but **`find -type d -name csv_exports` returns 0 matches anywhere**. Consequence: report 04 §1.4 rests on a **different revision** of the atlas than the manifest attests |
| **D-2** | **Five continuity-edge authority CSVs absent from the tree they are recorded in** | See A-10. Manifest generation date `2026-08-23T15:27:12.888083-04:00`; files dated `2026-07-31`/`2026-08-01`; absent today |
| **D-3** | **Manifest PATH column records basenames only** | Header claims `Columns: SHA256 \| SIZE_BYTES \| DATE \| TYPE \| PATH`, but entries read `… \| FILE \| Afro Barometer Round 5.sav` with no directory component, making the manifest unusable for locating files without a full-tree re-scan |
| **D-4** | **Superseded handoff still circulating** | `PYAT_CONTROL_ROOM/11_CURRENT_HQ_HANDOFF_20260926.md` carries a currentness notice: superseded; current sequencing is `15_HQD116_CONTROL_RECONCILIATION_AND_ROUTE_B_FORWARD_PROGRAM.md` + `HQ_HANDOFF/LATEST.json` |
| **D-5** | **GT34 Afrobarometer release not in the main tree** | 9 copies exist under nested checkouts (`FIABC-QF1-qualification-checkout/…`, `FIABC-P2X-protected-b53*/…`, `LOCAL_QUALIFICATION/FIABC-LITS-I-*/checkouts/…`); **0 copies under the main `data/ddm_build_copy`** |
| **D-6** | **CLOSED35 grades are a historical census, not current readiness** | `closed35.json` (B/P grades) and `report/K_CLOSED35_HORIZONTAL_MATRIX.md` (20 PASS / 15 BLOCKED at its own grain) must not be promoted as present-state competence |
| **D-7** | **Atlas mapping sparsity must not be read as non-comparability** | Atlas maps 0 rows for all EVS, GSS and LiTS waves (e.g. LiTS 2006 `0/1198`, EVS 1990 `0/390`), only 35/348 for Afro R5 and 73/613 for WVS W7. A zero is a mapping-layer artifact |

---

## B. Consumer missing edges (exact)

D1 disposition: `PARTIAL_SERVICE_IMPLEMENTATION_CONFIRMED__WORLD_CONSUMER_OPERATION_UNBOUND` — rich C1→F8 local computation is proven accepted; the join into a named service is not.

| ID | Consumer edge | What is proved | What is missing | Owner |
|---|---|---|---|---|
| **C-1** | **EE14 / PRE-V3 possibility consumer** for S1 | The demand requires an *admitted, reproducible* `q(Y|A)` then `q(Y|A,B)` **received by the selected consumer**, not a test-only precomputed scalar | The consumer's entrypoint, supported purpose, response type and supported/null use are **not named** | D1 → HQ |
| **C-2** | **N9 current/as-of objective-world selection** for S3.a | Field Forge relation machinery and context selection exist | *"Full N9 operation unbound"* (HQ249 D1 D3 table, S3 structural row) | D1 → HQ |
| **C-3** | **N10W positioned-subject / parent-prior capability** | — | Unbound; must be bound without instantiating a realized person (actor firewall) | D1 → HQ |
| **C-4** | **N10 rich multi-binding route** for S2 | The accepted one-binding scalar **N10E** wrapper exists | N10E is *not* presumed to encode an arbitrary multi-binding response; the already-lawful explicit multi-binding route must be selected (or a fully lossless contract independently demonstrated) | D1 → HQ |
| **C-5** | **Temporal → world consumer** for S3.b | 114 accepted R5↔R9 continuity edges exist | The demand requires the temporal product to be *"received by the selected structural/world/serving consumer, **not merely exist in an isolated test**"* — no such consumer receipt exists | D1 → HQ |
| **C-6** | **Release / replay / currentness contract** | LiTS I demonstrates the pattern: `FF02_READY__NO_SOURCE_REOPEN_REQUIRED`, zero-source resume PASS, affected/unaffected semantics inside the checkpoint | No contract binds *these three* sources to a consumer's as-of/replay expectation; affected-dependency invalidation on a changed input is undemonstrated for the bundle | D1 → HQ |
| **C-7** | **Independent falsifier per tier** | — | Targeted T0/T1/T2 falsifiers for S1–S3 are required in the `SELECTED_DEMAND_AND_INPUT_CONTRACT` join artifact and are not yet written | D1 + D3 |
| **C-8** | **Registered AT07 issuer consumption** | Narrow source-free `AT07_BIDIRECTIONAL_100` warranty held | Topology, independent ACK, root, model and use must be established for any chosen operation that *actually consumes* registered AT07 | HQ |
| **C-9** | **Native security / R3 quarantine** | — | `HQ248-OPEN-001` admission/construction leak, unbuilt production T1 ingress, mutable transitive trusted Python globals, unexecuted OOM/integrated P07→F7 positive, four historical forgeries. Narrow independent frozen-R3 review is permitted **in parallel** with no self-approved repair or cutover | separate independent court |

---

## C. Local vs transfer report

### C1. LOCAL — present now, no network needed

| Need | Exact locator | Verified how |
|---|---|---|
| Bundle source file 1 | `data/Data/LiTS_I.dta` 139,531,180 B | **physically re-hashed** `7cac43e2…8efc09` |
| Bundle source file 2 | `data/Data/Afro Barometer Round 5.sav` 49,689,458 B | present; size equals size in the GT34 Q2 release |
| Bundle source file 3 | `data/Data/Afro Barometer Round 9.sav` 70,621,348 B | present; manifest size matches |
| S1/S2 retained product | `…/court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json` 3,404,445,161 B | `stat` size; three agreeing recorded SHA records |
| S1/S2 frozen oracle | same dir `current_standard_lits_oracle.json` 264,917 B (SHA `cb1c6ae6…00e3f4`), plus 13 copies | present |
| S1/S2 long-format carrier | `LOCAL_COURTS/FIABC-P2X-DISPOSITIVE-R1-RUN3-20260924/cells/LITS_I/A/durable/lits_a_r5/` — 2,121 `.r5z` ≈ 216 MiB | present |
| S2 parity receipt | same dir `astra_substantive_parity_receipt.json` | present, all sections PASS |
| S3.a `S_2` release | `data/ddm_build_copy/recovery_integration/…/Q2_Q69B_Q86A_SAME_SOURCE_MATERIALIZATION_R1/` (9 copies) — `transport/q69b_q86a_same_source_transport.json.gz` 933,040 B etc. | present |
| S3.b continuity authority | extracted to `/tmp/rawlsing_empirical_readiness_20261009/_p2/Rawlsing_P2_Afrobarometer_Accepted_Longitudinal_Continuity_Edges_v1.csv` (source: `RawlsingsExcess.zip`) | read and counted (119/114/51) |
| WVS + EVS + GSS + Asian + LatAm + SouthAsia continuity authorities | same `_p2/` extraction + `Rawlsing_Authority_Document_Archive_2026-08-24/documents/other-authority-document/{24,25,26,27}_P2_*/…/02_WITHIN_SOURCE_CONTINUITY/` | read and counted |
| Cross-source seed table | `…/documents/source-and-question-authority/29_P2_ALL_NINE_CROSS_SOURCE_SEED_REFRESH/Rawlsing_P2_All_Nine_Source_Pairwise_Seed_Summary_v1.csv` | read (36 rows) |
| Continuity taxonomy | `…/documents/other-authority-document/07_P2_EXECUTION_CONTRACT/P2_Continuity_Edge_Taxonomy_v1.csv` | read |
| P2 per-family CURRENT_STATE | `…/documents/handoff-recovery-and-state/{09,10,12,19,27}_P2_*_PASS1/CURRENT_STATE.json` | read |
| Runtime-authority module | `FIABC-QF1-qualification-checkout/rawlsing_next/pre553_runtime_authority.py` (+ ≥10 more) | present |
| WVS7 oracle + carrier + authority | `…/FIABC-LM2-R1G-LOCAL-Q291/`, `…/FIABC-LM2-R1J-SAV-REPRESENTATION-AUTHORITY/`, `…/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/07_FRESH_WVS_ORACLE.json` (338,782 B), `WVS7.standard.json` (200,097 B) | present, terminals `PASS` |
| EE-P2X blocker receipts + stage ledger | `FIABC-QF1-qualification-checkout/WORKER_RETURNS/EE-P2X/…`, `LOCAL_COURTS/FIABC-P2X-DISPOSITIVE-R1-RUN3-20260924/…` | read |
| LITS slot-ownership ledger (R1 C1) | `LOCAL_COURTS/…/_be1_lits_projection/_be1_immutable/3ce639e1…/AS2A_LITS1_SHARED_CERTIFICATION_20260827/01_…CSV` 50,972 B | **present — C1 overturned** |
| HQ authority documents | `/tmp/…/_authority/{HQ249_R1,HQ249_D1_D3,11_CURRENT_HQ_HANDOFF,26_HQD216_…,24_HQD125_…,00_READ_ME_FIRST,15_HQD116_…}.md`, `LATEST.json` | retrieved from branch `dfc81f9d…` via `gh api …?ref=…` (read-only remote GET) |

### C2. LOCAL BUT NOT YET MATERIALIZED — needs a local, non-network action

| Item | Action required | Network? |
|---|---|---|
| `WORKER_RETURNS/ASTRA-D04-R2/{00,01,02,03}*` @ `e631de16` | `git show e631de162c582423639b7067a4f36b29f8aa4d89:WORKER_RETURNS/ASTRA-D04-R2/01_TYPED_LEARNED_EMPIRICAL_PRODUCT.json` etc. inside `FIABC-QF1-qualification-checkout` | **no** |
| `WORKER_RETURNS/EE-R10L/*` @ `1d01bd7a` | same pattern | **no** |
| Five `*_Accepted_Longitudinal_Continuity_Edges_v1.csv` | `unzip` from `/Users/matthewsmith/Desktop/RawlsingsExcess.zip` | **no** |
| Afrobarometer continuity edges back into the Rawlsing tree | governance decision on where they belong (they were recorded in-tree on 2026-08-23) | **no** |

### C3. TRANSFER REQUIRED — genuinely unavailable locally

| Item | Why | Impact |
|---|---|---|
| `WORKER_RETURNS/EE-R9L/01_PRODUCTION_CLOSURE_EVIDENCE.json` @ `c88d2a92521de1f2ef85e41279194d7d4f5434cb` | commit absent from all 3 local git repos | blocks any claim that Route-C determinants / Cacc2 atom bindings were ever proved |
| `data/Data/EVS 1981-2017 TREND ZA7503_v3-0-0.dta` (224,434 × 635) | declared, never present | blocks HQ249 **E2** (`ZA7503↔SRC12/SRC14`) as specified |
| `outputs/crosswave_driver_atlas/csv_exports/{FamilySummary,WaveSummary,SharedGlossary,RegionalGlossary}.csv` | recorded `present`, 0 matches | blocks CSV-level re-derivation of report 04 §1.4 |
| The atlas revision whose SHA is `4713eee8566dafc651846bd02ff4fc441f201aa08f83af9da904ef436373c0bc` (17,770,643 B) | only a 17,775,035 B revision (`55f306ee…`) exists | report 04 §1.4 cites a **different revision** than the manifest attests |

### C4. HQ-OWNED DECISIONS — neither local nor transfer

`measured_execution_authorized_via_warrant: false` · `c4_adopted: false` · `hq182_hold_lifted: false` · `source_hold_unchanged: true` · `raw_live_warrant_c7_actor_holds: true` · OBL049 adoption · naming of `A`,`B`,`Y` and of the EE14/PRE-V3, N9, N10W consumers · AT07 registrar/journal/epoch · independent frozen-R3 review scope · resolution of **IQ-1** (cross-family relational bridge vs substitution of report 04 Bundle 2).

### C5. Environment constraints observed this pass

| Constraint | Value |
|---|---|
| Disk | `/System/Volumes/Data` **433 GiB used / 466 GiB, 11 GiB free, 98%**; Rawlsing tree = 34 G. LiTS checkpoint alone = 3.4 GB |
| Scheduling | `caffeinate -dimsu` session required (R1 blocker C4); `caffeinate` processes observed running |
| Python | system 3.11.3 (`pyreadstat` 1.3.2, `pyarrow` 22.0.0); pinned `LOCAL_QUALIFICATION/FIABC-LITS-I-MEASURED-SOURCE-RUN-R1-HQD107/runtime-py3113/bin/python` (`pyreadstat` 1.3.6, `pyarrow` 25.0.1, `pandas` 2.3.1, `numpy` 2.3.2). GT34 Q2 ran on **Python 3.12.14** |
| Tooling | git 2.43.0; `gh` authenticated as `maidiu`; **`rg` unavailable** (use bounded `grep`); **`timeout` command unavailable**; whole-repo `grep -ril` exceeds 180 s |
| Read discipline | 3.4 GB checkpoint was **not** bulk-read; only bounded head/tail byte ranges were read |

---

## D. Next executable commission (proposed, not issued)

> **COMMISSION (draft) — PRE-V3 MINIMUM INPUT SET SELECTION RETURN**
>
> **Class:** documentary. **Warrant:** none implied; requires separate HQ seal. **Mutations permitted:** none in the repository. **Network:** read-only `gh api` against `maidiu/rawlsing` at branch `agent/hq249-prev3-service-demand-working-paper-r1` @ `dfc81f9d0b2694041ca9991b7c35db5f8fc3a` only.
>
> **Deliverable:** one artifact `SELECTED_DEMAND_AND_INPUT_CONTRACT` containing, in this order:
> 1. **Selected bundle** — accept, amend or reject report 04 Rank 1 `{LiTS_I, Afro_R5, Afro_R9}`; if rejected, state which of IQ-1, W1–W4 drove the rejection and name the substitute bundle from report 04.
> 2. **Fresh identity pass** — SHA-256 of `data/Data/Afro Barometer Round 5.sav` and `data/Data/Afro Barometer Round 9.sav` under warrant; compare to `c9200ba3…` and `3afcecd0…`.
> 3. **Local materialization report** — `git show` of `ASTRA-D04-R2` @ `e631de16` and `EE-R10L` @ `1d01bd7a`; `unzip` of the five `v1` continuity-edge CSVs from `RawlsingsExcess.zip`; report SHA-256 of each against the 2026-08-23 manifest.
> 4. **Named roles and consumer** — `A`, `B`, `Y` bound to existing LiTS I `EmpiricalPredicate`/`EmpiricalQuerySpec` object IDs; named EE14/PRE-V3 consumer, N9 operation and N10W route — or an explicit statement that they remain unbound.
> 5. **IQ-1 ruling** — accepted cross-source bridge for Afrobarometer↔LiTS, or substitution of report 04 Bundle 2.
> 6. **First real missing edge per service**, exactly one each: S1 = ?, S2 = ?, S3.a = ?, S3.b = ? — each as a named owner/contract/implementation/proof gap, not a restatement of "assembly unbound".
> 7. **Targeted falsifiers** — one T0 and one T1 per service, plus a T2 condition, each stating in advance what result would **disprove** the bundle's competence.
> 8. **Transfer list** — every item from §C3 with the exact holder and expected hash.
>
> **Explicitly out of scope:** raw `.sav`/`.dta` decoding; any statistic; any adoption; any warrant; any V3 actor; any change to `closed35.json`, K-matrix, `HQ_HANDOFF`, or the authority ceilings; any file written inside the repository.

**Highest-value single next step:** item 3 (local materialization of A-12/A-13/A-10). It converts three "missing" authorities into present bytes at zero network cost, and it is the only step that can prove or dismiss the LiTS-C blocker's D04 dependency before HQ spends a warrant.

---

## E. What this report deliberately does not do

- Does not select, adopt, warrant or authorize anything; the bundle in report 05 remains a proposal.
- Does not open any raw source file, compute any statistic, or assert any measured movement, direction or effect size.
- Does not convert a frozen oracle, a continuity edge, an atlas mapping or a cross-source seed row into an empirical product.
- Does not resolve IQ-1, name consumers, or speak for Astra (`HQ249_astra_audit` remains `HQ249_GATE_OPEN__…__P3_ASTRA`).
- Does not mutate, stage or commit any repository content; extracted reading copies exist only under `/tmp/`.

---

**TERMINAL:** `MINIMUM_EMPIRICAL_INPUT_SET_PROPOSED__NO_SELF_AUTHORIZATION`
