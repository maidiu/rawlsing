# 05 — RECOMMENDED EMPIRICAL SOURCE CONTRACT (PROPOSED)

**Status:** `PROPOSAL_ONLY__FOR_HQ_SELECTION__NO_AUTHORIZATION_ISSUED`
**Selects from:** `04_MINIMUM_CANDIDATE_SOURCE_BUNDLES.md` (Rank 1 bundle)
**Governing demand:** `PREV3_MINIMUM_EMPIRICAL_SERVICE_DEMAND_HQ249_R1.md` @ frozen commit `9f553f6b7e4d97f89bb149b3f6cfea5474f01621`
**Not amended:** HQD125 §2–10, §12 F1–F8 + companion crosswalk; HQD216 §§1–6; HQ249 holds; PRE-V3→V3 actor firewall.

---

## 1. The recommended minimum, in one line

**Three source-wave identities from two survey families:**

`LiTS_I.dta` · `Afro Barometer Round 5.sav` · `Afro Barometer Round 9.sav`

serving **S1 + S2 from LiTS I**, **S3 structural `S_1` from LiTS I**, **S3 structural `S_2` from Afrobarometer R5**, and **S3 temporal from Afrobarometer R5 ↔ R9**.

Three is the conditional logical lower bound named in HQ249 §4. No fourth wave is proposed; no wave is included that does not carry a named obligation.

---

## 2. Exact input identities (physical, under `data/Data/`)

| # | File | Bytes | SHA-256 (as recorded) | Identity status | Rows × variables |
|---|---|---|---|---|---|
| 1 | `LiTS_I.dta` | 139,531,180 | `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09` | **PHYSICALLY RE-HASHED THIS PASS, MATCHES** (R1) | 29,002 × 1,198 (as recorded in the retained checkpoint) |
| 2 | `Afro Barometer Round 5.sav` | 49,689,458 | `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651` | documentary; **byte size equals the size recorded inside the GT34 Q2 release**, and that release records the same SHA | 51,587 (as recorded in `00_RETURN.md` of the GT34 Q2 return) |
| 3 | `Afro Barometer Round 9.sav` | 70,621,348 | `3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8` | documentary only (2026-08-23 tree manifest; size matches) | not asserted here |

**Precondition P-1:** identities 2 and 3 must be **freshly hashed under warrant** before any execution. Only identity 1 has been independently re-proven.

---

## 3. Contract by demanded output family

### S1 — Progressively conditioned possibility (F1/F2/F3/F8)

| Item | Contract |
|---|---|
| **Source-wave** | `LiTS_I.dta` — **only** |
| **Retained measured product** | `LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json` — 3,404,445,161 B; document SHA-256 `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726` (three agreeing records, **not re-hashed**); checkpoint identity `3fab15f37db629f0ee24189620c65eff944d8a36c4b4509abb6b8bb2ea69c33f` |
| **Why this product satisfies the `q(Y|A)` → `q(Y|A,B)` witness** | It already contains **77/77 bound query roles** with distinct `EmpiricalPredicate@1.0.0` (×35) and `EmpiricalQuerySpec@1.0.0` (×63) objects — i.e. the different query/predicate/witness IDs the demand requires — and its rule set includes **`D02_P3_CONDITIONAL_REVERSAL` (1 candidate, `EVALUATED_SUPPORTED`)**, **`D02_P1_JOINT_DEPENDENCE` (1, `JOINT_NOT_PRODUCT_OF_MARGINALS`)**, **`D02_P2_HIGHER_ORDER_K3` (18)** and **`D02_P4_MINORITY_NONMODAL_COMPLETE_JOINT_CELLS` (25, `TARGET_CELL_SUPPORTED`)** |
| **Ordering of `A` and `B`** | **HQ must name them.** They remain illustrative symbolic roles; nothing in this proposal designates columns or measurements |
| **Consumer** | The actual selected EE14/PRE-V3 possibility consumer with its currentness/replay contract — **not yet named** (D1 disposition `PARTIAL_SERVICE_IMPLEMENTATION_CONFIRMED__WORLD_CONSUMER_OPERATION_UNBOUND`) |
| **Reversibility obligation** | Position→attitude and, at the exact supported grain, attitude→position or attitude→attitude — must be drawn from the 77-role set, not constructed |
| **Null handling** | The existing `VALID_EMPTY` candidate (1 of 50) must be preserved as a source-grounded result; it may **not** be re-labelled from a missing authority |
| **Explicit non-reliance** | Afrobarometer R5 is **not** used for S1. Its release carries 2 question bindings, which cannot host three conditioning roles |

