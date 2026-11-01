# Decisionless or contradictory cases

This is the finite residual docket. It does not invent a decision to make a branch look accounted for.

## Counts

| Fate category | Branches |
|---|---:|
| `HQ_ACCEPTED_CODE_INTEGRATION` | 9 |
| `HQ_ACCEPTED` | 42 |
| `HQ_ACCEPTED_WITH_HOLD` | 18 |
| `HQ_ACCEPTED_FOR_REVIEW` | 2 |
| `HQ_HELD` | 5 |
| `HQ_REVISE` | 2 |
| `HQ_SUPERSEDED_OR_RETIRED` | 1 |
| `REVIEW_ACCEPTED_BOUNDED` | 26 |
| `REVIEW_REVISE` | 36 |
| `REVIEW_HOLD` | 7 |
| `REVIEW_REJECTED` | 3 |
| `CANDIDATE_RETURNED_NO_HQ_DECISION` | 472 |
| `DOCUMENTED_NO_DECISION` | 132 |
| `CONTROL_OR_RECEIPT_ONLY` | 90 |

- Frozen roster rows: **845**.
- Distinct tips: **838**; duplicate-tip groups: **7**.
- Candidate/documented/control but no located HQ decision: **694**.
- Branches with an explicit reviewer verdict: **72**.
- Branches with a primary HQ/checkpoint/reviewer decision: **155**.

## Candidate / documented / control branches by program prefix

These are not all "unknown": most are worker returns or control receipts whose final HQ disposition was not appended in a branch-scoped form. They require HQ adjudication, not a new inference.

| Prefix | Branches |
|---|---:|
| `R3` | 73 |
| `HQ280` | 73 |
| `R1` | 47 |
| `HQ126` | 14 |
| `R157` | 13 |
| `SRC04` | 12 |
| `HQ282` | 12 |
| `R56` | 10 |
| `R61` | 10 |
| `R2` | 7 |
| `HQ281` | 7 |
| `HQ204` | 6 |
| `HQ254` | 6 |
| `R26` | 5 |
| `R43` | 5 |
| `R53` | 5 |
| `R4` | 5 |
| `R5` | 5 |
| `R6` | 5 |
| `R33` | 5 |
| `HQ260` | 5 |
| `HQ202` | 5 |
| `HQ203` | 5 |
| `HQ270` | 5 |
| `HQ273` | 4 |
| `R23` | 4 |
| `R27` | 4 |
| `R28` | 4 |
| `R29` | 4 |
| `R37` | 4 |

## Sample of branches with no located HQ decision

The complete 845-row disposition is in `RECENT_BRANCH_FATE_LEDGER.jsonl`. The first 80 residual rows are listed here in roster order.

