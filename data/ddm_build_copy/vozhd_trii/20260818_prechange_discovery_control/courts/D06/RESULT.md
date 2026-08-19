# D06 — Final R1 Question-Relation Authority → Current V550 Eligibility Court

**Repository:** `maidiu/rawlsing`  
**Audited base:** `bf9a0434eb2096d5c4725cf483ec757fd319b6af`  
**Current-production anchor represented at this base:** Final R1 merge lineage beginning at `0777a34e50221bde6801dbaca26c058a7350c9e8`  
**Court branch:** `agent/vozhd-trii-d06-r1-v550-eligibility`  
**Scope:** authority provenance and current compute eligibility only. No production code or authority was changed.

## 1. Verdict

### Primary ruling

Final R1 is a **question-relation / structural-semantic authority**, not a universal V550 workload authority.

Current V550 has three materially different kinds of gates which must not be collapsed:

1. **Question-relation semantic authority.** Final R1 determines whether a source/wave/country/question relation interpretation is governed, non-directional, administrative, excluded, or blocked, and for governed relational rows supplies the authorized structural coordinates and provenance.
2. **Synthesized question-use eligibility.** `ddm_v550_authority_contract.py` derives high-risk `allowed_as_*` permissions from multiple authorities: semantic-role certification, response-semantics certification, directionality/applicability, structural-mapping completeness, review state, temporal/runtime authority where relevant. Most of those booleans are not columns supplied by Final R1.
3. **Actual computational workload selection.** Several expensive V550 families are selected by implementation loops, fixed indicator inventories, data availability, and cloud resource switches. They are not selected by Final R1 and, for the core branching/conditional families, do not consult the corresponding `allowed_as_*` permission before computation.

Therefore the answer to the central question is family-specific. A question can be computed empirically in V550 even when its Final R1 structural/relation use is blocked, and can later be rejected for V551 relation evidence. Conversely, a Final R1 governed relation row does not by itself authorize computing every demographic conditional, recursive conjunction, or cloud.

### R11 proposition re-test

**CURRENTLY_NOT_DEMONSTRATED.**

At current main, the inspected authority surface still does not demonstrate a universal authority mandate of the form “for every selected question, compute every one of the 12 demographic fields and recursive conjunctions.” Current runtime behavior broadly performs that work, but the causal source of that behavior is hard-coded analytic enumeration in `ddm_v550_branching.py` plus unconditional calls in `build_determinicity_wave_shard_v550.py`, not a demonstrated authority grant.

This is an absence-of-demonstrated-authority ruling, not proof that no such mandate could exist anywhere outside the inspected governing surface.

---

## 2. R1 authority-surface taxonomy

Final R1 contains 18,518 retained question-relation rows. `AUTHORITY_STATUS_COUNTS_FINAL_R1.csv` partitions them as:

| authority_status | rows | current meaning |
|---|---:|---|
| `GOVERNED_NON_DIRECTIONAL_DISPOSITION` | 12,611 | governed non-directional/context disposition; no relation-evidence coordinates |
| `GOVERNED_QSMV2_RELATION_AUTHORITY` | 4,397 | governed QSMv2 directional relation authority |
| `GOVERNED_ADMINISTRATIVE_DISPOSITION` | 966 | governed administrative/non-evidentiary disposition |
| `EXCLUDED_INACTIVE_WAVE` | 259 | excluded authority scope |
| `GOVERNED_MANUAL_RELATION_AUTHORITY` | 173 | governed manual directional relation authority |
| `FROZEN_ACCEPTED_GSS` | 52 | frozen accepted directional GSS authority |
| `BLOCKED_STRUCTURAL_MAPPING_AUTHORITY` | 41 | semantic unit/implementation retained but required structural mapping is fail-closed |
| `BLOCKED_SOURCE_AUTHORITY` | 10 | source authority unresolved; fail-closed |
| `BLOCKED_IDENTITY_OR_AUTHORITY_JOIN` | 9 | identity/authority join unresolved; fail-closed |

The Final R1 package explicitly governs a relation/structural mapping jurisdiction. It adds four applied-mapping fields—`canonical_wave`, `country_code_scope`, `authority_status`, `authority_rule_id`—and fail-closes six structural coordinates where authority is insufficient. It does **not** declare that every governed row must receive every V550 diagnostic or conditional computation.

