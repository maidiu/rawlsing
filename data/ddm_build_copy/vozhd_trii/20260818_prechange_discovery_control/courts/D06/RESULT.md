# VOZHD TRII D06 — R2 FINAL R1 AUTHORITY → V550/V550J EXECUTION COURT

**Repository:** `maidiu/rawlsing`  
**Exact audited base:** `bf9a0434eb2096d5c4725cf483ec757fd319b6af`  
**Court branch:** `agent/vozhd-trii-d06-r1-v550-eligibility`  
**Write domain:** this D06 directory only. No production code or authority changed.  
**Disposition:** **R2 SUPERSEDES THE PRIOR D06 RESULT.**

## CENTRAL RULING

`CURRENTLY_NOT_DEMONSTRATED`

Final R1 is current question-relation / structural-semantic authority. It is **not demonstrated to be a universal workload authority for every current V550 computation family**.

That conclusion now rests on `AUTHORITY_TO_EXECUTION_GRAPH.csv`, not on name similarity or prose inference. The graph separates:

1. governing semantic authority;
2. permissions derived from several authorities;
3. operational resource policy;
4. implementation defaults and fixed inventories;
5. provenance-only transport;
6. unresolved edges.

The exact allowed edge types are:

- `GOVERNING AUTHORITY`
- `DERIVED PERMISSION`
- `OPERATIONAL RESOURCE POLICY`
- `IMPLEMENTATION DEFAULT`
- `PROVENANCE ONLY`
- `UNKNOWN`

`AUTHORITY_TO_COMPUTE_GATE_MATRIX.csv` is retained only as a compact subordinate view of the graph.

## R2 CORRECTIONS TO THE FIRST D06 RETURN

### 1. The V550/V550J co-execution surface was missed. That ruling is withdrawn.

The exact-base repository contains:

`data/ddm_build_copy/ddm_v550_shared_respondent_substrate.py`

Its module docstring is literally:

`Shared respondent-substrate helpers for V550/V550J co-execution.`

It defines `SHARED_SUBSTRATE_EXECUTION_CONTRACT_VERSION = "v550-v550j-coexecution-v1"`, resolves base plus registry-required J extraction, assigns `BASE_ONLY`, `JOINT_ONLY`, and `BASE_AND_JOINT` roles, validates and hashes the shared respondent substrate, and publishes a V550J-compatible prepared surface.

The prior D06 statement that no current V550J/co-execution selector or surface had been located was therefore materially false and is superseded.

### 2. `allowed_as_association_feature` was missed. That ruling is withdrawn.

`ddm_v550_shared_respondent_substrate.py` physically requires and transports `allowed_as_association_feature` in the prepared/shared respondent substrate.

`ddm_v550j_joint_patterns.py::_association_row_status()` actively reads it. After metadata / `not_direct_evidence` blocking, a row can be association-eligible when `is_substantive`, `allowed_as_association_feature`, or `allowed_as_attitude_cloud_feature` is true. Association-lane publication is then separately reconciled against `AssociationLaneRegistry` by the V550J compiler.

What remains unresolved is the authoritative **derivation/write source** that makes `allowed_as_association_feature` true upstream. The repository-wide symbol/path search and inspection of adjacent QUC, shared-substrate and V550J surfaces did not locate that derivation. Under the binding negative-proof rule this is `NOT_LOCATED`, **not `ABSENT`**.

## THE ACTUAL AUTHORITY → EXECUTION TOPOLOGY

### A. Final R1

Final R1 governs question-relation semantics at the exact source / canonical-wave / country-scope / question-or-variable resolution seam. Its principal surface contains 18,518 retained rows:

