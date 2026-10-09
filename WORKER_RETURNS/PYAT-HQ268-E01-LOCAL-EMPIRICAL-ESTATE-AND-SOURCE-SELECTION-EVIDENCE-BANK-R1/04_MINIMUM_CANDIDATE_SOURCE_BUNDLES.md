# 04 — MINIMUM CANDIDATE SOURCE BUNDLES

**Mode:** documentary / retained-product archaeology only. No raw `.sav`/`.dta` was opened, no statistic was computed, no survey permission, comparability authority, execution warrant or adoption is created here. Bundles are **proposals for HQ selection**, not selections.

**Governing demand:** `PYAT_CONTROL_ROOM/WORKING_PAPERS/PREV3_MINIMUM_EMPIRICAL_SERVICE_DEMAND_HQ249_R1.md` @ `9f553f6b7e4d97f89bb149b3f6cfea5474f01621` (frozen demand commit), read from branch `agent/hq249-prev3-service-demand-working-paper-r1` @ `dfc81f9d0b2694041ca9991b7c35db5f8fc3a`.

**Authority ceilings in force (from `HQ_HANDOFF/LATEST.json`):** `last_hq_decision HQD-2026-10-08-247`, `hq248_decision HQD-2026-10-08-248`, `hq249_decision HQD-2026-10-08-249`, `hq249_active_branches []`, `measured_execution_authorized_via_warrant false`, `raw_live_warrant_c7_actor_holds true`, `c4_adopted false`, `hq182_hold_lifted false`, `source_hold_unchanged true`, `hq249_astra_audit HQ249_GATE_OPEN__P0_SOL_HIGH__P1_ASTRA_AFTER_BANK__P2_SOL_HIGH__P3_ASTRA`.

---

## 0. What "minimum" is allowed to mean

HQ249 §4 is explicit:

> "If two distinct survey families and two comparable waves of one are required for the chosen demonstration, three source-wave identities are only a **conditional logical lower bound**, not a universal three-anchor doctrine or evidence those files are competent."

So the arithmetic floor for the demanded S3 is:

- **≥2 distinct source families** with admissible structural/field products (S3 structural), and
- **≥2 waves of one family** for a same-survey comparable-wave product (S3 temporal), and
- at least one source-wave carrying a retained respondent-backed product for S1/S2.

That floor is reachable in **exactly two shapes**:

| Shape | Composition | Count |
|---|---|---|
| **I — split** | 1 wave of family X (S1/S2 + structural 1) + 2 waves of family Y (structural 2 + temporal) | 3 waves, 2 families |
| **II — merged** | 2 waves of family X (S1/S2 + structural 1 + temporal) + 1 wave of family Y (structural 2) | 3 waves, 2 families |

Both shapes cost three source-wave identities. Every candidate bundle below is one of these two shapes. Two-wave bundles cannot satisfy S3 and are excluded.

---

## 1. Evidence base used for selection

Four inventories, all read-only. Nothing below is newly measured.

### 1.1 Retained respondent-backed products, by family

