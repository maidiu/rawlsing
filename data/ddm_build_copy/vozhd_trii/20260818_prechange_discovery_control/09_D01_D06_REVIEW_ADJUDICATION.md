# 09 — D01–D06 Second-Pass Review Adjudication

**Status:** `BINDING_PARENT_REVIEW__SUPERSEDES_08_WHERE_CONFLICTING`

**Repository:** `maidiu/rawlsing`

**Control branch:** `agent/vozhd-trii-prechange-discovery-control`

**Review scope:** returned Wave-1 courts D01 through D06 only. No production redesign or production-semantic change is authorized.

## 1. Review purpose

The first intake in `08_FIRST_WAVE_INTAKE_ADJUDICATION.md` established branch/base/output hygiene and banked the strongest returned findings. This second pass reviews the *substantive claims themselves* across courts, with particular attention to cross-court premise leakage, overclassification, missed current surfaces, and whether a local implementation fact was promoted into a stronger semantic/workload claim than governing authority supports.

Where this file conflicts with `08_FIRST_WAVE_INTAKE_ADJUDICATION.md`, this file controls.

## 2. Court verdicts after review

| Court | Review verdict | Dependency-closed? | Parent ruling |
|---|---|---:|---|
| D01 | `ACCEPTED_WITH_REVIEW_NORMALIZATION` | yes | Core lineage/search-geometry findings stand; narrow overstatements are normalized below. |
| D02 | `ACCEPTED` | yes | Technically strong; no mission-breaking error found. |
| D03 | `ACCEPTED_LINEAGE__D04_ORACLE_QUALIFIED` | yes | Lineage/no-conflation findings stand; exhaustive ordered-pair oracle is not itself current workload authority. |
| D04 | `EVIDENCE_ACCEPTED__DEFECT_CLASSIFICATION_PARTIALLY_QUALIFIED` | yes | Metric/special-state/resume defects stand; pair-completeness and pre-registration-gating defect labels require workload-law qualification. |
| D05 | `RETURN_REQUIRED__NOT_CLOSED` | no | Existing blocker remains correct, but output contract/evidence identity defects still prevent closure. |
| D06 | `RETURN_REQUIRED__CORE_RULING_RETAINED` | no | Core R1-vs-workload distinction stands, but material current V550J/shared-substrate and association-feature surfaces were missed; follow-on jurisdiction is partly wrong. |

## 3. D01 review

### Accepted

D01 correctly establishes that executable V547 performed exhaustive unordered pair search across its finite-scored non-country predictor set, while current `secondary_indicator_summary_rows` chooses a primary predictor first and searches only primary-plus-other pairs. The old all-pairs interaction-discovery geometry is therefore not preserved.

D01 also correctly establishes mathematical mutation across V547 MI, current entropy-reduction scoring, and current NMI, including the nats/bits mismatch and predictor-missingness issue.

### Parent normalization

D01's phrase `full unary response topology` is too strong for `indicator_answer_matrix`.

The current matrix preserves a **complete crosstab over the prepared frame's `response_value_normalized` categories for each emitted indicator value**, including raw and scalar-weighted cell mass/share. It does not by itself establish:

- typed DK/refusal/IAP/not-asked/inapplicable semantics;
- lawful multiselect set topology;
- routed risk-set semantics;
- survey-design weighting authority.

Use `complete prepared-frame unary crosstab` rather than `full lawful response topology` in later synthesis.

Likewise, current country-scoped execution does not mathematically reproduce V547's pooled `MI(country_code; response)` diagnostic. That historical quantity is no longer directly emitted; richer country-scoped response evidence may make it reconstructible, subject to retained substrate, but it is not identity-preserving `SUPERSEDED` computation.

No worker return is required for D01 because these are parent-level semantic precision corrections rather than failures of its central genealogy burden.

## 4. D02 review

D02 passes second review.

Its central distinction is sound: V548 is a directed majority-position-deviation search; current V550 is a greedy positive-entropy-reduction positional partition that retains only the two most frequent nonblank values and follows both. The current tree is not a lossless preservation of historical branch evidence.

The hostile XOR/parity, rare-category, truncated-path, nonpersisted-membership, overwritten-field, and misleading stop-reason findings remain technically supported.

One boundary remains explicit: D02's information-theoretic claim that a broader discovery search can be regenerated from respondent-grain response/position incidence is **not yet a physical-retention proof**. D05/D13 still own whether the actual retained production substrate is source-equivalent and replay-sufficient.

## 5. D03 review