The authority categories are separate:

- **Canonical question identity:** source/wave/country/question identifiers and R1 join identity.
- **Source/wave/country scope:** `canonical_wave`, `country_code_scope`, status and rule provenance.
- **Structural coordinates:** relation family/side and other governed structural coordinate fields.
- **Relation authority / directionality:** directional relation statuses versus non-directional/admin/blocked dispositions.
- **Semantic role:** compiled at runtime from R1 plus question-use/response authorities; not reducible to the R1 status string.
- **Evidence admissibility:** high-risk downstream eligibility is derived by the authority contract and rechecked in the V551 bridge.
- **Computation eligibility:** only some families consult synthesized eligibility.
- **Workload selection:** for major branching families, implementation enumeration rather than authority.

---

## 3. Runtime loading path

### 3.1 Final R1 loader

`ddm_v550_question_relation_authority.py` is the current question-level relation authority resolver.

Its default active authority is:

`authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv`

with `FULL_AUTHORITY_VERSION = qsm_full_question_relation_authority_r1_20260814`.

The module validates exact Final R1 cardinality and governed counts. The exact resolver key includes normalized:

`source_family + canonical_wave + country_code_scope + (var_code/question_id)`.

For a matched row, the resolver distinguishes governed directional, governed non-directional/context, administrative, excluded, and blocked dispositions. Directional governed statuses populate structural coordinates and current/V551 relation-evidence flags; non-directional and blocked resolutions clear relation-evidence coordinates/flags rather than inheriting stale directional meaning.

### 3.2 Active-path override

The Final R1 path is the default, but `active_authority_path()` remains overrideable through environment/configuration (`RAWLSING_QUESTION_RELATION_AUTHORITY_PATH` and authority-root resolution). This is a live fallback surface. It is not evidence that the normal current run uses stale authority, but Final R1 is not an unoverrideable singleton.

### 3.3 Legacy 20-row residual

`derive_legacy_latinobarometro_1995_residual()` deliberately loads the older 35-wave calibration registry to recover exactly 20 Latinobarómetro 1995 rows absent from Final R1. `apply_postgres_facet_ready_substrate.py` appends those residuals to the applied mapping substrate.

Thus “current authority loading” is not literally “R1 and nothing else.” The residual is explicit and bounded rather than an accidental whole-registry fallback.

### 3.4 Postgres/facet-ready substrate

`apply_postgres_facet_ready_substrate.py` persists Final R1 mapping metadata, including the four R1 fields, into `question_structural_mapping`.

However, the facet-ready response-view join to question mapping is materially weaker than the R1 resolver key. It joins by source, variable, and compatible raw wave. It does **not** use `country_code_scope` as a join predicate. The mapping table primary key is likewise source/wave/var oriented rather than R1 country-scope oriented.

Therefore country-scoped authority is preserved as metadata but is not universally enforced by this substrate join.

### 3.5 Shared cache

`ddm_v550_shared_cache.py` caches question-structural mappings by request/query signature. The cache key does not contain an R1 content hash or authority version. A process can therefore retain mapping results across an underlying database authority change until cache invalidation/reset. This is a stale-capability surface, not proof that a stale cache was present in the audited run.

### 3.6 Repository question list

`build_determinicity_repository_v550.py` constructs the V550 question list from scope plus question mapping. The list merge is source/wave oriented and does not carry all of:

- `authority_status`
- `authority_rule_id`
- `country_code_scope`

into the question-list gate.

The question list therefore does not implement “R1 authority_status permits computation” as a universal selection predicate. Country-specific empirical response retrieval happens later, but R1 country scope is not the question-list admission key.

### 3.7 qmeta / question-use compilation

`ddm_v550_question_use.py` combines mapping metadata with independent question-use authorities and overlays, then calls `derive_question_use_eligibility()` in `ddm_v550_authority_contract.py`.

This is the principal compiler for the `allowed_as_*` permissions. Those permissions are derived, not copied wholesale from Final R1.

### 3.8 V551 bridge re-resolution

`ddm_v550_bridge.py` re-applies `apply_question_relation_authority()` to bridge candidates **after** V550 artifacts already exist. This is a decisive provenance fact: Final R1 can reject downstream relation evidence after an upstream empirical workload has already been executed.

