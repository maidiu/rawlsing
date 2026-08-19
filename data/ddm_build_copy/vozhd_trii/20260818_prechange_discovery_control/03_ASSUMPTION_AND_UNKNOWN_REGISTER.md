# 03 — Assumption and Unknown Register

**Status:** `HOSTILE_PRECHANGE_QUESTION_SET`

This register exists to catch exactly the failure mode the user identified: the assistant may be making assumptions that the user has not thought to challenge, while the user may be carrying design premises that have never been tested against the present machine. Every material assumption below must either be verified, explicitly accepted as design law, or remain a named blocker before change design.

Status annotations added after first-wave adjudication use:

- `CLOSED_BY_Dxx` — the named court answered the question within its jurisdiction;
- `PARTIALLY_CLOSED_BY_Dxx` — implementation fact is known but authority/terminal meaning remains open;
- `OPEN` — still unresolved;
- `EMPIRICAL_UNKNOWN_NO_DB` — the question requires populated empirical evidence unavailable in this campaign; D05 is court-closed blocked and the unknown must be carried forward rather than guessed.

## A. Data-grain assumptions

### U-001 — Is `respondent_id` globally unique and stable across every source/wave used by V550?
**Status:** `EMPIRICAL_UNKNOWN_NO_DB`

Schema suggests a global respondent table, but same-person cloud correctness depends on actual key semantics, ingestion behavior and duplicate handling.

Need populated evidence to test:
- primary key and foreign-key enforcement in the actual populated deployment;
- source/wave-local ID remapping;
- duplicate respondent rows;
- respondent collisions across imported datasets;
- whether cloud state scope makes accidental collisions impossible even if IDs are only locally unique.

D04 establishes that the in-memory cloud key separates run/source/wave/canonical-wave/country. D05 supplies a contingency audit for identity/collisions but no populated run is available.

### U-002 — Does one respondent have at most one substantive response per canonical question in the analytic frame?
**Status:** `EMPIRICAL_UNKNOWN_NO_DB__EXECUTABLE_COLLAPSE_CONFIRMED_BY_D03_D04`

D03/D04 establish that current cloud preparation collapses duplicates with `drop_duplicates(respondent_id, keep=first)` and that conflicting duplicates are row-order sensitive. D06 R2 additionally identifies a shared-substrate scalar duplicate policy that rejects duplicate substantive respondent×variable keys by default. Whether populated data actually contain lawful repeated/multiselect/duplicate rows remains unmeasured.

### U-003 — Are position fields observed at the correct temporal grain?
**Status:** `EMPIRICAL_UNKNOWN_NO_DB`

`respondent_position_fact` looks static within a survey record. We cannot establish whether employment, class, religion, household or region values have source-specific temporal/routing semantics that make cross-question conditioning misleading without populated/source-native evidence.

### U-004 — Are weights valid for every conditional/joint operation currently performed?
**Status:** `PARTIALLY_CLOSED_BY_D01_D02_D04__NORMATIVE_AUTHORITY_OPEN__POPULATED_COVERAGE_UNKNOWN`

Executable behavior is clear: V547 was unweighted; current recursive tree and current attitude cloud are unweighted; some current V550 entropy/conditional summaries can use validated scalar weights. No court has established design-based survey-weight authority for every subgroup/joint operation. Actual populated weight coverage/pathology remains unknown under the no-DB constraint.

## B. Question-identity and response-topology assumptions

### U-010 — Does canonical question identity support cross-wave equivalence, or only within-source normalization?
**Status:** `OPEN`

Alias/reconcile surfaces exist, but the exact equivalence law and where it may be used need audit.

### U-011 — Are differently worded or differently routed questions ever collapsed into one canonical identity?
**Status:** `OPEN__AUTHORITY_AUDIT_REQUIRED__POPULATED_IMPACT_UNKNOWN_NO_DB`

If yes, attitude cotravel or cross-wave comparisons can acquire false equivalence. Static authority/identity law can still be audited; actual populated incidence of such cases cannot be measured in this campaign.

### U-012 — How do multi-select, batteries, matrix questions, derived references and non-substantive options participate in V547–V550 analytics?
**Status:** `PARTIALLY_CLOSED_BY_D04_D06`