- `GOVERNED_NON_DIRECTIONAL_DISPOSITION`: 12,611
- `GOVERNED_QSMV2_RELATION_AUTHORITY`: 4,397
- `GOVERNED_ADMINISTRATIVE_DISPOSITION`: 966
- `EXCLUDED_INACTIVE_WAVE`: 259
- `GOVERNED_MANUAL_RELATION_AUTHORITY`: 173
- `FROZEN_ACCEPTED_GSS`: 52
- `BLOCKED_STRUCTURAL_MAPPING_AUTHORITY`: 41
- `BLOCKED_SOURCE_AUTHORITY`: 10
- `BLOCKED_IDENTITY_OR_AUTHORITY_JOIN`: 9

The current mapping loader is not literally R1-only: it also derives exactly 20 bounded Latinobarómetro 1995 residual rows from the hash-validated legacy calibration authority. R1 remains primary on overlap.

### B. Question-use permissions are a separate synthesis layer

`ddm_v550_authority_contract.py::derive_question_use_eligibility()` derives, among others:

- `allowed_as_demographic_predictor`
- `allowed_as_branch_splitter`
- `allowed_as_branch_position_signature`
- `allowed_as_branch_relation_cosignature`
- `allowed_as_attitude_cloud_anchor`
- `allowed_as_attitude_cloud_feature`
- `allowed_as_v551_relation_evidence`

These are not direct R1 columns. They combine structural completeness, semantic role, response/relation certification and review-state authority. `ddm_v550_question_use.py` then applies current question-relation authority to the merged qmeta.

`allowed_as_v551_relation_evidence` is especially dual-layered: QUC derives it from the combined contract, and the current R1 resolver can then directly re-resolve relation eligibility.

### C. Base V550 selection and V550J selection are not one authority

The current full-J orchestration history and exact source prove three distinct decisions:

1. **combined strict/full-J selection** — an operational acceptance-run selection that may include governed J variables outside QSM;
2. **base V550 filter** — exact membership in the QSM namespace snapshot that produced the selection;
3. **joint/shared-substrate ingress** — executable joint-configuration registry membership, including lawful `JOINT_ONLY` variables absent from the base QSM namespace.

The PG8-016 / PG8-017 / PG8-017A lineage is decisive here: using response-semantics authority as a proxy for QSM membership was itself a demonstrated runtime defect. A governed J-only variable can have governed response semantics without thereby belonging to V550's base question namespace.

Therefore a single statement such as “the question was selected” is insufficient to establish what is authorized to execute.

## COMPUTATION-FAMILY RULINGS

### Answer distributions

For a selected base V550 question, `build_distribution_tables()` executes before the false `allowed_as_response_distribution` result is used to clear/suppress outputs. The permission is therefore an output/admissibility gate in this path, not a pre-compute workload gate.

### Position indicator summary / indicator-answer matrix / outlier / secondary summaries

The runner calls these builders for selected questions without first consulting `allowed_as_demographic_predictor` or another family-granular R1 workload predicate.

`ddm_v550_branching.py` uses the fixed 12-field `INDICATOR_FIELDS` inventory. The existence of a QUC demographic-predictor permission does not make that field the workload selector for these calls.

### Recursive branch nodes

`allowed_as_branch_splitter` is real and is derived by QUC. But `branch_nodes_rows()` does not accept or read it. Recursive split candidates come from remaining fixed `INDICATOR_FIELDS`; the implementation chooses among them by entropy gain / utility and support constraints.

Thus:

`allowed_as_branch_splitter exists` **does not imply** `allowed_as_branch_splitter gates current recursive V550 split execution`.

### Position signatures / relation co-signatures / attitude clouds

These are two-gate workloads:

1. `should_emit_cloud_tables(...)` is an **operational resource policy** deciding whether cloud-family builders run;
2. the builders then consume semantic permissions such as `allowed_as_branch_position_signature`, `allowed_as_branch_relation_cosignature`, `allowed_as_attitude_cloud_anchor`, and `allowed_as_attitude_cloud_feature`.

The cloud helper `_feature_allowed(..., default=True)` also has a permissive missing-field implementation fallback. That fallback is explicitly an `IMPLEMENTATION DEFAULT`; it has no authority status.

