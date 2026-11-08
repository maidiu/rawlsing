# Source → existing pre-553: evidence assessment and finite correction

**Prepared by the existing Codex HQ from exact primary artifacts. This is not an independently authored Browser HQ endorsement, and does not grant execution or adoption.** The heartbeat remains paused and workers remain stopped. The prior goal turn paused the heartbeat as explicitly requested; that changed automation state. This turn is progress: it recovered materially broader prior evidence, checked the real entrypoints and replayed the saved package checks. No raw survey files or respondent records were read by this assessment.

## Findings that change the next action

1. **The user's reuse concern is substantiated.** H48 already contains an item index for **all 18,276 items**, not only the 4,460 in the B49 subset. Its referenced primary full-question relation CSV is present in Git and its SHA matches the old evidence manifest. **18,250 original items have exact relation-ID joins**; their primary rows contain populated manual semantic-role/topology fields. The 26 unmatched explicit IDs remain identifiable. These are prior governed facts/interpretations with their original limits, not automatic current adoption or response-read permission.
2. The actual P2 phase-0 CSV is also present locally, hash-verified, with all **18,276** implementation IDs, question text, source variables, dispositions, response-binding states and source-authority references. It was unnecessary to describe those fields as globally unknown merely because R154 did not import them.
3. **33 waves' current header and codebook variable-name sets match exactly.** All **538 physical-only and 401 codebook-only entries are confined to two waves**: SRC25 Latinobarómetro 2011 (244/244) and SRC26 Latinobarómetro 2024 (294/157). Those need explicit mapping/edition classification, not a blanket all35 naming investigation. Examples include physical `P11ST.A` versus codebook `P11ST_A` in 2011. Such similarities are candidates to verify, not permission for an implicit punctuation/casefold join.
4. EVS 1999/2008 metadata encoding is **already qualified** in the current decoder's exact-SHA compatibility allowlist: their current hashes map to `latin1`. The new source-read wrapper does not pass an encoding argument to the decoder. This is a specific transport/configuration gap. Four LiTS hashes also have allowlist entries, but this assessment does not establish that all four need an override; default metadata reads succeeded for them.
5. **The R154 workload builder is a stub.** `r154_load.build_native_workload()` raises with a pending grant and also raises unconditionally on its other path. Supplying a permission would not make this function build a workload. The loader builds identity and selected-rule containers, not a governed projection or executable workload.
6. **The generic preimage adapter still constructs a synthetic universe.** At the accepted candidate cut, `materialize_native_preimages()` hardcodes `country_geography="ZZ"`, `sampling_geography="ZZ-SYNTHETIC"`, `target_population_and_sample_frame="SYNTHETIC_SOURCEFREE"`, and `sampling_design_regime="TEST_ONLY"`. Externally supplied authority snapshots do not replace those fields. This is a real production-binding gap if this helper is chosen; it is not a missing survey definition. The existing `GovernedC11Projection`/source-backed facade accepts genuine caller-owned universe and slot definitions and must be reused as the owner.
7. R154's **five saved tests pass**, but prove metadata counts, identity/package construction, cold database reload and refusal. They do not contain a successful native projection/workload construction from the full source preparation. A passing test that expects `CURRENT_SOURCE_READ_GRANT_REQUIRED` does not prove the preparation behind that gate is implemented.
8. The final banked snapshot differs from its stale author prose. Its database has **178 DONE + 35 DONE_WITH_EXACT_UNRESOLVED_FIELDS**, **zero BLOCKED**, 43 `sourceprep_artifacts` locator rows and no FIELD_FORGE requirement row. The report still describes 108 DONE/70 BLOCKED and FF. The compiler marks each WORKLOAD/PACKAGE DONE when it writes an identity/B49 container; it marks sourceprep reuse SATISFIED on creating locator rows. Those labels are not evidence of actual native production use. Preserve the interrupted report; correct the assessment rather than trusting either set of labels.

## 1. Real input boundary

The immediate boundary is a source file, a source-specific preparation/configuration, and a configured existing pre-553 producer. It is not a requirement that every downstream consumer be accepted before inputs can be prepared.

