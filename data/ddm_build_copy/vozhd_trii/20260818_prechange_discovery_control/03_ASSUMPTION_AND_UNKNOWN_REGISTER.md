# 03 — Assumption and Unknown Register

**Status:** `HOSTILE_PRECHANGE_QUESTION_SET`

This register exists to catch exactly the failure mode the user identified: the assistant may be making assumptions that the user has not thought to challenge, while the user may be carrying design premises that have never been tested against the present machine. Every material assumption below must either be verified, explicitly accepted as design law, or remain a named blocker before change design.

Status annotations added after first-wave intake use:

- `CLOSED_BY_Dxx` — the named court answered the question within its jurisdiction;
- `PARTIALLY_CLOSED_BY_Dxx` — implementation fact is known but authority/terminal meaning remains open;
- `OPEN` — still unresolved;
- `BLOCKED_BY_D05` — requires populated empirical substrate that D05 has not lawfully established.

## A. Data-grain assumptions

### U-001 — Is `respondent_id` globally unique and stable across every source/wave used by V550?
**Status:** `BLOCKED_BY_D05`

Schema suggests a global respondent table, but same-person cloud correctness depends on actual key semantics, ingestion behavior and duplicate handling.

Need to test:
- primary key and foreign-key enforcement;
- source/wave-local ID remapping;
- duplicate respondent rows;
- respondent collisions across imported datasets;
- whether cloud state scope makes accidental collisions impossible even if IDs are only locally unique.

D04 did establish that the in-memory cloud key separates run/source/wave/canonical-wave/country, but that does not establish populated respondent-ID integrity.

### U-002 — Does one respondent have at most one substantive response per canonical question in the analytic frame?
**Status:** `BLOCKED_BY_D05__EXECUTABLE_COLLAPSE_CONFIRMED_BY_D03_D04`

D03/D04 establish that current cloud preparation collapses duplicates with `drop_duplicates(respondent_id, keep=first)` and that conflicting duplicates are row-order sensitive. Whether populated data actually contain lawful repeated/multiselect/duplicate rows remains unmeasured.

### U-003 — Are position fields observed at the correct temporal grain?
**Status:** `BLOCKED_BY_D05`

`respondent_position_fact` looks static within a survey record. We must know whether employment, class, religion, household or region values have source-specific temporal/routing semantics that make cross-question conditioning misleading.

### U-004 — Are weights valid for every conditional/joint operation currently performed?
**Status:** `PARTIALLY_CLOSED_BY_D01_D02_D04__NORMATIVE_AUTHORITY_OPEN`

Executable behavior is now clearer: V547 was unweighted; current recursive tree and current attitude cloud are unweighted; some current V550 entropy/conditional summaries can use validated scalar weights. No court has established design-based survey-weight authority for every subgroup/joint operation. Populated weight coverage remains D05-blocked.

## B. Question-identity and response-topology assumptions

### U-010 — Does canonical question identity support cross-wave equivalence, or only within-source normalization?
**Status:** `OPEN`

Alias/reconcile surfaces exist, but the exact equivalence law and where it may be used need audit.

### U-011 — Are differently worded or differently routed questions ever collapsed into one canonical identity?
**Status:** `OPEN__D05_AND_LATER_AUTHORITY_AUDIT_REQUIRED`

If yes, attitude cotravel or cross-wave comparisons can acquire false equivalence.

### U-012 — How do multi-select, batteries, matrix questions, derived references and non-substantive options participate in V547–V550 analytics?
**Status:** `PARTIALLY_CLOSED_BY_D04`

D04 establishes that the current directional-atom cloud lane is restricted to certified scalar and binary-contrast topology; nominal, multiselect, ranked/routed, derived/reference, administrative/missingness and structurally classified matrix-child/factual-context forms are outside that lawful current cloud lane. Duplicate/multiselect set/order semantics remain `MISSING_AUTHORITY`, and other V550 analytic families still need topology-specific audit where relevant.