### V551 bridge

The bridge treats current QUC fields as authority over stale copies carried on candidate artifacts. It records conflicts as stale candidate authority overridden by current QUC.

Most importantly, the constructed bridge row is returned through:

`apply_question_relation_authority(bridge_row)`

So Final R1 directly re-resolves current downstream relation admissibility **after** the upstream V550 computation has already happened. The QUC-certified active-registry-no-match preservation seam remains an alternate certified-authority path; it is not evidence that R1 universally mandated the upstream computation.

## SHARED RESPONDENT SUBSTRATE / V550J

### Selection and extraction expansion

`resolve_shared_substrate_requirements()` requires an executable registry plus the bound P3 and joint-configuration authority releases. It resolves:

- `base_var_codes`
- `joint_required_var_codes`
- `union_var_codes`
- `base_only_var_codes`
- `joint_only_var_codes`
- `overlap_var_codes`

Registry-required J variables absent from base/QSM rows are explicitly appended as `joint_only` rows into `union_question_rows`. This is a real V550J-required extraction expansion beyond base V550 question membership.

### Is the shared substrate populated in normal production?

Ruling: `CONDITIONAL_NORMAL_JOINT_COEXECUTION_PATH`.

The V550 shard runner prepares/writes it when a joint configuration registry is supplied and shared-substrate mode is enabled. The canonical joint smoke/orchestration supplies the joint registry and shared-substrate write mode before V550J. A standalone/non-joint V550 invocation need not create it.

Therefore “normally populated for configured V550/V550J joint co-execution” is demonstrated; “universally populated by every V550 run” is false.

### What the substrate physically carries

The declared logical substrate includes respondent identity, weight, question/variable identity, response values and labels, response semantic status, direction/polarity, missing/DK/refusal/IAP flags, substantive status, target and position/context metadata, source-structure metadata, `not_direct_evidence`, `allowed_as_association_feature`, `allowed_as_attitude_cloud_feature`, association lane, selection role, and joint configuration IDs.

`canonicalize_shared_respondent_substrate()` describes itself as returning a V550J-compatible substrate **without reharmonizing rows**. Missing required columns are defaulted. It preserves existing extra columns by reindexing required columns first and then the original frame columns.

This means the co-execution transport is rich, but schema breadth is not empirical completeness proof.

### Are joint-only variables semantically prepared identically to base variables?

Ruling: `NOT_DEMONSTRATED`.

They can be admitted to extraction through the joint registry even when absent from QSM. The shared-substrate canonicalizer does not itself harmonize semantics; it can fill semantic fields with defaults. Runtime history also explicitly distinguished joint-only registry admission from base/QSM metadata admission.

Response-level harmonization may occur upstream, but identical QSM/qmeta semantic preparation for every joint-only variable is not established by this court.

### Duplicate-scalar validation risk

The shared substrate defines a substantive scalar duplicate key as:

`source + canonical_wave + country + respondent + var_code`.

Any duplicate is rejected by default as `unauthorized_duplicate_scalar_response_keys`.

That is compatible with a scalar-single-response model. It can reject a legitimate multiselect/repeated-answer structure if that structure is physically represented as multiple substantive rows for the same respondent×variable key. This is a demonstrated implementation-policy risk, not proof that a populated production run has already lost such rows.

### Hash / replay equivalence

`logical_shared_substrate_hash()` hashes sorted row hashes over `SHARED_SUBSTRATE_REQUIRED_COLUMNS`, together with schema and execution-contract versions. Row order therefore does not affect the logical hash; duplicate-row multiplicity does. The manifest also stores the serialized Parquet SHA-256 and reload validation.

This is strong integrity for the declared logical surface. It does **not** establish logical equivalence for arbitrary additional columns retained on the physical frame, because those extras are outside `LOGICAL_CONTENT_COLUMNS`.