| Stage | Existing owner and actual necessary inputs | Not a prerequisite at this stage |
|---|---|---|
| Physical metadata preparation | Current header/codebook receipts: exact SHA, format, column ordinal/name/type, value labels, missing declarations, MR/layout metadata and reader configuration | Field Forge, learned disposition, scientific frontier, response grant for a metadata-only operation already authorized |
| Response decoding when permitted | `pre553_source_read_admission.decode_with_source_read_permission(source_path, request, resolver)` → `pre553_physical_decoder.decode_sav/decode_dta`; exact SHA/format/host/purpose/use/current decision, exact allowed decoder configuration | UniversalGrammar `SourceInventory` and scientific-role certification are not arguments of the decoder |
| Source semantic projection | `GovernedC11Projection` + `PhysicalSourceIncidence` or `ExactPhysicalCellStream` → `build_validated_source_backed_c11_release` / `build_source_backed_c11_repository`; exact source/release/universe, row/respondent binding rule, question-variable bindings, response/coordinate/optional weight slots, routing and scoped authority/replay refs | A full estate frontier or FF acceptance; weights are conditional, not required to fabricate unit weights for raw-sample analysis |
| Native empirical workload | Actual projection + `RuntimeObjectCatalog`, exact I03 request or separately prepared I05 discovery, applicable original-U/expected-frontier roots, descriptor/current decision → issued workload/Route B/native executor | New empirical engine; automatic all-pairs; a discovery inventory for a query-only operation; downstream transformation acceptance |
| Pre-553 analytical/learned products where requested | Existing analytical/learned owners consume empirical results with family/validation contracts where constitutive | Not part of source/header preparation merely because the larger project eventually needs them |

`PhysicalSourceAuthorityProjection(candidate_builder=...)` and the governed C11 facade are already typed integration seams. Native respondent records and value witnesses are produced after permitted source decoding; a prepared callable/config can exist before those values are read. A source-preparation package must not fabricate respondent records to look complete.

`Occurrence`/`SourceInventory` belongs to the selected symbolic grammar/planner path. It is not a universal predecode gate for every scalar, text, continuous, coordinate or source-backed C11 input. Its finite domain restrictions must not be imposed on all raw physical columns.

## 2. Reusable work that was already done

### Full item and semantic inputs

- H48 `359ddabc89d78ceb4c8fa45561588ee4cad7dd11:.../evidence/original_item_authority_candidates.json.gz`: **18,276** exact original IDs and source-wave-variable keys, pointers to P2/deep/manual/overlays/O06/context/full-relation evidence. Grade remains `EXACT_COORDINATE_CANDIDATES_ONLY_NOT_ADOPTION` where recorded.
- Primary relation CSV `9561723cfe0932869e781f2be27e9c80b050ad7a:data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv`: 18,518 rows including excluded/out-of-scope rows. Use exact P2 IDs for the 18,250 matched original items, not a blind import of every row. Manual response topology includes scalar, nominal/ordinal/continuous context, binary and multiselect; normalization often explicitly preserves native categories without signing. This is more specific than blanket “meaning unknown.”
- Local hash-verified P2 file `/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_Authority_Document_Archive_2026-08-24/documents/source-and-question-authority/08_P2_PHASE0/Rawlsing_P2_Phase0_Question_Node_Skeleton_v1.csv`; SHA `d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6`, 18,276 rows. Example GSS2024 `abany` already has exact question identity/text, response classes and a GSS2024 semantic-overlay reference.
- Exact full-record relation matches are **not** all unrestricted scientific use. Preserve `does_not_measure`, forbidden inference, direction certification, response/routing status and historical/candidate/adopted scope. Raw nominal category use is distinct from directional signing.

### Existing source-preparation and execution components

- Current decoder, its allowlist and immutable-byte custody; current source-local universe admission; source-backed C11 projection/facade/repository; catalog and Route B/I03/I05/Batch/issued-workload owners. These are the functional owners, not new code to reimplement.
- Existing LiTS-I and WVS7 materializers under `rawlsing_next/runtime/ee_p2x/` supply scoped source-specific examples and explicit input bindings. Their old bounded question selections are not all35 configurations and must not become the current target scope by convenience.
- R154 metadata/store/reconciliation contains useful current physical facts. B49's 4,460 records remain useful but cannot replace the full index. The 38 typed surfaces are a representation subset, not the complete semantic inventory.

