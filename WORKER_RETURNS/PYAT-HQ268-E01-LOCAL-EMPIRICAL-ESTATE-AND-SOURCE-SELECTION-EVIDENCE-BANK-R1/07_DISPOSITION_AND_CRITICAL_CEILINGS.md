# 07 — DISPOSITION AND CRITICAL CEILINGS (PYAT HQ268 E01)

**Commission:** `WORKER_COMMISSIONS/PYAT-HQ268-E01-LOCAL-EMPIRICAL-ESTATE-AND-SOURCE-SELECTION-EVIDENCE-BANK-R1/00_COMMISSION.md`
**Commission blob:** `ee9ac0e55a4402682abccc7bf32fda77f5e843da` (8,048 B, read unchanged at commission tip)
**Disposition:** BANKING ONLY. Reports 00–06 are reproduced byte-identical to the local originals. This file is the only text added. No claim in 00–06 was rewritten, upgraded, corrected in place, or re-derived.
**Adoption:** NONE. `UNADOPTED`, `FOR_INDEPENDENT_HQ_COURT`.

---

## 1. Executor identity, local paths, hashes, branch geometry

| Item | Value |
|---|---|
| Agent / tool | OpenCode CLI worker (`opencode`), authenticated `gh api` (account `maidiu`, scopes `repo`) |
| Actual model | `opencode/mimo-v2.6-flash-free` — **MiMo V2.6-Flash** (declared as required; declared sufficient for mechanical documentary banking) |
| Machine | The Mac holding `/Users/matthewsmith/Desktop/Rawlsing/data/Data/` — macOS 13.2.1 (22D68), `x86_64` |
| Local report directory | `/tmp/rawlsing_empirical_readiness_20261009/` |
| Local banking scratch | `/tmp/hq268_e01/` (commission copy, upload log `upload_log.json`) |
| Remote branch | `agent/opencode-pyat-hq268-e01-local-empirical-evidence-bank-r1` |
| Frozen canonical issuance base (branch base) | `a12f619d8cc109f1245824a3ef220d3b5beb0d9a` |
| Commission tip (resolved before work; parent = base) | `b323ce465b5016201ebc02df34263177c1a33e52` |
| Committed remote head **after the seven uploads** | `9cb1fc59975e629def33fddedd3483bc131d4b41` |
| Final remote head after **this** `07` upload | recorded in the worker return (this file's own upload necessarily changes the head; it is the last of eight) |

### Reports 00–06 — sizes and SHA-256 (local, pre-upload; all seven available)

| # | File | Bytes | SHA-256 |
|---|---|---|---|
| 00 | `00_SOURCE_ESTATE_INVENTORY.md` | 6,632 | `77c81e23f881570aeaa56dc1cd0e360ac87244b5d36f5a77965d8acb485cec3f` |
| 01 | `01_SOURCE_IDENTITIES.json` | 175,250 | `2e844ef317bcdd58f9a40c0b72ae4447ecd3501390a37f410b6fe6ee9941acf9` |
| 02 | `02_LITS_CHECKPOINT_AND_RETAINED_PRODUCTS.md` | 10,205 | `771514d934aee1dae50c07e8aae49f2768a4a483241ce4af10d6d855dd38ba50` |
| 03 | `03_DOCUMENTATION_RUNTIME_AND_REAL_BLOCKERS.md` | 15,061 | `3d757e2a76caa4b4c5fcef97c6141c9bf2b70035dd14d0c3e69edc335a3522d2` |
| 04 | `04_MINIMUM_CANDIDATE_SOURCE_BUNDLES.md` | 28,000 | `eb0e7ea6a82ec967de54f5a5ddff65eab910d4a180b7b5278626e57a82039567` |
| 05 | `05_RECOMMENDED_EMPIRICAL_SOURCE_CONTRACT.md` | 16,933 | `8c726ed4b8212ebbcc0e50ccc0078776628014272eed077e04745c01e5555588` |
| 06 | `06_EXACT_AUTHORITY_AND_CONSUMER_MISSING_EDGES.md` | 24,153 | `fec8b4ee9b97d03ea996370a760faaa665b07076671ea0fdb1f6541ad7cd0b97` |

**Unavailable reports: none.** All seven existed locally and were uploaded.

**Not uploaded (not commissioned, listed for completeness):** `build_inventory.py` (13,810 B), `_authority/` (eight HQ authority documents fetched read-only), `_p2/` (three extracted continuity-edge CSVs), plus local auxiliary files `00…06` siblings `__pycache__`. These remain local only.

**Redactions performed: none.** No secret, token, credential, microdata row, respondent value, or binary payload was found or included in reports 00–06. A pre-upload scan of 00–06 for GitHub token prefixes, AWS access-key prefixes, PEM private-key headers and HTTP bearer headers returned zero matches. Absolute local research paths (13 unique `/Users/matthewsmith/…` prefixes) were retained unredacted in this private repo, as permitted by the commission.

**Governing checkpoint (binding, supersedes the primary reports' frame):** `HQD-2026-10-09-268`, `HQ_HANDOFF/LATEST.json` on `integration/pre-main-reconciliation-r1`, frozen canonical issuance base `a12f619d8cc109f1245824a3ef220d3b5beb0d9a`.

---

## 2. Local estate result as reported by the study (not re-verified here)

Reported local study finding from `00`/`01`, preserved verbatim in grade and scope:

- **44 / 44** source files present and readable in `/Users/matthewsmith/Desktop/Rawlsing/data/Data/`.
- **35 / 35** CLOSED35 registry identities present; **9 additional** files are Asian Barometer Wave 6 national country files not in CLOSED35 (so 44 = 35 + 9). *Commission wording "44/44 CLOSED35 inventory & 9 extra Asian Barometer W6 national sources" reads slightly differently from the study; the study's own composition (35 CLOSED35 + 9 extra = 44) is recorded here rather than being silently harmonised.*
- Composition **40 SAV + 4 DTA**; 0 genuinely missing or inaccessible.
- **44 / 44** have a previously recorded SHA-256 in the established manifest `/Users/matthewsmith/Desktop/Rawlsing_and_RawlsingsExcess_tree_sha_size_date.txt` (generated `2026-08-23T15:27:12.888083-04:00`), and **44 / 44** match that manifest on byte size *and* mtime.
- **Freshly re-hashed this pass: 2 only** — `LiTS_I.dta` (139,531,180 B → `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`, which also matches the `source_identity.sha256` recorded inside the retained checkpoint) and `South Asia Wave 1.sav` (595,974 B → `de7b51f9abf455b072555a84c5592e3ac46bb32c4f9f61bc055160f7d871e571`).
- **The other 42 files were deliberately not hashed.** Their status in `01_SOURCE_IDENTITIES.json` is `DOCUMENTARY_ONLY_NOT_REHASHED` (42 of 44; the other 2 are `PHYSICALLY_HASHED_THIS_PASS_AND_MATCHES`). **Size + mtime agreement is not byte identity.**
- **3.4 GB LiTS I05 checkpoint:** locally present at `…/precheck/current_i05_materialization_checkpoint_v3.json`, 3,404,445,161 B, own schema `FIABC_LITS_CURRENT_NEUTRAL_I05_MATERIALIZATION_CHECKPOINT@3.0.0`, documented document SHA-256 `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726` and identity `3fab15f37db629f0ee24189620c65eff944d8a36c4b4509abb6b8bb2ea69c33f`. **Metadata / byte-range reads of that object are not equivalent to a fresh full-object SHA-256 verification, and no such full re-hash was performed or is claimed.**
- **Closed35 grade letters** (20 PASS / 15 BLOCKED) are the historical representation census only — not DDM maturity, not file presence, and **never promotable to current readiness**.
- **Disk constraint:** report 00 recorded `/System/Volumes/Data` 466 GiB total, 433 GiB used, **12 GiB available (98 % capacity)**. A re-read at banking time shows **13 GiB available (98 %)**. The tree is ~34 G. This is a live constraint on any future large write and was the reason for Contents-API banking instead of a clone.

---

## 3. Leading *UNADOPTED* source set proposed

**`LiTS_I.dta`, `Afro Barometer Round 5.sav`, `Afro Barometer Round 9.sav`** (report 04 Rank 1; contract in report 05).

- **S1 / S2 (LiTS I):** retained, source-grounded product — **60 supported facts / 77 query roles / 50 candidates (49 supported + 1 `VALID_EMPTY`)**, rules `D02_P1×1, D02_P2×18, D02_P4×25, D02_P0×5, D02_P3×1`, covering joint-dependence, conditional reversal, minority-cell and greater-order structures; Astra parity receipt all sections PASS; `oracle_freeze_authorized: true`; `FF02_READY__NO_SOURCE_REOPEN_REQUIRED`. **Source-free serving binding and normative model-use are NOT thereby complete.**
- **S3 second distinct source family:** claimed via accepted narrow SRC02 GT2 plus additional GT34 archival C11 transport (Afro R5 release `R5_GT34_Q2_Q69B_Q86A_SAME_SOURCE_CANDIDATE_R1`, 19,210 respondents, 2 question bindings, 38,420 routing facts, court `6 passed / 55 warnings`). Its terminal explicitly records **`PASS__GT34_Q2_Q69B_Q86A_SAME_SOURCE_RELEASE_MATERIALIZED__NO_ADOPTION`**, obligation `OBL049: LAWFULLY_CLOSABLE_AT_HQ_FAN_IN`. **No general second structural-world admission and no N9 world consumer is thereby proved.**
- **Proposed R5↔R9 temporal pair:** **114** historical accepted within-family continuity edges, **51** at `QUESTION_AND_RESPONSE` grain. **These are family documentary question-lineage rulings. They are NOT adoption of any specific outcome, population, survey design/weights, native measurement scale, release identity, or an EE12/C7 temporal pair / model-use grant.**
- **Earlier official Ghana Q43/Q31 work is OPTIONAL** and is not necessarily the only admissible pair. **Do not substitute or infer a trend from it.**
- **Possession ≠ authority:** the three files are physically possessed on this Mac; operative authority to *use* them for S1/S2/S3 remains ungranted by this bank.
- **Report 05 open question `IQ-1` remains unresolved:** the accepted cross-source seed table records **0 rows / 0 shared propositions** for `Afrobarometer ↔ LiTS`. If HQ reads S3 as requiring a positive relational bridge, report 04 Bundle 2 (`LiTS_I`, `WVS7`, `WVS4` — 7 seed rows / 6 shared propositions) must be substituted. **This bank does not resolve IQ-1.**

---

## 4. Most important dissent / falsifiers

1. **Two-source `EE-P2X` produced no final measured PASS.** All six cells (`LITS_I/A,B,C`, `WVS7/A,B,C`) are `CANDIDATE_LOCAL_FAILURE` in the ledger, run stalled at 52/102 stages, `00_RETURN.md` status `BLOCKED__CANDIDATE_RUNTIME_AND_FINAL_VERIFIER`. This is kept **distinct** from the successful LiTS-I independent track; the LiTS-I track's success does not rescue EE-P2X.
2. **The R5 GT34 two-question respondent transport does not itself prove three-variable progressive conditioning.** It binds exactly two questions (`Q69B`, `Q86A`) on 19,210 respondents. Its `NO_ADOPTION` ceiling survives this bank unchanged.
3. **`LiTS_I` + Afrobarometer structural coexistence is only a *proposed* world composition.** Historical provisional shared seed mappings for that pair are **0/0**. That does not falsify source-indexed coexistence, and it does not establish a positive relational bridge.
4. **Candidate scores `114/51`, `92/66`, `23/2` are historical scope-specific continuity rulings only** — not design-based measured temporal truth, not pair-specific model-use grants, and not authority for any cross-survey artificial joint. No cross-survey artificial joint is proposed or implied.
5. **Supersession correction (stated here, not written into 00–06):** the original local research read an earlier `HQ249`-branch `HQ_HANDOFF/LATEST.json` and treated it as current. **The binding canonical current at issuance is HQ268 / `HQD-2026-10-09-268` @ `a12f619d8cc109f1245824a3ef220d3b5beb0d9a`.** Reports 00–06 therefore cite a **historical, non-authorizing HQ249 frame** (`PYAT_CONTROL_ROOM/WORKING_PAPERS/PREV3_MINIMUM_EMPIRICAL_SERVICE_DEMAND_HQ249_R1.md` @ `9f553f6b7e4d97f89bb149b3f6cfea5474f01621`, read from `agent/hq249-prev3-service-demand-working-paper-r1` @ `dfc81f9d0b2694041ca9991b7c35db5f8fc3a`). **The HQ249 handoff is historical and superseded by HQ268; it remains useful as documentary demand text but carries no current authority.** Primary reports were **not** rewritten to look current or positive — the correction lives only in this addendum.
6. **Scoped, not generic, questions.** Whether the missing historical EVS TREND `ZA7503` source, or the absent local `EE-R9L` commit (`WORKER_RETURNS/EE-R9L/01_PRODUCTION_CLOSURE_EVIDENCE.json` @ `c88d2a92521de1f2ef85e41279194d7d4f5434cb`, absent from all three local checkouts), matters to *this selected first bundle* is an open **scoped** question — not a generic blocker. The atlas manifest path/size mismatch (`…/manifests/crosswave_atlas_file_manifest.csv` pointing at a non-existent directory, 17 rows all `status=present`) and the LITS projection-owner ledger recovery observation (R1 blocker C1 overturned by the presence of `01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv` inside RUN3's `_be1_lits_projection` tree) are **hypotheses for an independent reproducibility court, not authorization**.
7. **Nothing is granted here.** No source execution, no arbitrary experimental permissions, no EE14 G0b model-use, no current/as-of T1, no T2 world, no AT07 trust root, no native F7 status, no V3 actor, no world/temporal permission, no `HQ_HANDOFF/LATEST.json` change, no dispatch of further workers, no self-adoption.

---

## 5. Next HQ action (not taken by this worker)

Examine 00–06 and this 07 **independently** against currently adopted authority and actual source meaning; select or reject the candidate bundle on true S1/S2/S3 suitability, structural-world meaning, and the actual selected service consumer; **only afterward** issue the minimal scoped source operation / temporal court. No self-adoption by the worker or by this bank.

## 6. Exact evidence paths cited in the reports

- Estate: `/Users/matthewsmith/Desktop/Rawlsing/data/Data/` (44 files); manifest `/Users/matthewsmith/Desktop/Rawlsing_and_RawlsingsExcess_tree_sha_size_date.txt`.
- LiTS I retained product: `/Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/court/oracle_producers/LITS_I/` (`current_i05_materialization_checkpoint_v3.json`, `current_standard_lits_oracle.json`, Astra parity receipt).
- Afro R5 retained release: `/Users/matthewsmith/Desktop/Rawlsing/FIABC-QF1-qualification-checkout/data/ddm_build_copy/recovery_integration/…/Q2_Q69B_Q86A_SAME_SOURCE_MATERIALIZATION_R1/` (`00_RETURN.md`, `transport/*.gz`).
- EE-P2X failure receipts: `/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/FIABC-P2X-DISPOSITIVE-R1-RUN3-20260924/` (`ee_p2x_stage_ledger.json`, `fiabc_driver_progress.jsonl`, `cells/{LITS_I,WVS7}/`); `/Users/matthewsmith/Desktop/Rawlsing/FIABC-QF1-qualification-checkout/WORKER_RETURNS/EE-P2X/00_RETURN.md`.
- Continuity-edge authorities (documentary): `Rawlsing_Authority_Document_Archive_2026-08-24/documents/handoff-recovery-and-state/{09,10,12,19,27}_P2_*_PASS1/CURRENT_STATE.json`; the five `v1` edge CSVs exist only inside `/Users/matthewsmith/Desktop/RawlsingsExcess.zip` under `RawlsingsExcess/Rawlsing_J_Family_Authority_Strategy_Handoff_v10_20260731/{09,10,12,15,19}_P2_*_PASS1/`.
- Atlas: `/Users/matthewsmith/Desktop/Rawlsing/rawlsing_authority_documents_pack_20260627T040000Z/outputs/crosswave_driver_atlas/atlas_data.json`.
- Authority frame used by 00–06 (historical): `PYAT_CONTROL_ROOM/WORKING_PAPERS/PREV3_MINIMUM_EMPIRICAL_SERVICE_DEMAND_HQ249_R1.md` @ `9f553f6b…`, branch `agent/hq249-prev3-service-demand-working-paper-r1` @ `dfc81f9d…`.
- Binding current authority: `HQ_HANDOFF/LATEST.json` on `integration/pre-main-reconciliation-r1`, `HQD-2026-10-09-268` @ `a12f619d8cc109f1245824a3ef220d3b5beb0d9a`.

No new authority label was fabricated; no historical report was rewritten to look positive.

---

**Class:** documentary banking return. **Adoption:** none. **Mutations permitted:** none outside `WORKER_RETURNS/PYAT-HQ268-E01-LOCAL-EMPIRICAL-ESTATE-AND-SOURCE-SELECTION-EVIDENCE-BANK-R1/` on the commissioned branch.

**TERMINAL:** `HQ268_E01_ESTATE_AND_SOURCE_SELECTION_BUNDLE_BANKED__UNADOPTED__FOR_INDEPENDENT_HQ_COURT`