### S2 — Empirical co-travel, rich joint, selective conservation (F3/F4)

| Item | Contract |
|---|---|
| **Source-wave** | `LiTS_I.dta` — **only** |
| **Retained measured product** | Same checkpoint. Supporting objects: `canonical_empirical_object_closure` → `EmpiricalFact@1.0.0` ×60, `DiscoveryResultReceipt@1.0.0` ×50, `AuthoritySnapshot@1.0.0` ×24, `DiscoveryAuthority@1.0.0` ×1, `EmpiricalUniverse@1.0.0` ×1; canonical closure identity `f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415` |
| **C11 logical release** | `LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669`, content hash `192926fa…436df43f` |
| **Contracts in force** | `PRE553_CARRIER_NEUTRAL_C11_I03_I05_EXECUTION_BINDING@1.0.0`, `PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0`, `PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0`, checkpoint schema `FIABC_LITS_CURRENT_NEUTRAL_I05_MATERIALIZATION_CHECKPOINT@3.0.0`, precheck schema `FIABC_LITS_CURRENT_NEUTRAL_I05_PRECHECK@1.0.0` |
| **Risk set / denominator / routing / ancestry** | Carried by the 60 facts with full preimages and by the long-format carrier `PRE553_R5_LONG_SHARDED_CARRIER@2.0.0` (`carrier id R5_LONG_SHARDED_TYPED_INCIDENCE_V1`, `canonical_row_count 34,745,595`, 2,121 `.r5z` members + `member_inventory.jsonl` 1,479,183 B, SHA `0d825556…`) |
| **Minority / counterpattern preservation** | Already materialized as `D02_P4` target cells (e.g. `[3,1]`, `[3,2]`, `[5,3]`, `[2,1]` exact-decimal pairs) — must be carried through, not flattened |
| **Independent parity anchor** | `astra_substantive_parity_receipt.json` (`FIABC_LITS_ASTRA_SUBSTANTIVE_PARITY_RECEIPT@1.0.0`) — all sections `PASS`, `status: PASS__CURRENT_LITS_EMPIRICAL_SUBSTANCE_EXACTLY_CONSERVES_ACCEPTED_ASTRA_D04_R2`, `oracle_freeze_authorized: true` |
| **Consumer** | existing accepted rich C1 / I03 / discovery / recursive path; the one-binding scalar N10E wrapper is **not** presumed to encode multi-binding response |
| **Explicit non-reliance** | The WVS7 frozen oracle (46 candidates / 58 roles **expected**, `candidate_outputs_seen: 0`) is **not** used as an S2 witness — a frozen expectation is not a product |

### S3 — Objective structural, multisource and temporal world (F5/F6/F7)

#### S3.a — two distinct source-family structural contributions

