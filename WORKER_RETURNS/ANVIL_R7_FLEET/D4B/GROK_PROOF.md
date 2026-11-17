# GROK_PROOF — D4B independent pre-grok (corrected exact-source pass)

**Role:** independent ANVIL corrective rabochiy, D4 / adversarial B. Not HQ, not final independent C, not architecture selector, not H1 receiver.
**Grounding mode:** `HOSTILE_INDEPENDENT_AUDIT` + `FORENSIC_READ_ONLY` under `GOVERNANCE_PROTOCOLS_R1/DECISION_AGENT_GROUNDING_PROTOCOL.md`.

**Status:** `GROK_INCOMPLETE_F26_EXACT_CALLER_ONLY`. All other required sources were read at exact bytes in the same local Git object store; the one genuine gap is the exact original F26 per-query caller/source, which the K3/P4R rows themselves mark unverified. No contradictory full-GROK or grounding PASS is asserted.

**Fleet bank intake (2026-11-17):** read `evidence/fleet_bank/START_HERE.md`, `FORENSIC_RECOVERY/ANVIL_118_FORENSIC_AUDIT.md`, `ANVIL_118_SOURCE_IDENTITY_MAP.tsv/.json`, and the bank's `SOURCE_SNAPSHOTS`/`FROZEN_GROKKING_SOURCES`. Bank commit `8523007613d411390a76683fa464002c0f25df83`. The forensic audit is treated as an **allegation tested against my own executions**, not authority; it independently corroborates H01/H02 (synthetic spine accepted), the 118→decision gap, boundary demotion and the false R5 SPINE prerequisite. Bank byte limits are reported in the table below.

## Exact cut and sources read this pass

| Item | Exact identity | Evidence |
|---|---|---|
| live protected | `31291d08179890852246c8742700e055168e9933` | local evidence copy |
| K3 snapshot | `7fc00289dd801d2d0a8ce159986c7595fc27a4d9` | K3 blobs identical at 31291d0 |
| K3 TSVs | blobs `a91214b9…`, `1f5a3ae8…`, `5a84ca8c…` | 29/26/14 rows |
| SEAM/25 | `596f1230258ff50f98d8543dec42a80e696720f4`, blob `181ab1aaee26d71524dd7401a59c2ca550b4a81c`, 81 lines | `git show` |
| SEAM/26 | `796452b8cb788fa5a02f37a7ce86eafce8312dfe`, blob `a05c21dd0b7b1d404fc500c0ef36c81aee67c96e`, 116 lines | `git show` |
| ANVIL/15 | `3cc09bba3d0e26c226da0ddca4b64c43dd74e493`, blob `6253a632d10f201e0bf446f055f96c82fb4a479f`, 235 lines | `git show` |
| V549 builder | `data/ddm_build_copy/build_branch_co_signature_summary_v549.py`, blob `eb143ffef48e099217b74079252dfce86a6e65ef`, 800 lines | `git show` |
| V550 branching | `data/ddm_build_copy/ddm_v550_branching.py`, blob `8f6d40e0d016d66e5a3b334b31747eaef752873f`, 466 lines | `git show` |
| V550 distributions | `data/ddm_build_copy/ddm_v550_distributions.py`, blob `43a62723b16f9c800ed7a6ef40a77e70a3f07377`, 321 lines | `git show` |
| V550J substrate | `data/ddm_build_copy/build_v550j_prepared_substrate.py`, blob `5226fef27903bf55984e0ca4134b6d42404305c2`, 523 lines | `git show` |
| V550J compiler | `data/ddm_build_copy/compile_v550j_joint_response_patterns.py`, blob `b42b00cadca6284ff99889116e8aebbc109e940e`, 2515 lines | `git show` |
| 4913 return | `4913b562d71a7773d5e4a6dec6c0d9684fd72410` | `FRAME.json`, `FRAME_GATE_OUTPUT.json`, `00_RETURN.md` |
| supplied ZIP | SHA-256 `526d835d…fbbfc9131072332`, 280 files | private copy, unchanged |
| fleet bank | `8523007613d411390a76683fa464002c0f25df83` | `evidence/fleet_bank/`; START_HERE + FORENSIC_RECOVERY read |
| bank manifest check | 299 entries, **297 hash-match, 2 mismatch**; 279 extracted ZIP text members, **278 exact, 1 CRLF→LF** | `evidence/FLEET_BANK_VERIFICATION.json`; not 299/299 or 279/279 |

