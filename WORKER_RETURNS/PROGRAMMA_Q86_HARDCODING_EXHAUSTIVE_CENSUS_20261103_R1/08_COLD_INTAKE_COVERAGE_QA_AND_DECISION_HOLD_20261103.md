# PROGRAMMA Q86-CENSUS — cold intake, accounting QA and decision HOLD
**Date:** 2026-11-03. **Type:** append-only S0–S1 intake verification, not a scientifically issuing authority, not the mandated independent hostile acceptance review, and not S2/S3. **Decision:** HOLD; no remediation selection. Preserve upstream worker return unchanged.

## Immutable source and current-ref verification
- Private repository: `maidiu/rawlsing`.
- Protected PRE-MAIN `integration/pre-main-reconciliation-r1` remained **identical** to `773bb412a820949f13a7178b6671327cd56a3bf1` when checked in this intake.
- Worker `research/programma-q86-hardcoding-exhaustive-census-20261103-r1` remained **identical** to `70574505dc3e2100cbe09fd5af1f65b811dcd1cb`, 16 commits strictly ahead of that protected base; compare listed exactly nine added paths (the commission plus eight required return artifacts).
- GF1 branch `agent/userdirect-pyat-20261016-r17-gf1-generic-native-pair-relation-r1` remained at `9f4a23cef1482e0a81afb1e7a65df90879931465`.
- R100 branch `agent/opencode-pyat-r100-q86-context-consumer-r1` remained at `79309093e39d363b760436df2a06f4009c81c789`.
- This intake branch was created from the exact worker return. No PRE-MAIN, worker return, original data, source science or production code was edited.

## Existing source files: canonical evidence packet
The prior commission and its seven associated evidence files are unchanged. Full path prefix: `WORKER_RETURNS/PROGRAMMA_Q86_HARDCODING_EXHAUSTIVE_CENSUS_20261103_R1/`.
- `00_RETURN.md` — explicit `INCOMPLETE_CENSUS` finding and source-graded answer.
- `01_RAW_OCCURRENCE_REGISTRY.jsonl` — raw token occurrences, not 2,466 independent defects.
- `02_INDIRECT_DEPENDENCY_AND_CONSUMER_REGISTRY.jsonl` — 16 scoped semantic/dependency hypotheses and receipts, not 16 independently executed chains.
- `03_BRANCH_BLOB_SOURCE_MANIFEST.jsonl` — four tree **count** inventories, a selected-blob scan log and ref name index. Not an all-branch content census.
- `04_CANARY_QUARANTINE_DISPOSITION.md` — provisional keep/quarantine/owner-hold recommendations, no actual rewrite.
- `05_PRIOR_ERADICATION_CAMPAIGN_FATE.md` — R2 adopted architecture versus source-specific canary versus GF1/R100 distinction.
- `06_GREP_OR_AST_REPRODUCER_AND_TRIPWIRE.md` — local reproduction script and tripwire contract, explicitly unrun.
- `07_HARD_NEGATIVE_FALSIFIERS_AND_HQ_HANDOFF.md` — F-A/F-B/F-C, independent review and owner-bound receiving gates, explicitly unrun.