### Accepted lineage

The no-conflation result stands:

- historical V549/V549b branch-conditioned cotravel used actual reconstructed branch membership;
- current position signature is within-question position×response association;
- current relation co-signature is within-frame feature×response association;
- current attitude cloud is same-respondent cross-question pairwise cotravel;
- historical profile-cluster/relation-vector ambition is not realized by a current equivalent.

Historical `profile_cluster_summary` and `profile_relation_vector` should be described as `INTENDED_BUT_NOT_PROVEN_REALIZED__ABSENT_CURRENT_LINEAGE`, not simply `LOST`, because D03 itself did not prove executable historical materialization of those objects.

### D04 oracle qualification

D03's D04 oracle states that every pair satisfying `anchor_eligible(A) AND feature_eligible(B)` belongs to a mandatory semantic ordered-pair set and that dual-eligible questions require both directions.

That is a useful **exhaustive-completeness test object**, but it is not independently established current **workload authority**.

D06 correctly distinguishes semantic/use eligibility from workload selection and finds no demonstrated universal mandate requiring every permitted cloud pair to be computed/materialized. Therefore:

- `allowed_as_attitude_cloud_anchor/feature` means the question is permitted for that role;
- it does not, by itself, prove that every Cartesian permitted ordered pair is required workload;
- D03's ordered-pair set may be used as the expected set **conditional on an exhaustive-cloud workload law**, but cannot itself create that law.

D07 must adjudicate the cloud workload requirement.

## 6. D04 review

D04's executable tests are valuable and mostly stand. The second pass changes the classification of two findings.

### Defects that remain accepted

- **D04-F02:** NMI divides `mutual_info_score` nats by entropy bits. This is a mathematical implementation defect.
- **D04-F03:** cloud preparation can admit nonblank special/missing/routing response states because it ignores harmonized row-level substantiveness/missingness flags. This violates the current response-semantics separation expected by the prepared substrate.
- **D04-F04:** resume does not rehydrate cross-question cloud state, so resumed execution is not equivalent to fresh execution for the algorithm's own cross-question pair formation.
- **D04-F06/F07:** empty-status typing and `mutual_information` naming ambiguity stand.
- **D04-F08–F11:** weighting, duplicate/multiselect, tie, and routed-risk-set questions remain missing authority.

### D04-F01 reclassification

Code fact: pair output is processing-order dependent and lower-triangular relative to the in-memory state.

Parent classification:

`IMPLEMENTATION_ORDER_DEPENDENCE__DEFECT_IF_EXHAUSTIVE_ORDERED_PAIR_WORKLOAD_REQUIRED`

It is not yet lawful to call every omitted reverse pair a governed semantic defect solely because D03 declared the exhaustive pair oracle. D07 must establish whether exhaustive permitted-pair computation is required, optional/on-demand, or bounded by another workload rule.

### D04-F05 reclassification

Code fact: `should_emit_cloud_tables(...)` is evaluated before `build_attitude_cloud_rows(...)`; a question gated out of cloud execution is therefore not registered in cloud state and cannot later participate as a feature.

Parent classification:

`WORKLOAD_POLICY_AND_COMPLETENESS_AMBIGUITY__NOT_PROVEN_IMPLEMENTATION_DEFECT`

A resource/cardinality gate may intentionally exclude a question from the cloud workload entirely. D06 proves that resource/workload selection is a separate authority problem. Until D07 establishes the intended gate semantics, pre-registration exclusion cannot be called a defect merely because it reduces the exhaustive-pair oracle.

D04 remains dependency-closed because no rerun is needed to preserve its empirical/code evidence; parent semantic classifications above control downstream use.

## 7. D05 review

D05 remains `RETURN_REQUIRED__NOT_CLOSED`.

The substantive fail-closed verdict `BLOCKED_MISSING_POPULATED_DATA_ACCESS` is correct. However:

1. required `RESULT.json` is absent;
2. the returned `RESULT.md` promises `AUDIT.sql` and `EXPECTED_OUTPUT_SCHEMAS.json`, but neither exists on the branch;
3. its reported attachment hashes conflict with the controlled evidence manifest at its exact base.

The controlled hashes are:

- `Rawlsing_WVS_public_schema.sql` = `2c3f4a9ebec1e6c0cf62e8827ab982e52243c5c8899c961cd0e30b489573ec76`
- `Rawlsing_WVS_authority_reconcile_schema.sql` = `57e8c58c9444be9c34df54765e1801a9819f7a15fd02ddaa9a8e194e57596877`