| Branch | Tip | Category | Tip date | Subject |
|---|---|---|---|---|
| `agent/astra-persona-first-prev3-completion-replan-r2` | `0d38dae68ff4` | `DOCUMENTED_NO_DECISION` | 2026-10-12 | Replan Rawlsing around a usable persona loop and parallel full-estate completion |
| `agent/astra-persona-first-prev3-seam-correction-r3` | `88d3c40def26` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-12 | Complete sociological PRE-V3 plan, seam contract and conserved R3 crosswalks |
| `agent/astra-r3-prea0-prev3-v3-joint-weld-advisory-r1` | `3b2d9a1b644a` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-14 | Complete official Astra joint weld advisory with corrective audit and exact freeze |
| `agent/astra-ur-program-sourcefree-evidence-direction-r1` | `f910b067e841` | `CONTROL_OR_RECEIPT_ONLY` | 2026-10-22 | docs(R56): close scoped first-flight qualification and prepare finite HQ handback |
| `agent/browser-astra-ur-m3-final-package-assembly-r1` | `fb20c9879477` | `CONTROL_OR_RECEIPT_ONLY` | 2026-10-21 | docs(UR-M3): assemble settled director A-G and unissued implementation flight |
| `agent/browser-astra-ur-s1-return-evidence-clarification-r1` | `a9fc811ecc2a` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-21 | docs(UR-S1): clarify S3 occurrence projection and S1 learned XOR evidence |
| `agent/browser-pyat-hq-r86-r8-succession-candidate-r1` | `93d057b31de0` | `CONTROL_OR_RECEIPT_ONLY` | 2026-10-23 | Prepare Browser Pyat HQ R86/R8 read-only succession and sourcefree R03 draft |
| `agent/browser-pyat-r121-c5-content-admission-use-r1` | `8cc9174ba0b2` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-25 | Issue exact retained position-cloud preimage retrieval after R121 |
| `agent/browser-pyat-r123-retained-position-cloud-preimage-r1` | `fd4a1c88d4d1` | `DOCUMENTED_NO_DECISION` | 2026-10-25 | R123: bounded retained P-cloud preimage retrieval, precise missing joint, Route B artifact |
| `agent/browser-pyat-r56-r00-independent-policy-r1` | `6d95a78bf6b7` | `CONTROL_OR_RECEIPT_ONLY` | 2026-10-22 | policy(R56-R00P): freeze successor r2 lawful renaming and linked-coverage correction |
| `agent/browser-pyat-r61-recurrence-substantive-contract-adjudication-r1` | `b733b9eb685a` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-23 | Bank user-confirmed bounded empirical-social recurrence intent; preserve pending R01/R03 c |
| `agent/browser-pyat-r98-grounding-and-treatment-r1` | `d29a9db26821` | `DOCUMENTED_NO_DECISION` | 2026-10-25 | Narrow R98 first empirical source to Afro R5 contextual Q86 and preserve GT2 structural ce |
| `agent/c02e-b5-mandatory-ingress-6b98a6e` | `20213bef82de` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-11 | C02E: mandatory B5 boundary candidate and test-only patch overlay |
| `agent/c02f-executed-b5-bypass-72f2612` | `6f5c2ab92524` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-11 | C02F: executed B5 bypass court — fix C02E fixture, run 29-case UNPATCHED/PATCHED/positive  |
| `agent/c02g-producer-trust-90a6a1f` | `83a9208e9f9a` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-11 | C02G: issuer verification candidate + 34-case court — OWNER_ISSUER_HOLD, no competent issu |
| `agent/c02h-separated-principal-0e01de5` | `82309fe17c70` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-12 | C02H: separate-principal B5 producer authentication demo — RSA issuer/verifier separation, |
| `agent/candidate-pyat-hq-20261021-max-strict-accession-r1` | `ec27ec4a14c7` | `CONTROL_OR_RECEIPT_ONLY` | 2026-10-21 | Sorok rev28 atomic R29P R29M returns, R30G material mechanism and R30A first neighbor sess |
| `agent/codex-hq-autonomous-orchestrator-program-20261022-r1` | `02a09b6a95d5` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-22 | Document synchronized Codex-HQ/OpenCode autonomous orchestration implementation program |
| `agent/codex-pyat-r59-full-hq-accession-eligibility-r1` | `e616b59dba77` | `CONTROL_OR_RECEIPT_ONLY` | 2026-10-23 | docs(R59): submit bounded whole-machine accession supplement for independent review |
| `agent/codex-pyat-r61-hq-checkpoint-r1` | `fdf5dc875c11` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-28 | Deliver Browser HQ SRC04 architecture and execution economy evidence packet |
| `agent/codex-pyat-r61-native-flight-director-r1` | `597198668bea` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-27 | R157 record independent acceptance and bounded parent return |
| `agent/codex-pyat-r61-r01-r7-retained-owner-repair-r1` | `813775c07f08` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-23 | R61-R01-R8: attach semantic binding return and evidence |
| `agent/codex-pyat-r61-r08-r7-canonical-cache-repair-r1` | `be1133391d91` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-23 | R61-R08-R8: bank bounded correction return and witness |
| `agent/coord-postastra-r3-parallel-wave-20261014-r1` | `0bc344606675` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-14 | HQ297 register 3 returned, seal 3 unstarted amended prompts and K9E exact Python recovery; |
| `agent/documentary-pyat-20261017-last-chat-continuity-and-science-plan-r1` | `9fd9a6d8cb18` | `CONTROL_OR_RECEIPT_ONLY` | 2026-10-18 | docs(pyat): correct Pyat/Sorok domain, Afro R5 PREV3 readiness and F6C actual source blob |
| `agent/opencode-pyat-r100-q86-context-consumer-r1` | `79309093e39d` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-25 | R100: attach retained Q86 context consumer return |
| `agent/opencode-pyat-r107-r06-world-progressive-integration-r1` | `22280a3f43e7` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-25 | R107: attach world progressive integration return |
| `agent/opencode-pyat-r110-r06-progressive-binding-repair-r1` | `359ffcef4c2d` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-25 | R110: attach progressive binding repair return |
| `agent/opencode-pyat-r112-r06-world-consuming-successor-r1` | `849a76de18ef` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-25 | R117: attach model identity repair return |
| `agent/opencode-pyat-r125-representative-route-b-launch-packet-r1` | `979d31366454` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-25 | R126: bind concrete retained LiTS next operation |
| `agent/opencode-pyat-r128-retained-real-native-artifacts-r1` | `be5c76ae6640` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-26 | R129: bind producer authority catalog and reach M1 input |
| `agent/opencode-pyat-r131-exact-native-support-m1-replay-r1` | `d933411889db` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-26 | R132: compose actual native smoke and bank source authority decision |
| `agent/opencode-pyat-r135-real-source-production-binding-r1` | `98612c6d511d` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-26 | R137: repair exact production binding and repeated-topology positive |
| `agent/opencode-pyat-r140-predecode-discovery-transport-r1` | `ccf97c89d276` | `DOCUMENTED_NO_DECISION` | 2026-10-26 | R140: add predecode source-read and external-authority discovery transport |
| `agent/opencode-pyat-r141-query-authority-scope-repair-r1` | `44e7ace44d9e` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-26 | R141: complete exact external query authority scope binding |
| `agent/opencode-pyat-r145-current-source-package-binding-r1` | `8d4801e850ca` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-26 | R145: bind metadata-only current source packages and full row accounting |
| `agent/opencode-pyat-r146-all35-existing-source-bindings-r1` | `e62b2447f042` | `DOCUMENTED_NO_DECISION` | 2026-10-26 | R146: reuse existing source bindings across all35 |
| `agent/opencode-pyat-r147-all35-current-metadata-r1` | `3801f743c506` | `DOCUMENTED_NO_DECISION` | 2026-10-26 | R147: consume all35 current metadata and reconcile historical labels |
| `agent/opencode-pyat-r148-all35-complete-metadata-r1` | `29982440dd31` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-26 | R148: complete all35 current metadata and native preparation |
| `agent/opencode-pyat-r150-scientific-native-input-r1` | `2e6ca20d307d` | `DOCUMENTED_NO_DECISION` | 2026-10-26 | R150: wire B49 item authority into native scientific inputs |
| `agent/opencode-pyat-r151-grounded-native-occurrences-r1` | `e3a95fef6eec` | `DOCUMENTED_NO_DECISION` | 2026-10-26 | R151: resolve grounded native occurrences from typed surfaces |
| `agent/opencode-pyat-r153-native-evidence-repair-r1` | `5e5e36354c42` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-26 | R153: hold unsupported WVS native objects and repair evidence binding |
| `agent/opencode-pyat-r154-exact-all35-input-compilation-r1` | `a02adc896264` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-26 | Bank interrupted R154 input compilation for user-requested Browser HQ assessment |
| `agent/opencode-pyat-r61-r01-generic-grammar-r1` | `fea3ca17d941` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-23 | R61-R01-R6: attach retained owner return and evidence |
| `agent/opencode-pyat-r61-r03-total-native-workload-r1` | `c912497b2541` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-24 | R61-R03-R5: attach shared capture validation return |
| `agent/opencode-pyat-r61-r08-evidence-binding-r1` | `d8a7b4005d23` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-23 | R61-R08-R6: bank return, completeness matrix, witness and manifest |
| `agent/opencode-pyat-r61-r09-local-runner-r1` | `4a10c82aa8ba` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-23 | R61-R09 R2: record repair return, witnesses and manifest |
| `agent/opencode-pyat-r61-r09f-facility-preflight-r1` | `2d30d98576ff` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-23 | R61-R09F: report finite existing-facility preflight gap |
| `agent/opencode-pyat-r91-r04-joined-custody-r1` | `e6f7b04c4977` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-24 | R91-R04-R3: attach restored output identity return |
| `agent/opencode-pyat-r91-r05-learned-consumer-r1` | `bc2b5465c8f0` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-24 | R91-R05-R8: bank admitted-original closure return |
| `agent/opencode-pyat-r95-r06-world-consumer-integration-r1` | `b2cfe93cee85` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-24 | R95-R06R4: attach pinned-owner boundary return |
| `agent/opencode-pyat-r97-world-scientific-treatment-recovery-r1` | `c9fb7e69e56d` | `CANDIDATE_RETURNED_NO_HQ_DECISION` | 2026-10-25 | R97: recover world treatments and user choices |
| `agent/pyat-campaign-a-src04-original-c11` | `009a3459b0e2` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | Campaign A1 repair: update portable tests and final return |
| `agent/pyat-campaign-a-src04-review` | `d76bc88ef413` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | Campaign A1 SRC04: focused recheck — PASS scoped after D01/D02 repair |
| `agent/pyat-campaign-b0-src04-consumer-preparation` | `283ac1ecd2f6` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | Campaign B0: record qualified fixture positive and preserve held SRC04 fixture |
| `agent/pyat-d1-src04-observed-tally` | `e1a57513196b` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | D1 repair: record held-authority negative and portable primary replay |
| `agent/pyat-d1-src04-observed-tally-review` | `5f6e03493495` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | D1 SRC04 focused recheck: PASS after held-authority, portability and mutation repairs |
| `agent/pyat-d2-src17-original-c11` | `5b1b9bd5f04f` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | D2 SRC17: record pre-admission metadata-listing deviation |
| `agent/pyat-d2-src17-original-c11-review` | `24f2f3f22f05` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | D2 SRC17 independent review: PASS with recorded process deviation |
| `agent/pyat-final-production-architecture-hq-20261028-r1` | `315251451a6d` | `CONTROL_OR_RECEIPT_ONLY` | 2026-10-28 | Record two-repository branch inventory and exact evidence ceiling |
| `agent/pyat-pre553-r157-afro` | `747dacbf6f4e` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | R157 AFRO: record full-library artifact commit with changed-artifact manifest |
| `agent/pyat-pre553-r157-arab` | `d9ef85f0b007` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | R157 ARAB: publish lane return with full-scope native traces |
| `agent/pyat-pre553-r157-asian` | `c5c3ea8fceb4` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | R157 ASIAN: record full-library artifact commit in receipts and lane return |
| `agent/pyat-pre553-r157-evs` | `9687ff50104f` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | R157 EVS: record full-library artifact commit in receipts and lane return |
| `agent/pyat-pre553-r157-final-review` | `d81bc2c67baf` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | R157 P6: independent all35 source-to-PRE553 review |
| `agent/pyat-pre553-r157-foundation` | `519355ec2215` | `DOCUMENTED_NO_DECISION` | 2026-10-26 | R157 P3: record final reader/key/loader return and manifest |
| `agent/pyat-pre553-r157-gss` | `42b115f25b4a` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | Complete GSS SRC16-SRC23 source configurations and native fixture validation |
| `agent/pyat-pre553-r157-integration` | `056849e23a83` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | R157 P5: final all35 portable index, readiness and native consumer evidence |
| `agent/pyat-pre553-r157-latin` | `f704de41db72` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | R157 LATIN: publish corrected lane return after topology and routing repair |
| `agent/pyat-pre553-r157-lits` | `c868cc731224` | `CONTROL_OR_RECEIPT_ONLY` | 2026-10-27 | Record R157 LITS full-scope artifact commit |
| `agent/pyat-pre553-r157-south-asia` | `3d30a416b93b` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | R157 SOUTH_ASIA: publish lane return with full-scope native traces |
| `agent/pyat-pre553-r157-wvs` | `a8e49e7518e7` | `CONTROL_OR_RECEIPT_ONLY` | 2026-10-27 | Publish WVS SRC33-SRC35 lane return |
| `agent/pyat-r3-incoming-hq-verified-succession-handoff-r1` | `4590740787ac` | `CONTROL_OR_RECEIPT_ONLY` | 2026-10-13 | docs(pyat): index candidate-only verified R3 succession handoff |
| `agent/pyat-source-pre553-r157` | `6be64d7e05f1` | `DOCUMENTED_NO_DECISION` | 2026-10-27 | R157 provide Browser HQ completion handoff and exact proof limits |
| `agent/pyat-src04-actual-carrier-review-20261028` | `751fece9bf86` | `DOCUMENTED_NO_DECISION` | 2026-10-28 | SRC04 carrier focused recheck: pin artifact commit |
| `agent/pyat-src04-cd-native-review-20261028` | `9b66083f89a6` | `DOCUMENTED_NO_DECISION` | 2026-10-28 | SRC04 C/D focused review: pin artifact commit |
| `agent/pyat-src04-consumers-20261028` | `39c713a1396c` | `DOCUMENTED_NO_DECISION` | 2026-10-28 | SRC04 lane D: record observed-provenance repair commit |
| `agent/pyat-src04-field-repair-20261028` | `da23c65d1e21` | `DOCUMENTED_NO_DECISION` | 2026-10-28 | SRC04 lane B: publish versioned iterator-repair successor return |
| `agent/pyat-src04-full-release-20261028` | `303a57851785` | `CONTROL_OR_RECEIPT_ONLY` | 2026-10-28 | Record actual SRC04 native release, replay and measured v3 return |
| `agent/pyat-src04-observed-empirical-20261028` | `b6be405899be` | `CONTROL_OR_RECEIPT_ONLY` | 2026-10-28 | Record measured SRC04 full-frontier execution scale blocker |