D04 establishes that the current directional-atom cloud lane is restricted to certified scalar and binary-contrast topology; nominal, multiselect, ranked/routed, derived/reference, administrative/missingness and structurally classified matrix-child/factual-context forms are outside that lawful current cloud lane. D06 R2 shows the shared-substrate scalar duplicate policy can reject repeated/multiselect row structures if represented as duplicate substantive respondent×variable keys. Lawful set/order semantics remain `MISSING_AUTHORITY`; populated incidence/loss remains unknown.

### U-013 — How are DK/refusal/IAP/not-asked/structural-zero states represented through cloud and branch calculations?
**Status:** `PARTIALLY_CLOSED_BY_D01_D02_D04_D06__POPULATED_PREVALENCE_UNKNOWN_NO_DB`

Current harmonization/shared transport can carry typed special-state flags, but D04 proves cloud preparation can admit nonblank special states as cotravel content. D01/D02 show branching/determinicity metrics do not automatically inherit typed semantic protection merely because flags exist elsewhere. D06 proves the shared substrate carries typed flags in its declared logical surface. Actual prevalence remains unknown.

## C. V547→V550 lineage assumptions

### U-020 — Are the V550-native functions faithful successors or merely similarly named replacements?
**Status:** `CLOSED_BY_D01_D02_D03`

They are capability-family successors with material mathematical/semantic mutation, not faithful identity-preserving replacements.

### U-021 — Did any historical capability disappear during consolidation into V550?
**Status:** `CLOSED_BY_D01_D02_D03_WITH_TERMINAL_REQUIREMENT_STILL_OPEN`

Confirmed losses/mutations include unrestricted V547 pair search, V547 shape classification, V548 majority-position-deviation quadrants/semantics, historical branch-conditioned cotravel in the current native cloud/signature path, and the intended-but-not-proven-realized profile-cluster/relation-vector ambition. Whether each capability is terminally required remains D12/later jurisdiction.

### U-022 — Did any V550-native output acquire a different semantic role than its historical ancestor?
**Status:** `CLOSED_BY_D01_D02_D03`

Yes. Current position/relation signatures and attitude cloud have materially different anchors/grains/semantics from historical branch-conditioned objects; current recursive tree also changed the discovery question.

## D. Attitude-cloud assumptions

### U-030 — Is current pair coverage complete independent of question order?
**Status:** `CLOSED_FOR_EXECUTABLE_BY_D04__NO__WORKLOAD_VIOLATION_OPEN_D07`

D04 proves the fresh-run executable pair surface depends on processing order. Parent review qualifies the normative conclusion: whether that incompleteness is a correctness violation depends on D07's workload law rather than semantic eligibility alone.

### U-031 — Is the cloud directional by design?
**Status:** `CLOSED_FOR_CURRENT_EXECUTABLE_BY_D03_D04__REQUIRED_MATERIALIZATION_LAW_OPEN_D07`

Yes for current conditional-probability fields. NMI/Cramér's V are symmetric summaries, but `P(candidate response | anchor response)` and baseline/lift fields are directional. D03's exhaustive ordered-pair set remains a conditional completeness oracle; D07 must decide whether both directions must be materialized, merely reconstructible, or selectively evaluated.

### U-032 — Are cloud probabilities weighted or unweighted, and is that intentional?
**Status:** `PARTIALLY_CLOSED_BY_D04`

Current cloud counts, modal-cell selection, probabilities, lift, NMI and Cramér's V are unweighted. Whether that is normatively lawful is `MISSING_AUTHORITY`.

### U-033 — What does `mutual_information` mean inside an anchor-response/candidate-response pair calculation?
**Status:** `CLOSED_FOR_CURRENT_EXECUTABLE_BY_D03_D04`

The cloud output field named `mutual_information` contains normalized mutual information, not raw MI. D04 confirms the current implementation mixes nats in the numerator with bits in the entropy denominator, so a perfect balanced binary deterministic relation reports approximately `0.693147` rather than `1.0`.

### U-034 — Does the baseline denominator preserve question routing and applicability?
**Status:** `PARTIALLY_CLOSED_BY_D03_D04__AUTHORITY_OPEN`

D04 confirms current arithmetic matches D03's executable oracle: selected anchor count uses the full prepared anchor frame while candidate baseline uses the full prepared candidate frame. Whether routed questions require a common risk-set denominator remains `MISSING_AUTHORITY`.