**Bank limits, precise:** the two manifest mismatches are
`FORENSIC_RECOVERY/ANVIL_118_SOURCE_IDENTITY_MAP.tsv` and
`R7_EXTRACTED/MAINMAC_R6_REFERENCE/ANVIL_R6/tests/SYNTHETIC_DERIVED/EVIDENCE_AND_FALSIFIERS.tsv`.
The latter differs from the original ZIP bytes only by CRLF→LF normalization
(`zip_sha256 b4877a0f…` vs `bank_sha256 c03e81f6…`). The identity map is a
navigation aid, and its K3 paths contain the known doubled slash
(`K3_HQ_POST_AB_OWNER_DECISIONS_20261116_R1//K3_CONSERVATION…`); it is not a
semantic record. The original ZIP SHA-256 `526d835d…` remains byte authority;
my private `PACKAGE/` was **not** overwritten from the bank.

## Ten probes, exact evidence and falsifier

### 1. Why `118 = 29+26+14+10+8+8+7+16`, and which 69 are K3 TSV rows?
`03_FROZEN_SOURCE_CUTS.json.mandatory`: `K1_CAP` 29, `PYAT_PC` 26, `P4R` 14, `SEAM_B` 10, `SEAM_S` 8, `ANVIL_L` 8, `BOUNDARY` 7, `TERMINAL` 16 = 118. The 69 exact K3 rows are the first three groups (`wc -l` 30/27/15 including headers). They are different kinds: SEAM/25 lines 32–41 give **B-01…B-10** as boundary questions ("Can actual source-qualified … reach a legitimate person/world generator without respondent→character identity collapse?"); SEAM/26 lines 36–43 give **S-01…S-08** as reverse requirements ("Whole configurations", "Conditional co-travel and minority", …); ANVIL/15 lines 50–57 give **L-01…L-08** as irreversible input-loss risks ("Native instrument meaning", "Granular respondent identity/occurrence", …). K3 `new_BUILD` is `NONE__NO_K4` on all 26 PC rows; all 14 P4R `protected_receiving` rows are `HELD__INDEPENDENT_K3_REVIEW_AND_CUSTODIAN_CAS_NOT_DONE`.
**Falsifier:** an accepted protected `ANVIL_SPINE_R5/R6` with 118 semantically complete function records. `20_RECOVERY_AND_TEST_PROVENANCE.md` says R5 is `PREPARED / LOCALLY STRUCTURALLY TESTED / NOT DISPATCHED` and a source-qualified SPINE was the expected output.

### 2. Why is a source-qualified 118 identity inventory lawful at S1 but a final 118→design/hold disposition only at decision?
At S1 the lawful object is identity accounting: exact source pointer, row bytes/hash, owner, negative and first consumer-or-hold. A design disposition has no referent until a candidate physical arrangement exists. `01_DECISION_CONSTITUTION.md` separates PRESERVE / PHYSICAL / FUTURE_NONPRECLUSION and defines the decision as the smallest arrangement; `29_R7_…` S1 requires the frame before design and S3 requires a non-vacuous disposition per requirement after the synthesis.
**Correction to my earlier attribution:** the exact 4913 return does **not** assign `PRESENT_PRESERVED` anywhere. Its `FRAME.json` has **no** disposition key, 53 requirement rows, `architecture_selected=false`, and `FRAME_GATE_OUTPUT.json` is `RED` with the single error `FRAME:HISTORY:NO_POINTER`. `00_RETURN.md` states "No INTEGRATED_DECISION exists… No architecture… was selected" and holds the missing SPINE. That attribution is withdrawn.
**Source-specific criticism now:** 4913 correctly refused to fabricate, but its `HISTORICAL_TRANSFER_HOLD.json` treats a full 118-record `ANVIL_SPINE_R5/R6` as the only lawful route and concludes K3 "covers only 69 of 118 identities and do[es] not carry the full R5/R6 semantic record shape". That is the false S1 dependency: the 118 is a mixed identity universe (probe 1), not 118 R5 records; the other 49 can be sourced from SEAM/25, SEAM/26 and ANVIL/15 directly. 4913's gate is RED only at the missing pointer, not at a semantic disposition failure.
**Falsifier:** a pre-decision document that assigns `PRESENT_PRESERVED` to a 118 row without a selected design or first consumer. 4913 is not that document.