---

## 4. Per-compute-family eligibility provenance

The companion `AUTHORITY_TO_COMPUTE_GATE_MATRIX.csv` is the concise provenance graph. The controlling rulings are:

### `answer_distribution`

**Workload source:** selected V550 question + empirical response rows.  
**Semantic gate:** `allowed_as_response_distribution`.  
**Actual order:** distribution computation occurs before the gate is applied; if the gate is false, emitted rows are cleared/suppressed afterward.  
**R1 role:** indirect input into qmeta semantic/structural classification, not the workload trigger.

Graph:

`R1 + response/question-use authorities → qmeta → allowed_as_response_distribution → post-compute retain/suppress → answer_distribution`

### `country_answer_distribution`

Same authority structure as `answer_distribution`: country-specific response data governs the empirical rows; the `allowed_as_response_distribution` gate controls retention, not initial execution.

### `position_distribution`

This family is question-independent.

`respondent scope + fixed position fields → wave/country aggregation → position_distribution`

There is no question-relation R1 predicate here.

### `position_indicator_summary`

`selected question + answer-bearing respondents + fixed INDICATOR_FIELDS → indicator summary computation → artifact`

No `allowed_as_demographic_predictor` check precedes or wraps the computation. The authority contract can derive that field, but the branching implementation does not consume it as its compute gate.

### `indicator_answer_matrix`

`selected question + answer-bearing respondents + fixed INDICATOR_FIELDS → cross-tab matrix → artifact`

No R1 status or synthesized high-risk permission is the workload selector.

### `outlier_cohort_summary`

`selected question + prepared branch frame → cohort discovery → artifact`

No Final R1 workload permission is consulted.

### `secondary_indicator_summary`

`selected question + branch frame → secondary/pair indicator analysis → artifact`

No Final R1 workload permission is consulted.

### `recursive_branch_nodes`

`selected question + branch frame + fixed INDICATOR_FIELDS → recursive split search → recursive_branch_nodes`

The authority contract derives `allowed_as_branch_splitter`, but `ddm_v550_branching.py` does not use that field to select split variables, and the wave-shard builder invokes recursive branching without first requiring it. The current recursive workload is therefore implementation-authorized in practice, not authority-authorized by Final R1.

### `branch_position_signature`

This family has a real semantic gate.

`R1 structural mapping + independent question-use authorities → qmeta → allowed_as_branch_position_signature → candidate POSITION_COORDINATE feature check → signature emission`

It also has a separate workload/operational gate: cloud tables must be enabled by `should_emit_cloud_tables`. Semantic eligibility alone does not force execution.

### `branch_relation_co_signature`

`R1 relation authority + response semantics + structural/review authorities → qmeta → allowed_as_branch_relation_cosignature → relation-feature candidate check → co-signature emission`

Final R1 is relevant but not sufficient by itself.

### `question_response_attitude_cloud`

Both anchor and feature are gated:

`R1 relation authority + independent certification → allowed_as_attitude_cloud_anchor/feature → current/structural/relation checks → attitude-cloud rows`

Again, a separate cloud resource/size gate decides whether the cloud family is executed at all.

### V551 bridge emission

This is where Final R1 is most directly operative.

`V550 candidate artifact → apply_question_relation_authority(source,wave,country,question) → current_directional_atom_eligible / allowed_as_v551_relation_evidence + other bridge checks → emit/skip V551 relation evidence`

R1 therefore governs downstream semantic admissibility, not retroactive authorization of the already-spent upstream V550 workload.

### V550J co-execution

No current production `V550J` module, co-execution selector, or R1→V550J gate was located in the audited current production surface. Repository searches for `V550J`, `550J`, and co-execution terminology did not establish such a current path. This court therefore records **NOT DEMONSTRATED / NO CURRENT SURFACE LOCATED** and does not infer an effect from V551J, cloud, or bridge machinery.

---

## 5. Default / fallback / overlay audit

### Requested eligibility fields