## Independent intake accounting QA (directly parsed GitHub blobs)
1. JSONL parse: **2,466/2,466** raw rows valid; **16/16** semantic rows valid; **3,201/3,201** manifest rows valid; no parsing errors observed.
2. Raw occurrence identifiers: **2,466 distinct IDs** and no duplicate `blob + line + column + needle` composite in the recorded set. Sum of manifest scanned-blob hit counts = **2,466**, agreeing with raw rows.
3. Raw occurrences: **1,705 CODE** rows and **761 TEST** rows; **29 matched paths**. Categories in raw `classification`: 1,628 `SOURCE_SPECIFIC_PRODUCER_OR_CONSUMER_NEEDS_REACHABILITY`; 761 `TEST_ONLY`; 77 `SOURCE_SPECIFIC_OR_GENERIC_REQUIRES_SEMANTIC_TRACE`. These are **automatic/provisional labels**, not individually adjudicated faults. All 2,466 raw entries give PRE-MAIN as the primary commit; the two original35 P1 blobs had no selected-token hits.
4. `first_downstream_consumer` on raw entries: **1,812 `UNKNOWN_PENDING_TRACE`**, **654 `TEST_CALLER`**. Hence the raw registry does **not** establish consumer-level reachability for its production-row majority.
5. Manifest composition reconciles exactly: **3,158 `HEAD_REF_INDEX_ONLY` + 37 `SCANNED_BLOB` + 4 `COMPLETE_TREE_PATH_INDEX_ONLY` + 1 `TREE_INVENTORY_ONLY` + 1 `ALL_HEAD_REF_LIST_ONLY` = 3,201**.
6. Of 37 content-scanned blobs, **35** belong to the PRE-MAIN priority-code/test scope, **2** to original35 P1. PRE-MAIN contains **8,128 tracked blobs** in its recorded path inventory, so **8,093 PRE-MAIN blobs had no evidenced content inspection**. The alternative tree counts (SAT-R 8,184; P1 8,107; Sorok W8-R 8,225) were **not** corresponding all-tree content scans; 3,158 branch names are not scanned branch trees.
7. The manifest has only **37 per-file `SCANNED_BLOB` records**, not one path record for every file in each tree. The previously queried remote complete path-index coverage cannot be independently rebuilt from this committed manifest; retain the exact `PATH_INDEX_ONLY` ceiling.
8. All **16/16** indirect dependency records state `tests_executed_by_this_worker: NOT_RUN`; GF1's location in row Q86-S13 is `UNKNOWN`; author-reported GF1/R100 execution must not be upgraded to independent reproduction.

### Two provenance/logging corrections to make before qualified acceptance
- `01` entries' `tree_sha` values equal their `commit` values (`773bb412...`) on **all 2,466 rows**, and sampled `03` records repeat the same pattern. The field is serving as a *commit/ref cut*, **not an independently verified Git tree-object SHA**. No actual tree-object ID was retrieved during this intake. Preserve underlying hashes but rename or derive a verified tree ID in the eventual authoritative census.
- `03`'s introductory `TREE_INVENTORY_ONLY.scope` says `12 priority rawlsing_next modules actually scanned`, whereas its `SCANNED_BLOB` rows number **35 PRE-MAIN blobs plus two P1 blobs**. Interpret “12” as an informal priority-subset description only, not the count of inspected files. Reconcile the metadata when the local scan is run.

## Source-checked static findings, not executable findings
- `rawlsing_next/field_forge_conditional_support.py` exact blob `a70decb20747d84cbcbe27d1280babc6de88ef33`: lines 34–35 bind Q86B/Q86A as module constants; `_query_component_material` (125–191) compares query target refs/order/domains to passed refs; `produce_exact_conditional_support_profile` (467–578) builds roles at 520–529 using the module constants; `ExactConditionalSupportProfile.semantic_projection` (415–457) repeats them. **F-A source-label mismatch is testable and plausible, but not executed here.**
- `gt12_c_to_d_relation_bridge.py` blob `ea04ec079e8d60e6e5c7236ec5b54898876be4b3`: validation 58–91 explicitly restricts projected labels to Q86B/Q86A and the frozen risk-set identity. It is an intentional narrow guard, not evidence of general permission.
- `wave1_ff_prev3_relation_admission.py` blob `c5fb675fd6f95cb7dc9e0ad505224803839cc645`: lines 33–44 bind Afrobarometer R5, Q86B→Q86A and 19,210; lines 415–435 label selection `CURRENT_FOR_FROZEN_GT2_CANARY_ONLY`. A valid historical canary is not a current universal sociological source.
- GF1 generic pair source blob `746d669314ddd114ec21d3a35c13c452666863fe` explicitly labels itself `TEST_ONLY`, `UNISSUED`, `NOT ACCEPTED`; its author return at blob `6f37f1a8d51a3aef5908364821ba27f050c39344` reports 44/44 tests, actual named consumer, and specifically says the old specialist Q86 owner labels non-Q86 examples Q86B/Q86A. That provides additional **author-reported** positive evidence for the F-A concern, but does not substitute for independent reproduction.
- R100 author return `b10ebad4c8e5f87d81c847ed2e083d749ed29385` reports 22 passing tests and six P41 receipts from *deliberately requested* retained Q86 CONTEXT, with `world_part=False`, `actor_state=NOT_TOUCHED`, `structural_assertion=None`, and historical nonoperative-current grade. This is not evidence of Q86 automatically selected as a generic world default.
- P1 original35 constructor blob `c8352c5ab0fbc1a817c38d8ef99d64beef628230`: `EligibleItem.stratum_refs=()` at 266; absent stratum specifically holds heterogeneity at 744–754. **Do not merge this separate source/item authority concern into Q86 contamination.**