### U-035 — What is lost when `_prepare_attitude_cloud_frame` keeps the first response per respondent?
**Status:** `PARTIALLY_CLOSED_BY_D03_D04_D06__POPULATED_OCCURRENCE_UNKNOWN_NO_DB`

Conflicting duplicates become row-order sensitive and multiselect set/order semantics are not represented by the helper. D06 R2 shows a separate shared-substrate scalar duplicate policy can reject duplicate substantive respondent×variable rows. Whether such structures occur in populated production and at what scale remains unknown.

### U-036 — What do `should_emit_cloud_tables` gates exclude in practice?
**Status:** `PARTIALLY_CLOSED_BY_D04_D06__POPULATED_COVERAGE_UNKNOWN_NO_DB__WORKLOAD_LAW_OPEN_D07`

The gate runs before state registration and is an operational resource policy distinct from semantic permission. A gated question can therefore disappear as a later feature candidate. Actual coverage counts/historically meaningful excluded cases cannot be measured here; D07 must decide what workload coverage is required.

### U-037 — Where does `allowed_as_attitude_cloud_anchor` actually enter current V550 metadata after the R1 migration?
**Status:** `CLOSED_BY_D06_R2`

It is synthesized by the current question-use/authority contract from R1 plus independent response/semantic/structural/review authorities; it is not a direct universal R1 column/workload grant. Cloud code consumes the synthesized anchor/feature permissions plus separate resource gates.

## E. Branch/position assumptions

### U-040 — Are fixed `INDICATOR_FIELDS` an implementation convenience, an empirical register, or lingering ontology?
**Status:** `PARTIALLY_CLOSED_BY_D01_D02_D06_R2__D07_READY`

Current V550 hard-codes a twelve-field analytic search universe for major branching families. D06 R2 did not locate a universal Final-R1/family-granular workload mandate for that enumeration and proves `allowed_as_branch_splitter` does not gate actual recursive split-variable execution. D07 is now ready to adjudicate governing workload authority.

### U-041 — Does recursive branching preserve actual cohort membership anywhere, or only summary nodes?
**Status:** `CLOSED_FOR_CURRENT_TREE_OUTPUT_BY_D02`

Current recursive tree output does not persist respondent IDs/membership. Broader membership replay requires deeper same-respondent incidence plus exact algorithm/scope/topology/missingness/provenance; physical replay sufficiency remains D13 jurisdiction.

### U-042 — Are greedy top-two branch splits appropriate as discovery heuristics?
**Status:** `PARTIALLY_CLOSED_BY_D02__TERMINAL_STANDARD_OPEN`

D02 proves specific loss modes: zero-marginal XOR/parity stops at the root and third-or-lower-frequency categories can disappear even when distinctive. Whether the heuristic is sufficient for terminal discovery obligations remains D12/later jurisdiction.

### U-043 — What lawful role, if any, do region/urbanicity/religion/income/employment play in the nine-stratum structural field?
**Status:** `OPEN__D10_READY__POPULATED_VALUE_INVENTORY_UNKNOWN_NO_DB`

D10 may now adjudicate explicit empirical-coordinate→structural-predicate authority from static/current authority evidence. It must not infer live field/value inventories, coverage or prevalence from names because D05 closed blocked.

## F. Historical-intent vs current-law assumptions

### U-050 — What did "profile posterior" mean in the historical architecture?
**Status:** `PARTIALLY_CLOSED_BY_D03__CURRENT_LAWFUL_SEAM_OPEN`

Historical evidence meant a broader position + branch + attitude-cotravel probabilistic construction, not a direct synonym for current V3 actor state. The owner correction now explicitly requires a probabilistic positioned-subject possibility field while preserving V3 causal realization. The exact current lawful seam remains open.

### U-051 — Which old intentions were deliberately superseded?
**Status:** `OPEN`

The current Governing Spirit is stricter than some old pack language. D01–D03 distinguish implementation loss/mutation from current authority, but deliberate semantic supersession still requires explicit genealogy rather than inference from absence.

### U-052 — Is "same answer, different cloud, different meaning" still a terminal requirement?
**Status:** `OPEN__D09`

The owner correction strengthens the case that empirical cotravel/possibility geometry matters, but it does not determine the lawful meaning-field/structural/V3 seam. D09 remains required after D08.

## G. Downstream-consumption assumptions