D05 must repair its return kit even if populated data remain unavailable. None of the substantive populated-data questions are closed.

## 8. D06 review

### Core ruling retained

D06's strongest result stands:

**Final R1 is question-relation / structural-semantic authority, not a universal V550 workload mandate.**

The distinction among:

1. R1 semantic relation authority;
2. synthesized question-use eligibility;
3. actual computation selected by hard-coded loops/resource switches;

is foundational and accepted.

### Material miss 1 — current V550/V550J shared co-execution surface exists

D06 states that no current V550J/co-execution surface was demonstrated. That is false as written.

At the audited base:

- `ddm_v550_shared_respondent_substrate.py` explicitly identifies itself as `Shared respondent-substrate helpers for V550/V550J co-execution` and declares execution contract `v550-v550j-coexecution-v1`;
- it imports `ddm_v550j_registry_contract`;
- `resolve_shared_substrate_requirements(...)` resolves bounded V550J joint-required variables from an executable joint-configuration registry;
- `build_determinicity_wave_shard_v550.py` consumes `joint_configuration_registry_path`, unions `joint_required_var_codes` with the base V550 extraction set, prefetches that union, and can write the shared respondent substrate with joint-registry/release provenance.

This does **not** prove that V550J joint analysis itself executes inside the V550 shard. The corrected ruling is:

`V550J_ANALYTIC_EXECUTION_NOT_YET_DEMONSTRATED__V550_V550J_SHARED_EXTRACTION_AND_REGISTRY_COEXECUTION_PRESENT`

D06 must trace the exact R1/question-use relationship to this shared extraction surface rather than reporting the surface absent.

### Material miss 2 — `allowed_as_association_feature` is present in current production substrate contracts

D06 says there is no demonstrated current `allowed_as_association_feature` field. At the audited base, the shared respondent-substrate contract explicitly requires `allowed_as_association_feature` and carries it through canonicalization alongside `allowed_as_attitude_cloud_feature`.

Therefore `ABSENT/NOT_DEMONSTRATED` is wrong as a surface claim. What remains unresolved is the field's **exact provenance and governing derivation** in the current preparation path. D06 must trace that provenance.

### Jurisdiction correction

D06 assigns a `workload-authority / compute-economy seam` to D10. That is not D10's charter.

- **D07** owns required/permitted/forbidden empirical workload authority, including fixed-field scans, branch/conjunction workloads, and cloud workloads.
- **D10** owns empirical-coordinate ↔ nine-stratum structural-predicate authority.
- **D14** owns measured compute/materialization cost after semantic workloads close.

D06's follow-on routing must be corrected accordingly.

### Return requirement

D06 is not dependency-closed until it returns a corrected `RESULT.md` / `RESULT.json` (and matrix if affected) that:

1. preserves the accepted Final-R1-vs-workload core distinction;
2. traces the current V550/V550J shared-extraction/registry co-execution surface;
3. traces `allowed_as_association_feature` provenance instead of declaring the field absent;
4. separates V550J shared extraction from actual joint analytic execution;
5. routes workload authority to D07, semantic coordinate→stratum mapping to D10, and measured compute to D14;
6. leaves country-scope collision/populated-impact questions explicitly dependent on D05 where live data are required.

## 9. Dependency state after review

Because D06 is now formally returned, its dependents are not unlocked merely because its core proposition is retained.

- D01: closed.
- D02: closed.
- D03: closed with oracle qualification.
- D04: closed with parent reclassification.
- D05: **not closed**.
- D06: **not closed**.
- D07: blocked by D05 + D06.
- D08: blocked by D05.
- D09: blocked by D08.
- D10: blocked by D05 + D06.
- D11: **re-blocked by D06 return**.
- D12–D15: transitively blocked.

No replacement architecture is authorized.

## 10. Controlling review summary

The first wave is not a failure. It has established several strong facts: V547 all-pairs interaction discovery was narrowed; V548's deviation-chasing capability mutated; historical branch-conditioned cotravel disappeared from the current native cloud path; current clouds are pairwise and stateful; current cloud metrics/resume/special-state handling contain real defects; and Final R1 does not itself authorize the broad V550 workload.

But Wave 1 is **not closed**.

The remaining first-wave repair is finite:

1. repair D05's blocker return kit and evidence identities;
2. return D06 for the missed V550J/shared-substrate and association-feature authority surfaces plus jurisdiction correction.

D03/D04 do not require reruns; their evidence stands under the parent qualifications in this review.