### U-013 — How are DK/refusal/IAP/not-asked/structural-zero states represented through cloud and branch calculations?
**Status:** `PARTIALLY_CLOSED_BY_D01_D02_D04`

Current harmonization can carry typed special-state flags, but D04 proves cloud preparation ignores them and can admit nonblank special states as cotravel content. D01/D02 show branching/determinicity metrics likewise do not automatically inherit typed semantic protection merely because flags exist elsewhere. Populated prevalence remains D05-blocked.

## C. V547→V550 lineage assumptions

### U-020 — Are the V550-native functions faithful successors or merely similarly named replacements?
**Status:** `CLOSED_BY_D01_D02_D03`

They are capability-family successors with material mathematical/semantic mutation, not faithful identity-preserving replacements.

### U-021 — Did any historical capability disappear during consolidation into V550?
**Status:** `CLOSED_BY_D01_D02_D03_WITH_TERMINAL_REQUIREMENT_STILL_OPEN`

Confirmed losses/mutations include unrestricted V547 pair search, V547 shape classification, V548 majority-position-deviation quadrants/semantics, historical branch-conditioned cotravel in the current native cloud/signature path, and the unrealized profile-cluster/relation-vector ambition. Whether each lost capability is terminally required remains D12/later jurisdiction.

### U-022 — Did any V550-native output acquire a different semantic role than its historical ancestor?
**Status:** `CLOSED_BY_D01_D02_D03`

Yes. Current position/relation signatures and attitude cloud have materially different anchors/grains/semantics from historical branch-conditioned objects; current recursive tree also changed the discovery question.

## D. Attitude-cloud assumptions

### U-030 — Is current pair coverage complete independent of question order?
**Status:** `CLOSED_BY_D04__NO`

D04 proves the fresh-run executable pair surface is a processing-order lower triangle of the lawful D03 ordered-pair graph, subject to other gates.

### U-031 — Is the cloud directional by design?
**Status:** `CLOSED_FOR_CURRENT_EXECUTABLE_BY_D03_D04__TERMINAL_LAW_OPEN`

Yes for current conditional-probability fields. NMI/Cramér's V are symmetric summaries, but `P(candidate response | anchor response)` and baseline/lift fields are directional. When both questions are dual-eligible, D03's current semantic oracle requires both ordered directions; current one-pass code does not produce both.

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
**Status:** `PARTIALLY_CLOSED_BY_D03_D04`

Conflicting duplicates become row-order sensitive and multiselect set/order semantics are not represented by the helper. Whether such rows occur and at what scale remains D05-blocked; lawful repeated/multiselect semantics remain authority-open.

### U-036 — What do `should_emit_cloud_tables` gates exclude in practice?
**Status:** `PARTIALLY_CLOSED_BY_D04__POPULATED_COVERAGE_BLOCKED_BY_D05`

D04 proves the gate is semantically consequential because it runs before state registration: a gated question can disappear as a later feature candidate. Actual coverage counts and historically meaningful excluded cases remain unmeasured.

### U-037 — Where does `allowed_as_attitude_cloud_anchor` actually enter current V550 metadata after the R1 migration?
**Status:** `CLOSED_BY_D06`

It is synthesized by the current question-use/authority contract from R1 plus independent response/semantic/structural/review authorities; it is not a direct universal R1 column/workload grant. Cloud code consumes the synthesized anchor/feature permissions plus separate resource gates.

## E. Branch/position assumptions

### U-040 — Are fixed `INDICATOR_FIELDS` an implementation convenience, an empirical register, or lingering ontology?
**Status:** `PARTIALLY_CLOSED_BY_D01_D02_D06__WORKLOAD_AUTHORITY_OPEN`

Current V550 hard-codes a twelve-field analytic search universe for major branching families. D06 finds no universal Final-R1 workload mandate for that enumeration. This does not itself decide which fields should be searched; D07 must adjudicate workload authority once D05 is contract-closed.

### U-041 — Does recursive branching preserve actual cohort membership anywhere, or only summary nodes?
**Status:** `CLOSED_FOR_CURRENT_TREE_OUTPUT_BY_D02`

