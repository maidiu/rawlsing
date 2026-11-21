# KUDA — post-VOZHD DAG reconstruction: stranded, unreceived, incompletely integrated code

**Revision KUDA-R4 — 2026-11-21. Scope corrected by the user.** **This is NOT an archaeological inventory of pre-FORGE DDM/V550–V558 legacy.** KUDA contains code written as part of the **August-and-after post-VOZHD, DVA/TRII/CHETIRI/PYAT/VOZDH-VERKHOVOD DAG rework**, where a potentially valid implementation or material code improvement was written but stranded, unreceived, unintegrated, wrong-versioned, or insufficiently recognized. Modern `pre553_`/current C11/S01–S11 code and explicit post-rework worker branches qualify. A legacy V550 name in a DAG parity document does **not** qualify code from `data/ddm_build_copy`. No new bridge or implementation is commissioned by KUDA.

**Hard exclusion:** Pre-FORGE legacy V542/V550/V550J/V551/V552/V553/V554/V555/V556/V557/V558, historical FFX R2 old DDM, and their questionnaire/storage/temporal/runtime files are not KUDA recoveries. Their history is preserved in [the immutable KUDA-R3 commit](https://github.com/maidiu/rawlsing/blob/f416acd7f752447007b950cfa7d2437adb66cf75/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/KUDA.md), but **R3 is superseded as the active research ledger**. Post-rework references *to* old code do not confer in-scope status unless an actual rewritten-DAG implementation body is inspected.

**Cut and authority:** Examine evidence written before **2026-11-19 ~12:50 America/New_York**, excluding subsequent PRE-MAIN/REMONT/Q014–Q020 ownership dispute delegated to PYAT HQ. Comparison selected PRE-MAIN `5d387a9a8c72c68e6ef87a671d6d486bfd1fc43e`; live operational receiving still requires refreshed source. Branch is **the same G4 repair branch** `agent/pyat-g4-one-time-complete-reconciliation-20261120-r1`. Existing G4 first-look, original machine tables, paired CURRENT_PROGRESS, owner and independent G5 remain controlling. Branch-only source != deployed runtime; author suite != independent review; scoped G5 != four-packet combined receiving; original/native/science/person authority not granted.

**ID preservation:** KUDA R3's out-of-scope and already-integrated IDs remain frozen and *retired from the active ledger* in immutable Git history. Do not reassign old IDs. The active ledger intentionally has noncontiguous stable IDs. KUDA now represents viable post-rework **reclamation candidates**, not all existing code. NEKUDA stores only lesser versions, invalid proofs and competing/unintegrated iterations of these post-rework candidates. All new writes must revise the same two files on the same branch with CAS, comparing live selected code to avoid duplicate implementation.

## Quick recovery queue (these are candidates, not commissions)

| ID | Post-rework code and function | Frozen evidence | Receiving fate at examined cut |
|---|---|---|---|
| `KUDA-001` | S1-B R157-to-current-C11 native/source configuration adapter | S01/S03 | `SCOPED_G5_SOURCEFREE_ACCEPTED__CUMULATIVE_UNMERGED` |
| `KUDA-002` | B49 administered source-rule selection and NativePreimage adaptation | S01/S02 | `ISOLATED_SOURCEFREE__UNADOPTED_AT_PRE_CUT` |
| `KUDA-003` | G50 separately governed operation/fate grammar | S02 | `ISOLATED_SOURCEFREE__UNADOPTED_AT_PRE_CUT` |
| `KUDA-004` | I51 B49+G50 integrated sourcefree operation lowering | S02/S03 | `ISOLATED_SOURCEFREE__NARROW_CONSUMER` |
| `KUDA-017` | F6M separate-source mathematically bounded synthesis | S07 | `POST_REWORK_WORKER_SOURCEFREE_CANDIDATE` |
| `KUDA-018` | F6P post-rework typed bounded-evidence consumer | S07/S10 | `POST_REWORK_WORKER_SOURCEFREE_CANDIDATE` |
| `KUDA-019` | P07 exact comparable-time and as-of semantic selector | S08/S09 | `POST_REWORK_TEST_ONLY_CANDIDATE` |
| `KUDA-026` | I01 sourcefree world→durable learned checkpoint/lifecycle composition | S05/S09 | `POST_REWORK_ISOLATED_INTEGRATION_CANDIDATE` |
| `KUDA-028` | W03/W04 compact C11 event bodies and cold I03/I05 reopening | S03 | `POST_REWORK_UNMERGED_DRAFT__PARTIAL_INDEPENDENT_REVIEW` |
| `KUDA-059` | S1-D independent CURRENT decision-resolver hardening | S02/S03 | `SCOPED_G5_SOURCEFREE_ACCEPTED__UNMERGED_VERSION_DELTA` |
| `KUDA-060` | S2-F exact complete durable empirical I03/I05 result-closure archive | S03/S04/S05 | `SCOPED_G5_SOURCEFREE_ACCEPTED__UNMERGED` |
| `KUDA-061` | S2-G full durable M1→M2→B5 learned lifecycle/cold-world archive | S05/S09/S10 | `SCOPED_INDEPENDENT_G5_PASS__UNMERGED` |
| `KUDA-062` | S1-A race-safe source-to-C11 cache admission | S01/S03 | `POST_REWORK_UNMERGED__G5_HELD` |
| `KUDA-063` | S1-C independently censused pending-operation/fate conservation | S01/S02 | `POST_REWORK_UNMERGED__G5_NOT_VERIFIED` |
| `KUDA-064` | S2-A sealed I02 semantic event-range mutation refusal | S03 | `POST_REWORK_UNMERGED__G5_HELD` |
| `KUDA-065` | S2-B direct sourcefree I02 family-stream construction and certificate guard | S03 | `POST_REWORK_UNMERGED__G5_HELD` |
| `KUDA-066` | S2-E exact native I03/I05/Batch output-fate and used-object conservation | S03/S04 | `POST_REWORK_UNMERGED__G5_NOT_VERIFIED` |
| `KUDA-067` | S3-A exact conditioned denominator and respondent membership for Field Forge | S04/S06 | `POST_REWORK_UNMERGED__G5_HELD` |
| `KUDA-068` | #997→#1073 exact source-I02→saved physical body handoff | S01/S03 | `SCOPED_ACCEPTED_INDIVIDUAL_BLOBS__JOINED_G5_HELD` |
| `KUDA-069` | S2-C/S2-D direct saved Parquet estate and cold native I03 index | S03/S04 | `INDIVIDUAL_SOURCEFREE_ACCEPTED__STACKED_UNMERGED` |
| `KUDA-070` | R03 governed original ELIGIBLE+SUPPORTED→QUERY v2 issuer | S02/S03 | `UNMERGED_AUTHOR_CANDIDATE__NO_G5_TEST_AT_CUT` |
| `KUDA-071` | W05 verified physical-order native respondent iterator optimization | S03 | `UNMERGED_AUTHOR_CANDIDATE__UNMEASURED_AT_CUT` |
| `KUDA-072` | P0 PreparedSavedC11Admission reusable cold saved I03 session | S03/S04 | `UNMERGED_LOCAL_AUTHOR_TESTED__INDEPENDENT_G5_HELD` |
| `KUDA-073` | #997/#1073 source-to-saved postconsumer fate/readback attribution | S03/S04 | `INDIVIDUAL_SCOPED_ACCEPTED__JOINED_RECEIVING_HELD` |

## Full post-rework implementation evidence

### KUDA-001 — S1-B R157-to-current-C11 native/source configuration adapter

**DAG organ:** S01/S03. **Fate:** `SCOPED_G5_SOURCEFREE_ACCEPTED__CUMULATIVE_UNMERGED`. **Existing PR:** [#980](https://github.com/maidiu/rawlsing/pull/980). 

**Exact post-rework code:** [rawlsing_next/pre553_r157_projection_adapter.py](https://github.com/maidiu/rawlsing/blob/c8e739470beb0dc65ad70c419a906e483a12ca8f/rawlsing_next/pre553_r157_projection_adapter.py) at `c8e739470beb0dc65ad70c419a906e483a12ca8f`, Git blob `d4d84ef164feba6fb0de0851568738eb5f5e937d`.

**Inputs:** Validated exact source configuration, independently scoped decoder/reader permission, current GovernedC11Projection and PhysicalCellStream.

**Implemented output:** Current existing physical-cell→C11 projection and exact native-key/cell provenance; no new evaluator.

**Actual or held first reader:** project_c11_candidate_from_config calls the current C11 physical projection first reader; isolated nonrespondent fixture tests and #980 cumulative sourcefree intake.

**Why it may be reclaimed:** Strongest verified post-rework form of R157. It adapts the old standalone source_configuration package rather than installing another parallel source engine.

**Qualification gap:** Selected pre-cut PRE-MAIN lacks the adapter. Sourcefree/nonrespondent G5 only; #980 combined execution and protected receiving held. Original source rights unissued.

**Shortest nonduplicative comparison:** Compare #980 exact accepted S1-B adapter against live owner C11 ABI, retain original case/scope negatives, then owner-reviewed cumulative receiving.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-001, NEKUDA-002.

### KUDA-002 — B49 administered source-rule selection and NativePreimage adaptation

**DAG organ:** S01/S02. **Fate:** `ISOLATED_SOURCEFREE__UNADOPTED_AT_PRE_CUT`. 

**Exact post-rework code:** [rawlsing_next/pre553_inherited_source_rules.py](https://github.com/maidiu/rawlsing/blob/b5600da96358f8526471d635a1befa8daa3f098b/rawlsing_next/pre553_inherited_source_rules.py) at `b5600da96358f8526471d635a1befa8daa3f098b`.

**Inputs:** Externally supplied and versioned source/wave/country administration and mapping authority rows.

**Implemented output:** SelectedSourceRulePackage with per-entity selected and unresolved roles.

**Actual or held first reader:** Existing preimage adapter provides a narrow sourcefree B49→U43/C11→I03+Batch demonstration.

**Why it may be reclaimed:** Real source-owner semantics for the rewritten pipeline, not the obsolete old DDM question-classifier.

**Qualification gap:** SelectedSourceRulePackage and NativeSourcePackage have different ABIs. Original U/Epre and rights not issued.

**Shortest nonduplicative comparison:** Compare with accepted R03/S1-B source adapter; recover only missing selected-rule semantics and avoid competing source configurations.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-002.

### KUDA-003 — G50 separately governed operation/fate grammar

**DAG organ:** S02. **Fate:** `ISOLATED_SOURCEFREE__UNADOPTED_AT_PRE_CUT`. 

**Exact post-rework code:** [WORKER_RETURNS/PYAT-R50-G50-GOVERNED-OPERATION-GRAMMAR-R1/g50/enumerate.py](https://github.com/maidiu/rawlsing/blob/d379bafe36b8d89da27ea5bf33614d33aca7f2d2/WORKER_RETURNS/PYAT-R50-G50-GOVERNED-OPERATION-GRAMMAR-R1/g50/enumerate.py) at `d379bafe36b8d89da27ea5bf33614d33aca7f2d2`.

**Inputs:** A separate scoped source decision package, scientific grammar and explicit permission decisions.

**Implemented output:** Finite operation frontier with typed unsupported, blocked and eligible claims.

**Actual or held first reader:** Standalone toy I05 and I51 B49-native lowering first readers.

**Why it may be reclaimed:** Source-specific bounded operation selection, separate from I03 numerical engine.

**Qualification gap:** Policy supplied, not scientifically issued; G50 toy I05 is not original administration.

**Shortest nonduplicative comparison:** Compare exact operation union with R03 compiler and accepted S1-C before proposing any new enumerator.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-003.

### KUDA-004 — I51 B49+G50 integrated sourcefree operation lowering

**DAG organ:** S02/S03. **Fate:** `ISOLATED_SOURCEFREE__NARROW_CONSUMER`. 

**Exact post-rework code:** [WORKER_RETURNS/PYAT-R51-I51-B49-G50-JOINED-PRODUCER-R1/candidate/r51_joined_source_producer.py](https://github.com/maidiu/rawlsing/blob/9bbf9e0509411beb210331d28160324b005a784e/WORKER_RETURNS/PYAT-R51-I51-B49-G50-JOINED-PRODUCER-R1/candidate/r51_joined_source_producer.py) at `9bbf9e0509411beb210331d28160324b005a784e`.

**Inputs:** B49 selected source preimage and G50 eligible operation.

**Implemented output:** One-target/no-condition issued U43/C11→existing I03/Batch native fact.

**Actual or held first reader:** execute_joined invokes selected existing sourcefree C11/I03/Batch, rejecting unsupported arities.

**Why it may be reclaimed:** Actual joined rewritten-DAG consumer, not an older V550 algorithm.

**Qualification gap:** General condition/multi-target unsupported and source/science permission external.

**Shortest nonduplicative comparison:** Determine whether current R03 already subsumes this exact lowering before porting.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-003.

### KUDA-017 — F6M separate-source mathematically bounded synthesis

**DAG organ:** S07. **Fate:** `POST_REWORK_WORKER_SOURCEFREE_CANDIDATE`. 

**Exact post-rework code:** [WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py](https://github.com/maidiu/rawlsing/blob/1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa/WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py) at `1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa`.

**Inputs:** Separately issued finite-population binary marginals with missing overlap/target mass.

**Implemented output:** Exact rational Fréchet partial identification rather than fabricated two-source joint.

**Actual or held first reader:** F6P explicitly reads and verifies the produced F6M bundle.

**Why it may be reclaimed:** Applicable to modern PYAT heterogeneous-relation synthesis without requiring shared respondent IDs.

**Qualification gap:** No original survey joint native/independent science; distinct F6 receiving still held.

**Shortest nonduplicative comparison:** Compare with accepted current F6/S04 owner code, preserve uncovered-mass bounds before any integration.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-015.

### KUDA-018 — F6P post-rework typed bounded-evidence consumer

**DAG organ:** S07/S10. **Fate:** `POST_REWORK_WORKER_SOURCEFREE_CANDIDATE`. 

**Exact post-rework code:** [WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1/f6p_partial_bound_evidence_consumer.py](https://github.com/maidiu/rawlsing/blob/016870e86913e6f7a811a51db6aba2d741bcfe58/WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1/f6p_partial_bound_evidence_consumer.py) at `016870e86913e6f7a811a51db6aba2d741bcfe58`.

**Inputs:** An actual F6M bundle with pinned source/method identity.

**Implemented output:** Complete/partial/unidentified/mismatched/revoked/transport-refused evidence dispositions.

**Actual or held first reader:** consume_f6m_evidence verifies genuine F6M prior calculation.

**Why it may be reclaimed:** Conserves uncertainty and prevents downstream guessed default route probabilities.

**Qualification gap:** No original source or actor permission, no native first consumer.

**Shortest nonduplicative comparison:** Reuse typed evidence states when modern F6 produces source-qualified bounds.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-015.

### KUDA-019 — P07 exact comparable-time and as-of semantic selector

**DAG organ:** S08/S09. **Fate:** `POST_REWORK_TEST_ONLY_CANDIDATE`. 

**Exact post-rework code:** [WORKER_RETURNS/PYAT-F7-P07-RECOVERY/candidate/temporal_method_candidate.py](https://github.com/maidiu/rawlsing/blob/f8fe03cc6e6a482f428bed9e03c08e50ce1e6479/WORKER_RETURNS/PYAT-F7-P07-RECOVERY/candidate/temporal_method_candidate.py) at `f8fe03cc6e6a482f428bed9e03c08e50ce1e6479`.

**Inputs:** Explicit temporal bounds, source comparability attestations and historical publication versions.

**Implemented output:** Typed pairwise temporal compatibility and exact as-of version, with no implicit nearest/latest.

**Actual or held first reader:** No independently qualified real N9 as-of reader at frozen cut; author tests only.

**Why it may be reclaimed:** Modern F7 trust primitive for nonfabricated time-scoped values.

**Qualification gap:** No original comparable-wave issuing authority, actual recipient held.

**Shortest nonduplicative comparison:** Compare existing F7/P07 gate, then qualify exact version first consumer.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-016.

### KUDA-026 — I01 sourcefree world→durable learned checkpoint/lifecycle composition

**DAG organ:** S05/S09. **Fate:** `POST_REWORK_ISOLATED_INTEGRATION_CANDIDATE`. 

**Exact post-rework code:** [rawlsing_next/pre553_i01_sourcefree_world_lifecycle_candidate.py](https://github.com/maidiu/rawlsing/blob/a1dc59411faaee01b3acb1c4f08b2e6f09d56028/rawlsing_next/pre553_i01_sourcefree_world_lifecycle_candidate.py) at `a1dc59411faaee01b3acb1c4f08b2e6f09d56028`.

**Inputs:** Selected current sourcefree progressive-world response, Batch checkpoint, exact M2/B5 product identity.

**Implemented output:** Saved/restorable sourcefree world consumer with invalidation and lifecycle handoff.

**Actual or held first reader:** Calls current progressive evidence and M2/B5; no original-authorized life-course/world producer.

**Why it may be reclaimed:** Orchestrates distinct modern existing pieces without replacing learned scientific product owners.

**Qualification gap:** May overlap accepted M2/B5 and #980 S2-G; true unique handoff must be proved.

**Shortest nonduplicative comparison:** Compare with S2-G cold learned lifecycle and retain only nonduplicated persistence/consumer behavior.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-022, NEKUDA-027.

### KUDA-028 — W03/W04 compact C11 event bodies and cold I03/I05 reopening

**DAG organ:** S03. **Fate:** `POST_REWORK_UNMERGED_DRAFT__PARTIAL_INDEPENDENT_REVIEW`. **Existing PR:** [#895](https://github.com/maidiu/rawlsing/pull/895). 

**Exact post-rework code:** [rawlsing_next/_pre553_c11_execution_view.py](https://github.com/maidiu/rawlsing/blob/46b7325637e68f78ccc7487d4b1abc7009c5ac0b/rawlsing_next/_pre553_c11_execution_view.py) at `46b7325637e68f78ccc7487d4b1abc7009c5ac0b`.

**Inputs:** Validated current C11 sourcefree release/event material and safe private accelerator root.

**Implemented output:** Zstd compact event chunks and cold physical ParquetC11Carrier reopen with actual I03/I05 parity tests.

**Actual or held first reader:** test_pre553_c11_cold_reopen_i03.py invokes CarrierNeutralResearchExecutor in a fresh Python process.

**Why it may be reclaimed:** Partial earlier independently reviewed compressed bodies; distinct cold test and exact PR integration still held.

**Qualification gap:** Warm retained RSS gains do not prove cold original-source memory. Current host settings/permissions and exact #895 joined G5 held.

**Shortest nonduplicative comparison:** Reconcile with S2-C/W05 native physical reader and benchmark 100k/6GiB before any cache deployment.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-024.

### KUDA-059 — S1-D independent CURRENT decision-resolver hardening

**DAG organ:** S02/S03. **Fate:** `SCOPED_G5_SOURCEFREE_ACCEPTED__UNMERGED_VERSION_DELTA`. **Existing PR:** [#980](https://github.com/maidiu/rawlsing/pull/980). 

**Exact post-rework code:** [rawlsing_next/pre553_issued_workload.py](https://github.com/maidiu/rawlsing/blob/c8e739470beb0dc65ad70c419a906e483a12ca8f/rawlsing_next/pre553_issued_workload.py) at `c8e739470beb0dc65ad70c419a906e483a12ca8f`, Git blob `47db61752d08fa5c774436b2c29e489a8d91c3f2`.

**Inputs:** Issued NativeWorkload and independent CURRENT decision resolver, authentic host/purpose/source authority.

**Implemented output:** Fail-closed original workload/current re-evaluation on initial execute/resume with exact refs.

**Actual or held first reader:** execute_issued_workload invokes current C11/RouteB I03/I05/Batch, no new issuer or source reader.

**Why it may be reclaimed:** Nov12 staged code differs from the November18 selected pre-main issued-workload blob. Contains stricter CurrentDecisionResolver and robust resume gates.

**Qualification gap:** Actual selected code already has issued workload functionality; only specific added currentness protections may be stranded. #980 combined tests/receiving held.

**Shortest nonduplicative comparison:** Diff exact source bodies/affected callsites, cherry-pick only independently accepted stronger resolver behavior, not whole file.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-052.

### KUDA-060 — S2-F exact complete durable empirical I03/I05 result-closure archive

**DAG organ:** S03/S04/S05. **Fate:** `SCOPED_G5_SOURCEFREE_ACCEPTED__UNMERGED`. **Existing PR:** [#980](https://github.com/maidiu/rawlsing/pull/980). 

**Exact post-rework code:** [rawlsing_next/pre553_durable_empirical_closure.py](https://github.com/maidiu/rawlsing/blob/c8e739470beb0dc65ad70c419a906e483a12ca8f/rawlsing_next/pre553_durable_empirical_closure.py) at `c8e739470beb0dc65ad70c419a906e483a12ca8f`, Git blob `ceeb8589cf785d2a24fe468073bd5f68df405be1`.

**Inputs:** Already-issued native I03/I05 complete output, typed negative results, exact original fact/receipt identity and external pin.

**Implemented output:** Content-addressed durable empirical closure with cold reopen/positive-negative replay and candidate M1/FF consumer views.

**Actual or held first reader:** DurableEmpiricalClosure and publish_empirical_closure; limited S2-F fixture cold consumer; full S2-E/D joined native first reader not yet qualified.

**Why it may be reclaimed:** Actual post-rework full-result persistence, unlike historical V550 stores. 101k-byte implementation body absent from selected November18 PRE-MAIN.

**Qualification gap:** Independent acceptance isolated fixture only; full end-to-end S2-F still waits S2-E/D and combined #980 receiving.

**Shortest nonduplicative comparison:** Compose with existing S2-D saved native owner; validate native-to-cold-to-M1/FF changes and negatives before protected receiving.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-053.

### KUDA-061 — S2-G full durable M1→M2→B5 learned lifecycle/cold-world archive

**DAG organ:** S05/S09/S10. **Fate:** `SCOPED_INDEPENDENT_G5_PASS__UNMERGED`. **Existing PR:** [#980](https://github.com/maidiu/rawlsing/pull/980). 

**Exact post-rework code:** [rawlsing_next/pre553_durable_learned_lifecycle.py](https://github.com/maidiu/rawlsing/blob/c8e739470beb0dc65ad70c419a906e483a12ca8f/rawlsing_next/pre553_durable_learned_lifecycle.py) at `c8e739470beb0dc65ad70c419a906e483a12ca8f`, Git blob `c261db4f13b6a63d0b41d0cb87855287f3c06347`.

**Inputs:** An existing LearnedWorldCompositionResult, M1 disposition, M2 release, B5 historical/current checkpoint, independently pinned root.

**Implemented output:** Cold content-addressed learned archive and exact current/as-of/consumer projection with wrong-source refusal.

**Actual or held first reader:** Real changed sourcefree empirical native input through M1→M2→B5→cold learned-world consumer, isolated test scope.

**Why it may be reclaimed:** 79k-byte functioning post-DAG custody adapter with independent sourcefree G5 after MR01 wrong-source repair; absent from selected November18 tree.

**Qualification gap:** Not an original/native learned science issue. #980 four-packet cumulative combined owner/receiving still pending.

**Shortest nonduplicative comparison:** Do not recreate B5; qualify exact S2-G archive→selected M2/B5 first reader in cumulative integration.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-054, NEKUDA-022.

### KUDA-062 — S1-A race-safe source-to-C11 cache admission

**DAG organ:** S01/S03. **Fate:** `POST_REWORK_UNMERGED__G5_HELD`. **Existing PR:** [#942](https://github.com/maidiu/rawlsing/pull/942). 

**Exact post-rework code:** [rawlsing_next/pre553_source_backed_c11_facade.py](https://github.com/maidiu/rawlsing/blob/783994fbbd09132fe7a4a3c9e6d5b1b9a4ec3ae5/rawlsing_next/pre553_source_backed_c11_facade.py) at `783994fbbd09132fe7a4a3c9e6d5b1b9a4ec3ae5`, Git blob `f29247b33cb78e5f1e620620d6968ab433ce407a`.

**Inputs:** An existing completely I02-qualified producer projection and concurrent source-backed C11 session cache.

**Implemented output:** Producer-only cache admission that does not reject legal second validated writers after clear/recompute race.

**Actual or held first reader:** Existing execute_empirical_query first reader; author reported execution of race reproduction.

**Why it may be reclaimed:** Narrow real concurrency repair to current physical/semantic facade, not new C11 engine.

**Qualification gap:** #942 is sourcefree S2 corrective candidate and remained unmerged/G5 not run at inspected cut.

**Shortest nonduplicative comparison:** Diff live facade cache key and CAS semantics; preserve anti-mismatch refusal and rerun concurrency negative.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-055.

### KUDA-063 — S1-C independently censused pending-operation/fate conservation

**DAG organ:** S01/S02. **Fate:** `POST_REWORK_UNMERGED__G5_NOT_VERIFIED`. **Existing PR:** [#975](https://github.com/maidiu/rawlsing/pull/975). 

**Exact post-rework code:** [rawlsing_next/pre553_operation_fate_census.py](https://github.com/maidiu/rawlsing/blob/779fea665829aae641a3f3d6b463f456c78f8316/rawlsing_next/pre553_operation_fate_census.py) at `779fea665829aae641a3f3d6b463f456c78f8316`, Git blob `dd5bf3940083679612d73f98e6a7b7711c223fd5`.

**Inputs:** Two separate frozen source/administration candidate and scientific eligibility/fate censuses.

**Implemented output:** Honest complete/partial pending list with budget-deferred eligible operations barred from I05 overissuance.

**Actual or held first reader:** verify_frozen_inputs before existing R03 compiler→I05 issuance; #975 adversarial forged pending-list run.

**Why it may be reclaimed:** Concrete provenance/census repair that prevents unauthorized extra work while count-based downstream anti-joins still pass.

**Qualification gap:** Corrected candidate #975 not G5-accepted/selected at frozen cut.

**Shortest nonduplicative comparison:** Compare R03 protected frontier representations; run forged-deferred-state negative with source-specific current owner.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-056.

### KUDA-064 — S2-A sealed I02 semantic event-range mutation refusal

**DAG organ:** S03. **Fate:** `POST_REWORK_UNMERGED__G5_HELD`. **Existing PR:** [#944](https://github.com/maidiu/rawlsing/pull/944). 

**Exact post-rework code:** [rawlsing_next/_pre553_verified_semantic_range.py](https://github.com/maidiu/rawlsing/blob/d3814d08dbe03b8464ac6fff4164765179869213/rawlsing_next/_pre553_verified_semantic_range.py) at `d3814d08dbe03b8464ac6fff4164765179869213`, Git blob `bd3b2bcc9cb244942d0257ede87c4a64a020af8b`.

**Inputs:** Existing fully I02-validated release and exact source-root-bound respondent event sequence.

**Implemented output:** CertifiedRespondentEvents immutable tuple range resisting post-digest sequence mutation.

**Actual or held first reader:** Actual native I03 selector receives verified semantic range; repaired distinct post-digest R1→R2 substitution breach.

**Why it may be reclaimed:** Not a new reader; concrete first-consumer integrity invariant absent from selected November18 tree.

**Qualification gap:** Author 105 pass/1 fail RED and corrective runs; independent G5 still held.

**Shortest nonduplicative comparison:** Apply only after exact provider receipt/body ABI compatibility, rerun mutable iterator attack.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-057.

### KUDA-065 — S2-B direct sourcefree I02 family-stream construction and certificate guard

**DAG organ:** S03. **Fate:** `POST_REWORK_UNMERGED__G5_HELD`. **Existing PR:** [#979](https://github.com/maidiu/rawlsing/pull/979). 

**Exact post-rework code:** [rawlsing_next/_pre553_direct_i02_sourcefree.py](https://github.com/maidiu/rawlsing/blob/cc35e0a4e51394961f58b632dec8a149deea21a2/rawlsing_next/_pre553_direct_i02_sourcefree.py) at `cc35e0a4e51394961f58b632dec8a149deea21a2`, Git blob `451727511af7f727b082c518aae2ba3a3dbe2ba3`.

**Inputs:** Typed C11 13-family section stream plus exact SourceReleaseManifest and external I02 certificate.

**Implemented output:** Direct native I02-prepared section/result without materializing old v1 C11LogicalRelease, with guarded manifest and event requirements.

**Actual or held first reader:** build_sourcefree_direct_i02→direct selector→native I03, actual 2→3→2 fact change/restore checked in author suite.

**Why it may be reclaimed:** Direct 13-family construction path written specifically for redesigned C11/RouteB physical architecture.

**Qualification gap:** Does not itself build S2-C durable Parquet. Source decoder→sections original-native owner still held.

**Shortest nonduplicative comparison:** Reconcile with #997/#1073 source-to-saved stage and accepted physical S2-C owner.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-058.

### KUDA-066 — S2-E exact native I03/I05/Batch output-fate and used-object conservation

**DAG organ:** S03/S04. **Fate:** `POST_REWORK_UNMERGED__G5_NOT_VERIFIED`. **Existing PR:** [#973](https://github.com/maidiu/rawlsing/pull/973). 

**Exact post-rework code:** [rawlsing_next/pre553_s2e_exact_conservation.py](https://github.com/maidiu/rawlsing/blob/1f787305f2f712f8a45e937cde7ee4b7a3be741e/rawlsing_next/pre553_s2e_exact_conservation.py) at `1f787305f2f712f8a45e937cde7ee4b7a3be741e`, Git blob `2b843d1c717f069969b7558f0f184ceec3145010`.

**Inputs:** Actual native retained I03 fact and I05 candidate provenance, query roles, source/fate preimages.

**Implemented output:** Incrementally hashed full exact output census and typed SUPPORTED/VALID_EMPTY/error fate proof; retains actual predicate/query object set.

**Actual or held first reader:** census_native_batch reads selected native I03/I05/Batch producer outputs, no replacement evaluator.

**Why it may be reclaimed:** Real sourcefree post-execution conservation function, closer to G4 live DAG than V550J pattern validation.

**Qualification gap:** A3 code/head on separate owner branch, tests/CI scope not independent G5 at inspected cut.

**Shortest nonduplicative comparison:** Use as negative court for #997/#1073 joined source→saved flow; no duplicate fact index.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-059.

### KUDA-067 — S3-A exact conditioned denominator and respondent membership for Field Forge

**DAG organ:** S04/S06. **Fate:** `POST_REWORK_UNMERGED__G5_HELD`. **Existing PR:** [#945](https://github.com/maidiu/rawlsing/pull/945). 

**Exact post-rework code:** [rawlsing_next/field_forge_conditional_support.py](https://github.com/maidiu/rawlsing/blob/624ad8d1516d32ecb30657d61103636c6fc966af/rawlsing_next/field_forge_conditional_support.py) at `624ad8d1516d32ecb30657d61103636c6fc966af`, Git blob `fd8570ec6bf6ee6e140abbcb251dd486da5d60cb`.

**Inputs:** Already-issued exact native I03 two-target joint; conditional respondent identities and eligible condition risk set.

**Implemented output:** Repaired exact conditional support profile with targets resolved only within conditioned denominator, no raw weighted leakage.

**Actual or held first reader:** Existing bounded GT2 Field Forge→PRE-V3/M1 first reader, with #945 96 PASS/1 XFAIL sourcefree test report.

**Why it may be reclaimed:** Repair to currently selected bounded FF relation; not a second Field Forge.

**Qualification gap:** Selected November18 FF code different blob; G5 independent at #945 held.

**Shortest nonduplicative comparison:** Compare with current GT2 owner exact denominator membership and authority before any merge.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-060.

### KUDA-068 — #997→#1073 exact source-I02→saved physical body handoff

**DAG organ:** S01/S03. **Fate:** `SCOPED_ACCEPTED_INDIVIDUAL_BLOBS__JOINED_G5_HELD`. **Existing PR:** [#1073](https://github.com/maidiu/rawlsing/pull/1073). 

**Exact post-rework code:** [rawlsing_next/pre553_source_i02_handoff.py](https://github.com/maidiu/rawlsing/blob/18dc7106f032bb86c89503daaefc5616cad29c58/rawlsing_next/pre553_source_i02_handoff.py) at `18dc7106f032bb86c89503daaefc5616cad29c58`, Git blob `31d99b70b9e726ecd1b2413aa68d642df4dc8151`.

**Inputs:** Current authorized source I02 13-family section evidence, source-realization preimage/fate, saved body builder.

**Implemented output:** Physical family stream to verified C11 saved Parquet/body closure with source/cell/slot identity and no-drop reconciliation.

**Actual or held first reader:** #997 R6 saved native I03/I05/Batch first consumer; #1073 cumulative stage imports source saved-body bridge.

**Why it may be reclaimed:** Real post-Vozdh source to saved reader code, not old V550 temporary Parquet.

**Qualification gap:** #997 individual G5 accepted sourcefree, but #1073 joined integration and protected receiving not independently approved.

**Shortest nonduplicative comparison:** Keep accepted source SHA, run joined I02→cold I03/I05/Batch→fact/negative parity with qualified host.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-061.

### KUDA-069 — S2-C/S2-D direct saved Parquet estate and cold native I03 index

**DAG organ:** S03/S04. **Fate:** `INDIVIDUAL_SOURCEFREE_ACCEPTED__STACKED_UNMERGED`. **Existing PR:** [#1073](https://github.com/maidiu/rawlsing/pull/1073). 

**Exact post-rework code:** [rawlsing_next/pre553_direct_estate_i03.py](https://github.com/maidiu/rawlsing/blob/18dc7106f032bb86c89503daaefc5616cad29c58/rawlsing_next/pre553_direct_estate_i03.py) at `18dc7106f032bb86c89503daaefc5616cad29c58`, Git blob `1dc82ab5658051f35dc1d81cbac30688e84a1623`.

**Inputs:** Authenticated source-direct C11 Parquet, externally pinned source/release and verified event/body semantic hashes.

**Implemented output:** Execution-local indexed native DirectEstateI03Session retaining original evaluator/predicate/risk-set and fact identity.

**Actual or held first reader:** #997 saved direct I03 and I05 sourcefree first readers, batch/restore; counterpart source_direct_parquet_estate.py.

**Why it may be reclaimed:** Post-rework direct C11 reader is already written and exercised; do not build another cold evaluator.

**Qualification gap:** Exact selected November18 PRE-MAIN lacks module. Index performance remains W05/P0 owner-qualification issue; no original35 rights.

**Shortest nonduplicative comparison:** Compare to #1103 prepared/session and #1083 W05 physical order before choosing one current reader.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-062.

### KUDA-070 — R03 governed original ELIGIBLE+SUPPORTED→QUERY v2 issuer

**DAG organ:** S02/S03. **Fate:** `UNMERGED_AUTHOR_CANDIDATE__NO_G5_TEST_AT_CUT`. **Existing PR:** [#1084](https://github.com/maidiu/rawlsing/pull/1084). 

**Exact post-rework code:** [rawlsing_next/pre553_governed_query_issuer_v2.py](https://github.com/maidiu/rawlsing/blob/357a0fbf50377788b050f5365089ed54a0548f23/rawlsing_next/pre553_governed_query_issuer_v2.py) at `357a0fbf50377788b050f5365089ed54a0548f23`, Git blob `83e7cc6a8924f1d65d221e53eb106c3d9bec56dc`.

**Inputs:** Current NativePreimageBundle, SourceInventory, GrammarPolicy, ScientificFrontier with external source and science eligibility.

**Implemented output:** Exact issued QUERY role jobs plus separate v2 decision/source/frontier hashes; original v1 discovery-only unchanged by default.

**Actual or held first reader:** Optional issuer_v2 into existing pre553_source_postconsumer_receipts and native cold saved Batch first reader.

**Why it may be reclaimed:** Addresses demonstrated 0 QUERY + 1 DISCOVERY original issuer without manually inventing queries or rewriting I03.

**Qualification gap:** New composite tests not executed on exact head; R03 owner ACK, SCIENCE_GRANT and independent G5 absent.

**Shortest nonduplicative comparison:** Run v1/v2 negative regressions against #1073 exact staged head; owner authorize only semantically supported queries.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-063.

### KUDA-071 — W05 verified physical-order native respondent iterator optimization

**DAG organ:** S03. **Fate:** `UNMERGED_AUTHOR_CANDIDATE__UNMEASURED_AT_CUT`. **Existing PR:** [#1083](https://github.com/maidiu/rawlsing/pull/1083). 

**Exact post-rework code:** [rawlsing_next/pre553_direct_estate_i03.py](https://github.com/maidiu/rawlsing/blob/1c37e2d45f5e74fc48b467272858986cd0bfc8a5/rawlsing_next/pre553_direct_estate_i03.py) at `1c37e2d45f5e74fc48b467272858986cd0bfc8a5`, Git blob `8825832f8067c7fce7a99a94505743cbb4eada06`.

**Inputs:** Authenticated direct saved estate/index with native physical respondent order and exact authority binding.

**Implemented output:** Opt-in reader locality shortcut when verified physical order is safe, retaining legacy selector and actual I03 semantics.

**Actual or held first reader:** DirectEstateI03Session.indices_for; focused sourcefree parity tests authored.

**Why it may be reclaimed:** Targets measured #1006 cold-query locality cost without a second SQL/evaluator or new source schema.

**Qualification gap:** No qualified G5 or 100k proof on this exact code; later R03 v2 stack may contain same blob lineage.

**Shortest nonduplicative comparison:** Compare selected reader/physical ABI and measure effect independently on real held sourcefree saved estate.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-064.

### KUDA-072 — P0 PreparedSavedC11Admission reusable cold saved I03 session

**DAG organ:** S03/S04. **Fate:** `UNMERGED_LOCAL_AUTHOR_TESTED__INDEPENDENT_G5_HELD`. **Existing PR:** [#1103](https://github.com/maidiu/rawlsing/pull/1103). 

**Exact post-rework code:** [rawlsing_next/pre553_prepared_saved_i03.py](https://github.com/maidiu/rawlsing/blob/cea2d4d3009e9087d2267e9d1f53bec28b730dc7/rawlsing_next/pre553_prepared_saved_i03.py) at `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`, Git blob `bcb146edae680028e027e47cae45891693f63526`.

**Inputs:** One authenticated cold saved C11 estate and qualified DirectEstateI03Session, distinct subsequent query and I05 operation descriptions.

**Implemented output:** One execution-local prepared posting index reused across many I03/I05 operations, identical computed outputs.

**Actual or held first reader:** PreparedSavedC11Admission.prepared_i03 invokes current original native evaluator; author 80 pass plus 100-op measured subset.

**Why it may be reclaimed:** Author observed 100 distinct ops 213.456s→126.424s, one build rather than 100, exact fact parity; no new evaluator.

**Qualification gap:** Sourcefree synthetic and only local author measurements. Fresh process rebuilds index; 100k/6GiB and native permissions not qualified.

**Shortest nonduplicative comparison:** Compare with W05 and #1073 saved direct session; benchmark same source-free workload and cumulative owner first reader.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-065.

### KUDA-073 — #997/#1073 source-to-saved postconsumer fate/readback attribution

**DAG organ:** S03/S04. **Fate:** `INDIVIDUAL_SCOPED_ACCEPTED__JOINED_RECEIVING_HELD`. **Existing PR:** [#1073](https://github.com/maidiu/rawlsing/pull/1073). 

**Exact post-rework code:** [rawlsing_next/pre553_source_postconsumer_receipts.py](https://github.com/maidiu/rawlsing/blob/18dc7106f032bb86c89503daaefc5616cad29c58/rawlsing_next/pre553_source_postconsumer_receipts.py) at `18dc7106f032bb86c89503daaefc5616cad29c58`.

**Inputs:** Native source operation, already-issued I03/I05/Batch outcome, exact candidate role and full operation fates.

**Implemented output:** Exact source/fate/native fact-provenance attribution and refusal for forged absent or manually inserted QUERY jobs.

**Actual or held first reader:** #997 R6 sourcefree saved real first-reader tests; #1084 optional v2 issuer extends this consumer.

**Why it may be reclaimed:** Real comparison of issued work versus actually executed current native results, not standalone test checksum.

**Qualification gap:** v1 0Q/1D, no science-created real QUERY; v2 owner receipt held.

**Shortest nonduplicative comparison:** Keep first-reader semantics, review v2 additive issuer only if separately qualified.

**Relevant NEKUDA predecessors / nonpromotable variants:** NEKUDA-061, NEKUDA-063.

## Existing rewritten-DAG baselines — do NOT call these stranded

- **Selected E41/R08/L01 path:** `rawlsing_next/pre553_evidence_world_consumer.py` at frozen PRE-MAIN `5d387a9a8c72`. Already selected sourcefree first reader; only discover a new branch-specific missing capability, not another binder.
- **Selected GT2 and GT3/GT4 canaries:** `rawlsing_next/tests/test_pre553_gt2_structural_positive_realization_court.py` at frozen PRE-MAIN `5d387a9a8c72`. Positive bounded first readers, not stranded actors or all35.
- **I07 source-relations, M2/B5/I4 learned product owners:** `rawlsing_next/pre553_source_relations.py` at frozen PRE-MAIN `5d387a9a8c72`. Selected guards and lifecycle; compare KUDA F6/I01/S2-G for incremental value.
- **K04 objective-position, M3 and M4 publication:** `rawlsing_next/prev3_objective_position_materializer.py` at frozen PRE-MAIN `5d387a9a8c72`. Selected and K04 identical historical blob; must not be ported again.
- **Existing R03 compiler, C11/RouteB, I03/I05/Batch:** `rawlsing_next/pre553_universal_workload.py` at frozen PRE-MAIN `5d387a9a8c72`. Original modern computational spine; new issuer/physical/readers integrate into these owners, never clone them.

The above are **comparison targets**. They are not counted in the KUDA recovery queue. A future investigation can add a stranded *extension* under a distinct ID only after an exact-code/consumer delta is proven. Unmerged #980/#1073 modules that are similar to protected ones still require field-by-field parity and independent combined receiving; absence in selected PRE-MAIN at the Nov18 cut does not prove absence at all later cuts.

## Next search law

Search **post-Aug DVA/TRII/CHETIRI/VOZDH-VERKHOVOD DAG lineages and post-rework current owners only**, following source-specific PR/commit custody into present first reader. Prioritize *code with demonstrated modern input/output* and documented receiving divergence; exclude theoretical plans, documentary prong counts, obsolete V550 algorithms, duplicate copies of selected modules and later disputed Q014–Q020 work. Before any action, consult current G4, and compare superior versions; preserve weaker variants in NEKUDA. If no real consuming owner exists, mark it as code-body-only rather than pretending completeness.