| Family | Retained product | Terminal / status | S1/S2 readiness |
|---|---|---|---|
| **LiTS I** | `current_i05_materialization_checkpoint_v3.json` (3,404,445,161 B) + `current_standard_lits_oracle.json` (264,917 B) + frozen court oracle `LITS_I.standard.json` + 2,121-member `PRE553_R5_LONG_SHARDED_CARRIER@2.0.0` (canonical_row_count 34,745,595) | `PASS__FINAL_LITS_RETRY_BANKED_COMPLETE_CANONICAL_EMPIRICAL_CLOSURE__…__FF02_READY__NO_CANDIDATES_RUN`; `FF02_READY__NO_SOURCE_REOPEN_REQUIRED`; Astra substantive parity all 12 sections PASS; `oracle_freeze_authorized: true` | **Complete.** 77/77 query roles bound, 60/60 empirical facts `SUPPORTED`, 50 candidates (49 `DISCOVERED_RESULT_SUPPORTED`, 1 `VALID_EMPTY`), rules `D02_P1_JOINT_DEPENDENCE` ×1, `D02_P2_HIGHER_ORDER_K3` ×18, `D02_P4_MINORITY_NONMODAL_COMPLETE_JOINT_CELLS` ×25, `D02_P0_REAL_POSITIVE_CONTROL` ×5, `D02_P3_CONDITIONAL_REVERSAL` ×1 |
| **Afrobarometer R5** | `Q2_Q69B_Q86A_SAME_SOURCE_MATERIALIZATION_R1/` → `transport/q69b_q86a_same_source_transport.json.gz` (933,040 B), `q86ab_ffp017_source_state_pairs.bin.gz` (12,508 B), `q86a_ffp017_risk_values.json.gz` (46,939 B) | `PASS__GT34_Q2_Q69B_Q86A_SAME_SOURCE_RELEASE_MATERIALIZED__NO_ADOPTION`; `OBL049: LAWFULLY_CLOSABLE_AT_HQ_FAN_IN`; court 6 passed / 55 warnings | **Partial but real.** 19,210 respondents, **2 question bindings** (Q69B+Q86A), 38,420 events + 38,420 routing facts. Predecessor releases `R5_GT12_Q86A_Q86B_FROZEN` and `R5_GT34_N2_Q69B_BOUNDED_CANDIDATE_R1` accepted and unmutated → three accepted R5 questions exist in total (Q69B, Q86A, Q86B), but only two co-reside in one release. **Not adopted into PRE-MAIN.** |
| **WVS7** | `WVS7.standard.json` (200,097 B, `RAWLSING_FIABC_CANDIDATE_NEUTRAL_PARITY_ORACLE@1.0.0`, `state: FROZEN_READ_ONLY`) + `wvs7_standard_oracle_acceptance.json` (`status: PASS`, `source_free_standardizer_status: PASS`, `standard_oracle_verifier: PASS`) + `wvs7_projection_structural_input.json` (4,658,099 B, 97,220 rows × 613 vars) + `FIABC_LM2_R1E_FROZEN_Q291_PHYSICAL_CELL_CARRIER.json` (83,340,882 B, 97,220 rows × 194,440 cells) + R1J SAV representation authority `PASS` + successor Lock2 `5e2a53f0…` | Oracle frozen; **learned product not produced** — `candidate_outputs_seen: 0`; all six EE-P2X cells ended `CANDIDATE_LOCAL_FAILURE` | **Expectation frozen, product absent.** Frozen expectation carries `candidate_count 46`, `query_role_count 58`, `typed_terminal_counts {COVERAGE_LIMITED: 46}`. EE-P2X blockers: no callable WVS `GovernedC11Projection`, no R5 compact carrier binding, `RecursionError` at S01 |
| **Afrobarometer R9** | none | — | raw file only |
| **WVS Wave 4** | none | — | raw file only |
| **LiTS II** | none | — | raw file only |
| **EVS (1981/1990/1999/2008/2017)** | **none** | — | raw files only; HQ249 D3 records D01/D02 decoder-lane residuals |
| **EVS trend ZA7503** | **absent from disk** | — | `survey_microdata_reload_manifest_EVS_TREND.json` declares `data/Data/EVS 1981-2017 TREND ZA7503_v3-0-0.dta`, 224,434 × 635, 142,515,579 responses — **no such file exists locally** (0 matches) |
| **GSS, Arab Barometer, Asian Barometer, Latinobarómetro, South Asia** | none located | — | raw files only |

Sources: R1 reports `02`/`03`; `LOCAL_COURTS/FIABC-P2X-DISPOSITIVE-R1-RUN3-20260924/`; `FIABC-QF1-qualification-checkout/WORKER_RETURNS/{EE-P2X,FIABC-LM2,FIABC-LM2-R1G-LOCAL-Q291,FIABC-LM2-R1J-SAV-REPRESENTATION-AUTHORITY,FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE}`; the GT34 Q2 return under `data/ddm_build_copy/recovery_integration/…/Q2_Q69B_Q86A_SAME_SOURCE_MATERIALIZATION_R1/` (9 copies, **none in the main `data/ddm_build_copy`**).

### 1.2 Accepted within-source longitudinal continuity edges (S3 temporal authority)