## Checkpoint snippets that were not promoted

**114** branches have a checkpoint `disposition`/`grade`/`verdict` snippet but no explicit branch-final HQ decision. Examples include `AUTHOR_CUSTODY_VERIFIED_INDEPENDENT_REVIEW_REQUIRED`, `BANKED_CODE_OBSERVED_NOT_REVIEWED_OR_ACCEPTED`, `INTERRUPTED_UNQUALIFIED_PARTIAL`, `PASS_C5_N5_SOURCE_FREE_CURRENT_PRODUCT__INDEPENDENT_REVIEW_REQUIRED`, and `NOT_INDEPENDENT_AUTHOR_ADJACENT_SELF_REVIEW__NO_ACCEPTANCE_PASS`. These are preserved as custody/review states, not acceptance. The exact 114 branch/checkpoint snippets are in the `checkpoint_signal` field of the 845-row fate ledger; only promoted decisions are in the provenance JSONL.

## Contradictions and mixed outcomes

"Contradictory" here means the surviving evidence points in more than one direction, or a decision is real but its downstream outcome is not the one the label suggests.

| Case | Exact evidence | Why it is contradictory / mixed |
|---|---|---|
| `agent/reviewer-pyat-hq150-c5-n5-r1` | `294d8935ccab`; HQD-151 / HQD-152 | Same reviewer branch is linked to a C5/N5 acceptance and to a C1-03A repair rejection; the two decisions concern different subjects. The fate row must not read the rejection as a rejection of C5/N5. |
| `integration/pyat-hq130-c3-source-free-accepted-r1` | HQD-131; tip `30686b18` | C3 source-free integration accepted, but no exact current PRE-MAIN code blob survives at the same path. Acceptance is historical, not current retention. |
| `integration/pyat-hq139-c1-01-source-free-accepted-r1` | HQD-139; tip `5fafb499` | C1-01 R8 accepted; current `pre553_analytical_composition.py`/test blobs differ. The later C1-02 acceptance is not a retroactive rejection of C1-01. |
| `integration/pyat-hq147-n10e-at17-source-free-accepted-r1` | HQD-147; tip `52e41a41` | N10E AT17 accepted; some exact blobs survive and some are changed. Partial retention cannot be reported as either full merge or no merge. |
| `integration/pyat-hq151-c5-n5-source-free-accepted-r1` | HQD-151; tip `151d3926` | C5/N5 accepted; current `current_gt2_structural_context.py`/test do not survive exactly. |
| `integration/pyat-hq159-c1-03r-source-free-accepted-r1` | HQD-159; tip `9ec7eaff` | C1-03R accepted, while the C1-03 join is explicitly blocked and two residuals are nonblocking. |
| `integration/pyat-hq166-at07-successor-spine-accepted-r1` | HQD-166; tip `069ac61b` | AT07 successor spine accepted; Omega-1 and later C4 work remain held. |
| `integration/pyat-hq168-c1-03-successor-join-accepted-r1` | HQD-168; tip `149c3d26` | C1-03 successor join accepted; C4 execution remains held. |
| `agent/opencode-pyat-hq143-c1-02-witness-pairing-repair-r1` / `integration/pyat-hq145-c1-02-source-free-accepted-r1` | shared tip `bc661188` | Candidate branch is a worker return; the identical commit is also the accepted integration tip. The branch name has no separate HQ decision. |
| `agent/opencode-pyat-hq149-c5-n5-current-structural-context-r1` / `integration/pyat-hq151-c5-n5-source-free-accepted-r1` | shared tip `151d3926` | Same commit, candidate and accepted integration names; retention is not exact. |
| `agent/deepseek-pyat-hq144-n10e-proof-provenance-correction-r1` / `integration/pyat-hq147-n10e-at17-source-free-accepted-r1` | shared tip `52e41a41` | Same commit, control/return and accepted integration names; only partial exact retention. |
| `agent/opencode-pyat-hq183-c4-disputed-claims-recheck-r1` / `agent/opencode-pyat-hq183-ops01-ops04-activation-r1` | shared tip `ef160e97` | One name is held; the other is a control/receipt. A duplicate tip is not two decisions. |
| PR #519 | head `59c9a7a4`; merge ref `7abc24f2`; base `299f41e9`; current PRE-MAIN `8e44ca9c` | The control PR is reviewed/accepted in its own branch, but its base is not current PRE-MAIN and the control law was not merged. |
| E8 family ledger | 602 `HOLD_EXACT_DECISION`, 243 `RETIRE`, 1,040 `PRESERVE_HISTORICAL` | These are family-level functional dispositions, not HQ branch decisions; they neither erase acceptance nor prove code adoption. |