### U-060 — Is V550 conditional/cotravel meaning currently stranded after R1, or did newer authority wiring create a consumer?
**Status:** `OPEN__D11_READY`

D01 finds the canonical V551 compiler does not consume the derived-determinicity lane at its base and a conditional helper is unwired/broken; D03 sees bridge reads of diagnostic cloud/signature artifacts. D06 R2 additionally proves current V550/V550J shared extraction, JOINT_ONLY expansion, and direct prepared-required V550J consumption. D11 is now ready and must trace current V551/V551J/V552/V552J end-to-end before a stranded-meaning ruling.

### U-061 — Can V551/V552 represent cotravel or branch-conditioned structural meaning without semantic leakage?
**Status:** `OPEN__D11_READY__D09_LATER`

Need exact current schemas and compiler paths, not field-name analogy.

### U-062 — Does any V553–V558 direct-DAG path preserve exact earlier empirical evidence references now?
**Status:** `OPEN__D11_READY_AND_LATER`

Direct reachability may solve transport while leaving interpretation unresolved.

### U-063 — Which V3 rule families could lawfully consume structural meaning derived from subgroup/cotravel evidence?
**Status:** `OPEN__D09_D10_D12`

The owner correction permits a probabilistic empirical possibility field but does not authorize a direct belief assignment. Exact structural/mediation/developmental binding remains open.

## H. Physical-retention assumptions

### U-070 — Is source replay actually exact enough to demote normalized respondent substrate?
**Status:** `OPEN__D13_LATER__EMPIRICAL_END_TO_END_PROOF_UNAVAILABLE_WITHOUT_NEW_DATA_ACCESS`

D13 can later prove static/information-theoretic sufficiency conditionally. It cannot claim a populated end-to-end replay proof against current production unless an exact production-equivalent materialization independently becomes available.

### U-071 — Does the public database itself already constitute a durable source-equivalent capsule?
**Status:** `EMPIRICAL_UNKNOWN_NO_DB__D13_LATER`

Schema and shared-substrate contracts cannot answer whether all source-native routing, labels, missingness, weights, multiple-response semantics and joint incidence survive ingestion losslessly. D05 is closed blocked with no positive source-equivalence claim.

### U-072 — Which "future-authorizable" empirical coordinates are lost if raw source files are discarded?
**Status:** `OPEN__D13_LATER__POPULATED_LOSS_UNKNOWN_NO_DB`

A source-equivalent projection must preserve the future query frontier, not just today's fields. D06 R2 proves strong integrity only for the declared shared-substrate logical surface, not arbitrary future-authorizable coordinates.

## I. Statistical assumptions

### U-080 — Are support thresholds functioning as epistemic caution or accidental significance tests?
**Status:** `PARTIALLY_CLOSED_BY_D04__BROADER_LAW_OPEN`

For the current cloud, support tiers mark low support/confidence and do not suppress an otherwise emitted positive-support pair. They are not established as significance/CI authority. Other analytics and terminal admission law remain to be adjudicated.

### U-081 — Are rare but structurally meaningful configurations systematically excluded by support gates?
**Status:** `PARTIALLY_CLOSED_BY_D02_D04__POPULATED_EFFECT_UNKNOWN_NO_DB`

D02 proves top-two recursive branching can erase lower-frequency categories and zero-marginal interactions. D04 shows support alone does not suppress cloud rows, but earlier gates/topology restrictions can. Actual populated loss rates remain unmeasured.

### U-082 — Would survey-design variance materially alter which empirical patterns Rawlsing should admit?
**Status:** `OPEN`

Current architecture lacks governed design-based variance; determine whether this is deferred enhancement or a blocker for any planned use.

## J. Compute assumptions

### U-090 — How much of current V550 wall-clock cost is actually caused by the old determinicity families?
**Status:** `OPEN__D14_LATER`

Static cardinality estimates are not enough. Need measured CPU, memory, I/O and materialization size after lawful workloads are known.

### U-091 — Would compute-on-demand merely move cost downstream and produce latency/replay problems?
**Status:** `OPEN__D13_D14_LATER`

Need realistic query-frequency and runtime-serving analysis.

### U-092 — Can one shared respondent incidence substrate serve CED, joint patterns and attitude clouds without duplicate scans?
**Status:** `PARTIALLY_CLOSED_BY_D06_R2__D08_D13_READY_LATER`