Authority status is `ACCEPTED_SOURCE_LOCAL_CONTINUITY` / `ACCEPTED_WITHIN_SOURCE_CONTINUITY` in every file read.

| Family | File | Total | Best same-survey pair | Edges for that pair | Of which response-comparable |
|---|---|---|---|---|---|
| **Afrobarometer** | `…_Afrobarometer_Accepted_Longitudinal_Continuity_Edges_v1.csv` (46,257 B) | 119 | **R5 ↔ R9** | **114** | **51** `QUESTION_AND_RESPONSE` (`response_signature_equal=True`), 63 `QUESTION_PROPOSITION_ONLY` |
| **WVS** | `…_WVS_Accepted_Longitudinal_Continuity_Edges_v1.csv` (81,057 B) | 180 | **W4 ↔ W7** | **92** | **66** `PORTABLE_EXACT_AT_QUESTION_AND_RESPONSE_GRAIN`, 15 scale-bridge, 8 named-construct, 4 other |
| **EVS** | `…_EVS_Accepted_Longitudinal_Continuity_Edges_v1.csv` (390,730 B) | 815 | 1990↔1999 (226) / 1999↔2008 (221) | 1990 ↔ **2008 = only 5** | — |
| **GSS** | `…_GSS_…v1.csv` (1,454,712 B) | 3,171 accepted adjacent (per `09_P2_GSS_PASS1/CURRENT_STATE.json`) | 8 waves | 3,171 | baseline closed at exact-name + negative-alias grain |
| **LiTS** | `…_LiTS_Accepted_Longitudinal_Continuity_Edges_v2.csv` (59,967 B) | 133 | III↔IV 82, II↔III 24, **2006↔II = 23** | 23 | **2** `QUESTION_AND_RESPONSE` (`q303_12→q303n`, `q704_1→q715_1`) |
| **Asian Barometer** | `…_v2.csv` (113,906 B) | 236 | W4↔W5 200 | 200 | 11 total `QUESTION_AND_RESPONSE` |
| **Latinobarómetro** | `…_v2.csv` (13,477 B) | 26 | 1995↔2011 / 1995↔2024 | 12 / 10 | — |
| **South Asia** | `…_v2.csv` (5,998 B) | 12 | W1↔W2 | 12 | — |
| **Arab Barometer** | `…_v1.csv` (40,861 B) | not read | — | — | — |

**Location defect:** the five `v1` continuity-edge files (Afrobarometer, WVS, EVS, GSS, Arab) are **not present anywhere under `/Users/matthewsmith/Desktop/Rawlsing`** (full `find` returned 0). They exist only inside `/Users/matthewsmith/Desktop/RawlsingsExcess.zip`, at `RawlsingsExcess/Rawlsing_J_Family_Authority_Strategy_Handoff_v10_20260731/{10,12,15,19,09}_P2_*_PASS1/`. The 2026-08-23 combined tree manifest still records them as live tree files → they were removed from the Rawlsing tree after 2026-08-23. For this report they were **extracted to `/tmp/…/_p2/` and read from there**; no repo file was created or changed.

### 1.3 Cross-source seed pairs (F6, all `PROVISIONAL_NON_AUTHORITY`)

From `29_P2_ALL_NINE_CROSS_SOURCE_SEED_REFRESH/Rawlsing_P2_All_Nine_Source_Pairwise_Seed_Summary_v1.csv` (36 rows, every one `PROVISIONAL_NON_AUTHORITY`):

| Pair | Seed rows | Shared propositions |
|---|---|---|
| EVS ↔ WVS | 95 | 24 |
| Asian Barometer ↔ South Asia | 28 | 5 |
| **LiTS ↔ WVS** | **7** | **6** |
| Asian Barometer ↔ WVS | 6 | 2 |
| EVS ↔ Latinobarómetro | 5 | 2 |
| Afrobarometer ↔ Asian Barometer | 4 | 2 |
| Arab Barometer ↔ Asian Barometer | 4 | 3 |
| Afrobarometer ↔ Arab Barometer | 2 | 1 |
| EVS ↔ LiTS | 2 | 2 |
| Asian Barometer ↔ Latinobarómetro | 2 | 2 |
| GSS ↔ WVS | 6 | 1 |
| **Afrobarometer ↔ LiTS** | **0** | **0** |
| **Afrobarometer ↔ WVS** | **0** | **0** |
| **Afrobarometer ↔ EVS** | **0** | **0** |
| all other zero rows | 0 | 0 |

