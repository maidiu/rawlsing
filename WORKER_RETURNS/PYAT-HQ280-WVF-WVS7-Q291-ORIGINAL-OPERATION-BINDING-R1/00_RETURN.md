# PYAT HQ280 WVF — WVS7 Q291 original-operation → I05 → T3 exact expected-work and no-drop binding

**TERMINAL:** `HQ280_WVF_EXISTING_WVS7_Q291_ORIGINAL_OPERATION_TO_I05_T3_INDEPENDENT_NO_DROP_BINDING_OR_EXACT_SCIENTIFIC_HOLD__GITHUB_PUSHED`
**Disposition:** `NO_DROP_CONFIRMED_AT_FRONTIER_GRAIN__PRE_I05_EXPECTED_SET_CONFIRMED__PRE_I05_TRUTH_ORACLE_FALSIFIED__ORIGINAL_INSTRUMENT_ITEM_FIELD_HOLD__NO_SELF_ADOPTION`
**Branch:** `agent/rabochii-pyat-hq280-wvf-wvs-q291-original-operation-binding-r1` @ sealed tip `e81b428bf6a7e28ede8959da05e6dd3fd68405f2`
**Law:** HQD-2026-10-10-280 · canonical `6a8c91d99dca1ae2fd3559ba3c11ee26649e3cd9` · PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (unmutated).
**Mode:** bounded reuse of an **already-retained real-source-derived product**. No raw WVS source opened, no new I05, no new engine, no adoption.

## 1. What the chain actually is (verified from accepted receipts)

| stage | identity | evidence |
|---|---|---|
| source | WVS7 `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`, 97,220 rows × 613 vars, `owner_class=EXACT_SOURCE` | `07` `source_identity`, `oracle_build_provenance.dependencies[0]` |
| R15 C11 release | `C11LogicalRelease` `WVS7_FROZEN_P2_EXACT_SOURCE` = `e6881e9a08a48f8871790e781c28bddbc44ee35db894d6ad7b1105a6a8fd262f` | `06` `admitted_r15_release_ref` |
| R15 replay | `ReplayManifest` `996ba218fc5da5e0ad1ddf0cdc7f91ce8fb8a7363ce62076dc3f4073b85c383f` | `06` `admitted_r15_replay_ref` |
| candidate grammar | `a94bd2ed3b64b2c51f6d329560feef6b97f69da3527081d8ca6168ae63e5f7f6` | `03`, `06` |
| generic I05 | blob `c7380774e8a1959da5ed8c6f23c2fc3cf99ad18d`, `generic_i05_modified: false`, `neutral_generic_i05_executions: 2` | `06`, `10` |
| evaluated frontier | `PRE553_I05_EVALUATED_FRONTIER` `b2c3c50b68bcadb94ff2bf898d11c2b72694ced9fee4154e535db2694e26a4f3` | `06` |
| I05 frontier replay | `a9d999d96533ceaf4535448a6a488227c05d205866a93feb391080c68d6f3024` | `06` |
| R1M fresh oracle | `3694b8bd0b5468433a1a83bd469337c7e36e552c3a9a5fef65fff88df8fce800`; truth payload `eb2f9224219385dbf21af70d317e0978383012ff057ce2ac857b59c130472405` | `07`, `08` |
| T3 standard oracle | `RAWLSING_FIABC_CANDIDATE_NEUTRAL_PARITY_ORACLE@1.0.0` `e546c15533ba138be9995095059ea3b70b64a6d7b5765e3789935cff7342ef00` | T3 freeze `court/oracles/WVS7.standard.json` |

## 2. The decisive chronology finding (HQ must read this)

The commission asks whether R1M's 46-member oracle was **independently frozen prior to the relevant I05 outcome**. Two different claims must be separated — and the retained evidence supports only one:

**CONFIRMED — independence from Candidate A/B/C.** `08_ORACLE_INDEPENDENCE_PROOF.json`: `candidate_outputs_seen: 0`, `candidate_owned_roots_consulted: []`, `candidate_owned_state_reused: false`, `candidate_processes_started: 0`, `first_successful_candidate_used_as_golden: false`, `pairwise_candidate_vote_used: false`, `pruning_performed: false`; freeze receipt `freeze_sequence: 1`, `candidate_output_first_sequence: null`; telemetry `candidate_a_b_c_processes_started: 0`. **No ABC winner exists.**

**FALSIFIED — "frozen before I05".** The executed pipeline order in `10_COMMAND_TELEMETRY.json` is:

```
GATE_3_SOURCE_FREE_FRONTIER_REPLAY   78 ms      (46 candidates)
GATE_4_SUCCESSOR_LOCK2               12 ms
GATE_5_R16_REENTRY              790,750 ms      <-- the two generic I05 executions
GATE_6_FRESH_ORACLE_AND_SECOND_REPLAY 504,100 ms  <-- the oracle truth payload is ASSEMBLED HERE
GATE_7_R01_R18_FINAL                  0 ms
```

and the oracle's own status is `PASS__FROZEN_BEFORE_CANDIDATE_EXECUTION` — i.e. frozen before **candidate (A/B/C)** execution, not before I05. The retained failure labels are literally `POST_I05_ORACLE_HELPER_ATTEMPTED_TEMPLATE_CATALOG_RESOLUTION_OF_GENERATED_QUERY_REF` and `POST_I05_ORACLE_SERIALIZER_ASSUMED_RECEIPT_REF_FIELDS_WERE_EXACTREF_NOT_MAPPINGPROXY`.