| field | provenance ruling |
|---|---|
| `allowed_as_demographic_predictor` | **Synthesized.** Derived in `ddm_v550_authority_contract.py`; requires a certified `POSITION_COORDINATE`, certified semantic authority, sufficiently complete structural mapping, and no blocking review state. Not an R1 column. |
| `allowed_as_branch_splitter` | **Synthesized.** Derived by authority contract from certified relation/position/context role plus complete structural mapping and review state. Not an R1 column. Current recursive branch computation does not consult it. |
| `allowed_as_branch_position_signature` | **Synthesized.** Effectively tied to demographic-predictor eligibility; consumed by cloud/signature code. |
| `allowed_as_branch_relation_cosignature` | **Synthesized.** Tied to V551-grade relation evidence eligibility; R1 relation authority is one necessary input on matched rows, not the entire grant. |
| `allowed_as_attitude_cloud_anchor` | **Synthesized.** V551-grade relation evidence eligibility; consumed by cloud code. |
| `allowed_as_attitude_cloud_feature` | **Synthesized.** Same high-risk relation-evidence authority family; consumed by cloud code. |
| `allowed_as_association_feature` | **Absent/not demonstrated.** No active current field/gate by this name was located. Do not equate it with attitude-cloud feature eligibility. |
| `allowed_as_v551_relation_evidence` | **Dual provenance.** Final R1 directional resolution emits/overwrites this relation-level permission; the question-use authority contract also synthesizes the high-risk permission from multiple certifications. Bridge re-resolution makes Final R1 direct again. |
| `is_substantive` | **Response-option semantics, not Final R1 question authority.** Its jurisdiction is response relation/category semantics in the facet-ready response substrate/response-relation loader. It is not a question-level Final R1 workload grant. |
| `not_direct_evidence` | **Artifact annotation.** Cloud/signature diagnostic outputs mark derived associations as not direct evidence. This is an epistemic/admissibility annotation, not an R1 source permission. |
| `position_conditioning` | **Independent question-use/position-conditioning overlay.** Absent from Final R1. |
| `position_modifiers` | **Independent question-use/position-conditioning overlay.** Absent from Final R1. |
| `conditional_strata_weights` | **Independent question-use/position-conditioning overlay.** Absent from Final R1. |

### QUC-preservation fallback

`apply_question_relation_authority()` contains a narrow but important no-match fallback: if the active registry has no matching row but incoming qmeta is already QUC-certified as complete, directional relation evidence, it can preserve those high-risk QUC fields under a `QUC_AUTHORITY_PRESERVED_ACTIVE_REGISTRY_NO_MATCH` resolution.

This is not Final R1 authorization. It is an alternate certified-authority preservation seam and must remain distinguishable in provenance.

### Cloud default

`ddm_v550_clouds.py` uses a contract helper whose missing/blank-field default is permissive (`default=True`) unless the caller supplies otherwise. Under the normal current qmeta pipeline the expected contract fields are populated, but the helper itself is a permissive fallback surface. Missing contract metadata must not be described as equivalent to an explicit Final R1 grant.

---

## 6. Blocked-row behavior

### `BLOCKED_STRUCTURAL_MAPPING_AUTHORITY`

Final R1 correctly fail-closes the unresolved structural coordinates. In the R1 resolver / bridge path, these rows do not become current directional V551 relation evidence.

But this status does **not** universally prevent V550 empirical computation. Because repository question selection is not an `authority_status` gate and core branch families run for selected questions, a blocked mapping row may still receive answer distributions and demographic diagnostic/branch computations if empirical response data are available.

Ruling: **empirical computation can occur while structural/relation use is blocked.**

### `BLOCKED_SOURCE_AUTHORITY`

Same workload distinction. R1 semantic/structural use is fail-closed at the resolver, but `authority_status` is not a universal pre-compute predicate in the repository/wave-shard loop.

Ruling: **not proven excluded from all V550 computation; fail-closed for governed structural/relation evidence.**

### `BLOCKED_IDENTITY_OR_AUTHORITY_JOIN`

Again, the R1 resolver fails closed for relation authority. Upstream V550 question-list admission is not universally keyed to this status.

Ruling: **possible empirical compute / blocked governed use; family-specific rather than globally excluded.**

### `EXCLUDED_INACTIVE_WAVE`

`ddm_v550_question_relation_authority.active_closed_35_waves()` excludes this class, including the Asian Barometer W6 exclusion. But the V550 repository builder does not use Final R1 `authority_status` as its universal question/workload predicate. Any effective wave exclusion can therefore also come from itinerary/source-scope authority rather than from the R1 row itself.