D06 R2 proves a deliberate V550/V550J shared respondent-grain substrate and direct prepared V550J consumption exist. It does not prove that declared substrate is semantically or physically sufficient for CED, arbitrary conjunctions, branch-conditioned cotravel, repeated/multiselect structure or all future-authorizable queries. D08 owns fact-algebra sufficiency; D13 later owns physical replay/retention sufficiency.

## K. Human-model assumptions

### U-100 — Which empirical distinctions are necessary to prevent the generated world from becoming too generic?
**Status:** `OPEN__D09_D12`

The danger is not only deterministic profiling. Overcompression can make every actor face the same flat structural field.

### U-101 — Which empirical distinctions would make the actor *too survey-like* if promoted downstream?
**Status:** `OPEN__D09_D12`

The inverse danger is demographic destiny or attitudinal puppetry. The owner correction explicitly permits probability-space constraint but preserves the ban on direct finished-belief/psyche assignment.

### U-102 — What is the correct empirical grain for "historical meaning fields"?
**Status:** `OPEN__D08_READY__D09_D12_LATER`

Possibilities include distributions, conditioned distributions, covariance/cotravel networks, branch cohorts, structural interpretations, probabilistic possibility fields, or combinations. This is a semantic question, not a storage question.

## L. First-wave control-state blockers and corrections

### U-110 — What is the actual populated empirical substrate available to current V550?
**Status:** `EMPIRICAL_UNKNOWN_NO_DB__D05_COURT_CLOSED_BLOCKED`

No populated counts or completeness claims are established. D05 now satisfies its fail-closed output contract with a materially complete contingency audit kit, but no live or production-equivalent populated database is available. The court is closed; the empirical proposition remains unknown.

### U-111 — Are the D05 evidence identities trustworthy as currently returned?
**Status:** `CLOSED__YES_AFTER_D05_RETURN_REPAIR`

The repaired D05 return restores the controlled hashes for both schema evidence files and binds its contingency audit to those identities. A minor R4/R2 run-manifest metadata mismatch remains recorded as a non-reopening contingency defect unless the audit is ever executed.

### U-112 — Did D04 violate its mandatory dependency on accepted D03 semantics?
**Status:** `CLOSED__NO`

The final D04 branch is based exactly on accepted D03 tip `7ea5962f644ad796064e30ffafb46f2c077404b9`. D03→D04 dependency satisfaction is verified.

### U-113 — Does Final R1 itself authorize all-question × fixed-12-field V550 branching work?
**Status:** `PARTIALLY_CLOSED_BY_D06_R2__UNIVERSAL_MANDATE_NOT_LOCATED__D07_READY`

D06 R2 establishes that major branching/conditional workloads are driven by implementation enumeration/unconditional orchestration rather than a demonstrated universal Final-R1 workload predicate. It deliberately uses `NOT_LOCATED`, not `ABSENT`, for a universal family-granular mandate. D07 must now determine whether governing law requires materialize-all, reconstructible-all, or an authority-selected subset.

### U-114 — Which later courts are presently unlocked?
**Status:** `CURRENT_CONTROL_STATE__WAVE1_CLOSED`

D07, D08, D10 and D11 are ready. D09 remains blocked by D08. D12 remains blocked by D09 + D10 + D11; D13/D14/D15 remain transitively blocked. D15 remains the first architecture-synthesis court.

### U-115 — Where is the authoritative derivation/write source of `allowed_as_association_feature`?
**Status:** `NOT_LOCATED_BY_D06_R2__OPEN_AUTHORITY_EDGE`

D06 R2 proves the field is physically transported by the V550/V550J shared substrate and actively read by V550J association eligibility. It does not locate the authoritative upstream derivation/write source. Under the campaign negative-proof law this is `NOT_LOCATED`, not `ABSENT`.

### U-116 — Are `JOINT_ONLY` variables semantically prepared identically to base-QSM variables before V550J consumes the shared substrate?
**Status:** `NOT_DEMONSTRATED_BY_D06_R2__D11_D08_RELEVANT`

The joint registry can lawfully expand extraction beyond base QSM membership, while the shared-substrate canonicalizer does not itself re-harmonize semantics and may fill missing required fields with defaults. D06 does not prove semantic-preparation parity. D11 should trace actual current J consumption; D08 should account for this distinction when adjudicating fact algebra.