### Exact routing limitation

The H48 index records O06 routing states, including truly unresolved and conditional cases. For example GSS2024 has 800 `SOURCE_ROUTING_UNRESOLVED` index rows plus explicit ballot, respondent-answer, multi-condition and split-sample cases; LiTS-I has 485 `UNCONDITIONAL_SOURCE_PROVEN` rows and substantial explicit conditional groups. Do not turn conditional/unknown into “everyone was asked.” Conversely, do not withhold every unconditional item because another source item is conditional.

The exact O06 archive locator in H48 was not present at its recorded local path during this assessment. This is a **specific retrieval limitation**, not global absence: its index states are recoverable, other source packets/full relation data exist, and the next worker must follow exact source/manual references to retrieve actual route expressions for operations that require them. Do not claim this assessment recovered all executable skip predicates.

## 3. Per-source remaining work

`PER_SOURCE_READINESS.csv` supplies all35 counts; `PER_SOURCE_GAPS.json` contains exact physical-only/codebook-only lists, per-source prior routing/response-binding state counts, primary field coverage and the exact 26 unmatched implementation IDs. These distinguish **unconsumed existing input** from a genuinely absent fact. They are not 35 blanket permission demands.

| ID | Wave | Prior item records | Physical / codebook | Physical-only / codebook-only |
|---|---|---:|---:|---:|
| SRC01 | Afrobarometer R1 | 144 | 144 / 144 | 0 / 0 |
| SRC02 | Afrobarometer R5 | 348 | 348 / 348 | 0 / 0 |
| SRC03 | Afrobarometer R9 | 421 | 421 / 421 | 0 / 0 |
| SRC04 | Arab Barometer I | 181 | 181 / 181 | 0 / 0 |
| SRC05 | Arab Barometer II | 468 | 468 / 468 | 0 / 0 |
| SRC06 | Arab Barometer V | 359 | 359 / 359 | 0 / 0 |
| SRC07 | Arab Barometer VIII | 690 | 690 / 690 | 0 / 0 |
| SRC08 | Asian Barometer W1 | 217 | 217 / 217 | 0 / 0 |
| SRC09 | Asian Barometer W4 | 289 | 289 / 289 | 0 / 0 |
| SRC10 | Asian Barometer W5 | 308 | 308 / 308 | 0 / 0 |
| SRC11 | EVS 1981 | 370 | 370 / 370 | 0 / 0 |
| SRC12 | EVS 1990 | 390 | 390 / 390 | 0 / 0 |
| SRC13 | EVS 1999 | 513 | 513 / 513 | 0 / 0 |
| SRC14 | EVS 2008 | 477 | 477 / 477 | 0 / 0 |
| SRC15 | EVS 2017 | 474 | 474 / 474 | 0 / 0 |
| SRC16 | GSS 1972 | 216 | 216 / 216 | 0 / 0 |
| SRC17 | GSS 1973 | 339 | 339 / 339 | 0 / 0 |
| SRC18 | GSS 1984 | 675 | 675 / 675 | 0 / 0 |
| SRC19 | GSS 1993 | 752 | 752 / 752 | 0 / 0 |
| SRC20 | GSS 2002 | 1119 | 1119 / 1119 | 0 / 0 |
| SRC21 | GSS 2010 | 922 | 922 / 922 | 0 / 0 |
| SRC22 | GSS 2016 | 1018 | 1018 / 1018 | 0 / 0 |
| SRC23 | GSS 2024 | 980 | 980 / 980 | 0 / 0 |
| SRC24 | Latinobarómetro 1995 | 203 | 203 / 203 | 0 / 0 |
| SRC25 | Latinobarómetro 2011 | 414 | 414 / 414 | 244 / 244 |
| SRC26 | Latinobarómetro 2024 | 195 | 332 / 195 | 294 / 157 |
| SRC27 | LiTS 2006 | 1198 | 1198 / 1198 | 0 / 0 |
| SRC28 | LiTS II | 627 | 627 / 627 | 0 / 0 |
| SRC29 | LiTS III | 1290 | 1290 / 1290 | 0 / 0 |
| SRC30 | LiTS IV | 1319 | 1319 / 1319 | 0 / 0 |
| SRC31 | South Asia W1 | 68 | 68 / 68 | 0 / 0 |
| SRC32 | South Asia W2 | 73 | 73 / 73 | 0 / 0 |
| SRC33 | WVS W1 | 188 | 188 / 188 | 0 / 0 |
| SRC34 | WVS W4 | 418 | 418 / 418 | 0 / 0 |
| SRC35 | WVS W7 | 613 | 613 / 613 | 0 / 0 |