## All 16 existing semantic records: preserved triage identity, not adoption
| Row | Area | Intake status |
|---|---|---|
| Q86-S01 | FF fixed-label producer | P1 potential misbinding, F-A NOT_RUN |
| Q86-S02 | frozen GT2 admission | bounded canary; preserve |
| Q86-S03 | GT12 C→D | frozen guard; preserve |
| Q86-S04 | GT12 D→M1→M4 | exact source-specific ingress to more generic receiver; selection unknown |
| Q86-S05 | permission translator | CONTEXT only, escalation prohibited |
| Q86-S06 | E2B pinned current binding | source-specific currentness; not generic CURRENT |
| Q86-S07 | E2B harness | TEST/INTEGRATION_ONLY |
| Q86-S08 | generic M1 receiver | non-Q86 caller/selection not verified |
| Q86-S09 | generic M5 currentness/peer prior | downstream selected-world/actor reachability unknown |
| Q86-S10 | N9/N10W progressive fixture | synthetic general candidate, not native original35 success |
| Q86-S11 | GT34 Q69B/Q86A | frozen example |
| Q86-S12 | P1 original35 constructor | separate, no direct Q86 hit |
| Q86-S13 | GF1 generic pair candidate | TEST_ONLY, semantics HOLD, cold review pending |
| Q86-S14 | R100 explicit context reader | author-reported source-specific positive; independent review pending |
| Q86-S15 | Field Forge R2 authority | adopted general conceptual grammar, not generalized physical code |
| Q86-S16 | PRE553 empirical query | general query exists; arbitrary pair route and default selection unproved |

## What is genuinely unclosed; do not record false negatives
- **P0 COVERAGE:** no executable local clone/gitrepo runner available in this session; container Git access to the private repo fails DNS resolution, while connected GitHub reads exact private blobs. No entire tracked-file content census, no all-ref code, test, fixture, archive, non-Python, binary/LFS ledger, no historical `git log -S/-G` or per-commit origin audit. All missing territory is **UNKNOWN / NOT_CONTENT_SCANNED**, not clean.
- **P0 QA:** all 16 dependency rows need exact import/call/selection reconciliation against full source trees; no acceptance of findings as complete. Fix field naming/tree manifest scope and first-consumer UNKNOWNs.
- **P1 F-A:** authorized sourcefree alternate pair through the frozen FF producer; inspect roles and guard rejection with immutable outputs.
- **P1 F-B:** first actual selected-world reader must not choose Q86 merely because retained object exists. None independently demonstrated here.
- **P1 F-C:** withdraw Q86 transport and prove unrelated legitimate source route continues without inherited labels/19,210 risk.
- **P1 GF1:** separate hostile code/first-consumer review and competent generic FIELD FORGE semantics owner; no duplicate engine order until qualified.
- **P1 R100:** separate independent reproduction of historical context-only P41 receipt chain and negative permission/no-world/no-actor assertions.
- **P1 historical fate:** primary scope of the user's earlier removal campaign, per-file introduction/reintroduction chronology and past acceptance custody are still **UNKNOWN**; R2 architecture success is not proof codebase generality and retained Q86 examples are not proof campaign failure.
- **Receiving discipline:** existing PROGRAMMA Pyat S02/S06/S09/S10 and SAT-R function-parity/current-seam registers are receiving coordinates, **not updated by this intake**. Sorok receives only a demonstrated actor-edge dependency. No autonomous launch, receiving adoption or rewrite has occurred.

## Decision boundary
What is now tracked: every **already reported** finding and absence, exact recorded source cuts, integrity QA results and missing proof obligations. What is **not** tracked exhaustively: every source file/blob/ref or actual first consumer across the repository. **Status remains INCOMPLETE_CENSUS; F-A/B/C NOT_RUN; GENERIC_NATIVE_SEMANTICS_HOLD; INDEPENDENT_ACCEPTANCE_NOT_RUN.** Do not select a fix or declare eradication complete from this log.
