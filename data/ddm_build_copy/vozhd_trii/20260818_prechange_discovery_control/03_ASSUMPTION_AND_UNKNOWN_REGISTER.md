# 03 — Assumption and Unknown Register

**Status:** `HOSTILE_PRECHANGE_QUESTION_SET`

This register exists to catch exactly the failure mode the user identified: the assistant may be making assumptions that the user has not thought to challenge, while the user may be carrying design premises that have never been tested against the present machine. Every material assumption below must either be verified, explicitly accepted as design law, or remain a named blocker before change design.

## A. Data-grain assumptions

### U-001 — Is `respondent_id` globally unique and stable across every source/wave used by V550?
Schema suggests a global respondent table, but same-person cloud correctness depends on actual key semantics, ingestion behavior and duplicate handling.

Need to test:
- primary key and foreign-key enforcement;
- source/wave-local ID remapping;
- duplicate respondent rows;
- respondent collisions across imported datasets;
- whether cloud state scope makes accidental collisions impossible even if IDs are only locally unique.

### U-002 — Does one respondent have at most one substantive response per canonical question in the analytic frame?
Current cloud preparation drops duplicates by respondent. That can silently discard multi-select, repeated-module, panel, routed or duplicated source records.

Need to classify every topology where this operation is lawful or lossy.

### U-003 — Are position fields observed at the correct temporal grain?
`respondent_position_fact` looks static within a survey record. We must know whether employment, class, religion, household or region values have source-specific temporal/routing semantics that make cross-question conditioning misleading.

### U-004 — Are weights valid for every conditional/joint operation currently performed?
A primary scalar weight exists, but the applicability of that weight to subgroup conditionals, cross-question overlap, missingness and multi-stage designs is not yet proved.

## B. Question-identity and response-topology assumptions

### U-010 — Does canonical question identity support cross-wave equivalence, or only within-source normalization?
Alias/reconcile surfaces exist, but the exact equivalence law and where it may be used need audit.

### U-011 — Are differently worded or differently routed questions ever collapsed into one canonical identity?
If yes, attitude cotravel or cross-wave comparisons can acquire false equivalence.

### U-012 — How do multi-select, batteries, matrix questions, derived references and non-substantive options participate in V547–V550 analytics?
A single string-valued response model can be invalid for several topologies.

### U-013 — How are DK/refusal/IAP/not-asked/structural-zero states represented through cloud and branch calculations?
Blank filtering can turn distinct epistemic states into one disappearance.

## C. V547→V550 lineage assumptions

### U-020 — Are the V550-native functions faithful successors or merely similarly named replacements?
Need function-by-function semantic diff:

```text
old numbered producer
vs
V550-native producer
```

Compare input grain, formulas, weighting, support, branch semantics, output grain, authority gates and intended consumers.

### U-021 — Did any historical capability disappear during consolidation into V550?
Especially:
- explicit interaction shape diagnostics;
- stable branch membership cohorts;
- profile covariance;
- majority-position deviation;
- branch split evidence;
- any cotravel semantics that no longer exist in current cloud rows.

### U-022 — Did any V550-native output acquire a different semantic role than its historical ancestor?
A diagnostic ancestor can become a bridge input; a historical profile feature can become explicitly `not_direct_evidence`. Names are not enough.

## D. Attitude-cloud assumptions

### U-030 — Is current pair coverage complete independent of question order?
The incremental state algorithm must be tested on all anchor/feature eligibility permutations.

### U-031 — Is the cloud directional by design?
`P(candidate | anchor)` is inherently asymmetric. Need to know whether both directions are required, whether only one is authority-permitted, and whether processing order accidentally decides which direction exists.

### U-032 — Are cloud probabilities weighted or unweighted, and is that intentional?
The current row schema contains counts and empirical measures; exact weighting semantics need direct code audit.

### U-033 — What does `mutual_information` mean inside an anchor-response/candidate-response pair calculation?
Need exact contingency definition and proof that it is computed on the intended population rather than a filtered overlap that changes the baseline.

### U-034 — Does the baseline denominator preserve question routing and applicability?
`p_cotravelling_baseline` must be scoped to the same lawful candidate universe or lift can be misleading.

### U-035 — What is lost when `_prepare_attitude_cloud_frame` keeps the first response per respondent?
This is potentially decisive for multi-select or duplicate response rows.

### U-036 — What do `should_emit_cloud_tables` gates exclude in practice?
Need coverage counts by source/wave/question and examples of excluded historically meaningful small groups.