Ruling: **R1 exclusion is authoritative in R1 resolver scope; direct universal V550 workload exclusion by that status is not demonstrated.**

### Inconsistency across families

The word “inconsistent” here is descriptive, not necessarily a bug finding:

- core empirical/branch diagnostics: broadly compute from selected empirical data;
- high-risk cloud/signature uses: consult synthesized contract gates;
- V551 bridge: re-resolves Final R1 and fails closed for relation evidence.

The current machine deliberately or incidentally separates discovery computation from semantic admissibility.

---

## 7. Canonical-wave / country-scope behavior

### Resolver path: strong

The Final R1 resolver key uses canonical wave and country scope. On this path, the authority can distinguish otherwise similar source/question rows by scope and can fail closed on missing/ambiguous matches.

### Postgres/facet-ready mapping path: weaker

The question mapping / facet-ready join is source + variable + compatible wave and does not enforce R1 `country_code_scope`. `canonical_wave`, `country_code_scope`, `authority_status`, and `authority_rule_id` are available as persisted metadata, but not all are join predicates.

### V550 question-list path: weaker

The repository question-list merge is source/wave oriented. It does not make `authority_status` or `authority_rule_id` a global admission predicate and does not use R1 country scope as the fundamental question-list join.

### Empirical response retrieval: country-specific

Once a question is being processed, response retrieval is scoped by the question run’s source/wave/country/variable identity. Thus empirical rows themselves do not become globally cross-country; the leakage risk is specifically **authority metadata/mapping selection across country scope**, not necessarily respondent-row mixing.

### Ruling

`canonical_wave`, `country_code_scope`, `authority_status`, and `authority_rule_id` **do alter behavior where the Final R1 resolver is actually invoked**, especially the V551 bridge. They do **not** uniformly govern V550 computation selection. Therefore they do not constitute a machine-wide prevention of cross-scope authority leakage.

---

## 8. V551 bridge eligibility

The bridge is the clearest current authority boundary.

For a candidate V550-derived relation row:

1. identify source/wave/country/question;
2. re-run current question-relation authority resolution;
3. copy/clear R1 structural and directional fields according to the resolution;
4. require current directional / V551 relation-evidence eligibility and the bridge’s other authority checks;
5. emit only admissible V551 relation evidence.

Blocked, excluded, missing, or ambiguous R1 relation authority therefore prevents ordinary R1-backed bridge admission even if V550 previously created demographic summaries, branch nodes, or other discovery artifacts for the question.

The exception that must stay separately typed is the QUC-preservation no-match fallback described above.

---

## 9. Workload-authority ruling

Final R1 answers questions of the form:

> May this source/wave/country/question carry this governed relation or structural meaning, with these coordinates and this authority provenance?

It does **not** by itself answer:

> Compute every demographic conditional for this question.

It does **not** by itself answer:

> Search all 12 indicators for recursive splits and conjunctions.

It does **not** by itself answer:

> Execute attitude-cloud work for this question.

For cloud/signature families, actual execution is the conjunction of a semantic eligibility contract and an operational cloud-selection switch. For core determinicity/branching families, actual execution is driven by selected question/data loops and fixed indicator enumeration.

The current machine therefore contains **semantic authority**, **use authority**, and **workload implementation policy** as distinct layers. No inspected current authority file closes the third layer into a universal governed workload policy.

---

## 10. Comparison with frozen VT3 R11 / R09

### R11

Frozen R11 found that broad all-question × 12-field demographic work was implemented but that no universal authority mandate for that workload had been demonstrated.

Current-main re-test: **the implementation claim survives and is stronger in provenance, while the authority-mandate claim remains not demonstrated.** Final R1 materially improves question-relation authority and current loading, but does not convert the fixed V550 branching inventory into an authority-issued workload mandate.

### R09

Frozen R09 treated position-conditioned meaning and actor binding as an authority problem and warned against inferring generated-position authority from shared coordinate names.

Current Final R1 does not erase that distinction. R1 governs question-relation structural coordinates; it does not authorize actor binding merely because a coordinate name resembles a V3 position field, and it does not supply `position_conditioning`, `position_modifiers`, or `conditional_strata_weights`.

Current R1 therefore supersedes frozen implementation details where loading changed, but **does not supersede the semantic separation R09 was protecting**.