| | `S_1` | `S_2` |
|---|---|---|
| **Source-wave** | `LiTS_I.dta` | `Afro Barometer Round 5.sav` |
| **Family** | LiTS | Afrobarometer |
| **Universe** | 29,002 respondents × 1,198 variables (recorded `source_identity` inside the checkpoint) | 19,210 risk respondents co-residing on Q69B + Q86A, drawn from 51,587 source rows; empirical-universe SHA `4dc56730f5c3b06838cc8a6116e0f4c78662b76d75b578918f7207cea3902dd1` |
| **Scope / operation** | exact bounded discovery over the declared frontier: `coverage_claim COMPLETE_FOR_EXACT_DECLARED_FRONTIER`, `claim_kind LEARNED_EMPIRICAL_EXECUTION_ONLY`, `actor_v3_effect false`, `causal_truth_effect false`, `exact_ref_count 225` | one content-addressed mechanical same-source C11 materialization/replay candidate only; release `R5_GT34_Q2_Q69B_Q86A_SAME_SOURCE_CANDIDATE_R1`, release semantic `86a3c75c9f50a0399b6283dd427f0158f4c4767b2dfbfd6e36b231a17c321c58`, source release manifest `a8692ba4…`, replay/package manifest `2c03d007…` |
| **Evidence identities** | checkpoint identity `3fab15f3…`, execution `e547bfc6…3b85c5`, replay `dbd18f3c…428640`, frozen companion oracle `cb1c6ae6…00e3f4` (264,917 B) | transport `GT34_Q2_R5_Q69B_Q86A_SAME_SOURCE_TRANSPORT@1.0.0`, canonical 4,220,457 B / semantic `f179a516…161a61`, gzip 933,040 B / `bac725d5…7ed82`, predecessors `R5_GT34_N2_Q69B_BOUNDED_CANDIDATE_R1` (`23430235…95ec`) and `R5_GT12_Q86A_Q86B_FROZEN` (`8315b104…68295`) |
| **Composition operation** | source-indexed coexistence in the declared objective view, `no synthetic shared respondent` (HQ249 §3 world-context query) | same |
| **Adoption state** | FF02_READY, zero-source resume PASS, machinery present in local checkouts | **`NO_ADOPTION`** — `OBL049: LAWFULLY_CLOSABLE_AT_HQ_FAN_IN`; adoption is HQ-owned |

**Forbidden, explicitly:** pooling the two universes; a synthetic shared respondent table; a numerical structural-pressure multiplier; averaging cross-family respondents; treating either family's respondents as the other's.

**Open interpretive question IQ-1 for HQ:** the accepted cross-source seed table records **0 rows / 0 shared propositions** for `Afrobarometer ↔ LiTS` (and for `Afrobarometer ↔ WVS`, `Afrobarometer ↔ EVS`). HQ249 §2 S3 demands *distinct* contributions entering one view, not a relational bridge, so this proposal reads the 0/0 as non-blocking. If HQ reads it as requiring an accepted F6 relation, either (a) an F6 refresh must be commissioned for this pair, or (b) Bundle 2 of report 04 (LiTS + WVS7, 7 rows / 6 shared propositions) must be substituted. **This proposal does not resolve IQ-1.**

#### S3.b — one same-survey comparable-wave product