Companion: `22_P2_AFRO_EVS_CROSS_SOURCE_REFRESH/CURRENT_STATE.json` = rows 6, shared_propositions 1, `PROVISIONAL_NON_AUTHORITY`.

### 1.4 Cross-wave atlas (measured-movement support, secondary)

`rawlsing_authority_documents_pack_20260627T040000Z/outputs/crosswave_driver_atlas/atlas_data.json` (17,775,035 B):

- Within-family shared **mapped** content ids: **Afrobarometer R5↔R9 = 16** (R1↔R5 12, R1↔R9 11); Asian Barometer W1↔W6 15; Arab Barometer W1↔W8 9; Latinobarómetro 1995↔2011 12; **WVS W4↔W7 = 4** (`AGENCY_CONTROL`, `CIVIC_INTEREST_POLITICS`, `HAPPINESS`, `LIFE_SATISFACTION`).
- **Mapping-layer sparsity caveat:** the atlas maps only a fraction of each wave's variables (Afro R5 35/348, WVS W7 73/613, Afro R1 22/143) and **zero rows for EVS, GSS and all four LiTS waves**. Therefore an atlas count of `0` for EVS/GSS/LiTS is an artifact of the mapping layer, **not evidence of non-comparability**. The same caveat applies to the 0-row cross-source seeds for those families.

### 1.5 Physical presence and identity (from `01_SOURCE_IDENTITIES.json`)

| File | Bytes | Recorded SHA-256 | Identity status |
|---|---|---|---|
| `LiTS_I.dta` | 139,531,180 | `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09` | **PHYSICALLY_HASHED_THIS_PASS_AND_MATCHES** |
| `Afro Barometer Round 5.sav` | 49,689,458 | `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651` | documentary; **size matches the SHA recorded inside the GT34 Q2 release** |
| `Afro Barometer Round 9.sav` | 70,621,348 | `3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8` | documentary |
| `WVS Wave 7.sav` | 185,163,494 | `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d` | documentary; size matches WVS7 receipts |
| `WVS Wave 4.sav` | 41,997,221 | `c6757ed187655c8b9af88ae4c23c00f066696a641af2f316b4343272ea1d4a0a` | documentary |
| `LiTS_II.dta` | 199,716,969 | `c43d0e1821c51398817d7dfdfad2c0a4a5bb0d492f6a58096670e623bb6130e9` | documentary |

All six are physically present under `data/Data/` (44 files total, 35 CLOSED35 + 9 Asian Barometer country files).

---

## 2. Selection criteria derived from S1/S2/S3

| # | Criterion (from HQ249 §2) | Consequence for bundle choice |
|---|---|---|
| C1 | S1 needs an **admitted, reproducible `q(Y|A)` then `q(Y|A,B)`** with different query/predicate/witness IDs and demonstrably jointly supported cells, plus position↔attitude reversibility at the supported grain | Needs a family with a **produced** multi-role retained product, not merely a frozen expectation. Only LiTS I qualifies today (77 roles, `D02_P3_CONDITIONAL_REVERSAL` supported) |
| C2 | S2 needs source-native **same-respondent co-signature / attitude-cloud and ordered joint configuration** with risk set, routing, denominator, uncertainty, minority support, recursive ancestry | Same requirement; LiTS I's 60 facts + 50-candidate frontier carry it. Afro R5's Q2 release carries a 2-question joint only |
| C3 | S3 structural needs **two independently admissible source-family structural/field products**, each with its own universe/respondents, scope, operation and evidence identities, entering **one** declared objective-world view as **distinct** contributions | Two families, both with materialized (or at minimum released) products. Pooling and synthetic shared respondents are forbidden |
| C4 | S3 temporal needs **one same-survey comparable-wave pair** with exact positive pair-specific authority and authentic measured movement/no-change/typed noncomparability | Needs **already accepted continuity edges** for the chosen wave pair — the pair-specific authority cannot be invented later |
| C5 | "Temporal labels and subtracted marginals alone do not confer comparability" | File-year pairing is worthless; accepted edges are the only admissible basis |
| C6 | "The minimum's actual competent source set is NOT selected here" + E3: "select based on **evidence cost not physical PASS status**" | Rank by how much *new* adjudication/execution each bundle forces |
| C7 | No self-authorization; `measured_execution_authorized_via_warrant false`, `source_hold_unchanged true` | Every bundle is contingent on separate HQ warrants regardless of ranking |