---

## 11. Missing authority

The current inspected surface lacks a demonstrated authority object that says, at family granularity:

- which questions should receive `position_indicator_summary`;
- which structural/position fields may be searched for each question as empirical predictors;
- which questions may receive `indicator_answer_matrix`;
- which questions may receive outlier-cohort search;
- which questions may receive secondary-indicator pair search;
- which questions may receive recursive branch generation;
- which branch depths/conjunctions are authorized as necessary workload;
- which cloud computations are semantically necessary rather than merely permitted;
- whether any universal all-question × 12-field computation is required at all.

There is also no demonstrated current `allowed_as_association_feature` field and no demonstrated current V550J co-execution authority surface.

This court does not create those authorities.

---

## 12. Exact dependencies opened for D07 / D10 / D11

### D07

Open the **scope-enforcement seam**:

1. determine whether any country-scoped Final R1 rows collide or become ambiguous when reduced to `question_structural_mapping`'s source/wave/var grain;
2. determine empirically whether the facet-ready join can attach a mapping authorized for one `country_code_scope` to responses from another;
3. distinguish metadata leakage from actual respondent-row leakage;
4. test whether cache reuse can preserve a pre-R1 or alternate mapping after authority changes.

### D10

Open the **workload-authority / compute-economy seam**:

1. classify each unconditional branching call as terminally necessary, discovery-only, diagnostic, or stranded;
2. determine whether the 12-field `INDICATOR_FIELDS` inventory has any governing authority outside the implementation;
3. measure compute/cardinality attributable to question families that later fail high-risk semantic gates;
4. determine the minimum authority object needed to distinguish “permitted semantic use” from “required computation” without designing the replacement here.

### D11

Open the **downstream admissibility / preservation seam**:

1. trace whether V551/V551J/V552+ can consume any V550 diagnostic family without the bridge’s Final R1 re-resolution;
2. determine whether the QUC-preservation no-match fallback can admit relation evidence not represented in Final R1 and under exactly which certified authority;
3. test whether preserving raw/conditional empirical substrate is sufficient to reconstruct needed downstream facts without preserving all current diagnostic artifacts;
4. locate any actual current joint/co-execution surface that might correspond to the requested “V550J” concept; none was demonstrated in this D06 surface.

---

## Provenance graph summary

```text
Final R1 row
  ├─ exact resolver key: source + canonical_wave + country_code_scope + question
  │    ├─ governed directional → structural coordinates + current relation eligibility
  │    ├─ governed non-directional/admin → relation coordinates cleared
  │    └─ blocked/excluded/missing/ambiguous → fail-closed relation use
  │
  ├─ Postgres question_structural_mapping
  │    └─ facet-ready join: source + var + compatible raw wave
  │         [country_code_scope is metadata, not universal join predicate]
  │
  └─ V550 qmeta
       ├─ independent question-use / response / mapping / review authorities
       │    └─ ddm_v550_authority_contract.py
       │         ├─ allowed_as_demographic_predictor
       │         ├─ allowed_as_branch_splitter
       │         ├─ allowed_as_branch_position_signature
       │         ├─ allowed_as_branch_relation_cosignature
       │         ├─ allowed_as_attitude_cloud_anchor/feature
       │         └─ allowed_as_v551_relation_evidence
       │
       ├─ core branch workload
       │    └─ selected question + fixed 12 indicators
       │         [corresponding high-risk gates generally NOT consulted]
       │
       ├─ cloud/signature workload
       │    └─ operational should_emit_cloud_tables
       │         + synthesized semantic gates
       │
       └─ V551 bridge
            └─ re-apply Final R1 resolver
                 → emit/skip downstream relation evidence
```

## Final court answer

For any V550 computation, “why was this question allowed?” must be answered with two separate sentences:

1. **Why did the runtime execute it?** — usually because the question entered the V550 source/wave/country question loop, empirical rows existed, and that compute family was unconditionally enumerated or operationally enabled.
2. **Why may its result carry a particular semantic meaning downstream?** — because Final R1 and/or independent certified question-use/response authorities produced the relevant qmeta permission and, for V551 relation evidence, the bridge re-resolved current Final R1 fail-closed.

Where those two sentences are collapsed into one, current provenance is misstated.