| Item | Contract |
|---|---|
| **Pair** | **Afrobarometer R5 ↔ R9** (same survey family, two waves, both physically present) |
| **Pair-specific authority already accepted** | `Rawlsing_P2_Afrobarometer_Accepted_Longitudinal_Continuity_Edges_v1.csv`, 46,257 B, SHA-256 `03cb2e904cc248056932101d99ffdca317c84eab9636e725772832050bde93cc`; **114 of 119 edges are R5↔R9**; all `authority_status = ACCEPTED_SOURCE_LOCAL_CONTINUITY` |
| **Response-comparable subset to be used** | **51 edges** with `portability_ceiling = QUESTION_AND_RESPONSE` and `response_signature_equal = True` — `relation_type EXACT_PROPOSITION_AND_RESPONSE_CONTINUITY`. Candidate pairs include `DemandDemo↔DemandDemo`, `EA_SEC_B↔EA_SEC_B`, `EA_SEC_C↔EA_SEC_C`, `Q107A↔Q106A`, `Q107B↔Q106B`, `Q107C↔Q106C`, `Q107D↔Q106D`, `Q107E↔Q106E`, `Q108↔Q107`, `Q110A↔Q109A`, `Q110B↔Q109B`, `Q110C↔Q109C`, `Q110E↔Q109E`, `Q110F↔Q109F`, `Q13B↔Q74B`, `Q13C↔Q74C`, `Q13D↔Q74D`, `Q15↔Q8`, `Q17A↔Q9A`, `Q20↔Q16`, `Q22↔Q20`, `Q33↔Q18`, `Q34↔Q24`, `Q41↔Q29A`, `Q52B↔Q33A`, `Q55↔Q14B`, `Q56A↔Q33D`, `Q59D↔Q37A`, `Q60E↔Q38E`, `Q7↔Q3`, … |
| **Explicitly NOT usable as the temporal product** | `R5 Q69B → R9 Q41E` — `QUESTION_PROPOSITION_ONLY`, `response_signature_equal=False`. The currently retained R5 questions therefore **cannot** carry the temporal obligation by themselves |
| **Accepted relation types in the file** | `EXACT_PROPOSITION_AND_RESPONSE_CONTINUITY` ×46, `EXACT_PROPOSITION_CONTINUITY_RESPONSE_TOPOLOGY_REVIEW` ×55, `ACCEPTED_DIFFERENT_CODE_WORDING_REVISION_CONTINUITY` ×12, `GOVERNED_WORDING_REVISION_CONTINUITY` ×1 |
| **Portability ceiling** | 51 `QUESTION_AND_RESPONSE`, 68 `QUESTION_PROPOSITION_ONLY`. `r1_caveat` is empty on all 114 R5↔R9 edges |
| **Corroborating (secondary, not authority)** | cross-wave driver atlas: R5↔R9 = **16 shared mapped content ids** (the largest within-family count in the atlas), out of 35 variables mapped in R5 and 27 in R9 |
| **What must still be produced** | One exact same-survey comparable-wave product for at least one of the 51 accepted pairs — i.e. an R5 wave product and an R9 wave product for the *same* accepted construct, both materialized through the already-exercised GT34/GT12 per-question release path, then passed through the lawful temporal→world consumer |
| **Permitted outputs** | increase, decrease, **no change**, changed branch/co-signature/structural relation, or a genuinely produced typed noncomparability. A source-grounded `no-change` must not be rejected because movement was expected (hostile test #8) |
| **Forbidden** | file-year labels as authority; subtracted marginals presented as comparability; declaring the pair competent before both wave products exist |

---

## 4. What is retained versus what must still be produced

| Obligation | Retained today | Must still be produced | Nature of the gap |
|---|---|---|---|
| S1 conditioning | 77 roles, 60 facts, 50 candidates, conditional reversal `EVALUATED_SUPPORTED` | Bind HQ-named `A`,`B`,`Y` to existing role/predicate/query objects; expose through the selected consumer | **governance + consumer binding**, no new science |
| S2 rich joint | Full I03/I05 closure + long-format carrier + frozen oracle | Same consumer binding; multi-binding route selection (not N10E scalar) | governance |
| S3 structural `S_1` | LiTS I product, parity PASS | admission into the declared objective view | governance |
| S3 structural `S_2` | Afro R5 GT34 release, court PASS | **HQ adoption of OBL049** + admission into the view | governance |
| S3 temporal | 114 accepted continuity edges (51 Q&R) for R5↔R9 | **Two wave products for one accepted construct pair**, then temporal→world consumer receipt | **new materialization** (pipeline exists, executed for R5 Q2) |
| Source identity | LiTS I physically re-hashed | Fresh hash of R5 and R9 under warrant | one-time hash pass |
| Consumer / world operation | D1: rich C1→F8 computation accepted | **Named world/current-as-of consumer (N9) and positioned-subject capability (N10W)** | **unbound — report 06 §C** |
| Warrant | `raw_live_warrant_c7_actor_holds: true` | `measured_execution_authorized_via_warrant` must become true for *this* source set | HQ |

**Total new source-facing materialization forced by this contract: one same-survey temporal pair (two wave products on Afrobarometer, one accepted construct).** Everything else is governance, naming, or consumer binding. That is the whole reason this bundle is recommended.

---

## 5. Evidence-cost ledger (why this and not Bundle 2)

| Cost item | Bundle 1 (recommended) | Bundle 2 `{LiTS_I, WVS7, WVS4}` |
|---|---|---|
| Produced second structural product | **already produced** (Afro R5 GT34, court PASS) | **not produced** (WVS7 `candidate_outputs_seen: 0`) |
| Proved execution gaps on the path | none specific to this bundle | 3 (`pre553_runtime_authority` driver-path, no callable WVS `GovernedC11Projection`, `RecursionError` at S01 + *"building one from the SAV would create forbidden carrier/projection work"*) |
| Cold third wave | R9 sits on an **exercised** release pipeline | W4 has **zero** retained artifacts and **no** SAV representation authority of its own (R1J is scoped to SHA `2bd2a20f…`) |
| Temporal authority depth | 114 edges / 51 response-comparable | 92 edges / 66 exact Q&R |
| Cross-family documented overlap | 0 rows / 0 propositions → **IQ-1 open** | 7 rows / 6 propositions → closed |
| Non-execution prerequisite | HQ adoption of OBL049 | three execution gaps to clear first |

Bundle 2 is superior on **cross-family bridge depth** and **response-comparable edge count (66 > 51)**; Bundle 1 is superior on **everything that determines whether a product can exist at all**. Under E3's rule — *"select based on evidence cost not physical PASS status"* — Bundle 1 wins.

---

## 6. Preconditions and explicit non-claims

**Preconditions (all HQ-owned):**

1. **P-1** fresh SHA-256 pass on `Afro Barometer Round 5.sav` and `Afro Barometer Round 9.sav` under warrant.
2. **P-2** HQ adoption decision on `OBL049` for release `R5_GT34_Q2_Q69B_Q86A_SAME_SOURCE_CANDIDATE_R1`.
3. **P-3** resolution of **IQ-1** (cross-family relational bridge or substitution of Bundle 2).
4. **P-4** naming of the actual `A`, `B`, `Y` roles and of the selected EE14/PRE-V3 possibility consumer + N9 world/current-as-of operation + N10W positioned-subject route (D1 currently `WORLD_CONSUMER_OPERATION_UNBOUND`).
5. **P-5** `measured_execution_authorized_via_warrant` set true for this exact source set; `c4_adopted` and `hq182_hold_lifted` resolved as required by HQD125/HQD216; `source_hold_unchanged` reviewed only by HQ.
6. **P-6** execution environment: 11 GiB free of 466 GiB (98% used) must be verified sufficient for a temporal pair materialization before dispatch; `caffeinate -dimsu` session per R1 blocker C4.

**Explicit non-claims:**

- No new ontology, stage, operator, model rule, survey permission, runtime schema or consumer implementation is proposed.
- No pooling, portability, comparator, PSEPF, metabolism, CAN-008, V2 or V3 authority is created or widened.
- No causal claim, coefficient, effect size, social group or temporal direction is asserted; actual source truth is allowed to disappoint.
- No raw `.sav`/`.dta` content was opened in producing this contract.
- No repo file was created, modified, staged or committed; the five continuity-edge CSVs were extracted to `/tmp/…/_p2/` for reading only.
- `A`, `B`, `Y`, `q(A)`, `q(A,B)` remain illustrative symbolic roles.
- No V3 actor is instantiated; possibility distributions remain population-conditioned fields.

---

**TERMINAL:** `MINIMUM_EMPIRICAL_INPUT_SET_PROPOSED__NO_SELF_AUTHORIZATION`