Current recursive tree output does not persist respondent IDs/membership. Broader membership is replayable only from deeper same-respondent incidence plus exact algorithm/scope/topology/missingness/provenance.

### U-042 — Are greedy top-two branch splits appropriate as discovery heuristics?
**Status:** `PARTIALLY_CLOSED_BY_D02__TERMINAL_STANDARD_OPEN`

D02 proves specific loss modes: zero-marginal XOR/parity stops at the root and third-or-lower-frequency categories can disappear even when distinctive. Whether the heuristic is sufficient for terminal discovery obligations remains D12/later jurisdiction.

### U-043 — What lawful role, if any, do region/urbanicity/religion/income/employment play in the nine-stratum structural field?
**Status:** `BLOCKED_BY_D05_AND_D10`

This requires actual populated coordinate reality plus explicit empirical-coordinate→structural-predicate authority rather than string matching.

## F. Historical-intent vs current-law assumptions

### U-050 — What did "profile posterior" mean in the historical architecture?
**Status:** `PARTIALLY_CLOSED_BY_D03__CURRENT_LAWFUL_SEAM_OPEN`

Historical evidence meant a broader position + branch + attitude-cotravel probabilistic construction, not a direct synonym for current V3 actor state. The owner correction now explicitly requires a probabilistic positioned-subject possibility field while preserving V3 causal realization. The exact current lawful seam remains open.

### U-051 — Which old intentions were deliberately superseded?
**Status:** `OPEN`

The current Governing Spirit is stricter than some old pack language. D01–D03 distinguish implementation loss/mutation from current authority, but deliberate semantic supersession still requires explicit genealogy rather than inference from absence.

### U-052 — Is "same answer, different cloud, different meaning" still a terminal requirement?
**Status:** `OPEN__D09`

The owner correction strengthens the case that empirical cotravel/possibility geometry matters, but it does not determine the lawful meaning-field/structural/V3 seam. D09 remains required.

## G. Downstream-consumption assumptions

### U-060 — Is V550 conditional/cotravel meaning currently stranded after R1, or did newer authority wiring create a consumer?
**Status:** `OPEN__D11_UNLOCKED`

D01 finds the canonical V551 compiler does not consume the derived-determinicity lane at its base and a conditional helper is unwired/broken; D03 sees bridge reads of diagnostic cloud/signature artifacts. D11 must trace current V551/V551J/V552/V552J end-to-end before a current stranded-meaning ruling.

### U-061 — Can V551/V552 represent cotravel or branch-conditioned structural meaning without semantic leakage?
**Status:** `OPEN__D11_D09`

Need exact current schemas and compiler paths, not field-name analogy.

### U-062 — Does any V553–V558 direct-DAG path preserve exact earlier empirical evidence references now?
**Status:** `OPEN__D11_AND_LATER`

Direct reachability may solve transport while leaving interpretation unresolved.

### U-063 — Which V3 rule families could lawfully consume structural meaning derived from subgroup/cotravel evidence?
**Status:** `OPEN__D09_D10_D12`

The owner correction permits a probabilistic empirical possibility field but does not authorize a direct belief assignment. Exact structural/mediation/developmental binding remains open.

## H. Physical-retention assumptions

### U-070 — Is source replay actually exact enough to demote normalized respondent substrate?
**Status:** `BLOCKED_BY_D05_AND_LATER_D13`

Need hash-bound replay proof on representative and hostile source families.

### U-071 — Does the public database itself already constitute a durable source-equivalent capsule?
**Status:** `BLOCKED_BY_D05`

Schema alone cannot answer whether all source-native routing, labels, missingness, weights and joint incidence survive ingestion losslessly. D05's current worker return is not closed and provides no populated evidence.

### U-072 — Which "future-authorizable" empirical coordinates are lost if raw source files are discarded?
**Status:** `BLOCKED_BY_D05_AND_LATER_D13`

A source-equivalent projection must preserve the future query frontier, not just today's 12 fields.