---

## 3. Scoring

Scale: **strong / adequate / weak / absent**. "Evidence cost" = new work forced beyond what is already retained.

| Criterion | Bundle 1 `{LiTS_I, Afro_R5, Afro_R9}` | Bundle 2 `{LiTS_I, WVS7, WVS4}` | Bundle 3 `{Afro_R5, EVS_1990, EVS_2008}` |
|---|---|---|---|
| Shape | II (LiTS split: S1/S2 + structural 1; Afro split: structural 2 + temporal) | II (LiTS S1/S2 + structural 1; WVS structural 2 + temporal) | I (Afro S1/S2 + structural 1; EVS structural 2 + temporal) |
| **S1 conditioning** | **strong** — LiTS I 77 roles, conditional reversal supported | **strong** — same LiTS I product | **weak** — Afro R5 has 2 questions in one release (needs a third binding for `A,B,Y`); no conditioning rule evidence |
| **S2 rich joint** | **strong** — LiTS I 60 facts / 50 candidates / K3 + minority-cell rules / recursive references | **strong** — same | **weak** — 2-question joint only, no I03/I05 |
| **S3 structural family 1** | **strong** — LiTS I produced product, Astra parity PASS | **strong** — same | **adequate** — SRC02 GT2/GT34 accepted at one local `CONTEXT` grain (HQ249 D3) |
| **S3 structural family 2** | **adequate** — Afro R5 GT34 release materialized + court PASS, **adoption pending HQ (OBL049)** | **weak→adequate** — WVS7 frozen oracle, projection input, Q291 carrier, R1J authority all PASS, but **learned product absent** (`candidate_outputs_seen: 0`, six cells `CANDIDATE_LOCAL_FAILURE`) | **absent** — EVS has zero retained product |
| **S3 temporal pair authority** | **strong** — R5↔R9 **114 accepted edges, 51 response-comparable** | **strong** — W4↔W7 **92 accepted edges, 66 exact Q&R** | **absent/weak** — 1990↔2008 has **only 5** accepted edges; the competent EVS pairs are 1990↔1999 (226) and 1999↔2008 (221) |
| **Temporal measured-movement support** | **adequate** — atlas R5↔R9 = 16 shared mapped content ids (of 35 mapped in R5) | **weak** — atlas W4↔W7 = 4 shared mapped content ids | **absent** — EVS has 2 mapped content ids in total |
| **Cross-family documented overlap** | **absent** — Afrobarometer↔LiTS = 0/0 seed rows (but zero overlap also makes silent pooling impossible to mistake for support) | **adequate** — LiTS↔WVS = 7 rows / 6 shared propositions | **absent** — Afrobarometer↔EVS = 0/0 |
| **Pipeline already exercised on the second/third wave** | **strong** — GT34/GT12 per-question release path proven and court-passed on R5; applying it to R9 reuses the same machinery | **weak** — W4 has zero retained artifacts and no SAV representation authority of its own (R1J covers WVS7 only) | **absent** — no EVS pipeline |
| **Known blocking defects touching the bundle** | OBL049 adoption (HQ-owned, governance only) | EE-P2X: missing `rawlsing_next.pre553_runtime_authority` **on the driver path** + no callable WVS `GovernedC11Projection` + `RecursionError` at S01 | D01/D02 decoder-lane residuals; ZA7503 trend file absent |
| **Evidence cost rank** | **1 (lowest)** | **2** | **3 (highest)** |

---

## 4. Bundle 1 — RANK 1

### `{LiTS_I.dta, Afro Barometer Round 5.sav, Afro Barometer Round 9.sav}`

**Shape II.** Two families (LiTS, Afrobarometer), three source-wave identities.