**Correct decomposition:**

| layer | before/after I05 | content |
|---|---|---|
| **expected set** (frontier, 46 ordered candidate identities, `candidate_grammar a94bd2ed…`, `frontier_digest cf825581…`) | **BEFORE** (GATE_3) | the genuine pre-I05 expected-work identities |
| **truth evaluation** (`expected_fact_manifest`, `COVERAGE_LIMITED`, `empirical_fact_refs`) | **AFTER** (GATE_6) | a post-I05 truth *evaluation* of that frontier |

So: **an independently-derived pre-I05 expected set EXISTS; a pre-I05 truth oracle does NOT.** The 46-member expected *identities* may be used as the expected set. The 46 typed *outcomes* must be labelled post-I05 evaluation, never a pre-registered oracle.

## 3. The 46 typed outcomes — honest coverage limit, not a manufactured result

All 46 are `coverage_state = EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY` → typed `COVERAGE_LIMITED`, and **all 46 carry a real `empirical_fact_refs`** (each was actually measured). Distribution:

| family | n | rule | validation |
|---|---:|---|---|
| `BOUNDED_K_WAY_RESPONSE_CONFIGURATION` | 25 | `R08_JOINT_5X5` | `TARGET_CELL_SUPPORTED` (35 total) |
| `UNARY_SOCIAL_FORK` | 10 | `R08_UNARY_Q0` ×5, `R08_UNARY_Q1` ×5 | `TARGET_CELL_SUPPORTED` |
| `BRANCH_CONDITIONED_DISTRIBUTION` | 10 | `R08_BRANCH_Q0_TO_Q1` ×5, `R08_BRANCH_Q1_TO_Q0` ×5 | `DISTRIBUTION_DIFFERS_FROM_BASELINE` (10 total) |
| `PAIR_RESPONSE_COTRAVEL` | 1 | `R08_PAIR_COTRAVEL` | `JOINT_NOT_PRODUCT_OF_MARGINALS` (1 total) |

**Typed-negative classification (per commission item 3):** these are **honest coverage limits** — *not* missing jobs (all 46 executed), *not* unsupported (each has a measured fact), *not* zero denominators, *not* merely absent, *not* arbitrarily dropped. The limit is precisely **missing/conflicting governing authority to promote an evaluated fact into an eligible operation**.

## 4. No-drop — CONFIRMED at the frontier grain

- `06_R16_EXECUTION_RECEIPT.json`: `covered_candidate_count: 46` **=** `candidate_count: 46`; `ordered_candidate_hashes` conserved; `03_46_CANDIDATE_REPLAY_CONSERVATION.json`: `exact_hash_stream_equal: true`, `additions: 0`, `candidate_ranking_controls_frontier: false`.
- **Cross-oracle grain preservation:** the R1M fresh oracle and the T3 standard oracle carry the **same** `frontier_digest cf8255816dc2ba5a51f6fc5918f09e901a5190f147a5192bd805f2908987299e` and the **same** `authority_closure_digest b9be2091764654a91e6b2c62e6e05311c677b60af3b5d8b942f5041280e056c4`, and both hold **46 `COVERAGE_LIMITED`** in `expected_fact_manifest` (T3 additionally carries 58 `UNAVAILABLE` + 1 `FROZEN_READ_ONLY` outside the 46).
- **No-drop at the permitted scope = 46/46 conserved, 0 additions, 0 drops, stable order, replay equal.** This does **not** extend to the 78,037 WGC annotations or to 35 waves.

## 5. Original instrument item — exact HOLD at one field

The accepted receipts bind the **source**, the **R15 release**, the **candidate grammar**, the **I05 frontier** and the **oracles**. They do **not** bind the **source-native original instrument item** for Q291: question wording, native response codes, asked/routing exposure, respondent-unit identity, weight/design role.

- The chain's item-level identities are **I05 candidate/query/predicate hashes** and **R08 rule ids** — derived operation identities, not original instrument semantics.
- LR-C documents "WVS7 Q291" at the **documentary** level; that is **not** an accepted in-repo source-authority binding.

**Therefore: `HOLD__ORIGINAL_INSTRUMENT_ITEM_FIELD_UNBOUND`.** I do **not** invent respondent risk, measure meaning, codes or routing from a physical variable name. Smallest competent packet needed: the WVS7 Q291 original questionnaire/codebook entry (wording + native codes + routing) plus the source-native role/weight designation, issued by the WVS source-semantics owner.

## 6. What is credited, and what is NOT claimed

**Credited (prior execution, not mine):** the persisted WVS7 real-source-derived carrier → admitted R15 C11 release → two generic I05 executions → R1M oracle → T3 loader chain; the 46 conserved `COVERAGE_LIMITED` outcomes; `neutral_generic_i05_executions: 2`; `generic_i05_modified: false`.

**NOT claimed:** no new raw-source remeasurement (`raw_wvs_source_reads: 0`, `wvs_sav_opened: false`); no fresh I05 run; no all-35 no-drop; no ABC winner; no objective-world/N9/V3/actor; no adopted expected-work key; no eligibility for other waves or sources.

**Terminal:** `HQ280_WVF_EXISTING_WVS7_Q291_ORIGINAL_OPERATION_TO_I05_T3_INDEPENDENT_NO_DROP_BINDING_OR_EXACT_SCIENTIFIC_HOLD__GITHUB_PUSHED`.