### 3. What goes wrong when a synthetic source-consistent `SPINE.json` passes a local transfer equality check?
`r7_transfer_conservation.transfer()` accepts any object with schema `ANVIL_SPINE_R5/R6` and calls only `r7_integrated.check_history()`; that check requires the 118 IDs and six prose fields of ≥12 chars (`tools/r7_integrated.py:57-79`). `check_frame()` then compares `original.coverage != history.coverage` (`:119-120`). Two copies of the same synthetic ledger are equal to each other. Executed: H01 `PASS_TRANSFERRED`; H02 FRAME `PASS_LOCAL_COMMON_REQUIREMENTS_NOT_OWNER_AUTHENTICATED`. Source-authenticate by `git show 7fc…:TSV`, exact row SHA-256, excerpt-in-row and negative vocabulary; H03 (row hash changed) then becomes RED.
**Falsifier:** if the helper authenticated source, the H01 boilerplate ledger would fail. It does not.

### 4. What essential information from V549/V550/V550J/F26 survives irrespective of old Postgres layout, and which historic bugs do not?
Exact source evidence:
- **V549** (`build_branch_co_signature_summary_v549.py:58-63`) defines a `BranchNode(row,parent,branch_type,conditions)`; `build_branch_mask` (`:449-493`) recursively reuses a parent mask and distinguishes `majority_position_conformity`, `majority_position_deviation`, `minority_position_convergence`, `minority_position_divergence`; `summarize_branch` (`:560-585`) keeps `branch_n`, `base_branch_values` vs `base_all_values`, and `valid_join = branch_mask & item_values.notna()` with `valid_n`. That is the surviving recursive lineage/minority/denominator information.
- **V550 branching** (`ddm_v550_branching.py:372-435`) recurses with `effective_min_branch_n = support_threshold_from_total(...)`, `conditional_entropy`, `entropy_gain_from_parent`, and stops on `pure_or_near_pure`, `max_depth`, `underpowered`, `no_remaining_indicators`; branches are support-gated, not enumerated Cartesian products.
- **V550 distributions** (`ddm_v550_distributions.py:230-260`) computes `weight_status`, `total_weighted`, `total_unweighted`, `n_weighted`, `pct_weighted`, `pct_unweighted`, and treats underpowered answers separately. Weighted and unweighted denominators are distinct source facts.
- **V550J substrate** (`build_v550j_prepared_substrate.py:94-130`) preserves `respondent_id`, `respondent_id_norm`, `weight_value`, `weight_status`, `var_code`, `response_value`, `is_missing`, `is_dk`, `is_refusal`, `is_iap`, `is_valid_substantive_response`; `load_or_build_v550j_prepared_substrate` (`:316+`) validates a cached prepared substrate against authority/registry/semantics/schema hashes.
- **V550J compiler** (`compile_v550j_joint_response_patterns.py:868-878`) requires `joint_response_pattern_index`, `joint_pattern_respondent_membership`, `joint_pattern_meaning_summary`, `joint_pattern_audit`, etc.; `_family_item_order` (`ddm_v550j_joint_patterns.py:1465-1473`) fixes ordered item membership; membership rows (`:1540-1552`) carry `respondent_id`, `weight_value`, `pattern_count_unweighted`, `pattern_count_weighted`, `pattern_support_status`.
Surviving semantics: question/option/translation/routing, same-respondent membership, ordered events, support thresholds, recursive branches, minority/convergence/deviation, weighted vs unweighted denominators, typed missing. Not surviving as authority: PostgreSQL as canonical semantic owner/universal law, historical V550J `2,499/15,990`, the empty V552 contradiction tensor, and pairing products as joints (`00_CANONICAL_ENTRYPOINT` §6–§7; `05_HISTORICAL_FUNCTION_SUCCESSION…`).
**Precise F26 gap:** F26 is not a file in the protected tree. K3 `K1-CAP-24` (row 25) says `T1_NECESSITY=F26_HISTORICAL_EXECUTABLE_UNVERIFIED` and `F26_OLD_CALLER_HOLD_NO_BUILD…`; `P4R-R02` (row 3) says `Actual old F26 per-query caller/identity and source-data invalidation` is `HELD_SOURCE_LOCATOR`; `PYAT-PC-R11-21` (row 22) says `old F26 callsite not independently verified; do not require replication of an obsolete cache`. The bank's `FROZEN_GROKKING_SOURCES/` and `SOURCE_SNAPSHOTS/` contain F26 only inside the same K3 TSVs; no F26 source file or caller was found. The exact original F26 caller is therefore a **precise GROK_INCOMPLETE**, not a claim that V549/V550/V550J were unavailable.
**Falsifier:** a protected file that makes PostgreSQL or the 2,499/15,990 carrier current authority; or an F26 source file/caller that contradicts the K3 hold.