| Role in the demand | Source-wave | Basis |
|---|---|---|
| S1 + S2 (conditioning, rich joint) | **LiTS I** | 3.4 GB retained I05 checkpoint: 77 query roles, 60 supported facts, joint-dependence / higher-order-K3 / minority-cell / conditional-reversal rules all `EVALUATED_SUPPORTED`; FF02_READY; zero-source resume PASS; Astra parity PASS; source SHA physically re-proven |
| S3 structural `S_1` | **LiTS I** | same product, distinct LiTS universe (29,002 respondents × 1,198 variables) with its own evidence identities |
| S3 structural `S_2` | **Afrobarometer R5** | `R5_GT34_Q2_Q69B_Q86A_SAME_SOURCE_CANDIDATE_R1`: 19,210 respondents, own empirical-universe SHA `4dc56730…`, own release/replay/manifest identities, court PASS, **distinct** Afrobarometer universe (51,587 source rows) |
| S3 temporal `W_t ↔ W_{t+1}` | **Afrobarometer R5 ↔ R9** | **114 accepted continuity edges**, of which **51** are `QUESTION_AND_RESPONSE` with `response_signature_equal=True` (e.g. `DemandDemo→DemandDemo`, `EA_SEC_B→EA_SEC_B`, `Q107A→Q106A` … `Q107E→Q106E`, `Q108→Q107`, `Q110A→Q109A` …) |

**Why it ranks first**

1. **Both structural contributions are already materialized.** No family in the bundle has a "frozen expectation but no product" gap. LiTS I is produced; Afro R5 is produced, court-passed, and blocked only by an adoption decision that HQ owns (`OBL049: LAWFULLY_CLOSABLE_AT_HQ_FAN_IN`).
2. **The temporal pair has the deepest accepted pair-specific authority of any pair whose second wave already has a proven release pipeline.** 114 edges / 51 response-comparable beats WVS's 92/66 in raw count and beats LiTS 2006↔II's 23/2 by a factor of five.
3. **The materialization path for the temporal product already exists and has been executed.** The GT34/GT12 per-question release machinery was run, court-tested (6 passed) and frozen for R5. Extending it to R9 is reuse, not invention.
4. **Evidence cost is governance, not science.** The only non-execution prerequisite unique to this bundle is HQ adoption of OBL049 plus warrants — exactly the class of decision the authority ceilings reserve to HQ.
5. **Zero cross-family overlap is defensible here.** HQ249 §2 S3 requires *distinct* contributions and forbids pooling; hostile test #7 fails on *silent pooling*, not on missing overlap. A bundle with 0 shared seed rows cannot be accused of smuggling a pooled respondent table.

**Known weaknesses (stated, not hidden)**

- **W1 — retained constructs do not continue to R9 at response grain.** Of the three accepted R5 questions, only two touch the continuity table: `R5 Q69B → R9 Q41E` (`QUESTION_PROPOSITION_ONLY`, `response_signature_equal=False`) and `R5 Q88A → R9 Q86B` (Q&R, but Q88A is not one of the retained questions). So the *currently released* R5 constructs are **not** the response-comparable set. The temporal product must therefore be built from the 51 Q&R-continuous pairs (e.g. `Q107A↔Q106A`), which are **not yet released for either wave**. This is new per-question release work on two waves using a proven pipeline.
- **W2 — no documented cross-family proposition overlap** between LiTS and Afrobarometer (0 seed rows / 0 shared propositions, `PROVISIONAL_NON_AUTHORITY`). Interpretation risk: if HQ reads "entering the same declared objective-world view" as requiring a *relational* bridge rather than mere distinct coexistence, this bundle would need an added third family or a new F6 refresh. Flagged as **open interpretive question IQ-1** for HQ in report 06.
- **W3 — the Afro R5 S1/S2 surface is thin.** Two question bindings in one release; the demand's illustrative `A,B,Y` needs three roles. Bundle 1 therefore does **not** rely on Afro R5 for S1/S2 — but a reviewer who insists the conditioning run and the structural `S_2` share a source would find this arrangement unsatisfying.
- **W4 — documentary identity only** for all three files except `LiTS_I.dta`. A fresh hash pass on R5/R9 is required before any warrant-backed execution.