## I. Statistical assumptions

### U-080 — Are support thresholds functioning as epistemic caution or accidental significance tests?
**Status:** `PARTIALLY_CLOSED_BY_D04__BROADER_LAW_OPEN`

For the current cloud, support tiers mark low support/confidence and do not suppress an otherwise emitted positive-support pair. They are not established as significance/CI authority. Other analytics and terminal admission law remain to be adjudicated.

### U-081 — Are rare but structurally meaningful configurations systematically excluded by support gates?
**Status:** `PARTIALLY_CLOSED_BY_D02_D04__POPULATED_EFFECT_BLOCKED_BY_D05`

D02 proves top-two recursive branching can erase lower-frequency categories and zero-marginal interactions. D04 shows support alone does not suppress cloud rows, but earlier gates/topology restrictions can. Actual historical/populated loss rates remain unmeasured.

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
**Status:** `OPEN__D08_D13_LATER`

D01–D03 strengthen the information requirement for same-respondent incidence, but architecture may not be selected before semantic/physical courts close.

## K. Human-model assumptions

### U-100 — Which empirical distinctions are necessary to prevent the generated world from becoming too generic?
**Status:** `OPEN__D09_D12`

The danger is not only deterministic profiling. Overcompression can make every actor face the same flat structural field.

### U-101 — Which empirical distinctions would make the actor *too survey-like* if promoted downstream?
**Status:** `OPEN__D09_D12`

The inverse danger is demographic destiny or attitudinal puppetry. The owner correction explicitly permits probability-space constraint but preserves the ban on direct finished-belief/psyche assignment.

### U-102 — What is the correct empirical grain for "historical meaning fields"?
**Status:** `OPEN__D08_D09_D12`

Possibilities include distributions, conditioned distributions, covariance/cotravel networks, branch cohorts, structural interpretations, probabilistic possibility fields, or combinations. This is a semantic question, not a storage question.

## L. First-wave control-state blockers and corrections

### U-110 — What is the actual populated empirical substrate available to current V550?
**Status:** `D05_RETURN_REQUIRED__POPULATED_DATA_ACCESS_MISSING`

No populated counts or completeness claims are closed. D05's substantive blocker verdict is provisionally correct, but the court failed its output contract: required `RESULT.json` and promised exact audit SQL/output-schema artifacts are absent.

### U-111 — Are the D05 evidence identities trustworthy as currently returned?
**Status:** `CLOSED__NO__REPAIR_REQUIRED`

At D05's exact base, the controlled `evidence/conversation_inputs/SHA256SUMS.txt` records:

- `Rawlsing_WVS_public_schema.sql` = `2c3f4a9ebec1e6c0cf62e8827ab982e52243c5c8899c961cd0e30b489573ec76`
- `Rawlsing_WVS_authority_reconcile_schema.sql` = `57e8c58c9444be9c34df54765e1801a9819f7a15fd02ddaa9a8e194e57596877`

D05's current result reports different hashes. It must correct or explicitly prove a distinct byte source before closure.

### U-112 — Did D04 violate its mandatory dependency on accepted D03 semantics?
**Status:** `CLOSED__NO`

The final D04 branch is based exactly on accepted D03 tip `7ea5962f644ad796064e30ffafb46f2c077404b9`. D03→D04 dependency satisfaction is verified.

### U-113 — Does Final R1 itself authorize all-question × fixed-12-field V550 branching work?
**Status:** `CLOSED_BY_D06__NO_UNIVERSAL_MANDATE_DEMONSTRATED`

D06 establishes that major branching/conditional workloads are driven by implementation enumeration/unconditional orchestration rather than a demonstrated universal Final-R1 workload predicate. D07 must still determine the lawful workload authority that should govern future computation.

### U-114 — Which later court is presently unlocked?
**Status:** `CURRENT_CONTROL_STATE`

D11 is unlocked by accepted D06. D07, D08 and D10 remain blocked by non-closed D05 under the machine-readable dependency register; D09/D12/D13/D14/D15 remain transitively blocked.