Accordingly D06 does not elevate the hash into a proof that every empirically relevant fact needed by arbitrary future replay is retained.

### Does V550J consume the shared substrate directly?

Yes, in the prepared-required/no-database path.

`compile_v550j_joint_response_patterns.py` reads the explicit prepared Parquet and manifest, validates the shared-substrate contract and logical hash, and requires `prepared_required` when database access is forbidden. The explicit prepared path uses those rows directly rather than calling the forensic `_harmonize_question_frame` path.

Other V550J modes can independently query/re-harmonize. Direct shared-substrate consumption and forensic fallback are therefore distinct execution modes.

## ASSOCIATION AUTHORITY

`allowed_as_association_feature` is now proven to be both physically transported and read during V550J association eligibility.

However, current evidence does not locate its upstream authoritative derivation. Meanwhile association **publication** is separately governed: `_enforce_governed_association_lane_authority()` requires registry classification and strips nonpublishable rows from the main association index.

So at least three association layers must not be collapsed:

1. upstream association-feature permission — source `NOT_LOCATED`;
2. candidate eligibility using that permission plus substantive/cloud status and blocking rules;
3. governed association-lane publication.

## NEGATIVE-PROOF LEDGER

Binding law for this R2 result:

> `ABSENT` requires repository-wide symbol/path search plus inspection of semantically adjacent surfaces. Otherwise the ruling is `NOT_LOCATED`.

The GitHub file-search interface produced false negatives for surfaces independently proven to exist, including the V550/V550J machinery. Search no-hit is therefore not sufficient negative evidence.

This court issues **no material `ABSENT` ruling** for the missing workload authorities.

Current `NOT_LOCATED` items include:

- the authoritative derivation/write source for `allowed_as_association_feature`;
- a universal family-granular authority that mandates all selected-question × fixed-indicator V550 work;
- a universal R1 rule that mandates recursive branch exploration depth/conjunctions;
- a universal R1 rule that mandates cloud computation whenever semantic relation authority exists.

## RETENTION / EMPIRICAL-COMPLETENESS BOUNDARY

D06 establishes the **authority and execution graph** of the shared respondent substrate. It does not prove the populated data are complete enough to reconstruct all unary, pairwise, arbitrary conjunction, joint-pattern, multiselect, or repeated-measure empirical facts.

Those empirical/physical claims require D05/D13 populated-substrate and retention evidence. D06 therefore records:

- unary replay completeness: `NOT_DEMONSTRATED_BY_D06`;
- pairwise replay completeness: `NOT_DEMONSTRATED_BY_D06`;
- arbitrary joint replay completeness: `NOT_DEMONSTRATED_BY_D06`;
- preservation of repeated/multiselect respondent structure: `AT_RISK_UNDER_SCALAR_DUPLICATE_POLICY__EMPIRICAL_LOSS_NOT_PROVEN`.

## FINAL D06 R2 DISPOSITION

Final R1 remains sovereign where current relation meaning must be resolved. It can affect whether a question is admissible as relation evidence, relation co-signature material, or an attitude-cloud anchor/feature, and it is directly re-applied at the V551 bridge.

But current V550/V550J execution is governed by a **plural authority/execution topology**:

- R1 relation authority;
- QUC-derived multi-authority permissions;
- exact QSM base membership;
- independent executable joint-configuration authority;
- explicit base/joint/overlap unioning for shared extraction;
- resource-profile workload policy;
- fixed implementation inventories and defaults;
- later V550J lane/publication authority;
- downstream R1 re-resolution.

Therefore the proposition that “Final R1 authorizes all current V550 work performed for every selected question” remains **CURRENTLY_NOT_DEMONSTRATED**.

The materially stronger positive finding is that current Rawlsing already possesses a deliberate V550/V550J shared respondent-grain co-execution substrate whose selection geometry and authority boundaries are substantially richer than the first D06 return reported.