Concrete remaining tasks:

- **All35:** consume the complete prior row evidence into the actual chosen projection/config fields. R154's current container does not do this. Report source/item/required field/existing evidence/decision only for cells that cannot be populated after that join. Do not re-author all question meanings.
- **SRC25/SRC26 only:** resolve the listed column-coordinate mismatches by exact source preparation/alias or edition evidence. Do not equate `P` and `Q`, dots/underscores or upper/lowercase silently. Preserve physical-only administrative/extra fields explicitly when legitimately outside measurement; do not drop them from the source-column ledger.
- **SRC13/SRC14:** transport their existing exact-hash `latin1` configuration through the permitted source-read path. No new encoding research is needed for these hashes. The metadata retries agree with the current allowlist.
- **26 exact unmatched relation IDs:** retain source-specific primary/manual/P2 evidence and the missing-ID witness. Do not let failure of a full-relation join erase the original item or promote a different row. Resolve the exact identity relation only if the required operation needs that relation authority.
- **Actual unresolved or conditional routing/unit/form fields:** retrieve the specific existing source packet/route expression; use the source scope's native subject/row rule. Only genuinely unretrieved premises block their dependent operations. Header storage types alone cannot prove a skip predicate, respondent universe, household membership or material-position interpretation.
- **Shared code:** implement the missing connection from prepared configuration to the current native projection/workload. Do not attribute the R154 unconditional refusal, synthetic universe construction or omitted encoding argument to missing human source knowledge.

This assessment does not establish that every undocumented current scientific choice is settled. It establishes that the previous blanket-null diagnosis was not justified, and gives exact evidence and bounded residuals to finish the actual source-input composition.

## 4. Keep, correct, retire

| Material | Disposition |
|---|---|
| R154 current physical receipts, header/codebook tables, exact SHA and reconciliation lists | KEEP as current factual inputs; preserve original metadata-only scope |
| Existing P2/H48/full relation/manual/route and qualified source-specific packages | REUSE at exact scope; expand beyond partial B49 input before declaring a gap |
| SQLite indexed form and per-source exports | KEEP practical form; record exact referenced-code dependencies; no more parallel wrapper layers |
| `sourceprep_artifacts` and DONE/SATISFIED labels | CORRECT: locators/hashes are not actual consumer-use evidence; require call/result and input coverage |
| R154 `build_native_workload` | REPLACE STUB WITH REAL WIRING within the existing owner interface; passing a grant does not fix it |
| Generic adapter synthetic universe/defaults | DO NOT USE AS REAL SOURCE BINDING; reuse source-backed facade with grounded universe/coordinate/slot config or narrowly parameterize the existing helper |
| R145–R153 renderers and intermediate pending JSON | RETAIN historical evidence; STOP making them live pipeline layers if superseded by one canonical source config |
| FieldForge acceptance and population/causal/temporal/new-signing requirements as universal sourceprep gates | REMOVE from this task; apply only to their actual governed operations |
| Blanket source-grant request as explanation for incomplete metadata/configuration | REMOVE as a preparation blocker; keep a precise separate response-execution gate |
| Private `.r61/.../pre553_inherited_source_rules.py` loader dependency | PIN/RESOLVE from immutable Git or a declared supported module; cold-copying a DB inside the same worktree does not prove a portable fresh checkout |

R152's rejection of unsupported administration/form/unit/topology assertions remains valid. It does not justify inventing replacements or concluding those facts cannot be recovered from the full prior work.

## 5. Finite executable correction for one existing worker

The machine-readable contract is `CORRECTION_TASKS.json`. No worker is launched by this assessment.