### U-037 — Where does `allowed_as_attitude_cloud_anchor` actually enter current V550 metadata after the R1 migration?
The public compendium has the field; the authority-enriched response view observed in the schema surfaced some eligibility fields but not obviously every one. Trace exact runtime authority source.

## E. Branch/position assumptions

### U-040 — Are fixed `INDICATOR_FIELDS` an implementation convenience, an empirical register, or lingering ontology?
VT3 held that they are not terminal structural-position ontology. Current R1 may alter authority context but does not by itself answer workload selection.

### U-041 — Does recursive branching preserve actual cohort membership anywhere, or only summary nodes?
If only summary nodes remain, later cotravel cannot reconstruct branch-level same-person incidence without replay.

### U-042 — Are greedy top-two branch splits appropriate as discovery heuristics?
They may systematically erase rare categories, nonmonotonic effects or configurations whose importance is historical rather than predictive.

### U-043 — What lawful role, if any, do region/urbanicity/religion/income/employment play in the nine-stratum structural field?
This requires explicit empirical-coordinate→structural-predicate authority rather than string matching.

## F. Historical-intent vs current-law assumptions

### U-050 — What did "profile posterior" mean in the historical architecture?
We must not assume it meant the same thing as current V3 actor state or personality.

### U-051 — Which old intentions were deliberately superseded?
The current Governing Spirit is stricter than some old pack language. We need an explicit supersession genealogy rather than treating every historical idea as a lost requirement.

### U-052 — Is "same answer, different cloud, different meaning" still a terminal requirement?
Possible lawful interpretations include semantic/structural-context evidence rather than actor belief. This must be adjudicated.

## G. Downstream-consumption assumptions

### U-060 — Is V550 conditional/cotravel meaning currently stranded after R1, or did newer authority wiring create a consumer?
Frozen VT3 found stranded unary conditional meaning. Current main must be traced afresh.

### U-061 — Can V551/V552 represent cotravel or branch-conditioned structural meaning without semantic leakage?
Need exact current schemas and compiler paths, not field-name analogy.

### U-062 — Does any V553–V558 direct-DAG path preserve exact earlier empirical evidence references now?
Direct reachability may solve transport while leaving interpretation unresolved.

### U-063 — Which V3 rule families could lawfully consume structural meaning derived from subgroup/cotravel evidence?
Potential destinations include generated position, opportunity/exposure, mediation, knowledge availability, household context or other structural constraints; none should be assumed.

## H. Physical-retention assumptions

### U-070 — Is source replay actually exact enough to demote normalized respondent substrate?
Need hash-bound replay proof on representative and hostile source families.

### U-071 — Does the public database itself already constitute a durable source-equivalent capsule?
Schema alone cannot answer whether all source-native routing, labels, missingness, weights and joint incidence survive ingestion losslessly.

### U-072 — Which "future-authorizable" empirical coordinates are lost if raw source files are discarded?
A source-equivalent projection must preserve the future query frontier, not just today's 12 fields.

## I. Statistical assumptions

### U-080 — Are support thresholds functioning as epistemic caution or accidental significance tests?
Current labels must not be read as CI/significance.

### U-081 — Are rare but structurally meaningful configurations systematically excluded by support gates?
Need hostile minority fixtures and historical cases.

### U-082 — Would survey-design variance materially alter which empirical patterns Rawlsing should admit?
Current architecture lacks governed design-based variance; determine whether this is deferred enhancement or a blocker for any planned use.

## J. Compute assumptions

### U-090 — How much of current V550 wall-clock cost is actually caused by the old determinicity families?
Static cardinality estimates are not enough. Need measured CPU, memory, I/O and materialization size.

### U-091 — Would compute-on-demand merely move cost downstream and produce latency/replay problems?
Need realistic query-frequency and runtime-serving analysis.

### U-092 — Can one shared respondent incidence substrate serve CED, joint patterns and attitude clouds without duplicate scans?
Likely, but must be designed only after semantic workloads are known.

## K. Human-model assumptions

### U-100 — Which empirical distinctions are necessary to prevent the generated world from becoming too generic?
The danger is not only deterministic profiling. Overcompression can make every actor face the same flat structural field.

### U-101 — Which empirical distinctions would make the actor *too survey-like* if promoted downstream?
The inverse danger is demographic destiny or attitudinal puppetry.

### U-102 — What is the correct empirical grain for "historical meaning fields"?
Possibilities include distributions, conditioned distributions, covariance/cotravel networks, branch cohorts, structural interpretations, or combinations. This is a semantic question, not a storage question.