### Accepted ≠ retained

The nine integration acceptances show why the distinction matters:

| Branch | Decision | Current exact retention |
|---|---|---|
| `integration/pyat-hq130-c3-source-free-accepted-r1` | `HQD-2026-09-30-131` | `NO_CODE_BLOB_IN_PREMAIN` |
| `integration/pyat-hq139-c1-01-source-free-accepted-r1` | `HQD-2026-09-30-139` | `NO_CODE_BLOB_IN_PREMAIN` |
| `integration/pyat-hq145-c1-02-source-free-accepted-r1` | `HQD-2026-10-01-145` | `ALL_CODE_BLOBS_EXACT_IN_PREMAIN` |
| `integration/pyat-hq147-n10e-at17-source-free-accepted-r1` | `HQD-2026-10-01-147` | `PARTIAL_CODE_BLOBS_EXACT_IN_PREMAIN` |
| `integration/pyat-hq151-c5-n5-source-free-accepted-r1` | `HQD-2026-10-01-151` | `NO_CODE_BLOB_IN_PREMAIN` |
| `integration/pyat-hq159-c1-03r-source-free-accepted-r1` | `HQD-2026-10-01-159` | `ALL_CODE_BLOBS_EXACT_IN_PREMAIN` |
| `integration/pyat-hq162-c1-03a-source-free-accepted-r1` | `HQD-2026-10-01-162` | `ALL_CODE_BLOBS_EXACT_IN_PREMAIN` |
| `integration/pyat-hq166-at07-successor-spine-accepted-r1` | `HQD-2026-10-01-166` | `NO_CODE_DELTA` |
| `integration/pyat-hq168-c1-03-successor-join-accepted-r1` | `HQD-2026-10-01-168` | `ALL_CODE_BLOBS_EXACT_IN_PREMAIN` |