### 5. Why can matching survey marginals conceal different true three-way respondent patterns? Distinct F2 denominators and typed missing/routing.
Correct exact witness (script `MUTATION_TESTS/probe5_witness.py`, log `PROBE5_WITNESS.log`):
- A: X,Y,Z iid Bernoulli(1/2): all eight cells 1/8.
- B: X,Y iid Bernoulli(1/2), Z=X⊕Y: `000,011,101,110` each 1/4; `001,010,100,111` each 0.
Both have every univariate marginal 1/2 and every pairwise marginal 1/4 per cell; the 3-way joint differs. Forward `P(Z=1|X=0,Y=0)` is 1/2 in A, 0 in B. Reverse `P(Y=1|X=1,Z=1)` is 1/2 in A, 0 in B. `P(Y=1|Z=1)=1/2` but `P(Y=1|X=1,Z=1)=0` in B: the reverse risk set is different. SEAM/26 line 90 states the requirement: "Same marginals, different true 3-way joint: fixed univariate/pairwise frequencies but rearranged k-way same-person patterns must produce different FF consumer configuration possibilities".
Typed missing/routing: `NOT_ASKED`, `ASKED_REFUSED`, `NOT_RELEASED`, `NOT_ELIGIBLE`, `HOUSEHOLD_MEASURE`, `MODELED_PROXY`, `FICTIONAL_ONLY` (`01_DECISION_CONSTITUTION`; `ANVIL/15` L-03/L-04). F2 forward and reverse denominators differ by eligible/asked/released/answered and by weight.
**Correction:** my earlier "000/111 equiprobable" illustration was false; it does not share pairwise marginals with the parity distribution. It is replaced by the XOR witness above.

### 6. Why may an instrument's sampled design stratum not imply measured respondent sect/ancestry? Native source vs modeled possibility.
ANVIL/15 lines 115–120 define the observability classes: `OBSERVED_RESPONDENT`, `COLLECTED_BUT_NOT_RELEASED`, `SAMPLE_DESIGN_ONLY`, `EXTERNAL_GROUP_CONTEXT`, `PROXY_OBSERVED`, `MEASUREMENT_NONCOMPARABLE`, `SOURCE_UNAVAILABLE / RIGHTS_HELD`. The case study is exact: "Arab Barometer II: technical sampling of Lebanese religious strata does not license particular A/B/C Sunni/Shia"; "Latinobarómetro Brazilian Muslim: broad race/color and religious identifiers can omit Lebanese ancestry; group estimates cannot be projected onto a specific respondent" (lines 127–130). SEAM/26 S-06 (line 41) adds "Wave II 'Muslim' cast as measured sect; independent cross-sections used as longitudinal self" as a prohibited move. Native source state is `NOT_ASKED`/`NOT_RELEASED`; person-level attribution is at most `MODELED_PROXY` and must refuse or be labelled modeled.
**Falsifier:** a released individual-level ancestry/sect field for the named instrument. None is asserted in the protected source.

### 7. Distinguish FF01 descriptive, FF02 structural/causal owner, N9/N10W world, SOROK actor psychology. Negative example.
FF01 is the actor-independent descriptive relation (co-travel, marginals, conditionals). FF02/N6 owns independently sourced material/structural power: SEAM/25 B-02 (line 33) requires "independently evidenced institutional control, labor/care/tenure, sanction and counterpower … separated from survey opinion prevalence"; SEAM/26 S-04 (line 39) requires "Independently measured/qualified structural resources, class ownership/labor/care, institutions, coercion, sanction". N9/N10W compose selected possible worlds/opportunities; SEAM/25 B-03 (line 34) requires the conditioned option to "actually change… not joined-hash only". SOROK owns access, perception, motive, activity and development; SEAM/25 B-07 (line 38) states "Event offscreen but no actor access ⇒ no automatic knowledge" and "PYAT supplies no private motive". Negative example: identical survey attitude joint plus two admitted synthetic household work/tenure arrangements may change actual P2 feasibility, but must not claim PYAT observed those households or infer a caregiver psyche (SEAM/25 Case A, lines 63–65). T4/T6 vetoes in `02_BOUNDARY_CONTRACTS.json` forbid survey opinion as institutional power and survey answers as mandatory private motives.
**Falsifier:** a graph edge from `OBSERVED`/`DESCRIPTIVE_MODELED` to `ACTOR_STATE` without an admitted event/access witness; the supplied R7 gate permits it (H09).