---

## 5. Bundle 2 — RANK 2

### `{LiTS_I.dta, WVS Wave 7.sav, WVS Wave 4.sav}`

**Shape II.** Two families (LiTS, WVS), three source-wave identities.

| Role | Source-wave | Basis |
|---|---|---|
| S1 + S2 + `S_1` | **LiTS I** | as Bundle 1 |
| S3 structural `S_2` | **WVS7** | frozen parity oracle `e546c155…` (`FROZEN_READ_ONLY`, 46 candidates / 58 query roles expected), `wvs7_projection_structural_input` (97,220 × 613, identity `151907b3…`), Q291 physical carrier (83,340,882 B, `1aea888d…`), R1J SAV representation authority `PASS`, successor Lock2 `5e2a53f0…`, discovery authority `3aee3601…` |
| S3 temporal | **WVS W4 ↔ W7** | **92 accepted edges, 66 `PORTABLE_EXACT_AT_QUESTION_AND_RESPONSE_GRAIN`** with stable variable pairs (`V4↔Q1`, `V5↔Q2`, `V6↔Q3`, `V7↔Q4`, `V8↔Q5`, `V17↔Q10`, `V70↔Q24`, `V82↔Q48`, `I_ABORTLIB↔I_ABORTLIB`, `VOICE↔VOICE`, …) |

**Why it ranks second**

1. **The demand's own worked example lives here.** HQ249 §1/§2 uses `A,B,Y` illustratively, and the estate's only frozen Q291 carrier is `Q291G5`/`Q291P5` — the exact variables bound in Lock2 and R1J. Choosing WVS keeps the demonstration variables and the retained carrier in the same family.
2. **Cross-family bridge exists.** LiTS↔WVS is the **only** pair with both (a) a retained product on each side and (b) nonzero accepted cross-source seeds (7 rows / 6 shared propositions).
3. **66 exact Q&R temporal edges** is the highest response-comparable count of any pair in the estate (Afro R5↔R9 has 51).

**Why it ranks below Bundle 1**

1. **The second structural contribution is not actually produced.** `wvs7_standard_oracle_acceptance.json` records `candidate_outputs_seen: 0`; all six EE-P2X cells (`LITS_I/A,B,C`, `WVS7/A,B,C`) terminate `CANDIDATE_LOCAL_FAILURE` under `ee_p2x_stage_ledger.json` (branch `agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`, head `a954e2d6…`, manifest `RAWLSING_FIABC_CURRENT_SIX_CELL_EXECUTION_MANIFEST@1.0.0`, `9acc2f38…`), driver stalled at 52/102 stages. `00_RETURN.md` states flatly: *"No final two-source measured PASS was claimed."*
2. **Three proved execution gaps sit on this bundle's path:** `LITS_I/A` `ModuleNotFoundError: rawlsing_next.pre553_runtime_authority` (module **is** present in 10+ local checkouts — a driver-path defect, see 06); `WVS7/A,B` `RecursionError` at S01 with *"No accepted WVS7 R5 compact carrier, R5LongShardedReader binding, or callable preparation binding exists; building one from the SAV would create forbidden carrier/projection work"*; `WVS7/B` *"no callable WVS GovernedC11Projection … Deriving one would add prohibited semantic/projection imp[lementation]"*.
3. **W4 is colder than R9.** W4 has zero retained artifacts and no SAV representation authority of its own (R1J is scoped to source SHA `2bd2a20f…` = WVS7). Afro R9 at least sits on a release pipeline already exercised 114-edge-neighbours away.

---

## 6. Bundle 3 — RANK 3 (the HQ249 D3 hypothesis) — NOT RECOMMENDED

### `{Afro Barometer Round 5.sav, EVS 1990.sav, EVS 2008.sav}` (SRC02 + SRC12 + SRC14)

HQ249 D3 disposition: `SRC02_GT2_ACCEPTED_REAL_ANCHOR__NO_COMPLETE_COMPETENT_T2_SET__EVS_PAIR_DOCUMENTARY_ONLY`, with E3 later recommending a *comparison* rather than adoption.