- `ALL_CODE_BLOBS_EXACT_IN_PREMAIN` means every code path in the branch delta has an exact blob at the same path now. It does not prove the acceptance decision is still current or behaviorally equivalent.
- `NO_CODE_BLOB_IN_PREMAIN` means no exact code blob from that branch delta is present at the same path. The accepted code may have been adapted, superseded or never integrated; the evidence does not choose among those causes.
- `NO_CODE_DELTA` (AT07) means the accepted material was identity data, not a code delta.

### Duplicate tips

Seven tips are shared by more than one name. The important cases are the accepted-integration/candidate pairs:

- `151d39260a80` — `agent/opencode-pyat-hq149-c5-n5-current-structural-context-r1`, `integration/pyat-hq151-c5-n5-source-free-accepted-r1` (CANDIDATE_RETURNED_NO_HQ_DECISION, HQ_ACCEPTED_CODE_INTEGRATION)
- `0c77582bb2bb` — `agent/rabochii-pyat-hq280-wgd-exact-operation-authority-bridge-r1`, `agent/vozhd-pyat-hq280-wgd-operation-binding-dispatch-r1` (DOCUMENTED_NO_DECISION, CONTROL_OR_RECEIPT_ONLY)
- `4037b75bfc65` — `agent/reviewer-pyat-hq280-wgar-independent-source-workload-authority-r1`, `agent/vozhd-pyat-hq280-wga-hostile-intake-r1` (DOCUMENTED_NO_DECISION, CONTROL_OR_RECEIPT_ONLY)
- `d14fefd5e7e6` — `agent/rabochii-pyat-hq280-wge-preoutcome-gt2-e2b-positive-r1`, `agent/vozhd-pyat-hq280-wgd-to-wge-dispatch-r1` (CANDIDATE_RETURNED_NO_HQ_DECISION, CONTROL_OR_RECEIPT_ONLY)
- `bc661188b51e` — `agent/opencode-pyat-hq143-c1-02-witness-pairing-repair-r1`, `integration/pyat-hq145-c1-02-source-free-accepted-r1` (CANDIDATE_RETURNED_NO_HQ_DECISION, HQ_ACCEPTED_CODE_INTEGRATION)
- `ef160e9769f9` — `agent/opencode-pyat-hq183-c4-disputed-claims-recheck-r1`, `agent/opencode-pyat-hq183-ops01-ops04-activation-r1` (HQ_HELD, DOCUMENTED_NO_DECISION)
- `52e41a41e8bc` — `agent/deepseek-pyat-hq144-n10e-proof-provenance-correction-r1`, `integration/pyat-hq147-n10e-at17-source-free-accepted-r1` (CONTROL_OR_RECEIPT_ONLY, HQ_ACCEPTED_CODE_INTEGRATION)