### 8. Why does a producer and verifier agreeing on a hash not prove source truth? Cold revocation and actor/world firewall.
A hash proves byte identity, not protected provenance or authority. ANVIL/15 L-07 (line 56) says "No 'same hash' unanchored proof". H01/H02 show two synthetic documents agreeing; H04 shows a forged file whose self-hash matches while the claimed Git blob content differs. Cold revocation must store a release id/status and a revocation test; a revoked/superseded id must refuse before any row is served and exact restore must reproduce. Actor/world firewall: an admitted event with recorded access may change actor state; an inaccessible event must produce no knowledge; fictional/world effects may never write empirical C11 (T7; SEAM/25 B-10, lines 41; SEAM/26 section 7, lines 104–113).
**Falsifier:** a packet with `release.status=REVOKED` and a fabricated protected head still passes. That is H10 in the supplied gate.

### 9. What are the seven T1–T7 boundary questions, and why are they neither seven new pipeline stages nor independently accredited science?
T1 source→governed canonical evidence; T2 canonical→respondent-coherent computation; T3 computation→differentiated social field; T4 field+structural→objective-world relations; T5 possibility→particular fictional world/encounter; T6 encounter→independent developing person; T7 performed activity→next historical situation. Each has producer, receiver, must-preserve, first effect, veto, time class and owner (`02_BOUNDARY_CONTRACTS.json`, `status: FROZEN_REVIEW_INSTRUMENT_NOT_ADOPTED_PREV3_SCIENCE`). Direct branches may bypass intermediate products if the invariant survives; satisfying the text grants no science/source/actor authority.
**Falsifier:** a claim that T1–T7 are seven executable stages or that their JSON text accredits PRE-V3 science.

### 10. Acceptance difference: prepared/locally tested R5 tools vs source-verified 118 inventory vs integrated decision vs independent C vs protected H1.
- R5 tools: `PREPARED / LOCALLY STRUCTURALLY TESTED / NOT DISPATCHED` (`20_RECOVERY`), synthetic/format only.
- Source-verified 118 inventory: S1 documentary identity accounting at exact K3/SEAM/ANVIL rows; no design, no science.
- Integrated decision: one author synthesis, `AUTHOR_PROPOSED_PENDING_C`; local gate `PASS_LOCAL_INTEGRATED_DECISION_PENDING_C`.
- Independent C: distinct nonauthor review of the same frame and actual first reader; local guard `PASS_LOCAL_C_PACKET_ONLY_INDEPENDENCE_UNVERIFIED`; cannot prove independence.
- Protected H1: competent owner/protected receiving after exact review; "No local H1 accreditation" (`00_R7_READ_FIRST` §5). The exact 4913 return is an S1 frame with `RED` `FRAME:HISTORY:NO_POINTER`, not H1.
**Falsifier:** an artifact claiming H1, scientific grant or protected receiving from a local PASS. None exists in the supplied ZIP.

## Grounding receipt (corrected)

- **receipt ID:** D4B-GROUND-20261117-R2
- **canonical head:** `31291d08179890852246c8742700e055168e9933` (local copy; live GitHub not re-queried)
- **fleet bank pin:** `8523007613d411390a76683fa464002c0f25df83` (297/299 manifest, 278/279 ZIP text; limits above)
- **task scope:** hostile mutation of the ANVIL R7 instrument and its source/consumer contracts; not physical architecture selection.
- **required sources read:** K3 29/26/14 raw rows; SEAM/25; SEAM/26; ANVIL/15; V549/V550/V550J named files at exact blobs; 4913 FRAME/gate/return; W55 ground; MCR-lite; historical succession law; PYAT front door; `01_DECISION_CONSTITUTION`; `02_BOUNDARY_CONTRACTS`; `03_FROZEN_SOURCE_CUTS`.
- **precise missing original:** exact F26 per-query caller/source bytes; K3 `K1-CAP-24`/`P4R-R02`/`PYAT-PC-R11-21` mark it `F26_HISTORICAL_EXECUTABLE_UNVERIFIED` / `HELD_SOURCE_LOCATOR`. Owner: ZL02/F26 source owner and #815.
- **GROK status:** `GROK_INCOMPLETE_F26_EXACT_CALLER_ONLY`.
- **GROUNDING_COMPLETE_FOR_DECLARED_SCOPE:** `NOT_ASSERTED` (consistent with the F26 gap; all other declared topics pass).
- **authority ceiling:** I may decide only whether the named instrument defects are real and whether the bounded strict overlay makes them RED.
- **may not decide:** architecture winner, science/source/actor grants, independent C verdict, protected H1, another worker's status.
- **return destination:** `WORKER_RETURNS/ANVIL_R7_FLEET/D4B/`.