| Role | Assessment |
|---|---|
| S1 + S2 | **weak.** Afro R5 carries 2 question bindings and a 2-way joint; no conditioning-rule evidence, no I03/I05 |
| S3 structural `S_1` | **adequate** — SRC02 GT2 accepted at one local `CONTEXT` grain only (HQ249 D3) |
| S3 structural `S_2` | **absent.** EVS has **zero** retained products in the estate; D01/D02 decoder-lane residuals remain |
| S3 temporal `1990 ↔ 2008` | **absent/weak.** Only **5** accepted continuity edges for that exact pair (vs 226 for 1990↔1999 and 221 for 1999↔2008). D3 itself says the pair is *"physical candidates, not yet an authorized comparable pair"* |
| Cross-family bridge | **absent** — Afrobarometer↔EVS = 0 seed rows / 0 shared propositions |
| Additional defect | The E2 commission names `ZA7503↔SRC12/SRC14`; `ZA7503` is the EVS 1981–2017 trend file, declared in `survey_microdata_reload_manifest_EVS_TREND.json` at `data/Data/EVS 1981-2017 TREND ZA7503_v3-0-0.dta` (224,434 × 635) but **physically absent from disk** |

**Verdict:** this bundle is the only one of the three in which *two* of the three legs have no retained product at all. It is retained here for the record because it is the hypothesis HQ249 D3 actually named — not because it survives the evidence-cost test in E3.

---

## 7. Variants considered and rejected

| Variant | Why rejected |
|---|---|
| `{LiTS_I, LiTS_II, WVS7}` (LiTS as the temporal family) | LiTS 2006↔II has only **23** accepted continuity edges, of which only **2** are `QUESTION_AND_RESPONSE` (`q303_12→q303n`, `q704_1→q715_1`). Thinnest temporal authority of any same-survey pair with a retained first wave. LiTS II also has zero retained artifacts |
| `{Afro_R5, Afro_R9, WVS7}` (Afro temporal + WVS structural) | Drops the only complete retained S1/S2 product (LiTS I) → S1 becomes Afro R5's 2-question surface, which cannot host three conditioning roles |
| `{Afro_R5, Afro_R9, LiTS_II}` | Same as Bundle 1 but with a cold second wave (LiTS II, no retained artifacts, no exercised release pipeline) instead of the retained LiTS I — strictly dominated |
| Any 2-wave bundle | Cannot satisfy S3 (two families + two waves of one) simultaneously |
| Any bundle using GSS as temporal family | GSS has 3,171 accepted adjacent edges (the largest authority in the estate) but **zero** retained products, zero atlas mapping rows, and its continuity file exists only inside `RawlsingsExcess.zip` |
| Any bundle using EVS as temporal family at 1990↔2008 | 5 accepted edges; the competent EVS pairs are adjacent waves, and no EVS wave has a retained product |
| `{LiTS_I, WVS7, WVS4}` promoted to rank 1 | Considered. Rejected because the S3 structural `S_2` leg would be a frozen *expectation* (46 candidates / 58 roles expected, 0 produced) rather than a produced product, and three execution gaps are already proved against that path |

---

## 8. What these bundles do **not** establish

- They do not authorize execution. `measured_execution_authorized_via_warrant` remains `false`; `source_hold_unchanged` remains `true`; `c4_adopted` remains `false`.
- They do not confer comparability, pooling, portability, comparator, PSEPF, metabolism, CAN-008, V2 or V3 authority — no bundle creates or widens any of them.
- They do not convert a frozen oracle, a continuity-edge file, a cross-source seed row or an atlas mapping into a produced empirical product.
- They do not assert that any wave pair moves. A genuinely produced `no-change` or typed noncomparability is a permitted outcome under HQ249 §2 S3 and hostile test #8.
- They do not treat the CLOSED35 grades in `closed35.json` as current readiness; those remain the historical representation census only.
- `A`, `B`, `Y`, `q(A)`, `q(A,B)` stay illustrative symbolic roles; HQ must name the actual operation, columns and consumer.

---

**TERMINAL:** `MINIMUM_EMPIRICAL_INPUT_SET_PROPOSED__NO_SELF_AUTHORIZATION`