A shared tip means the commit is the same; it does not give the candidate branch name a separate HQ decision. The fate ledger records `same_tip_accepted_integration`.

### E8 statuses are not decisions

E8 reports **602 HOLD_EXACT_DECISION**, **243 RETIRE**, **1,040 PRESERVE_HISTORICAL**, and **0 ADOPT/ADAPT_MINIMAL** at family grain. Those are functional dispositions after a later ledger build, not HQ branch acceptance rates. They must not be used to erase the current acceptance records or to promote a whole family from a file-level decision.

### Pending / overlapping reviews

- E8 names **#564/#565** (PE/S7 map) and **#569/#570/#571** (C3/R9, P41/R08, F7/P07) as pending. **#575–#579** were not found in the frozen roster or PRE-MAIN read cut.
- The GitHub issue/PR API returns `403 Resource not accessible by personal access token`; this reconciliation cannot verify issue state, assignees, comments or current PR head beyond Git refs.
- No worker was relaunched and no pending review was pre-empted. Treat the branch-local returns as evidence inputs, not as acceptance.

## What HQ still has to decide

1. For each of the 472 candidate returns without an HQ disposition: accept, reject, hold or retire at a named grain, or explicitly leave the branch as historical evidence.
2. For each acceptance without exact PRE-MAIN retention: decide whether the current code is a lawful successor, an unmerged acceptance, or a stale decision.
3. For the 132 documented-only and 90 control/receipt branches: identify whether a decision exists in an issue/comment not present in Git, or declare the branch evidentiary only.
4. For the 114 checkpoint-snippet branches: decide whether the snippet is a real HQ disposition or only an intake state.
5. Resolve the duplicate-tip candidate/integration pairs without inventing a second decision.