1. **Recover the full preparation inputs once.** Use the exact H48 compressed index, primary relation CSV and verified P2 path above. Join by implementation ID/fingerprint and explicit source-wave-variable coordinate; retain all18,276 items and26 unmatched relation IDs. Output one evidence-aware table, not a new prose census. DONE: every source item accounted and actual field values/grades available to the adapter.
2. **Resolve only actual column differences.** Process SRC25 and SRC26's exact lists, one mapping/edition fact at a time. Other33 source name sets are already matched. DONE: every physical/codebook column is mapped or has a specific reason and active-use consequence; no implicit normalization.
3. **Compile source-specific configuration, one wave fully at a time.** Load full existing meanings/normalization/routing/unit/layout evidence into the actual facade's question/response/coordinate/optional weight/universe/authority inputs. Preserve typed unknowns only for genuinely missing facts. Keep target and conditioner ownership separate. Use existing materializer rules within their lawful scope; complete new compatibility glue only. DONE: current native constructors accept the prepared source configuration and exact dependent residuals are exposed; no synthetic defaults.
4. **Connect the actual producer and decoder configuration.** Reuse the existing validated C11 facade and catalog/issued-workload owners. Implement the real R154 builder/factory connection and exact allowed EVS encoding transport. The factory creates respondent/value-dependent fields after a permitted decode. DONE: actual calls reach the existing native owner; an absent runtime permission refuses at its boundary, not an unconditional unimplemented-function path.
5. **Verify and deliver one library.** Cold-load from declared code/data dependencies; verify full item/column conservation, exact type/missing/route bindings, wrong-source/config refusal and source-backed owner acceptance. Use existing source-free fixtures only to verify mechanical wiring where permitted, labelled as such; do not claim original-source science. Deliver runnable source-config → pre-553 commands and exact remaining response-run authorization. No FieldForge work or second engine.

Steps are finite deliverables/checks, not five more investigative commissions. A missing file/decision produces one exact acquisition request and blocks only dependent work. Reuse completed metadata checks. Do not retry old retained-response demonstrations or keep relaunching after two objects.

## 6. Completion and the next actual run

### Prepared source inputs are complete only if

- Every source file identity/reader configuration and physical column is reconciled against the chosen source config.
- Existing item semantics/coding/missing/routing/unit/topology facts are actually consumed into the current producer fields, with exact limits and operation-level residuals, rather than merely listed as artifact paths.
- A native source-preparation loader/factory has a real successful construction path, uses no synthetic metadata/default authority and declares all code dependencies.
- The source-backed C11/native owner validators accept the declared prepared scope; unresolved optional lanes are not silently converted into supported results.
- The output is one reproducible input library/configuration and concrete command/API arguments. A notebook, metadata renderer, DONE row or permission refusal is not sufficient.

### Next actual source run, separately authorized

The next operation after preparation is the existing source-read wrapper with the exact current source identity, configured reader, host/purpose/use and applicable resolver; then invoke the prepared projection builder and native C11/RouteB/I03 or I05 owner at the frozen scope. This assessment does not issue those decisions, choose a historical dataset as a new target, or claim an original source run was performed. Response-execution permission does not substitute for technical source readiness; technical preparation does not manufacture legal/scientific permission.

### Evidence audit of this assessment

- Read R155 report/evidence index and the referenced pasted goal.
- Verified all90 banked R154 manifest entries against immutable Git objects; the snapshot identity is unchanged.
- Inspected current accepted owners and actual R154 compiler/loader/tests rather than accepting the report's claims.
- Verified H48 full index and primary relation bytes; full source match and per-source counts generated by `audit_inputs.py` from immutable inputs and the read-only snapshot DB.
- Verified the locally present full P2 file hash; recorded exact O06 archive retrieval limitation.
- Replayed saved R154 metadata-only tests: **5 passed**, no source decode, with JUnit evidence. They prove their narrow assertions and do not prove native pipeline readiness.
- All35 per-source readiness/gap rows retained. No source responses, old response checkpoints, new model/provider, workers or automation restarts.

**External independent Browser HQ acceptance has not occurred in this chat.** This assessment supplies primary evidence and a finite correction for that review; it must not be described as a separate Browser review of the same HQ's work.
